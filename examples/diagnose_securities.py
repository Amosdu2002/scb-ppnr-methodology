"""Securities-loader diagnostic — classifies every issue instead of stopping.

    PYTHONPATH=src python3 examples/diagnose_securities.py --config config/local/company.toml

Walks the same parsing as load_securities_inputs but never raises on data
issues: every security is classified into short ISSUE CODES, and the final
"SUMMARY TO RELAY" block contains ONLY codes and counts — no identifiers, no
amounts — so it can be copied out of a restricted environment verbatim.
Detailed lines above it (masked IDs; cell blank/zero states, never values) are
for local eyes only.

Issue codes:
  COLMAP-MISSING:<MDRM>   expected positions column not found in the MDRM header row
  ENRICH-UNMATCHED        no enrichment row for the security's identifier
  CATEGORY-UNMAPPED:<c>   security_description_1 not in the PID-SEC-5 map (category name is Fed vocabulary — safe)
  EQ-OOS-SKIP             equity intent / out-of-scope category (excluded by design)
  RATE-TYPE-UNKNOWN       enrichment rate-type value not FIXED/FLOATING/ZERO COUPON
  WAL-NONPOS              non-positive WAL (parked skip)
  SEC7-WAL-MATURITY       Agency MBS maturity date missing -> WAL used (PID-SEC-7, informational)
  S3-PROXY-OK             PID-SEC-3 trigger fired, price present -> AC proxied (works)
  S3-STOP[<legs>]         PID-SEC-3 trigger fired, AC missing/zero AND price blank -> the hard stop
                          legs: MAT (maturity missing), BY0 (book yield missing/zero), AC0 (AC missing/zero)
  OK                      loads cleanly
"""

from __future__ import annotations

import argparse
from collections import Counter

from scb_ppnr.ingestion import load_config
from scb_ppnr.ingestion.securities_loader import (
    _POSITIONS_MDRM,
    _RATE_TYPE_MAP,
    _REQUIRED_MDRM,
    _blank,
    _enrichment_map,
    _load_workbook,
    _parse_date,
    _positions_rows,
    _prepayment_map,
    _sheet,
)
from scb_ppnr.interest_income import OUT_OF_SCOPE, ValidationFailure, assign_model
from scb_ppnr.interest_income.securities_schemas import CATEGORY_MODEL_MAP


def _mask(identifier: str) -> str:
    text = str(identifier)
    return text if len(text) <= 4 else f"{text[:2]}***{text[-2:]}"


def _state(value: object) -> str:
    """Relayable cell state: EMPTY / ZERO / NUMBER / TEXT — never the value."""
    if _blank(value):
        return "EMPTY"
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return "ZERO" if float(value) == 0.0 else "NUMBER"
    try:
        return "ZERO" if float(str(value).replace(",", "")) == 0.0 else "NUMBER"
    except ValueError:
        return "TEXT"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True)
    parser.add_argument("--detail", type=int, default=10, help="how many problem securities to detail (local only)")
    args = parser.parse_args()

    config = load_config(args.config)
    if config.firm_data is None or config.firm_data.securities is None:
        raise SystemExit("config has no [firm_data.securities] section")
    sc = config.firm_data.securities
    path = config.resolve(sc.workbook)
    workbook = _load_workbook(path)

    relay: list[str] = []
    try:
        # ---- 1. Column map --------------------------------------------------
        records, columns, header_notes = _positions_rows(_sheet(workbook, sc.positions_sheet, path), path, sc.price_mdrm)
        print(f"positions sheet {sc.positions_sheet!r}: {len(records)} data rows")
        for note in header_notes:
            print(f"header note: {note}")
        print("column map (field <- MDRM -> found?):")
        checks = {**_POSITIONS_MDRM, sc.price_mdrm: "price"}
        for mdrm, field in checks.items():
            found = field in columns
            marker = "" if found else "   <-- MISSING"
            print(f"  {field:24s} <- {mdrm:10s} {'found' if found else 'NOT FOUND'}{marker}")
            if not found:
                required = " (REQUIRED)" if mdrm in _REQUIRED_MDRM else ""
                relay.append(f"COLMAP-MISSING:{mdrm}{required}")
        # MDRM codes are regulatory identifiers — safe to relay. This shows what the
        # header row actually carries (e.g., which code the price column really has).
        worksheet = _sheet(workbook, sc.positions_sheet, path)
        for row in worksheet.iter_rows(values_only=True):
            cells = [str(c).strip() for c in row if c is not None and str(c).strip()]
            if "CQSCP084" in cells:
                relay.append("HEADER-CODES: " + " | ".join(cells))
                break

        # ---- 2. Enrichment + prepayment ------------------------------------
        enrichment: dict[str, dict[str, object]] = {}
        for spec in sc.enrichment:
            tab = _enrichment_map(workbook, spec, path)
            print(f"enrichment tab {spec.sheet!r}: {len(tab)} keyed rows")
            for key, fields in tab.items():
                enrichment.setdefault(key, fields)
        prepay_warnings: list[str] = []
        prepayment: dict[str, dict[int, float]] = {}
        if sc.prepayment_sheet is not None:
            prepayment = _prepayment_map(_sheet(workbook, sc.prepayment_sheet, path), path, sc.money_scale, prepay_warnings)
            skipped = sum("PQ1 face is 0" in w for w in prepay_warnings)
            print(f"prepayment sheet: {len(prepayment)} usable rows, {skipped} skipped (PQ1=0/blank)")
            relay.append(f"PREPAY-ROWS:{len(prepayment)} PREPAY-SKIPPED:{skipped}")
    finally:
        workbook.close()

    report_date = None
    if records and "report_date" in records[0] and not _blank(records[0].get("report_date")):
        report_date = _parse_date(records[0]["report_date"], context="D_DT")

    # ---- 3. Per-security classification ------------------------------------
    codes: Counter[str] = Counter()
    details: list[str] = []
    unknown_rate_types: Counter[str] = Counter()      # distinct labels — safe to relay
    identifier_rows: Counter[str] = Counter()
    intent_counts: Counter[str] = Counter()
    for index, record in enumerate(records, start=1):
        sid = str(record.get("identifier_value", "")).strip()
        identifier_rows[sid] += 1
        intent_counts["" if _blank(record.get("accounting_intent")) else str(record["accounting_intent"]).strip().upper()] += 1
        category = "" if _blank(record.get("security_description_1")) else str(record["security_description_1"]).strip()

        try:
            model, agency = assign_model(category) if category else (None, False)
        except ValidationFailure:
            codes[f"CATEGORY-UNMAPPED:{category}"] += 1
            continue
        intent = "" if _blank(record.get("accounting_intent")) else str(record["accounting_intent"]).strip().upper()
        if model == OUT_OF_SCOPE or intent == "EQ":
            codes["EQ-OOS-SKIP"] += 1
            continue

        fields = enrichment.get(sid)
        if fields is None:
            codes["ENRICH-UNMATCHED"] += 1
            details.append(f"  #{index} {_mask(sid)} [{category}]: no enrichment match")
            continue

        rate_raw = "" if _blank(fields.get("rate_type")) else str(fields["rate_type"]).strip().upper()
        if rate_raw not in _RATE_TYPE_MAP:
            codes["RATE-TYPE-UNKNOWN"] += 1
            unknown_rate_types[rate_raw or "(blank)"] += 1
            details.append(f"  #{index} {_mask(sid)} [{category}]: rate type cell is {_state(fields.get('rate_type'))}")
            continue

        from scb_ppnr.interest_income import RATE_FLOATING
        if _RATE_TYPE_MAP.get(rate_raw) == RATE_FLOATING and _state(fields.get("coupon")) == "EMPTY":
            codes["FLOATER-NO-COUPON"] += 1
            details.append(f"  #{index} {_mask(sid)} [{category}]: FLOATING with an empty coupon cell — margin imputation impossible")
            continue

        wal_state = _state(fields.get("wal"))
        wal_ok = wal_state == "NUMBER" and float(str(fields["wal"]).replace(",", "")) > 0
        if wal_state != "EMPTY" and not wal_ok:
            codes["WAL-NONPOS"] += 1
            continue

        maturity_missing = _blank(fields.get("maturity")) or report_date is None
        if maturity_missing and agency and wal_ok:
            codes["SEC7-WAL-MATURITY"] += 1
            maturity_missing = False

        by_state = _state(record.get("book_yield"))
        ac_state = _state(record.get("amortized_cost"))
        price_state = _state(record.get("price"))
        legs = []
        if maturity_missing:
            legs.append("MAT")
        if by_state in ("EMPTY", "ZERO"):
            legs.append("BY0")
        if ac_state in ("EMPTY", "ZERO"):
            legs.append("AC0")

        if legs and ac_state in ("EMPTY", "ZERO"):
            if price_state in ("EMPTY", "ZERO"):
                code = f"S3-STOP[{'+'.join(legs)}]"
                codes[code] += 1
                details.append(
                    f"  #{index} {_mask(sid)} [{category}/{rate_raw}]: THE HARD STOP — "
                    f"AC={ac_state} BY={by_state} maturity={'MISSING' if maturity_missing else 'ok'} "
                    f"price={price_state}"
                )
            else:
                codes["S3-PROXY-OK"] += 1
        elif legs:
            codes["S3-TRIGGER-NO-STOP"] += 1        # trigger legs but AC present -> loads fine
        else:
            codes["OK"] += 1

    # ---- 4. Output ----------------------------------------------------------
    print(f"\nfirst {min(args.detail, len(details))} problem securities (LOCAL ONLY — masked ids, no values):")
    for line in details[: args.detail]:
        print(line)

    duplicates = {sid: n for sid, n in identifier_rows.items() if n > 1}
    print("\n================ SUMMARY TO RELAY (codes and counts only — safe to copy) ================")
    for line in relay:
        print(line)
    for code, count in sorted(codes.items()):
        print(f"{code}: {count}")
    if unknown_rate_types:
        print("UNKNOWN-RATE-TYPE-LABELS:", "; ".join(f"{label} x{n}" for label, n in unknown_rate_types.most_common(15)))
    print(f"IDENTIFIERS: distinct={len(identifier_rows)} with-multiple-rows={len(duplicates)} "
          f"max-rows-per-identifier={max(identifier_rows.values(), default=0)}")
    print("INTENT-COUNTS:", "; ".join(f"{k or '(blank)'}={n}" for k, n in intent_counts.most_common()))
    print("known categories in the PID-SEC-5 map:", len(CATEGORY_MODEL_MAP))
    print("==========================================================================================")


if __name__ == "__main__":
    main()

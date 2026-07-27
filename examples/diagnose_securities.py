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
  SEC9-MATURITY-FROM-POSITIONS  maturity date missing -> positions-sheet maturity-years column used (PID-SEC-9)
  FLOATER-CPN-FROM-POSITIONS    floating with a blank enrichment coupon -> positions-sheet coupon used (PID-SEC-9)
  OK                      loads cleanly
"""

from __future__ import annotations

import argparse
from collections import Counter

from scb_ppnr.ingestion import load_config, load_mev_scenario, load_securities_inputs
from scb_ppnr.ingestion.securities_loader import (
    _EXCEL_ERRORS,
    _POSITIONS_MDRM,
    _RATE_TYPE_MAP,
    _REQUIRED_MDRM,
    _STEP_LABELS,
    _blank,
    _enrichment_map,
    _load_workbook,
    _parse_date,
    _positions_rows,
    _prepayment_map,
    _sheet,
    _technical_columns,
)
from scb_ppnr.interest_income import OUT_OF_SCOPE, RATE_FLOATING, ValidationFailure, assign_model
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
    parser.add_argument("--compare", action="store_true",
                        help="diff our per-security income against the workbook's own II_PQ1..II_PQ9 columns")
    parser.add_argument("--scenario", default=None, help="scenario id for --compare (defaults to the first configured)")
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
        records, columns, header_notes = _positions_rows(
            _sheet(workbook, sc.positions_sheet, path), path, sc.price_mdrm, _technical_columns(sc)
        )
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
        excel_error_cells = sum(
            1 for record in records for value in record.values()
            if isinstance(value, str) and value.strip().upper() in _EXCEL_ERRORS
        )
        relay.append(f"EXCEL-ERROR-CELLS:{excel_error_cells} (treated as missing — user-directed 2026-07-27)")
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
        if rate_raw in _STEP_LABELS:
            codes["STEP-CPN-INTERIM"] += 1                 # handled by the loader (fixed at launch coupon)
        elif rate_raw not in _RATE_TYPE_MAP:
            codes["RATE-TYPE-UNKNOWN"] += 1
            unknown_rate_types[rate_raw or "(blank)"] += 1
            details.append(f"  #{index} {_mask(sid)} [{category}]: rate type cell is {_state(fields.get('rate_type'))}")
            continue

        if _RATE_TYPE_MAP.get(rate_raw) == RATE_FLOATING and _state(fields.get("coupon")) == "EMPTY":
            if _state(record.get("tech_coupon")) in ("NUMBER", "ZERO"):
                codes["FLOATER-CPN-FROM-POSITIONS"] += 1   # PID-SEC-9 fallback covers it — loads fine
            else:
                codes["FLOATER-NO-COUPON"] += 1
                details.append(f"  #{index} {_mask(sid)} [{category}]: FLOATING with an empty coupon cell — margin imputation impossible")
                continue

        wal_state = _state(fields.get("wal"))
        wal_ok = wal_state == "NUMBER" and float(str(fields["wal"]).replace(",", "")) > 0
        if wal_state != "EMPTY" and not wal_ok:
            codes["WAL-NONPOS"] += 1
            continue

        maturity_missing = _blank(fields.get("maturity")) or report_date is None
        if maturity_missing and _state(record.get("tech_maturity_years")) == "NUMBER":
            codes["SEC9-MATURITY-FROM-POSITIONS"] += 1     # PID-SEC-9 fallback covers it
            maturity_missing = False
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

    if args.compare:
        run_compare(config, args)


def run_compare(config, args) -> None:
    """Per-security diff: our income vs the workbook's own II_PQ1..II_PQ9 columns.

    Local section shows category aggregates in USD millions and the worst movers
    (masked ids). The relay section carries only counts, tolerance bands, and
    ours/reference RATIOS — no amounts."""
    from scb_ppnr.interest_income import ii_mbs as m_mbs
    from scb_ppnr.interest_income import ii_other_sec as m_osec
    from scb_ppnr.interest_income import ii_ust as m_ust
    from scb_ppnr.interest_income.securities_engine import reinvestment_income

    sc = config.firm_data.securities
    if config.mev is None:
        raise SystemExit("--compare needs a [mev] section for the scenario")
    scenario_id = args.scenario or next(iter(config.mev.scenarios))
    scenario = load_mev_scenario(config, scenario_id).interest_income_scenario_paths()
    inputs = load_securities_inputs(config)

    quarters = range(1, 10)
    bands = ((0.001, "<=0.1%"), (0.01, "<=1%"), (0.05, "<=5%"))
    per_cat: dict[str, dict[str, float]] = {}
    worst: list[tuple[float, str]] = []
    ours_q = {q: 0.0 for q in quarters}
    ref_q = {q: 0.0 for q in quarters}
    no_reference = 0
    compare_skipped = 0

    def flows_for(position, sink):
        if position.model == "ii_ust":
            return m_ust._flows(position, sink)
        if position.model == "ii_mbs":
            coupon = m_mbs._coupon_path(position, scenario, sc.floor_mode, sink)
            if position.face_path is not None:
                return m_mbs._agency_flows(position, coupon, sink)
            return m_mbs._other_mbs_flows(position, coupon, sink)
        return m_osec._flows(position, scenario, sc.floor_mode, sink)

    for group in (inputs.ust, inputs.mbs, inputs.other_sec):
        for position in group:
            if position.reference_income is None:
                no_reference += 1
                continue
            sink: list[str] = []
            try:
                flows = flows_for(position, sink)
            except ValidationFailure:
                compare_skipped += 1
                continue
            reinv, _ = reinvestment_income(flows.reinvestment_events(sc.reinvest_paydowns), scenario)
            ours = {q: flows.total.get(q, 0.0) + reinv[q] for q in quarters}
            ref = position.reference_income
            ours_total = sum(ours.values())
            ours_xr_total = ours_total - sum(reinv[q] for q in quarters)   # excluding reinvestment
            ref_total = sum(ref[q] for q in quarters)
            for q in quarters:
                ours_q[q] += ours[q]
                ref_q[q] += ref[q]

            stats = per_cat.setdefault(position.category, {"n": 0, "ours": 0.0, "ours_xr": 0.0, "ref": 0.0,
                                                           "<=0.1%": 0, "<=1%": 0, "<=5%": 0, ">5%": 0,
                                                           "ref-zero": 0})
            stats["n"] += 1
            stats["ours"] += ours_total
            stats["ours_xr"] += ours_xr_total
            stats["ref"] += ref_total
            if ref_total == 0.0 and abs(ours_total) > 1e-9:
                stats["ref-zero"] += 1                     # reference row books NO income at all
                                                           # (e.g. blank sovereign-ZCB II_PQ rows)
            # Bands on the xr basis: II_PQ excludes reinvestment (resolved 2026-07-24),
            # so the like-for-like per-security diff is ours-excluding-reinvestment vs ref.
            diff = ours_xr_total - ref_total
            rel = abs(diff) / abs(ref_total) if ref_total != 0.0 else (0.0 if abs(diff) < 1e-9 else 1.0)
            for threshold, label in bands:
                if rel <= threshold:
                    stats[label] += 1
                    break
            else:
                stats[">5%"] += 1
                worst.append((abs(diff), f"{_mask(position.security_id)} [{position.category}/{position.rate_type}] "
                                         f"rel-gap {rel:6.1%} sign {'OURS-HIGH' if diff > 0 else 'OURS-LOW'}"))

    print("\nCOMPARE — LOCAL DETAIL (USD millions; masked ids):")
    for category, stats in sorted(per_cat.items()):
        print(f"  {category:42s} n={stats['n']:>6}  ours={stats['ours']:14.2f}  ref={stats['ref']:14.2f}")
    worst.sort(reverse=True)
    for _, line in worst[:15]:
        print(f"  worst: {line}")

    print("\n================ COMPARE SUMMARY TO RELAY (counts/bands/ratios only) ================")
    print("(xr/ref is PRIMARY — resolved 2026-07-24: the II_PQ columns exclude reinvestment income)")
    total_xr = 0.0
    for category, stats in sorted(per_cat.items()):
        ratio = stats["ours"] / stats["ref"] if stats["ref"] else float("nan")
        ratio_xr = stats["ours_xr"] / stats["ref"] if stats["ref"] else float("nan")
        total_xr += stats["ours_xr"]
        print(f"COMPARE {category}: n={stats['n']} <=0.1%:{stats['<=0.1%']} <=1%:{stats['<=1%']} "
              f"<=5%:{stats['<=5%']} >5%:{stats['>5%']} ref-zero:{stats['ref-zero']} "
              f"xr/ref={ratio_xr:.4f} incl-reinv/ref={ratio:.4f}")
    total_ours, total_ref = sum(ours_q.values()), sum(ref_q.values())
    if total_ref:
        print(f"COMPARE-TOTAL: xr/ref={total_xr / total_ref:.4f} incl-reinv/ref={total_ours / total_ref:.4f}")
    else:
        print("COMPARE-TOTAL: no reference")
    print("COMPARE-BY-QUARTER ours/ref:",
          " ".join(f"PQ{q}={ours_q[q] / ref_q[q]:.3f}" if ref_q[q] else f"PQ{q}=n/a" for q in quarters))
    floor_suspect = sum("suspect source-cell units" in w for w in inputs.warnings)
    print(f"COMPARE-NO-REFERENCE: {no_reference}   COMPARE-SKIPPED: {compare_skipped}   FLOOR-SUSPECT: {floor_suspect}")
    print("======================================================================================")


if __name__ == "__main__":
    main()

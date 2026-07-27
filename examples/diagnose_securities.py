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
    parser.add_argument("--gaps", default=None, metavar="FILE.csv",
                        help="write the largest per-security gaps to a CSV — LOCAL ONLY (unmasked ids, "
                             "exact ours/ref amounts per quarter, and the inputs used) so rows can be "
                             "found in the workbook; never relay or commit this file")
    parser.add_argument("--gaps-top", type=int, default=25,
                        help="how many securities per category in the --gaps file (by absolute gap; default 25)")
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
    # Floating-coupon rule bake-off (2026-07-27): the floor hypothesis is refuted for
    # Non-Agency RMBS / CMBS (no floor on file in ANY source; totals immobile across
    # floor sources), so candidate coupon rules are priced side by side — coupon leg
    # swapped per rule, AA leg ours — and reported as relay-safe rule/ref ratios.
    #   current   = the configured floor_mode path (baseline; equals xr for the subset)
    #   flat_c0   = launch coupon held flat PQ1..9 (floater treated as fixed)
    #   lag3m_f0  = max(margin + 3M(q−1), 0), margin vs 3M(PQ0) — the PRIOR-QUARTER
    #               reset: PQ1 accrues at the launch coupon (fixed at the last reset),
    #               each later quarter at the prior quarter-end's 3M; floored at 0
    #   lag1_3m   = c0 + (3M(q) − 3M(PQ1)) — PQ1 anchored, floating with the 3M change
    #   by_flat   = book yield held flat (launch coupon when book yield is missing)
    #   excel_ind = flat_c0 where the sheet's own float/fixed indicator says Fixed,
    #               else lag3m_f0 (needs positions_rate_type_column; missing → lag3m_f0)
    #   freeze1_f0 = c0 in PQ1, then max(margin + 3M(PQ1), 0) FROZEN for PQ2..9 — one
    #               reset at PQ1, constant thereafter (per-row-constant accrual)
    #   blend13   = monthly-reset PQ1: ⅓·c0 + ⅔·(margin + 3M(PQ1)), then the spot rule
    #               max(margin + 3M(q), 0) — round-3 identified PQ1 index ≈ 2.4–2.7 %
    #   neg_hold  = negative-margin floaters HOLD the launch coupon flat (never
    #               projected); positive margins follow the spot rule — round-3
    #               identified Non-Agency RMBS implied ≈ 0.99 flat at c0
    # CPN-SOURCE: per category, the sheet's own coupon column ÷ the ITO coupon
    # (face-weighted mean, median, share differing >1 %) — a constant multiplier
    # (e.g. municipal ≈ 1.13–1.27) means the reference uses a different COUPON
    # INPUT (tax-equivalent), not a different formula.
    # IMPLIED-CPN (round 3): the reference's own implied coupon path — per category
    # and rate-type subset, [Σ(ref(q) − our AA(q))] / [Σ face(q−1)/4 × c0], i.e. the
    # face-weighted implied coupon as a RATIO to the launch coupon (relay-safe).
    # Read with the SCENARIO-3M line to identify the rule directly.
    float_rules: dict[str, dict[str, float]] = {}
    ratio_rows: dict[str, list[float]] = {}
    implied: dict[tuple[str, str], dict[int, list[float]]] = {}   # (category, subset) -> q -> [num, c0-weight]
    cpn_source: dict[str, list[tuple[float, float]]] = {}         # category -> [(face, sheet/ito coupon ratio)]
    # FIXED-RULES (2026-07-27, Municipal focus): fixed-rate accrual candidates —
    #   current      = coupon × face/4 + our AA (the PID-SEC-8 baseline)
    #   by_face_aa   = BOOK YIELD × face/4 + our AA (BY-basis coupon leg)
    #   by_face_only = BOOK YIELD × face/4 alone (≡ coupon leg + AA=(BY−c0)·face/4,
    #                  the constant "yield adjustment" — total income = BY × face/4)
    fixed_rules: dict[str, dict[str, float]] = {}
    # SOVEREIGN-ZCB decomposition (OQ-028): which reference behavior carries the gap.
    zcb_buckets: dict[str, list[float]] = {"ref_zero": [0, 0.0, 0.0], "pq1_only": [0, 0.0, 0.0],
                                           "full": [0, 0.0, 0.0]}    # [n, ours_xr, ref]
    gap_records: list[dict] = []                                     # --gaps CSV rows (LOCAL ONLY)
    t3m = scenario.usd_3m_treasury

    def treatment_for(position) -> str:
        """The treatment actually applied to this row (for the --gaps file)."""
        if position.category in sc.book_yield_categories and position.book_yield is not None \
                and position.rate_type != "zero_coupon":
            return "book_yield_flat"
        if position.rate_type == "zero_coupon":
            return ("zcb_no_accretion" if position.category in sc.zcb_no_accretion_categories
                    else "zero_coupon")
        if position.rate_type == "floating":
            return sc.floating_projection_overrides.get(position.category, sc.floating_projection)
        return position.rate_type

    def flows_for(position, sink):
        if position.model == "ii_ust":
            return m_ust._flows(position, sink)
        if position.model == "ii_mbs":
            coupon = m_mbs._coupon_path(position, scenario, sc.floor_mode, sink,
                                        sc.floating_projection, sc.floating_projection_overrides)
            if position.face_path is not None:
                return m_mbs._agency_flows(position, coupon, sink)
            return m_mbs._other_mbs_flows(position, coupon, sink)
        return m_osec._flows(position, scenario, sc.floor_mode, sink,
                             sc.floating_projection, sc.book_yield_categories,
                             sc.floating_projection_overrides, sc.zcb_no_accretion_categories)

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

            if ref_total > 0.0:
                ratio_rows.setdefault(position.category, []).append(ours_xr_total / ref_total)

            if args.gaps:
                record = {
                    "category": position.category,
                    "security_id": position.security_id,
                    "rate_type": position.rate_type,
                    "treatment": treatment_for(position),
                    "ours_9q_xr": round(ours_xr_total, 6),
                    "ref_9q": round(ref_total, 6),
                    "gap": round(ours_xr_total - ref_total, 6),
                    "rel_gap": round((ours_xr_total - ref_total) / ref_total, 4) if ref_total else "",
                    "current_face": round(position.current_face, 6),
                    "amortized_cost": round(position.amortized_cost, 6),
                    "coupon_rate": position.coupon_rate,
                    "book_yield": position.book_yield,
                    "coupon_floor": position.coupon_floor,
                    "maturity_years": position.maturity_years,
                    "maturity_quarters": position.maturity_quarters,
                    "wal_years": position.wal_years,
                    "ac_proxied": position.ac_proxied,
                }
                for q in quarters:
                    record[f"ours_q{q}"] = round(flows.total.get(q, 0.0), 6)
                for q in quarters:
                    record[f"ref_q{q}"] = round(ref[q], 6)
                gap_records.append(record)

            if (position.coupon_rate not in (None, 0.0) and position.excel_coupon_rate is not None
                    and position.rate_type in ("floating", "fixed")):
                cpn_source.setdefault(position.category, []).append(
                    (position.current_face, position.excel_coupon_rate / position.coupon_rate)
                )

            if (position.rate_type == "fixed" and position.coupon_rate not in (None, 0.0)
                    and position.book_yield is not None and ref_total > 0.0):
                fx = fixed_rules.setdefault(position.category, {"n": 0, "ref": 0.0, "current": 0.0,
                                                                "by_face_aa": 0.0, "by_face_only": 0.0})
                aa_total = sum(flows.accretion.get(q, 0.0) for q in quarters)
                weight_sum = sum(
                    (position.face_path[q - 1] if position.face_path is not None else position.current_face) / 4.0
                    for q in quarters if q <= flows.alive_through
                )
                fx["n"] += 1
                fx["ref"] += ref_total
                fx["current"] += ours_xr_total
                fx["by_face_aa"] += weight_sum * position.book_yield + aa_total
                fx["by_face_only"] += weight_sum * position.book_yield

            if position.category == "Sovereign Bond" and position.rate_type == "zero_coupon":
                nonzero_quarters = [q for q in quarters if abs(ref[q]) > 1e-9]
                if not nonzero_quarters:
                    bucket = zcb_buckets["ref_zero"]
                elif nonzero_quarters == [1]:
                    bucket = zcb_buckets["pq1_only"]
                else:
                    bucket = zcb_buckets["full"]
                bucket[0] += 1
                bucket[1] += ours_xr_total
                bucket[2] += ref_total

            if position.coupon_rate is not None and position.rate_type in ("floating", "fixed") and ref_total > 0.0:
                bucket = implied.setdefault((position.category, position.rate_type), {q: [0.0, 0.0] for q in quarters})
                for quarter in quarters:
                    if quarter > flows.alive_through:
                        break
                    face_prior = (position.face_path[quarter - 1] if position.face_path is not None
                                  else position.current_face)
                    bucket[quarter][0] += ref[quarter] - flows.accretion.get(quarter, 0.0)
                    bucket[quarter][1] += face_prior / 4.0 * position.coupon_rate

            if position.rate_type == RATE_FLOATING and position.coupon_rate is not None:
                fr = float_rules.setdefault(position.category, {"n": 0, "ref": 0.0, "current": 0.0,
                                                                "flat_c0": 0.0, "lag3m_f0": 0.0,
                                                                "lag1_3m": 0.0, "by_flat": 0.0,
                                                                "excel_ind": 0.0, "freeze1_f0": 0.0,
                                                                "blend13": 0.0, "neg_hold": 0.0,
                                                                "ind_fixed": 0, "ind_float": 0, "ind_na": 0})
                fr["n"] += 1
                fr["ref"] += ref_total
                fr["current"] += ours_xr_total
                aa_total = sum(flows.accretion.get(q, 0.0) for q in quarters)
                c0 = position.coupon_rate
                by = position.book_yield if position.book_yield is not None else c0
                margin = c0 - t3m[0]
                label = (position.excel_rate_label or "").upper()
                ind_fixed = "FIX" in label
                if not label:
                    fr["ind_na"] += 1
                elif ind_fixed:
                    fr["ind_fixed"] += 1
                else:
                    fr["ind_float"] += 1
                for quarter in quarters:
                    if quarter > flows.alive_through:
                        break
                    face_prior = (position.face_path[quarter - 1] if position.face_path is not None
                                  else position.current_face)
                    weight = face_prior / 4.0
                    lag_coupon = max(margin + t3m[quarter - 1], 0.0)
                    fr["flat_c0"] += weight * c0
                    fr["lag3m_f0"] += weight * lag_coupon
                    fr["lag1_3m"] += weight * (c0 + t3m[quarter] - t3m[1])
                    fr["by_flat"] += weight * by
                    fr["excel_ind"] += weight * (c0 if ind_fixed else lag_coupon)
                    fr["freeze1_f0"] += weight * (c0 if quarter == 1 else max(margin + t3m[1], 0.0))
                    spot_coupon = max(margin + t3m[quarter], 0.0)
                    blend_pq1 = max(c0 / 3.0 + 2.0 * (margin + t3m[1]) / 3.0, 0.0)
                    fr["blend13"] += weight * (blend_pq1 if quarter == 1 else spot_coupon)
                    fr["neg_hold"] += weight * (c0 if margin < 0.0 else spot_coupon)
                for rule in ("flat_c0", "lag3m_f0", "lag1_3m", "by_flat", "excel_ind", "freeze1_f0",
                             "blend13", "neg_hold"):
                    fr[rule] += aa_total

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
    if float_rules:
        print("FLOAT-RULES (floating+reference subset; coupon leg per rule, AA leg ours; ratios rule/ref):")
        print("  current=configured mode | flat_c0=launch coupon flat | lag3m_f0=max(margin+3M(q-1),0) prior-quarter reset")
        print("  lag1_3m=c0+(3M(q)-3M(PQ1)) | by_flat=book yield flat | excel_ind=flat_c0 if sheet says Fixed else lag3m_f0")
        print("  freeze1_f0=c0 in PQ1 then max(margin+3M(PQ1),0) frozen PQ2..9")
        print("  blend13=PQ1 1/3*c0+2/3*(margin+3M(PQ1)) then spot | neg_hold=margin<0 holds c0 flat, else spot")
        for category, fr in sorted(float_rules.items()):
            if not fr["ref"]:
                print(f"FLOAT-RULES {category}: n={fr['n']} ref-total-zero — ratios n/a")
                continue
            print(f"FLOAT-RULES {category}: n={fr['n']} current={fr['current'] / fr['ref']:.4f} "
                  f"flat_c0={fr['flat_c0'] / fr['ref']:.4f} lag3m_f0={fr['lag3m_f0'] / fr['ref']:.4f} "
                  f"lag1_3m={fr['lag1_3m'] / fr['ref']:.4f} by_flat={fr['by_flat'] / fr['ref']:.4f} "
                  f"excel_ind={fr['excel_ind'] / fr['ref']:.4f} freeze1_f0={fr['freeze1_f0'] / fr['ref']:.4f} "
                  f"blend13={fr['blend13'] / fr['ref']:.4f} neg_hold={fr['neg_hold'] / fr['ref']:.4f} "
                  f"ind(F/x/na)={fr['ind_fixed']}/{fr['ind_float']}/{fr['ind_na']}")
    off_for_fixed = {c for c, s in per_cat.items() if s["ref"] and abs(s["ours_xr"] / s["ref"] - 1.0) > 0.02}
    fixed_lines = [(category, fx) for category, fx in sorted(fixed_rules.items())
                   if category in off_for_fixed and fx["ref"]]
    if fixed_lines:
        print("FIXED-RULES (fixed+reference subset, categories >2% off; ratios rule/ref):")
        print("  current=coupon*face/4 + our AA | by_face_aa=BY*face/4 + our AA | by_face_only=BY*face/4 alone")
        for category, fx in fixed_lines:
            print(f"FIXED-RULES {category}: n={fx['n']} current={fx['current'] / fx['ref']:.4f} "
                  f"by_face_aa={fx['by_face_aa'] / fx['ref']:.4f} by_face_only={fx['by_face_only'] / fx['ref']:.4f}")
    if any(bucket[0] for bucket in zcb_buckets.values()):
        sov_ours_total = sum(bucket[1] for bucket in zcb_buckets.values())
        parts = []
        for name, (count, ours_sum, ref_sum) in zcb_buckets.items():
            share = ours_sum / sov_ours_total if sov_ours_total else 0.0
            ratio = f" ours/ref={ours_sum / ref_sum:.3f}" if ref_sum else ""
            parts.append(f"{name}: n={int(count)} ours-share={share:.1%}{ratio}")
        print("SOVEREIGN-ZCB (reference behavior buckets; ours-share = share of OUR sovereign-ZCB income):")
        print("SOVEREIGN-ZCB " + " | ".join(parts))
    if cpn_source:
        print("CPN-SOURCE (positions-sheet coupon ÷ ITO coupon; face-weighted mean / median / share >1% apart):")
        for category, pairs in sorted(cpn_source.items()):
            faces = sum(f for f, _ in pairs)
            wmean = sum(f * r for f, r in pairs) / faces if faces else float("nan")
            med = sorted(r for _, r in pairs)[len(pairs) // 2]
            share = sum(1 for _, r in pairs if abs(r - 1.0) > 0.01) / len(pairs)
            print(f"CPN-SOURCE {category}: n={len(pairs)} wmean={wmean:.4f} p50={med:.4f} diff>1%:{share:.1%}")
    print("SCENARIO-3M (supervisory scenario path, annualized decimals — public FRB data):",
          " ".join(f"PQ{q}={t3m[q]:.4f}" for q in range(0, 10)))
    if implied:
        print("IMPLIED-CPN (reference implied coupon ÷ launch coupon, face-weighted; ref minus OUR AA leg):")
        off_categories = {c for c, s in per_cat.items() if s["ref"] and abs(s["ours_xr"] / s["ref"] - 1.0) > 0.02}
        for (category, subset), bucket in sorted(implied.items()):
            if subset == "fixed" and category not in off_categories:
                continue
            cells = []
            for q in quarters:
                num, c0w = bucket[q]
                cells.append(f"q{q}={num / c0w:.3f}" if c0w > 0 else f"q{q}=n/a")
            print(f"IMPLIED-CPN {category} [{subset}]: " + " ".join(cells))
    spread_lines = []
    for category, stats in sorted(per_cat.items()):
        if not stats["ref"] or abs(stats["ours_xr"] / stats["ref"] - 1.0) <= 0.02:
            continue
        values = sorted(ratio_rows.get(category, []))
        if len(values) < 5:
            continue
        picks = {p: values[min(len(values) - 1, max(0, round(p / 100 * (len(values) - 1))))] for p in (10, 25, 50, 75, 90)}
        spread_lines.append(f"RATIO-SPREAD {category}: n={len(values)} " +
                            " ".join(f"p{p}={v:.3f}" for p, v in picks.items()))
    if spread_lines:
        print("RATIO-SPREAD (per-row xr/ref percentiles; categories >2% off, ref>0 rows — tax-gross-up or")
        print("  split-population signatures show up as clusters away from 1.000):")
        for line in spread_lines:
            print(line)
    total_ours, total_ref = sum(ours_q.values()), sum(ref_q.values())
    if total_ref:
        print(f"COMPARE-TOTAL: xr/ref={total_xr / total_ref:.4f} incl-reinv/ref={total_ours / total_ref:.4f}")
    else:
        print("COMPARE-TOTAL: no reference")
    print("COMPARE-BY-QUARTER ours/ref:",
          " ".join(f"PQ{q}={ours_q[q] / ref_q[q]:.3f}" if ref_q[q] else f"PQ{q}=n/a" for q in quarters))
    floor_suspect = sum("suspect source-cell units" in w for w in inputs.warnings)
    print(f"COMPARE-NO-REFERENCE: {no_reference}   COMPARE-SKIPPED: {compare_skipped}   FLOOR-SUSPECT: {floor_suspect}")

    if args.gaps and gap_records:
        import csv
        by_category: dict[str, list[dict]] = {}
        for record in gap_records:
            by_category.setdefault(record["category"], []).append(record)
        selected: list[dict] = []
        for category in sorted(by_category):
            rows = by_category[category]
            rows.sort(key=lambda r: abs(r["gap"]), reverse=True)
            selected.extend(rows[: args.gaps_top])
        with open(args.gaps, "w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(selected[0].keys()))
            writer.writeheader()
            writer.writerows(selected)
        print(f"\nGAP DETAIL: {len(selected)} rows written to {args.gaps} — top {args.gaps_top} per "
              f"category by absolute gap (USD millions; ours excludes reinvestment = the II_PQ basis).")
        print("  LOCAL ONLY: the file carries unmasked ids and exact amounts — find rows in the workbook")
        print("  via the CQSCS383 unique-id column; do NOT relay, screenshot, or commit this file.")
    print("======================================================================================")


if __name__ == "__main__":
    main()

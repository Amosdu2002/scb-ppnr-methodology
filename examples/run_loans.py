"""Corporate wholesale loans (`ii_loans` — Corporate), driven by the firm workbook.

    PYTHONPATH=src python3 examples/run_loans.py                            # synthetic demo
    PYTHONPATH=src python3 examples/run_loans.py \
        --config config/local/company.toml --report loans_report.txt        # company run

Everything physical lives in the config's [firm_data.loans] section — workbook
path, every sheet name, header row and column header, the launch point, and the
scenario name (see config/company.template.toml). Nothing is passed as a CLI
path. --scenario and --launch-point exist only as one-off OVERRIDES of the
config values.

Scenario names: history rows are matched under `Actual` (through PQ0); projection
rows under the configured scenario, default `Supervisory Severely Adverse` — the
sheet's own block name. Projection rows are mapped to PQ1..PQ9 BY THEIR Date
column relative to the launch point, never by sheet order; a wrong scenario
spelling errors with the row names actually found.

Censuses print FIRST, results after — the securities-loop lesson: the diagnostics
are the product of a first run, the numbers only matter once the censuses are
clean. Output amounts: USD MILLIONS per quarter (D-006). The report file carries
firm amounts — keep it local, never commit it (gitignored `loans_report*.txt`).

The Federal Reserve model is PROPOSED for the 2026 stress test, NOT adopted.
Decisions: PID-LOAN-1..11 (`handbook/open-questions.md`); computation:
`specifications/interest-income/loans/ii_loans_corporate.spec.md`."""

from __future__ import annotations

import argparse
import datetime as dt
import tempfile
from pathlib import Path

from scb_ppnr.core.schemas import PROJECTION_QUARTERS, ValidationFailure
from scb_ppnr.ingestion.config import format_effective_config, load_config
from scb_ppnr.ingestion.loans_loader import (
    LoansSheetSpec,
    load_3m_treasury,
    load_category_balances,
    load_facilities,
    load_merged_bucket_balance,
    load_reference_results,
)
from scb_ppnr.ingestion.loans_mapping import (
    DEPOSITORY_INSTITUTION_H1_CODES,
    FED_CATEGORY_NAMES,
    scalars_by_category_name,
)
from scb_ppnr.interest_income.loans_launchpoint import (
    build_launch_point,
    merged_bucket_launch_point,
)
from scb_ppnr.interest_income.loans_projection import project_corporate
from scb_ppnr.interest_income.loans_schemas import projection_quarter_index


def _run(spec: LoansSheetSpec, scenario: str, launch_point: str,
         floor_collapse: str = "balance_weighted", apply_scalar: bool = True,
         share_basis: str = "committed", balance_source: str = "m1",
         engine: str = "pid", collected: list[str] | None = None) -> str:
    """Each section PRINTS the moment it is produced (the securities-loop
    lesson): a failure deep in the run must never hide the censuses that
    explain it. `collected` receives the sections for the report file even
    when a later step raises."""
    sections: list[str] = collected if collected is not None else []

    def emit(text: str) -> None:
        print(text, end="\n\n", flush=True)
        sections.append(text)

    quarters = PROJECTION_QUARTERS

    facilities, load_census = load_facilities(spec)
    balances, side_balances, m1_census = load_category_balances(spec)
    merged_balance, merged_parts = load_merged_bucket_balance(spec)
    history, base_path, launch_3m = load_3m_treasury(spec, scenario, quarters, launch_point)

    emit(
        f"RUN SETTINGS\n"
        f"  workbook      : {spec.workbook}\n"
        f"  scenario      : {scenario}\n"
        f"  launch point  : {launch_point} (PQ0); PQ1..PQ9 follow\n"
        f"  3M at PQ0     : {launch_3m:.4%}   history quarters: {len(history)} "
        f"(earliest {min(history)})\n"
        f"  engine: {engine}   floor collapse: {floor_collapse}   share basis: {share_basis}"
        f"   balance source: {balance_source}\n"
        f"  units         : USD millions; annualized decimal rates"
    )
    emit(
        "SCENARIO 3M PATH\n  PQ0 " + f"{launch_3m:7.4%}  "
        + "  ".join(f"PQ{q} {base_path[q]:7.4%}" for q in quarters)
    )
    emit(load_census.render())
    if m1_census.warnings:
        emit("M.1 NOTES\n" + "\n".join(f"  {note}" for note in m1_census.warnings))

    m1_lines = ["M.1 CATEGORY BALANCES (cross-check: the FRB SCALARS sheet's 'Sch M bal' column)"]
    for name, value in sorted(balances.items(), key=lambda kv: -kv[1]):
        m1_lines.append(f"  {value:>12,.1f}  {name}")
    m1_lines.append(
        f"  {merged_balance:>12,.1f}  merged 9/10/11 bucket from FR Y-9C "
        f"({', '.join(f'{k} {v:,.1f}' for k, v in sorted(merged_parts.items()))})"
    )
    emit("\n".join(m1_lines))

    launch, launch_diagnostics = build_launch_point(
        facilities, balances, launch_3m, history, quarters,
        lambda when: projection_quarter_index(when, launch_point),
        share_measure=share_basis,
        floor_collapse=floor_collapse,
        balance_source=balance_source,
        engine=engine,
        side_balances=side_balances,
    )
    merged = merged_bucket_launch_point(
        facilities, merged_balance, launch_3m, DEPOSITORY_INSTITUTION_H1_CODES,
        FED_CATEGORY_NAMES[9], floor_collapse=floor_collapse,
    )
    emit(launch_diagnostics.render())

    register = ["LAUNCH-POINT REGISTER (compare each line against the workbook's own cells)"]
    register.append(
        "  segment (category/LOCOM/vt)                     share%   balance"
        "   pool rate  base@(qtr)     spread    floor   sum-wt"
    )
    for key in sorted(launch, key=str):
        lp = launch[key]
        if lp.spread is not None:
            pool = f"{lp.spread.pool_rate:8.4%}"
            base_at = lp.spread.base_quarter or "PQ0"
            base = f"{lp.spread.base_rate:7.4%}@{base_at:<7}"
            spread = f"{lp.spread.spread:8.4%}"
        else:
            pool, base, spread = "       -", "        -      ", "       -"
        floor_text = f"{lp.floor:7.4%}" if lp.floor is not None else "      -"
        wt_text = (
            f"{sum(lp.reorigination_weights.values()):7.3f}"
            if lp.reorigination_weights else "      -"
        )
        register.append(
            f"  {str(key)[:46]:<46}  {lp.share:6.2%}  {lp.balance:>8,.1f}"
            f"  {pool}  {base}  {spread}  {floor_text}  {wt_text}"
        )
    register.append(
        f"  {str(merged.segment)[:46]:<46}    n/a   {merged.balance:>8,.1f}"
        f"  {merged.spread.pool_rate:8.4%}  {merged.spread.base_rate:7.4%}@PQ0    "
        f"  {merged.spread.spread:8.4%}  "
        + (f"{merged.floor:7.4%}" if merged.floor is not None else "      -") + "        -"
    )
    emit("\n".join(register))

    emit(
        f"MERGED 9/10/11 BUCKET\n"
        f"  donor pool rate (depository floating) : {merged.spread.pool_rate:.4%}\n"
        f"  spread vs 3M(PQ0)                     : {merged.spread.spread:.4%}\n"
        f"  floor                                 : "
        + (f"{merged.floor:.4%}" if merged.floor is not None else "none on file")
    )

    if apply_scalar:
        scalars, scalar_warnings = scalars_by_category_name()
    else:
        # Reference-matching runs: the workbook's own results carry NO industry
        # scalar (verified 2026-08-12 — the grand total is the plain block sum).
        scalars, scalar_warnings = {}, ()
    projections, totals, projection_diagnostics = project_corporate(
        {**dict(launch), merged.segment: merged}, base_path, quarters, scalars,
        require_scalar=apply_scalar,
    )
    emit(projection_diagnostics.render())
    for warning in scalar_warnings:
        emit(f"WARN: {warning}")

    scaling_note = "scaled" if apply_scalar else "UNSCALED — apply_scalar = false"
    result_lines = [f"PROJECTED CORPORATE LOAN INTEREST INCOME ({scaling_note}, USD millions)"]
    result_lines.append("  category / PQ                " + "".join(f"{f'PQ{q}':>9}" for q in quarters) + "      9Q")
    grand = {q: 0.0 for q in quarters}
    for name, path in sorted(totals.items(), key=lambda kv: -sum(kv[1].values())):
        for q in quarters:
            grand[q] += path[q]
        result_lines.append(
            f"  {name[:27]:<27}  " + "".join(f"{path[q]:>9,.1f}" for q in quarters)
            + f"{sum(path.values()):>9,.1f}"
        )
    result_lines.append(
        "  TOTAL                        " + "".join(f"{grand[q]:>9,.1f}" for q in quarters)
        + f"{sum(grand.values()):>9,.1f}"
    )
    result_lines.append(f"  segments projected: {len(projections)}")
    emit("\n".join(result_lines))

    if spec.results_sheet is not None:
        reference = load_reference_results(spec)
        emit(_compare(reference, projections, base_path, quarters, scalars))

    return "\n\n".join(sections)


def _compare(reference, projections, base_path, quarters, scalars) -> str:
    """Ours (UNSCALED, per segment) against the workbook's results blocks.

    Their block Total exceeds Fixed + Variable: the workbook sums a third stream
    whose rate signature (linear in 3M, spread above the variable stream's) says
    Mixed — so theirs' mixed is derived as Total - Fixed - Variable and compared
    to our v3 stream. Implied balance and spread per floating stream come from
    the PQ1->PQ2 slope, identically on both sides, so the decomposition into
    balance-vs-spread differences is assumption-free."""
    from scb_ppnr.interest_income.loans_schemas import (
        VT_FIXED, VT_FLOATING, VT_MIXED,
    )

    from scb_ppnr.ingestion.loans_mapping import scalars_by_category_name

    # The reference's row structure (settled 2026-08-12): Fixed and Variable rows
    # are UNSCALED, and Total = (Fixed + Variable) x the Table A8 scalar — verified
    # exact on every transcribed block. So: our fixed/variable streams compare RAW
    # (mixed folds into variable — the reference carries no separate mixed row),
    # and our total compares with the scalar applied.
    a8, _ = scalars_by_category_name()
    ours: dict[tuple[str, str], dict[str, dict[int, float]]] = {}
    stream_of = {VT_FIXED: "fixed", VT_FLOATING: "variable", VT_MIXED: "variable"}
    for key, projection in projections.items():
        stream = stream_of.get(key.variable_type)
        if key.locom == "MERGED":
            stream = "variable"                     # the merged bucket is one floating block
        if stream is None:
            continue
        block = ours.setdefault((key.category, key.locom), {})
        path = block.setdefault(stream, {q: 0.0 for q in quarters})
        for q in quarters:
            path[q] += projection.income_path[q]
    lines = ["LOANS COMPARE (fixed/variable UNSCALED both sides; total = ours x Table A8 vs "
             "theirs Total; ratio = ours/theirs)"]
    lines.append("  block                                     stream       PQ1 o/t          PQ2 o/t          9Q o/t            ratio")

    def fmt(pair):
        mine, theirs = pair
        return f"{mine:>8,.1f}/{theirs:>8,.1f}"

    grand_ours = {q: 0.0 for q in quarters}
    grand_theirs = {q: 0.0 for q in quarters}
    implied_lines: list[str] = []

    for key in sorted(reference):
        category, klass = key
        streams = reference[key]
        total_theirs = streams.get("total", {})
        if all(total_theirs.get(q, 0.0) == 0.0 for q in quarters):
            continue
        block_ours = ours.get(key, {})
        scalar = a8.get(category, 1.0)
        totals_ours = {
            q: (block_ours.get("fixed", {}).get(q, 0.0)
                + block_ours.get("variable", {}).get(q, 0.0)) * scalar
            for q in quarters
        }
        for q in quarters:
            grand_ours[q] += totals_ours[q]
            grand_theirs[q] += total_theirs.get(q, 0.0)

        rows = [
            ("fixed", block_ours.get("fixed", {}), streams.get("fixed", {})),
            ("variable", block_ours.get("variable", {}), streams.get("variable", {})),
            ("total*A8", totals_ours, total_theirs),
        ]
        label = f"{category[:32]}/{klass}"
        for name, mine, theirs in rows:
            nine_mine = sum(mine.get(q, 0.0) for q in quarters)
            nine_theirs = sum(theirs.get(q, 0.0) for q in quarters)
            if nine_mine == 0.0 and nine_theirs == 0.0:
                continue
            ratio = f"{nine_mine / nine_theirs:8.4f}" if nine_theirs else "     n/a"
            lines.append(
                f"  {label:<41} {name:<9}"
                f"  {fmt((mine.get(1, 0.0), theirs.get(1, 0.0)))}"
                f"  {fmt((mine.get(2, 0.0), theirs.get(2, 0.0)))}"
                f"  {fmt((nine_mine, nine_theirs))}  {ratio}"
            )
            label = ""
            if name == "variable":
                implied = []
                for side, path in (("ours", mine), ("theirs", theirs)):
                    m1, m2 = base_path[1], base_path[2]
                    if abs(m1 - m2) < 1e-9:
                        continue
                    balance = (path.get(1, 0.0) - path.get(2, 0.0)) * 4.0 / (m1 - m2)
                    if balance <= 0.0:
                        continue
                    spread = path.get(2, 0.0) * 4.0 / balance - m2
                    implied.append(f"{side} bal {balance:>11,.0f} spread {spread:7.4%}")
                if implied:
                    implied_lines.append(
                        f"      {category[:32]}/{klass} {name:<9} " + "   ".join(implied)
                    )

    nine_ours, nine_theirs = sum(grand_ours.values()), sum(grand_theirs.values())
    lines.append(
        f"  {'GRAND (blocks present on both sides)':<41} {'total':<9}"
        f"  {fmt((grand_ours[1], grand_theirs[1]))}"
        f"  {fmt((grand_ours[2], grand_theirs[2]))}"
        f"  {fmt((nine_ours, nine_theirs))}  "
        + (f"{nine_ours / nine_theirs:8.4f}" if nine_theirs else "     n/a")
    )
    lines.append("  IMPLIED FROM THE PQ1->PQ2 SLOPE (floating streams; balance in USD millions):")
    lines.extend(implied_lines)
    lines.append(
        "  note: a matching ratio with different implied balance AND spread means the two"
    )
    lines.append(
        "  offset — fix the balance first, then re-read the spread."
    )
    return "\n".join(lines)


def _synthetic_workbook(directory: Path) -> Path:
    """A tiny invented book so the runner is demonstrable without any .xlsx on disk."""
    import openpyxl

    book = openpyxl.Workbook()
    h1 = book.active
    h1.title = "CORP H.1"
    headers = [
        "Customer ID", "Line Reported on FR Y9C", "Interest Rate Variability",
        "Lower of Cost or Market Flag", "Interest Rate", "Committed Exposure Global",
        "Utilized Exposure Global", "Interest Rate Floor", "Origination Date", "Maturity Date",
    ]
    for _ in range(3):
        h1.append([None] * len(headers))
    h1.append(headers)
    for row in (
        ["C1", 4, 2, 3, 0.061, 400e6, 300e6, 0.02, "15-Oct-2024", "15-Oct-2030"],
        ["C2", 5, 1, 3, 0.070, 300e6, 300e6, None, "15-Jan-2020", "15-Feb-2026"],
        ["C3", 4, 3, 3, 0.055, 100e6, 80e6, None, "17-May-2022", "15-Oct-2028"],
        ["D1", 1, 2, 3, 0.055, 200e6, 150e6, None, "15-Oct-2024", "15-Oct-2027"],
        ["N1", 7, 2, 3, 0.090, 150e6, 150e6, None, "15-Oct-2024", "15-Oct-2027"],
        ["X1", 8, "[NULL]", 3, None, 50e6, 50e6, None, None, None],
        ["F1", 4, 4, 3, 0.030, 80e6, 10e6, None, "15-Oct-2024", "15-Oct-2027"],
    ):
        h1.append(row)

    fry9c = book.create_sheet("FR-Y9C 4Q 2024")
    for _ in range(7):
        fry9c.append([None, None, None])
    fry9c.append(["ID_RSSD", "Description", "Value"])
    fry9c.append(["BHCK1545", "purch/carry securities", 1_500_000.0])
    fry9c.append(["BHDM1420", "farmland", 500_000.0])

    m1 = book.create_sheet("M.1 Balance")
    for _ in range(10):
        m1.append([None] * 11)
    m1.append(["Wholesale - Corp - C&I and others", "Wholesale - Corp - C&I and others",
               "2.a Graded", "M", 700.0, "M", 90.0, "M", 180.0, "M", 10.0])
    m1.append(["Wholesale - Corp - FI", "Wholesale - Corp - FI",
               "5.d", "M", 260.0, "M", 0.0, "M", 90.0, "M", 0.0])

    mev = book.create_sheet("MEV")
    mev.append(["Scenario Name", "Date", "3-month Treasury rate"])
    history = {1976: 4.9, 2020: 1.5, 2022: 0.8}
    for year, rate in history.items():
        for quarter in (1, 2, 3, 4):
            mev.append(["Actual", f"{year} Q{quarter}", rate])
    mev.append(["Actual", "2024 Q4", 4.4])
    path_3m = [3.0, 1.8, 0.6, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
    for index, rate in enumerate(path_3m):
        year, quarter = 2025 + index // 4, index % 4 + 1
        mev.append(["Supervisory Severely Adverse", f"{year} Q{quarter}", rate])

    target = directory / "synthetic_loans.xlsx"
    book.save(target)
    return target


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--config", type=Path, default=None,
                        help="company config with a [firm_data.loans] section; "
                             "omit for the synthetic demo")
    parser.add_argument("--scenario", default=None,
                        help="override the configured MEV projection-block name for one run")
    parser.add_argument("--launch-point", default=None,
                        help="override the configured PQ0 quarter for one run")
    parser.add_argument("--report", type=Path, default=None,
                        help="also write the output to this file (keep it local)")
    args = parser.parse_args(argv)

    collected: list[str] = []
    try:
        if args.config is None:
            with tempfile.TemporaryDirectory() as scratch:
                workbook = _synthetic_workbook(Path(scratch))
                print("SYNTHETIC DEMO — invented data, hand-checkable numbers. "
                      "Point --config at the company config for a real run.\n", flush=True)
                _run(
                    LoansSheetSpec(workbook=workbook),
                    args.scenario or "Supervisory Severely Adverse",
                    args.launch_point or "2024Q4",
                    collected=collected,
                )
        else:
            config = load_config(args.config)
            if config.firm_data is None or config.firm_data.loans is None:
                raise ValidationFailure(
                    f"{args.config}: no [firm_data.loans] section — the loans run is configured "
                    f"there (workbook path, sheet names, launch point; see "
                    f"config/company.template.toml)"
                )
            loans = config.firm_data.loans
            print(format_effective_config(config) + "\n", flush=True)
            _run(
                loans.spec,
                args.scenario or loans.scenario,
                args.launch_point or loans.launch_point,
                loans.floor_collapse,
                loans.apply_scalar,
                loans.share_basis,
                loans.balance_source,
                loans.engine,
                collected=collected,
            )
        failed = None
    except ValidationFailure as error:
        failed = str(error)
        print("\nVALIDATION FAILURE — the run stopped here; every section above "
              "already printed:\n  " + failed, flush=True)

    if args.report is not None:
        body = "\n\n".join(collected)
        if failed is not None:
            body += f"\n\nVALIDATION FAILURE\n  {failed}"
        args.report.write_text(body + f"\n\ngenerated {dt.datetime.now():%Y-%m-%d %H:%M}\n",
                               encoding="utf-8")
        print(f"\nreport written to {args.report} — carries firm amounts; keep it local")
    return 0 if failed is None else 1


if __name__ == "__main__":
    raise SystemExit(main())

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
         floor_collapse: str = "balance_weighted") -> str:
    sections: list[str] = []
    quarters = PROJECTION_QUARTERS

    facilities, load_census = load_facilities(spec)
    balances, m1_census = load_category_balances(spec)
    merged_balance, merged_parts = load_merged_bucket_balance(spec)
    history, base_path, launch_3m = load_3m_treasury(spec, scenario, quarters, launch_point)

    sections.append(
        f"RUN SETTINGS\n"
        f"  workbook      : {spec.workbook}\n"
        f"  scenario      : {scenario}\n"
        f"  launch point  : {launch_point} (PQ0); PQ1..PQ9 follow\n"
        f"  3M at PQ0     : {launch_3m:.4%}   history quarters: {len(history)} "
        f"(earliest {min(history)})\n"
        f"  units         : USD millions; annualized decimal rates"
    )
    sections.append(load_census.render())
    if m1_census.warnings:
        sections.append("M.1 NOTES\n" + "\n".join(f"  {note}" for note in m1_census.warnings))

    m1_lines = ["M.1 CATEGORY BALANCES (cross-check: the FRB SCALARS sheet's 'Sch M bal' column)"]
    for name, value in sorted(balances.items(), key=lambda kv: -kv[1]):
        m1_lines.append(f"  {value:>12,.1f}  {name}")
    m1_lines.append(
        f"  {merged_balance:>12,.1f}  merged 9/10/11 bucket from FR Y-9C "
        f"({', '.join(f'{k} {v:,.1f}' for k, v in sorted(merged_parts.items()))})"
    )
    sections.append("\n".join(m1_lines))

    launch, launch_diagnostics = build_launch_point(
        facilities, balances, launch_3m, history, quarters,
        lambda when: projection_quarter_index(when, launch_point),
        floor_collapse=floor_collapse,
    )
    merged = merged_bucket_launch_point(
        facilities, merged_balance, launch_3m, DEPOSITORY_INSTITUTION_H1_CODES,
        FED_CATEGORY_NAMES[9], floor_collapse=floor_collapse,
    )
    sections.append(launch_diagnostics.render())
    sections.append(
        f"MERGED 9/10/11 BUCKET\n"
        f"  donor pool rate (depository floating) : {merged.spread.pool_rate:.4%}\n"
        f"  spread vs 3M(PQ0)                     : {merged.spread.spread:.4%}\n"
        f"  floor                                 : "
        + (f"{merged.floor:.4%}" if merged.floor is not None else "none on file")
    )

    scalars, scalar_warnings = scalars_by_category_name()
    projections, totals, projection_diagnostics = project_corporate(
        {**dict(launch), merged.segment: merged}, base_path, quarters, scalars
    )
    sections.append(projection_diagnostics.render())
    for warning in scalar_warnings:
        sections.append(f"WARN: {warning}")

    result_lines = ["PROJECTED CORPORATE LOAN INTEREST INCOME (scaled, USD millions)"]
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
    sections.append("\n".join(result_lines))

    return "\n\n".join(sections)


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

    if args.config is None:
        with tempfile.TemporaryDirectory() as scratch:
            workbook = _synthetic_workbook(Path(scratch))
            banner = ("SYNTHETIC DEMO — invented data, hand-checkable numbers. "
                      "Point --config at the company config for a real run.\n\n")
            output = banner + _run(
                LoansSheetSpec(workbook=workbook),
                args.scenario or "Supervisory Severely Adverse",
                args.launch_point or "2024Q4",
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
        output = format_effective_config(config) + "\n\n" + _run(
            loans.spec,
            args.scenario or loans.scenario,
            args.launch_point or loans.launch_point,
            loans.floor_collapse,
        )

    print(output)
    if args.report is not None:
        args.report.write_text(output + f"\n\ngenerated {dt.datetime.now():%Y-%m-%d %H:%M}\n",
                               encoding="utf-8")
        print(f"\nreport written to {args.report} — carries firm amounts; keep it local")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

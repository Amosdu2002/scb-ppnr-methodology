"""Trading NII + income family + combined NII, driven by a config file — the
Increment 4 compare runner.

    PYTHONPATH=src python3 examples/run_nii.py                        # synthetic demo
    PYTHONPATH=src python3 examples/run_nii.py \
        --config config/local/company.toml \
        --component-paths loans_paths.csv securities_paths.csv        # company run

Company workflow (three steps, each already familiar):
  1. python3 examples/run_loans.py      --config <cfg> --paths-out loans_paths.csv
  2. python3 examples/run_securities.py --config <cfg> --paths-out securities_paths.csv
  3. python3 examples/run_nii.py        --config <cfg> --component-paths loans_paths.csv securities_paths.csv

Step 3 computes the two Family A calculators itself, assembles the six sibling
income paths, prints the ROUND-0 DIAGNOSTIC (our implied trading-NII residual —
compare it against the workbook's "Implied FRB results" row FIRST, before
judging α), then runs the PID-TRD-1 calibration and the family reconciliation,
and finally — when the expense-side inputs are configured — the combined-NII
monitor against `frb_net_interest_income`.

Config needs (see config/company.template.toml): the two nii_trading_al spot
rows (PID-TRD-2 pair), the `family` quarterly rows incl. frb_total_interest_income,
and [mev]. Subtraction-basis knobs live in the FAMILY runners: loans
apply_scalar/retail_auto_scalar and securities --paths-basis (xr excludes
reinvestment income per PID-SEC-8) must mirror the workbook's own components
sheet. Amounts: USD MILLIONS per quarter (D-006), pre-hedge. Everything prints
the moment it is produced; --report is written even on failure."""

from __future__ import annotations

import argparse
import datetime as dt
from pathlib import Path

from scb_ppnr.consolidated import (
    consolidated_tables,
    write_consolidated_csv,
    write_consolidated_workbook,
)
from scb_ppnr.core.schemas import PROJECTION_QUARTERS, ValidationFailure
from scb_ppnr.ingestion import (
    load_config,
    load_family_inputs,
    load_income_inputs,
    load_mev_scenario,
)
from scb_ppnr.interest_expense import run_interest_expense_family
from scb_ppnr.interest_income import (
    SIBLING_MODEL_IDS,
    implied_trading_path,
    income_family_report,
    project_dep_banks_other,
    project_other_ida,
    run_interest_income_family,
    sibling_paths_from_results,
)
from scb_ppnr.nii_monitor import combined_nii_monitor, combined_nii_report_text

_CALCULATOR_IDS = ("ii_dep_banks_other", "ii_other_ida")
_CSV_IDS = tuple(m for m in SIBLING_MODEL_IDS if m not in _CALCULATOR_IDS)
_LOANS_PART_IDS = ("ii_loans_corporate", "ii_loans_cre", "ii_loans_retail")


def read_component_paths(files: list[Path]) -> dict[str, dict[int, float]]:
    """Read the wide component CSVs written by the family runners
    (component,PQ1..PQ9; USD millions, canonical — no scale column).
    `ii_loans` may arrive as one total row or as parts to be summed."""
    paths: dict[str, dict[int, float]] = {}
    known = set(_CSV_IDS) | set(_LOANS_PART_IDS)
    for file in files:
        lines = [line.strip() for line in file.read_text(encoding="utf-8").splitlines() if line.strip()]
        if not lines:
            raise ValidationFailure(f"{file}: empty component-paths file")
        header = [cell.strip() for cell in lines[0].split(",")]
        expected = ["component", *(f"PQ{q}" for q in PROJECTION_QUARTERS)]
        if header != expected:
            raise ValidationFailure(
                f"{file}: header {header} != {expected} — use the family runners' --paths-out output"
            )
        for line_no, line in enumerate(lines[1:], start=2):
            cells = [cell.strip() for cell in line.split(",")]
            if len(cells) != len(expected):
                raise ValidationFailure(f"{file} line {line_no}: expected {len(expected)} cells, got {len(cells)}")
            name = cells[0]
            if name not in known:
                raise ValidationFailure(
                    f"{file} line {line_no}: unknown component {name!r}; known: {sorted(known)} "
                    f"(the calculators are computed by this runner, not read from CSV)"
                )
            if name in paths:
                raise ValidationFailure(f"{file} line {line_no}: duplicate component {name!r}")
            try:
                paths[name] = {q: float(cells[i]) for i, q in enumerate(PROJECTION_QUARTERS, start=1)}
            except ValueError as exc:
                raise ValidationFailure(f"{file} line {line_no}: {exc}") from None
    return paths


def assemble_loans_total(paths: dict[str, dict[int, float]], emit) -> None:
    """Ensure an `ii_loans` entry: use the total row when present, else sum the
    supplied parts (with a printed census of what went in)."""
    parts = [name for name in _LOANS_PART_IDS if name in paths]
    if "ii_loans" in paths:
        if parts:
            total = {q: sum(paths[name][q] for name in parts) for q in PROJECTION_QUARTERS}
            gap = max(abs(total[q] - paths["ii_loans"][q]) for q in PROJECTION_QUARTERS)
            emit(f"LOANS PATHS: total row present alongside parts {parts}; using the total row "
                 f"(max |total − Σparts| = {gap:.6f})")
            for name in parts:
                del paths[name]
        return
    if not parts:
        raise ValidationFailure(
            "component paths carry no ii_loans row and no ii_loans_* parts — run "
            "run_loans.py --paths-out first (full run for the total row)"
        )
    emit(f"LOANS PATHS: no total row — summing parts {parts} into ii_loans "
         f"(a partial loans run understates the residual; prefer a full run)")
    paths["ii_loans"] = {q: sum(paths[name][q] for name in parts) for q in PROJECTION_QUARTERS}
    for name in parts:
        del paths[name]


def _path_row(label: str, path, total=None) -> str:
    total = sum(path[q] for q in PROJECTION_QUARTERS) if total is None else total
    return (label.ljust(22) + "".join(f"{path[q]:9.3f}" for q in PROJECTION_QUARTERS)
            + f"{total:11.3f}")


def _synthetic_defaults() -> tuple[Path, list[Path]]:
    examples = Path(__file__).parent
    return (examples / "synthetic_config.toml",
            [examples / "synthetic_data" / "component_paths.csv"])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--config", type=Path, default=None,
                        help="company config (spot/quarterly sheets incl. the nii_trading_al pair "
                             "and frb_total_interest_income; [mev]); omit for the synthetic demo")
    parser.add_argument("--scenario", default=None,
                        help="scenario id; defaults to the only/first configured one")
    parser.add_argument("--component-paths", type=Path, nargs="+", default=None,
                        help="one or more --paths-out CSVs from run_loans.py / run_securities.py")
    parser.add_argument("--skip-expense", action="store_true",
                        help="skip the expense family + combined-NII monitor even if configured")
    parser.add_argument("--report", type=Path, default=None,
                        help="also write the output to this file (keep it local)")
    parser.add_argument("--consolidated-out", type=Path, default=None,
                        help="write a consolidated results workbook (Summary/Income/Expense "
                             "sheets) to this .xlsx path, plus a flat .csv twin of the "
                             "quarterly paths; carries firm amounts — keep it local")
    args = parser.parse_args(argv)

    sections: list[str] = []

    def emit(text: str) -> None:
        print(text, end="\n\n", flush=True)
        sections.append(text)

    failed: str | None = None
    try:
        if args.config is None:
            config_path, path_files = _synthetic_defaults()
            emit("SYNTHETIC DEMO — invented component paths + the committed synthetic sheets. "
                 "Point --config / --component-paths at company files for a real run.")
        else:
            config_path = args.config
            if args.component_paths is None:
                raise ValidationFailure(
                    "--component-paths is required for a company run: feed the --paths-out CSVs "
                    "from run_loans.py and run_securities.py (steps 1–2 in this runner's header)"
                )
            path_files = list(args.component_paths)
        if args.component_paths is not None:
            path_files = list(args.component_paths)

        config = load_config(config_path)
        if config.mev is None:
            raise ValidationFailure("config has no [mev] section")
        scenario_id = args.scenario or next(iter(config.mev.scenarios))
        mev = load_mev_scenario(config, scenario_id)
        scenario = mev.interest_income_scenario_paths()

        family = load_income_inputs(config)
        if family.trading is None:
            raise ValidationFailure(
                "spot sheet carries no nii_trading_al rows — add the PID-TRD-2 pair "
                "(trading_assets_avg_balance / trading_liabilities_avg_balance; see "
                "config/company.template.toml)"
            )
        if family.frb_total_interest_income is None:
            raise ValidationFailure(
                "quarterly sheet carries no family.frb_total_interest_income row — the "
                "PID-TRD-1 calibration target (see config/company.template.toml)"
            )

        emit(f"NII TRADING A&L + INCOME FAMILY — proposed 2026 suite, NOT adopted\n"
             f"firm: {family.firm_id}   scenario: {scenario.scenario_id}   config: {config_path}\n"
             f"component paths: {', '.join(str(f) for f in path_files)}\n"
             f"trading inputs: assets {family.trading.trading_assets_avg_balance:,.1f} − "
             f"liabilities {family.trading.trading_liabilities_avg_balance:,.1f} = "
             f"NetTA {family.trading.net_trading_assets:,.1f} (PID-TRD-2; flat)\n"
             f"AMOUNTS: USD MILLIONS per quarter — canonical unit, D-006; pre-hedge\n"
             f"BASIS NOTE: the residual is only as aligned as the component basis — loans "
             f"apply_scalar/retail_auto_scalar and securities --paths-basis (xr = reinvestment "
             f"excluded, PID-SEC-8) must mirror the workbook's own components sheet")

        csv_paths = read_component_paths(path_files)
        loans_parts = {name: dict(path) for name, path in csv_paths.items()
                       if name in _LOANS_PART_IDS}
        assemble_loans_total(csv_paths, emit)

        calculators = sibling_paths_from_results(
            firm_id=family.firm_id, scenario_id=scenario.scenario_id,
            ii_dep_banks_other=project_dep_banks_other(family.dep_banks_other, scenario),
            ii_other_ida=project_other_ida(family.other_ida, scenario),
        )
        overlap = sorted(set(csv_paths) & set(calculators))
        if overlap:
            raise ValidationFailure(
                f"component CSVs also carry {overlap} — the calculators are computed by this "
                f"runner from the spot sheet; remove those rows"
            )
        sibling_paths = {**csv_paths, **calculators}

        table = ["COMPONENT INCOME PATHS (USD millions per quarter)"]
        table.append("component".ljust(22)
                     + "".join(f"PQ{q}".rjust(9) for q in PROJECTION_QUARTERS) + "     total".rjust(11))
        for model_id in SIBLING_MODEL_IDS:
            table.append(_path_row(model_id, sibling_paths[model_id]))
        table.append(_path_row("sum of siblings", {
            q: sum(path[q] for path in sibling_paths.values()) for q in PROJECTION_QUARTERS
        }))
        table.append(_path_row("frb_income (target)", family.frb_total_interest_income))
        emit("\n".join(table))

        # ROUND-0 DIAGNOSTIC first (the retail-rounds lesson): the implied path
        # inherits every sibling's convergence error — judge it before α.
        implied = implied_trading_path(family.frb_total_interest_income, sibling_paths)
        emit("ROUND-0 DIAGNOSTIC — implied trading NII (compare against the workbook's "
             "'Implied FRB results' row FIRST):\n"
             + _path_row("implied TATL", implied))

        result = run_interest_income_family(
            firm_id=family.firm_id,
            scenario=scenario,
            sibling_income_paths=sibling_paths,
            trading=family.trading,
            frb_total_interest_income=family.frb_total_interest_income,
        )
        emit(income_family_report(result, family.frb_total_interest_income))

        expense_family = None
        expense_result = None
        monitor = None
        if args.skip_expense:
            emit("COMBINED NII: skipped (--skip-expense)")
        else:
            try:
                expense_family = load_family_inputs(config)
            except ValidationFailure as error:
                expense_family = None
                emit(f"COMBINED NII: skipped — expense-side inputs not loadable from this "
                     f"config ({error})")
            else:
                expense_scenario = mev.interest_expense_scenario_paths()
                expense_result = run_interest_expense_family(expense_family, expense_scenario)
                expense_total = {
                    q: sum(r.expense_path()[q] for r in expense_result.results.values())
                    for q in PROJECTION_QUARTERS
                }
                monitor = combined_nii_monitor(
                    result.total_income_path(), expense_total,
                    frb_net_interest_income=family.frb_net_interest_income,
                )
                emit(combined_nii_report_text(monitor))

        if args.consolidated_out is not None:
            tables = consolidated_tables(
                income_result=result,
                implied_path=implied,
                loans_parts=loans_parts,
                frb_total_interest_income=family.frb_total_interest_income,
                expense_result=expense_result,
                frb_total_interest_expense=(expense_family.frb_total_interest_expense
                                            if expense_family is not None else None),
                monitor=monitor,
                generated=f"{dt.datetime.now():%Y-%m-%d %H:%M}",
            )
            csv_twin = args.consolidated_out.with_suffix(".csv")
            write_consolidated_csv(tables, csv_twin)
            try:
                write_consolidated_workbook(tables, args.consolidated_out)
            except ImportError:
                emit(f"CONSOLIDATED: workbook skipped (openpyxl not installed) — quarterly "
                     f"paths written to {csv_twin}")
            else:
                emit(f"CONSOLIDATED: results written to {args.consolidated_out} "
                     f"(+ {csv_twin.name}) — carries firm amounts; keep it local")
    except ValidationFailure as error:
        failed = str(error)
        print("\nVALIDATION FAILURE — the run stopped here; every section above "
              "already printed:\n  " + failed, flush=True)

    if args.report is not None:
        body = "\n\n".join(sections)
        if failed is not None:
            body += f"\n\nVALIDATION FAILURE\n  {failed}"
        args.report.write_text(body + f"\n\ngenerated {dt.datetime.now():%Y-%m-%d %H:%M}\n",
                               encoding="utf-8")
        print(f"\nreport written to {args.report} — carries firm amounts; keep it local")
    return 0 if failed is None else 1


if __name__ == "__main__":
    raise SystemExit(main())

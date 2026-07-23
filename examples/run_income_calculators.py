"""Family A interest-income calculators driven by a config file — the company workflow.

    PYTHONPATH=src python3 examples/run_income_calculators.py
    PYTHONPATH=src python3 examples/run_income_calculators.py \
        --config config/local/company.toml --scenario severely_adverse

Defaults to the fully synthetic demo (examples/synthetic_config.toml). Point
--config at your company-local config built from config/company.template.toml;
this repository never contains company paths, sheets, or data. Runs the two
Increment 1 calculators only — the income orchestrator, trading NII, and the
family reconciliation monitor arrive in later increments."""

from __future__ import annotations

import argparse
from pathlib import Path

from scb_ppnr.ingestion import load_config, load_income_inputs, load_mev_scenario
from scb_ppnr.interest_income import (
    IncomeModelResult,
    project_dep_banks_other,
    project_other_ida,
)
from scb_ppnr.interest_income.schemas import PROJECTION_QUARTERS


def _print_model(result: IncomeModelResult) -> None:
    print(f"\n{result.model_id}  [{result.validation_status}]")
    header = "  ".join(f"   PQ{q}" for q in PROJECTION_QUARTERS)
    rates = "  ".join(f"{result.rate_path()[q] * 100:6.3f}" for q in PROJECTION_QUARTERS)
    income = "  ".join(f"{result.income_path()[q]:6.2f}" for q in PROJECTION_QUARTERS)
    print(f"  quarter          {header}")
    print(f"  rate (% ann.)    {rates}")
    print(f"  income           {income}")
    print(f"  9-quarter cumulative income: {result.cumulative_income:.2f}")
    for warning in result.warnings:
        print(f"  warning: {warning}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default=Path(__file__).parent / "synthetic_config.toml")
    parser.add_argument("--scenario", default=None, help="scenario id; defaults to the only/first configured one")
    args = parser.parse_args()

    config = load_config(args.config)
    if config.mev is None:
        raise SystemExit("config has no [mev] section")
    scenario_id = args.scenario or next(iter(config.mev.scenarios))

    scenario = load_mev_scenario(config, scenario_id).interest_income_scenario_paths()
    family = load_income_inputs(config)

    print("INTEREST-INCOME FAMILY A (calculators) — proposed 2026 suite, NOT adopted")
    print(f"firm: {family.firm_id}   scenario: {scenario.scenario_id}")
    print("AMOUNTS: USD MILLIONS per quarter — canonical unit, D-006; pre-hedge")

    _print_model(project_dep_banks_other(family.dep_banks_other, scenario))
    _print_model(project_other_ida(family.other_ida, scenario))


if __name__ == "__main__":
    main()

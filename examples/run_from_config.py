"""End-to-end run driven by a config file plus data files — the company workflow.

    PYTHONPATH=src python3 examples/run_from_config.py
    PYTHONPATH=src python3 examples/run_from_config.py \
        --config config/local/company.toml --scenario severely_adverse

Defaults to the fully synthetic demo (examples/synthetic_config.toml). Point
--config at your company-local config built from config/company.template.toml;
this repository never contains company paths, sheets, or data."""

from __future__ import annotations

import argparse
from pathlib import Path

from scb_ppnr.ingestion import load_config, load_family_inputs, load_mev_scenario
from scb_ppnr.interest_expense import family_report, run_interest_expense_family


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default=Path(__file__).parent / "synthetic_config.toml")
    parser.add_argument("--scenario", default=None, help="scenario id; defaults to the only/first configured one")
    args = parser.parse_args()

    config = load_config(args.config)
    if config.mev is None:
        raise SystemExit("config has no [mev] section")
    scenario_id = args.scenario or next(iter(config.mev.scenarios))

    scenario = load_mev_scenario(config, scenario_id).interest_expense_scenario_paths()
    family = load_family_inputs(config)
    result = run_interest_expense_family(family, scenario)
    print(family_report(result, family.frb_total_interest_expense))


if __name__ == "__main__":
    main()

"""End-to-end interest-expense run driven by a config file — the company workflow.

    PYTHONPATH=src python3 examples/run_from_config.py
    PYTHONPATH=src python3 examples/run_from_config.py \
        --config config/local/company.toml --scenario severely_adverse

Defaults to the fully synthetic demo (examples/synthetic_config.toml). Point
--config at your company-local config built from config/company.template.toml;
this repository never contains company paths, sheets, or data. run.py at the
repo root invokes this runner as its expense stage."""

from __future__ import annotations

import argparse
import datetime as dt
from pathlib import Path

from scb_ppnr.core.schemas import ValidationFailure
from scb_ppnr.ingestion import load_config, load_family_inputs, load_mev_scenario
from scb_ppnr.interest_expense import family_report, run_interest_expense_family


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--config", type=Path,
                        default=Path(__file__).parent / "synthetic_config.toml")
    parser.add_argument("--scenario", default=None,
                        help="scenario id; defaults to the only/first configured one")
    parser.add_argument("--report", type=Path, default=None,
                        help="also write the output to this file (keep it local)")
    args = parser.parse_args(argv)

    sections: list[str] = []
    failed: str | None = None
    try:
        config = load_config(args.config)
        if config.mev is None:
            raise ValidationFailure("config has no [mev] section")
        scenario_id = args.scenario or next(iter(config.mev.scenarios))

        scenario = load_mev_scenario(config, scenario_id).interest_expense_scenario_paths()
        family = load_family_inputs(config)
        result = run_interest_expense_family(family, scenario)
        report = family_report(result, family.frb_total_interest_expense)
        print(report, flush=True)
        sections.append(report)
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

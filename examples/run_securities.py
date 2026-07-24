"""Securities family (ii_ust / ii_mbs / ii_other_sec) driven by a config file.

    PYTHONPATH=src python3 examples/run_securities.py                       # synthetic demo
    PYTHONPATH=src python3 examples/run_securities.py \
        --config config/local/company.toml --scenario severely_adverse      # company run

The company config needs a [firm_data.securities] section (PID-SEC-6 — see
config/company.template.toml). The synthetic demo generates a small in-memory
workbook (invented securities, hand-calculable numbers) so no .xlsx is committed.
Requires openpyxl. Output amounts: USD MILLIONS per quarter (D-006), pre-hedge."""

from __future__ import annotations

import argparse
import datetime as dt
import tempfile
from pathlib import Path

from scb_ppnr.ingestion import load_config, load_mev_scenario, load_securities_inputs
from scb_ppnr.ingestion.config import (
    FirmDataConfig,
    IngestionConfig,
    SecuritiesConfig,
    SecuritiesEnrichmentSheet,
    TableSource,
)
from scb_ppnr.interest_income import (
    FLOOR_MODE_SECURITY,
    IncomeModelResult,
    IncomeScenarioPaths,
    project_mbs,
    project_other_sec,
    project_ust,
)
from scb_ppnr.interest_income.schemas import PROJECTION_QUARTERS


def _print_model(result: IncomeModelResult) -> None:
    print(f"\n{result.model_id}  [{result.validation_status}]")
    print("  quarter        " + "  ".join(f"   PQ{q}" for q in PROJECTION_QUARTERS))
    print("  income         " + "  ".join(f"{result.income_path()[q]:7.2f}" for q in PROJECTION_QUARTERS))
    diag = [result.quarters[q - 1].diagnostics for q in PROJECTION_QUARTERS]
    print("  coupon leg     " + "  ".join(f"{d.coupon_accrual:7.2f}" for d in diag))
    print("  accretion leg  " + "  ".join(f"{d.accretion:7.2f}" for d in diag))
    print("  reinvested     " + "  ".join(f"{d.reinvested_income:7.2f}" for d in diag))
    print(f"  9-quarter cumulative income: {result.cumulative_income:.2f}")
    for warning in result.warnings:
        print(f"  warning: {warning}")


def _synthetic_demo() -> tuple[IngestionConfig, IncomeScenarioPaths]:
    import openpyxl

    tmp = Path(tempfile.mkdtemp(prefix="scb_ppnr_securities_demo_"))
    epoch = dt.date(1899, 12, 30)
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Positions"
    mdrm = ["D_DT", "CQSCP083", "CQSCP084", "CQSCP087", "CQSCP089", "CQSCP090", "CQSCP092", "CQSCP094", "CQSCJH21"]
    for filler in (["_"] * len(mdrm), ["tech"] * len(mdrm), ["desc"] * len(mdrm)):
        ws.append(filler)
    ws.append(mdrm)
    ws.append([20241231, "DEMOUST01", "US Treasuries & Agencies", 960e6, 1000e6, 1000e6, "AFS", 4.2, None])
    ws.append([20241231, "DEMOAGY01", "Agency MBS", 950e6, 1000e6, 1200e6, "AFS", 5.0, None])
    ws.append([20241231, "DEMOOTH01", "Corporate Bond", 2000e6, 2000e6, 2000e6, "AFS", 5.0, None])
    ito = wb.create_sheet("ITO")
    ito.append(["CUSIP", "Maturity Date", "Coupon Rate", "CPN_TYP", "CPN_Floor", "WAL"])
    ito.append(["DEMOUST01", (dt.date(2025, 12, 31) - epoch).days, 4.0, "FIXED", None, None])
    ito.append(["DEMOAGY01", None, 5.0, "FIXED", None, 2.5])
    ito.append(["DEMOOTH01", (dt.date(2035, 6, 30) - epoch).days, 5.0, "FIXED", None, None])
    prepay = wb.create_sheet("prepay")
    prepay.append(["Sum of current_face", "Column Labels"])
    prepay.append(["Row Labels", 0, 3, 6, 9, 12, 15, 18, 21, 24, 27, "Grand Total"])
    prepay.append(["DEMOAGY01", 1000e6, 800e6, 800e6, 800e6, 800e6, 800e6, 800e6, 800e6, 800e6, 800e6, 0])
    wb.save(tmp / "securities.xlsx")

    config = IngestionConfig(
        base_dir=tmp,
        firm_data=FirmDataConfig(
            firm_id="SYNTHETIC_FIRM",
            spot=TableSource(Path("unused.csv")),
            quarterly=TableSource(Path("unused.csv")),
            securities=SecuritiesConfig(
                workbook=Path("securities.xlsx"), positions_sheet="Positions",
                money_scale="dollars", coupon_scale="percent", book_yield_scale="percent",
                floor_mode=FLOOR_MODE_SECURITY, prepayment_sheet="prepay",
                enrichment=(SecuritiesEnrichmentSheet(
                    sheet="ITO", key_column="CUSIP", maturity_column="Maturity Date",
                    coupon_column="Coupon Rate", rate_type_column="CPN_TYP",
                    wal_column="WAL", floor_column="CPN_Floor", header_row=1,
                ),),
            ),
        ),
    )
    flat = {q: 0.0400 for q in PROJECTION_QUARTERS}
    scenario = IncomeScenarioPaths(
        scenario_id="synthetic_demo",
        usd_3m_treasury={0: 0.0300, **{q: 0.0300 for q in PROJECTION_QUARTERS}},
        usd_1y_treasury=flat,
        usd_10y_treasury={q: 0.0450 for q in PROJECTION_QUARTERS},
        prime_rate={q: 0.0700 for q in PROJECTION_QUARTERS},
        mortgage_rate={q: 0.0650 for q in PROJECTION_QUARTERS},
    )
    return config, scenario


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default=None, help="company-local config with [firm_data.securities]")
    parser.add_argument("--scenario", default=None, help="scenario id (company runs)")
    args = parser.parse_args()

    if args.config is None:
        config, scenario = _synthetic_demo()
        print("SYNTHETIC DEMO (generated workbook — invented securities)")
    else:
        config = load_config(args.config)
        if config.mev is None:
            raise SystemExit("config has no [mev] section")
        scenario_id = args.scenario or next(iter(config.mev.scenarios))
        scenario = load_mev_scenario(config, scenario_id).interest_income_scenario_paths()

    inputs = load_securities_inputs(config)
    floor_mode = config.firm_data.securities.floor_mode
    on_error = config.firm_data.securities.on_security_error

    print(f"firm: {inputs.firm_id}   scenario: {scenario.scenario_id}   "
          f"floor_mode: {floor_mode}   on_security_error: {on_error}")
    print("AMOUNTS: USD MILLIONS per quarter — canonical unit, D-006; pre-hedge")
    for warning in inputs.warnings:
        print(f"loader warning: {warning}")

    _print_model(project_ust(inputs.ust, scenario, firm_id=inputs.firm_id, on_error=on_error))
    _print_model(project_mbs(inputs.mbs, scenario, firm_id=inputs.firm_id, floor_mode=floor_mode, on_error=on_error))
    _print_model(project_other_sec(inputs.other_sec, scenario, firm_id=inputs.firm_id, floor_mode=floor_mode, on_error=on_error))


if __name__ == "__main__":
    main()

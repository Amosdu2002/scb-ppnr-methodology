"""Income-side ingestion: load_income_inputs from the committed synthetic sheets,
the four-series income scenario selector, D-006/D-007 normalization on income
rows, and sheet-placement enforcement for income fields."""

from __future__ import annotations

from pathlib import Path

import pytest

from scb_ppnr.ingestion import load_config, load_income_inputs, load_mev_scenario
from scb_ppnr.ingestion.config import FirmDataConfig, IngestionConfig, TableSource
from scb_ppnr.ingestion.firm_data_loader import load_family_inputs
from scb_ppnr.interest_income import ValidationFailure
from scb_ppnr.interest_income.schemas import PROJECTION_QUARTERS

ROOT = Path(__file__).resolve().parents[3]
SYNTHETIC_SPOT = ROOT / "examples" / "synthetic_data" / "firm_inputs_spot.csv"


def test_synthetic_spot_sheet_loads_income_inputs():
    config = load_config(ROOT / "examples" / "synthetic_config.toml")
    family = load_income_inputs(config)
    assert family.firm_id == "SYNTHETIC_FIRM"
    assert family.dep_banks_other.balance == pytest.approx(1000.0)
    assert family.other_ida.total_balance == pytest.approx(2000.0)
    assert family.other_ida.short_rate_share == pytest.approx(0.60)


def test_income_scenario_selector_windows_and_scales():
    config = load_config(ROOT / "examples" / "synthetic_config.toml")
    scenario = load_mev_scenario(config, "synthetic_severely_adverse").interest_income_scenario_paths()
    # 3M carries PQ0 (2025Q4 actuals row, 3.00% → 0.0300); the others are PQ1..PQ9 only.
    assert scenario.usd_3m_treasury[0] == pytest.approx(0.0300)
    assert scenario.usd_3m_treasury[1] == pytest.approx(0.0400)
    assert set(scenario.usd_10y_treasury) == set(PROJECTION_QUARTERS)
    assert scenario.usd_10y_treasury[1] == pytest.approx(0.0450)
    assert scenario.usd_10y_treasury[9] == pytest.approx(0.0445)
    assert scenario.prime_rate[1] == pytest.approx(0.0700)
    assert scenario.mortgage_rate[1] == pytest.approx(0.0650)


def _config_with(tmp_path: Path, spot_text: str | None = None, quarterly_text: str | None = None) -> IngestionConfig:
    spot = SYNTHETIC_SPOT
    if spot_text is not None:
        spot = tmp_path / "spot.csv"
        spot.write_text(spot_text, encoding="utf-8")
    quarterly = tmp_path / "quarterly.csv"
    if quarterly_text is None:
        quarterly_text = (
            "model,field,subcomponent,scale," + ",".join(f"PQ{q}" for q in PROJECTION_QUARTERS) + "\n"
            "family,frb_total_interest_expense,,millions," + ",".join(["40"] * 9) + "\n"
        )
    quarterly.write_text(quarterly_text, encoding="utf-8")
    return IngestionConfig(
        base_dir=tmp_path,
        firm_data=FirmDataConfig(firm_id="FIRM_T", spot=TableSource(spot), quarterly=TableSource(quarterly)),
    )


def test_missing_income_row_surfaces(tmp_path):
    spot_text = (
        "model,field,subcomponent,scale,value\n"
        "ii_dep_banks_other,balance,,millions,1000\n"
        "ii_other_ida,total_balance,,millions,2000\n"
    )
    config = _config_with(tmp_path, spot_text=spot_text)
    with pytest.raises(ValidationFailure, match="missing required inputs: ii_other_ida.short_rate_share"):
        load_income_inputs(config)


def test_percent_scaled_share_normalizes(tmp_path):
    spot_text = (
        "model,field,subcomponent,scale,value\n"
        "ii_dep_banks_other,balance,,billions,1\n"
        "ii_other_ida,total_balance,,millions,2000\n"
        "ii_other_ida,short_rate_share,,percent,60\n"
    )
    config = _config_with(tmp_path, spot_text=spot_text)
    family = load_income_inputs(config)
    assert family.dep_banks_other.balance == pytest.approx(1000.0)  # billions → USD millions (D-006)
    assert family.other_ida.short_rate_share == pytest.approx(0.60)  # percent → decimal


def test_income_spot_field_rejected_on_quarterly_sheet(tmp_path):
    quarterly_text = (
        "model,field,subcomponent,scale," + ",".join(f"PQ{q}" for q in PROJECTION_QUARTERS) + "\n"
        "family,frb_total_interest_expense,,millions," + ",".join(["40"] * 9) + "\n"
        "ii_other_ida,short_rate_share,,decimal," + ",".join(["0.6"] * 9) + "\n"
    )
    config = _config_with(tmp_path, quarterly_text=quarterly_text)
    with pytest.raises(ValidationFailure, match="belongs in the spot sheet"):
        load_family_inputs(config)

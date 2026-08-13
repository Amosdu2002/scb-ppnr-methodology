"""Trading-NII ingestion (Increment 4): the PID-TRD-2 spot pair on the D-007
spot sheet (both rows or neither), the FRB family income/NII paths picked up
from the quarterly sheet when declared, and D-006 scale normalization."""

from __future__ import annotations

from pathlib import Path

import pytest

from scb_ppnr.ingestion import load_config, load_income_inputs
from scb_ppnr.ingestion.config import FirmDataConfig, IngestionConfig, TableSource
from scb_ppnr.interest_income import ValidationFailure
from scb_ppnr.interest_income.schemas import PROJECTION_QUARTERS

ROOT = Path(__file__).resolve().parents[3]

_CALCULATOR_ROWS = (
    "model,field,subcomponent,scale,value\n"
    "ii_dep_banks_other,balance,,millions,1000\n"
    "ii_other_ida,total_balance,,millions,2000\n"
    "ii_other_ida,short_rate_share,,decimal,0.6\n"
)
_QUARTERLY_HEADER = "model,field,subcomponent,scale," + ",".join(f"PQ{q}" for q in PROJECTION_QUARTERS) + "\n"


def _config(tmp_path: Path, spot_text: str, quarterly_text: str | None = None) -> IngestionConfig:
    spot = tmp_path / "spot.csv"
    spot.write_text(spot_text, encoding="utf-8")
    quarterly = None
    if quarterly_text is not None:
        quarterly_file = tmp_path / "quarterly.csv"
        quarterly_file.write_text(quarterly_text, encoding="utf-8")
        quarterly = TableSource(quarterly_file)
    return IngestionConfig(
        base_dir=tmp_path,
        firm_data=FirmDataConfig(firm_id="FIRM_T", spot=TableSource(spot), quarterly=quarterly),
    )


def test_trading_pair_loads_with_scale_normalization(tmp_path):
    spot_text = _CALCULATOR_ROWS + (
        "nii_trading_al,trading_assets_avg_balance,,millions,1500\n"
        "nii_trading_al,trading_liabilities_avg_balance,,billions,0.5\n"   # 0.5 B → 500 M (D-006)
    )
    family = load_income_inputs(_config(tmp_path, spot_text))
    assert family.trading is not None
    assert family.trading.trading_assets_avg_balance == pytest.approx(1500.0)
    assert family.trading.trading_liabilities_avg_balance == pytest.approx(500.0)
    assert family.trading.net_trading_assets == pytest.approx(1000.0)


def test_trading_rows_absent_is_a_legal_calculator_only_run(tmp_path):
    family = load_income_inputs(_config(tmp_path, _CALCULATOR_ROWS))
    assert family.trading is None
    assert family.frb_total_interest_income is None


def test_lone_trading_leg_is_refused(tmp_path):
    spot_text = _CALCULATOR_ROWS + "nii_trading_al,trading_assets_avg_balance,,millions,1500\n"
    with pytest.raises(ValidationFailure, match="pair.*trading_liabilities_avg_balance"):
        load_income_inputs(_config(tmp_path, spot_text))


def test_frb_income_paths_read_from_quarterly_sheet_when_declared(tmp_path):
    quarterly_text = _QUARTERLY_HEADER + (
        "family,frb_total_interest_expense,,millions," + ",".join(["40"] * 9) + "\n"
        "family,frb_total_interest_income,,millions," + ",".join(["100"] * 9) + "\n"
        "family,frb_net_interest_income,,millions," + ",".join(["60"] * 9) + "\n"
    )
    family = load_income_inputs(_config(tmp_path, _CALCULATOR_ROWS, quarterly_text))
    assert family.frb_total_interest_income is not None
    assert all(family.frb_total_interest_income[q] == pytest.approx(100.0) for q in PROJECTION_QUARTERS)
    assert all(family.frb_net_interest_income[q] == pytest.approx(60.0) for q in PROJECTION_QUARTERS)


def test_synthetic_config_now_carries_the_frb_income_paths():
    config = load_config(ROOT / "examples" / "synthetic_config.toml")
    family = load_income_inputs(config)
    # The committed synthetic quarterly sheet carries all three family paths;
    # income and NII pass through as-entered (D-008).
    assert all(family.frb_total_interest_income[q] == pytest.approx(100.0) for q in PROJECTION_QUARTERS)
    assert all(family.frb_net_interest_income[q] == pytest.approx(60.0) for q in PROJECTION_QUARTERS)
    # And the synthetic spot sheet carries the PID-TRD-2 trading pair, matching
    # the unit-test hand fixture (1500 − 500 → NetTA 1000).
    assert family.trading is not None
    assert family.trading.net_trading_assets == pytest.approx(1000.0)


def test_trading_field_rejected_on_quarterly_sheet(tmp_path):
    quarterly_text = _QUARTERLY_HEADER + (
        "nii_trading_al,trading_assets_avg_balance,,millions," + ",".join(["1500"] * 9) + "\n"
    )
    with pytest.raises(ValidationFailure, match="belongs in the spot sheet"):
        load_income_inputs(_config(tmp_path, _CALCULATOR_ROWS, quarterly_text))

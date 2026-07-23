"""ii_dep_banks_other (Eq A39) — hand-calculable fixture: item-14 balance 1000,
Treasury3m flat 4% → rate exactly 0.04 and income 1000 × 0.04 / 4 = 10 per quarter;
the income path is exactly proportional to the Treasury3m path."""

from __future__ import annotations

import pytest

from scb_ppnr.interest_income import DepBanksOtherInputs, project_dep_banks_other
from scb_ppnr.interest_income.schemas import PROJECTION_QUARTERS
from conftest import flat

FIRM = DepBanksOtherInputs("FIRM_A", balance=1000.0)


def test_hand_income_and_flat_balance(make_income_scenario):
    scenario = make_income_scenario(t3m={0: 0.0400, **flat(0.0400)})
    result = project_dep_banks_other(FIRM, scenario)
    assert all(q.quarterly_income == pytest.approx(10.0) for q in result.quarters)
    assert all(q.average_balance == 1000.0 for q in result.quarters)
    assert result.validation_status == "passed"


def test_rate_is_contemporaneous_treasury3m(make_income_scenario):
    scenario = make_income_scenario()
    result = project_dep_banks_other(FIRM, scenario)
    for row in result.quarters:
        assert row.annualized_rate == scenario.usd_3m_treasury[row.quarter]  # no spread, no lag
        assert row.diagnostics.usd_3m_treasury == row.annualized_rate


def test_income_proportional_to_treasury_path(make_income_scenario):
    base = project_dep_banks_other(FIRM, make_income_scenario())
    doubled_t3m = {q: 2.0 * v for q, v in make_income_scenario().usd_3m_treasury.items()}
    scaled = project_dep_banks_other(FIRM, make_income_scenario(t3m=doubled_t3m))
    for q_base, q_scaled in zip(base.quarters, scaled.quarters):
        assert q_scaled.quarterly_income == pytest.approx(2.0 * q_base.quarterly_income)


def test_zero_balance_warns_and_yields_zero(make_income_scenario):
    result = project_dep_banks_other(DepBanksOtherInputs("FIRM_A", 0.0), make_income_scenario())
    assert all(q.quarterly_income == 0.0 for q in result.quarters)
    assert result.validation_status == "passed_with_warnings"
    assert any("identically zero" in w for w in result.warnings)


def test_negative_treasury_logged_never_clamped(make_income_scenario):
    t3m = {0: 0.0100, 1: -0.0100, **{q: 0.0100 for q in PROJECTION_QUARTERS if q != 1}}
    result = project_dep_banks_other(FIRM, make_income_scenario(t3m=t3m))
    assert result.quarters[0].annualized_rate == pytest.approx(-0.0100)
    assert result.quarters[0].quarterly_income == pytest.approx(-2.5)
    assert any("negative Treasury3m" in w for w in result.warnings)

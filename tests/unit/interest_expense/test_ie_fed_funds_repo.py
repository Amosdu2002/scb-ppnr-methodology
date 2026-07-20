"""ie_fed_funds_repo (Eq A48) — hand-calculable fixture: balance 600 + 400 = 1000,
Treasury3m flat 4% → rate exactly 0.04 and expense 1000 × 0.04 / 4 = 10 per quarter;
the expense path is exactly proportional to the Treasury3m path."""

from __future__ import annotations

import pytest

from scb_ppnr.interest_expense import FedFundsRepoInputs, project_fed_funds_repo
from scb_ppnr.interest_expense.schemas import PROJECTION_QUARTERS
from conftest import flat

FIRM = FedFundsRepoInputs("FIRM_A", fed_funds_purchased_balance=600.0, repo_sold_balance=400.0)


def test_balance_aggregation(make_scenario):
    result = project_fed_funds_repo(FIRM, make_scenario())
    assert all(q.average_balance == 1000.0 for q in result.quarters)
    diag = result.quarters[0].diagnostics
    assert diag.fed_funds_purchased_balance == 600.0
    assert diag.repo_sold_balance == 400.0


def test_rate_is_contemporaneous_treasury3m(make_scenario):
    scenario = make_scenario()
    result = project_fed_funds_repo(FIRM, scenario)
    for row in result.quarters:
        assert row.annualized_rate == scenario.usd_3m_treasury[row.quarter]  # no spread, no lag


def test_hand_expense_and_flat_balance(make_scenario):
    scenario = make_scenario(t3m={0: 0.0400, **flat(0.0400)})
    result = project_fed_funds_repo(FIRM, scenario)
    assert all(q.quarterly_expense == pytest.approx(10.0) for q in result.quarters)


def test_expense_proportional_to_treasury_path(make_scenario):
    base = project_fed_funds_repo(FIRM, make_scenario())
    doubled = make_scenario(t3m={q: 2.0 * v for q, v in make_scenario().usd_3m_treasury.items()})
    scaled = project_fed_funds_repo(FIRM, doubled)
    for q_base, q_scaled in zip(base.quarters, scaled.quarters):
        assert q_scaled.quarterly_expense == pytest.approx(2.0 * q_base.quarterly_expense)


def test_both_zero_balances_warn_and_yield_zero(make_scenario):
    inputs = FedFundsRepoInputs("FIRM_A", 0.0, 0.0)
    result = project_fed_funds_repo(inputs, make_scenario())
    assert all(q.quarterly_expense == 0.0 for q in result.quarters)
    assert result.validation_status == "passed_with_warnings"
    assert any("identically zero" in w for w in result.warnings)


def test_negative_treasury_logged_never_clamped(make_scenario):
    t3m = {0: 0.0100, 1: -0.0100, **{q: 0.0100 for q in PROJECTION_QUARTERS if q != 1}}
    result = project_fed_funds_repo(FIRM, make_scenario(t3m=t3m))
    assert result.quarters[0].annualized_rate == pytest.approx(-0.0100)
    assert result.quarters[0].quarterly_expense == pytest.approx(-2.5)
    assert any("negative Treasury3m" in w for w in result.warnings)

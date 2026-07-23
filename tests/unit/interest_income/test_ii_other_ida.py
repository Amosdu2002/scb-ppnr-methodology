"""ii_other_ida (Eq A43) — hand-calculable fixture: item-15 balance 2000, α = 0.6,
Treasury3m flat 4%, Treasury10y flat 5% → blended rate 0.6·0.04 + 0.4·0.05 = 0.044
and income 2000 × 0.044 / 4 = 22 per quarter; legs 1200 × 0.04 / 4 = 12 and
800 × 0.05 / 4 = 10. No 6% cap exists (footnote 66 is rationale, not mechanics)."""

from __future__ import annotations

import pytest

from scb_ppnr.interest_income import OtherIdaInputs, project_other_ida
from scb_ppnr.interest_income.schemas import PROJECTION_QUARTERS
from conftest import flat

FIRM = OtherIdaInputs("FIRM_A", total_balance=2000.0, short_rate_share=0.60)


def _flat_scenario(make_income_scenario):
    return make_income_scenario(t3m={0: 0.0400, **flat(0.0400)}, t10y=flat(0.0500))


def test_hand_income_blend_and_legs(make_income_scenario):
    result = project_other_ida(FIRM, _flat_scenario(make_income_scenario))
    for row in result.quarters:
        assert row.annualized_rate == pytest.approx(0.044)
        assert row.quarterly_income == pytest.approx(22.0)
        assert row.diagnostics.short_leg_income == pytest.approx(12.0)
        assert row.diagnostics.long_leg_income == pytest.approx(10.0)
        assert row.diagnostics.short_leg_income + row.diagnostics.long_leg_income == pytest.approx(
            row.quarterly_income
        )
    assert result.validation_status == "passed"


def test_blend_bounds_invariant(make_income_scenario):
    scenario = make_income_scenario()
    result = project_other_ida(FIRM, scenario)
    for row in result.quarters:
        t3m = scenario.usd_3m_treasury[row.quarter]
        t10y = scenario.usd_10y_treasury[row.quarter]
        assert min(t3m, t10y) <= row.annualized_rate <= max(t3m, t10y)


def test_flat_balance_and_share_invariants(make_income_scenario):
    result = project_other_ida(FIRM, make_income_scenario())
    assert all(q.average_balance == 2000.0 for q in result.quarters)
    assert all(q.diagnostics.short_rate_share == 0.60 for q in result.quarters)


def test_alpha_zero_is_degenerate_long_leg_only(make_income_scenario):
    inputs = OtherIdaInputs("FIRM_A", total_balance=2000.0, short_rate_share=0.0)
    result = project_other_ida(inputs, _flat_scenario(make_income_scenario))
    assert all(q.quarterly_income == pytest.approx(25.0) for q in result.quarters)  # 2000·0.05/4
    assert result.validation_status == "passed_with_warnings"
    assert any("exactly 0" in w for w in result.warnings)


def test_alpha_one_is_degenerate_short_leg_only(make_income_scenario):
    inputs = OtherIdaInputs("FIRM_A", total_balance=2000.0, short_rate_share=1.0)
    result = project_other_ida(inputs, _flat_scenario(make_income_scenario))
    assert all(q.quarterly_income == pytest.approx(20.0) for q in result.quarters)  # 2000·0.04/4
    assert any("exactly 1" in w for w in result.warnings)


def test_negative_leg_logged_never_clamped(make_income_scenario):
    t10y = {1: -0.0100, **{q: 0.0500 for q in PROJECTION_QUARTERS if q != 1}}
    result = project_other_ida(FIRM, make_income_scenario(t3m={0: 0.0400, **flat(0.0400)}, t10y=t10y))
    # PQ1: 0.6·0.04 + 0.4·(−0.01) = 0.020 → 2000·0.020/4 = 10
    assert result.quarters[0].annualized_rate == pytest.approx(0.020)
    assert result.quarters[0].quarterly_income == pytest.approx(10.0)
    assert any("negative Treasury10y" in w for w in result.warnings)


def test_bilinearity_in_both_treasury_paths(make_income_scenario):
    base_scenario = make_income_scenario()
    base = project_other_ida(FIRM, base_scenario)
    doubled = make_income_scenario(
        t3m={q: 2.0 * v for q, v in base_scenario.usd_3m_treasury.items()},
        t10y={q: 2.0 * v for q, v in base_scenario.usd_10y_treasury.items()},
    )
    scaled = project_other_ida(FIRM, doubled)
    for q_base, q_scaled in zip(base.quarters, scaled.quarters):
        assert q_scaled.quarterly_income == pytest.approx(2.0 * q_base.quarterly_income)

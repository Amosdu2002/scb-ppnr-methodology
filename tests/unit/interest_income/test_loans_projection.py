"""Projection of Corporate wholesale loan income across PQ1..PQ9.

Synthetic inputs only. The scenario path falls (4.4% -> 0.1%) so the floor and
the fixed-rate blend are both genuinely exercised rather than trivially inert."""

from __future__ import annotations

import pytest

from scb_ppnr.core.schemas import ValidationFailure
from scb_ppnr.interest_income.loans_projection import (
    ProjectionDiagnostics,
    project_corporate,
    project_fixed_rate,
    project_segment,
    project_variable_rate,
)
from scb_ppnr.interest_income.loans_schemas import (
    VT_DO_NOT_USE,
    VT_ENTRY_FEE,
    VT_FIXED,
    VT_FLOATING,
    VT_MIXED,
    SegmentKey,
    SegmentLaunchPoint,
    SegmentSpread,
)

QUARTERS = tuple(range(1, 10))
FALLING_3M = {1: 0.044, 2: 0.030, 3: 0.018, 4: 0.010, 5: 0.005,
              6: 0.002, 7: 0.001, 8: 0.001, 9: 0.001}
FLAT_3M = {q: 0.02 for q in QUARTERS}


def _key(code: int, category: str = "C&I", locom: str = "HFI") -> SegmentKey:
    return SegmentKey(category=category, locom=locom, variable_type=code)


def _launch(
    code: int,
    balance: float = 1000.0,
    spread: float = 0.02,
    pool_rate: float = 0.06,
    floor: float | None = None,
    weights: dict[int, float] | None = None,
    category: str = "C&I",
) -> SegmentLaunchPoint:
    key = _key(code, category)
    carries_spread = code in (VT_FIXED, VT_FLOATING, VT_MIXED)
    return SegmentLaunchPoint(
        segment=key,
        share=0.5,
        balance=balance,
        spread=SegmentSpread(
            segment=key, spread=spread, pool_rate=pool_rate, base_rate=pool_rate - spread,
            base_quarter=None,
        ) if carries_spread else None,
        floor=floor,
        floor_dispersion=0.0,
        reorigination_weights=weights or {},
    )


# --- variable engine (Equation A33) ---------------------------------------

def test_variable_rate_is_base_plus_a_constant_spread():
    rates, unfloored, binds = project_variable_rate(0.02, FALLING_3M, None, QUARTERS)

    assert rates[1] == pytest.approx(0.064)
    assert rates[9] == pytest.approx(0.021)
    assert binds == ()
    assert unfloored == rates


def test_floor_binds_only_where_the_projected_rate_falls_below_it():
    rates, unfloored, binds = project_variable_rate(0.02, FALLING_3M, 0.030, QUARTERS)

    assert rates[1] == pytest.approx(0.064)          # above the floor, untouched
    assert rates[9] == pytest.approx(0.030)          # floored
    assert unfloored[9] == pytest.approx(0.021)      # what it would have been
    assert binds == (5, 6, 7, 8, 9)


# --- fixed engine (Equation A38) ------------------------------------------

def test_fixed_rate_with_zero_weight_never_moves():
    """Equation A34: existing rates are carried unchanged except where re-originated."""
    rates, _, _ = project_fixed_rate(0.07, 0.02, FALLING_3M, {}, None, QUARTERS)
    assert all(rates[q] == pytest.approx(0.07) for q in QUARTERS)


def test_fixed_rate_blends_toward_the_new_origination_rate():
    weights = {q: 0.25 for q in QUARTERS}
    rates, _, _ = project_fixed_rate(0.07, 0.02, FLAT_3M, weights, None, QUARTERS)

    # new-origination rate is flat at 0.02 + 0.02 = 0.04; the carried rate walks
    # a quarter of the way there each quarter.
    assert rates[1] == pytest.approx(0.75 * 0.07 + 0.25 * 0.04)
    assert rates[2] == pytest.approx(0.75 * rates[1] + 0.25 * 0.04)
    assert rates[9] < rates[1] < 0.07


def test_full_reorigination_replaces_the_rate_entirely():
    rates, _, _ = project_fixed_rate(0.07, 0.02, FLAT_3M, {q: 1.0 for q in QUARTERS}, None, QUARTERS)
    assert all(rates[q] == pytest.approx(0.04) for q in QUARTERS)


def test_floored_rate_is_what_carries_forward():
    """A binding floor means the portfolio really is earning its floor, so the
    next quarter's carried component is that rate — not a shadow value the loans
    never earned. The unfloored path is kept so the difference stays visible."""
    weights = {q: 0.5 for q in QUARTERS}
    rates, unfloored, binds = project_fixed_rate(0.07, 0.0, FALLING_3M, weights, 0.05, QUARTERS)

    assert 1 in binds or 2 in binds
    assert all(rates[q] >= 0.05 - 1e-12 for q in QUARTERS)
    # the shadow path is free to fall below the floor
    assert unfloored[9] < 0.05
    # and carrying the floored value keeps the effective path at the floor
    assert rates[9] == pytest.approx(0.05)


# --- routing (PID-LOAN-5) -------------------------------------------------

@pytest.mark.parametrize("code", [VT_DO_NOT_USE, VT_ENTRY_FEE])
def test_no_income_codes_hold_balance_and_earn_zero(code):
    diagnostics = ProjectionDiagnostics()
    projection = project_segment(_launch(code, balance=750.0), FALLING_3M, QUARTERS, diagnostics)

    assert projection.rate_path is None
    assert projection.total_income == 0.0
    assert projection.balance == 750.0
    assert diagnostics.no_income_balance == 750.0


def test_mixed_projects_on_the_variable_engine():
    """PID-LOAN-4/5: Mixed derives its spread on the fixed convention at launch
    but reprices with the scenario like a floater — it has no wt, so it cannot
    run the Equation A38 blend."""
    mixed = project_segment(_launch(VT_MIXED, spread=0.02), FALLING_3M, QUARTERS)
    floating = project_segment(_launch(VT_FLOATING, spread=0.02), FALLING_3M, QUARTERS)

    assert mixed.rate_path == floating.rate_path


def test_income_is_balance_times_rate_over_four():
    projection = project_segment(_launch(VT_FLOATING, balance=1000.0, spread=0.02), FLAT_3M, QUARTERS)
    assert projection.income_path[1] == pytest.approx(1000.0 * 0.04 / 4.0)
    assert projection.total_income == pytest.approx(9 * 1000.0 * 0.04 / 4.0)


def test_income_earning_segment_without_a_spread_is_refused():
    key = _key(VT_FLOATING)
    broken = SegmentLaunchPoint(segment=key, share=0.5, balance=100.0, spread=None,
                                floor=None, floor_dispersion=0.0)
    with pytest.raises(ValidationFailure, match="no launch-point spread"):
        project_segment(broken, FLAT_3M, QUARTERS)


# --- roll-up and the scalar -----------------------------------------------

def test_category_totals_apply_the_industry_scalar_every_quarter():
    launches = {
        _key(VT_FLOATING): _launch(VT_FLOATING, balance=1000.0, spread=0.02),
        _key(VT_ENTRY_FEE): _launch(VT_ENTRY_FEE, balance=500.0),
    }
    _, totals, diagnostics = project_corporate(launches, FLAT_3M, QUARTERS, {"C&I": 1.033})

    unscaled = 1000.0 * 0.04 / 4.0        # the fee segment contributes nothing
    assert totals["C&I"][1] == pytest.approx(unscaled * 1.033)
    assert diagnostics.scalars_applied == {"C&I": 1.033}
    assert diagnostics.no_income_balance == 500.0


def test_missing_scalar_is_refused_rather_than_defaulted_to_one():
    launches = {_key(VT_FLOATING): _launch(VT_FLOATING)}
    with pytest.raises(ValidationFailure, match="no industry scalar"):
        project_corporate(launches, FLAT_3M, QUARTERS, {})


def test_missing_scalar_can_be_tolerated_for_diagnostic_runs():
    launches = {_key(VT_FLOATING): _launch(VT_FLOATING)}
    _, _, diagnostics = project_corporate(launches, FLAT_3M, QUARTERS, {}, require_scalar=False)
    assert diagnostics.unscaled_categories == ["C&I"]


def test_a_gap_in_the_scenario_path_is_refused():
    launches = {_key(VT_FLOATING): _launch(VT_FLOATING)}
    with pytest.raises(ValidationFailure, match="missing PQ9"):
        project_corporate(launches, {q: 0.02 for q in range(1, 9)}, QUARTERS, {"C&I": 1.0})


def test_negative_projected_rates_are_logged_not_clamped():
    launches = {_key(VT_FLOATING): _launch(VT_FLOATING, spread=-0.05, floor=None)}
    projections, _, diagnostics = project_corporate(launches, FALLING_3M, QUARTERS, {"C&I": 1.0})

    assert projections[_key(VT_FLOATING)].rate_path[9] < 0.0
    assert len(diagnostics.negative_rates) > 0
    assert "negative projected rates" in diagnostics.render()


def test_diagnostics_render_reports_floor_binds_and_dormant_balance():
    launches = {
        _key(VT_FLOATING): _launch(VT_FLOATING, spread=0.0, floor=0.035),
        _key(VT_DO_NOT_USE): _launch(VT_DO_NOT_USE, balance=250.0),
    }
    _, _, diagnostics = project_corporate(launches, FALLING_3M, QUARTERS, {"C&I": 1.0})
    rendered = diagnostics.render()

    assert "floor binds" in rendered
    assert len(diagnostics.floor_binds) > 0
    assert "250.00 (codes 0 and 4)" in rendered

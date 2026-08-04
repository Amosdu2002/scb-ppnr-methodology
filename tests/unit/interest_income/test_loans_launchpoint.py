"""Launch-point construction for Corporate wholesale loans.

Synthetic facilities only — no company data. Each test pins one rule from
`specifications/interest-income/loans/ii_loans_corporate.spec.md`, with the
arithmetic worked by hand in the assertion so a change in behaviour has to be
argued with rather than absorbed."""

from __future__ import annotations

from datetime import date

import pytest

from scb_ppnr.core.schemas import ValidationFailure
from scb_ppnr.interest_income.loans_launchpoint import (
    build_launch_point,
    collapse_floor,
    compute_pool_rates,
    compute_reorigination_weights,
    median_origination_quarter,
    resolve_base_rate,
)
from scb_ppnr.interest_income.loans_schemas import (
    EXPOSURE_UTILIZED,
    FALLBACK_NO_ORIGINATION_DATE,
    FALLBACK_OUTSIDE_MEV,
    FLOOR_COLLAPSE_MAX,
    POOL_FIXED,
    POOL_FLOAT,
    VT_DO_NOT_USE,
    VT_ENTRY_FEE,
    VT_FIXED,
    VT_FLOATING,
    VT_MIXED,
    LoanFacility,
    SegmentKey,
    quarter_label,
)

QUARTERS = tuple(range(1, 10))
HIST_3M = {"2020Q1": 0.015, "2022Q2": 0.008, "2023Q3": 0.052}


def _key(code: int, category: str = "C&I", locom: str = "HFI") -> SegmentKey:
    return SegmentKey(category=category, locom=locom, variable_type=code)


def _facility(
    facility_id: str,
    code: int,
    committed: float,
    rate: float | None = None,
    utilized: float | None = None,
    floor: float | None = None,
    originated: date | None = None,
    matures: date | None = None,
    category: str = "C&I",
    locom: str = "HFI",
) -> LoanFacility:
    return LoanFacility(
        facility_id=facility_id,
        segment=_key(code, category, locom),
        committed_exposure=committed,
        utilized_exposure=committed if utilized is None else utilized,
        interest_rate=rate,
        interest_rate_floor=floor,
        origination_date=originated,
        maturity_date=matures,
    )


def _quarter_of_maturity(when: date) -> int | None:
    """PQ0 = 2024Q4, so PQ1 = 2025Q1 ... PQ9 = 2027Q1."""
    index = (when.year - 2025) * 4 + (when.month - 1) // 3 + 1
    return index if 1 <= index <= 9 else None


# --- rate pools (PID-LOAN-3) ----------------------------------------------

def test_float_pool_holds_floating_and_mixed_fixed_pool_holds_fixed_only():
    facilities = [
        _facility("float-1", VT_FLOATING, committed=100.0, rate=0.06),
        _facility("mixed-1", VT_MIXED, committed=100.0, rate=0.04),
        _facility("fixed-1", VT_FIXED, committed=50.0, rate=0.08),
    ]
    pools = compute_pool_rates(facilities)

    # Floating + Mixed pooled: (100*0.06 + 100*0.04) / 200
    assert pools[("C&I", "HFI", POOL_FLOAT)].rate == pytest.approx(0.05)
    # Fixed alone
    assert pools[("C&I", "HFI", POOL_FIXED)].rate == pytest.approx(0.08)


def test_missing_rate_row_leaves_both_sides_of_the_average():
    """The dilution bug this rule exists to prevent: a rate-less row left in the
    denominator would drag a 6% pool toward 3%."""
    facilities = [
        _facility("has-rate", VT_FLOATING, committed=100.0, rate=0.06),
        _facility("no-rate", VT_FLOATING, committed=100.0, rate=None),
    ]
    pool = compute_pool_rates(facilities)[("C&I", "HFI", POOL_FLOAT)]

    assert pool.rate == pytest.approx(0.06)
    assert pool.rows_dropped == 1
    assert pool.exposure_dropped == pytest.approx(100.0)


def test_pool_weighting_uses_committed_not_utilized_exposure():
    facilities = [
        _facility("wide-commit", VT_FLOATING, committed=1000.0, utilized=10.0, rate=0.02),
        _facility("drawn", VT_FLOATING, committed=100.0, utilized=100.0, rate=0.10),
    ]
    pool = compute_pool_rates(facilities)[("C&I", "HFI", POOL_FLOAT)]

    # committed weighting: (1000*0.02 + 100*0.10) / 1100
    assert pool.rate == pytest.approx((1000 * 0.02 + 100 * 0.10) / 1100)


# --- median origination quarter (PID-LOAN-4) ------------------------------

def test_median_origination_maps_month_to_its_calendar_quarter():
    assert quarter_label(date(2022, 5, 17)) == "2022Q2"
    assert quarter_label(date(2022, 1, 1)) == "2022Q1"
    assert quarter_label(date(2022, 12, 31)) == "2022Q4"


def test_median_origination_returns_an_observed_date():
    facilities = [
        _facility("a", VT_FIXED, 10.0, originated=date(2020, 1, 15)),
        _facility("b", VT_FIXED, 10.0, originated=date(2022, 5, 17)),
        _facility("c", VT_FIXED, 10.0, originated=date(2023, 8, 2)),
    ]
    assert median_origination_quarter(facilities) == "2022Q2"


def test_floating_uses_launch_point_while_fixed_uses_its_own_median():
    fixed = [_facility("f", VT_FIXED, 10.0, originated=date(2022, 5, 17))]
    floating = [_facility("v", VT_FLOATING, 10.0, originated=date(2022, 5, 17))]

    fixed_base, fixed_quarter, _ = resolve_base_rate(_key(VT_FIXED), fixed, 0.044, HIST_3M)
    float_base, float_quarter, _ = resolve_base_rate(_key(VT_FLOATING), floating, 0.044, HIST_3M)

    assert (fixed_base, fixed_quarter) == (0.008, "2022Q2")
    assert (float_base, float_quarter) == (0.044, None)


def test_missing_origination_date_falls_back_to_zero_and_is_censused():
    facilities = [_facility("f", VT_FIXED, 10.0, originated=None)]
    base, quarter, fallback = resolve_base_rate(_key(VT_FIXED), facilities, 0.044, HIST_3M)

    assert base == 0.0 and quarter is None
    assert fallback == FALLBACK_NO_ORIGINATION_DATE


def test_quarter_outside_history_falls_back_and_records_the_other_cause():
    facilities = [_facility("f", VT_FIXED, 10.0, originated=date(1975, 6, 1))]
    base, quarter, fallback = resolve_base_rate(_key(VT_FIXED), facilities, 0.044, HIST_3M)

    assert base == 0.0 and quarter == "1975Q2"
    assert fallback == FALLBACK_OUTSIDE_MEV


# --- floors (PID-LOAN-7) --------------------------------------------------

def test_absent_floors_mean_no_floor_while_a_populated_zero_participates():
    assert collapse_floor([_facility("a", VT_FLOATING, 10.0, floor=None)]) == (None, 0.0)

    floor, dispersion = collapse_floor([
        _facility("a", VT_FLOATING, 100.0, floor=0.0),
        _facility("b", VT_FLOATING, 100.0, floor=0.04),
    ])
    assert floor == pytest.approx(0.02)
    assert dispersion == pytest.approx(0.04)


def test_floor_collapse_modes_differ():
    facilities = [
        _facility("a", VT_FLOATING, 100.0, floor=0.01),
        _facility("b", VT_FLOATING, 300.0, floor=0.05),
    ]
    assert collapse_floor(facilities)[0] == pytest.approx((100 * 0.01 + 300 * 0.05) / 400)
    assert collapse_floor(facilities, FLOOR_COLLAPSE_MAX)[0] == pytest.approx(0.05)


# --- re-origination weight (PID-LOAN-6) -----------------------------------

def test_wt_is_utilized_exposure_maturing_in_the_quarter_over_the_fixed_balance():
    facilities = [
        _facility("m1", VT_FIXED, 100.0, utilized=80.0, matures=date(2025, 2, 1)),   # PQ1
        _facility("m2", VT_FIXED, 100.0, utilized=40.0, matures=date(2025, 5, 1)),   # PQ2
        _facility("far", VT_FIXED, 100.0, utilized=80.0, matures=date(2035, 1, 1)),  # beyond
    ]
    weights = compute_reorigination_weights(facilities, 200.0, _quarter_of_maturity, QUARTERS)

    assert weights[1] == pytest.approx(80.0 / 200.0)
    assert weights[2] == pytest.approx(40.0 / 200.0)
    assert weights[3] == pytest.approx(0.0)


def test_wt_above_one_is_surfaced_not_clamped():
    from scb_ppnr.interest_income.loans_launchpoint import LaunchPointDiagnostics

    diagnostics = LaunchPointDiagnostics()
    facilities = [_facility("m", VT_FIXED, 500.0, utilized=500.0, matures=date(2025, 2, 1))]
    weights = compute_reorigination_weights(
        facilities, 100.0, _quarter_of_maturity, QUARTERS, _key(VT_FIXED), diagnostics
    )

    assert weights[1] == pytest.approx(5.0)          # not clamped to 1
    assert diagnostics.wt_over_one == [(_key(VT_FIXED), 1, pytest.approx(5.0))]


# --- assembly (PID-LOAN-5) ------------------------------------------------

def _mixed_book() -> list[LoanFacility]:
    return [
        _facility("float", VT_FLOATING, 400.0, rate=0.06, originated=date(2023, 8, 2)),
        _facility("mixed", VT_MIXED, 100.0, rate=0.05, originated=date(2022, 5, 17)),
        _facility("fixed", VT_FIXED, 300.0, rate=0.07, originated=date(2020, 1, 15),
                  matures=date(2025, 2, 1)),
        _facility("fee", VT_ENTRY_FEE, 150.0, rate=0.03),
        _facility("nouse", VT_DO_NOT_USE, 50.0, rate=None),
    ]


def test_no_income_codes_hold_balance_but_earn_nothing():
    segments, _ = build_launch_point(
        _mixed_book(), {"C&I": 1000.0}, 0.044, HIST_3M, QUARTERS, _quarter_of_maturity
    )

    fee = segments[_key(VT_ENTRY_FEE)]
    nouse = segments[_key(VT_DO_NOT_USE)]

    assert fee.spread is None and nouse.spread is None
    assert fee.earns_income is False and nouse.earns_income is False
    # ... but they take their share of the category balance, diluting the rest:
    assert fee.share == pytest.approx(150.0 / 1000.0)
    assert nouse.share == pytest.approx(50.0 / 1000.0)
    assert fee.balance == pytest.approx(150.0)


def test_shares_span_every_rate_type_and_sum_to_one():
    segments, _ = build_launch_point(
        _mixed_book(), {"C&I": 1000.0}, 0.044, HIST_3M, QUARTERS, _quarter_of_maturity
    )
    assert sum(s.share for s in segments.values()) == pytest.approx(1.0)


def test_mixed_borrows_the_fixed_pool_rate_against_its_own_median_quarter():
    """The hybrid of PID-LOAN-4: Mixed's exposures feed the FLOAT pool, but its
    spread is built from the FIXED pool's rate less its OWN median-origination
    base rate."""
    segments, _ = build_launch_point(
        _mixed_book(), {"C&I": 1000.0}, 0.044, HIST_3M, QUARTERS, _quarter_of_maturity
    )
    mixed = segments[_key(VT_MIXED)].spread
    fixed = segments[_key(VT_FIXED)].spread
    floating = segments[_key(VT_FLOATING)].spread

    assert mixed.pool_rate == pytest.approx(0.07)      # the FIXED pool, not the float pool
    assert mixed.base_quarter == "2022Q2"              # its own median origination
    assert mixed.spread == pytest.approx(0.07 - 0.008)

    assert fixed.pool_rate == pytest.approx(0.07)
    assert fixed.base_quarter == "2020Q1"
    assert fixed.spread == pytest.approx(0.07 - 0.015)

    # the float pool still holds Floating + Mixed: (400*0.06 + 100*0.05) / 500
    assert floating.pool_rate == pytest.approx((400 * 0.06 + 100 * 0.05) / 500)
    assert floating.base_quarter is None
    assert floating.spread == pytest.approx((400 * 0.06 + 100 * 0.05) / 500 - 0.044)


def test_fixed_segment_carries_weights_and_variable_segments_do_not():
    segments, _ = build_launch_point(
        _mixed_book(), {"C&I": 1000.0}, 0.044, HIST_3M, QUARTERS, _quarter_of_maturity
    )
    assert segments[_key(VT_FIXED)].reorigination_weights[1] == pytest.approx(300.0 / 300.0)
    assert segments[_key(VT_FLOATING)].reorigination_weights == {}


def test_a_pool_with_no_usable_rate_surfaces_rather_than_defaulting():
    facilities = [_facility("f", VT_FIXED, 100.0, rate=None, originated=date(2020, 1, 15))]
    with pytest.raises(ValidationFailure, match="no usable interest rates"):
        build_launch_point(facilities, {"C&I": 100.0}, 0.044, HIST_3M, QUARTERS, _quarter_of_maturity)


def test_unmapped_variable_type_code_is_refused():
    with pytest.raises(ValidationFailure, match="unmapped code is refused"):
        SegmentKey(category="C&I", locom="HFI", variable_type=7)


def test_diagnostics_render_covers_every_census():
    facilities = _mixed_book() + [
        _facility("norate", VT_FLOATING, 25.0, rate=None),
        _facility("nodate", VT_FIXED, 10.0, rate=0.07, originated=None, locom="HFS"),
    ]
    _, diagnostics = build_launch_point(
        facilities, {"C&I": 1000.0}, 0.044, HIST_3M, QUARTERS, _quarter_of_maturity
    )
    rendered = diagnostics.render()

    assert "base-rate fallbacks to zero : 1" in rendered
    assert "rows dropped from rate pools" in rendered
    assert any(cause == FALLBACK_NO_ORIGINATION_DATE for _, cause in diagnostics.base_rate_fallbacks)

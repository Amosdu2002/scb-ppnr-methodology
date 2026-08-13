"""The CRE part of the loans model (PID-LOAN-18..25).

Synthetic facilities and workbooks only — no company data. Each test pins one
rule from `specifications/interest-income/loans/ii_loans_cre.spec.md`, with the
arithmetic worked by hand in the assertion so a change in behaviour has to be
argued with rather than absorbed."""

from __future__ import annotations

from datetime import date

import pytest

from scb_ppnr.core.schemas import ValidationFailure
from scb_ppnr.ingestion.loans_cre_mapping import (
    CRE_CATEGORY_NAMES,
    H2_CODE_TO_CRE_CATEGORY,
    H2_DO_NOT_USE_CODES,
    cre_reference_key,
    cre_scalars_by_category_name,
    decode_cre_segment,
    is_h2_do_not_use,
    parse_h2_code,
)
from scb_ppnr.interest_income.loans_launchpoint import (
    build_cre_launch_point,
    weighted_origination_quarter,
)
from scb_ppnr.interest_income.loans_schemas import (
    EXPOSURE_OUTSTANDING,
    ORIG_DATE_WEIGHTED_MEAN,
    ORIG_DATE_WEIGHTED_MEDIAN,
    VT_DO_NOT_USE,
    VT_ENTRY_FEE,
    VT_FIXED,
    VT_FLOATING,
    VT_MIXED,
    LoanFacility,
    SegmentKey,
    projection_quarter_index,
)

QUARTERS = tuple(range(1, 10))
LAUNCH_3M = 0.044
HIST_3M = {"2021Q2": 0.003, "2022Q2": 0.008}


def _facility(
    facility_id: str,
    code_category: str,
    vt: int,
    committed: float,
    outstanding: float,
    rate: float | None = None,
    floor: float | None = None,
    originated: date | None = None,
    matures: date | None = None,
    locom: str = "HFI",
) -> LoanFacility:
    return LoanFacility(
        facility_id=facility_id,
        segment=SegmentKey(category=code_category, locom=locom, variable_type=vt),
        committed_exposure=committed,
        utilized_exposure=0.0,          # H.2 carries no utilized column
        interest_rate=rate,
        interest_rate_floor=floor,
        origination_date=originated,
        maturity_date=matures,
        outstanding_balance=outstanding,
    )


# --- H.2 mapping (PID-LOAN-19/21) -------------------------------------------


def test_codes_one_and_two_both_land_in_domestic_construction():
    assert H2_CODE_TO_CRE_CATEGORY[1] == 1
    assert H2_CODE_TO_CRE_CATEGORY[2] == 1
    a = decode_cre_segment(1, 2, 3)
    b = decode_cre_segment(2, 2, 3)
    assert a == b == SegmentKey("CRE Dom construction", "HFI", VT_FLOATING)


def test_code_seven_is_the_merged_international_category():
    segment = decode_cre_segment(7, 1, 3)
    assert segment.category == "CRE International (Fed 4-6 merged)"


def test_do_not_use_codes_parse_but_never_decode():
    for code in H2_DO_NOT_USE_CODES:
        assert parse_h2_code(code) == code
        assert is_h2_do_not_use(code)
        with pytest.raises(ValidationFailure):
            decode_cre_segment(code, 2, 3)


def test_an_unknown_h2_code_is_refused():
    with pytest.raises(ValidationFailure):
        parse_h2_code(8)
    with pytest.raises(ValidationFailure):
        parse_h2_code("")


def test_cre_reference_key_matches_the_workbook_spelling():
    assert cre_reference_key(1, 2, 3) == "1_2_3"
    assert cre_reference_key(7, "[NULL]", 1) == "7_[NULL]_1"


def test_the_pid_loan_21_scalar_assignment():
    scalars = cre_scalars_by_category_name()
    assert scalars["CRE Dom construction"] == 1.081
    assert scalars["CRE Dom multifamily"] == 1.081
    assert scalars["CRE Dom non-owner-occupied"] == 1.081
    assert scalars["CRE International (Fed 4-6 merged)"] == 1.113
    assert set(scalars) == set(CRE_CATEGORY_NAMES.values())


# --- weighted origination date (PID-LOAN-22) --------------------------------


def test_weighted_mean_of_two_equal_weights_is_the_midpoint_quarter():
    rows = [
        _facility("A", "X", VT_FIXED, 1.0, 100.0, originated=date(2020, 2, 15)),
        _facility("B", "X", VT_FIXED, 1.0, 100.0, originated=date(2022, 2, 15)),
    ]
    # equal weights: the mean ordinal is the midpoint, 2021-02-14/15 -> 2021Q1
    assert weighted_origination_quarter(rows, EXPOSURE_OUTSTANDING, ORIG_DATE_WEIGHTED_MEAN) == "2021Q1"


def test_weighted_median_follows_the_balance_not_the_row_count():
    rows = [
        _facility("A", "X", VT_FIXED, 1.0, 1.0, originated=date(2019, 1, 1)),
        _facility("B", "X", VT_FIXED, 1.0, 10.0, originated=date(2023, 6, 1)),
    ]
    # half the weight is 5.5; the cumulative first reaches it on the 2023 row —
    # an unweighted median_low would have said 2019Q1
    assert weighted_origination_quarter(rows, EXPOSURE_OUTSTANDING, ORIG_DATE_WEIGHTED_MEDIAN) == "2023Q2"


def test_all_zero_weights_degenerate_to_the_unweighted_median():
    rows = [
        _facility("A", "X", VT_FIXED, 1.0, 0.0, originated=date(2019, 1, 1)),
        _facility("B", "X", VT_FIXED, 1.0, 0.0, originated=date(2023, 6, 1)),
    ]
    assert weighted_origination_quarter(rows, EXPOSURE_OUTSTANDING, ORIG_DATE_WEIGHTED_MEAN) == "2019Q1"


def test_no_dates_means_no_quarter():
    rows = [_facility("A", "X", VT_FIXED, 1.0, 100.0)]
    assert weighted_origination_quarter(rows, EXPOSURE_OUTSTANDING, ORIG_DATE_WEIGHTED_MEAN) is None


def test_an_unknown_statistic_is_refused():
    with pytest.raises(ValidationFailure):
        weighted_origination_quarter([], EXPOSURE_OUTSTANDING, "median_low")


# --- the CRE launch point (PID-LOAN-20/22/23/24/25) --------------------------

CONSTRUCTION = "CRE Dom construction"
MULTIFAMILY = "CRE Dom multifamily"


def _cre_rows() -> list[LoanFacility]:
    return [
        # construction HFI: two floating rows, a fee row and a DO-NOT-USE row
        _facility("F1", CONSTRUCTION, VT_FLOATING, 200.0, 150.0, rate=0.070, floor=0.05),
        _facility("F2", CONSTRUCTION, VT_FLOATING, 100.0, 50.0, rate=0.065),
        _facility("F3", CONSTRUCTION, VT_ENTRY_FEE, 40.0, 30.0, rate=0.030),
        _facility("F4", CONSTRUCTION, VT_DO_NOT_USE, 10.0, 5.0),
        # multifamily HFI: a fixed row maturing at PQ5 and a mixed sibling
        _facility("F5", MULTIFAMILY, VT_FIXED, 300.0, 300.0, rate=0.050,
                  originated=date(2021, 5, 15), matures=date(2026, 2, 15)),
        _facility("F6", MULTIFAMILY, VT_MIXED, 80.0, 60.0, rate=0.055,
                  originated=date(2022, 5, 17)),
    ]


def _build(rows=None, statistic=ORIG_DATE_WEIGHTED_MEAN):
    return build_cre_launch_point(
        rows if rows is not None else _cre_rows(),
        {(CONSTRUCTION, "HFI"): 210.0, (MULTIFAMILY, "HFI"): 380.0},
        LAUNCH_3M,
        HIST_3M,
        QUARTERS,
        lambda when: projection_quarter_index(when, "2024Q4"),
        orig_date_statistic=statistic,
    )


def test_shares_span_all_rate_types_and_balances_come_from_the_side_m1():
    launch, _ = _build()
    floating = launch[SegmentKey(CONSTRUCTION, "HFI", VT_FLOATING)]
    # denominator 150 + 50 + 30 + 5 = 235: fee and DO-NOT-USE rows dilute
    assert floating.share == pytest.approx(200.0 / 235.0)
    assert floating.balance == pytest.approx(200.0 / 235.0 * 210.0)
    fee = launch[SegmentKey(CONSTRUCTION, "HFI", VT_ENTRY_FEE)]
    assert fee.share == pytest.approx(30.0 / 235.0)
    assert not fee.earns_income and fee.spread is None


def test_floating_spread_is_committed_pool_rate_less_the_launch_point_base():
    launch, _ = _build()
    spread = launch[SegmentKey(CONSTRUCTION, "HFI", VT_FLOATING)].spread
    pool = (200.0 * 0.070 + 100.0 * 0.065) / 300.0        # committed-weighted
    assert spread.pool_rate == pytest.approx(pool)
    assert spread.base_rate == LAUNCH_3M and spread.base_quarter is None
    assert spread.spread == pytest.approx(pool - LAUNCH_3M)


def test_the_mixed_hybrid_spread_uses_the_fixed_pool_at_mixeds_own_quarter():
    launch, _ = _build()
    mixed = launch[SegmentKey(MULTIFAMILY, "HFI", VT_MIXED)].spread
    # PID-LOAN-23: fixed-pool rate (5%), base at MIXED's own weighted origination
    # quarter (2022Q2 -> 0.8%), NOT the floating pool and NOT the fixed rows' quarter
    assert mixed.pool_rate == pytest.approx(0.050)
    assert mixed.base_quarter == "2022Q2"
    assert mixed.spread == pytest.approx(0.050 - 0.008)


def test_the_fixed_spread_uses_the_weighted_origination_quarter():
    launch, _ = _build()
    fixed = launch[SegmentKey(MULTIFAMILY, "HFI", VT_FIXED)].spread
    assert fixed.base_quarter == "2021Q2"
    assert fixed.spread == pytest.approx(0.050 - 0.003)


def test_the_block_floor_is_outstanding_weighted_with_blanks_as_zero():
    launch, _ = _build()
    floating = launch[SegmentKey(CONSTRUCTION, "HFI", VT_FLOATING)]
    # (150 x 5% + 50 x 0) / 200 — F2's blank floor counts as ZERO (PID-LOAN-25)
    assert floating.floor == pytest.approx(0.0375)


def test_the_blocks_variable_floor_is_shared_by_floating_and_mixed():
    rows = _cre_rows() + [
        _facility("F7", MULTIFAMILY, VT_FLOATING, 40.0, 40.0, rate=0.06, floor=0.02),
    ]
    launch, _ = _build(rows)
    # over the block's floating + mixed rows: (40 x 2% + 60 x 0) / 100 = 0.8%
    expected = (40.0 * 0.02) / 100.0
    assert launch[SegmentKey(MULTIFAMILY, "HFI", VT_FLOATING)].floor == pytest.approx(expected)
    assert launch[SegmentKey(MULTIFAMILY, "HFI", VT_MIXED)].floor == pytest.approx(expected)


def test_the_fixed_floor_is_exactly_zero():
    launch, _ = _build()
    assert launch[SegmentKey(MULTIFAMILY, "HFI", VT_FIXED)].floor == 0.0


def test_wt_is_outstanding_weighted_maturities_over_the_fixed_block_balance():
    launch, _ = _build()
    weights = launch[SegmentKey(MULTIFAMILY, "HFI", VT_FIXED)].reorigination_weights
    # F5 matures 2026-02-15 -> PQ5 off a 2024Q4 launch; 300/300 = 1.0
    assert weights[5] == pytest.approx(1.0)
    assert all(weights[q] == 0.0 for q in QUARTERS if q != 5)


def test_a_mixed_segment_with_no_fixed_siblings_is_refused_not_defaulted():
    rows = [
        _facility("M1", CONSTRUCTION, VT_MIXED, 50.0, 40.0, rate=0.06,
                  originated=date(2022, 5, 17)),
    ]
    with pytest.raises(ValidationFailure):
        _build(rows)


def test_the_statistic_switch_reaches_the_spread():
    # two fixed rows: median (by outstanding weight) sits on the 2021 row while
    # the mean is pulled toward it too — use unequal weights so the two statistics
    # land in DIFFERENT quarters and the switch is observable
    rows = [
        _facility("F5", MULTIFAMILY, VT_FIXED, 100.0, 20.0, rate=0.050,
                  originated=date(2021, 5, 15)),
        _facility("F6", MULTIFAMILY, VT_FIXED, 100.0, 80.0, rate=0.050,
                  originated=date(2022, 5, 17)),
    ]
    launch_median, _ = _build(rows, statistic=ORIG_DATE_WEIGHTED_MEDIAN)
    fixed = launch_median[SegmentKey(MULTIFAMILY, "HFI", VT_FIXED)].spread
    assert fixed.base_quarter == "2022Q2"          # 80% of the weight sits there
    launch_mean, _ = _build(rows, statistic=ORIG_DATE_WEIGHTED_MEAN)
    fixed_mean = launch_mean[SegmentKey(MULTIFAMILY, "HFI", VT_FIXED)].spread
    # the mean is pulled 20% of the 367-day gap (~73 days) back from 2022-05-17,
    # into March -> a DIFFERENT quarter than the weighted median's
    assert fixed_mean.base_quarter == "2022Q1"


def test_a_missing_base_quarter_falls_back_to_zero_and_is_censused():
    rows = [
        _facility("F5", MULTIFAMILY, VT_FIXED, 300.0, 300.0, rate=0.050,
                  originated=date(1999, 5, 15), matures=date(2026, 2, 15)),
        _facility("F6", MULTIFAMILY, VT_MIXED, 80.0, 60.0, rate=0.055,
                  originated=date(2022, 5, 17)),
    ]
    launch, diagnostics = _build(rows)
    fixed = launch[SegmentKey(MULTIFAMILY, "HFI", VT_FIXED)].spread
    assert fixed.base_rate == 0.0
    assert fixed.spread == pytest.approx(0.050)    # collapses to the full pool rate
    assert any(cause == "outside_mev_range" for _, cause in diagnostics.base_rate_fallbacks)

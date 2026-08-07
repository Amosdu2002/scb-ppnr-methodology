"""Corporate loans end to end: facilities -> launch point -> nine-quarter income.

Synthetic facilities only. The point of this test is the seam between the two
layers, and one number that matters for review: the size and DIRECTION of the
recorded fee-based divergence from the Fed source."""

from __future__ import annotations

from datetime import date

import pytest

from scb_ppnr.interest_income.loans_launchpoint import build_launch_point
from scb_ppnr.interest_income.loans_projection import project_corporate
from scb_ppnr.interest_income.loans_schemas import (
    VT_ENTRY_FEE,
    VT_FIXED,
    VT_FLOATING,
    VT_MIXED,
    LoanFacility,
    SegmentKey,
)

QUARTERS = tuple(range(1, 10))
FALLING_3M = {1: 0.044, 2: 0.030, 3: 0.018, 4: 0.010, 5: 0.005,
              6: 0.002, 7: 0.001, 8: 0.001, 9: 0.001}
HIST_3M = {"2020Q1": 0.015, "2022Q2": 0.008}
SCALARS = {"C&I": 1.033}


def _quarter_of_maturity(when: date) -> int | None:
    index = (when.year - 2025) * 4 + (when.month - 1) // 3 + 1
    return index if 1 <= index <= 9 else None


def _facility(fid, code, committed, rate=None, floor=None, originated=None, matures=None):
    return LoanFacility(
        facility_id=fid,
        segment=SegmentKey(category="C&I", locom="HFI", variable_type=code),
        committed_exposure=committed,
        utilized_exposure=committed,
        interest_rate=rate,
        interest_rate_floor=floor,
        origination_date=originated,
        maturity_date=matures,
    )


def _book(with_fee_based: bool) -> list[LoanFacility]:
    book = [
        _facility("float-1", VT_FLOATING, 400.0, rate=0.061, floor=0.02),
        _facility("mixed-1", VT_MIXED, 100.0, rate=0.055, originated=date(2022, 5, 17)),
        _facility("fixed-1", VT_FIXED, 300.0, rate=0.070, originated=date(2020, 1, 15),
                  matures=date(2026, 2, 1)),
    ]
    if with_fee_based:
        book.append(_facility("fee-1", VT_ENTRY_FEE, 200.0, rate=0.03))
    return book


def _run(book):
    launch, launch_diagnostics = build_launch_point(
        book, {"C&I": 1000.0}, 0.044, HIST_3M, QUARTERS, _quarter_of_maturity
    )
    projections, totals, projection_diagnostics = project_corporate(
        launch, FALLING_3M, QUARTERS, SCALARS
    )
    return launch, projections, totals, launch_diagnostics, projection_diagnostics


def test_full_chain_produces_nine_quarters_per_category():
    _, _, totals, _, _ = _run(_book(with_fee_based=True))
    assert set(totals["C&I"]) == set(QUARTERS)
    assert all(totals["C&I"][q] > 0.0 for q in QUARTERS)


def test_fee_based_balances_lower_total_income():
    """The recorded divergence, measured.

    The Fed excludes fee-only balances from the total-balances calculation
    (PDF p. 176); this implementation keeps them in the share denominator while
    they earn nothing. Same category balance either way, so the income-earning
    segments simply receive smaller shares — the divergence reduces projected
    income, which is the opposite of what a reader might assume from 'fee-based
    loans are included'."""
    _, _, with_fee, _, diagnostics = _run(_book(with_fee_based=True))
    _, _, without_fee, _, _ = _run(_book(with_fee_based=False))

    total_with = sum(with_fee["C&I"].values())
    total_without = sum(without_fee["C&I"].values())

    assert total_with < total_without
    # 200 of 1000 exposure sits idle, so the earning segments keep 800/1000.
    assert total_with == pytest.approx(total_without * 0.8, rel=1e-9)
    assert diagnostics.no_income_balance == pytest.approx(200.0)


def test_the_scalar_is_the_last_step_and_scales_everything():
    _, _, scaled, _, _ = _run(_book(with_fee_based=True))
    launch, projections, _, _, _ = _run(_book(with_fee_based=True))

    raw = sum(p.income_path[1] for p in projections.values())
    assert scaled["C&I"][1] == pytest.approx(raw * SCALARS["C&I"])


def test_fixed_segment_reprices_only_as_it_matures():
    launch, projections, _, _, _ = _run(_book(with_fee_based=True))
    fixed = projections[SegmentKey(category="C&I", locom="HFI", variable_type=VT_FIXED)]

    # The single fixed facility matures in PQ5 (2026Q1), so PQ1..PQ4 carry the
    # launch rate untouched and the blend only bites from PQ5.
    assert fixed.rate_path[1] == pytest.approx(0.070)
    assert fixed.rate_path[4] == pytest.approx(0.070)
    assert fixed.rate_path[5] < 0.070


def test_launch_point_diagnostics_survive_to_the_caller():
    _, _, _, launch_diagnostics, projection_diagnostics = _run(_book(with_fee_based=True))

    assert launch_diagnostics.base_rate_fallbacks == []       # every fixed/mixed row has a date
    assert "LAUNCH-POINT DIAGNOSTICS" in launch_diagnostics.render()
    assert "PROJECTION DIAGNOSTICS" in projection_diagnostics.render()
    assert len(projection_diagnostics.floor_binds) > 0        # the floater's 2% floor binds late

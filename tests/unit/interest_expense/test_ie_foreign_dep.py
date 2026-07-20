"""ie_foreign_dep (A45–A47 by reference) — hand-calculable fixture:
t3m PQ0 3.00% → PQ1 4.00% (Δ=+0.0100), flat after (PQ2 tests Δ=0), seeds
non-time 0.80% / time 1.20%. Table A7 foreign betas: non-time 0.890/0.790,
time 1.000/1.000 — the time subcomponent tracks ΔTreasury3m one-for-one."""

from __future__ import annotations

import pytest

from scb_ppnr.interest_expense import (
    TABLE_A7_FOREIGN,
    DepositSubcomponent,
    ForeignDepInputs,
    ValidationFailure,
    project_foreign_dep,
)

RISE_T3M = {0: 0.0300, 1: 0.0400, **{q: 0.0400 for q in range(2, 10)}}
FALL_T3M = {0: 0.0300, 1: 0.0400, 2: 0.0350, **{q: 0.0350 for q in range(3, 10)}}


def _inputs() -> ForeignDepInputs:
    return ForeignDepInputs(
        "FIRM_A",
        subcomponents={
            "foreign_nontime": DepositSubcomponent(0.0080, 500.0, 0.0004),
            "foreign_time": DepositSubcomponent(0.0120, 500.0, 0.0006),
        },
    )


def test_table_a7_foreign_medians():
    assert dict(TABLE_A7_FOREIGN.beta_up) == {"foreign_nontime": 0.890, "foreign_time": 1.000}
    assert dict(TABLE_A7_FOREIGN.beta_down) == {"foreign_nontime": 0.790, "foreign_time": 1.000}


def test_time_beta_one_tracks_delta_one_for_one(make_scenario):
    result = project_foreign_dep(_inputs(), make_scenario(t3m=RISE_T3M))
    time_pq1 = result.quarters[0].diagnostics.subcomponents["foreign_time"]
    assert time_pq1.rate == pytest.approx(0.0220)   # 0.0120 + 0.0100 × 1.000
    time_pq2 = result.quarters[1].diagnostics.subcomponents["foreign_time"]
    assert time_pq2.rate == pytest.approx(0.0220)   # Δ = 0


def test_nontime_up_and_down_betas(make_scenario):
    result = project_foreign_dep(_inputs(), make_scenario(t3m=FALL_T3M))
    nontime_pq1 = result.quarters[0].diagnostics.subcomponents["foreign_nontime"]
    assert nontime_pq1.rate == pytest.approx(0.0169)             # 0.0080 + 0.0100 × 0.890
    nontime_pq2 = result.quarters[1].diagnostics.subcomponents["foreign_nontime"]
    assert nontime_pq2.rate == pytest.approx(0.0169 - 0.0050 * 0.790)


def test_expense_uses_summed_subcomponent_balances(make_scenario):
    result = project_foreign_dep(_inputs(), make_scenario(t3m=RISE_T3M))
    pq1 = result.quarters[0]
    aggregate = (0.0169 * 500.0 + 0.0220 * 500.0) / 1000.0
    assert pq1.annualized_rate == pytest.approx(aggregate)
    assert pq1.average_balance == 1000.0                          # 35A + 35B, both roles
    assert pq1.quarterly_expense == pytest.approx(1000.0 * aggregate / 4.0)


def test_flat_balances_across_quarters(make_scenario):
    result = project_foreign_dep(_inputs(), make_scenario(t3m=RISE_T3M))
    assert all(q.average_balance == 1000.0 for q in result.quarters)


def test_both_balances_zero_fails(make_scenario):
    inputs = ForeignDepInputs(
        "FIRM_A",
        subcomponents={
            "foreign_nontime": DepositSubcomponent(0.0080, 0.0, 0.0004),
            "foreign_time": DepositSubcomponent(0.0120, 0.0, 0.0006),
        },
    )
    with pytest.raises(ValidationFailure, match="weights sum to zero"):
        project_foreign_dep(inputs, make_scenario(t3m=RISE_T3M))

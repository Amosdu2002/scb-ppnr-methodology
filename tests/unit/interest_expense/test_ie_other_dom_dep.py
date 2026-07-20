"""ie_other_dom_dep (Eqs A45–A47) — hand-calculable fixtures.

Non-ELB path (t3m: PQ0 3.00%, PQ1 4.00%, PQ2+ 3.50%), seeds mma 1.00% / savings
0.50% / transaction 0.20%, Table A7 betas:
  PQ1 (Δ=+0.0100, up): mma 0.0162, savings 0.0081, transaction 0.00665
  PQ2 (Δ=−0.0050, down): mma 0.012975, savings 0.006425, transaction 0.0042
  A47 with weights 600/300/100: PQ1 aggregate 0.012815.

ELB/floor path (t3m: PQ0 0.20%, PQ1 0.10%, PQ2 0.30%, PQ3 0.26%; spread 0.05%):
first_elb = 0.0020 (PQ0 is the first sub-25bp observation); mma floor 0.0025;
PQ1 ELB rate 0.0015 (below floor — legal); PQ2 unfloored 0.00274 (no bind);
PQ3 unfloored 0.002482 → floored at 0.0025."""

from __future__ import annotations

import pytest

from scb_ppnr.interest_expense import (
    DepositSubcomponent,
    OtherDomDepInputs,
    ValidationFailure,
    project_other_dom_dep,
)

HAND_T3M = {0: 0.0300, 1: 0.0400, 2: 0.0350, 3: 0.0350, 4: 0.0350,
            5: 0.0350, 6: 0.0350, 7: 0.0350, 8: 0.0350, 9: 0.0350}
ELB_T3M = {0: 0.0020, 1: 0.0010, 2: 0.0030, 3: 0.0026, 4: 0.0030,
           5: 0.0030, 6: 0.0030, 7: 0.0030, 8: 0.0030, 9: 0.0030}


def _inputs(spread: float = 0.0010, total_average_balance: float = 2000.0) -> OtherDomDepInputs:
    return OtherDomDepInputs(
        "FIRM_A",
        subcomponents={
            "mma": DepositSubcomponent(0.0100, 600.0, spread),
            "savings": DepositSubcomponent(0.0050, 300.0, spread),
            "transaction": DepositSubcomponent(0.0020, 100.0, spread),
        },
        total_average_balance=total_average_balance,
    )


def test_up_beta_on_rising_quarter_uses_pq0_delta(make_scenario):
    result = project_other_dom_dep(_inputs(), make_scenario(t3m=HAND_T3M))
    diag = result.quarters[0].diagnostics
    assert diag.subcomponents["mma"].market_rate_change == pytest.approx(0.0100)  # PQ1 − PQ0
    assert diag.subcomponents["mma"].beta_applied == pytest.approx(0.620)
    assert diag.subcomponents["mma"].rate == pytest.approx(0.0162)
    assert diag.subcomponents["savings"].rate == pytest.approx(0.0081)
    assert diag.subcomponents["transaction"].rate == pytest.approx(0.00665)


def test_down_beta_on_falling_quarter(make_scenario):
    result = project_other_dom_dep(_inputs(), make_scenario(t3m=HAND_T3M))
    diag = result.quarters[1].diagnostics
    assert diag.subcomponents["mma"].beta_applied == pytest.approx(0.645)
    assert diag.subcomponents["mma"].rate == pytest.approx(0.012975)
    assert diag.subcomponents["savings"].rate == pytest.approx(0.006425)
    assert diag.subcomponents["transaction"].rate == pytest.approx(0.0042)


def test_zero_delta_holds_rate(make_scenario):
    result = project_other_dom_dep(_inputs(), make_scenario(t3m=HAND_T3M))
    diag = result.quarters[2].diagnostics  # PQ3: Δ = 0
    assert diag.subcomponents["mma"].beta_applied == 0.0
    assert diag.subcomponents["mma"].rate == pytest.approx(0.012975)


def test_a47_aggregation_and_expense_multiplicand(make_scenario):
    result = project_other_dom_dep(_inputs(), make_scenario(t3m=HAND_T3M))
    pq1 = result.quarters[0]
    assert pq1.annualized_rate == pytest.approx(0.012815)  # (0.0162·600 + 0.0081·300 + 0.00665·100)/1000
    assert pq1.average_balance == 2000.0
    assert pq1.quarterly_expense == pytest.approx(2000.0 * 0.012815 / 4.0)
    # weights (1000) vs multiplicand (2000) are different physical sources — monitor fires
    assert any("consistency monitor" in w for w in result.warnings)


def test_elb_regime_is_equality_not_floor(make_scenario):
    result = project_other_dom_dep(_inputs(spread=0.0005), make_scenario(t3m=ELB_T3M))
    diag = result.quarters[0].diagnostics  # PQ1: t3m 0.0010 < 25 bp → ELB
    sub = diag.subcomponents["mma"]
    assert sub.regime == "elb"
    assert sub.rate == pytest.approx(0.0015)          # Treasury3m + spread, exactly
    assert diag.first_elb_treasury3m == pytest.approx(0.0020)  # PQ0 is the first sub-threshold obs
    assert sub.assumed_floor == pytest.approx(0.0025)
    assert not sub.floor_binding                       # A45 has no floor
    assert any("below the assumed floor" in w for w in result.warnings)


def test_floor_binds_only_inside_a46(make_scenario):
    result = project_other_dom_dep(_inputs(spread=0.0005), make_scenario(t3m=ELB_T3M))
    pq2 = result.quarters[1].diagnostics.subcomponents["mma"]   # Δ=+0.0020 from ELB rate
    assert pq2.regime == "non_elb"
    assert pq2.unfloored_rate == pytest.approx(0.00274)
    assert not pq2.floor_binding
    pq3 = result.quarters[2].diagnostics.subcomponents["mma"]   # Δ=−0.0004
    assert pq3.unfloored_rate == pytest.approx(0.002482)
    assert pq3.floor_binding
    assert pq3.rate == pytest.approx(0.0025)


def test_regime_transition_recorded(make_scenario):
    result = project_other_dom_dep(_inputs(spread=0.0005), make_scenario(t3m=ELB_T3M))
    regimes = [q.diagnostics.subcomponents["mma"].regime for q in result.quarters]
    assert regimes[0] == "elb"
    assert set(regimes[1:]) == {"non_elb"}


def test_boundary_exactly_25bp_takes_non_elb_with_warning(make_scenario):
    t3m = {0: 0.0300, 1: 0.0025, **{q: 0.0300 for q in range(2, 10)}}
    result = project_other_dom_dep(_inputs(), make_scenario(t3m=t3m))
    diag = result.quarters[0].diagnostics
    assert diag.subcomponents["mma"].regime == "non_elb"
    assert any("OQ-013" in w for w in result.warnings)


def test_zero_aggregation_weights_fail(make_scenario):
    subs = {
        "mma": DepositSubcomponent(0.0100, 0.0, 0.0010),
        "savings": DepositSubcomponent(0.0050, 0.0, 0.0010),
        "transaction": DepositSubcomponent(0.0020, 0.0, 0.0010),
    }
    inputs = OtherDomDepInputs("FIRM_A", subs, total_average_balance=1000.0)
    with pytest.raises(ValidationFailure, match="weights sum to zero"):
        project_other_dom_dep(inputs, make_scenario(t3m=HAND_T3M))

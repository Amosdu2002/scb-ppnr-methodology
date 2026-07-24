"""Securities engine + three models — hand-calculable goldens.

Reinvestment ledger: matured 1000 in PQ2 → 1Y Treasury bought PQ3 at y1(PQ3),
FIXED four quarters, rolls at PQ7. UST golden: face 1000, AC 960, M=4 quarters,
coupon 4% → 10 coupon + 10 accretion = 20/qtr through PQ4, then reinvested
10/qtr (y1 4%) PQ5–8, 20 at PQ9 when the roll reprices at 8%. Other-sec clean
golden: AC=face=2000, coupon=BY=5% → exactly 25/qtr, zero accretion."""

from __future__ import annotations

import pytest

from scb_ppnr.interest_income import (
    FLOOR_MODE_NONE,
    FLOOR_MODE_SECURITY,
    FLOOR_MODE_ZERO,
    MODEL_MBS,
    MODEL_OTHER_SEC,
    MODEL_UST,
    RATE_FIXED,
    RATE_FLOATING,
    RATE_ZERO_COUPON,
    SecurityPosition,
    ValidationFailure,
    assign_model,
    project_mbs,
    project_other_sec,
    project_ust,
    reinvestment_income,
)
from scb_ppnr.interest_income.securities_engine import (
    effective_interest_step,
    floating_coupon_path,
)
from conftest import flat


def _pos(model: str, sid: str = "SEC000001", **kw) -> SecurityPosition:
    defaults = dict(
        model=model, category="test", rate_type=RATE_FIXED, accounting_intent="AFS",
        current_face=1000.0, amortized_cost=1000.0,
    )
    defaults.update(kw)
    return SecurityPosition(security_id=sid, **defaults)


# ---------------------------------------------------------------- engine

def test_reinvestment_rolls_with_fixed_four_quarter_coupon(make_income_scenario):
    t1y = {**flat(0.0400), 7: 0.0600}
    scenario = make_income_scenario(t1y=t1y)
    income, balance = reinvestment_income({2: 1000.0}, scenario)
    assert [round(income[q], 6) for q in range(1, 10)] == [0, 0, 10.0, 10.0, 10.0, 10.0, 15.0, 15.0, 15.0]
    assert balance[3] == balance[9] == 1000.0 and balance[2] == 0.0


def test_floating_floor_modes(make_income_scenario):
    scenario = make_income_scenario(t3m={0: 0.0100, **flat(0.0060)})
    pos = _pos(MODEL_OTHER_SEC, rate_type=RATE_FLOATING, coupon_rate=0.0020, coupon_floor=0.0010)
    raw = floating_coupon_path(pos, scenario, FLOOR_MODE_NONE, [])
    assert raw[1] == pytest.approx(-0.0020)                       # margin −0.008 + 0.006
    zero = floating_coupon_path(pos, scenario, FLOOR_MODE_ZERO, [])
    assert zero[1] == 0.0
    floored = floating_coupon_path(pos, scenario, FLOOR_MODE_SECURITY, [])
    assert floored[1] == pytest.approx(0.0010)
    positive = _pos(MODEL_OTHER_SEC, rate_type=RATE_FLOATING, coupon_rate=0.0500)
    for mode in (FLOOR_MODE_NONE, FLOOR_MODE_ZERO, FLOOR_MODE_SECURITY):
        assert floating_coupon_path(positive, scenario, mode, [])[1] == pytest.approx(0.0460)


def test_effective_interest_step_hand_values():
    total, accretion, ac = effective_interest_step(900.0, 0.08, 10.0)
    assert (total, accretion, ac) == (pytest.approx(18.0), pytest.approx(8.0), pytest.approx(908.0))


# ---------------------------------------------------------------- ii_ust

def test_ust_golden_with_maturity_and_roll(make_income_scenario):
    scenario = make_income_scenario(t1y={**flat(0.0400), 9: 0.0800})
    maturing = _pos(MODEL_UST, "UST000001", coupon_rate=0.04, amortized_cost=960.0, maturity_quarters=4)
    perpetual = _pos(MODEL_UST, "UST000002", current_face=2000.0, amortized_cost=2000.0,
                     coupon_rate=0.03, maturity_quarters=40)
    result = project_ust([maturing, perpetual], scenario, firm_id="FIRM_A")
    assert [round(v, 6) for v in result.income_path().values()] == [35.0, 35.0, 35.0, 35.0, 25.0, 25.0, 25.0, 25.0, 35.0]
    d5 = result.quarters[4].diagnostics
    assert d5.reinvested_income == pytest.approx(10.0) and d5.reinvested_balance == 1000.0
    assert result.quarters[3].diagnostics.matured_face == pytest.approx(1000.0)
    assert result.quarters[0].diagnostics.securities_alive == 2
    assert result.quarters[8].diagnostics.securities_alive == 1


def test_ust_missing_coupon_and_floater_surface(make_income_scenario):
    scenario = make_income_scenario()
    with pytest.raises(ValidationFailure, match="OQ-027"):
        project_ust([_pos(MODEL_UST, coupon_rate=None, maturity_quarters=8)], scenario, firm_id="F")
    with pytest.raises(ValidationFailure, match="floating-rate U.S. Treasury"):
        project_ust([_pos(MODEL_UST, rate_type=RATE_FLOATING, coupon_rate=0.04, maturity_quarters=8)],
                    scenario, firm_id="F")


# ---------------------------------------------------------------- ii_mbs

def test_mbs_agency_face_path_recursion(make_income_scenario):
    scenario = make_income_scenario()
    face_path = {0: 1000.0, 1: 800.0, **{q: 800.0 for q in range(2, 10)}}
    pos = _pos(MODEL_MBS, "AGY000001", coupon_rate=0.05, amortized_cost=950.0,
               wal_years=2.5, face_path=face_path)
    result = project_mbs([pos], scenario, firm_id="FIRM_A", floor_mode=FLOOR_MODE_NONE)
    d1, d2 = result.quarters[0].diagnostics, result.quarters[1].diagnostics
    assert d1.coupon_accrual == pytest.approx(12.5)               # 5% × 1000 / 4 (prior-EOP face)
    assert d1.accretion == pytest.approx(5.0)                     # (1000 − 950) / 10
    assert d2.coupon_accrual == pytest.approx(10.0)               # 5% × 800 / 4
    assert d2.accretion == pytest.approx(3.5)                     # (800 − 765) / 10; AC scaled 950×0.8+5
    assert result.quarters[2].diagnostics.accretion == pytest.approx(3.15)


def test_mbs_agency_pq0_mismatch_warns(make_income_scenario):
    face_path = {0: 990.0, **{q: 990.0 for q in range(1, 10)}}
    pos = _pos(MODEL_MBS, "AGY000002", coupon_rate=0.05, wal_years=2.0, face_path=face_path)
    result = project_mbs([pos], make_income_scenario(), firm_id="F", floor_mode=FLOOR_MODE_NONE)
    assert any("differs" in w for w in result.warnings)


def test_mbs_other_fixed_effective_interest_and_zero_coupon(make_income_scenario):
    scenario = make_income_scenario()
    fixed = _pos(MODEL_MBS, "CMB000001", coupon_rate=0.04, amortized_cost=900.0, book_yield=0.08)
    zero = _pos(MODEL_MBS, "CMB000002", rate_type=RATE_ZERO_COUPON, coupon_rate=None,
                current_face=500.0, amortized_cost=500.0, book_yield=0.06)
    result = project_mbs([fixed, zero], scenario, firm_id="F", floor_mode=FLOOR_MODE_NONE)
    d1 = result.quarters[0].diagnostics
    assert d1.coupon_accrual == pytest.approx(10.0)               # fixed cash only; zero-coupon cash = 0
    assert d1.accretion == pytest.approx(8.0 + 7.5)               # EI residual + zero-coupon accrual
    d2 = result.quarters[1].diagnostics
    assert d2.accretion == pytest.approx(8.16 + 7.6125)


def test_mbs_floater_uses_straight_line_interim(make_income_scenario):
    scenario = make_income_scenario(t3m={0: 0.0300, **flat(0.0300)})
    pos = _pos(MODEL_MBS, "CMB000003", rate_type=RATE_FLOATING, coupon_rate=0.05,
               amortized_cost=980.0, book_yield=0.06, wal_years=5.0)
    result = project_mbs([pos], scenario, firm_id="F", floor_mode=FLOOR_MODE_NONE)
    d1 = result.quarters[0].diagnostics
    assert d1.coupon_accrual == pytest.approx(12.5)               # margin 2% + 3M 3% = 5% × 1000/4
    assert d1.accretion == pytest.approx(1.0)                     # (1000 − 980) / (4 × 5)
    assert any("INTERIM" in w for w in result.warnings)


# ---------------------------------------------------------------- ii_other_sec

def test_other_sec_clean_golden(make_income_scenario):
    pos = _pos(MODEL_OTHER_SEC, "OTH000001", current_face=2000.0, amortized_cost=2000.0,
               coupon_rate=0.05, book_yield=0.05)
    result = project_other_sec([pos], make_income_scenario(), firm_id="F", floor_mode=FLOOR_MODE_NONE)
    assert all(v == pytest.approx(25.0) for v in result.income_path().values())
    assert all(q.diagnostics.accretion == pytest.approx(0.0) for q in result.quarters)


def test_other_sec_floater_book_yield_shift(make_income_scenario):
    scenario = make_income_scenario(t3m={0: 0.0100, **flat(0.0300)})     # shift +2%
    pos = _pos(MODEL_OTHER_SEC, "OTH000002", coupon_rate=0.02, book_yield=0.06,
               amortized_cost=900.0, rate_type=RATE_FLOATING)
    result = project_other_sec([pos], scenario, firm_id="F", floor_mode=FLOOR_MODE_NONE)
    d1 = result.quarters[0].diagnostics
    assert d1.coupon_accrual == pytest.approx(10.0)               # coupon 2%+2% = 4% × 1000/4
    assert d1.accretion == pytest.approx(8.0)                     # AC 900 × BY (6%+2%)/4 − 10
    assert result.quarters[0].quarterly_income == pytest.approx(18.0)


def test_other_sec_maturity_reinvests(make_income_scenario):
    scenario = make_income_scenario()
    pos = _pos(MODEL_OTHER_SEC, "OTH000003", coupon_rate=0.05, book_yield=0.05,
               maturity_quarters=2)
    result = project_other_sec([pos], scenario, firm_id="F", floor_mode=FLOOR_MODE_NONE)
    assert result.quarters[1].diagnostics.matured_face == pytest.approx(1000.0)
    assert result.quarters[2].diagnostics.reinvested_income == pytest.approx(10.0)   # 1000 × 4% / 4
    assert result.quarters[2].diagnostics.coupon_accrual == 0.0


# ---------------------------------------------------------------- schemas

def test_assign_model_policy():
    assert assign_model("US Treasuries & Agencies") == (MODEL_UST, False)
    assert assign_model("Agency MBS") == (MODEL_MBS, True)
    assert assign_model("CMBS") == (MODEL_MBS, False)
    with pytest.raises(ValidationFailure, match="not in the confirmed PID-SEC-5 mapping"):
        assign_model("Covered Bond")


def test_position_validation():
    with pytest.raises(ValidationFailure, match="zero-coupon security carries a nonzero coupon"):
        _pos(MODEL_MBS, rate_type=RATE_ZERO_COUPON, coupon_rate=0.03)
    with pytest.raises(ValidationFailure, match="wal_years must be > 0"):
        _pos(MODEL_MBS, wal_years=-0.1)
    with pytest.raises(ValidationFailure, match="equity-intent"):
        _pos(MODEL_OTHER_SEC, accounting_intent="EQ")

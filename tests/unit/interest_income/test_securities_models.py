"""Securities engine + three models — hand-calculable goldens.

Reinvestment ledger: matured 1000 in PQ2 → 1Y Treasury bought PQ3 at y1(PQ3),
FIXED four quarters, rolls at PQ7. UST golden: face 1000, AC 960, M=4 quarters,
coupon 4% → 10 coupon + 10 accretion = 20/qtr through PQ4, then reinvested
10/qtr (y1 4%) PQ5–8, 20 at PQ9 when the roll reprices at 8%. Other-sec clean
golden: AC=face=2000, coupon=BY=5% → exactly 25/qtr, zero accretion."""

from __future__ import annotations

import pytest

from scb_ppnr.interest_income import (
    FLOAT_PROJECTION_BLEND13,
    FLOAT_PROJECTION_FLAT_C0,
    FLOAT_PROJECTION_FREEZE1,
    FLOAT_PROJECTION_NEG_HOLD,
    FLOAT_PROJECTION_NEG_HOLD_BLEND,
    FLOOR_MODE_NONE,
    FLOOR_MODE_SECURITY,
    FLOOR_MODE_SECURITY_ELSE_ZERO,
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
    floating_coupon_path,
    reference_accretion_step,
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


def test_floating_security_floor_else_zero_mode(make_income_scenario):
    # Reference-workbook rule (2026-07-24): EVERY floater floored at
    # max(margin + 3M(q), security floor if on file else 0).
    scenario = make_income_scenario(t3m={0: 0.0100, **flat(0.0060)})
    with_floor = _pos(MODEL_OTHER_SEC, rate_type=RATE_FLOATING, coupon_rate=0.0020, coupon_floor=0.0010)
    sink: list[str] = []
    path = floating_coupon_path(with_floor, scenario, FLOOR_MODE_SECURITY_ELSE_ZERO, sink)
    assert all(path[q] == pytest.approx(0.0010) for q in range(1, 10))       # raw −0.002 → floor
    assert any("security_floor_else_zero" in w and "security floor" in w for w in sink)

    no_floor = _pos(MODEL_OTHER_SEC, rate_type=RATE_FLOATING, coupon_rate=0.0020)
    path0 = floating_coupon_path(no_floor, scenario, FLOOR_MODE_SECURITY_ELSE_ZERO, [])
    assert all(path0[q] == 0.0 for q in range(1, 10))                        # no floor on file → 0

    # Positive-margin floater still binds when the path drops below its floor —
    # this is the mode's difference vs the negative-margin-scoped modes.
    positive = _pos(MODEL_OTHER_SEC, rate_type=RATE_FLOATING, coupon_rate=0.0500, coupon_floor=0.0480)
    sink2: list[str] = []
    pathp = floating_coupon_path(positive, scenario, FLOOR_MODE_SECURITY_ELSE_ZERO, sink2)
    assert pathp[1] == pytest.approx(0.0480)                                 # raw 0.046 < floor 0.048
    assert floating_coupon_path(positive, scenario, FLOOR_MODE_SECURITY, [])[1] == pytest.approx(0.0460)


def test_floating_projection_modes(make_income_scenario):
    # PID-SEC-10: neg_hold holds a negative-margin floater at the launch coupon for
    # all nine quarters; neg_hold_blend13 adds the monthly-reset PQ1 for positive margins.
    scenario = make_income_scenario(t3m={0: 0.0100, **flat(0.0060)})
    negative = _pos(MODEL_OTHER_SEC, rate_type=RATE_FLOATING, coupon_rate=0.0020)
    sink: list[str] = []
    held = floating_coupon_path(negative, scenario, FLOOR_MODE_ZERO, sink, FLOAT_PROJECTION_NEG_HOLD)
    assert all(held[q] == pytest.approx(0.0020) for q in range(1, 10))       # never re-projected
    assert any("PID-SEC-10" in w and "held" in w for w in sink)

    positive = _pos(MODEL_OTHER_SEC, rate_type=RATE_FLOATING, coupon_rate=0.0500)   # margin +4%
    hold_only = floating_coupon_path(positive, scenario, FLOOR_MODE_ZERO, [], FLOAT_PROJECTION_NEG_HOLD)
    assert hold_only[1] == pytest.approx(0.0460)                             # positive margin: spot unchanged
    blended = floating_coupon_path(positive, scenario, FLOOR_MODE_ZERO, [], FLOAT_PROJECTION_NEG_HOLD_BLEND)
    assert blended[1] == pytest.approx(0.0500 / 3 + 2 * 0.0460 / 3)          # ⅓·c0 + ⅔·(margin+3M(1))
    assert blended[2] == pytest.approx(0.0460)                               # spot thereafter

    flat_all = floating_coupon_path(positive, scenario, FLOOR_MODE_ZERO, [], FLOAT_PROJECTION_FLAT_C0)
    assert all(flat_all[q] == pytest.approx(0.0500) for q in range(1, 10))   # every floater held
    blend_no_hold = floating_coupon_path(negative, scenario, FLOOR_MODE_ZERO, [], FLOAT_PROJECTION_BLEND13)
    assert blend_no_hold[1] == 0.0 and blend_no_hold[2] == 0.0               # negative margin NOT held —
                                                                             # blended/spot path floors at 0


def test_floating_projection_freeze1(make_income_scenario):
    # PID-SEC-10 'freeze1' (2026-07-28, Agency-MBS-identified): PQ1 still accrues at
    # the coupon fixed before launch; the coupon then resets ONCE off 3M(PQ1) and is
    # frozen there for PQ2..9 — so a falling 3M path after PQ1 never reaches it.
    scenario = make_income_scenario(t3m={0: 0.0100, 1: 0.0060, **{q: 0.0010 for q in range(2, 10)}})
    positive = _pos(MODEL_OTHER_SEC, rate_type=RATE_FLOATING, coupon_rate=0.0500)   # margin +4%
    sink: list[str] = []
    path = floating_coupon_path(positive, scenario, FLOOR_MODE_ZERO, sink, FLOAT_PROJECTION_FREEZE1)
    assert path[1] == pytest.approx(0.0500)                                  # launch coupon
    frozen = 0.0400 + 0.0060                                                 # margin + 3M(PQ1)
    assert all(path[q] == pytest.approx(frozen) for q in range(2, 10))       # frozen, not tracking 3M
    assert any("freeze1" in w for w in sink)

    # The frozen leg floors at 0 (part of the identified rule), while PQ1 keeps the
    # launch coupon whatever the margin.
    negative = _pos(MODEL_OTHER_SEC, rate_type=RATE_FLOATING, coupon_rate=0.0020)   # margin -0.8%
    deep = floating_coupon_path(negative, scenario, FLOOR_MODE_NONE, [], FLOAT_PROJECTION_FREEZE1)
    assert deep[1] == pytest.approx(0.0020)
    assert all(deep[q] == 0.0 for q in range(2, 10))                          # -0.8% + 0.6% < 0 -> 0


def test_other_sec_projection_override_per_category(make_income_scenario):
    scenario = make_income_scenario(t3m={0: 0.0100, **flat(0.0060)})
    clo = _pos(MODEL_OTHER_SEC, "CLO0000X1", category="CLO", rate_type=RATE_FLOATING, coupon_rate=0.0500)
    result = project_other_sec([clo], scenario, firm_id="F", floor_mode=FLOOR_MODE_ZERO,
                               floating_projection="spot",
                               projection_overrides={"CLO": FLOAT_PROJECTION_FLAT_C0})
    assert result.quarters[0].diagnostics.coupon_accrual == pytest.approx(12.5)   # held flat, not 11.5 spot
    assert result.quarters[8].diagnostics.coupon_accrual == pytest.approx(12.5)


def test_other_sec_book_yield_category_override(make_income_scenario):
    # PID-SEC-11: configured categories accrue at book yield held flat; missing BY
    # falls back to the coupon with a surfaced warning.
    scenario = make_income_scenario()
    muni = _pos(MODEL_OTHER_SEC, "MUN0000X1", category="Municipal Bond", coupon_rate=0.04,
                book_yield=0.05, maturity_quarters=40, maturity_years=10.0)
    no_by = _pos(MODEL_OTHER_SEC, "MUN0000X2", category="Municipal Bond", coupon_rate=0.04,
                 maturity_quarters=40, maturity_years=10.0)
    result = project_other_sec([muni, no_by], scenario, firm_id="F", floor_mode=FLOOR_MODE_ZERO,
                               book_yield_categories=("Municipal Bond",))
    d1 = result.quarters[0].diagnostics
    assert d1.coupon_accrual == pytest.approx(1000.0 * 0.05 / 4 + 1000.0 * 0.04 / 4)   # BY + coupon fallback
    assert any("BOOK YIELD" in w and "1 position" in w for w in result.warnings)
    assert any(w.startswith("MUN0000X2") and "no book yield" in w for w in result.warnings)


def test_reference_accretion_step_hand_values():
    # PID-SEC-8: AA = (prior face − prior AC)/denominator; AC = prior + AA − paydown.
    aa, ac = reference_accretion_step(1000.0, 950.0, 800.0, 10.0, paydown=200.0)
    assert (aa, ac) == (pytest.approx(5.0), pytest.approx(755.0))
    aa_zero, ac_zero = reference_accretion_step(1000.0, 950.0, 0.0, 10.0, paydown=1000.0)
    assert aa_zero == 0.0 and ac_zero == pytest.approx(-50.0)     # zero-face guard; AC absorbs the paydown


# ---------------------------------------------------------------- ii_ust

def test_ust_golden_with_maturity_and_roll(make_income_scenario):
    scenario = make_income_scenario(t1y={**flat(0.0400), 9: 0.0800})
    maturing = _pos(MODEL_UST, "UST000001", coupon_rate=0.04, amortized_cost=960.0,
                    maturity_quarters=4, maturity_years=1.0)
    perpetual = _pos(MODEL_UST, "UST000002", current_face=2000.0, amortized_cost=2000.0,
                     coupon_rate=0.03, maturity_quarters=40, maturity_years=10.0)
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
        project_ust([_pos(MODEL_UST, coupon_rate=None, maturity_quarters=8, maturity_years=2.0)],
                    scenario, firm_id="F")
    with pytest.raises(ValidationFailure, match="floating-rate U.S. Treasury"):
        project_ust([_pos(MODEL_UST, rate_type=RATE_FLOATING, coupon_rate=0.04,
                          maturity_quarters=8, maturity_years=2.0)], scenario, firm_id="F")


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
    assert d2.accretion == pytest.approx(4.5)                     # PID-SEC-8: AC1 = 950 + 5 − 200 = 755 → (800 − 755)/10
    assert result.quarters[2].diagnostics.accretion == pytest.approx(4.05)   # AC2 = 759.5 → (800 − 759.5)/10


def test_mbs_paydown_proceeds_reinvest(make_income_scenario):
    scenario = make_income_scenario()                     # t1y flat 4%
    face_path = {0: 1000.0, 1: 800.0, **{q: 800.0 for q in range(2, 10)}}
    pos = _pos(MODEL_MBS, "AGY000003", coupon_rate=0.05, amortized_cost=950.0,
               wal_years=2.5, face_path=face_path)
    result = project_mbs([pos], scenario, firm_id="F", floor_mode=FLOOR_MODE_NONE)
    assert result.quarters[0].diagnostics.reinvested_income == 0.0
    # 200 paid down in PQ1 → 1Y Treasury bought PQ2 at 4%, rolls at PQ6: 2.0/qtr PQ2..PQ9
    assert all(result.quarters[q - 1].diagnostics.reinvested_income == pytest.approx(2.0) for q in range(2, 10))
    off = project_mbs([pos], scenario, firm_id="F", floor_mode=FLOOR_MODE_NONE, reinvest_paydowns=False)
    assert all(q.diagnostics.reinvested_income == 0.0 for q in off.quarters)
    assert any("reinvest_paydowns=false" in w for w in off.warnings)


def test_mbs_agency_pq0_mismatch_warns(make_income_scenario):
    face_path = {0: 990.0, **{q: 990.0 for q in range(1, 10)}}
    pos = _pos(MODEL_MBS, "AGY000002", coupon_rate=0.05, wal_years=2.0, face_path=face_path)
    result = project_mbs([pos], make_income_scenario(), firm_id="F", floor_mode=FLOOR_MODE_NONE)
    assert any("differs" in w for w in result.warnings)


def test_mbs_other_fixed_and_zero_coupon_reference_form(make_income_scenario):
    scenario = make_income_scenario()
    fixed = _pos(MODEL_MBS, "CMB000001", coupon_rate=0.04, amortized_cost=900.0,
                 book_yield=0.08, maturity_years=10.0)
    zero = _pos(MODEL_MBS, "CMB000002", rate_type=RATE_ZERO_COUPON, coupon_rate=None,
                current_face=500.0, amortized_cost=400.0, book_yield=0.06, maturity_years=5.0)
    result = project_mbs([fixed, zero], scenario, firm_id="F", floor_mode=FLOOR_MODE_NONE)
    d1 = result.quarters[0].diagnostics
    assert d1.coupon_accrual == pytest.approx(10.0)               # fixed cash only; zero-coupon cash = 0
    assert d1.accretion == pytest.approx(2.5 + 5.0)               # (1000−900)/40 + (500−400)/20
    d2 = result.quarters[1].diagnostics
    assert d2.accretion == pytest.approx(2.4375 + 4.75)           # t-dated AC: 902.5 / 405


def test_mbs_floater_reference_accretion(make_income_scenario):
    scenario = make_income_scenario(t3m={0: 0.0300, **flat(0.0300)})
    pos = _pos(MODEL_MBS, "CMB000003", rate_type=RATE_FLOATING, coupon_rate=0.05,
               amortized_cost=980.0, book_yield=0.06, wal_years=5.0, maturity_years=5.0)
    result = project_mbs([pos], scenario, firm_id="F", floor_mode=FLOOR_MODE_NONE)
    d1 = result.quarters[0].diagnostics
    assert d1.coupon_accrual == pytest.approx(12.5)               # margin 2% + 3M 3% = 5% × 1000/4
    assert d1.accretion == pytest.approx(1.0)                     # (1000 − 980) / (4 × 5)


# ---------------------------------------------------------------- ii_other_sec

def test_other_sec_clean_golden(make_income_scenario):
    pos = _pos(MODEL_OTHER_SEC, "OTH000001", current_face=2000.0, amortized_cost=2000.0,
               coupon_rate=0.05, book_yield=0.05, maturity_years=10.0)
    result = project_other_sec([pos], make_income_scenario(), firm_id="F", floor_mode=FLOOR_MODE_NONE)
    assert all(v == pytest.approx(25.0) for v in result.income_path().values())
    assert all(q.diagnostics.accretion == pytest.approx(0.0) for q in result.quarters)


def test_other_sec_floater_reference_form(make_income_scenario):
    scenario = make_income_scenario(t3m={0: 0.0100, **flat(0.0300)})     # coupon shift +2%
    pos = _pos(MODEL_OTHER_SEC, "OTH000002", coupon_rate=0.02, book_yield=0.06,
               amortized_cost=900.0, rate_type=RATE_FLOATING, maturity_years=5.0)
    result = project_other_sec([pos], scenario, firm_id="F", floor_mode=FLOOR_MODE_NONE)
    d1 = result.quarters[0].diagnostics
    assert d1.coupon_accrual == pytest.approx(10.0)               # coupon 2%+2% = 4% × 1000/4
    assert d1.accretion == pytest.approx(5.0)                     # PID-SEC-8: (1000 − 900)/(4 × 5)
    assert result.quarters[0].quarterly_income == pytest.approx(15.0)
    assert result.quarters[1].diagnostics.accretion == pytest.approx(4.75)   # AC1 = 905 → (1000−905)/20


def test_on_error_skip_isolates_a_failing_security(make_income_scenario):
    scenario = make_income_scenario()
    broken = _pos(MODEL_OTHER_SEC, "BAD000001", rate_type=RATE_FLOATING, coupon_rate=None,
                  book_yield=0.06, amortized_cost=900.0)          # floater without a t0 coupon
    clean = _pos(MODEL_OTHER_SEC, "OTH000009", current_face=2000.0, amortized_cost=2000.0,
                 coupon_rate=0.05, book_yield=0.05)
    with pytest.raises(ValidationFailure, match="no t=0 coupon"):
        project_other_sec([broken, clean], scenario, firm_id="F", floor_mode=FLOOR_MODE_NONE)
    result = project_other_sec([broken, clean], scenario, firm_id="F",
                               floor_mode=FLOOR_MODE_NONE, on_error="skip")
    assert result.income_path()[1] == pytest.approx(25.0)         # clean security only
    assert any(w.startswith("HIGHLIGHT BAD000001") for w in result.warnings)
    assert any("understated" in w for w in result.warnings)


def test_other_sec_maturity_reinvests(make_income_scenario):
    scenario = make_income_scenario()
    pos = _pos(MODEL_OTHER_SEC, "OTH000003", coupon_rate=0.05, book_yield=0.05,
               maturity_quarters=2, maturity_years=0.5)
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

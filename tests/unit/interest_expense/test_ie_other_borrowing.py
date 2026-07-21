"""ie_other_borrowing (Eq A53 + PID-OB-5) — hand-calculable fixture.

Shares CP 0.10 / subdebt 0.20; t3m flat 4%, BBB flat 6% →
R0 = 0.04 + 0.254·0.06 − 0.036·0.10 + 0.066·0.20 = 0.06504 (flat).
Flat balance 1000; implied expense flat 20 → α_b = (4·180 − 9000·0.06504)/9000
= 0.014960 and the modeled path is exactly 20 per quarter.
PQ0 actual expense does not exist anywhere in this model's API (PID-OB-5)."""

from __future__ import annotations

import pytest

from scb_ppnr.interest_expense import (
    TABLE_A9_OTHER_BORROWING,
    OtherBorrowingInputs,
    OtherBorrowingParams,
    ValidationFailure,
    balance_path,
    calibrate_alpha_b,
    implied_other_borrowing_path,
    pre_alpha_rate_path,
    project_other_borrowing,
    run_other_borrowing,
)
from scb_ppnr.interest_expense.schemas import PROJECTION_QUARTERS
from conftest import flat

INPUTS = OtherBorrowingInputs("FIRM_A", total_balance=1000.0, cp_share=0.10, subdebt_share=0.20)
R0_HAND = 0.04 + 0.254 * 0.06 - 0.036 * 0.10 + 0.066 * 0.20  # 0.06504
ALPHA_HAND = (4.0 * 180.0 - 9.0 * 1000.0 * R0_HAND) / 9000.0  # 0.014960


def _scenario(make_scenario):
    return make_scenario(t3m={0: 0.0300, **flat(0.0400)}, bbb=flat(0.0600))


def _siblings(stub_result, scenario_id="sev_adverse"):
    return (
        stub_result("ie_dom_time_dep", scenario_id=scenario_id, expenses=flat(8.0)),
        stub_result("ie_other_dom_dep", scenario_id=scenario_id, expenses=flat(7.0)),
        stub_result("ie_foreign_dep", scenario_id=scenario_id, expenses=flat(5.0)),
        stub_result("ie_fed_funds_repo", scenario_id=scenario_id, expenses=flat(10.0)),
    )


def test_published_betas_used_unchanged(make_scenario):
    assert TABLE_A9_OTHER_BORROWING == OtherBorrowingParams(beta_bbb=0.254, beta_cp=-0.036, beta_subdebt=0.066)
    rates = pre_alpha_rate_path(INPUTS, _scenario(make_scenario))
    assert all(rates[q] == pytest.approx(R0_HAND) for q in PROJECTION_QUARTERS)


def test_implied_quarterly_residuals(stub_result):
    implied = implied_other_borrowing_path(flat(40.0), *_siblings(stub_result))
    assert all(implied[q] == pytest.approx(40.0 - 30.0) for q in PROJECTION_QUARTERS)


def test_units_mismatch_guard_trips_in_both_directions(stub_result):
    # Siblings sum to 30/quarter (270 cumulative). FRB total 1000× too big — as if
    # Schedule G balances were fed in billions against an FRB path in millions:
    with pytest.raises(ValidationFailure, match="money-unit mismatch"):
        implied_other_borrowing_path(flat(40000.0), *_siblings(stub_result))
    # FRB total 1000× too small — billions against Schedule G millions, the direction
    # the |alpha_b| magnitude warning can miss:
    with pytest.raises(ValidationFailure, match="money-unit mismatch"):
        implied_other_borrowing_path(flat(0.04), *_siblings(stub_result))


def test_units_ratio_under_guard_passes(stub_result):
    # 1400×9 = 12600 vs 270 cumulative → ×46.7, under the 50× screen: legal, no error.
    implied = implied_other_borrowing_path(flat(1400.0), *_siblings(stub_result))
    assert implied[1] == pytest.approx(1400.0 - 30.0)


def test_closed_form_alpha_exact_cumulative_match(make_scenario):
    cal = calibrate_alpha_b(flat(20.0), balance_path(INPUTS), pre_alpha_rate_path(INPUTS, _scenario(make_scenario)))
    assert cal.alpha_b == pytest.approx(ALPHA_HAND, rel=1e-12)
    assert cal.cumulative_implied == pytest.approx(180.0)
    assert cal.cumulative_modeled == pytest.approx(180.0, abs=1e-9)
    assert abs(cal.cumulative_difference) <= 1e-9
    assert all(cal.modeled_path[q] == pytest.approx(20.0) for q in PROJECTION_QUARTERS)


def test_alpha_constant_across_all_nine_quarters(make_scenario, stub_result):
    result, cal = run_other_borrowing(INPUTS, _scenario(make_scenario), flat(50.0), *_siblings(stub_result))
    alphas = {row.diagnostics.alpha_b for row in result.quarters}
    assert alphas == {cal.alpha_b}


def test_quarterly_paths_differ_but_cumulative_matches(make_scenario):
    implied = {**flat(20.0), 1: 10.0, 2: 30.0}  # same 180 total, uneven quarters
    cal = calibrate_alpha_b(implied, balance_path(INPUTS), pre_alpha_rate_path(INPUTS, _scenario(make_scenario)))
    assert cal.alpha_b == pytest.approx(ALPHA_HAND, rel=1e-12)          # cumulative target unchanged
    assert cal.modeled_path[1] == pytest.approx(20.0)                    # NOT forced to the quarterly residual
    assert cal.modeled_path[1] != pytest.approx(cal.implied_path[1])
    assert cal.quarterly_difference_path[1] == pytest.approx(10.0)
    assert cal.quarterly_difference_path[2] == pytest.approx(-10.0)
    assert sum(cal.quarterly_difference_path.values()) == pytest.approx(0.0, abs=1e-9)


def test_zero_cumulative_balance_fails(make_scenario):
    zero_balances = {q: 0.0 for q in PROJECTION_QUARTERS}
    with pytest.raises(ValidationFailure, match="zero or invalid"):
        calibrate_alpha_b(flat(20.0), zero_balances, pre_alpha_rate_path(INPUTS, _scenario(make_scenario)))


def test_pq0_scenario_values_never_used(make_scenario, stub_result):
    scenario_a = make_scenario(t3m={0: 0.0300, **flat(0.0400)}, bbb=flat(0.0600))
    scenario_b = make_scenario(t3m={0: 0.0010, **flat(0.0400)}, bbb=flat(0.0600))  # only PQ0 differs
    result_a, _ = run_other_borrowing(INPUTS, scenario_a, flat(50.0), *_siblings(stub_result))
    result_b, _ = run_other_borrowing(INPUTS, scenario_b, flat(50.0), *_siblings(stub_result))
    assert result_a == result_b


def test_negative_implied_quarter_logged_never_clamped(stub_result, make_scenario):
    implied = implied_other_borrowing_path(flat(20.0), *_siblings(stub_result))  # 20 − 30 = −10
    cal = calibrate_alpha_b(implied, balance_path(INPUTS), pre_alpha_rate_path(INPUTS, _scenario(make_scenario)))
    assert all(cal.implied_path[q] == pytest.approx(-10.0) for q in PROJECTION_QUARTERS)
    assert any("negative implied" in w for w in cal.warnings)


def test_wrong_sibling_position_fails(stub_result):
    dtd, odd, fgn, ffr = _siblings(stub_result)
    with pytest.raises(ValidationFailure, match="expected a ie_dom_time_dep"):
        implied_other_borrowing_path(flat(40.0), ffr, odd, fgn, dtd)


def test_sibling_from_other_run_fails(stub_result, make_scenario):
    dtd, odd, fgn, _ = _siblings(stub_result)
    foreign_run_ffr = stub_result("ie_fed_funds_repo", scenario_id="baseline", expenses=flat(10.0))
    with pytest.raises(ValidationFailure, match="does not match expected"):
        implied_other_borrowing_path(flat(40.0), dtd, odd, fgn, foreign_run_ffr)


def test_calibration_must_match_inputs_and_scenario(make_scenario):
    cal = calibrate_alpha_b(flat(20.0), balance_path(INPUTS), pre_alpha_rate_path(INPUTS, _scenario(make_scenario)))
    other_inputs = OtherBorrowingInputs("FIRM_A", total_balance=1000.0, cp_share=0.30, subdebt_share=0.20)
    with pytest.raises(ValidationFailure, match="pre-alpha rate mismatch"):
        project_other_borrowing(other_inputs, _scenario(make_scenario), cal)


def test_calibration_must_match_balance(make_scenario):
    half_balance = {q: 500.0 for q in PROJECTION_QUARTERS}
    cal = calibrate_alpha_b(flat(20.0), half_balance, pre_alpha_rate_path(INPUTS, _scenario(make_scenario)))
    with pytest.raises(ValidationFailure, match="modeled expense mismatch"):
        project_other_borrowing(INPUTS, _scenario(make_scenario), cal)

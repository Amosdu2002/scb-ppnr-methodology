"""nii_trading_al (Eq A52 + PID-TRD-1/PID-TRD-3) — hand-calculable fixture.

Trading assets 1500 / liabilities 500 → NetTA = 1000, flat. t3m flat 4% →
R0 = 0.278·0.04 = 0.01112 (annualized, flat). Six siblings flat 10/5/6/4/3/2 →
Σ = 30/quarter; FRB income flat 50 → implied flat 20, 9Q = 180. Closed form
(PID-TRD-3 annualized basis, the PID-OB-5 shape WITH ×4):

    α_b = (4·180 − 9·1000·0.01112) / 9000 = (720 − 100.08)/9000 = 0.068880

Rate = 0.01112 + 0.06888 = 0.08 exactly → modeled = 1000·0.08/4 = 20 per
quarter — the cumulative match is exact and the fixture is round. BASIS PIN:
under the superseded quarterly-LHS reading (no ×4) the same fixture would give
α = (180 − 100.08)/9000 = 0.008880 — the golden below fails by ~×7.8 if the ×4
is ever dropped, and the modeled path would be 4× low if the output ÷4 were
dropped instead. PQ0 actuals and PQ0 scenario values do not exist anywhere in
this model's API (PID-TRD-1)."""

from __future__ import annotations

import pytest

from scb_ppnr.interest_income import (
    TABLE_A9_TRADING,
    TradingNiiInputs,
    TradingNiiParams,
    ValidationFailure,
    calibrate_alpha_b,
    implied_trading_path,
    net_trading_asset_path,
    pre_alpha_rate_path,
    project_trading_nii,
    run_trading_nii,
)
from scb_ppnr.interest_income.schemas import PROJECTION_QUARTERS
from conftest import flat

INPUTS = TradingNiiInputs("FIRM_A", trading_assets_avg_balance=1500.0, trading_liabilities_avg_balance=500.0)
R0_HAND = 0.278 * 0.04                                   # 0.01112
ALPHA_HAND = (4.0 * 180.0 - 9.0 * 1000.0 * R0_HAND) / 9000.0   # 0.068880
ALPHA_WRONG_QUARTERLY_BASIS = (180.0 - 9.0 * 1000.0 * R0_HAND) / 9000.0  # 0.008880 — must NOT be produced


def _scenario(make_income_scenario):
    return make_income_scenario(t3m={0: 0.0300, **flat(0.0400)})


def _sibling_paths():
    return {
        "ii_loans": flat(10.0),
        "ii_dep_banks_other": flat(5.0),
        "ii_ust": flat(6.0),
        "ii_mbs": flat(4.0),
        "ii_other_sec": flat(3.0),
        "ii_other_ida": flat(2.0),
    }


def test_published_beta_used_unchanged(make_income_scenario):
    assert TABLE_A9_TRADING == TradingNiiParams(beta_treasury3m=0.278)
    rates = pre_alpha_rate_path(_scenario(make_income_scenario))
    assert all(rates[q] == pytest.approx(R0_HAND) for q in PROJECTION_QUARTERS)


def test_net_trading_assets_and_flat_path():
    assert INPUTS.net_trading_assets == pytest.approx(1000.0)
    path = net_trading_asset_path(INPUTS)
    assert all(path[q] == pytest.approx(1000.0) for q in PROJECTION_QUARTERS)


def test_nonpositive_net_trading_assets_fail_at_the_boundary():
    with pytest.raises(ValidationFailure, match="must be > 0"):
        TradingNiiInputs("FIRM_A", trading_assets_avg_balance=500.0, trading_liabilities_avg_balance=500.0)
    with pytest.raises(ValidationFailure, match="negative net trading book"):
        TradingNiiInputs("FIRM_A", trading_assets_avg_balance=400.0, trading_liabilities_avg_balance=500.0)


def test_implied_quarterly_residuals():
    implied = implied_trading_path(flat(50.0), _sibling_paths())
    assert all(implied[q] == pytest.approx(50.0 - 30.0) for q in PROJECTION_QUARTERS)


def test_sibling_key_set_enforced():
    paths = _sibling_paths()
    del paths["ii_mbs"]
    with pytest.raises(ValidationFailure, match=r"missing \['ii_mbs'\]"):
        implied_trading_path(flat(50.0), paths)
    paths = {**_sibling_paths(), "ie_other_borrowing": flat(1.0)}
    with pytest.raises(ValidationFailure, match=r"unexpected \['ie_other_borrowing'\]"):
        implied_trading_path(flat(50.0), paths)


def test_units_mismatch_guard_trips_in_both_directions():
    # Siblings sum to 30/quarter (270 cumulative). FRB income 1000× too big:
    with pytest.raises(ValidationFailure, match="money-unit mismatch"):
        implied_trading_path(flat(50000.0), _sibling_paths())
    # FRB income 1000× too small — billions against millions, the direction the
    # |alpha_b| magnitude warning can miss:
    with pytest.raises(ValidationFailure, match="money-unit mismatch"):
        implied_trading_path(flat(0.05), _sibling_paths())


def test_closed_form_alpha_exact_cumulative_match_with_the_x4(make_income_scenario):
    cal = calibrate_alpha_b(
        flat(20.0), net_trading_asset_path(INPUTS), pre_alpha_rate_path(_scenario(make_income_scenario))
    )
    assert cal.alpha_b == pytest.approx(ALPHA_HAND, rel=1e-12)
    assert cal.alpha_b != pytest.approx(ALPHA_WRONG_QUARTERLY_BASIS, rel=1e-3)  # the ×4 basis pin
    assert cal.cumulative_implied == pytest.approx(180.0)
    assert cal.cumulative_modeled == pytest.approx(180.0, abs=1e-9)
    assert abs(cal.cumulative_difference) <= 1e-9
    assert all(cal.modeled_path[q] == pytest.approx(20.0) for q in PROJECTION_QUARTERS)


def test_alpha_constant_across_all_nine_quarters(make_income_scenario):
    result, cal = run_trading_nii(INPUTS, _scenario(make_income_scenario), flat(50.0), _sibling_paths())
    alphas = {row.diagnostics.alpha_b for row in result.quarters}
    assert alphas == {cal.alpha_b}
    assert all(row.annualized_rate == pytest.approx(0.08) for row in result.quarters)
    assert all(row.quarterly_income == pytest.approx(20.0) for row in result.quarters)


def test_quarterly_paths_differ_but_cumulative_matches(make_income_scenario):
    implied = {**flat(20.0), 1: 10.0, 2: 30.0}  # same 180 total, uneven quarters
    cal = calibrate_alpha_b(
        implied, net_trading_asset_path(INPUTS), pre_alpha_rate_path(_scenario(make_income_scenario))
    )
    assert cal.alpha_b == pytest.approx(ALPHA_HAND, rel=1e-12)          # cumulative target unchanged
    assert cal.modeled_path[1] == pytest.approx(20.0)                    # NOT forced to the quarterly residual
    assert cal.modeled_path[1] != pytest.approx(cal.implied_path[1])
    assert cal.quarterly_difference_path[1] == pytest.approx(10.0)
    assert cal.quarterly_difference_path[2] == pytest.approx(-10.0)
    assert sum(cal.quarterly_difference_path.values()) == pytest.approx(0.0, abs=1e-9)


def test_zero_cumulative_balance_fails(make_income_scenario):
    zero_balances = {q: 0.0 for q in PROJECTION_QUARTERS}
    with pytest.raises(ValidationFailure, match="zero or invalid"):
        calibrate_alpha_b(flat(20.0), zero_balances, pre_alpha_rate_path(_scenario(make_income_scenario)))


def test_pq0_scenario_values_never_used(make_income_scenario):
    scenario_a = make_income_scenario(t3m={0: 0.0300, **flat(0.0400)})
    scenario_b = make_income_scenario(t3m={0: 0.0010, **flat(0.0400)})  # only PQ0 differs
    result_a, _ = run_trading_nii(INPUTS, scenario_a, flat(50.0), _sibling_paths())
    result_b, _ = run_trading_nii(INPUTS, scenario_b, flat(50.0), _sibling_paths())
    assert result_a == result_b


def test_negative_implied_quarters_logged_never_clamped(make_income_scenario):
    implied = implied_trading_path(flat(20.0), _sibling_paths())  # 20 − 30 = −10
    cal = calibrate_alpha_b(
        implied, net_trading_asset_path(INPUTS), pre_alpha_rate_path(_scenario(make_income_scenario))
    )
    assert all(cal.implied_path[q] == pytest.approx(-10.0) for q in PROJECTION_QUARTERS)
    assert any("negative implied" in w for w in cal.warnings)


def test_negative_modeled_net_income_logged_never_clamped(make_income_scenario):
    # Implied −10/quarter drags alpha negative enough that the modeled NET item
    # goes negative — legal for a net quantity; logged, never clamped or floored.
    result, cal = run_trading_nii(INPUTS, _scenario(make_income_scenario), flat(20.0), _sibling_paths())
    assert all(row.quarterly_income == pytest.approx(-10.0) for row in result.quarters)
    assert any("negative modeled trading NII" in w for w in result.warnings)
    assert result.validation_status == "passed_with_warnings"


def test_calibration_must_match_scenario(make_income_scenario):
    cal = calibrate_alpha_b(
        flat(20.0), net_trading_asset_path(INPUTS), pre_alpha_rate_path(_scenario(make_income_scenario))
    )
    other_scenario = make_income_scenario(t3m={0: 0.0300, **flat(0.0100)})
    with pytest.raises(ValidationFailure, match="pre-alpha rate mismatch"):
        project_trading_nii(INPUTS, other_scenario, cal)


def test_calibration_must_match_net_balance(make_income_scenario):
    half_net = {q: 500.0 for q in PROJECTION_QUARTERS}
    cal = calibrate_alpha_b(flat(20.0), half_net, pre_alpha_rate_path(_scenario(make_income_scenario)))
    with pytest.raises(ValidationFailure, match="modeled income mismatch"):
        project_trading_nii(INPUTS, _scenario(make_income_scenario), cal)

"""Income-family orchestration: execution order, results-level composition, the
exact-by-construction reconciliation (PID-TRD-1), reporting, and the calculator
fold-in helper. Uses the round test_nii_trading_al fixture: siblings 30/quarter,
FRB income 50/quarter → trading NII exactly 20/quarter and the family total
equals the FRB path in every quarter."""

from __future__ import annotations

import pytest

from scb_ppnr.interest_income import (
    INCOME_MODEL_EXECUTION_ORDER,
    SIBLING_MODEL_IDS,
    IncomeQuarterResult,
    IncomeModelResult,
    TradingNiiInputs,
    ValidationFailure,
    income_family_report,
    run_interest_income_family,
    sibling_paths_from_results,
)
from scb_ppnr.interest_income.schemas import PROJECTION_QUARTERS
from conftest import flat

TRADING = TradingNiiInputs("FIRM_A", trading_assets_avg_balance=1500.0, trading_liabilities_avg_balance=500.0)


def _sibling_paths():
    return {
        "ii_loans": flat(10.0),
        "ii_dep_banks_other": flat(5.0),
        "ii_ust": flat(6.0),
        "ii_mbs": flat(4.0),
        "ii_other_sec": flat(3.0),
        "ii_other_ida": flat(2.0),
    }


def _income_stub(model_id: str, firm_id="FIRM_A", scenario_id="sev_adverse", incomes=None) -> IncomeModelResult:
    if incomes is None:
        incomes = flat(5.0)
    rows = tuple(
        IncomeQuarterResult(q, annualized_rate=None, average_balance=None,
                            quarterly_income=incomes[q], diagnostics=None)
        for q in PROJECTION_QUARTERS
    )
    return IncomeModelResult(model_id, firm_id, scenario_id, rows, "passed", ())


def test_execution_order_contract():
    # The six Fed-independent income models first, the PID-TRD-1 consumer last.
    assert INCOME_MODEL_EXECUTION_ORDER == (*SIBLING_MODEL_IDS, "nii_trading_al")
    assert INCOME_MODEL_EXECUTION_ORDER == (
        "ii_loans", "ii_dep_banks_other", "ii_ust", "ii_mbs", "ii_other_sec", "ii_other_ida",
        "nii_trading_al",
    )


def test_family_run_reconciles_exactly(make_income_scenario):
    result = run_interest_income_family(
        firm_id="FIRM_A",
        scenario=make_income_scenario(t3m={0: 0.0300, **flat(0.0400)}),
        sibling_income_paths=_sibling_paths(),
        trading=TRADING,
        frb_total_interest_income=flat(50.0),
    )
    assert result.firm_id == "FIRM_A"
    assert set(result.sibling_paths) == set(SIBLING_MODEL_IDS)
    assert all(result.trading_result.income_path()[q] == pytest.approx(20.0) for q in PROJECTION_QUARTERS)
    reconciliation = result.reconciliation
    assert reconciliation.frb_total_cumulative == pytest.approx(450.0)
    assert reconciliation.components_total_cumulative == pytest.approx(450.0)
    assert reconciliation.within_tolerance is True
    assert abs(reconciliation.cumulative_difference) <= reconciliation.tolerance
    assert set(reconciliation.components_cumulative) == set(INCOME_MODEL_EXECUTION_ORDER)
    # In this round fixture the modeled trading path absorbs the residual exactly
    # per quarter too, so the per-quarter differences are all ~0.
    assert all(abs(d) <= 1e-9 for d in reconciliation.per_quarter_difference.values())
    total = result.total_income_path()
    assert all(total[q] == pytest.approx(50.0) for q in PROJECTION_QUARTERS)


def test_family_warnings_are_model_prefixed(make_income_scenario):
    result = run_interest_income_family(
        firm_id="FIRM_A",
        scenario=make_income_scenario(t3m={0: 0.0300, **flat(0.0400)}),
        sibling_income_paths=_sibling_paths(),
        trading=TRADING,
        frb_total_interest_income=flat(20.0),   # implied −10/quarter → warnings
    )
    assert result.warnings
    assert all(w.startswith("nii_trading_al: ") for w in result.warnings)


def test_firm_mismatch_fails(make_income_scenario):
    with pytest.raises(ValidationFailure, match="does not match family firm_id"):
        run_interest_income_family(
            firm_id="FIRM_B",
            scenario=make_income_scenario(t3m={0: 0.0300, **flat(0.0400)}),
            sibling_income_paths=_sibling_paths(),
            trading=TRADING,
            frb_total_interest_income=flat(50.0),
        )


def test_report_carries_the_paste_compare_rows(make_income_scenario):
    result = run_interest_income_family(
        firm_id="FIRM_A",
        scenario=make_income_scenario(t3m={0: 0.0300, **flat(0.0400)}),
        sibling_income_paths=_sibling_paths(),
        trading=TRADING,
        frb_total_interest_income=flat(50.0),
    )
    report = income_family_report(result, flat(50.0))
    assert "alpha_b" in report
    assert "NII TATL" in report                  # the reference tab's modeled row label
    assert "Implied FRB results" in report       # the reference tab's implied row label
    assert "frb_income (target)" in report
    for model_id in INCOME_MODEL_EXECUTION_ORDER:
        assert model_id in report


def test_sibling_paths_from_results_enforces_identity():
    dep = _income_stub("ii_dep_banks_other")
    ida = _income_stub("ii_other_ida")
    paths = sibling_paths_from_results(
        firm_id="FIRM_A", scenario_id="sev_adverse",
        ii_dep_banks_other=dep, ii_other_ida=ida,
    )
    assert set(paths) == {"ii_dep_banks_other", "ii_other_ida"}
    assert paths["ii_dep_banks_other"][1] == pytest.approx(5.0)
    with pytest.raises(ValidationFailure, match="does not match expected"):
        sibling_paths_from_results(
            firm_id="FIRM_A", scenario_id="baseline", ii_dep_banks_other=dep,
        )
    with pytest.raises(ValidationFailure, match="carries model_id"):
        sibling_paths_from_results(
            firm_id="FIRM_A", scenario_id="sev_adverse", ii_ust=dep,
        )

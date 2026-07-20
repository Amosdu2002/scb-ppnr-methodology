"""Family integration: Section-F execution order on a fully synthetic firm/scenario,
ending with the nine-quarter cumulative reconciliation to the FRB total."""

from __future__ import annotations

import pytest

from scb_ppnr.interest_expense import (
    MODEL_EXECUTION_ORDER,
    FamilyInputs,
    ValidationFailure,
    run_interest_expense_family,
)
from scb_ppnr.interest_expense.schemas import PROJECTION_QUARTERS
from conftest import flat


def test_execution_order_contract():
    assert MODEL_EXECUTION_ORDER == (
        "ie_dom_time_dep",
        "ie_other_dom_dep",
        "ie_foreign_dep",
        "ie_fed_funds_repo",
        "ie_other_borrowing",
    )


def test_family_run_reconciles_to_frb_total(make_family, make_scenario):
    family = make_family(frb_total=flat(40.0))
    out = run_interest_expense_family(family, make_scenario())

    assert set(out.results) == set(MODEL_EXECUTION_ORDER)
    assert out.firm_id == "FIRM_A" and out.scenario_id == "sev_adverse"

    components_total = sum(r.cumulative_expense for r in out.results.values())
    assert components_total == pytest.approx(360.0, abs=1e-8)          # 9 × 40
    assert out.reconciliation.within_tolerance
    assert abs(out.reconciliation.cumulative_difference) <= out.reconciliation.tolerance
    assert sum(out.reconciliation.per_quarter_difference.values()) == pytest.approx(0.0, abs=1e-8)


def test_other_borrowing_consumes_completed_sibling_paths(make_family, make_scenario):
    out = run_interest_expense_family(make_family(frb_total=flat(40.0)), make_scenario())
    four_pq1 = sum(out.results[mid].expense_path()[1] for mid in MODEL_EXECUTION_ORDER[:4])
    assert out.calibration.implied_path[1] == pytest.approx(40.0 - four_pq1)
    assert out.calibration.balance_sum == pytest.approx(9000.0)
    ob = out.results["ie_other_borrowing"]
    assert ob.expense_path()[1] == pytest.approx(out.calibration.modeled_path[1])
    alphas = {row.diagnostics.alpha_b for row in ob.quarters}
    assert len(alphas) == 1


def test_deterministic_and_inputs_untouched(make_family, make_scenario):
    frb = flat(40.0)
    frb_snapshot = dict(frb)
    family = make_family(frb_total=frb)
    first = run_interest_expense_family(family, make_scenario())
    second = run_interest_expense_family(family, make_scenario())
    assert first == second
    assert frb == frb_snapshot


def test_family_firm_alignment_enforced(make_family):
    good = make_family()
    with pytest.raises(ValidationFailure, match="does not match family firm_id"):
        FamilyInputs(
            firm_id="FIRM_B",
            dom_time_dep=good.dom_time_dep,
            other_dom_dep=good.other_dom_dep,
            foreign_dep=good.foreign_dep,
            fed_funds_repo=good.fed_funds_repo,
            other_borrowing=good.other_borrowing,
            frb_total_interest_expense=flat(40.0),
        )


def test_missing_frb_quarter_fails(make_family):
    frb = flat(40.0)
    del frb[9]
    with pytest.raises(ValidationFailure, match="frb_total_interest_expense"):
        make_family(frb_total=frb)

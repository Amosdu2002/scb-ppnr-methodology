"""Shared operations: the single D-004 ÷4, nine-ordered-quarter result contract,
and firm/scenario run alignment."""

from __future__ import annotations

import pytest

from scb_ppnr.interest_expense import ModelResult, QuarterResult, ValidationFailure, quarterly_expense
from scb_ppnr.interest_expense.common import require_same_run, sum_path
from scb_ppnr.interest_expense.schemas import PROJECTION_QUARTERS
from conftest import flat


def test_quarterly_expense_is_balance_times_rate_over_four():
    assert quarterly_expense(1000.0, 0.04) == 10.0
    assert quarterly_expense(0.0, 0.04) == 0.0
    assert quarterly_expense(1000.0, -0.01) == -2.5


def _rows(quarters):
    return tuple(QuarterResult(q, 0.01, 1.0, 0.0025, None) for q in quarters)


def test_model_result_requires_exactly_nine_quarters():
    with pytest.raises(ValidationFailure, match="PQ1..PQ9"):
        ModelResult("m", "f", "s", _rows(range(1, 9)), "passed", ())


def test_model_result_requires_ordered_quarters():
    shuffled = (2, 1, 3, 4, 5, 6, 7, 8, 9)
    with pytest.raises(ValidationFailure, match="in order"):
        ModelResult("m", "f", "s", _rows(shuffled), "passed", ())


def test_require_same_run_rejects_mismatched_identity(stub_result):
    a = stub_result("ie_dom_time_dep", scenario_id="sev_adverse")
    b = stub_result("ie_fed_funds_repo", scenario_id="baseline")
    with pytest.raises(ValidationFailure, match="does not match expected"):
        require_same_run((a, b), firm_id="FIRM_A", scenario_id="sev_adverse")


def test_sum_path_covers_projection_quarters():
    assert sum_path(flat(2.0)) == pytest.approx(18.0)
    assert len(PROJECTION_QUARTERS) == 9

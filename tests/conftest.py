"""Synthetic, deterministic canonical fixtures. No confidential data — every value
is hand-picked for hand-calculability (see the model test modules)."""

from __future__ import annotations

import pytest

from scb_ppnr.interest_expense import (
    DepositSubcomponent,
    DomTimeDepInputs,
    FamilyInputs,
    FedFundsRepoInputs,
    ForeignDepInputs,
    ModelResult,
    OtherBorrowingInputs,
    OtherDomDepInputs,
    QuarterResult,
    ScenarioPaths,
)
from scb_ppnr.interest_expense.schemas import PROJECTION_QUARTERS


def flat(value: float, quarters: tuple[int, ...] = PROJECTION_QUARTERS) -> dict[int, float]:
    return {q: value for q in quarters}


@pytest.fixture
def flat_path():
    return flat


@pytest.fixture
def make_scenario():
    def _make(scenario_id: str = "sev_adverse", t3m=None, t1y=None, bbb=None) -> ScenarioPaths:
        if t3m is None:
            t3m = {0: 0.0300, 1: 0.0400, 2: 0.0350, 3: 0.0350, 4: 0.0300,
                   5: 0.0250, 6: 0.0250, 7: 0.0300, 8: 0.0350, 9: 0.0400}
        if t1y is None:
            t1y = flat(0.0400)
        if bbb is None:
            bbb = flat(0.0600)
        return ScenarioPaths(scenario_id, t3m, t1y, bbb)

    return _make


@pytest.fixture
def make_family():
    def _make(firm_id: str = "FIRM_A", frb_total=None, frb_income=None, frb_nii=None) -> FamilyInputs:
        if frb_total is None:
            frb_total = flat(40.0)
        return FamilyInputs(
            firm_id=firm_id,
            dom_time_dep=DomTimeDepInputs(firm_id, rate_launchpoint=0.0200, wal_months=12.0, balance=1000.0),
            other_dom_dep=OtherDomDepInputs(
                firm_id,
                subcomponents={
                    "mma": DepositSubcomponent(0.0100, 600.0, 0.0010),
                    "savings": DepositSubcomponent(0.0050, 300.0, 0.0010),
                    "transaction": DepositSubcomponent(0.0020, 100.0, 0.0010),
                },
                total_average_balance=1050.0,
            ),
            foreign_dep=ForeignDepInputs(
                firm_id,
                subcomponents={
                    "foreign_nontime": DepositSubcomponent(0.0080, 500.0, 0.0004),
                    "foreign_time": DepositSubcomponent(0.0120, 500.0, 0.0006),
                },
            ),
            fed_funds_repo=FedFundsRepoInputs(firm_id, fed_funds_purchased_balance=600.0, repo_sold_balance=400.0),
            other_borrowing=OtherBorrowingInputs(firm_id, total_balance=1000.0, cp_share=0.10, subdebt_share=0.20),
            frb_total_interest_expense=frb_total,
            frb_total_interest_income=frb_income,
            frb_net_interest_income=frb_nii,
        )

    return _make


@pytest.fixture
def stub_result():
    """Minimal ModelResult factory for feeding the Other Borrowing calibration with
    hand-known sibling expense paths."""

    def _stub(model_id: str, firm_id: str = "FIRM_A", scenario_id: str = "sev_adverse",
              expenses=None) -> ModelResult:
        if expenses is None:
            expenses = flat(5.0)
        rows = tuple(
            QuarterResult(q, annualized_rate=0.02, average_balance=1000.0,
                          quarterly_expense=expenses[q], diagnostics=None)
            for q in PROJECTION_QUARTERS
        )
        return ModelResult(model_id, firm_id, scenario_id, rows, "passed", ())

    return _stub

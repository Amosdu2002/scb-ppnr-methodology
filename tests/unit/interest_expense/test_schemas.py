"""Canonical-boundary contracts: exact nine-quarter horizon, decimal-rate guard,
share/balance validation, immutability, firm/scenario alignment."""

from __future__ import annotations

import dataclasses

import pytest

from scb_ppnr.interest_expense import (
    DepositSubcomponent,
    DomTimeDepInputs,
    ForeignDepInputs,
    OtherBorrowingInputs,
    OtherDomDepInputs,
    ScenarioPaths,
    ValidationFailure,
    project_dom_time_dep,
)
from scb_ppnr.interest_expense.schemas import PROJECTION_QUARTERS
from conftest import flat


def test_scenario_missing_projection_quarter_fails():
    t1y = flat(0.04)
    del t1y[5]
    with pytest.raises(ValidationFailure, match=r"usd_1y_treasury.*missing \[5\]"):
        ScenarioPaths("s", {0: 0.03, **flat(0.04)}, t1y, flat(0.06))


def test_scenario_requires_pq0_for_treasury3m():
    with pytest.raises(ValidationFailure, match=r"usd_3m_treasury.*missing \[0\]"):
        ScenarioPaths("s", flat(0.04), flat(0.04), flat(0.06))


def test_extra_quarter_rejected():
    bbb = flat(0.06)
    bbb[10] = 0.06
    with pytest.raises(ValidationFailure, match=r"unexpected \[10\]"):
        ScenarioPaths("s", {0: 0.03, **flat(0.04)}, flat(0.04), bbb)


def test_percent_scale_rate_rejected():
    with pytest.raises(ValidationFailure, match="percent"):
        ScenarioPaths("s", {0: 0.03, **flat(0.04)}, flat(4.25), flat(0.06))
    with pytest.raises(ValidationFailure, match="percent"):
        DomTimeDepInputs("f", rate_launchpoint=2.0, wal_months=12.0, balance=1000.0)


def test_non_finite_rate_rejected():
    with pytest.raises(ValidationFailure, match="finite"):
        ScenarioPaths("s", {0: 0.03, **flat(0.04)}, {**flat(0.04), 5: float("nan")}, flat(0.06))


def test_share_bounds_and_sum():
    with pytest.raises(ValidationFailure, match=r"\[0, 1\]"):
        OtherBorrowingInputs("f", 1000.0, cp_share=1.2, subdebt_share=0.1)
    with pytest.raises(ValidationFailure, match="exceeds 1"):
        OtherBorrowingInputs("f", 1000.0, cp_share=0.6, subdebt_share=0.5)


def test_other_borrowing_balance_must_be_positive():
    for bad in (0.0, -5.0):
        with pytest.raises(ValidationFailure, match="> 0"):
            OtherBorrowingInputs("f", bad, cp_share=0.1, subdebt_share=0.2)


def test_negative_balance_rejected():
    with pytest.raises(ValidationFailure, match=">= 0"):
        DepositSubcomponent(0.01, -1.0, 0.001)


def test_wrong_subcomponent_keys_fail():
    subs = {"mma": DepositSubcomponent(0.01, 1.0, 0.001), "savings": DepositSubcomponent(0.01, 1.0, 0.001)}
    with pytest.raises(ValidationFailure, match="exactly subcomponents"):
        OtherDomDepInputs("f", subs, total_average_balance=1.0)
    with pytest.raises(ValidationFailure, match="exactly subcomponents"):
        ForeignDepInputs("f", {"mma": DepositSubcomponent(0.01, 1.0, 0.001)})


def test_inputs_are_frozen_and_sources_never_mutated(make_scenario):
    t3m = {0: 0.0300, **flat(0.0400)}
    t3m_snapshot = dict(t3m)
    scenario = ScenarioPaths("s", t3m, flat(0.0400), flat(0.0600))

    with pytest.raises(TypeError):
        scenario.usd_3m_treasury[1] = 0.4  # type: ignore[index]
    with pytest.raises(dataclasses.FrozenInstanceError):
        scenario.scenario_id = "other"  # type: ignore[misc]

    inputs = DomTimeDepInputs("f", 0.02, 12.0, 1000.0)
    project_dom_time_dep(inputs, scenario)
    assert t3m == t3m_snapshot  # the caller's dict was copied, never aliased or mutated


def test_other_borrowing_inputs_have_no_pq0_expense_field():
    field_names = {f.name for f in dataclasses.fields(OtherBorrowingInputs)}
    assert field_names == {"firm_id", "total_balance", "cp_share", "subdebt_share"}


def test_uniformly_negative_frb_expense_refused_at_canonical_boundary(make_family, flat_path):
    with pytest.raises(ValidationFailure, match="frb_expense_sign"):
        make_family(frb_total=flat_path(-40.0))

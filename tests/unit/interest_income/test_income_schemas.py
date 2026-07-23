"""Income-side canonical contracts: the four-series scenario container, the two
calculator input types, and the result invariants (sign-unconstrained income;
exactly PQ1..PQ9). All values hand-picked for hand-calculability."""

from __future__ import annotations

import dataclasses

import pytest

from scb_ppnr.interest_income import (
    DepBanksOtherInputs,
    IncomeFamilyInputs,
    IncomeModelResult,
    IncomeQuarterResult,
    IncomeScenarioPaths,
    OtherIdaInputs,
    ValidationFailure,
)
from scb_ppnr.interest_income.schemas import PROJECTION_QUARTERS
from conftest import flat


def _rows(income: float = 1.0) -> tuple[IncomeQuarterResult, ...]:
    return tuple(
        IncomeQuarterResult(q, annualized_rate=0.04, average_balance=100.0,
                            quarterly_income=income, diagnostics=None)
        for q in PROJECTION_QUARTERS
    )


def test_scenario_requires_pq0_on_3m_only(make_income_scenario):
    scenario = make_income_scenario()
    assert set(scenario.usd_3m_treasury) == {0, *PROJECTION_QUARTERS}
    assert set(scenario.usd_10y_treasury) == set(PROJECTION_QUARTERS)
    with pytest.raises(ValidationFailure, match="usd_3m_treasury.*missing \\[0\\]"):
        IncomeScenarioPaths("s", flat(0.04), flat(0.045), flat(0.07), flat(0.065))
    with pytest.raises(ValidationFailure, match="usd_10y_treasury.*unexpected \\[0\\]"):
        IncomeScenarioPaths("s", {0: 0.03, **flat(0.04)}, {0: 0.045, **flat(0.045)}, flat(0.07), flat(0.065))


def test_scenario_rejects_percent_scale_leakage():
    with pytest.raises(ValidationFailure, match="looks percent-scaled"):
        IncomeScenarioPaths("s", {0: 0.03, **flat(0.04)}, flat(4.5), flat(0.07), flat(0.065))


def test_input_validation():
    with pytest.raises(ValidationFailure, match="balance must be >= 0"):
        DepBanksOtherInputs("FIRM_A", balance=-1.0)
    with pytest.raises(ValidationFailure, match="short_rate_share must lie in \\[0, 1\\]"):
        OtherIdaInputs("FIRM_A", total_balance=100.0, short_rate_share=1.2)
    with pytest.raises(ValidationFailure, match="firm_id must be a non-empty string"):
        DepBanksOtherInputs("", balance=1.0)


def test_negative_quarterly_income_is_legal():
    # No sign constraint on income — trading NII is legitimately negative (schemas docstring).
    result = IncomeModelResult("m", "FIRM_A", "s", _rows(income=-2.5), "passed", ())
    assert result.cumulative_income == pytest.approx(-22.5)
    assert result.income_path()[1] == pytest.approx(-2.5)


def test_result_requires_exactly_pq1_to_pq9_in_order():
    with pytest.raises(ValidationFailure, match="must cover exactly PQ1..PQ9 in order"):
        IncomeModelResult("m", "FIRM_A", "s", _rows()[:8], "passed", ())
    with pytest.raises(ValidationFailure, match="must cover exactly PQ1..PQ9 in order"):
        IncomeModelResult("m", "FIRM_A", "s", tuple(reversed(_rows())), "passed", ())


def test_result_paths_and_immutability():
    result = IncomeModelResult("m", "FIRM_A", "s", _rows(), "passed", ())
    assert result.rate_path()[5] == pytest.approx(0.04)
    with pytest.raises(TypeError):
        result.income_path()[1] = 99.0  # type: ignore[index]
    with pytest.raises(dataclasses.FrozenInstanceError):
        result.model_id = "other"  # type: ignore[misc]


def test_family_bundle_checks_firm_alignment():
    dep = DepBanksOtherInputs("FIRM_A", balance=1000.0)
    ida = OtherIdaInputs("FIRM_B", total_balance=2000.0, short_rate_share=0.6)
    with pytest.raises(ValidationFailure, match="does not match family firm_id"):
        IncomeFamilyInputs("FIRM_A", dep_banks_other=dep, other_ida=ida)

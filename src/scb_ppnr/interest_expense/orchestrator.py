"""Interest-expense family orchestrator — the Section-F execution order.

Steps 1–4: the four structural/deposit models are mutually independent (no proposed
model consumes another's output in the Fed suite) and could run in any order or in
parallel. Steps 5–8 are the PID-OB-5 project-level sequence: the implied Other
Borrowing residual from the FRB total-interest-expense path, the closed-form α_b,
the final Other Borrowing path, and the nine-quarter cumulative reconciliation of
all five components to the FRB total. There is no circular dependency: Other
Borrowing consumes the four completed expense paths, never the reverse.

The hedge adjustment (Section v.c, Eqs A49–A51) is an external downstream interface —
every result here is a pre-hedge expense path (OQ-005).
"""

from __future__ import annotations

from types import MappingProxyType

from .common import reconciliation_tolerance, sum_path
from .ie_dom_time_dep import project_dom_time_dep
from .ie_fed_funds_repo import project_fed_funds_repo
from .ie_foreign_dep import project_foreign_dep
from .ie_other_borrowing import run_other_borrowing
from .ie_other_dom_dep import project_other_dom_dep
from .schemas import (
    PROJECTION_QUARTERS,
    TABLE_A7_FOREIGN,
    TABLE_A7_OTHER_DOM,
    TABLE_A9_OTHER_BORROWING,
    DepositBetaParams,
    FamilyInputs,
    FamilyReconciliation,
    FamilyResult,
    ModelResult,
    OtherBorrowingParams,
    ScenarioPaths,
    ValidationFailure,
)

MODEL_EXECUTION_ORDER: tuple[str, ...] = (
    "ie_dom_time_dep",
    "ie_other_dom_dep",
    "ie_foreign_dep",
    "ie_fed_funds_repo",
    "ie_other_borrowing",
)


def run_interest_expense_family(
    family: FamilyInputs,
    scenario: ScenarioPaths,
    *,
    other_dom_params: DepositBetaParams = TABLE_A7_OTHER_DOM,
    foreign_params: DepositBetaParams = TABLE_A7_FOREIGN,
    other_borrowing_params: OtherBorrowingParams = TABLE_A9_OTHER_BORROWING,
) -> FamilyResult:
    # Steps 1–4: independent models (order immaterial).
    dom_time = project_dom_time_dep(family.dom_time_dep, scenario)
    other_dom = project_other_dom_dep(family.other_dom_dep, scenario, other_dom_params)
    foreign = project_foreign_dep(family.foreign_dep, scenario, foreign_params)
    fed_funds = project_fed_funds_repo(family.fed_funds_repo, scenario)

    # Steps 5–7: implied residual → closed-form α_b → Other Borrowing path (PID-OB-5).
    other_borrowing, calibration = run_other_borrowing(
        family.other_borrowing,
        scenario,
        family.frb_total_interest_expense,
        dom_time,
        other_dom,
        foreign,
        fed_funds,
        other_borrowing_params,
    )

    results = {r.model_id: r for r in (dom_time, other_dom, foreign, fed_funds, other_borrowing)}

    # Step 8: nine-quarter cumulative reconciliation to the FRB total.
    reconciliation = _reconcile(family.frb_total_interest_expense, results)

    warnings = tuple(f"{model_id}: {w}" for model_id in MODEL_EXECUTION_ORDER for w in results[model_id].warnings)
    return FamilyResult(
        firm_id=family.firm_id,
        scenario_id=scenario.scenario_id,
        results=MappingProxyType(results),
        calibration=calibration,
        reconciliation=reconciliation,
        warnings=warnings,
    )


def _reconcile(frb_total, results: dict[str, ModelResult]) -> FamilyReconciliation:
    per_quarter_difference = MappingProxyType(
        {
            q: sum(r.expense_path()[q] for r in results.values()) - frb_total[q]
            for q in PROJECTION_QUARTERS
        }
    )
    components_cumulative = MappingProxyType(
        {model_id: results[model_id].cumulative_expense for model_id in MODEL_EXECUTION_ORDER}
    )
    components_total = sum(components_cumulative.values())
    frb_cumulative = sum_path(frb_total)
    difference = components_total - frb_cumulative
    tolerance = reconciliation_tolerance(frb_cumulative)
    if abs(difference) > tolerance:
        raise ValidationFailure(
            f"nine-quarter reconciliation failed: five-component cumulative {components_total} vs "
            f"FRB total {frb_cumulative} (difference {difference}, tolerance {tolerance}) — "
            f"exact by construction under PID-OB-5, so a violation indicates a coding error"
        )
    return FamilyReconciliation(
        frb_total_cumulative=frb_cumulative,
        components_cumulative=components_cumulative,
        components_total_cumulative=components_total,
        cumulative_difference=difference,
        per_quarter_difference=per_quarter_difference,
        tolerance=tolerance,
        within_tolerance=True,
    )

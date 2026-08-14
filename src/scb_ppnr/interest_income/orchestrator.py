"""Interest-income family orchestrator — the Increment 4 execution order.

The six sibling income models are mutually independent in the Fed suite (no
proposed model consumes another's output) and run FIRST; `nii_trading_al` runs
LAST, consuming their completed income paths plus the FRB total-interest-income
path — the PID-TRD-1 project-level sequence mirroring PID-OB-5 on the expense
side. There is no circular dependency: trading NII is a pure consumer.

Composition is at the RESULTS level: loans and securities run from their own
workbook loaders (multi-workbook inputs), so the caller supplies each sibling's
completed PQ1..PQ9 income path; the two Family A calculators can be folded in
via `sibling_paths_from_results`. Firm/scenario alignment of plain paths is the
caller's contract — enforced here for anything typed.

Reconciliation is EXACT BY CONSTRUCTION under PID-TRD-1 (gate decision
2026-08-13; supersedes the pre-gate monitor-mode note in
docs/architecture/interest-income-design.md): the seven-component nine-quarter
cumulative equals the FRB income total, and a breach raises — it indicates a
coding error, exactly as on the expense side. Per-quarter differences remain
diagnostics. The hedge adjustment (Section v.c) stays an external downstream
interface — every path here is pre-hedge income (OQ-005).
"""

from __future__ import annotations

from types import MappingProxyType
from typing import Mapping

from ..core.common import reconciliation_tolerance, sum_path
from ..core.schemas import PROJECTION_QUARTERS, ValidationFailure
from .nii_trading_al import SIBLING_MODEL_IDS, run_trading_nii
from .schemas import (
    TABLE_A9_TRADING,
    IncomeFamilyReconciliation,
    IncomeFamilyResult,
    IncomeScenarioPaths,
    TradingNiiInputs,
    TradingNiiParams,
)

INCOME_MODEL_EXECUTION_ORDER: tuple[str, ...] = (*SIBLING_MODEL_IDS, "nii_trading_al")


def run_interest_income_family(
    *,
    firm_id: str,
    scenario: IncomeScenarioPaths,
    sibling_income_paths: Mapping[str, Mapping[int, float]],
    trading: TradingNiiInputs,
    frb_total_interest_income: Mapping[int, float],
    trading_params: TradingNiiParams = TABLE_A9_TRADING,
) -> IncomeFamilyResult:
    if trading.firm_id != firm_id:
        raise ValidationFailure(
            f"trading.firm_id = {trading.firm_id!r} does not match family firm_id = {firm_id!r}"
        )

    # Execution-order tail (PID-TRD-1): implied residual → closed-form α_b → trading path.
    trading_result, calibration = run_trading_nii(
        trading, scenario, frb_total_interest_income, sibling_income_paths, trading_params
    )

    reconciliation = _reconcile(frb_total_interest_income, sibling_income_paths, trading_result)

    warnings = tuple(f"{trading_result.model_id}: {w}" for w in trading_result.warnings)
    return IncomeFamilyResult(
        firm_id=firm_id,
        scenario_id=scenario.scenario_id,
        sibling_paths=sibling_income_paths,
        trading_result=trading_result,
        calibration=calibration,
        reconciliation=reconciliation,
        warnings=warnings,
    )


def _reconcile(
    frb_total: Mapping[int, float],
    sibling_paths: Mapping[str, Mapping[int, float]],
    trading_result,
) -> IncomeFamilyReconciliation:
    trading_path = trading_result.income_path()
    per_quarter_difference = MappingProxyType(
        {
            q: sum(path[q] for path in sibling_paths.values()) + trading_path[q] - frb_total[q]
            for q in PROJECTION_QUARTERS
        }
    )
    components_cumulative = MappingProxyType(
        {
            **{model_id: sum_path(sibling_paths[model_id]) for model_id in SIBLING_MODEL_IDS},
            trading_result.model_id: trading_result.cumulative_income,
        }
    )
    components_total = sum(components_cumulative.values())
    frb_cumulative = sum_path(frb_total)
    difference = components_total - frb_cumulative
    tolerance = reconciliation_tolerance(frb_cumulative)
    if abs(difference) > tolerance:
        raise ValidationFailure(
            f"nine-quarter income reconciliation failed: seven-component cumulative {components_total} vs "
            f"FRB income total {frb_cumulative} (difference {difference}, tolerance {tolerance}) — "
            f"exact by construction under PID-TRD-1, so a violation indicates a coding error"
        )
    return IncomeFamilyReconciliation(
        frb_total_cumulative=frb_cumulative,
        components_cumulative=components_cumulative,
        components_total_cumulative=components_total,
        cumulative_difference=difference,
        per_quarter_difference=per_quarter_difference,
        tolerance=tolerance,
        within_tolerance=True,
    )

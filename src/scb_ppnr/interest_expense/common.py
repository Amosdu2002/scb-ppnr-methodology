"""Genuinely shared operations for the interest-expense family (conventions §8).

Only cross-model mechanics live here: the single D-004 annualized-rate →
quarterly-dollar conversion, projection-path helpers, result assembly, and
firm/scenario alignment checks. Each model's rate engine stays in its own module —
the five calculation forms are never harmonized."""

from __future__ import annotations

from types import MappingProxyType
from typing import Iterable, Mapping

from .schemas import (
    PROJECTION_QUARTERS,
    ModelResult,
    QuarterResult,
    ValidationFailure,
)

# Reconciliation identities are exact by construction; the tolerance only absorbs
# float arithmetic (relative to the magnitude being reconciled, floored at 1.0).
RECONCILIATION_TOLERANCE_REL: float = 1e-9


def quarterly_expense(average_balance: float, annualized_rate: float) -> float:
    """QuarterlyExpense = AverageBalance × AnnualizedRate / 4 — the single D-004 ÷4,
    applied only at this final conversion (simple nominal quarterization)."""
    return average_balance * annualized_rate / 4.0


def sum_path(path: Mapping[int, float]) -> float:
    return sum(path[q] for q in PROJECTION_QUARTERS)


def freeze_projection_path(name: str, values: Mapping[int, float]) -> Mapping[int, float]:
    """Read-only PQ1..PQ9 copy; raises if any projection quarter is missing."""
    try:
        return MappingProxyType({q: float(values[q]) for q in PROJECTION_QUARTERS})
    except KeyError as exc:
        raise ValidationFailure(f"{name} is missing projection quarter PQ{exc.args[0]}") from None


def reconciliation_tolerance(reference: float) -> float:
    return RECONCILIATION_TOLERANCE_REL * max(1.0, abs(reference))


def build_result(
    model_id: str,
    firm_id: str,
    scenario_id: str,
    rows: Iterable[QuarterResult],
    warnings: Iterable[str],
) -> ModelResult:
    warning_tuple = tuple(warnings)
    status = "passed" if not warning_tuple else "passed_with_warnings"
    return ModelResult(model_id, firm_id, scenario_id, tuple(rows), status, warning_tuple)


def require_same_run(results: Iterable[ModelResult], *, firm_id: str, scenario_id: str) -> None:
    """Balances, rates, and expenses must align on firm, scenario, and quarter;
    mixing runs is a hard failure, never silently reconciled."""
    for result in results:
        if result.firm_id != firm_id or result.scenario_id != scenario_id:
            raise ValidationFailure(
                f"{result.model_id}: result identity ({result.firm_id!r}, {result.scenario_id!r}) "
                f"does not match expected ({firm_id!r}, {scenario_id!r})"
            )

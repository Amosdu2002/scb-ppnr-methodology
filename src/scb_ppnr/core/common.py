"""Side-neutral shared mechanics: the single D-004 annualized-rate →
quarterly-dollar conversion, projection-path helpers, generic result assembly,
and firm/scenario run-alignment checks. Moved verbatim from the verified
interest-expense common module at the core extraction (2026-07-23). Family
engines never live here — each model's calculation form stays in its own
family package, unharmonized."""

from __future__ import annotations

from types import MappingProxyType
from typing import Any, Iterable, Mapping, Protocol

from .schemas import PROJECTION_QUARTERS, ValidationFailure

# Reconciliation identities are exact by construction; the tolerance only absorbs
# float arithmetic (relative to the magnitude being reconciled, floored at 1.0).
RECONCILIATION_TOLERANCE_REL: float = 1e-9


def quarterly_flow(average_balance: float, annualized_rate: float) -> float:
    """QuarterlyFlow = AverageBalance × AnnualizedRate / 4 — the single D-004 ÷4,
    applied only at this final conversion (simple nominal quarterization). Each
    family re-exports it under its own name (quarterly_expense, quarterly_income)."""
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


class RunIdentified(Protocol):
    """Anything carrying a run identity — both families' result types satisfy it."""

    model_id: str
    firm_id: str
    scenario_id: str


def build_result(
    result_cls: type,
    model_id: str,
    firm_id: str,
    scenario_id: str,
    rows: Iterable[Any],
    warnings: Iterable[str],
):
    """Shared result assembly with the "passed"/"passed_with_warnings" derivation.

    `result_cls` must accept the six-field positional order
    (model_id, firm_id, scenario_id, quarters, validation_status, warnings) —
    the documented contract both families' result classes satisfy."""
    warning_tuple = tuple(warnings)
    status = "passed" if not warning_tuple else "passed_with_warnings"
    return result_cls(model_id, firm_id, scenario_id, tuple(rows), status, warning_tuple)


def require_same_run(results: Iterable[RunIdentified], *, firm_id: str, scenario_id: str) -> None:
    """Balances, rates, and flows must align on firm, scenario, and quarter;
    mixing runs is a hard failure, never silently reconciled."""
    for result in results:
        if result.firm_id != firm_id or result.scenario_id != scenario_id:
            raise ValidationFailure(
                f"{result.model_id}: result identity ({result.firm_id!r}, {result.scenario_id!r}) "
                f"does not match expected ({firm_id!r}, {scenario_id!r})"
            )

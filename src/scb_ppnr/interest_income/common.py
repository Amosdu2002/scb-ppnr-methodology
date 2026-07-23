"""Genuinely shared operations for the interest-income family.

Thin family-side bindings of the side-neutral core mechanics: the single D-004
÷4 under its income-side name, and result assembly bound to IncomeModelResult.
Each model's calculation stays in its own module — the calculator, securities,
loans, and trading-NII forms are never harmonized (asset conventions §1/§11)."""

from __future__ import annotations

from typing import Iterable

from ..core.common import build_result as _build_result, quarterly_flow
from .schemas import IncomeModelResult, IncomeQuarterResult

# The single D-004 ÷4 under its income-side name — the same function object.
quarterly_income = quarterly_flow


def build_income_result(
    model_id: str,
    firm_id: str,
    scenario_id: str,
    rows: Iterable[IncomeQuarterResult],
    warnings: Iterable[str],
) -> IncomeModelResult:
    return _build_result(IncomeModelResult, model_id, firm_id, scenario_id, rows, warnings)

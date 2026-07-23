"""Genuinely shared operations for the interest-expense family (conventions §8).

The side-neutral mechanics (the single D-004 ÷4, projection-path helpers, generic
result assembly, run-alignment checks) moved verbatim to `scb_ppnr.core.common`
at the core extraction (2026-07-23); this module re-exports them under their
established expense-side names — same objects, same behavior. Each model's rate
engine stays in its own module — the five calculation forms are never harmonized."""

from __future__ import annotations

from typing import Iterable

from ..core.common import (
    RECONCILIATION_TOLERANCE_REL,
    build_result as _build_result,
    freeze_projection_path,
    quarterly_flow,
    reconciliation_tolerance,
    require_same_run,
    sum_path,
)
from .schemas import ModelResult, QuarterResult

# The single D-004 ÷4 under its expense-side name — the same function object.
quarterly_expense = quarterly_flow


def build_result(
    model_id: str,
    firm_id: str,
    scenario_id: str,
    rows: Iterable[QuarterResult],
    warnings: Iterable[str],
) -> ModelResult:
    return _build_result(ModelResult, model_id, firm_id, scenario_id, rows, warnings)

"""Plain-text run report for an income-family result. Returns a string so callers
decide where it goes (stdout, a log, a file). Mirrors the expense-side report:
USD MILLIONS, pre-hedge labels; the calibration block prints the implied and
modeled rows plus their differences — the same three rows the reference trading
tab carries, so a paste-compare lines up row for row."""

from __future__ import annotations

from typing import Mapping

from ..core.common import format_path_header, format_path_row
from .orchestrator import INCOME_MODEL_EXECUTION_ORDER
from .schemas import PROJECTION_QUARTERS, IncomeFamilyResult


def income_family_report(result: IncomeFamilyResult, frb_total_interest_income: Mapping[int, float]) -> str:
    lines = [f"firm={result.firm_id}  scenario={result.scenario_id}", ""]
    lines.append("Quarterly income paths (USD MILLIONS per quarter — canonical unit, D-006; pre-hedge):")
    lines.append(format_path_header("model"))
    trading_path = result.trading_result.income_path()
    for model_id in INCOME_MODEL_EXECUTION_ORDER:
        path = trading_path if model_id == result.trading_result.model_id else result.sibling_paths[model_id]
        lines.append(format_path_row(model_id, path))
    lines.append(format_path_row("frb_income (target)", frb_total_interest_income))

    calibration = result.calibration
    lines += [
        "",
        "Trading NII calibration (PID-TRD-1, annualized basis PID-TRD-3):",
        f"  alpha_b                    = {calibration.alpha_b:.6f} (annualized decimal, constant PQ1..PQ9)",
        f"  nine-quarter implied total = {calibration.cumulative_implied:.6f}",
        f"  nine-quarter modeled total = {calibration.cumulative_modeled:.6f}",
        f"  cumulative difference      = {calibration.cumulative_difference:.3e}",
        "  modeled trading NII (the reference tab's 'NII TATL' row):",
        "    " + "  ".join(f"PQ{q}:{calibration.modeled_path[q]:.3f}" for q in PROJECTION_QUARTERS),
        "  implied trading NII (the reference tab's 'Implied FRB results' row):",
        "    " + "  ".join(f"PQ{q}:{calibration.implied_path[q]:.3f}" for q in PROJECTION_QUARTERS),
        "  quarterly modeled-vs-implied differences (diagnostic, need not be zero; sum ~ 0):",
        "    " + "  ".join(f"PQ{q}:{calibration.quarterly_difference_path[q]:+.3f}" for q in PROJECTION_QUARTERS),
    ]

    reconciliation = result.reconciliation
    lines += [
        "",
        f"Family reconciliation: seven-component total {reconciliation.components_total_cumulative:.6f} "
        f"vs FRB income total {reconciliation.frb_total_cumulative:.6f} "
        f"(difference {reconciliation.cumulative_difference:.3e}, within tolerance: {reconciliation.within_tolerance})",
    ]
    if result.warnings:
        lines.append("")
        lines.append("Logged events (log, never clamp):")
        lines += [f"  - {warning}" for warning in result.warnings]
    else:
        lines += ["", "No logged edge events."]
    return "\n".join(lines)

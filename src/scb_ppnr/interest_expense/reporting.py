"""Plain-text run report for a family result. Returns a string so callers decide
where it goes (stdout, a log, a file)."""

from __future__ import annotations

from typing import Mapping

from .orchestrator import MODEL_EXECUTION_ORDER
from .schemas import PROJECTION_QUARTERS, FamilyResult


def family_report(result: FamilyResult, frb_total: Mapping[int, float]) -> str:
    lines = [f"firm={result.firm_id}  scenario={result.scenario_id}", ""]
    lines.append("Quarterly expense paths (USD per quarter, pre-hedge):")
    lines.append(
        "model".ljust(22) + "".join(f"PQ{q}".rjust(9) for q in PROJECTION_QUARTERS) + "     total".rjust(11)
    )
    for model_id in MODEL_EXECUTION_ORDER:
        model_result = result.results[model_id]
        path = model_result.expense_path()
        lines.append(
            model_id.ljust(22)
            + "".join(f"{path[q]:9.3f}" for q in PROJECTION_QUARTERS)
            + f"{model_result.cumulative_expense:11.3f}"
        )
    lines.append(
        "frb_total (target)".ljust(22)
        + "".join(f"{frb_total[q]:9.3f}" for q in PROJECTION_QUARTERS)
        + f"{sum(frb_total[q] for q in PROJECTION_QUARTERS):11.3f}"
    )

    calibration = result.calibration
    lines += [
        "",
        "Other Borrowing calibration (PID-OB-5):",
        f"  alpha_b                    = {calibration.alpha_b:.6f} (annualized decimal, constant PQ1..PQ9)",
        f"  nine-quarter implied total = {calibration.cumulative_implied:.6f}",
        f"  nine-quarter modeled total = {calibration.cumulative_modeled:.6f}",
        f"  cumulative difference      = {calibration.cumulative_difference:.3e}",
        "  quarterly modeled-vs-implied differences (diagnostic, need not be zero):",
        "    " + "  ".join(f"PQ{q}:{calibration.quarterly_difference_path[q]:+.3f}" for q in PROJECTION_QUARTERS),
    ]

    reconciliation = result.reconciliation
    lines += [
        "",
        f"Family reconciliation: five-component total {reconciliation.components_total_cumulative:.6f} "
        f"vs FRB total {reconciliation.frb_total_cumulative:.6f} "
        f"(difference {reconciliation.cumulative_difference:.3e}, within tolerance: {reconciliation.within_tolerance})",
    ]
    if result.warnings:
        lines.append("")
        lines.append("Logged events (log, never clamp):")
        lines += [f"  - {warning}" for warning in result.warnings]
    else:
        lines += ["", "No logged edge events."]
    return "\n".join(lines)

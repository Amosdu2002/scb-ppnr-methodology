"""Combined-NII monitor — the side-neutral roll-up of the two family totals.

    NII(q) = TotalInterestIncome(q) − TotalInterestExpense(q)

Compares the modeled NII path against the FRB-provided `frb_net_interest_income`
path when supplied. REPORTS, NEVER FORCES (conventions §10): with both sides
calibrated exact-by-construction to their FRB paths (PID-OB-5 expense,
PID-TRD-1 income), the CUMULATIVE gap closes whenever the three hardcoded FRB
paths satisfy their own income − expense = NII identity — so this monitor is
primarily a wiring/units tripwire across the two families, and its verdict is
judged on the nine-quarter cumulative gap against the same 1% guard the
input-side identity check uses (FRB_IDENTITY_GUARD_REL). Per-quarter gaps are
carried as pure diagnostics WITHOUT a verdict: both calibrations match
cumulatives only, so quarterly modeled-vs-FRB divergence is structural, not a
defect. A cumulative breach lands in `notes`; values are never adjusted and
nothing raises except structural path defects.

The Fed source states no total-NII aggregation for the proposed suite (Section v
models each component independently — FACT absence); this roll-up is project
tooling, never Fed methodology.
"""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping

from .core.common import format_path_header, format_path_row, freeze_projection_path, sum_path
from .core.schemas import PROJECTION_QUARTERS
from .interest_expense.schemas import FRB_IDENTITY_GUARD_REL


@dataclass(frozen=True)
class CombinedNiiReport:
    """Modeled income/expense/NII paths, their cumulatives, and — when the FRB
    NII path is supplied — per-quarter and cumulative gaps plus the 1%-guard
    verdict. `within_identity_guard` is None when no FRB path was supplied."""

    income_path: Mapping[int, float]
    expense_path: Mapping[int, float]
    nii_path: Mapping[int, float]
    cumulative_income: float
    cumulative_expense: float
    cumulative_nii: float
    frb_net_interest_income: Mapping[int, float] | None
    per_quarter_gap: Mapping[int, float] | None      # modeled NII − FRB NII (diagnostic only —
                                                     # quarterly divergence is structural under
                                                     # cumulative-only calibration)
    cumulative_gap: float | None
    within_identity_guard: bool | None               # verdict on the CUMULATIVE gap
    notes: tuple[str, ...]


def combined_nii_monitor(
    total_income_path: Mapping[int, float],
    total_expense_path: Mapping[int, float],
    *,
    frb_net_interest_income: Mapping[int, float] | None = None,
) -> CombinedNiiReport:
    """Both totals in canonical positive-magnitude convention (D-008: expense
    positive; NII = income − expense), USD millions per quarter, PQ1..PQ9."""
    income = freeze_projection_path("total_income_path", total_income_path)
    expense = freeze_projection_path("total_expense_path", total_expense_path)
    nii = MappingProxyType({q: income[q] - expense[q] for q in PROJECTION_QUARTERS})

    notes: list[str] = []
    frb_nii = None
    per_quarter_gap = None
    cumulative_gap = None
    within = None
    if frb_net_interest_income is not None:
        frb_nii = freeze_projection_path("frb_net_interest_income", frb_net_interest_income)
        per_quarter_gap = MappingProxyType({q: nii[q] - frb_nii[q] for q in PROJECTION_QUARTERS})
        cumulative_gap = sum_path(nii) - sum_path(frb_nii)
        guard = FRB_IDENTITY_GUARD_REL * max(
            1.0, abs(sum_path(income)), abs(sum_path(expense))
        )
        within = abs(cumulative_gap) <= guard
        if not within:
            notes.append(
                f"cumulative modeled NII {sum_path(nii)} vs cumulative FRB NII "
                f"{sum_path(frb_nii)} (gap {cumulative_gap}, guard {guard}) — with both "
                f"families calibrated to their FRB paths this should close; likely a wiring, "
                f"units, or path-scope issue across the two families; reported, never forced"
            )

    return CombinedNiiReport(
        income_path=income,
        expense_path=expense,
        nii_path=nii,
        cumulative_income=sum_path(income),
        cumulative_expense=sum_path(expense),
        cumulative_nii=sum_path(nii),
        frb_net_interest_income=frb_nii,
        per_quarter_gap=per_quarter_gap,
        cumulative_gap=cumulative_gap,
        within_identity_guard=within,
        notes=tuple(notes),
    )


def combined_nii_report_text(report: CombinedNiiReport) -> str:
    lines = ["Combined NII (USD MILLIONS per quarter; income − expense, D-008 convention; pre-hedge):"]
    lines.append(format_path_header("series"))
    rows = [
        ("total_income", report.income_path, report.cumulative_income),
        ("total_expense", report.expense_path, report.cumulative_expense),
        ("modeled_nii", report.nii_path, report.cumulative_nii),
    ]
    if report.frb_net_interest_income is not None:
        rows.append(
            ("frb_nii (target)", report.frb_net_interest_income, sum_path(report.frb_net_interest_income))
        )
        rows.append(("gap (modeled-frb)", report.per_quarter_gap, report.cumulative_gap))
    for label, path, total in rows:
        lines.append(format_path_row(label, path, total))
    if report.within_identity_guard is not None:
        lines.append(
            f"Cumulative gap within the {FRB_IDENTITY_GUARD_REL:.0%} identity guard: "
            f"{report.within_identity_guard} (per-quarter gaps are diagnostics — quarterly "
            f"divergence is structural under cumulative-only calibration; reported, never forced)"
        )
    if report.notes:
        lines.append("Notes:")
        lines += [f"  - {note}" for note in report.notes]
    return "\n".join(lines)

"""ii_other_ida — Interest Income on Other Interest/Dividend-Bearing Assets
(Eq A43, B.v.a(6)).

Two-rate blend calculator: the fed-funds-sold/reverse-repo share α earns the
contemporaneous 3-month Treasury yield; the remaining (1 − α) share earns the
contemporaneous 10-year Treasury yield. Balance (Schedule G G.2 line item 15,
source-stated) and share α (supplied input, OQ-024) are both held flat at the
launch point (Fed-stated). Footnote 66's "lesser of six percent and the 10-year
Treasury yield" is rationale for the 10Y choice, not model mechanics — no cap
term appears in Eq A43 and none is implemented (chapter §5 [CODE]).

    other_ida_interest_income(b,q)
        = item15_balance × [α·Treasury3m(q) + (1 − α)·Treasury10y(q)] / 4   (D-004)
"""

from __future__ import annotations

from ..core.schemas import PROJECTION_QUARTERS
from .common import build_income_result, quarterly_income
from .schemas import (
    IncomeModelResult,
    IncomeQuarterResult,
    IncomeScenarioPaths,
    OtherIdaInputs,
    OtherIdaQuarterDiagnostics,
)

MODEL_ID = "ii_other_ida"


def project_other_ida(inputs: OtherIdaInputs, scenario: IncomeScenarioPaths) -> IncomeModelResult:
    balance = inputs.total_balance
    alpha = inputs.short_rate_share
    warnings: list[str] = []
    if balance == 0.0:
        warnings.append("total_balance is zero — income is identically zero (logged)")
    if alpha == 0.0:
        warnings.append(
            "short_rate_share is exactly 0 — the whole balance earns the 10-year Treasury "
            "(degenerate single-rate case; the source states fed funds sold comprise most of "
            "this component, so review the input — logged, never adjusted)"
        )
    elif alpha == 1.0:
        warnings.append(
            "short_rate_share is exactly 1 — the whole balance earns the 3-month Treasury "
            "(degenerate single-rate case; logged, never adjusted)"
        )

    rows: list[IncomeQuarterResult] = []
    for quarter in PROJECTION_QUARTERS:
        t3m = scenario.usd_3m_treasury[quarter]
        t10y = scenario.usd_10y_treasury[quarter]
        for leg_name, leg_rate in (("Treasury3m", t3m), ("Treasury10y", t10y)):
            if leg_rate < 0.0:
                warnings.append(
                    f"PQ{quarter}: negative {leg_name} {leg_rate} can flip the income sign "
                    f"(arithmetically valid; logged, never clamped)"
                )
        blended_rate = alpha * t3m + (1.0 - alpha) * t10y
        rows.append(
            IncomeQuarterResult(
                quarter=quarter,
                annualized_rate=blended_rate,
                average_balance=balance,
                # Chapter §6 step 4: the D-004 ÷4 applied once, to the A43 sum.
                quarterly_income=quarterly_income(balance, blended_rate),
                diagnostics=OtherIdaQuarterDiagnostics(
                    total_balance=balance,
                    short_rate_share=alpha,
                    usd_3m_treasury=t3m,
                    usd_10y_treasury=t10y,
                    blended_rate=blended_rate,
                    short_leg_income=quarterly_income(alpha * balance, t3m),
                    long_leg_income=quarterly_income((1.0 - alpha) * balance, t10y),
                ),
            )
        )
    return build_income_result(MODEL_ID, inputs.firm_id, scenario.scenario_id, rows, warnings)

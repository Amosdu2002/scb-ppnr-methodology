"""ie_other_dom_dep — Interest Expense on Other Domestic Deposits (Eqs A45–A47, B.v.a(8)).

Two-regime deposit-beta model over subcomponents {mma, savings, transaction} with the
Table A7 median betas; rate mechanics live in deposit_regime_engine (shared, by Fed
statement, only with ie_foreign_dep).

Expense multiplicand (PID-ODD-3, company-reference confirmed 2026-07-23): the sum of
the A47 weight balances (items 34B+34C+34D) — the same balances that weight the rates,
so the expense equals Σ_i rate_i × balance_i. The PID-ODD-2 MDRM sum
(`total_average_balance`) no longer enters the expense; when supplied, it serves only
the consistency monitor — divergence beyond the threshold is logged, never forced equal.

    odd_interest_expense(b,t) = Σ_i balance_i(b) × aggregate_rate(b,t) / 4   (D-004)
"""

from __future__ import annotations

from .common import build_result, quarterly_expense
from .deposit_regime_engine import project_deposit_rates
from .schemas import (
    PROJECTION_QUARTERS,
    TABLE_A7_OTHER_DOM,
    DepositBetaParams,
    ModelResult,
    OtherDomDepInputs,
    QuarterResult,
    ScenarioPaths,
)

MODEL_ID = "ie_other_dom_dep"

# [CODE] monitor threshold only — flags divergence between the expense balance and the
# optional PID-ODD-2 reference total; not methodology, never alters any value.
BALANCE_CONSISTENCY_MONITOR_REL = 0.10


def project_other_dom_dep(
    inputs: OtherDomDepInputs,
    scenario: ScenarioPaths,
    params: DepositBetaParams = TABLE_A7_OTHER_DOM,
) -> ModelResult:
    quarter_diags, warnings = project_deposit_rates(inputs.subcomponents, scenario, params)

    expense_balance = sum(sub.balance for sub in inputs.subcomponents.values())
    reference = inputs.total_average_balance
    if reference is not None:
        larger = max(expense_balance, reference)
        if larger > 0.0 and abs(expense_balance - reference) / larger > BALANCE_CONSISTENCY_MONITOR_REL:
            warnings.append(
                f"consistency monitor: expense balance (A47 weight sum) {expense_balance} vs the "
                f"PID-ODD-2 reference total {reference} diverge beyond "
                f"{BALANCE_CONSISTENCY_MONITOR_REL:.0%} (different physical sources; logged, "
                f"never forced equal — the reference never enters the expense, PID-ODD-3)"
            )

    rows = [
        QuarterResult(
            quarter=quarter,
            annualized_rate=diag.aggregate_rate,
            average_balance=expense_balance,
            quarterly_expense=quarterly_expense(expense_balance, diag.aggregate_rate),
            diagnostics=diag,
        )
        for quarter, diag in zip(PROJECTION_QUARTERS, quarter_diags)
    ]
    return build_result(MODEL_ID, inputs.firm_id, scenario.scenario_id, rows, warnings)

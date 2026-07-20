"""ie_other_dom_dep — Interest Expense on Other Domestic Deposits (Eqs A45–A47, B.v.a(8)).

Two-regime deposit-beta model over subcomponents {mma, savings, transaction} with the
Table A7 median betas; rate mechanics live in deposit_regime_engine (shared, by Fed
statement, only with ie_foreign_dep). The expense multiplicand `total_average_balance`
(PID-ODD-2) deliberately comes from a different physical source than the A47 weights
(PID-ODD-1): their closeness is a consistency monitor, never an identity — divergence
beyond the monitor threshold is logged, equality is never forced.

    odd_interest_expense(b,t) = total_average_balance(b) × aggregate_rate(b,t) / 4   (D-004)
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

# [CODE] monitor threshold only — flags PID-ODD-1 vs PID-ODD-2 divergence for review;
# not methodology and never used to alter any value.
BALANCE_CONSISTENCY_MONITOR_REL = 0.10


def project_other_dom_dep(
    inputs: OtherDomDepInputs,
    scenario: ScenarioPaths,
    params: DepositBetaParams = TABLE_A7_OTHER_DOM,
) -> ModelResult:
    quarter_diags, warnings = project_deposit_rates(inputs.subcomponents, scenario, params)

    weights_sum = sum(sub.balance for sub in inputs.subcomponents.values())
    larger = max(weights_sum, inputs.total_average_balance)
    if larger > 0.0 and abs(weights_sum - inputs.total_average_balance) / larger > BALANCE_CONSISTENCY_MONITOR_REL:
        warnings.append(
            f"consistency monitor: A47 weight sum {weights_sum} vs expense multiplicand "
            f"{inputs.total_average_balance} diverge beyond {BALANCE_CONSISTENCY_MONITOR_REL:.0%} "
            f"(different physical sources, PID-ODD-1 vs PID-ODD-2; logged, never forced equal)"
        )

    rows = [
        QuarterResult(
            quarter=quarter,
            annualized_rate=diag.aggregate_rate,
            average_balance=inputs.total_average_balance,
            quarterly_expense=quarterly_expense(inputs.total_average_balance, diag.aggregate_rate),
            diagnostics=diag,
        )
        for quarter, diag in zip(PROJECTION_QUARTERS, quarter_diags)
    ]
    return build_result(MODEL_ID, inputs.firm_id, scenario.scenario_id, rows, warnings)

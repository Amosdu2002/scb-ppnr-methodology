"""ie_foreign_dep — Interest Expense on Foreign Deposits (B.v.a(9)).

Reuses the Equations A45–A47 framework of ie_other_dom_dep by reference (Fed-stated)
over subcomponents {foreign_nontime, foreign_time} with the Table A7 foreign median
betas (non-time 0.890/0.790; time 1.000/1.000 — so the time rate tracks ΔTreasury3m
one-for-one in non-ELB quarters). No FX translation (Fed-stated). Unlike
ie_other_dom_dep, the same 35A/35B balances serve as both the A47 weights and, summed,
the expense multiplicand (INT-a):

    foreign_interest_expense(b,t) = (35A + 35B) × aggregate_rate(b,t) / 4   (D-004)
"""

from __future__ import annotations

from .common import build_result, quarterly_expense
from .deposit_regime_engine import project_deposit_rates
from .schemas import (
    PROJECTION_QUARTERS,
    TABLE_A7_FOREIGN,
    DepositBetaParams,
    ForeignDepInputs,
    ModelResult,
    QuarterResult,
    ScenarioPaths,
)

MODEL_ID = "ie_foreign_dep"


def project_foreign_dep(
    inputs: ForeignDepInputs,
    scenario: ScenarioPaths,
    params: DepositBetaParams = TABLE_A7_FOREIGN,
) -> ModelResult:
    quarter_diags, warnings = project_deposit_rates(inputs.subcomponents, scenario, params)
    expense_balance = sum(sub.balance for sub in inputs.subcomponents.values())

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

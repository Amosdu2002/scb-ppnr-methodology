"""ie_fed_funds_repo — Interest Expense on Federal Funds Purchased and Securities Sold
under Agreements to Repurchase (Eq A48, B.v.a(10)).

Direct structural calculator: the rate is exactly the contemporaneous 3-month Treasury
yield — no spread, scaling, lag, regime, or parameters of any kind; the balance is
items 36A + 36B (PID-FFR-1), held flat at the launch point (Fed-stated). The expense
path is therefore exactly proportional to the Treasury3m path.

    fed_funds_repo_interest_expense(b,q) = (36A + 36B) × Treasury3m(q) / 4   (D-004)
"""

from __future__ import annotations

from .common import build_result, quarterly_expense
from .schemas import (
    PROJECTION_QUARTERS,
    FedFundsRepoInputs,
    FedFundsRepoQuarterDiagnostics,
    ModelResult,
    QuarterResult,
    ScenarioPaths,
)

MODEL_ID = "ie_fed_funds_repo"


def project_fed_funds_repo(inputs: FedFundsRepoInputs, scenario: ScenarioPaths) -> ModelResult:
    balance = inputs.fed_funds_purchased_balance + inputs.repo_sold_balance
    warnings: list[str] = []
    if balance == 0.0:
        warnings.append("both balance components are zero — expense is identically zero (logged)")

    rows: list[QuarterResult] = []
    for quarter in PROJECTION_QUARTERS:
        rate = scenario.usd_3m_treasury[quarter]
        if rate < 0.0:
            warnings.append(
                f"PQ{quarter}: negative Treasury3m {rate} flips the expense sign "
                f"(arithmetically valid; logged, never clamped)"
            )
        rows.append(
            QuarterResult(
                quarter=quarter,
                annualized_rate=rate,
                average_balance=balance,
                quarterly_expense=quarterly_expense(balance, rate),
                diagnostics=FedFundsRepoQuarterDiagnostics(
                    fed_funds_purchased_balance=inputs.fed_funds_purchased_balance,
                    repo_sold_balance=inputs.repo_sold_balance,
                    usd_3m_treasury=rate,
                ),
            )
        )
    return build_result(MODEL_ID, inputs.firm_id, scenario.scenario_id, rows, warnings)

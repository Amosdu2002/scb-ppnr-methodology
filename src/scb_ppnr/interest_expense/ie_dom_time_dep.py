"""ie_dom_time_dep — Interest Expense on Domestic Time Deposits (Eq A44, B.v.a(7)).

WAL-based repricing recursion, run in annualized decimal rates:

    Rate(b,t) = ρ_b · Treasury1y(t) + (1 − ρ_b) · Rate(b,t−1),   t = 1..9

with ρ_b = 1/WAL_quarters = 3/WAL_months (item 71 in months, PID-3/PID-4), the t=1
lag seeded by the item 42E launch-point rate, and the item 34E balance held flat
(PID-1). No spread, floor, cap, or regime exists (FACT absence); negative rates are
logged, never clamped. Expense: balance × rate / 4 at the final step only (D-004/PID-6).
"""

from __future__ import annotations

from .common import build_result, quarterly_expense
from .schemas import (
    PROJECTION_QUARTERS,
    DomTimeDepInputs,
    DomTimeDepQuarterDiagnostics,
    ModelResult,
    QuarterResult,
    ScenarioPaths,
    ValidationFailure,
)

MODEL_ID = "ie_dom_time_dep"


def project_dom_time_dep(inputs: DomTimeDepInputs, scenario: ScenarioPaths) -> ModelResult:
    wal_months = inputs.wal_months
    rho = 3.0 / wal_months
    if not 0.0 < rho <= 1.0:
        raise ValidationFailure(
            f"{MODEL_ID}: rho = 3/WAL_months = {rho} lies outside (0, 1] "
            f"(wal_months = {wal_months}; a WAL below 3 months is invalid)"
        )
    wal_quarters = wal_months / 3.0

    warnings: list[str] = []
    rows: list[QuarterResult] = []
    previous_rate = inputs.rate_launchpoint
    for quarter in PROJECTION_QUARTERS:
        treasury_1y = scenario.usd_1y_treasury[quarter]
        rate = rho * treasury_1y + (1.0 - rho) * previous_rate
        if rate < 0.0:
            warnings.append(f"PQ{quarter}: negative projected rate {rate} (legal; logged, never clamped)")
        rows.append(
            QuarterResult(
                quarter=quarter,
                annualized_rate=rate,
                average_balance=inputs.balance,
                quarterly_expense=quarterly_expense(inputs.balance, rate),
                diagnostics=DomTimeDepQuarterDiagnostics(
                    wal_months=wal_months,
                    wal_quarters=wal_quarters,
                    rho=rho,
                    previous_rate=previous_rate,
                    usd_1y_treasury=treasury_1y,
                ),
            )
        )
        previous_rate = rate
    return build_result(MODEL_ID, inputs.firm_id, scenario.scenario_id, rows, warnings)

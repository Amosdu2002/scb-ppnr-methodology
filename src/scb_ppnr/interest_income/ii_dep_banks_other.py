"""ii_dep_banks_other — Interest Income on Deposits with Banks and Other
(Eq A39, B.v.a(2)).

Direct structural calculator: the rate is exactly the contemporaneous 3-month
Treasury yield — no spread, scaling, lag, regime, or parameters of any kind; the
balance is the Schedule G NII Worksheet line item 14 (source-stated), held flat
at the launch point (Fed-stated). The income path is therefore exactly
proportional to the Treasury3m path.

    dep_banks_other_interest_income(b,q) = item14_balance × Treasury3m(q) / 4   (D-004)
"""

from __future__ import annotations

from ..core.schemas import PROJECTION_QUARTERS
from .common import build_income_result, quarterly_income
from .schemas import (
    DepBanksOtherInputs,
    DepBanksOtherQuarterDiagnostics,
    IncomeModelResult,
    IncomeQuarterResult,
    IncomeScenarioPaths,
)

MODEL_ID = "ii_dep_banks_other"


def project_dep_banks_other(inputs: DepBanksOtherInputs, scenario: IncomeScenarioPaths) -> IncomeModelResult:
    balance = inputs.balance
    warnings: list[str] = []
    if balance == 0.0:
        warnings.append("balance is zero — income is identically zero (logged)")

    rows: list[IncomeQuarterResult] = []
    for quarter in PROJECTION_QUARTERS:
        rate = scenario.usd_3m_treasury[quarter]
        if rate < 0.0:
            warnings.append(
                f"PQ{quarter}: negative Treasury3m {rate} flips the income sign "
                f"(arithmetically valid; logged, never clamped)"
            )
        rows.append(
            IncomeQuarterResult(
                quarter=quarter,
                annualized_rate=rate,
                average_balance=balance,
                quarterly_income=quarterly_income(balance, rate),
                diagnostics=DepBanksOtherQuarterDiagnostics(
                    balance=balance,
                    usd_3m_treasury=rate,
                ),
            )
        )
    return build_income_result(MODEL_ID, inputs.firm_id, scenario.scenario_id, rows, warnings)

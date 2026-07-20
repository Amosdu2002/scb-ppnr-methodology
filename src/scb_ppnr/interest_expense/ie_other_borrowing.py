"""ie_other_borrowing — Interest Expense on Other Borrowing (Eq A53, B.v.d(2)) with the
PID-OB-5 nine-quarter alpha calibration.

Rate (annualized decimal, Table A9 betas; Treasury3m coefficient 1 by construction):

    R(b,q) = Treasury3m(q) + β1·BBB(q) + β2·CPShare(b,0) + β3·SubdebtShare(b,0) + α_b

α_b is a PROJECT CALIBRATION PARAMETER (PID-OB-5, user-confirmed 2026-07-20; supersedes
the PQ0 backsolve of PID-OB-1/PID-OB-3) — never a Fed published coefficient, and PQ0
actual expense is never used. The four sibling models run first; per quarter q = 1..9:

    ImpliedOB(b,q) = FRBTotal(b,q) − DomTime(b,q) − OtherDom(b,q) − Foreign(b,q) − FedFundsRepo(b,q)

and the single α_b, constant across PQ1..PQ9, solves the nine-quarter cumulative match

    Σ_q B(b,q)·(R0(b,q) + α_b)/4 = Σ_q ImpliedOB(b,q)
    ⇒  α_b = (4·Σ_q ImpliedOB − Σ_q B·R0) / Σ_q B          (closed form; no optimizer)

Only the cumulative total is matched — the quarterly modeled and implied paths generally
differ and are both preserved as diagnostics. Σ_q B zero or invalid is a validation
error with no fallback. Negative implied quarters and negative rates are logged, never
clamped; no floor or cap exists on the rate or on α_b.
"""

from __future__ import annotations

from types import MappingProxyType
from typing import Mapping

from .common import (
    build_result,
    freeze_projection_path,
    quarterly_expense,
    reconciliation_tolerance,
    require_same_run,
    sum_path,
)
from .schemas import (
    PROJECTION_QUARTERS,
    RATE_SCALE_GUARD,
    TABLE_A9_OTHER_BORROWING,
    AlphaCalibration,
    ModelResult,
    OtherBorrowingInputs,
    OtherBorrowingParams,
    OtherBorrowingQuarterDiagnostics,
    QuarterResult,
    ScenarioPaths,
    ValidationFailure,
)

MODEL_ID = "ie_other_borrowing"

# Execution-order contract (chapter §9/§3.4): these four complete before calibration.
SIBLING_MODEL_IDS: tuple[str, ...] = (
    "ie_dom_time_dep",
    "ie_other_dom_dep",
    "ie_foreign_dep",
    "ie_fed_funds_repo",
)

_CALIBRATION_MATCH_TOL = 1e-12


def pre_alpha_rate_path(
    inputs: OtherBorrowingInputs,
    scenario: ScenarioPaths,
    params: OtherBorrowingParams = TABLE_A9_OTHER_BORROWING,
) -> Mapping[int, float]:
    """R0(b,q): the Eq A53 rate with α_b excluded, annualized decimal."""
    return MappingProxyType(
        {
            q: (
                scenario.usd_3m_treasury[q]
                + params.beta_bbb * scenario.bbb_corporate_yield[q]
                + params.beta_cp * inputs.cp_share
                + params.beta_subdebt * inputs.subdebt_share
            )
            for q in PROJECTION_QUARTERS
        }
    )


def balance_path(inputs: OtherBorrowingInputs) -> Mapping[int, float]:
    """B(b,q) — flat at B(b,0) per the Fed's constant-balance statement."""
    return MappingProxyType({q: inputs.total_balance for q in PROJECTION_QUARTERS})


def implied_other_borrowing_path(
    frb_total_interest_expense: Mapping[int, float],
    dom_time_dep: ModelResult,
    other_dom_dep: ModelResult,
    foreign_dep: ModelResult,
    fed_funds_repo: ModelResult,
) -> Mapping[int, float]:
    """ImpliedOB(b,q) = FRBTotal(b,q) − the four sibling expenses, q = 1..9.

    Validates that the four results are the expected models from one firm × scenario
    run; negative implied quarters are legal and preserved (callers log them)."""
    siblings = (dom_time_dep, other_dom_dep, foreign_dep, fed_funds_repo)
    for result, expected_id in zip(siblings, SIBLING_MODEL_IDS):
        if result.model_id != expected_id:
            raise ValidationFailure(
                f"{MODEL_ID}: expected a {expected_id} result in this position, got {result.model_id}"
            )
    require_same_run(siblings, firm_id=dom_time_dep.firm_id, scenario_id=dom_time_dep.scenario_id)
    frb_total = freeze_projection_path("frb_total_interest_expense", frb_total_interest_expense)
    return MappingProxyType(
        {
            q: frb_total[q] - sum(result.expense_path()[q] for result in siblings)
            for q in PROJECTION_QUARTERS
        }
    )


def calibrate_alpha_b(
    implied_path: Mapping[int, float],
    balances: Mapping[int, float],
    pre_alpha_rates: Mapping[int, float],
) -> AlphaCalibration:
    """Closed-form PID-OB-5 calibration (all paths over PQ1..PQ9; USD, USD, decimal)."""
    implied = freeze_projection_path("implied_path", implied_path)
    balance = freeze_projection_path("balance_path", balances)
    rate0 = freeze_projection_path("pre_alpha_rate_path", pre_alpha_rates)

    balance_sum = sum_path(balance)
    if balance_sum <= 0.0:
        raise ValidationFailure(
            f"{MODEL_ID}: sum of PQ1..PQ9 balances is {balance_sum} — zero or invalid; "
            f"calibration blocked, no fallback (PID-OB-5)"
        )

    implied_sum = sum_path(implied)
    balance_weighted_rate0 = sum(balance[q] * rate0[q] for q in PROJECTION_QUARTERS)
    alpha_b = (4.0 * implied_sum - balance_weighted_rate0) / balance_sum

    modeled = MappingProxyType(
        {q: quarterly_expense(balance[q], rate0[q] + alpha_b) for q in PROJECTION_QUARTERS}
    )
    differences = MappingProxyType(
        {q: modeled[q] - implied[q] for q in PROJECTION_QUARTERS}
    )
    cumulative_modeled = sum_path(modeled)
    cumulative_difference = cumulative_modeled - implied_sum
    if abs(cumulative_difference) > 10.0 * reconciliation_tolerance(implied_sum):
        raise ValidationFailure(
            f"{MODEL_ID}: internal error — closed-form alpha failed the nine-quarter "
            f"cumulative match (difference {cumulative_difference})"
        )

    warnings: list[str] = []
    for q in PROJECTION_QUARTERS:
        if implied[q] < 0.0:
            warnings.append(
                f"PQ{q}: negative implied Other Borrowing expense {implied[q]} "
                f"(legal; logged, never clamped)"
            )
    if abs(alpha_b) >= RATE_SCALE_GUARD:
        warnings.append(
            f"|alpha_b| = {abs(alpha_b)} exceeds the magnitude screen {RATE_SCALE_GUARD} — "
            f"possible scale mismatch or a residual target inconsistent with the modeled components"
        )

    return AlphaCalibration(
        alpha_b=alpha_b,
        balance_sum=balance_sum,
        implied_path=implied,
        pre_alpha_rate_path=rate0,
        modeled_path=modeled,
        quarterly_difference_path=differences,
        cumulative_implied=implied_sum,
        cumulative_modeled=cumulative_modeled,
        cumulative_difference=cumulative_difference,
        warnings=tuple(warnings),
    )


def project_other_borrowing(
    inputs: OtherBorrowingInputs,
    scenario: ScenarioPaths,
    calibration: AlphaCalibration,
    params: OtherBorrowingParams = TABLE_A9_OTHER_BORROWING,
) -> ModelResult:
    """Final Eq A53 rate and expense path using the calibrated α_b.

    Guards that the calibration actually corresponds to these inputs and this
    scenario (pre-α rates and modeled expenses must reproduce exactly)."""
    rate0 = pre_alpha_rate_path(inputs, scenario, params)
    for q in PROJECTION_QUARTERS:
        if abs(rate0[q] - calibration.pre_alpha_rate_path[q]) > _CALIBRATION_MATCH_TOL:
            raise ValidationFailure(
                f"{MODEL_ID}: calibration does not correspond to these inputs/scenario "
                f"(pre-alpha rate mismatch at PQ{q})"
            )
        expected_modeled = quarterly_expense(inputs.total_balance, rate0[q] + calibration.alpha_b)
        if abs(expected_modeled - calibration.modeled_path[q]) > max(
            _CALIBRATION_MATCH_TOL, reconciliation_tolerance(calibration.modeled_path[q])
        ):
            raise ValidationFailure(
                f"{MODEL_ID}: calibration does not correspond to this balance "
                f"(modeled expense mismatch at PQ{q})"
            )

    warnings: list[str] = list(calibration.warnings)
    rows: list[QuarterResult] = []
    for q in PROJECTION_QUARTERS:
        rate = rate0[q] + calibration.alpha_b
        if rate < 0.0:
            warnings.append(f"PQ{q}: negative rate {rate} (legal — no floor exists; logged, never clamped)")
        rows.append(
            QuarterResult(
                quarter=q,
                annualized_rate=rate,
                average_balance=inputs.total_balance,
                quarterly_expense=quarterly_expense(inputs.total_balance, rate),
                diagnostics=OtherBorrowingQuarterDiagnostics(
                    usd_3m_treasury=scenario.usd_3m_treasury[q],
                    bbb_contribution=params.beta_bbb * scenario.bbb_corporate_yield[q],
                    cp_share_contribution=params.beta_cp * inputs.cp_share,
                    subdebt_share_contribution=params.beta_subdebt * inputs.subdebt_share,
                    pre_alpha_rate=rate0[q],
                    alpha_b=calibration.alpha_b,
                    implied_expense=calibration.implied_path[q],
                    modeled_expense=calibration.modeled_path[q],
                    quarterly_difference=calibration.quarterly_difference_path[q],
                ),
            )
        )
    return build_result(MODEL_ID, inputs.firm_id, scenario.scenario_id, rows, warnings)


def run_other_borrowing(
    inputs: OtherBorrowingInputs,
    scenario: ScenarioPaths,
    frb_total_interest_expense: Mapping[int, float],
    dom_time_dep: ModelResult,
    other_dom_dep: ModelResult,
    foreign_dep: ModelResult,
    fed_funds_repo: ModelResult,
    params: OtherBorrowingParams = TABLE_A9_OTHER_BORROWING,
) -> tuple[ModelResult, AlphaCalibration]:
    """Steps 5–7 of the family execution order: implied residual → closed-form α_b →
    final rate/expense path. Requires the four completed sibling results."""
    require_same_run(
        (dom_time_dep, other_dom_dep, foreign_dep, fed_funds_repo),
        firm_id=inputs.firm_id,
        scenario_id=scenario.scenario_id,
    )
    implied = implied_other_borrowing_path(
        frb_total_interest_expense, dom_time_dep, other_dom_dep, foreign_dep, fed_funds_repo
    )
    calibration = calibrate_alpha_b(implied, balance_path(inputs), pre_alpha_rate_path(inputs, scenario, params))
    result = project_other_borrowing(inputs, scenario, calibration, params)
    return result, calibration

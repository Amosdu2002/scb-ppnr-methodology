"""nii_trading_al — Net Interest Income on Trading Assets and Liabilities (Eq A52,
B.v.d(1)) with the PID-TRD-1 nine-quarter alpha calibration on the PID-TRD-3
annualized basis. Mirrors ie_other_borrowing's factoring (pre-α path → calibrate
→ project); the calibration policy is isolated in `calibrate_alpha_b`.

Rate (ANNUALIZED per the reference basis, PID-TRD-3; Table A9 beta):

    Rate(b,q) = β·Treasury3m(q) + α_b            β = 0.278 (Table A9, PDF p. 234)

The source states ESTIMATION only — no projection step, no balance basis, no
launch-point language (pp. 225–230, image-verified; OQ-007). The projection
construction here reproduces the observed reference workbook (PID-TRD-2/3,
user-confirmed 2026-08-13): dollars = Rate × NetTA(b,0) / 4 with NetTA the
Schedule G trading assets − trading liabilities average balances held flat.

α_b is a PROJECT CALIBRATION PARAMETER (PID-TRD-1 — the PID-OB-5 income-side
mirror) — never a Fed published coefficient, and PQ0 actuals are never used.
The six sibling income models run first; per quarter q = 1..9:

    ImpliedTATL(b,q) = FRBIncome(b,q) − Σ_m Income_m(b,q)
        m ∈ {ii_loans, ii_dep_banks_other, ii_ust, ii_mbs, ii_other_sec, ii_other_ida}

and the single α_b, constant across PQ1..PQ9, solves the nine-quarter match

    Σ_q NetTA(b,q)·(R0(b,q) + α_b)/4 = Σ_q ImpliedTATL(b,q)
    ⇒  α_b = (4·Σ_q ImpliedTATL − Σ_q NetTA·R0) / Σ_q NetTA     (closed form)

BASIS TRIPWIRE (chapter §8): the ×4 belongs to the PID-TRD-3 annualized basis —
under the source-literal quarterly-LHS reading (the estimation numerator is
stated quarterly, PDF p. 225, retained as recorded tension) the formula would
carry NO ×4. The basis is declared here, never mixed; a mix-up mis-scales α_b
and the scenario sensitivity by 4.

Only the cumulative total is matched — the quarterly modeled and implied paths
generally differ and are both preserved as diagnostics (the reference tab itself
carries all three rows plus the average of the differences). Negative implied
quarters and negative modeled net income are legal (a NET item) — logged, never
clamped; no floor or cap exists. A money-unit mismatch between the FRB income
path and the sibling incomes would be silently absorbed into α_b, so the
implied-path step hard-fails at ≥ UNITS_MISMATCH_RATIO_GUARD (D-006 class).
"""

from __future__ import annotations

from types import MappingProxyType
from typing import Mapping

from ..core.common import (
    freeze_projection_path,
    reconciliation_tolerance,
    require_same_run,
    sum_path,
)
from ..core.schemas import PROJECTION_QUARTERS, RATE_SCALE_GUARD, ValidationFailure
from .common import build_income_result, quarterly_income
from .schemas import (
    TABLE_A9_TRADING,
    IncomeModelResult,
    IncomeQuarterResult,
    IncomeScenarioPaths,
    TradingAlphaCalibration,
    TradingNiiInputs,
    TradingNiiParams,
    TradingQuarterDiagnostics,
)

MODEL_ID = "nii_trading_al"

# Execution-order contract (chapter §11/§13): the six sibling income models
# complete before calibration — the PID-OB-5 execution-order analog.
SIBLING_MODEL_IDS: tuple[str, ...] = (
    "ii_loans",
    "ii_dep_banks_other",
    "ii_ust",
    "ii_mbs",
    "ii_other_sec",
    "ii_other_ida",
)

_CALIBRATION_MATCH_TOL = 1e-12

# A cumulative FRB-income vs cumulative sibling-income ratio at or beyond this
# screen is treated as a money-unit mismatch (D-006 class) and blocks the run —
# α_b would otherwise absorb it and the final reconciliation would still pass.
UNITS_MISMATCH_RATIO_GUARD: float = 50.0


def pre_alpha_rate_path(
    scenario: IncomeScenarioPaths,
    params: TradingNiiParams = TABLE_A9_TRADING,
) -> Mapping[int, float]:
    """R0(b,q) = β·Treasury3m(q): the Eq A52 projection rate with α_b excluded,
    ANNUALIZED per the PID-TRD-3 basis. PQ1..PQ9 only — no PQ0 value is consumed
    (PID-TRD-1: no launch-point backsolve exists in this model)."""
    return MappingProxyType(
        {q: params.beta_treasury3m * scenario.usd_3m_treasury[q] for q in PROJECTION_QUARTERS}
    )


def net_trading_asset_path(inputs: TradingNiiInputs) -> Mapping[int, float]:
    """NetTA(b,q) — flat at NetTA(b,0) (PID-TRD-3, reference-observed: a single
    Balance cell feeds every projection quarter; the source states no projection
    balance basis at all — OQ-007 resolved-for-project)."""
    return MappingProxyType({q: inputs.net_trading_assets for q in PROJECTION_QUARTERS})


def implied_trading_path(
    frb_total_interest_income: Mapping[int, float],
    sibling_income_paths: Mapping[str, Mapping[int, float]],
) -> Mapping[int, float]:
    """ImpliedTATL(b,q) = FRBIncome(b,q) − Σ six sibling incomes, q = 1..9.

    `sibling_income_paths` must carry exactly the six SIBLING_MODEL_IDS keys
    (results-level composition — loans and securities arrive from their own
    runners; firm/scenario alignment is the caller's contract, enforced where
    typed results exist via the orchestrator). Negative implied quarters are
    legal and preserved (callers log them)."""
    got = set(sibling_income_paths.keys())
    expected = set(SIBLING_MODEL_IDS)
    if got != expected:
        missing = sorted(expected - got)
        extra = sorted(got - expected)
        raise ValidationFailure(
            f"{MODEL_ID}: expected exactly the six sibling income paths {list(SIBLING_MODEL_IDS)}; "
            f"missing {missing}, unexpected {extra}"
        )
    siblings = {
        model_id: freeze_projection_path(f"sibling_income_paths[{model_id}]", sibling_income_paths[model_id])
        for model_id in SIBLING_MODEL_IDS
    }
    frb_income = freeze_projection_path("frb_total_interest_income", frb_total_interest_income)

    frb_sum = sum_path(frb_income)
    sibling_sum = sum(sum_path(path) for path in siblings.values())
    if frb_sum > 0.0 and sibling_sum > 0.0:
        ratio = max(frb_sum, sibling_sum) / min(frb_sum, sibling_sum)
        if ratio >= UNITS_MISMATCH_RATIO_GUARD:
            raise ValidationFailure(
                f"{MODEL_ID}: cumulative FRB income {frb_sum} vs cumulative sibling incomes "
                f"{sibling_sum} differ by ×{ratio:.0f} (screen {UNITS_MISMATCH_RATIO_GUARD:.0f}) — "
                f"probable money-unit mismatch (e.g. FRB billions against Schedule G millions); "
                f"every money row must declare millions|billions, canonical unit USD millions "
                f"(D-006); calibration blocked, α_b never absorbs a unit error"
            )

    return MappingProxyType(
        {
            q: frb_income[q] - sum(path[q] for path in siblings.values())
            for q in PROJECTION_QUARTERS
        }
    )


def calibrate_alpha_b(
    implied_path: Mapping[int, float],
    net_trading_assets: Mapping[int, float],
    pre_alpha_rates: Mapping[int, float],
) -> TradingAlphaCalibration:
    """Closed-form PID-TRD-1 calibration on the PID-TRD-3 annualized basis
    (all paths over PQ1..PQ9; USD, USD, annualized decimal).

    The isolated calibration policy (architecture note): the basis lives HERE —
    the ×4 reverses the ÷4 at the dollar step exactly as in ie_other_borrowing;
    under the source-literal quarterly-LHS reading there would be no ×4."""
    implied = freeze_projection_path("implied_path", implied_path)
    balance = freeze_projection_path("net_trading_asset_path", net_trading_assets)
    rate0 = freeze_projection_path("pre_alpha_rate_path", pre_alpha_rates)

    balance_sum = sum_path(balance)
    if balance_sum <= 0.0:
        raise ValidationFailure(
            f"{MODEL_ID}: sum of PQ1..PQ9 net trading assets is {balance_sum} — zero or invalid; "
            f"calibration blocked, no fallback (PID-TRD-1)"
        )

    implied_sum = sum_path(implied)
    balance_weighted_rate0 = sum(balance[q] * rate0[q] for q in PROJECTION_QUARTERS)
    alpha_b = (4.0 * implied_sum - balance_weighted_rate0) / balance_sum

    modeled = MappingProxyType(
        {q: quarterly_income(balance[q], rate0[q] + alpha_b) for q in PROJECTION_QUARTERS}
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
                f"PQ{q}: negative implied trading NII {implied[q]} "
                f"(legal — a NET item; logged, never clamped)"
            )
    if abs(alpha_b) >= RATE_SCALE_GUARD:
        warnings.append(
            f"|alpha_b| = {abs(alpha_b)} exceeds the magnitude screen {RATE_SCALE_GUARD} "
            f"(annualized-decimal basis, PID-TRD-3) — possible scale mismatch or a residual "
            f"target inconsistent with the modeled components"
        )

    return TradingAlphaCalibration(
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


def project_trading_nii(
    inputs: TradingNiiInputs,
    scenario: IncomeScenarioPaths,
    calibration: TradingAlphaCalibration,
    params: TradingNiiParams = TABLE_A9_TRADING,
) -> IncomeModelResult:
    """Final rate and net-income path using the calibrated α_b.

    Guards that the calibration actually corresponds to this scenario and this
    net balance (pre-α rates and modeled incomes must reproduce exactly)."""
    rate0 = pre_alpha_rate_path(scenario, params)
    for q in PROJECTION_QUARTERS:
        if abs(rate0[q] - calibration.pre_alpha_rate_path[q]) > _CALIBRATION_MATCH_TOL:
            raise ValidationFailure(
                f"{MODEL_ID}: calibration does not correspond to this scenario "
                f"(pre-alpha rate mismatch at PQ{q})"
            )
        expected_modeled = quarterly_income(inputs.net_trading_assets, rate0[q] + calibration.alpha_b)
        if abs(expected_modeled - calibration.modeled_path[q]) > max(
            _CALIBRATION_MATCH_TOL, reconciliation_tolerance(calibration.modeled_path[q])
        ):
            raise ValidationFailure(
                f"{MODEL_ID}: calibration does not correspond to this net trading balance "
                f"(modeled income mismatch at PQ{q})"
            )

    warnings: list[str] = list(calibration.warnings)
    rows: list[IncomeQuarterResult] = []
    for q in PROJECTION_QUARTERS:
        rate = rate0[q] + calibration.alpha_b
        income = quarterly_income(inputs.net_trading_assets, rate)
        if income < 0.0:
            warnings.append(
                f"PQ{q}: negative modeled trading NII {income} "
                f"(legal — a NET item, no floor exists; logged, never clamped)"
            )
        rows.append(
            IncomeQuarterResult(
                quarter=q,
                annualized_rate=rate,
                average_balance=inputs.net_trading_assets,
                quarterly_income=income,
                diagnostics=TradingQuarterDiagnostics(
                    usd_3m_treasury=scenario.usd_3m_treasury[q],
                    pre_alpha_rate=rate0[q],
                    alpha_b=calibration.alpha_b,
                    net_trading_assets=inputs.net_trading_assets,
                    implied_income=calibration.implied_path[q],
                    modeled_income=calibration.modeled_path[q],
                    quarterly_difference=calibration.quarterly_difference_path[q],
                ),
            )
        )
    return build_income_result(MODEL_ID, inputs.firm_id, scenario.scenario_id, rows, warnings)


def run_trading_nii(
    inputs: TradingNiiInputs,
    scenario: IncomeScenarioPaths,
    frb_total_interest_income: Mapping[int, float],
    sibling_income_paths: Mapping[str, Mapping[int, float]],
    params: TradingNiiParams = TABLE_A9_TRADING,
) -> tuple[IncomeModelResult, TradingAlphaCalibration]:
    """The family execution-order tail: implied residual → closed-form α_b →
    final rate/net-income path. Requires the six completed sibling paths."""
    implied = implied_trading_path(frb_total_interest_income, sibling_income_paths)
    calibration = calibrate_alpha_b(
        implied, net_trading_asset_path(inputs), pre_alpha_rate_path(scenario, params)
    )
    result = project_trading_nii(inputs, scenario, calibration, params)
    return result, calibration


def sibling_paths_from_results(
    results: Mapping[str, IncomeModelResult] | None = None,
    *,
    firm_id: str,
    scenario_id: str,
    **by_model_id: IncomeModelResult,
) -> dict[str, Mapping[int, float]]:
    """Convenience for callers holding typed results (e.g. the two calculators):
    extract income paths keyed by model id, enforcing run identity. Models whose
    engines produce plain paths (loans, securities runners) are merged by the
    caller into the same mapping."""
    merged: dict[str, IncomeModelResult] = dict(results or {})
    merged.update(by_model_id)
    require_same_run(merged.values(), firm_id=firm_id, scenario_id=scenario_id)
    for key, result in merged.items():
        if result.model_id != key:
            raise ValidationFailure(
                f"{MODEL_ID}: result keyed {key!r} carries model_id {result.model_id!r}"
            )
    return {key: result.income_path() for key, result in merged.items()}

"""Canonical input and result contracts for the proposed 2026 interest-income models.

Increment 1 scope: the Family A calculators `ii_dep_banks_other` (Eq A39) and
`ii_other_ida` (Eq A43). Later increments add the securities family (A40–A42),
loans (A32–A38, in a `loans/` subpackage), and trading NII (A52), extending —
never rewriting — these contracts.

Canonical units (asset-side conventions chapter §3–§4; decisions D-004, D-006):
monetary amounts in USD millions; every rate an annualized decimal; projection
horizon PQ1..PQ9 with PQ0 the launch point. Result types parallel the verified
expense-side shapes deliberately (same six-field positional contract consumed by
`core.build_result`); they are separate classes because the sides differ where it
matters — `quarterly_income` carries no sign constraint (trading NII is
legitimately negative), and rate/balance are Optional because the securities
models have no single balance × rate decomposition."""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Mapping

from ..core.schemas import (
    PROJECTION_QUARTERS,
    SCENARIO_QUARTERS_WITH_LAUNCH,
    ValidationFailure,
    check_balance,
    check_finite,
    check_rate,
    check_share,
    freeze_path,
    require_id,
)

# ---------------------------------------------------------------------------
# Scenario inputs
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class IncomeScenarioPaths:
    """Income-side scenario MEV paths in canonical names (asset conventions §3).

    All family series are required from day one (mirrors the expense
    precedent) even though Family A consumes only the two Treasury series.
    `usd_3m_treasury` includes PQ0 — required by the securities floating-margin
    imputation, which uses the t = 0 **spot** 3-month Treasury; the calculators
    read PQ1..PQ9 only. `usd_1y_treasury` (added at Increment 2) is the
    securities reinvestment coupon — the par-Treasury-curve 1-year yield
    (OQ-025(d), user-confirmed). Pre-PQ0 history never enters this container
    (the Eq A37 wholesale spread anchors are supplied launch-point firm inputs
    — asset conventions §5)."""

    scenario_id: str
    usd_3m_treasury: Mapping[int, float]
    usd_1y_treasury: Mapping[int, float]
    usd_10y_treasury: Mapping[int, float]
    prime_rate: Mapping[int, float]
    mortgage_rate: Mapping[int, float]

    def __post_init__(self) -> None:
        require_id("scenario_id", self.scenario_id)
        object.__setattr__(
            self, "usd_3m_treasury",
            freeze_path("usd_3m_treasury", self.usd_3m_treasury, SCENARIO_QUARTERS_WITH_LAUNCH, check_rate),
        )
        for name in ("usd_1y_treasury", "usd_10y_treasury", "prime_rate", "mortgage_rate"):
            object.__setattr__(
                self, name,
                freeze_path(name, getattr(self, name), PROJECTION_QUARTERS, check_rate),
            )


# ---------------------------------------------------------------------------
# Per-model firm inputs
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class DepBanksOtherInputs:
    """ii_dep_banks_other firm inputs: the Schedule G NII Worksheet line item 14
    balance (source-stated), held flat at the launch point (Fed-stated)."""

    firm_id: str
    balance: float

    def __post_init__(self) -> None:
        require_id("firm_id", self.firm_id)
        object.__setattr__(self, "balance", check_balance("balance", self.balance))


@dataclass(frozen=True)
class OtherIdaInputs:
    """ii_other_ida firm inputs: the Schedule G (G.2) line item 15 balance
    (source-stated) and the fed-funds-sold/reverse-repo share α — a supplied
    launch-point input (its worksheet-footnote derivation is unstated, OQ-024).
    Both held flat at the launch point (Fed-stated, including the share)."""

    firm_id: str
    total_balance: float
    short_rate_share: float

    def __post_init__(self) -> None:
        require_id("firm_id", self.firm_id)
        object.__setattr__(self, "total_balance", check_balance("total_balance", self.total_balance))
        object.__setattr__(self, "short_rate_share", check_share("short_rate_share", self.short_rate_share))


# ---------------------------------------------------------------------------
# Per-model quarter diagnostics (traceability intermediates)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class TradingNiiInputs:
    """nii_trading_al firm inputs (PID-TRD-2, user-supplied 2026-08-13): the
    Schedule G NII Worksheet trading assets and trading liabilities average
    balances at the launch point (physical cells R30 / R112 on the reference
    workbook's "14Q Sch G" sheet; the Fed source names the worksheet but no line
    items — FACT absence). Net trading assets = assets − liabilities (the
    source's own netting, PDF p. 225), held flat over the horizon (PID-TRD-3,
    reference-observed).

    A zero net breaks the ratio and the calibration divisor; a NEGATIVE net
    trading book has no user-directed treatment yet (chapter §12 — the WLS
    weighting context treats net trading assets as a magnitude). Both surface
    as hard failures, never defaulted."""

    firm_id: str
    trading_assets_avg_balance: float
    trading_liabilities_avg_balance: float

    def __post_init__(self) -> None:
        require_id("firm_id", self.firm_id)
        object.__setattr__(
            self, "trading_assets_avg_balance",
            check_balance("trading_assets_avg_balance", self.trading_assets_avg_balance),
        )
        object.__setattr__(
            self, "trading_liabilities_avg_balance",
            check_balance("trading_liabilities_avg_balance", self.trading_liabilities_avg_balance),
        )
        net = self.trading_assets_avg_balance - self.trading_liabilities_avg_balance
        if net <= 0.0:
            raise ValidationFailure(
                f"net trading assets = {net} (trading assets {self.trading_assets_avg_balance} "
                f"− trading liabilities {self.trading_liabilities_avg_balance}) — must be > 0: "
                f"zero breaks the ratio and the calibration divisor, and a negative net trading "
                f"book has no user-directed treatment yet (nii_trading_al chapter §12); "
                f"surfaced, never defaulted"
            )

    @property
    def net_trading_assets(self) -> float:
        """NetTA(b,0) — the Eq A52 denominator and the projection multiplicand."""
        return self.trading_assets_avg_balance - self.trading_liabilities_avg_balance


@dataclass(frozen=True)
class TradingNiiParams:
    """Table A9 (PDF p. 234) Eq A52 coefficient. alpha_b is NOT a member: it is
    calibrated per firm (PID-TRD-1/PID-TRD-3), never a published value. The
    reference workbook sources beta from an FRB-provided coefficients input,
    observed equal to the published 0.278 (PID-TRD-2) — a divergence between
    the two must surface, never be absorbed."""

    beta_treasury3m: float = 0.278

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "beta_treasury3m",
            check_finite("beta_treasury3m", self.beta_treasury3m),
        )


TABLE_A9_TRADING = TradingNiiParams()


@dataclass(frozen=True)
class DepBanksOtherQuarterDiagnostics:
    balance: float
    usd_3m_treasury: float


@dataclass(frozen=True)
class OtherIdaQuarterDiagnostics:
    total_balance: float
    short_rate_share: float
    usd_3m_treasury: float
    usd_10y_treasury: float
    blended_rate: float                  # α·T3m + (1−α)·T10y — chapter §5 [CODE] restatement
    short_leg_income: float              # α·B·T3m/4  (diagnostic; legs sum ≈ quarterly_income)
    long_leg_income: float               # (1−α)·B·T10y/4


@dataclass(frozen=True)
class TradingQuarterDiagnostics:
    usd_3m_treasury: float
    pre_alpha_rate: float                # beta * T3m(q) — annualized (PID-TRD-3 basis)
    alpha_b: float
    net_trading_assets: float
    implied_income: float                # FRBIncome(q) − Σ six sibling incomes
    modeled_income: float
    quarterly_difference: float          # modeled − implied (sums to ~0 over PQ1..PQ9)


# ---------------------------------------------------------------------------
# Results
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class IncomeQuarterResult:
    """One projection quarter of an income model.

    `annualized_rate`/`average_balance` are None when the model has no single
    balance × rate decomposition (the securities three-term template, Increment 2);
    the true decomposition then lives in the typed diagnostics. `quarterly_income`
    carries no sign constraint — negative values are legal (rate-driven sign flips
    are logged by the models; trading NII is a net item)."""

    quarter: int
    annualized_rate: float | None
    average_balance: float | None
    quarterly_income: float
    diagnostics: Any


@dataclass(frozen=True)
class IncomeModelResult:
    """Standardized per-model output: exactly nine ordered projection quarters.

    Hard failures raise ValidationFailure instead of producing a result;
    log-never-clamp events land in `warnings` (conventions §6)."""

    model_id: str
    firm_id: str
    scenario_id: str
    quarters: tuple[IncomeQuarterResult, ...]
    validation_status: str               # "passed" | "passed_with_warnings"
    warnings: tuple[str, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "quarters", tuple(self.quarters))
        object.__setattr__(self, "warnings", tuple(str(w) for w in self.warnings))
        got = tuple(q.quarter for q in self.quarters)
        if got != PROJECTION_QUARTERS:
            raise ValidationFailure(
                f"{self.model_id}: results must cover exactly PQ1..PQ9 in order, got {list(got)}"
            )

    def income_path(self) -> Mapping[int, float]:
        return MappingProxyType({q.quarter: q.quarterly_income for q in self.quarters})

    def rate_path(self) -> Mapping[int, float | None]:
        return MappingProxyType({q.quarter: q.annualized_rate for q in self.quarters})

    @property
    def cumulative_income(self) -> float:
        return sum(q.quarterly_income for q in self.quarters)


# ---------------------------------------------------------------------------
# Trading-NII calibration record (PID-TRD-1/PID-TRD-3) — parallels the verified
# expense-side AlphaCalibration deliberately; separate class, never shared.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class TradingAlphaCalibration:
    """PID-TRD-1 calibration record under the PID-TRD-3 annualized basis: the
    closed-form alpha_b (an annualized intercept) plus both quarterly paths and
    their differences, preserved for diagnostics even though only the
    nine-quarter cumulative is matched — the reference trading tab itself
    carries all three rows plus the average of the differences (observed)."""

    alpha_b: float
    balance_sum: float
    implied_path: Mapping[int, float]
    pre_alpha_rate_path: Mapping[int, float]
    modeled_path: Mapping[int, float]
    quarterly_difference_path: Mapping[int, float]   # modeled - implied
    cumulative_implied: float
    cumulative_modeled: float
    cumulative_difference: float
    warnings: tuple[str, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "warnings", tuple(str(w) for w in self.warnings))


# ---------------------------------------------------------------------------
# Family bundle (grows per increment)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class IncomeFamilyInputs:
    """Canonical income-side inputs for one firm × one scenario run.

    Increment 1 carries the two Family A calculators. Increment 4 adds the
    optional trading-NII inputs (PID-TRD-2) and the FRB family paths
    (`frb_total_interest_income` — the PID-TRD-1 calibration target — and
    `frb_net_interest_income` for the combined-NII monitor). All three stay
    optional here so calculator-only runs remain valid; the income orchestrator
    requires the trading inputs and the income path at run time. Sign
    convention (D-008): income and NII paths pass through as-entered."""

    firm_id: str
    dep_banks_other: DepBanksOtherInputs
    other_ida: OtherIdaInputs
    trading: TradingNiiInputs | None = None
    frb_total_interest_income: Mapping[int, float] | None = None
    frb_net_interest_income: Mapping[int, float] | None = None

    def __post_init__(self) -> None:
        require_id("firm_id", self.firm_id)
        for field_name in ("dep_banks_other", "other_ida"):
            model_inputs = getattr(self, field_name)
            if model_inputs.firm_id != self.firm_id:
                raise ValidationFailure(
                    f"{field_name}.firm_id = {model_inputs.firm_id!r} does not match family firm_id = {self.firm_id!r}"
                )
        if self.trading is not None and self.trading.firm_id != self.firm_id:
            raise ValidationFailure(
                f"trading.firm_id = {self.trading.firm_id!r} does not match family firm_id = {self.firm_id!r}"
            )
        for optional_name in ("frb_total_interest_income", "frb_net_interest_income"):
            value = getattr(self, optional_name)
            if value is not None:
                object.__setattr__(
                    self, optional_name, freeze_path(optional_name, value, PROJECTION_QUARTERS)
                )


# ---------------------------------------------------------------------------
# Family result (Increment 4) — parallels the verified expense-side shapes.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class IncomeFamilyReconciliation:
    """Income-family reconciliation: the six sibling components plus the trading
    NII against the FRB total-interest-income path. Exact by construction
    (PID-TRD-1) up to float tolerance; per-quarter differences are diagnostics
    and need not be zero."""

    frb_total_cumulative: float
    components_cumulative: Mapping[str, float]
    components_total_cumulative: float
    cumulative_difference: float
    per_quarter_difference: Mapping[int, float]
    tolerance: float
    within_tolerance: bool


@dataclass(frozen=True)
class IncomeFamilyResult:
    """One firm × one scenario income-family run: the six supplied sibling paths
    (results-level composition — loans and securities run from their own
    workbook loaders), the trading-NII result and calibration, and the family
    reconciliation to the FRB income path."""

    firm_id: str
    scenario_id: str
    sibling_paths: Mapping[str, Mapping[int, float]]
    trading_result: IncomeModelResult
    calibration: TradingAlphaCalibration
    reconciliation: IncomeFamilyReconciliation
    warnings: tuple[str, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "warnings", tuple(str(w) for w in self.warnings))
        object.__setattr__(
            self,
            "sibling_paths",
            MappingProxyType(
                {
                    model_id: freeze_path(f"sibling_paths[{model_id}]", path, PROJECTION_QUARTERS)
                    for model_id, path in dict(self.sibling_paths).items()
                }
            ),
        )

    def total_income_path(self) -> Mapping[int, float]:
        """Σ six sibling incomes + trading NII per quarter — the family total."""
        trading = self.trading_result.income_path()
        return MappingProxyType(
            {
                q: sum(path[q] for path in self.sibling_paths.values()) + trading[q]
                for q in PROJECTION_QUARTERS
            }
        )

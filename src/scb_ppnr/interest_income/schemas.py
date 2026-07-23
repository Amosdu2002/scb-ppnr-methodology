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

    All four family series are required from day one (mirrors the expense
    precedent) even though Family A consumes only the two Treasury series.
    `usd_3m_treasury` includes PQ0 — required by the securities floating-margin
    imputation, which uses the t = 0 **spot** 3-month Treasury (Increment 2);
    the calculators read PQ1..PQ9 only. Pre-PQ0 history never enters this
    container (the Eq A37 wholesale spread anchors are supplied launch-point
    firm inputs — asset conventions §5)."""

    scenario_id: str
    usd_3m_treasury: Mapping[int, float]
    usd_10y_treasury: Mapping[int, float]
    prime_rate: Mapping[int, float]
    mortgage_rate: Mapping[int, float]

    def __post_init__(self) -> None:
        require_id("scenario_id", self.scenario_id)
        object.__setattr__(
            self, "usd_3m_treasury",
            freeze_path("usd_3m_treasury", self.usd_3m_treasury, SCENARIO_QUARTERS_WITH_LAUNCH, check_rate),
        )
        for name in ("usd_10y_treasury", "prime_rate", "mortgage_rate"):
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
# Family bundle (grows per increment)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class IncomeFamilyInputs:
    """Canonical income-side inputs for one firm × one scenario run.

    Increment 1 carries the two Family A calculators; later increments add the
    securities, loans, and trading-NII inputs plus the `frb_total_interest_income`
    monitor target (already ingested on the expense-side FamilyInputs as an
    optional companion — it moves to a required role only at Increment 4)."""

    firm_id: str
    dep_banks_other: DepBanksOtherInputs
    other_ida: OtherIdaInputs

    def __post_init__(self) -> None:
        require_id("firm_id", self.firm_id)
        for field_name in ("dep_banks_other", "other_ida"):
            model_inputs = getattr(self, field_name)
            if model_inputs.firm_id != self.firm_id:
                raise ValidationFailure(
                    f"{field_name}.firm_id = {model_inputs.firm_id!r} does not match family firm_id = {self.firm_id!r}"
                )

"""Canonical input and result contracts for the five proposed 2026 interest-expense models.

Canonical units (conventions chapter §2–§3; decision D-004): monetary balances in USD;
every rate, spread, and beta an annualized decimal rate; projection horizon PQ1..PQ9 with
PQ0 the launch point. Percent→decimal normalization belongs at the ingestion boundary,
upstream of these types — a rate magnitude >= RATE_SCALE_GUARD is rejected as
percent-scale leakage rather than silently reinterpreted.

These types are the boundary between data retrieval and model calculation (conventions
§5): model functions accept them and never know whether values came from an Excel
worksheet, an MDRM lookup, a CSV, a database, or a synthetic test fixture.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Mapping

PROJECTION_QUARTERS: tuple[int, ...] = (1, 2, 3, 4, 5, 6, 7, 8, 9)
LAUNCH_QUARTER: int = 0
SCENARIO_QUARTERS_WITH_LAUNCH: tuple[int, ...] = (LAUNCH_QUARTER, *PROJECTION_QUARTERS)

# A "rate" at or beyond this magnitude is treated as percent-scale leakage
# (e.g. 4.25 passed where 0.0425 was meant) and rejected at the canonical boundary.
RATE_SCALE_GUARD: float = 0.5

OTHER_DOM_SUBCOMPONENTS: tuple[str, ...] = ("mma", "savings", "transaction")
FOREIGN_SUBCOMPONENTS: tuple[str, ...] = ("foreign_nontime", "foreign_time")


class ValidationFailure(ValueError):
    """Contract violation on canonical inputs or a calculation invariant.

    Never caught to substitute a fallback value — failures surface, nothing
    defaults silently (conventions §6)."""


def _finite(name: str, value: Any) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValidationFailure(f"{name} must be a number, got {value!r}")
    v = float(value)
    if not math.isfinite(v):
        raise ValidationFailure(f"{name} must be finite, got {value!r}")
    return v


def check_rate(name: str, value: Any) -> float:
    v = _finite(name, value)
    if abs(v) >= RATE_SCALE_GUARD:
        raise ValidationFailure(
            f"{name} = {v} looks percent-scaled; canonical rates are annualized decimals "
            f"(|rate| < {RATE_SCALE_GUARD}). Normalize percent vs decimal at the ingestion "
            f"boundary, never inside the models."
        )
    return v


def check_balance(name: str, value: Any) -> float:
    v = _finite(name, value)
    if v < 0.0:
        raise ValidationFailure(f"{name} must be >= 0 USD, got {v}")
    return v


def check_share(name: str, value: Any) -> float:
    v = _finite(name, value)
    if not 0.0 <= v <= 1.0:
        raise ValidationFailure(f"{name} must lie in [0, 1], got {v}")
    return v


def freeze_path(
    name: str,
    values: Mapping[int, Any],
    quarters: tuple[int, ...],
    check=_finite,
) -> Mapping[int, float]:
    """Validate and defensively copy a quarter→value mapping.

    The mapping must cover exactly `quarters` (no gaps, no extras); each value is
    validated by `check`. Returns a read-only view over a fresh dict in quarter
    order, so the caller's mapping is never aliased or mutated."""
    if not isinstance(values, Mapping):
        raise ValidationFailure(f"{name} must be a mapping of quarter -> value, got {type(values).__name__}")
    got = set(values.keys())
    expected = set(quarters)
    if got != expected:
        missing = sorted(expected - got)
        extra = sorted(q for q in got if q not in expected)
        raise ValidationFailure(
            f"{name} must cover exactly quarters {list(quarters)}; missing {missing}, unexpected {extra}"
        )
    return MappingProxyType({q: check(f"{name}[PQ{q}]", values[q]) for q in quarters})


def _require_id(name: str, value: Any) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValidationFailure(f"{name} must be a non-empty string, got {value!r}")


# ---------------------------------------------------------------------------
# Scenario inputs
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ScenarioPaths:
    """Scenario MEV paths in canonical names (conventions §2).

    `usd_3m_treasury` includes PQ0 — required only by the A46 ΔTreasury3m seed at
    t=1 in the two deposit-beta models (OQ-018). `ie_dom_time_dep` seeds from firm
    data; `ie_fed_funds_repo` and `ie_other_borrowing` consume no PQ0 value (PID-OB-5)."""

    scenario_id: str
    usd_3m_treasury: Mapping[int, float]
    usd_1y_treasury: Mapping[int, float]
    bbb_corporate_yield: Mapping[int, float]

    def __post_init__(self) -> None:
        _require_id("scenario_id", self.scenario_id)
        object.__setattr__(
            self, "usd_3m_treasury",
            freeze_path("usd_3m_treasury", self.usd_3m_treasury, SCENARIO_QUARTERS_WITH_LAUNCH, check_rate),
        )
        object.__setattr__(
            self, "usd_1y_treasury",
            freeze_path("usd_1y_treasury", self.usd_1y_treasury, PROJECTION_QUARTERS, check_rate),
        )
        object.__setattr__(
            self, "bbb_corporate_yield",
            freeze_path("bbb_corporate_yield", self.bbb_corporate_yield, PROJECTION_QUARTERS, check_rate),
        )


# ---------------------------------------------------------------------------
# Per-model firm inputs
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class DomTimeDepInputs:
    """ie_dom_time_dep firm inputs: item 42E seed rate, item 71 WAL in months
    (PID-3), item 34E balance held flat (PID-1)."""

    firm_id: str
    rate_launchpoint: float
    wal_months: float
    balance: float

    def __post_init__(self) -> None:
        _require_id("firm_id", self.firm_id)
        object.__setattr__(self, "rate_launchpoint", check_rate("rate_launchpoint", self.rate_launchpoint))
        wal = _finite("wal_months", self.wal_months)
        if wal <= 0.0:
            raise ValidationFailure(f"wal_months must be > 0, got {wal}")
        object.__setattr__(self, "wal_months", wal)
        object.__setattr__(self, "balance", check_balance("balance", self.balance))


@dataclass(frozen=True)
class DepositSubcomponent:
    """One deposit subcomponent i: seed rate (OQ-018), A47 weight balance, and the
    supplied ELB spread — the OQ-017 spread *derivation* is out of scope, so the
    value arrives as a canonical input."""

    rate_launchpoint: float
    balance: float
    elb_spread: float

    def __post_init__(self) -> None:
        object.__setattr__(self, "rate_launchpoint", check_rate("rate_launchpoint", self.rate_launchpoint))
        object.__setattr__(self, "balance", check_balance("balance", self.balance))
        object.__setattr__(self, "elb_spread", check_rate("elb_spread", self.elb_spread))


def _freeze_subcomponents(
    name: str,
    values: Mapping[str, DepositSubcomponent],
    expected: tuple[str, ...],
) -> Mapping[str, DepositSubcomponent]:
    if not isinstance(values, Mapping):
        raise ValidationFailure(f"{name} must be a mapping of subcomponent -> DepositSubcomponent")
    if set(values.keys()) != set(expected):
        raise ValidationFailure(f"{name} must have exactly subcomponents {list(expected)}, got {sorted(values.keys())}")
    for key, sub in values.items():
        if not isinstance(sub, DepositSubcomponent):
            raise ValidationFailure(f"{name}[{key!r}] must be a DepositSubcomponent, got {type(sub).__name__}")
    return MappingProxyType({key: values[key] for key in expected})


@dataclass(frozen=True)
class OtherDomDepInputs:
    """ie_other_dom_dep firm inputs. The A47 weights (subcomponent balances,
    PID-ODD-1) and the expense multiplicand `total_average_balance` (PID-ODD-2)
    deliberately come from different physical sources — a consistency monitor,
    never an identity."""

    firm_id: str
    subcomponents: Mapping[str, DepositSubcomponent]
    total_average_balance: float

    def __post_init__(self) -> None:
        _require_id("firm_id", self.firm_id)
        object.__setattr__(
            self, "subcomponents",
            _freeze_subcomponents("subcomponents", self.subcomponents, OTHER_DOM_SUBCOMPONENTS),
        )
        object.__setattr__(
            self, "total_average_balance", check_balance("total_average_balance", self.total_average_balance)
        )


@dataclass(frozen=True)
class ForeignDepInputs:
    """ie_foreign_dep firm inputs (items 35A/35B). Unlike ie_other_dom_dep, the
    same subcomponent balances serve as both the A47 weights and, summed, the
    expense multiplicand (INT-a)."""

    firm_id: str
    subcomponents: Mapping[str, DepositSubcomponent]

    def __post_init__(self) -> None:
        _require_id("firm_id", self.firm_id)
        object.__setattr__(
            self, "subcomponents",
            _freeze_subcomponents("subcomponents", self.subcomponents, FOREIGN_SUBCOMPONENTS),
        )


@dataclass(frozen=True)
class FedFundsRepoInputs:
    """ie_fed_funds_repo firm inputs: items 36A + 36B (PID-FFR-1), held flat."""

    firm_id: str
    fed_funds_purchased_balance: float
    repo_sold_balance: float

    def __post_init__(self) -> None:
        _require_id("firm_id", self.firm_id)
        object.__setattr__(
            self, "fed_funds_purchased_balance",
            check_balance("fed_funds_purchased_balance", self.fed_funds_purchased_balance),
        )
        object.__setattr__(self, "repo_sold_balance", check_balance("repo_sold_balance", self.repo_sold_balance))


@dataclass(frozen=True)
class OtherBorrowingInputs:
    """ie_other_borrowing firm inputs: total balance (Schedule G 36C+38+39 physical
    mapping, PID-OB-2) and the two PQ0-frozen composition shares. There is no PQ0
    actual-expense input — PID-OB-5 never uses one."""

    firm_id: str
    total_balance: float
    cp_share: float
    subdebt_share: float

    def __post_init__(self) -> None:
        _require_id("firm_id", self.firm_id)
        bal = _finite("total_balance", self.total_balance)
        if bal <= 0.0:
            raise ValidationFailure(
                f"total_balance must be > 0 USD (zero also breaks the share denominators), got {bal}"
            )
        object.__setattr__(self, "total_balance", bal)
        object.__setattr__(self, "cp_share", check_share("cp_share", self.cp_share))
        object.__setattr__(self, "subdebt_share", check_share("subdebt_share", self.subdebt_share))
        if self.cp_share + self.subdebt_share > 1.0:
            raise ValidationFailure(
                f"cp_share + subdebt_share = {self.cp_share + self.subdebt_share} exceeds 1 "
                f"(possible under the mixed Y-9C/Schedule G form, OQ-022) — surfaced, never clipped"
            )


# ---------------------------------------------------------------------------
# Published / supplied parameters
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class DepositBetaParams:
    """Table A7 median betas per subcomponent and direction, plus the 25 bp ELB
    threshold (expressed in the normalized decimal scale)."""

    beta_up: Mapping[str, float]
    beta_down: Mapping[str, float]
    elb_threshold: float = 0.0025

    def __post_init__(self) -> None:
        if set(self.beta_up.keys()) != set(self.beta_down.keys()):
            raise ValidationFailure("beta_up and beta_down must cover the same subcomponents")
        object.__setattr__(
            self, "beta_up", MappingProxyType({k: _finite(f"beta_up[{k}]", v) for k, v in self.beta_up.items()})
        )
        object.__setattr__(
            self, "beta_down", MappingProxyType({k: _finite(f"beta_down[{k}]", v) for k, v in self.beta_down.items()})
        )
        thr = _finite("elb_threshold", self.elb_threshold)
        if not 0.0 < thr < RATE_SCALE_GUARD:
            raise ValidationFailure(f"elb_threshold must be a positive decimal rate, got {thr}")
        object.__setattr__(self, "elb_threshold", thr)


# Table A7 (PDF p. 219) — verified values; significance/labels are metadata elsewhere.
TABLE_A7_OTHER_DOM = DepositBetaParams(
    beta_up={"mma": 0.620, "savings": 0.310, "transaction": 0.465},
    beta_down={"mma": 0.645, "savings": 0.335, "transaction": 0.490},
)
TABLE_A7_FOREIGN = DepositBetaParams(
    beta_up={"foreign_nontime": 0.890, "foreign_time": 1.000},
    beta_down={"foreign_nontime": 0.790, "foreign_time": 1.000},
)


@dataclass(frozen=True)
class OtherBorrowingParams:
    """Table A9 (PDF p. 234) Eq A53(2) coefficients. The 3-month Treasury enters
    Eq A53(1) with coefficient 1 by construction and has no entry here. alpha_b is
    NOT a member: it is calibrated per firm (PID-OB-5), never a published value."""

    beta_bbb: float = 0.254
    beta_cp: float = -0.036
    beta_subdebt: float = 0.066

    def __post_init__(self) -> None:
        for name in ("beta_bbb", "beta_cp", "beta_subdebt"):
            object.__setattr__(self, name, _finite(name, getattr(self, name)))


TABLE_A9_OTHER_BORROWING = OtherBorrowingParams()


# ---------------------------------------------------------------------------
# Per-model quarter diagnostics (traceability intermediates)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class DomTimeDepQuarterDiagnostics:
    wal_months: float
    wal_quarters: float
    rho: float
    previous_rate: float
    usd_1y_treasury: float


@dataclass(frozen=True)
class DepositSubcomponentDiagnostics:
    regime: str                          # "elb" | "non_elb"
    beta_applied: float | None           # None in ELB quarters; 0.0 when ΔT3m == 0
    market_rate_change: float | None     # ΔTreasury3m(t); None in ELB quarters
    elb_spread: float
    assumed_floor: float
    floor_binding: bool
    unfloored_rate: float | None         # None in ELB quarters
    rate: float
    weight_balance: float


@dataclass(frozen=True)
class DepositQuarterDiagnostics:
    usd_3m_treasury: float
    first_elb_treasury3m: float
    subcomponents: Mapping[str, DepositSubcomponentDiagnostics]
    aggregate_rate: float

    def __post_init__(self) -> None:
        object.__setattr__(self, "subcomponents", MappingProxyType(dict(self.subcomponents)))


@dataclass(frozen=True)
class FedFundsRepoQuarterDiagnostics:
    fed_funds_purchased_balance: float
    repo_sold_balance: float
    usd_3m_treasury: float


@dataclass(frozen=True)
class OtherBorrowingQuarterDiagnostics:
    usd_3m_treasury: float
    bbb_contribution: float              # beta_bbb * BBB(q)
    cp_share_contribution: float         # beta_cp * CPShare(b,0)
    subdebt_share_contribution: float    # beta_subdebt * SubdebtShare(b,0)
    pre_alpha_rate: float
    alpha_b: float
    implied_expense: float
    modeled_expense: float
    quarterly_difference: float          # modeled - implied (sums to ~0 over PQ1..PQ9)


# ---------------------------------------------------------------------------
# Results
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class QuarterResult:
    quarter: int
    annualized_rate: float
    average_balance: float
    quarterly_expense: float
    diagnostics: Any


@dataclass(frozen=True)
class ModelResult:
    """Standardized per-model output: exactly nine ordered projection quarters.

    Hard failures raise ValidationFailure instead of producing a result;
    log-never-clamp events land in `warnings` (conventions §6)."""

    model_id: str
    firm_id: str
    scenario_id: str
    quarters: tuple[QuarterResult, ...]
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

    def expense_path(self) -> Mapping[int, float]:
        return MappingProxyType({q.quarter: q.quarterly_expense for q in self.quarters})

    def rate_path(self) -> Mapping[int, float]:
        return MappingProxyType({q.quarter: q.annualized_rate for q in self.quarters})

    @property
    def cumulative_expense(self) -> float:
        return sum(q.quarterly_expense for q in self.quarters)


@dataclass(frozen=True)
class AlphaCalibration:
    """PID-OB-5 calibration record: the closed-form alpha_b plus both quarterly
    paths and their differences, preserved for diagnostics even though only the
    nine-quarter cumulative is matched."""

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


@dataclass(frozen=True)
class FamilyInputs:
    """Canonical inputs for one firm × one scenario family run, including the
    project-supplied FRB total-interest-expense path (PID-OB-5; source OQ-023)."""

    firm_id: str
    dom_time_dep: DomTimeDepInputs
    other_dom_dep: OtherDomDepInputs
    foreign_dep: ForeignDepInputs
    fed_funds_repo: FedFundsRepoInputs
    other_borrowing: OtherBorrowingInputs
    frb_total_interest_expense: Mapping[int, float]

    def __post_init__(self) -> None:
        _require_id("firm_id", self.firm_id)
        for field_name in ("dom_time_dep", "other_dom_dep", "foreign_dep", "fed_funds_repo", "other_borrowing"):
            model_inputs = getattr(self, field_name)
            if model_inputs.firm_id != self.firm_id:
                raise ValidationFailure(
                    f"{field_name}.firm_id = {model_inputs.firm_id!r} does not match family firm_id = {self.firm_id!r}"
                )
        object.__setattr__(
            self, "frb_total_interest_expense",
            freeze_path("frb_total_interest_expense", self.frb_total_interest_expense, PROJECTION_QUARTERS),
        )


@dataclass(frozen=True)
class FamilyReconciliation:
    """Step-8 reconciliation: the five components' nine-quarter cumulative expense
    against the FRB total. Exact by construction (PID-OB-5) up to float tolerance;
    per-quarter differences are diagnostics and need not be zero."""

    frb_total_cumulative: float
    components_cumulative: Mapping[str, float]
    components_total_cumulative: float
    cumulative_difference: float
    per_quarter_difference: Mapping[int, float]
    tolerance: float
    within_tolerance: bool


@dataclass(frozen=True)
class FamilyResult:
    firm_id: str
    scenario_id: str
    results: Mapping[str, ModelResult]
    calibration: AlphaCalibration
    reconciliation: FamilyReconciliation
    warnings: tuple[str, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "results", MappingProxyType(dict(self.results)))
        object.__setattr__(self, "warnings", tuple(str(w) for w in self.warnings))

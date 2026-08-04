"""Canonical containers for the Corporate wholesale loan model (`ii_loans`).

The Federal Reserve model these implement is PROPOSED for the 2026 stress test
(public-comment stage), NOT adopted. Fed methodology lives in the three loans
source briefs; every project decision below is a PID registered in
`handbook/open-questions.md` and specified in
`specifications/interest-income/loans/ii_loans_corporate.spec.md`.

Units are canonical at this boundary: rates are annualized decimals, money is
USD millions (D-006). Percent-vs-decimal and money scaling are resolved at
ingestion and never inside the model."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from types import MappingProxyType
from typing import Mapping

from ..core.schemas import ValidationFailure, check_balance, check_finite, check_rate, require_id

# --- Variable Type codes (PID-LOAN-2) -------------------------------------
# The CORP H.1 mapping's own vocabulary. There is NO demand-loan code, so the
# Fed's "demand loans are treated as variable-rate" rule (PDF p. 176) has no
# counterpart in this data — recorded as inapplicable, never invented.
VT_DO_NOT_USE = 0
VT_FIXED = 1
VT_FLOATING = 2
VT_MIXED = 3
VT_ENTRY_FEE = 4
VARIABLE_TYPES = (VT_DO_NOT_USE, VT_FIXED, VT_FLOATING, VT_MIXED, VT_ENTRY_FEE)

# --- Treatments (PID-LOAN-5) ----------------------------------------------
TREATMENT_NO_INCOME = "no_income"   # counts toward balance, earns nothing
TREATMENT_FIXED = "fixed"           # Equation A34/A38 blend
TREATMENT_VARIABLE = "variable"     # Equation A33

TREATMENT_BY_CODE: Mapping[int, str] = MappingProxyType({
    VT_DO_NOT_USE: TREATMENT_NO_INCOME,
    VT_FIXED: TREATMENT_FIXED,
    VT_FLOATING: TREATMENT_VARIABLE,
    VT_MIXED: TREATMENT_VARIABLE,   # the Fed treats mixed as variable-rate going forward
    VT_ENTRY_FEE: TREATMENT_NO_INCOME,
})

# --- Rate pools (PID-LOAN-3) ----------------------------------------------
# Mixed's exposures feed the FLOATING pool, while Mixed's own spread is built
# from the FIXED pool's rate (PID-LOAN-4). The two are deliberately different
# lookups, so they are named separately rather than derived from each other.
POOL_FLOAT = "float"
POOL_FIXED = "fixed"

POOL_MEMBERSHIP: Mapping[str, tuple[int, ...]] = MappingProxyType({
    POOL_FLOAT: (VT_FLOATING, VT_MIXED),
    POOL_FIXED: (VT_FIXED,),
})

# Which pool rate each rate type's spread is built from.
SPREAD_POOL_BY_CODE: Mapping[int, str] = MappingProxyType({
    VT_FIXED: POOL_FIXED,
    VT_FLOATING: POOL_FLOAT,
    VT_MIXED: POOL_FIXED,           # hybrid: priced in the past, projected as variable
})

# Whether the spread's base rate is the launch-point 3M or the rate type's own
# median origination quarter (PID-LOAN-4).
BASE_AT_LAUNCH_POINT = "launch_point"
BASE_AT_MEDIAN_ORIGINATION = "median_origination"

SPREAD_BASE_BY_CODE: Mapping[int, str] = MappingProxyType({
    VT_FIXED: BASE_AT_MEDIAN_ORIGINATION,
    VT_FLOATING: BASE_AT_LAUNCH_POINT,
    VT_MIXED: BASE_AT_MEDIAN_ORIGINATION,
})

# --- Floor collapse (PID-LOAN-7) ------------------------------------------
FLOOR_COLLAPSE_BALANCE_WEIGHTED = "balance_weighted"
FLOOR_COLLAPSE_MAX = "max"
FLOOR_COLLAPSE_MIN = "min"
FLOOR_COLLAPSES = (FLOOR_COLLAPSE_BALANCE_WEIGHTED, FLOOR_COLLAPSE_MAX, FLOOR_COLLAPSE_MIN)

# --- Exposure measures ----------------------------------------------------
# Two different columns for two different jobs, never conflated: rates are
# weighted by COMMITTED exposure while wt is built from UTILIZED exposure
# (PID-LOAN-3 / PID-LOAN-6, both user-specified).
EXPOSURE_COMMITTED = "committed"
EXPOSURE_UTILIZED = "utilized"
EXPOSURE_MEASURES = (EXPOSURE_COMMITTED, EXPOSURE_UTILIZED)

# Why a segment fell back to a zero base rate (PID-LOAN-4 amendment).
FALLBACK_OUTSIDE_MEV = "outside_mev_range"
FALLBACK_NO_ORIGINATION_DATE = "missing_origination_date"


def check_segment_share(name: str, value: float) -> float:
    """Shares are validated in [0, 1] and never clipped (asset conventions §8).

    A hair of tolerance above 1 absorbs float summation only; anything larger
    surfaces rather than being silently normalized."""
    v = check_finite(name, value)
    if not 0.0 <= v <= 1.0 + 1e-9:
        raise ValidationFailure(f"{name} must lie in [0, 1], got {v}")
    return v


def check_quarter_label(name: str, value: str) -> str:
    """Validate a historical quarter label of the form `YYYYQn`."""
    if not isinstance(value, str) or len(value) != 6 or value[4] != "Q":
        raise ValidationFailure(f"{name} must look like 'YYYYQn', got {value!r}")
    year, quarter = value[:4], value[5]
    if not year.isdigit() or quarter not in "1234":
        raise ValidationFailure(f"{name} must look like 'YYYYQn', got {value!r}")
    return value


def quarter_label(when: date) -> str:
    """Map an origination date to its calendar quarter (PID-LOAN-4).

    May 2022 -> '2022Q2'. The Fed's Equation A37 says only "the base rate from
    the median origination date (t-a)"; mapping the month to its quarter is the
    project's operationalization."""
    return f"{when.year}Q{(when.month - 1) // 3 + 1}"


@dataclass(frozen=True)
class SegmentKey:
    """The CORP H.1 three-part reference key (PID-LOAN-2).

    `locom` is the lower-of-cost-or-market flag, which is the physical
    realization of the Fed's HFI vs FVO/HFS asset classification (PDF p. 175)."""

    category: str          # Fed Category 1-11
    locom: str             # "HFI" | "HFS"
    variable_type: int     # 0-4

    def __post_init__(self) -> None:
        require_id("category", self.category)
        require_id("locom", self.locom)
        if self.variable_type not in VARIABLE_TYPES:
            raise ValidationFailure(
                f"segment {self.category}/{self.locom}: variable_type must be one of "
                f"{VARIABLE_TYPES}, got {self.variable_type!r} — an unmapped code is refused, "
                f"never defaulted, because the value vocabulary is only evidenced for 0-4"
            )

    @property
    def treatment(self) -> str:
        return TREATMENT_BY_CODE[self.variable_type]

    def __str__(self) -> str:
        return f"{self.category}/{self.locom}/v{self.variable_type}"


@dataclass(frozen=True)
class LoanFacility:
    """One CORP H.1 facility row in canonical units.

    `interest_rate` is None where the H.1 cell is NA or [NULL]; such a row leaves
    BOTH sides of the rate-pool average (PID-LOAN-3) while its balance remains a
    real exposure. `interest_rate_floor` is None for NA / [NULL] / NONE, which
    all mean no floor (PID-LOAN-7); a populated 0.0 is a genuine zero floor —
    the distinction PID-SEC-18 cost several diagnostic rounds to learn."""

    facility_id: str
    segment: SegmentKey
    committed_exposure: float
    utilized_exposure: float
    interest_rate: float | None = None
    interest_rate_floor: float | None = None
    origination_date: date | None = None
    maturity_date: date | None = None

    def __post_init__(self) -> None:
        require_id("facility_id", self.facility_id)
        check_balance(f"{self.facility_id}.committed_exposure", self.committed_exposure)
        check_balance(f"{self.facility_id}.utilized_exposure", self.utilized_exposure)
        if self.interest_rate is not None:
            check_rate(f"{self.facility_id}.interest_rate", self.interest_rate)
        if self.interest_rate_floor is not None:
            check_rate(f"{self.facility_id}.interest_rate_floor", self.interest_rate_floor)

    def exposure(self, measure: str) -> float:
        if measure == EXPOSURE_COMMITTED:
            return self.committed_exposure
        if measure == EXPOSURE_UTILIZED:
            return self.utilized_exposure
        raise ValidationFailure(f"exposure measure must be one of {EXPOSURE_MEASURES}, got {measure!r}")


@dataclass(frozen=True)
class PoolRate:
    """A balance-weighted launch-point rate for one pool of one category/LOCOM."""

    pool: str
    rate: float
    weight: float              # total exposure behind the average
    rows_used: int
    rows_dropped: int          # rows excluded for a missing interest rate
    exposure_dropped: float    # their exposure — a large silent dropout must be visible

    def __post_init__(self) -> None:
        check_rate(f"pool[{self.pool}].rate", self.rate)
        check_balance(f"pool[{self.pool}].weight", self.weight)


@dataclass(frozen=True)
class SegmentSpread:
    """A launch-point spread and the provenance of the base rate behind it."""

    segment: SegmentKey
    spread: float
    pool_rate: float
    base_rate: float
    base_quarter: str | None            # None when the base rate is the launch point
    base_rate_fallback: str | None = None   # FALLBACK_* when the base rate defaulted to 0

    def __post_init__(self) -> None:
        check_rate(f"{self.segment}.spread", self.spread)
        check_rate(f"{self.segment}.pool_rate", self.pool_rate)
        check_rate(f"{self.segment}.base_rate", self.base_rate)


@dataclass(frozen=True)
class SegmentLaunchPoint:
    """Everything the projection needs for one segment, fixed at PQ0."""

    segment: SegmentKey
    share: float                        # of the category's total exposure
    balance: float                      # share x M.1 category balance, USD millions
    spread: SegmentSpread | None        # None for the no-income rate types
    floor: float | None                 # collapsed to the segment; None = no floor
    floor_dispersion: float             # max - min across the segment's populated floors
    reorigination_weights: Mapping[int, float] = MappingProxyType({})   # PQ -> wt, fixed only

    def __post_init__(self) -> None:
        check_segment_share(f"{self.segment}.share", self.share)
        check_balance(f"{self.segment}.balance", self.balance)
        if self.floor is not None:
            check_rate(f"{self.segment}.floor", self.floor)

    @property
    def earns_income(self) -> bool:
        return self.segment.treatment != TREATMENT_NO_INCOME

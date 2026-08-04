"""Launch-point (PQ0) construction for Corporate wholesale loans.

Pure computation over canonical facilities — no I/O, no workbook knowledge. The
physical binding lives in ingestion; this module takes `LoanFacility` rows and
produces the per-segment quantities the projection consumes: pool rates,
spreads, shares, balances, collapsed floors and re-origination weights.

Every rule is a PID registered in `handbook/open-questions.md` and specified in
`specifications/interest-income/loans/ii_loans_corporate.spec.md`. The Federal
Reserve model is PROPOSED for the 2026 stress test, NOT adopted.

Diagnostics are first-class rather than an afterthought: several rules here can
be quietly wrong in ways that only show up as a small drift in a nine-quarter
total, so each one reports what it did."""

from __future__ import annotations

import statistics
from collections import defaultdict
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Iterable, Mapping, Sequence

from ..core.schemas import ValidationFailure
from .loans_schemas import (
    BASE_AT_LAUNCH_POINT,
    BASE_AT_MEDIAN_ORIGINATION,
    EXPOSURE_COMMITTED,
    EXPOSURE_UTILIZED,
    FALLBACK_NO_ORIGINATION_DATE,
    FALLBACK_OUTSIDE_MEV,
    FLOOR_COLLAPSE_BALANCE_WEIGHTED,
    FLOOR_COLLAPSE_MAX,
    FLOOR_COLLAPSE_MIN,
    FLOOR_COLLAPSES,
    POOL_MEMBERSHIP,
    SPREAD_BASE_BY_CODE,
    SPREAD_POOL_BY_CODE,
    TREATMENT_FIXED,
    TREATMENT_NO_INCOME,
    LoanFacility,
    PoolRate,
    SegmentKey,
    SegmentLaunchPoint,
    SegmentSpread,
    quarter_label,
)


@dataclass
class LaunchPointDiagnostics:
    """First-run visibility for the rules that can be silently wrong.

    Each list is a census, not a log line: the spec requires these on every run
    because a fallback that fires on a material segment moves the projection
    without failing anything."""

    base_rate_fallbacks: list[tuple[SegmentKey, str]] = field(default_factory=list)
    # (category, locom, pool, rows, exposure) — reported against the POOL, since a
    # pool spans two rate types and naming one of them would mislabel the other.
    rate_rows_dropped: list[tuple[str, str, str, int, float]] = field(default_factory=list)
    floor_dispersion: list[tuple[SegmentKey, float]] = field(default_factory=list)
    wt_over_one: list[tuple[SegmentKey, int, float]] = field(default_factory=list)
    empty_pools: list[tuple[str, str, str]] = field(default_factory=list)

    def render(self) -> str:
        lines = ["LAUNCH-POINT DIAGNOSTICS"]
        lines.append(f"  base-rate fallbacks to zero : {len(self.base_rate_fallbacks)}")
        for segment, cause in self.base_rate_fallbacks:
            lines.append(f"      {segment}  cause={cause}")
        lines.append(f"  rows dropped from rate pools: {len(self.rate_rows_dropped)} pools")
        for category, locom, pool, rows, exposure in self.rate_rows_dropped:
            lines.append(f"      {category}/{locom} pool={pool}  rows={rows}  exposure={exposure:,.2f}")
        lines.append(f"  floors collapsed with spread: {len(self.floor_dispersion)} segments")
        for segment, spread in self.floor_dispersion:
            lines.append(f"      {segment}  max-min={spread:.4%}")
        lines.append(f"  wt > 1 (Eq A38 non-convex)  : {len(self.wt_over_one)}")
        for segment, quarter, value in self.wt_over_one:
            lines.append(f"      {segment}  PQ{quarter}  wt={value:.4f}")
        lines.append(f"  empty pools                 : {len(self.empty_pools)}")
        for category, locom, pool in self.empty_pools:
            lines.append(f"      {category}/{locom}  pool={pool}")
        return "\n".join(lines)


def _pool_of(category: str, locom: str) -> tuple[str, str]:
    return (category, locom)


def compute_pool_rates(
    facilities: Iterable[LoanFacility],
    diagnostics: LaunchPointDiagnostics | None = None,
) -> Mapping[tuple[str, str, str], PoolRate]:
    """Balance-weighted launch-point rates per category x LOCOM x pool (PID-LOAN-3).

    The Floating pool is Floating + Mixed; the Fixed pool is Fixed alone. Weights
    are COMMITTED exposure. A row whose interest rate is missing leaves BOTH the
    numerator and the denominator — leaving it in the denominator would drag the
    average toward zero, which is the failure mode this rule exists to prevent.
    """
    numerators: dict[tuple[str, str, str], float] = defaultdict(float)
    denominators: dict[tuple[str, str, str], float] = defaultdict(float)
    used: dict[tuple[str, str, str], int] = defaultdict(int)
    dropped: dict[tuple[str, str, str], int] = defaultdict(int)
    dropped_exposure: dict[tuple[str, str, str], float] = defaultdict(float)

    for facility in facilities:
        segment = facility.segment
        for pool, codes in POOL_MEMBERSHIP.items():
            if segment.variable_type not in codes:
                continue
            key = (segment.category, segment.locom, pool)
            exposure = facility.exposure(EXPOSURE_COMMITTED)
            if facility.interest_rate is None:
                dropped[key] += 1
                dropped_exposure[key] += exposure
                continue
            numerators[key] += exposure * facility.interest_rate
            denominators[key] += exposure
            used[key] += 1

    rates: dict[tuple[str, str, str], PoolRate] = {}
    for key in set(numerators) | set(dropped):
        weight = denominators.get(key, 0.0)
        if weight <= 0.0:
            if diagnostics is not None:
                diagnostics.empty_pools.append((key[0], key[1], key[2]))
            continue
        rates[key] = PoolRate(
            pool=key[2],
            rate=numerators[key] / weight,
            weight=weight,
            rows_used=used.get(key, 0),
            rows_dropped=dropped.get(key, 0),
            exposure_dropped=dropped_exposure.get(key, 0.0),
        )
    return MappingProxyType(rates)


def median_origination_quarter(facilities: Sequence[LoanFacility]) -> str | None:
    """The median origination date of a rate type, mapped to its calendar quarter.

    `statistics.median_low` returns an actually observed date rather than an
    interpolated one, so the quarter is always a quarter some loan was really
    originated in. The Fed states only "the median origination date (t-a) for
    that portfolio" (PDF p. 182) — the row-unweighted reading is the plain one,
    and the choice is recorded rather than assumed away."""
    dates = [f.origination_date for f in facilities if f.origination_date is not None]
    if not dates:
        return None
    return quarter_label(statistics.median_low(dates))


def resolve_base_rate(
    segment: SegmentKey,
    facilities: Sequence[LoanFacility],
    launch_point_3m: float,
    historical_3m: Mapping[str, float],
    diagnostics: LaunchPointDiagnostics | None = None,
) -> tuple[float, str | None, str | None]:
    """The base rate a segment's spread is measured against (PID-LOAN-4).

    Floating uses the launch-point 3M. Fixed and Mixed use the 3M of their own
    median origination quarter. Where that lookup misses, the base rate is 0 per
    the user-directed amendment of 2026-08-03 — which is NOT neutral: the spread
    then collapses to the full pool rate, so the segment's new-origination rate
    becomes 3M(t) + pool rate, overstated by the omitted base-rate level. Hence
    the census: cause is recorded so a data-quality problem in the origination
    dates is distinguishable from a genuine gap in the rate history."""
    basis = SPREAD_BASE_BY_CODE.get(segment.variable_type)
    if basis == BASE_AT_LAUNCH_POINT:
        return launch_point_3m, None, None
    if basis != BASE_AT_MEDIAN_ORIGINATION:
        raise ValidationFailure(f"{segment}: no spread basis is defined for variable_type {segment.variable_type}")

    quarter = median_origination_quarter(facilities)
    if quarter is None:
        if diagnostics is not None:
            diagnostics.base_rate_fallbacks.append((segment, FALLBACK_NO_ORIGINATION_DATE))
        return 0.0, None, FALLBACK_NO_ORIGINATION_DATE
    if quarter not in historical_3m:
        if diagnostics is not None:
            diagnostics.base_rate_fallbacks.append((segment, FALLBACK_OUTSIDE_MEV))
        return 0.0, quarter, FALLBACK_OUTSIDE_MEV
    return historical_3m[quarter], quarter, None


def collapse_floor(
    facilities: Sequence[LoanFacility],
    mode: str = FLOOR_COLLAPSE_BALANCE_WEIGHTED,
    measure: str = EXPOSURE_COMMITTED,
) -> tuple[float | None, float]:
    """Collapse per-facility floors to one segment floor (PID-LOAN-7).

    CORP H.1 carries floors per facility while the model projects one rate per
    segment, so they must be collapsed. NA / [NULL] / NONE all mean no floor and
    are absent here; a populated 0.0 is a genuine zero floor and participates —
    the distinction PID-SEC-18 cost several diagnostic rounds to learn.

    Returns (floor, dispersion). Dispersion is max - min across the populated
    floors, reported so a segment averaging wildly different floors is visible
    instead of hiding behind its mean."""
    if mode not in FLOOR_COLLAPSES:
        raise ValidationFailure(f"floor collapse mode must be one of {FLOOR_COLLAPSES}, got {mode!r}")
    populated = [f for f in facilities if f.interest_rate_floor is not None]
    if not populated:
        return None, 0.0
    floors = [f.interest_rate_floor for f in populated]
    dispersion = max(floors) - min(floors)
    if mode == FLOOR_COLLAPSE_MAX:
        return max(floors), dispersion
    if mode == FLOOR_COLLAPSE_MIN:
        return min(floors), dispersion
    weight = sum(f.exposure(measure) for f in populated)
    if weight <= 0.0:
        return statistics.fmean(floors), dispersion
    return sum(f.exposure(measure) * f.interest_rate_floor for f in populated) / weight, dispersion


def compute_reorigination_weights(
    fixed_facilities: Sequence[LoanFacility],
    fixed_launch_balance: float,
    quarter_of_maturity,
    quarters: Sequence[int],
    segment: SegmentKey | None = None,
    diagnostics: LaunchPointDiagnostics | None = None,
) -> Mapping[int, float]:
    """The Equation A38 blend weight, from contractual maturities (PID-LOAN-6).

    wt(PQx) = utilized exposure of Fixed facilities maturing in PQx, divided by
    the launch-point Fixed balance. `quarter_of_maturity` maps a maturity date to
    a projection quarter or None if it falls outside the horizon — supplied by
    the caller so the projection calendar stays in one place.

    Divergence from the Fed, recorded not smoothed: the Board derives wt from
    "the default rate, prepayment rate, and maturity rate" (PDF p. 183); this
    uses maturity alone.

    A wt above 1 makes Equation A38 non-convex and (1 - wt) negative. It is
    surfaced, never clamped — a clamp would hide the data problem that caused it.
    """
    if fixed_launch_balance <= 0.0:
        return MappingProxyType({q: 0.0 for q in quarters})

    maturing: dict[int, float] = defaultdict(float)
    for facility in fixed_facilities:
        if facility.maturity_date is None:
            continue
        quarter = quarter_of_maturity(facility.maturity_date)
        if quarter is None:
            continue
        maturing[quarter] += facility.exposure(EXPOSURE_UTILIZED)

    weights: dict[int, float] = {}
    for quarter in quarters:
        value = maturing.get(quarter, 0.0) / fixed_launch_balance
        if value > 1.0 and diagnostics is not None and segment is not None:
            diagnostics.wt_over_one.append((segment, quarter, value))
        weights[quarter] = value
    return MappingProxyType(weights)


def build_launch_point(
    facilities: Iterable[LoanFacility],
    category_balances: Mapping[str, float],
    launch_point_3m: float,
    historical_3m: Mapping[str, float],
    quarters: Sequence[int],
    quarter_of_maturity,
    share_measure: str = EXPOSURE_COMMITTED,
    floor_collapse: str = FLOOR_COLLAPSE_BALANCE_WEIGHTED,
) -> tuple[Mapping[SegmentKey, SegmentLaunchPoint], LaunchPointDiagnostics]:
    """Assemble every segment's launch-point quantities.

    `category_balances` is the M.1 portfolio balance per Fed Category — the
    Equation A32 multiplicand. Segment shares are taken over the category's TOTAL
    exposure across all five rate types, so the no-income codes 0 and 4 dilute
    the income-earning segments exactly as PID-LOAN-5 specifies (a recorded
    divergence: the Fed excludes fee-only balances from that denominator, which
    means this treatment produces LOWER income than a literal reading)."""
    rows = list(facilities)
    diagnostics = LaunchPointDiagnostics()

    by_segment: dict[SegmentKey, list[LoanFacility]] = defaultdict(list)
    for facility in rows:
        by_segment[facility.segment].append(facility)

    category_exposure: dict[str, float] = defaultdict(float)
    for facility in rows:
        category_exposure[facility.segment.category] += facility.exposure(share_measure)

    pool_rates = compute_pool_rates(rows, diagnostics)
    for (category, locom, pool), rate in pool_rates.items():
        if rate.rows_dropped:
            diagnostics.rate_rows_dropped.append(
                (category, locom, pool, rate.rows_dropped, rate.exposure_dropped)
            )

    fixed_launch_balances: dict[tuple[str, str], float] = defaultdict(float)
    for facility in rows:
        if facility.segment.treatment == TREATMENT_FIXED:
            fixed_launch_balances[_pool_of(facility.segment.category, facility.segment.locom)] += (
                facility.exposure(EXPOSURE_UTILIZED)
            )

    result: dict[SegmentKey, SegmentLaunchPoint] = {}
    for segment, segment_rows in by_segment.items():
        total = category_exposure.get(segment.category, 0.0)
        exposure = sum(f.exposure(share_measure) for f in segment_rows)
        share = exposure / total if total > 0.0 else 0.0
        balance = share * category_balances.get(segment.category, 0.0)

        spread: SegmentSpread | None = None
        if segment.treatment != TREATMENT_NO_INCOME:
            pool = SPREAD_POOL_BY_CODE[segment.variable_type]
            pool_rate = pool_rates.get((segment.category, segment.locom, pool))
            if pool_rate is None:
                raise ValidationFailure(
                    f"{segment}: the {pool!r} pool for {segment.category}/{segment.locom} has no "
                    f"usable interest rates, so no spread can be formed. Surfaced rather than "
                    f"defaulted — a zero spread here would silently reprice the whole segment."
                )
            base, base_quarter, fallback = resolve_base_rate(
                segment, segment_rows, launch_point_3m, historical_3m, diagnostics
            )
            spread = SegmentSpread(
                segment=segment,
                spread=pool_rate.rate - base,
                pool_rate=pool_rate.rate,
                base_rate=base,
                base_quarter=base_quarter,
                base_rate_fallback=fallback,
            )

        floor, dispersion = collapse_floor(segment_rows, floor_collapse, share_measure)
        if dispersion > 0.0:
            diagnostics.floor_dispersion.append((segment, dispersion))

        weights: Mapping[int, float] = MappingProxyType({})
        if segment.treatment == TREATMENT_FIXED:
            weights = compute_reorigination_weights(
                segment_rows,
                fixed_launch_balances[_pool_of(segment.category, segment.locom)],
                quarter_of_maturity,
                quarters,
                segment,
                diagnostics,
            )

        result[segment] = SegmentLaunchPoint(
            segment=segment,
            share=share,
            balance=balance,
            spread=spread,
            floor=floor,
            floor_dispersion=dispersion,
            reorigination_weights=weights,
        )

    return MappingProxyType(result), diagnostics

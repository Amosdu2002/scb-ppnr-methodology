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
    CLASS_MERGED,
    BASE_AT_MEDIAN_ORIGINATION,
    EXPOSURE_COMMITTED,
    EXPOSURE_OUTSTANDING,
    EXPOSURE_UTILIZED,
    FALLBACK_NO_ORIGINATION_DATE,
    FALLBACK_OUTSIDE_MEV,
    FLOOR_COLLAPSE_BALANCE_WEIGHTED,
    FLOOR_COLLAPSE_MAX,
    FLOOR_COLLAPSE_MIN,
    FLOOR_COLLAPSES,
    ORIG_DATE_STATISTICS,
    ORIG_DATE_WEIGHTED_MEAN,
    ORIG_DATE_WEIGHTED_MEDIAN,
    POOL_MEMBERSHIP,
    SPREAD_BASE_BY_CODE,
    SPREAD_POOL_BY_CODE,
    TREATMENT_FIXED,
    TREATMENT_NO_INCOME,
    TREATMENT_VARIABLE,
    VT_FLOATING,
    VT_MIXED,
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


def weighted_origination_quarter(
    facilities: Sequence[LoanFacility],
    measure: str,
    statistic: str,
) -> str | None:
    """A balance-weighted origination-date statistic, as a calendar quarter.

    The CRE workbook weights origination dates by OUTSTANDING balance
    (PID-LOAN-22: "balance weighted orig date based on: outstanding") where
    Corporate's PID-LOAN-4 used an unweighted row median. Whether the weighted
    statistic is a median or a mean is unread in the cell formula, so both are
    offered; `weighted_median` returns an actually observed date (the first
    whose cumulative weight reaches half), `weighted_mean` interpolates one
    from date ordinals.

    Rows without a date carry no information and are skipped. Rows whose weight
    is zero are skipped too; if EVERY dated row has zero weight the statistic
    degenerates to the unweighted row median — the limit of the weighted form,
    not a new rule."""
    if statistic not in ORIG_DATE_STATISTICS:
        raise ValidationFailure(
            f"orig-date statistic must be one of {ORIG_DATE_STATISTICS}, got {statistic!r}"
        )
    dated = [
        (f.origination_date, f.exposure(measure))
        for f in facilities
        if f.origination_date is not None
    ]
    if not dated:
        return None
    weighted = [(when, weight) for when, weight in dated if weight > 0.0]
    if not weighted:
        return quarter_label(statistics.median_low([when for when, _ in dated]))

    if statistic == ORIG_DATE_WEIGHTED_MEAN:
        total = sum(weight for _, weight in weighted)
        mean_ordinal = sum(when.toordinal() * weight for when, weight in weighted) / total
        import datetime as _dt
        return quarter_label(_dt.date.fromordinal(int(round(mean_ordinal))))

    # weighted median: sort by date, take the first whose cumulative weight
    # reaches half the total — always a really observed date, median_low-style.
    ordered = sorted(weighted, key=lambda pair: pair[0])
    half = sum(weight for _, weight in ordered) / 2.0
    running = 0.0
    for when, weight in ordered:
        running += weight
        if running >= half:
            return quarter_label(when)
    return quarter_label(ordered[-1][0])   # pragma: no cover - float-sum guard


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
    measure: str = EXPOSURE_UTILIZED,
) -> Mapping[int, float]:
    """The Equation A38 blend weight, from contractual maturities (PID-LOAN-6).

    wt(PQx) = `measure` exposure of Fixed facilities maturing in PQx, divided by
    the launch-point Fixed balance. Corporate measures with UTILIZED exposure
    (the default, PID-LOAN-6); the CRE construction weighs with the OUTSTANDING
    balance column, matching its share basis. `quarter_of_maturity` maps a
    maturity date to a projection quarter or None if it falls outside the
    horizon — supplied by the caller so the projection calendar stays in one
    place.

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
        maturing[quarter] += facility.exposure(measure)

    weights: dict[int, float] = {}
    for quarter in quarters:
        value = maturing.get(quarter, 0.0) / fixed_launch_balance
        if value > 1.0 and diagnostics is not None and segment is not None:
            diagnostics.wt_over_one.append((segment, quarter, value))
        weights[quarter] = value
    return MappingProxyType(weights)


def merged_bucket_launch_point(
    facilities: Iterable[LoanFacility],
    balance: float,
    launch_point_3m: float,
    depository_h1_codes: Sequence[int],
    merged_category_name: str,
    floor_collapse: str = FLOOR_COLLAPSE_BALANCE_WEIGHTED,
    include_mixed: bool = False,
) -> SegmentLaunchPoint:
    """Fed Categories 9, 10 and 11 as one floating bucket (PID-LOAN-10).

    Those portfolios carry no H.1 code — the physical form of the Board's own
    statement that they "have no loan-level data on the FR Y-14Q H.1 schedule"
    (PDF p. 176) — so their balance comes from FR Y-9C and their rate is borrowed.

    The lender is the **depository-institutions** slice, H.1 codes 1 and 2 only.
    That is strictly narrower than Fed Category 8, which also holds code 7,
    nondepository financial institutions: the Board writes "their variable-rate
    lending to depository institutions" while its portfolio list says "financial
    institutions", and this is what that gap resolves to. Only the FLOATING rows
    of that slice price the bucket, per the workbook's own label.

    The result is one variable-rate segment holding the whole merged balance;
    `share` is left at 0 because the bucket is sized from FR Y-9C directly rather
    than as a fraction of an H.1 category."""
    codes = set(depository_h1_codes)
    donor_types = {VT_FLOATING, VT_MIXED} if include_mixed else {VT_FLOATING}
    donors = [
        f for f in facilities
        if f.h1_code in codes
        and f.segment.variable_type in donor_types
        and f.interest_rate is not None
    ]
    if not donors:
        raise ValidationFailure(
            f"the merged 9/10/11 bucket is priced off floating lending to depository "
            f"institutions (H.1 codes {sorted(codes)}), and no such rows carry an interest "
            f"rate. Refused rather than defaulted — a borrowed spread that silently became "
            f"zero would reprice the whole bucket to the base rate."
        )

    weight = sum(f.exposure(EXPOSURE_COMMITTED) for f in donors)
    if weight <= 0.0:
        raise ValidationFailure(
            "the depository-institutions floating rows carry no committed exposure, so no "
            "balance-weighted rate can be formed for the merged 9/10/11 bucket"
        )
    pool_rate = sum(f.exposure(EXPOSURE_COMMITTED) * f.interest_rate for f in donors) / weight

    segment = SegmentKey(
        category=merged_category_name, locom=CLASS_MERGED, variable_type=VT_FLOATING
    )
    floor, dispersion = collapse_floor(donors, floor_collapse, EXPOSURE_COMMITTED)
    return SegmentLaunchPoint(
        segment=segment,
        share=0.0,
        balance=balance,
        spread=SegmentSpread(
            segment=segment,
            spread=pool_rate - launch_point_3m,
            pool_rate=pool_rate,
            base_rate=launch_point_3m,
            base_quarter=None,
        ),
        floor=floor,
        floor_dispersion=dispersion,
    )


def build_launch_point(
    facilities: Iterable[LoanFacility],
    category_balances: Mapping[str, float],
    launch_point_3m: float,
    historical_3m: Mapping[str, float],
    quarters: Sequence[int],
    quarter_of_maturity,
    share_measure: str = EXPOSURE_COMMITTED,
    floor_collapse: str = FLOOR_COLLAPSE_BALANCE_WEIGHTED,
    balance_source: str = "m1",
    engine: str = "pid",
    side_balances: Mapping[tuple[str, str], float] | None = None,
) -> tuple[Mapping[SegmentKey, SegmentLaunchPoint], LaunchPointDiagnostics]:
    """Assemble every segment's launch-point quantities.

    `category_balances` is the M.1 portfolio balance per Fed Category — the
    Equation A32 multiplicand. Segment shares are taken over the category's TOTAL
    exposure across all five rate types, so the no-income codes 0 and 4 dilute
    the income-earning segments exactly as PID-LOAN-5 specifies (a recorded
    divergence: the Fed excludes fee-only balances from that denominator, which
    means this treatment produces LOWER income than a literal reading).

    `balance_source` selects the Equation A32 multiplicand: "m1" (share x the
    M.1 category balance — the original construction) or "h1_sum" (the segment's
    own H.1 exposure sum under `share_measure`, with no M.1 normalization).

    `engine` = "reference" reproduces the workbook's income construction
    (user-supplied formulas, 2026-08-12):

        Fixed row    = M.1(side) x out-share(v1 | side) x A38 rate, floored at 0
        Variable row = M.1(side) x out-share(v2+v3 | side)
                       x max(floor, base + FLOATING spread)
        floor        = sum(out x floor, blanks counting as ZERO, over v2+v3)
                       / sum(out over v2+v3), then max(.., 0)

    Mechanically: v3 rows are merged into the v2 segment (mixed carries the
    floating spread — the user's earlier separate-mixed-spread description is
    superseded by the cell formulas); balances come from `side_balances`
    (the M.1 balance of the block's own LOCOM side); the fixed segment's floor
    is exactly 0; the wt denominator uses `share_measure` instead of utilized.
    Shares within a side span ALL rate types, so codes 0/4 still dilute."""
    if engine not in ("pid", "reference"):
        raise ValidationFailure(f"engine must be 'pid' or 'reference', got {engine!r}")
    # (CRE runs through build_cre_launch_point below, not through an engine flag
    # here — the two wholesale parts use different constructions, PID-LOAN-23.)
    if engine == "reference" and side_balances is None:
        raise ValidationFailure(
            "engine='reference' needs the per-(category, side) M.1 balances — pass side_balances"
        )

    rows = list(facilities)
    if engine == "reference":
        # Mixed merges into the floating segment: same balance bucket, same
        # (floating) spread. The rate pools are computed from the ORIGINAL
        # facilities below, so the float pool already contains v2+v3 (its
        # committed-weighted rate matched the reference to four decimals).
        from dataclasses import replace as _replace
        rows = [
            _replace(f, segment=SegmentKey(f.segment.category, f.segment.locom, VT_FLOATING))
            if f.segment.variable_type == VT_MIXED else f
            for f in rows
        ]
    diagnostics = LaunchPointDiagnostics()

    by_segment: dict[SegmentKey, list[LoanFacility]] = defaultdict(list)
    for facility in rows:
        by_segment[facility.segment].append(facility)

    category_exposure: dict[str, float] = defaultdict(float)
    side_exposure: dict[tuple[str, str], float] = defaultdict(float)
    for facility in rows:
        category_exposure[facility.segment.category] += facility.exposure(share_measure)
        side_exposure[(facility.segment.category, facility.segment.locom)] += (
            facility.exposure(share_measure)
        )

    pool_rates = compute_pool_rates(rows, diagnostics)
    for (category, locom, pool), rate in pool_rates.items():
        if rate.rows_dropped:
            diagnostics.rate_rows_dropped.append(
                (category, locom, pool, rate.rows_dropped, rate.exposure_dropped)
            )

    wt_denominator_measure = share_measure if engine == "reference" else EXPOSURE_UTILIZED
    fixed_launch_balances: dict[tuple[str, str], float] = defaultdict(float)
    for facility in rows:
        if facility.segment.treatment == TREATMENT_FIXED:
            fixed_launch_balances[_pool_of(facility.segment.category, facility.segment.locom)] += (
                facility.exposure(wt_denominator_measure)
            )

    result: dict[SegmentKey, SegmentLaunchPoint] = {}
    for segment, segment_rows in by_segment.items():
        exposure = sum(f.exposure(share_measure) for f in segment_rows)
        if engine == "reference":
            side_total = side_exposure.get((segment.category, segment.locom), 0.0)
            share = exposure / side_total if side_total > 0.0 else 0.0
            balance = share * side_balances.get((segment.category, segment.locom), 0.0)
        else:
            total = category_exposure.get(segment.category, 0.0)
            share = exposure / total if total > 0.0 else 0.0
            if balance_source == "h1_sum":
                balance = exposure
            elif balance_source == "m1":
                balance = share * category_balances.get(segment.category, 0.0)
            else:
                raise ValidationFailure(
                    f"balance_source must be 'm1' or 'h1_sum', got {balance_source!r}"
                )

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

        if engine == "reference":
            if segment.treatment == TREATMENT_FIXED:
                # the workbook floors the fixed path at exactly zero
                floor, dispersion = 0.0, 0.0
            elif segment.treatment == TREATMENT_NO_INCOME:
                floor, dispersion = None, 0.0
            else:
                # outstanding-weighted floor over ALL v2+v3 rows, blanks counting
                # as ZERO in the numerator (dilutive), then floored at 0 — the
                # user-supplied formula. Deliberately different from the PID
                # collapse, which averages populated floors only.
                weight = sum(f.exposure(share_measure) for f in segment_rows)
                if weight > 0.0:
                    weighted = sum(
                        f.exposure(share_measure) * (f.interest_rate_floor or 0.0)
                        for f in segment_rows
                    )
                    floor = max(weighted / weight, 0.0)
                else:
                    floor = None
                populated = [f.interest_rate_floor for f in segment_rows
                             if f.interest_rate_floor is not None]
                dispersion = (max(populated) - min(populated)) if populated else 0.0
        else:
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


def build_cre_launch_point(
    facilities: Iterable[LoanFacility],
    side_balances: Mapping[tuple[str, str], float],
    launch_point_3m: float,
    historical_3m: Mapping[str, float],
    quarters: Sequence[int],
    quarter_of_maturity,
    orig_date_statistic: str = ORIG_DATE_WEIGHTED_MEDIAN,
) -> tuple[Mapping[SegmentKey, SegmentLaunchPoint], LaunchPointDiagnostics]:
    """Assemble the CRE launch point (PID-LOAN-18..25, as amended).

    The CRE construction is NEITHER Corporate engine: it shares the reference
    engine's balance side (per-LOCOM M.1 balances, all-rate-type share
    denominators, fixed path floored at 0, zeros-included weighted variable
    floor) while its spreads and wt are built per rate type below.

    Two rules were AMENDED by the first real compare (2026-08-12, grand 1.0008):

    - Mixed keeps its own segment for visibility but prices at the FLOATING
      spread (float pool minus the launch-point 3M) — the reference's implied
      variable spread equalled the v2 spread exactly, so the launch sheet's
      hybrid mixed-spread columns are computed but unused, precisely as
      Corporate's were (PID-LOAN-23 amended; the PID-LOAN-15 pattern again).
    - The origination-date statistic defaults to the weighted MEDIAN: the
      reference's median-date cells are actually observed dates, and the mean
      missed construction/HFI fixed by one quarter (ratio 1.0447 -> the
      PID-LOAN-22 amendment).

    Piece by piece:

        shares/balances   OUTSTANDING-weighted within (category, LOCOM); the
                          denominator spans ALL rate types, so fee-based and
                          DO-NOT-USE rows dilute the earners (PID-LOAN-24);
                          balance = share x the side's M.1 balance (PID-LOAN-20)
        rate pools        committed-weighted, Float = v2+v3, Fixed = v1
                          (observed on the CRE launch sheet; the PID-LOAN-3
                          pattern — residual item (i) of the CRE brief)
        spreads           floating AND mixed vs 3M(PQ0) at the float-pool rate;
                          fixed vs the 3M of its outstanding-WEIGHTED
                          origination quarter (PID-LOAN-22, median default;
                          `orig_date_statistic` keeps the mean for A/B)
        variable floor    per (category, LOCOM) block over floating + mixed
                          rows together, outstanding-weighted with blank floors
                          counting as ZERO, then max(.., 0) — one value shared
                          by the block's v2 and v3 segments (PID-LOAN-25)
        fixed floor       exactly 0 (the PID-LOAN-15 family, carried)
        wt                fixed rows' maturing OUTSTANDING balance over the
                          block's fixed outstanding balance — the PID-LOAN-6
                          analogue; the OQ-001 CRE leg is otherwise open, so
                          this is the flagged working construction

    A base-rate lookup miss falls back to 0 with a censused cause, exactly as
    Corporate (PID-LOAN-4 amendment) — the fallback inflates that segment's
    new-origination rate by the omitted base-rate level, so it must be visible."""
    diagnostics = LaunchPointDiagnostics()
    rows = list(facilities)
    if not rows:
        raise ValidationFailure("no CRE facilities supplied — nothing to build a launch point from")

    by_segment: dict[SegmentKey, list[LoanFacility]] = defaultdict(list)
    by_block: dict[tuple[str, str], list[LoanFacility]] = defaultdict(list)
    side_exposure: dict[tuple[str, str], float] = defaultdict(float)
    for facility in rows:
        by_segment[facility.segment].append(facility)
        block = (facility.segment.category, facility.segment.locom)
        by_block[block].append(facility)
        side_exposure[block] += facility.exposure(EXPOSURE_OUTSTANDING)

    pool_rates = compute_pool_rates(rows, diagnostics)
    for (category, locom, pool), rate in pool_rates.items():
        if rate.rows_dropped:
            diagnostics.rate_rows_dropped.append(
                (category, locom, pool, rate.rows_dropped, rate.exposure_dropped)
            )

    # PID-LOAN-25: one variable floor per block, over floating + mixed rows,
    # outstanding-weighted, blanks as ZERO (dilutive), floored at 0.
    block_floor: dict[tuple[str, str], float | None] = {}
    block_floor_dispersion: dict[tuple[str, str], float] = {}
    for block, block_rows in by_block.items():
        variable_rows = [
            f for f in block_rows if f.segment.variable_type in (VT_FLOATING, VT_MIXED)
        ]
        weight = sum(f.exposure(EXPOSURE_OUTSTANDING) for f in variable_rows)
        if weight > 0.0:
            weighted = sum(
                f.exposure(EXPOSURE_OUTSTANDING) * (f.interest_rate_floor or 0.0)
                for f in variable_rows
            )
            block_floor[block] = max(weighted / weight, 0.0)
        else:
            block_floor[block] = None
        populated = [
            f.interest_rate_floor for f in variable_rows if f.interest_rate_floor is not None
        ]
        block_floor_dispersion[block] = (max(populated) - min(populated)) if populated else 0.0

    # wt denominator: the block's fixed OUTSTANDING balance (PID-LOAN-6 analogue
    # on the CRE share basis).
    fixed_launch_balances: dict[tuple[str, str], float] = defaultdict(float)
    for facility in rows:
        if facility.segment.treatment == TREATMENT_FIXED:
            fixed_launch_balances[(facility.segment.category, facility.segment.locom)] += (
                facility.exposure(EXPOSURE_OUTSTANDING)
            )

    result: dict[SegmentKey, SegmentLaunchPoint] = {}
    for segment, segment_rows in by_segment.items():
        block = (segment.category, segment.locom)
        exposure = sum(f.exposure(EXPOSURE_OUTSTANDING) for f in segment_rows)
        side_total = side_exposure[block]
        share = exposure / side_total if side_total > 0.0 else 0.0
        balance = share * side_balances.get(block, 0.0)

        spread: SegmentSpread | None = None
        if segment.treatment != TREATMENT_NO_INCOME:
            if segment.variable_type == VT_MIXED:
                # PID-LOAN-23 as amended (compare round 1): mixed prices at the
                # FLOATING spread — float pool (which already contains the mixed
                # rows) minus the launch-point 3M. The hybrid fixed-pool spread
                # the launch sheet computes is unused in the reference's income.
                pool, basis = "float", BASE_AT_LAUNCH_POINT
            else:
                pool = SPREAD_POOL_BY_CODE[segment.variable_type]
                basis = SPREAD_BASE_BY_CODE[segment.variable_type]
            pool_rate = pool_rates.get((segment.category, segment.locom, pool))
            if pool_rate is None:
                raise ValidationFailure(
                    f"{segment}: the {pool!r} pool for {segment.category}/{segment.locom} has no "
                    f"usable interest rates, so no spread can be formed. Surfaced rather than "
                    f"defaulted — a zero spread here would silently reprice the whole segment."
                )
            if basis == BASE_AT_LAUNCH_POINT:
                base, base_quarter, fallback = launch_point_3m, None, None
            else:
                quarter = weighted_origination_quarter(
                    segment_rows, EXPOSURE_OUTSTANDING, orig_date_statistic
                )
                if quarter is None:
                    base, base_quarter, fallback = 0.0, None, FALLBACK_NO_ORIGINATION_DATE
                    diagnostics.base_rate_fallbacks.append((segment, FALLBACK_NO_ORIGINATION_DATE))
                elif quarter not in historical_3m:
                    base, base_quarter, fallback = 0.0, quarter, FALLBACK_OUTSIDE_MEV
                    diagnostics.base_rate_fallbacks.append((segment, FALLBACK_OUTSIDE_MEV))
                else:
                    base, base_quarter, fallback = historical_3m[quarter], quarter, None
            spread = SegmentSpread(
                segment=segment,
                spread=pool_rate.rate - base,
                pool_rate=pool_rate.rate,
                base_rate=base,
                base_quarter=base_quarter,
                base_rate_fallback=fallback,
            )

        if segment.treatment == TREATMENT_FIXED:
            floor, dispersion = 0.0, 0.0      # the workbook floors the fixed path at exactly 0
        elif segment.treatment == TREATMENT_VARIABLE:
            floor = block_floor[block]
            dispersion = block_floor_dispersion[block]
        else:
            floor, dispersion = None, 0.0
        if dispersion > 0.0:
            diagnostics.floor_dispersion.append((segment, dispersion))

        weights: Mapping[int, float] = MappingProxyType({})
        if segment.treatment == TREATMENT_FIXED:
            weights = compute_reorigination_weights(
                segment_rows,
                fixed_launch_balances[block],
                quarter_of_maturity,
                quarters,
                segment,
                diagnostics,
                measure=EXPOSURE_OUTSTANDING,
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

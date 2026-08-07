"""Projection of Corporate wholesale loan interest income across PQ1..PQ9.

Consumes the launch-point layer's per-segment quantities and the scenario's
3-month Treasury path; produces per-segment rate and income paths, then the
category totals with the FRB industry scalar applied.

Three engines, assigned by rate type (PID-LOAN-5):

    Floating, Mixed   IR(t) = max(3M(t) + spread, floor)         Equation A33
    Fixed             Equation A38 blend of the carried rate and the
                      new-origination rate, floored
    DO NOT USE,       no income at all — the balance still counts toward the
    Entry Fee Based   category's share denominator

The Federal Reserve model is PROPOSED for the 2026 stress test, NOT adopted.
Divergences from the source are recorded in
`specifications/interest-income/loans/ii_loans_corporate.spec.md` §7."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Mapping, Sequence

from ..core.schemas import ValidationFailure, check_rate
from .common import quarterly_income
from .loans_schemas import (
    TREATMENT_FIXED,
    TREATMENT_NO_INCOME,
    TREATMENT_VARIABLE,
    SegmentKey,
    SegmentLaunchPoint,
)


@dataclass(frozen=True)
class SegmentProjection:
    """One segment's nine-quarter rate and income paths.

    `rate_path` is None for the no-income rate types — they hold balance and earn
    nothing, so there is no rate to report. `unfloored_rate_path` is carried
    alongside the effective path so the cost of a binding floor is measurable
    rather than invisible."""

    segment: SegmentKey
    balance: float
    rate_path: Mapping[int, float] | None
    unfloored_rate_path: Mapping[int, float] | None
    income_path: Mapping[int, float]
    floor_binds: tuple[int, ...] = ()

    @property
    def total_income(self) -> float:
        return sum(self.income_path.values())


@dataclass
class ProjectionDiagnostics:
    """What the projection did, reported rather than assumed.

    A binding floor and a negative rate both change the answer without failing
    anything, so both are counted. `no_income_balance` is the exposure sitting in
    codes 0 and 4 — the recorded divergence from the Fed, whose size a reviewer
    should be able to see at a glance."""

    floor_binds: list[tuple[SegmentKey, int]] = field(default_factory=list)
    negative_rates: list[tuple[SegmentKey, int, float]] = field(default_factory=list)
    no_income_balance: float = 0.0
    scalars_applied: dict[str, float] = field(default_factory=dict)
    unscaled_categories: list[str] = field(default_factory=list)

    def render(self) -> str:
        lines = ["PROJECTION DIAGNOSTICS"]
        lines.append(f"  floor binds                 : {len(self.floor_binds)} segment-quarters")
        for segment, quarter in self.floor_binds[:20]:
            lines.append(f"      {segment}  PQ{quarter}")
        if len(self.floor_binds) > 20:
            lines.append(f"      ... {len(self.floor_binds) - 20} more")
        lines.append(f"  negative projected rates    : {len(self.negative_rates)}")
        for segment, quarter, rate in self.negative_rates:
            lines.append(f"      {segment}  PQ{quarter}  rate={rate:.4%}")
        lines.append(f"  balance earning no income   : {self.no_income_balance:,.2f} (codes 0 and 4)")
        lines.append(f"  scalars applied             : {len(self.scalars_applied)}")
        for category, scalar in sorted(self.scalars_applied.items()):
            lines.append(f"      {category}  x{scalar:.4f}")
        if self.unscaled_categories:
            lines.append(f"  categories with NO scalar   : {sorted(self.unscaled_categories)}")
        return "\n".join(lines)


def project_variable_rate(
    spread: float,
    base_path: Mapping[int, float],
    floor: float | None,
    quarters: Sequence[int],
) -> tuple[Mapping[int, float], Mapping[int, float], tuple[int, ...]]:
    """Equation A33: base rate plus a spread held constant from the launch point.

    Returns (effective, unfloored, quarters where the floor bound)."""
    unfloored = {q: base_path[q] + spread for q in quarters}
    effective: dict[int, float] = {}
    binds: list[int] = []
    for q in quarters:
        rate = unfloored[q]
        if floor is not None and rate < floor:
            rate = floor
            binds.append(q)
        effective[q] = rate
    return MappingProxyType(effective), MappingProxyType(unfloored), tuple(binds)


def project_fixed_rate(
    launch_rate: float,
    spread: float,
    base_path: Mapping[int, float],
    weights: Mapping[int, float],
    floor: float | None,
    quarters: Sequence[int],
) -> tuple[Mapping[int, float], Mapping[int, float], tuple[int, ...]]:
    """Equation A38: blend the carried rate with the new-origination rate.

        IR(t) = (1 - wt(t)) * IR(t-1) + wt(t) * (base(t) + spread)

    seeded at IR(0) = the launch-point Fixed pool rate (Equation A34 — existing
    rates are carried unchanged except where re-originated).

    The floor is applied after blending, and **the floored rate is what carries
    forward**: a floor that binds means the portfolio is actually earning its
    floor, so the next quarter's carried component is that rate, not a shadow
    value the loans never earned. The spec says only "floor applied after
    blending", so this recursion choice is recorded as a flagged decision —
    `unfloored` is returned alongside so the difference stays measurable."""
    carried = launch_rate
    carried_unfloored = launch_rate
    effective: dict[int, float] = {}
    unfloored: dict[int, float] = {}
    binds: list[int] = []

    for q in quarters:
        wt = weights.get(q, 0.0)
        new_rate = base_path[q] + spread
        blended = (1.0 - wt) * carried + wt * new_rate
        unfloored[q] = (1.0 - wt) * carried_unfloored + wt * new_rate
        if floor is not None and blended < floor:
            blended = floor
            binds.append(q)
        effective[q] = blended
        carried = blended
        carried_unfloored = unfloored[q]

    return MappingProxyType(effective), MappingProxyType(unfloored), tuple(binds)


def project_segment(
    launch: SegmentLaunchPoint,
    base_path: Mapping[int, float],
    quarters: Sequence[int],
    diagnostics: ProjectionDiagnostics | None = None,
) -> SegmentProjection:
    """Route one segment to its engine and turn its rate path into income.

    Income is `balance x rate / 4` — the single D-004 quarterization, applied at
    the final step only, never inside a rate recursion."""
    treatment = launch.segment.treatment

    if treatment == TREATMENT_NO_INCOME:
        if diagnostics is not None:
            diagnostics.no_income_balance += launch.balance
        return SegmentProjection(
            segment=launch.segment,
            balance=launch.balance,
            rate_path=None,
            unfloored_rate_path=None,
            income_path=MappingProxyType({q: 0.0 for q in quarters}),
        )

    if launch.spread is None:
        raise ValidationFailure(
            f"{launch.segment}: an income-earning segment has no launch-point spread — "
            f"the launch-point layer must supply one, and a zero default would silently "
            f"reprice the whole segment"
        )

    if treatment == TREATMENT_VARIABLE:
        rates, unfloored, binds = project_variable_rate(
            launch.spread.spread, base_path, launch.floor, quarters
        )
    elif treatment == TREATMENT_FIXED:
        rates, unfloored, binds = project_fixed_rate(
            launch.spread.pool_rate,
            launch.spread.spread,
            base_path,
            launch.reorigination_weights,
            launch.floor,
            quarters,
        )
    else:
        raise ValidationFailure(f"{launch.segment}: no engine is defined for treatment {treatment!r}")

    if diagnostics is not None:
        for q in binds:
            diagnostics.floor_binds.append((launch.segment, q))
        for q in quarters:
            if rates[q] < 0.0:
                diagnostics.negative_rates.append((launch.segment, q, rates[q]))

    income = {q: quarterly_income(launch.balance, rates[q]) for q in quarters}
    return SegmentProjection(
        segment=launch.segment,
        balance=launch.balance,
        rate_path=rates,
        unfloored_rate_path=unfloored,
        income_path=MappingProxyType(income),
        floor_binds=binds,
    )


def project_corporate(
    launch_points: Mapping[SegmentKey, SegmentLaunchPoint],
    base_path: Mapping[int, float],
    quarters: Sequence[int],
    scalars: Mapping[str, float],
    require_scalar: bool = True,
) -> tuple[Mapping[SegmentKey, SegmentProjection], Mapping[str, Mapping[int, float]], ProjectionDiagnostics]:
    """Project every segment, then roll up to category totals with the scalar.

    The FRB industry scalar is a constant multiplicative true-up applied in every
    projection quarter (PDF p. 184). A category with no scalar is a hard error by
    default: silently defaulting to 1.0 would look like a clean run while leaving
    that category un-trued-up, and the scalar-to-category mapping is itself an
    open question (OQ-010). Pass `require_scalar=False` only for diagnostic runs.

    Returns (per-segment projections, per-category income paths, diagnostics)."""
    for q in quarters:
        if q not in base_path:
            raise ValidationFailure(
                f"scenario base rate is missing PQ{q} — the projection covers exactly "
                f"{list(quarters)} with no gaps"
            )
        check_rate(f"base_path[PQ{q}]", base_path[q])

    diagnostics = ProjectionDiagnostics()
    projections: dict[SegmentKey, SegmentProjection] = {}
    by_category: dict[str, dict[int, float]] = defaultdict(lambda: {q: 0.0 for q in quarters})

    for key, launch in launch_points.items():
        projection = project_segment(launch, base_path, quarters, diagnostics)
        projections[key] = projection
        for q in quarters:
            by_category[key.category][q] += projection.income_path[q]

    scaled: dict[str, Mapping[int, float]] = {}
    for category, path in by_category.items():
        if category in scalars:
            scalar = float(scalars[category])
            diagnostics.scalars_applied[category] = scalar
        elif require_scalar:
            raise ValidationFailure(
                f"no industry scalar supplied for category {category!r}. Refused rather than "
                f"defaulted to 1.0: an unscaled category is indistinguishable from a scaled one "
                f"in the output, and the scalar-to-category mapping is unresolved (OQ-010)"
            )
        else:
            scalar = 1.0
            diagnostics.unscaled_categories.append(category)
        scaled[category] = MappingProxyType({q: path[q] * scalar for q in quarters})

    return MappingProxyType(projections), MappingProxyType(scaled), diagnostics

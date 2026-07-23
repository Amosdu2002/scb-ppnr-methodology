"""Side-neutral canonical-boundary conventions shared by every model family.

Moved verbatim from the verified interest-expense schemas at the core extraction
(asset-side Increment 1, 2026-07-23): the projection-quarter grid, the validation
vocabulary, and the path freezer. Core holds conventions, never model semantics.
`interest_expense` re-exports every name here (with `_finite`/`_require_id`
aliases for the formerly-private helpers), so its public API is unchanged and its
bit-exact golden tests gate this move.

Canonical units (conventions chapters; decisions D-004, D-006): monetary amounts
in USD millions; every rate, spread, and beta an annualized decimal rate;
projection horizon PQ1..PQ9 with PQ0 the launch point. Percent→decimal and
billions→millions normalization belongs at the ingestion boundary, upstream of
these types — a rate magnitude >= RATE_SCALE_GUARD is rejected as percent-scale
leakage rather than silently reinterpreted."""

from __future__ import annotations

import math
from types import MappingProxyType
from typing import Any, Mapping

PROJECTION_QUARTERS: tuple[int, ...] = (1, 2, 3, 4, 5, 6, 7, 8, 9)
LAUNCH_QUARTER: int = 0
SCENARIO_QUARTERS_WITH_LAUNCH: tuple[int, ...] = (LAUNCH_QUARTER, *PROJECTION_QUARTERS)

# A "rate" at or beyond this magnitude is treated as percent-scale leakage
# (e.g. 4.25 passed where 0.0425 was meant) and rejected at the canonical boundary.
RATE_SCALE_GUARD: float = 0.5


class ValidationFailure(ValueError):
    """Contract violation on canonical inputs or a calculation invariant.

    Never caught to substitute a fallback value — failures surface, nothing
    defaults silently (conventions §6)."""


def check_finite(name: str, value: Any) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValidationFailure(f"{name} must be a number, got {value!r}")
    v = float(value)
    if not math.isfinite(v):
        raise ValidationFailure(f"{name} must be finite, got {value!r}")
    return v


def check_rate(name: str, value: Any) -> float:
    v = check_finite(name, value)
    if abs(v) >= RATE_SCALE_GUARD:
        raise ValidationFailure(
            f"{name} = {v} looks percent-scaled; canonical rates are annualized decimals "
            f"(|rate| < {RATE_SCALE_GUARD}). Normalize percent vs decimal at the ingestion "
            f"boundary, never inside the models."
        )
    return v


def check_balance(name: str, value: Any) -> float:
    v = check_finite(name, value)
    if v < 0.0:
        raise ValidationFailure(f"{name} must be >= 0 USD, got {v}")
    return v


def check_share(name: str, value: Any) -> float:
    v = check_finite(name, value)
    if not 0.0 <= v <= 1.0:
        raise ValidationFailure(f"{name} must lie in [0, 1], got {v}")
    return v


def freeze_path(
    name: str,
    values: Mapping[int, Any],
    quarters: tuple[int, ...],
    check=check_finite,
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


def require_id(name: str, value: Any) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValidationFailure(f"{name} must be a non-empty string, got {value!r}")

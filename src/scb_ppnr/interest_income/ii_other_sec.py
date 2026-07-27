"""ii_other_sec — Interest Income on Other Securities (Eq A42, B.v.a(5)).

The collapsed book-yield variant [FACT]: total income = AC(t) × BookYield/4
(effective-interest; coupon and book yield constant for the security's life;
straight-line fallback when either is missing). No prepayments. Floaters use
the imputed-margin machinery on the coupon (PID-SEC-2 floor modes) and shift
the book yield by the same 3M-Treasury delta [INTERIM — chapter §6 step 3
flag]; the floor is applied to the coupon leg only. Maturities feed the shared
1Y-Treasury reinvestment ledger. For reporting consistency with the A41-style
decomposition, income is carried as cash coupon + accretion residual — their
sum equals the A42 total."""

from __future__ import annotations

from typing import Iterable, Mapping

from ..core.schemas import PROJECTION_QUARTERS, ValidationFailure
from .schemas import IncomeModelResult, IncomeScenarioPaths
from .securities_engine import (
    PerSecurityFlows,
    aggregate_model_result,
    floating_coupon_path,
    quarterly,
    reference_accretion_step,
)
from .securities_schemas import (
    MODEL_OTHER_SEC,
    RATE_FLOATING,
    RATE_ZERO_COUPON,
    SecurityPosition,
)

MODEL_ID = MODEL_OTHER_SEC


def _flows(position: SecurityPosition, scenario: IncomeScenarioPaths,
           floor_mode: str, warnings: list[str],
           floating_projection: str = "spot",
           book_yield_categories: tuple[str, ...] = (),
           projection_overrides: Mapping[str, str] | None = None) -> PerSecurityFlows:
    face = position.current_face
    maturity = position.maturity_quarters
    last_quarter = min(maturity, PROJECTION_QUARTERS[-1]) if maturity is not None else PROJECTION_QUARTERS[-1]

    # PID-SEC-11 (reference-identified 2026-07-27): configured categories accrue at
    # BOOK YIELD held flat — fixed AND floating alike (Municipal floaters matched
    # book-yield-flat exactly; fixed implied a constant BY/coupon multiplier).
    # Zero-coupon rows are untouched; a missing book yield falls back to the coupon.
    if (position.category in book_yield_categories and position.rate_type != RATE_ZERO_COUPON
            and position.book_yield is not None):
        coupon = {q: position.book_yield for q in PROJECTION_QUARTERS}
    elif position.rate_type == RATE_FLOATING:
        if position.category in book_yield_categories:
            warnings.append(f"{position.security_id}: book-yield category but no book yield on file — floating margin machinery used (surfaced)")
        mode = (projection_overrides or {}).get(position.category, floating_projection)
        coupon = floating_coupon_path(position, scenario, floor_mode, warnings, mode)
    elif position.rate_type == RATE_ZERO_COUPON:
        coupon = {q: 0.0 for q in PROJECTION_QUARTERS}
    else:
        if position.coupon_rate is None:
            raise ValidationFailure(f"{position.security_id}: fixed-rate security without a coupon rate")
        if position.category in book_yield_categories:
            warnings.append(f"{position.security_id}: book-yield category but no book yield on file — coupon fallback (surfaced)")
        coupon = {q: position.coupon_rate for q in PROJECTION_QUARTERS}

    # PID-SEC-8 (user-verified 2026-07-24): income is ALWAYS cash coupon + AA
    # (+ hedge + reinvestment) — the collapsed A42 book-yield form is not what
    # the reference computes. AA = (prior face − prior AC)/(4 × maturity years);
    # AC(q) = AC(q−1) + AA(q).
    denominator = 4.0 * position.maturity_years if position.maturity_years is not None else None
    if denominator is None and not position.ac_proxied and face != position.amortized_cost:
        warnings.append(f"{position.security_id}: no maturity for the PID-SEC-8 accretion denominator — AA held at 0 (surfaced)")

    coupon_cash: dict[int, float] = {}
    accretion: dict[int, float] = {}
    ac = position.amortized_cost
    for quarter in range(1, last_quarter + 1):
        coupon_cash[quarter] = quarterly(face, coupon[quarter])
        if position.ac_proxied or denominator is None:
            accretion[quarter] = 0.0
        else:
            accretion[quarter], ac = reference_accretion_step(face, ac, face, denominator)
    matured = {maturity: face} if maturity is not None and maturity <= PROJECTION_QUARTERS[-1] else {}
    return PerSecurityFlows(position.security_id, coupon_cash, accretion, matured, alive_through=last_quarter)


def project_other_sec(
    positions: Iterable[SecurityPosition],
    scenario: IncomeScenarioPaths,
    *,
    firm_id: str,
    floor_mode: str,
    on_error: str = "stop",
    floating_projection: str = "spot",
    book_yield_categories: tuple[str, ...] = (),
    projection_overrides: Mapping[str, str] | None = None,
) -> IncomeModelResult:
    warnings: list[str] = []
    flows = []
    skipped = 0
    by_override = 0
    for position in positions:
        if position.model != MODEL_ID:
            raise ValidationFailure(f"{position.security_id}: model {position.model!r} passed to {MODEL_ID}")
        try:
            if position.ac_proxied:
                warnings.append(f"{position.security_id}: PID-SEC-3 proxied amortized cost — accretion held at 0")
            if (position.category in book_yield_categories and position.book_yield is not None
                    and position.rate_type != "zero_coupon"):
                by_override += 1
            flows.append(_flows(position, scenario, floor_mode, warnings,
                                floating_projection, book_yield_categories, projection_overrides))
        except ValidationFailure as exc:
            if on_error != "skip":
                raise
            skipped += 1
            warnings.append(f"HIGHLIGHT {position.security_id}: skipped (on_security_error='skip') — {exc}")
    if skipped:
        warnings.append(f"{skipped} other-securities position(s) skipped on error — HIGHLIGHTED above; income understated by their contribution")
    if by_override:
        warnings.append(
            f"{by_override} position(s) in {sorted(set(book_yield_categories))} accrued at BOOK YIELD "
            f"held flat (PID-SEC-11, reference-identified — pending confirmation)"
        )
    if not flows:
        warnings.append("no in-scope other-securities positions — income is identically zero (logged)")
    return aggregate_model_result(MODEL_ID, firm_id, scenario, flows, warnings)

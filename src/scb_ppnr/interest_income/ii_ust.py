"""ii_ust — Interest Income on U.S. Treasuries (Eq A40, B.v.a(3)).

Per security: coupon accrual = face × coupon/4 on the flat launch face through
the maturing quarter (PID-SEC-4: prior-quarter EOP face — flat until maturity);
accretion = (face(t=0) − AC(t=0)) ÷ maturity-in-quarters(t=0), the printed A40
straight-line with BOTH arguments at t=0, ceasing at maturity; hedge term zero
(current data state). Matured face reinvests per the shared 1Y-Treasury ledger
(securities_engine.reinvestment_income). PID-SEC-3 securities (proxied AC)
carry zero accretion. A missing coupon is a hard error naming OQ-027 (no
fallback is stated for this component); a floating-rate Treasury is surfaced
as an error (v.a(3) states no floating machinery — ask before treating)."""

from __future__ import annotations

from typing import Iterable

from ..core.schemas import PROJECTION_QUARTERS, ValidationFailure
from .schemas import IncomeModelResult, IncomeScenarioPaths
from .securities_engine import (
    PerSecurityFlows,
    aggregate_model_result,
    quarterly,
    straight_line_amount,
)
from .securities_schemas import MODEL_UST, RATE_FLOATING, SecurityPosition

MODEL_ID = MODEL_UST


def _flows(position: SecurityPosition, warnings: list[str]) -> PerSecurityFlows:
    if position.rate_type == RATE_FLOATING:
        raise ValidationFailure(
            f"{position.security_id}: floating-rate U.S. Treasury — v.a(3) states no floating "
            f"machinery for this component; surfaced for user clarification (PID-SEC-5 policy)"
        )
    if position.coupon_rate is None:
        raise ValidationFailure(
            f"{position.security_id}: coupon rate missing — no fallback is stated for U.S. "
            f"Treasuries (OQ-027); surfaced, never defaulted"
        )
    if position.maturity_quarters is None:
        raise ValidationFailure(f"{position.security_id}: maturity required for the A40 straight-line accretion")

    maturity = position.maturity_quarters
    last_quarter = min(maturity, PROJECTION_QUARTERS[-1])
    if position.ac_proxied:
        accretion_amount = 0.0
        warnings.append(f"{position.security_id}: PID-SEC-3 proxied amortized cost — accretion held at 0")
    else:
        # A40 / PID-SEC-8: PQ0 numerator AND denominator, constant per quarter. The
        # denominator is WHOLE maturity quarters — empirically confirmed 2026-07-24
        # (0.05% match vs the reference; the fractional day/365 divisor overstated
        # accretion on short maturities).
        accretion_amount = straight_line_amount(position.current_face, position.amortized_cost, maturity)

    coupon_cash = {q: quarterly(position.current_face, position.coupon_rate) for q in range(1, last_quarter + 1)}
    accretion = {q: accretion_amount for q in range(1, last_quarter + 1)}
    matured = {maturity: position.current_face} if maturity <= PROJECTION_QUARTERS[-1] else {}
    return PerSecurityFlows(position.security_id, coupon_cash, accretion, matured, alive_through=last_quarter)


def project_ust(
    positions: Iterable[SecurityPosition],
    scenario: IncomeScenarioPaths,
    *,
    firm_id: str,
    on_error: str = "stop",
) -> IncomeModelResult:
    warnings: list[str] = []
    flows = []
    skipped = 0
    for position in positions:
        if position.model != MODEL_ID:
            raise ValidationFailure(f"{position.security_id}: model {position.model!r} passed to {MODEL_ID}")
        try:
            flows.append(_flows(position, warnings))
        except ValidationFailure as exc:
            if on_error != "skip":
                raise
            skipped += 1
            warnings.append(f"HIGHLIGHT {position.security_id}: skipped (on_security_error='skip') — {exc}")
    if skipped:
        warnings.append(f"{skipped} U.S. Treasury position(s) skipped on error — HIGHLIGHTED above; income understated by their contribution")
    if not flows:
        warnings.append("no in-scope U.S. Treasury positions — income is identically zero (logged)")
    return aggregate_model_result(MODEL_ID, firm_id, scenario, flows, warnings)

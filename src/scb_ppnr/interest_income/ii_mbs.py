"""ii_mbs — Interest Income on Mortgage-Backed Securities (Eq A41, B.v.a(4)).

Two source-stated regimes in one component:

Agency prepayment securities (PID-MBS-1): the vendor-supplied projected face
path drives the balances — coupon accrual = coupon(q) × face(q−1)/4
(PID-SEC-4), accretion per the printed A41 straight-line/WAL form on
prior-quarter values with the AC recursion isolated in
securities_engine.agency_accretion_step [INTERIM]. An Agency security absent
from the prepayment sheet arrives with face_path=None and is treated as
flat-face (multi-family, no prepayment — PID-SEC-5).

All other MBS: flat face; vendor coupon with the Fed-stated book-yield
fallback; zero-coupon accrues at book yield; floaters use the imputed-margin
machinery with the PID-SEC-2 floor modes and straight-line accretion
[INTERIM]; fixed-rate uses the effective-interest method (constant coupon and
book yield), straight-line fallback when data are missing [FACT]. Maturities
feed the shared 1Y-Treasury reinvestment ledger; Agency paydown proceeds are
NOT reinvested yet (OQ-025(c) open, flagged)."""

from __future__ import annotations

from typing import Iterable

from ..core.schemas import PROJECTION_QUARTERS, ValidationFailure
from .schemas import IncomeModelResult, IncomeScenarioPaths
from .securities_engine import (
    PerSecurityFlows,
    agency_accretion_step,
    aggregate_model_result,
    effective_interest_step,
    floating_coupon_path,
    quarterly,
    straight_line_amount,
)
from .securities_schemas import (
    MODEL_MBS,
    RATE_FIXED,
    RATE_FLOATING,
    RATE_ZERO_COUPON,
    SecurityPosition,
)

MODEL_ID = MODEL_MBS


def _straight_line_denominator(position: SecurityPosition) -> float:
    if position.wal_years is not None:
        return 4.0 * position.wal_years          # A41's printed 4 × WAL(t=0)
    if position.maturity_quarters is not None:
        return float(position.maturity_quarters)
    raise ValidationFailure(f"{position.security_id}: neither WAL nor maturity available for straight-line accretion")


def _coupon_path(position: SecurityPosition, scenario: IncomeScenarioPaths,
                 floor_mode: str, warnings: list[str]) -> dict[int, float]:
    if position.rate_type == RATE_FLOATING:
        return floating_coupon_path(position, scenario, floor_mode, warnings)
    if position.rate_type == RATE_ZERO_COUPON:
        return {q: 0.0 for q in PROJECTION_QUARTERS}
    if position.coupon_rate is None:
        if position.book_yield is None:
            raise ValidationFailure(f"{position.security_id}: coupon missing and no book yield to fall back to")
        warnings.append(f"{position.security_id}: vendor coupon missing — book-yield fallback applied (Fed-stated)")
        return {q: position.book_yield for q in PROJECTION_QUARTERS}
    return {q: position.coupon_rate for q in PROJECTION_QUARTERS}


def _agency_flows(position: SecurityPosition, coupon: dict[int, float], warnings: list[str]) -> PerSecurityFlows:
    face_path = position.face_path
    assert face_path is not None
    if abs(face_path[0] - position.current_face) > 1e-6 * max(1.0, position.current_face):
        warnings.append(
            f"{position.security_id}: prepayment-sheet PQ0 face {face_path[0]} differs from the "
            f"positions-sheet current face {position.current_face} — surfaced, never adjusted"
        )
    wal_quarters = 4.0 * position.wal_years if position.wal_years is not None else None
    if wal_quarters is None and not position.ac_proxied:
        raise ValidationFailure(f"{position.security_id}: Agency accretion needs WAL(t=0)")
    maturity = position.maturity_quarters
    last_quarter = min(maturity, PROJECTION_QUARTERS[-1]) if maturity is not None else PROJECTION_QUARTERS[-1]

    coupon_cash: dict[int, float] = {}
    accretion: dict[int, float] = {}
    paydowns: dict[int, float] = {}
    ac = position.amortized_cost
    for quarter in range(1, last_quarter + 1):
        face_prior = face_path[quarter - 1]
        coupon_cash[quarter] = quarterly(face_prior, coupon[quarter])
        paydown = face_prior - face_path[quarter]
        if paydown < 0.0:
            warnings.append(f"{position.security_id}: face path INCREASES at PQ{quarter} — no paydown booked (surfaced, monotone expected)")
        elif paydown > 0.0:
            paydowns[quarter] = paydown                    # reinvests per MRM p. 72 (toggleable)
        if position.ac_proxied:
            accretion[quarter] = 0.0
        else:
            accretion[quarter], ac = agency_accretion_step(face_prior, ac, face_path[quarter], wal_quarters)
    matured = {}
    if maturity is not None and maturity <= PROJECTION_QUARTERS[-1]:
        matured = {maturity: face_path[maturity]}
    return PerSecurityFlows(position.security_id, coupon_cash, accretion, matured,
                            alive_through=last_quarter, paydown_face=paydowns)


def _other_mbs_flows(position: SecurityPosition, coupon: dict[int, float], warnings: list[str]) -> PerSecurityFlows:
    face = position.current_face
    maturity = position.maturity_quarters
    last_quarter = min(maturity, PROJECTION_QUARTERS[-1]) if maturity is not None else PROJECTION_QUARTERS[-1]

    use_effective_interest = (
        position.rate_type in (RATE_FIXED, RATE_ZERO_COUPON)
        and position.book_yield is not None
        and not position.ac_proxied
    )
    if position.rate_type == RATE_FLOATING and not position.ac_proxied:
        warnings.append(f"{position.security_id}: floater accretion uses the straight-line form [INTERIM — reference-check]")

    coupon_cash: dict[int, float] = {}
    accretion: dict[int, float] = {}
    ac = position.amortized_cost
    sl_amount: float | None = None
    for quarter in range(1, last_quarter + 1):
        cash = quarterly(face, coupon[quarter])
        coupon_cash[quarter] = cash
        if position.ac_proxied:
            accretion[quarter] = 0.0
        elif use_effective_interest:
            _, accretion[quarter], ac = effective_interest_step(ac, position.book_yield, cash)
        else:
            if sl_amount is None:
                sl_amount = straight_line_amount(face, position.amortized_cost, _straight_line_denominator(position))
                if position.rate_type in (RATE_FIXED, RATE_ZERO_COUPON):
                    warnings.append(f"{position.security_id}: effective-interest inputs missing — straight-line fallback (Fed-stated)")
            accretion[quarter] = sl_amount
    matured = {maturity: face} if maturity is not None and maturity <= PROJECTION_QUARTERS[-1] else {}
    return PerSecurityFlows(position.security_id, coupon_cash, accretion, matured, alive_through=last_quarter)


def project_mbs(
    positions: Iterable[SecurityPosition],
    scenario: IncomeScenarioPaths,
    *,
    firm_id: str,
    floor_mode: str,
    on_error: str = "stop",
    reinvest_paydowns: bool = True,
) -> IncomeModelResult:
    warnings: list[str] = []
    flows = []
    skipped = 0
    for position in positions:
        if position.model != MODEL_ID:
            raise ValidationFailure(f"{position.security_id}: model {position.model!r} passed to {MODEL_ID}")
        try:
            coupon = _coupon_path(position, scenario, floor_mode, warnings)
            if position.ac_proxied:
                warnings.append(f"{position.security_id}: PID-SEC-3 proxied amortized cost — accretion held at 0")
            if position.face_path is not None:
                flows.append(_agency_flows(position, coupon, warnings))
            else:
                flows.append(_other_mbs_flows(position, coupon, warnings))
        except ValidationFailure as exc:
            if on_error != "skip":
                raise
            skipped += 1
            warnings.append(f"HIGHLIGHT {position.security_id}: skipped (on_security_error='skip') — {exc}")
    if skipped:
        warnings.append(f"{skipped} MBS position(s) skipped on error — HIGHLIGHTED above; income understated by their contribution")
    if not flows:
        warnings.append("no in-scope MBS positions — income is identically zero (logged)")
    if not reinvest_paydowns:
        warnings.append("reinvest_paydowns=false — paydown proceeds NOT reinvested (A/B toggle; MRM p. 72 says they are)")
    return aggregate_model_result(MODEL_ID, firm_id, scenario, flows, warnings,
                                  reinvest_paydowns=reinvest_paydowns)

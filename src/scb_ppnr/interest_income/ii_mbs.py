"""ii_mbs — Interest Income on Mortgage-Backed Securities (Eq A41, B.v.a(4)).

Two source-stated regimes in one component:

Agency prepayment securities (PID-MBS-1): the vendor-supplied projected face
path drives the balances — coupon accrual = coupon(q) × face(q−1)/4
(PID-SEC-4), accretion per the PID-SEC-8 reference recursion
(securities_engine.reference_accretion_step) over 4 × WAL(t=0), with paydowns
absorbed into AC. An Agency security absent from the prepayment sheet arrives
with face_path=None and is treated as flat-face (multi-family, no prepayment —
PID-SEC-5; flat treatment confirmed vs the reference 2026-07-24).

All other MBS: flat face; vendor coupon with the Fed-stated book-yield
fallback; zero-coupon accrues via AA only; floaters use the imputed-margin
machinery with the PID-SEC-2 floor modes; accretion follows the PID-SEC-8
form over 4 × maturity years. Maturities AND Agency paydowns feed the shared
1Y-Treasury reinvestment ledger (MRM p. 72; validated vs the reference
2026-07-24; `reinvest_paydowns` toggle)."""

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
    MODEL_MBS,
    RATE_FIXED,
    RATE_FLOATING,
    RATE_ZERO_COUPON,
    SecurityPosition,
)

MODEL_ID = MODEL_MBS


def _coupon_path(position: SecurityPosition, scenario: IncomeScenarioPaths,
                 floor_mode: str, warnings: list[str],
                 floating_projection: str = "spot",
                 projection_overrides: Mapping[str, str] | None = None) -> dict[int, float]:
    if position.rate_type == RATE_FLOATING:
        mode = (projection_overrides or {}).get(position.category, floating_projection)
        return floating_coupon_path(position, scenario, floor_mode, warnings, mode)
    if position.rate_type == RATE_ZERO_COUPON:
        return {q: 0.0 for q in PROJECTION_QUARTERS}
    if position.coupon_rate is None:
        if position.book_yield is None:
            raise ValidationFailure(f"{position.security_id}: coupon missing and no book yield to fall back to")
        warnings.append(f"{position.security_id}: vendor coupon missing — book-yield fallback applied (Fed-stated)")
        return {q: position.book_yield for q in PROJECTION_QUARTERS}
    return {q: position.coupon_rate for q in PROJECTION_QUARTERS}


def _agency_flows(position: SecurityPosition, coupon: dict[int, float], warnings: list[str],
                  face_path_survival: bool = False) -> PerSecurityFlows:
    face_path = position.face_path
    assert face_path is not None
    if abs(face_path[0] - position.current_face) > 1e-6 * max(1.0, position.current_face):
        warnings.append(
            f"{position.security_id}: prepayment-sheet PQ0 face {face_path[0]} differs from the "
            f"positions-sheet current face {position.current_face} — surfaced, never adjusted"
        )
    wal_quarters = 4.0 * position.wal_years if position.wal_years is not None else None
    if wal_quarters is None and not position.suppress_accretion:
        raise ValidationFailure(f"{position.security_id}: Agency accretion needs WAL(t=0)")
    maturity = position.maturity_quarters
    last_quarter = min(maturity, PROJECTION_QUARTERS[-1]) if maturity is not None else PROJECTION_QUARTERS[-1]
    # PID-SEC-16: the vendor face path is the balance projection. A WAL-derived
    # maturity (PID-SEC-7) is an average life, not a maturity date, and must not
    # end a security the vendor says still has face.
    if face_path_survival:
        alive = [q for q in PROJECTION_QUARTERS if face_path[q] > 0.0]
        path_last = alive[-1] if alive else 0
        # ONLY EXTEND (fixed 2026-07-29). The switch exists to stop a WAL-derived
        # maturity ending a security the vendor says still has balance; it must never
        # do the reverse. Taking the path end unconditionally shortened lives instead,
        # because trailing BLANK cells in the prepayment pivot are read as 0 (PID-SEC-8)
        # and are indistinguishable from a genuine paydown to zero — that is how
        # TRUNC Agency MBS went 476 rows @ PQ7.3 to 520 @ PQ5.5 with the switch ON.
        if path_last > last_quarter:
            warnings.append(
                f"{position.security_id}: face path carries balance through PQ{path_last} but "
                f"maturity_quarters={maturity} would end it at PQ{last_quarter} — path governs "
                f"(PID-SEC-16)"
            )
            last_quarter = path_last
        elif path_last < last_quarter:
            warnings.append(
                f"{position.security_id}: face path ends at PQ{path_last}, before "
                f"maturity_quarters={maturity} — NOT shortened (PID-SEC-16 only extends; "
                f"trailing blank prepayment cells read as 0 are indistinguishable from a real "
                f"paydown to zero)"
            )

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
            paydown = 0.0
        elif paydown > 0.0:
            paydowns[quarter] = paydown                    # reinvests per MRM p. 72 (toggleable)
        if position.suppress_accretion:
            accretion[quarter] = 0.0
        else:
            # PID-SEC-8: AA on prior-quarter values over 4×WAL(t=0); AC absorbs AA minus the paydown.
            accretion[quarter], ac = reference_accretion_step(face_prior, ac, face_path[quarter], wal_quarters, paydown)
    matured = {}
    if face_path_survival:
        # Matured only where the vendor path itself reaches zero; the remaining
        # face is carried by the paydown ledger instead.
        zero_quarter = next((q for q in PROJECTION_QUARTERS if face_path[q] == 0.0), None)
        if zero_quarter is not None and face_path[zero_quarter - 1] > 0.0:
            matured = {zero_quarter: face_path[zero_quarter - 1]}
    elif maturity is not None and maturity <= PROJECTION_QUARTERS[-1]:
        matured = {maturity: face_path[maturity]}
    return PerSecurityFlows(position.security_id, coupon_cash, accretion, matured,
                            alive_through=last_quarter, paydown_face=paydowns)


def _other_mbs_flows(position: SecurityPosition, coupon: dict[int, float], warnings: list[str]) -> PerSecurityFlows:
    """Flat-face securities under the PID-SEC-8 reference scheme: cash coupon on
    the prior-EOP face plus AA = (prior face − prior AC)/(4 × maturity years),
    AC(q) = AC(q−1) + AA(q)."""
    face = position.current_face
    maturity = position.maturity_quarters
    last_quarter = min(maturity, PROJECTION_QUARTERS[-1]) if maturity is not None else PROJECTION_QUARTERS[-1]

    denominator = 4.0 * position.maturity_years if position.maturity_years is not None else None
    if denominator is None and not position.suppress_accretion and position.current_face != position.amortized_cost:
        warnings.append(f"{position.security_id}: no maturity for the PID-SEC-8 accretion denominator — AA held at 0 (surfaced)")

    coupon_cash: dict[int, float] = {}
    accretion: dict[int, float] = {}
    ac = position.amortized_cost
    for quarter in range(1, last_quarter + 1):
        coupon_cash[quarter] = quarterly(face, coupon[quarter])
        if position.suppress_accretion or denominator is None:
            accretion[quarter] = 0.0
        else:
            accretion[quarter], ac = reference_accretion_step(face, ac, face, denominator)
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
    floating_projection: str = "spot",
    projection_overrides: Mapping[str, str] | None = None,
    agency_face_path_survival: bool = False,
) -> IncomeModelResult:
    warnings: list[str] = []
    flows = []
    skipped = 0
    for position in positions:
        if position.model != MODEL_ID:
            raise ValidationFailure(f"{position.security_id}: model {position.model!r} passed to {MODEL_ID}")
        try:
            coupon = _coupon_path(position, scenario, floor_mode, warnings, floating_projection, projection_overrides)
            if position.suppress_accretion:
                warnings.append(f"{position.security_id}: PID-SEC-3 proxied amortized cost — accretion held at 0")
            if position.face_path is not None:
                flows.append(_agency_flows(position, coupon, warnings, agency_face_path_survival))
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

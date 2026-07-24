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

from typing import Iterable

from ..core.schemas import PROJECTION_QUARTERS, ValidationFailure
from .schemas import IncomeModelResult, IncomeScenarioPaths
from .securities_engine import (
    PerSecurityFlows,
    aggregate_model_result,
    floating_coupon_path,
    quarterly,
    straight_line_amount,
)
from .securities_schemas import (
    MODEL_OTHER_SEC,
    RATE_FLOATING,
    RATE_ZERO_COUPON,
    SecurityPosition,
)

MODEL_ID = MODEL_OTHER_SEC


def _flows(position: SecurityPosition, scenario: IncomeScenarioPaths,
           floor_mode: str, warnings: list[str]) -> PerSecurityFlows:
    face = position.current_face
    maturity = position.maturity_quarters
    last_quarter = min(maturity, PROJECTION_QUARTERS[-1]) if maturity is not None else PROJECTION_QUARTERS[-1]

    if position.rate_type == RATE_FLOATING:
        coupon = floating_coupon_path(position, scenario, floor_mode, warnings)
    elif position.rate_type == RATE_ZERO_COUPON:
        coupon = {q: 0.0 for q in PROJECTION_QUARTERS}
    else:
        if position.coupon_rate is None:
            raise ValidationFailure(f"{position.security_id}: fixed-rate security without a coupon rate")
        coupon = {q: position.coupon_rate for q in PROJECTION_QUARTERS}

    coupon_cash: dict[int, float] = {}
    accretion: dict[int, float] = {}
    ac = position.amortized_cost
    sl_amount: float | None = None
    for quarter in range(1, last_quarter + 1):
        cash = quarterly(face, coupon[quarter])
        coupon_cash[quarter] = cash
        if position.ac_proxied:
            accretion[quarter] = 0.0
        elif position.book_yield is not None:
            if position.rate_type == RATE_FLOATING:
                # [INTERIM] the book yield floats by the same 3M delta as the coupon;
                # the PID-SEC-2 floor applies to the coupon leg only.
                book_yield = position.book_yield + (
                    scenario.usd_3m_treasury[quarter] - scenario.usd_3m_treasury[0]
                )
            else:
                book_yield = position.book_yield
            total = quarterly(ac, book_yield)              # A42: AC(t) × BookYield/4 — source-stated ÷4
            accretion[quarter] = total - cash
            ac = ac + accretion[quarter]
        else:
            if sl_amount is None:
                if maturity is None:
                    raise ValidationFailure(
                        f"{position.security_id}: book yield missing and no maturity for the straight-line fallback"
                    )
                sl_amount = straight_line_amount(face, position.amortized_cost, float(maturity))
                warnings.append(f"{position.security_id}: book yield missing — straight-line fallback (Fed-stated)")
            accretion[quarter] = sl_amount
    matured = {maturity: face} if maturity is not None and maturity <= PROJECTION_QUARTERS[-1] else {}
    return PerSecurityFlows(position.security_id, coupon_cash, accretion, matured, alive_through=last_quarter)


def project_other_sec(
    positions: Iterable[SecurityPosition],
    scenario: IncomeScenarioPaths,
    *,
    firm_id: str,
    floor_mode: str,
) -> IncomeModelResult:
    warnings: list[str] = []
    flows = []
    for position in positions:
        if position.model != MODEL_ID:
            raise ValidationFailure(f"{position.security_id}: model {position.model!r} passed to {MODEL_ID}")
        if position.ac_proxied:
            warnings.append(f"{position.security_id}: PID-SEC-3 proxied amortized cost — accretion held at 0")
        flows.append(_flows(position, scenario, floor_mode, warnings))
    if not flows:
        warnings.append("no in-scope other-securities positions — income is identically zero (logged)")
    return aggregate_model_result(MODEL_ID, firm_id, scenario, flows, warnings)

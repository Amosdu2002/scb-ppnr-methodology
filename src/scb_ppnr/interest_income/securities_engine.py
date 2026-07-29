"""Shared securities machinery — exactly what the Fed shares across Eqs A40–A42
(asset conventions §12), plus the user-confirmed reinvestment ledger.

Every source-stated ÷4 lives inside these functions (the source governs — not
D-004). Deliberately-interim choices are isolated in single functions and named
in `INTERIM_CHOICES` so the company-reference check can confirm or replace them
one at a time; nothing here silently clamps — floors are the Fed-stated /
PID-SEC-2 modeled binds, and every bind or fallback is logged by the callers.

Reinvestment (conventions §12; MRM pp. 72–74; OQ-025(a)(b)(d) user-confirmed):
matured face buys a hypothetical 1-year Treasury at face value on the first day
of the following quarter; the coupon is the par-curve 1Y yield of the purchase
quarter (`usd_1y_treasury`), FIXED for the tranche's four-quarter window; at
maturity the tranche rolls into a new 1Y at the then-current yield; no accretion
(purchased at face), no hedges; income attribution stays with the originating
component. Paydown proceeds reinvest exactly like maturities (MRM p. 72;
`reinvest_paydowns` toggle; validated vs the reference 2026-07-24)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping

from ..core.schemas import PROJECTION_QUARTERS, ValidationFailure
from .common import build_income_result
from .schemas import IncomeModelResult, IncomeQuarterResult, IncomeScenarioPaths
from .securities_schemas import (
    FLOAT_PROJECTION_BLEND13,
    FLOAT_PROJECTION_FLAT_C0,
    FLOAT_PROJECTION_FREEZE1,
    FLOAT_PROJECTION_MODES,
    FLOAT_PROJECTION_NEG_HOLD_BLEND,
    FLOAT_PROJECTION_POS_HOLD,
    FLOAT_PROJECTION_POS_HOLD_BLEND,
    FLOAT_PROJECTION_SPOT,
    FLOOR_MODE_SECURITY,
    FLOOR_MODE_SECURITY_ELSE_ZERO,
    FLOOR_MODE_ZERO,
    FLOOR_MODES,
    SecuritiesQuarterDiagnostics,
    SecurityPosition,
)

# Remaining interim choices. The accretion/AC machinery is no longer interim:
# PID-SEC-8 (user-verified against the reference workbook, 2026-07-24) fixes
# income = coupon accrual + AA + hedge + reinvestment for every security, with
# AA = 0 if the quarter's face is 0 else (prior face − prior AC)/denominator
# (denominator = 4 × maturity years; 4 × WAL(t=0) for Agency MBS; PQ0 numerator
# and denominator for U.S. Treasuries) and AC(q) = AC(q−1) + AA(q) − paydown(q).
# 2026-07-24 compare-mode confirmations: paydown reinvestment (Agency MBS ours/ref
# 1.0055), floor-at-zero semantics (the reference accrues PQ1 then nothing on
# negative-margin floaters — exactly mode 'zero'), STEP CPN flat at the launch
# coupon, multifamily flat-face. reference_income_scope RESOLVED 2026-07-24 by
# the dual ratios: the II_PQ columns EXCLUDE reinvestment income (booked only in
# the separate 'Reinvestment Interest income' section) — UST xr/ref = 0.9985 vs
# 1.0081 including, Agency MBS 0.9975 vs 1.0055 — so xr/ref is the primary
# verification ratio. No interim choices remain open in this module.
INTERIM_CHOICES: dict[str, str] = {}


def quarterly(amount_balance: float, annualized_rate: float) -> float:
    """balance × rate / 4 — the source-stated ÷4 inside Eqs A40–A42."""
    return amount_balance * annualized_rate / 4.0


def floating_coupon_path(
    position: SecurityPosition,
    scenario: IncomeScenarioPaths,
    floor_mode: str,
    warnings: list[str],
    projection_mode: str = FLOAT_PROJECTION_SPOT,
) -> dict[int, float]:
    """Imputed floating coupon (FACT, PPNR pp. 196/201) + PID-SEC-2 floor modes
    + PID-SEC-10 projection modes.

    margin = t0 coupon − t0 spot 3M; coupon(q) = margin + 3M(q). Floor modes:
    'zero' / 'security_floor' / 'none' scoped to negative-launch-margin floaters
    (the original PID-SEC-2 statement); 'security_floor_else_zero' floors EVERY
    floater at max(coupon(q), security floor if on file else 0). Projection
    modes (PID-SEC-10, reference-identified 2026-07-27; per-category via config
    overrides): 'neg_hold' holds a negative-margin floater's launch coupon flat
    (never re-projected); 'neg_hold_blend13' additionally accrues PQ1 at
    ⅓·launch + ⅔·(margin + 3M(PQ1)) for positive margins (monthly-reset blend);
    'blend13' applies the PQ1 blend WITHOUT the negative-margin hold (CLO/Auto/
    Foreign-RMBS-identified); 'flat_c0' holds EVERY floater at the launch coupon
    (Non-Agency-RMBS-identified). Every hold/bind is logged, never silent."""
    if floor_mode not in FLOOR_MODES:
        raise ValidationFailure(f"floor_mode must be one of {FLOOR_MODES}, got {floor_mode!r}")
    if projection_mode not in FLOAT_PROJECTION_MODES:
        raise ValidationFailure(f"floating projection mode must be one of {FLOAT_PROJECTION_MODES}, got {projection_mode!r}")
    if position.coupon_rate is None:
        raise ValidationFailure(f"{position.security_id}: floating security has no t=0 coupon for the margin imputation")
    # PID-SEC-17: a SUPPLIED margin wins over the imputation. The Fed's imputation
    # (margin = t0 coupon - t0 spot 3M) is explicitly a fallback for instruments whose
    # margin the Board does not hold — and Agency residential MBS are the stated
    # exception (PPNR p. 199), so those carry a real spread.
    if position.margin is not None:
        margin = position.margin
        warnings.append(
            f"{position.security_id}: supplied margin {margin:.6f} used (PID-SEC-17); "
            f"the t0 imputation would have given {position.coupon_rate - scenario.usd_3m_treasury[0]:.6f}"
        )
    else:
        margin = position.coupon_rate - scenario.usd_3m_treasury[0]
    negative_margin = margin < 0.0
    if negative_margin:
        warnings.append(
            f"{position.security_id}: negative imputed margin {margin:.6f} "
            f"(t0 coupon {position.coupon_rate} < t0 spot 3M {scenario.usd_3m_treasury[0]}) — "
            f"PID-SEC-2 floor_mode={floor_mode!r} governs"
        )
    if projection_mode == FLOAT_PROJECTION_FREEZE1:
        # One reset after launch, then frozen: PQ1 still accrues at the coupon
        # fixed before the launch date; PQ2..9 all accrue at the rate set off
        # 3M(PQ1). Floored at 0 — part of the reference-identified rule.
        frozen = max(margin + scenario.usd_3m_treasury[1], 0.0)
        warnings.append(
            f"{position.security_id}: PQ1 at the launch coupon {position.coupon_rate}, then frozen at "
            f"{frozen:.6f} for PQ2–9 (PID-SEC-10 mode 'freeze1'; single reset off 3M(PQ1))"
        )
        return {quarter: (position.coupon_rate if quarter == 1 else frozen)
                for quarter in PROJECTION_QUARTERS}
    if projection_mode == FLOAT_PROJECTION_FLAT_C0:
        warnings.append(
            f"{position.security_id}: launch coupon {position.coupon_rate} held flat PQ1–9 "
            f"(PID-SEC-10 mode 'flat_c0'; floater never re-projected)"
        )
        return {quarter: position.coupon_rate for quarter in PROJECTION_QUARTERS}
    if not negative_margin and projection_mode in (FLOAT_PROJECTION_POS_HOLD,
                                                   FLOAT_PROJECTION_POS_HOLD_BLEND):
        # Mirror of neg_hold (CMBS-identified 2026-07-28): the POSITIVE-margin
        # floater is the one that is never re-projected. Because 3M falls from the
        # launch spot in this scenario, margin + 3M(q) is always below the launch
        # coupon — the reference behaves as if the coupon cannot reset downward.
        warnings.append(
            f"{position.security_id}: positive margin {margin:.6f} — launch coupon "
            f"{position.coupon_rate} held flat PQ1–9 (PID-SEC-10 mode {projection_mode!r})"
        )
        return {quarter: position.coupon_rate for quarter in PROJECTION_QUARTERS}
    if negative_margin and projection_mode in ("neg_hold", FLOAT_PROJECTION_NEG_HOLD_BLEND):
        warnings.append(
            f"{position.security_id}: negative margin — launch coupon {position.coupon_rate} held "
            f"flat PQ1–9 (PID-SEC-10 mode {projection_mode!r}; never re-projected)"
        )
        return {quarter: position.coupon_rate for quarter in PROJECTION_QUARTERS}
    universal_floor: float | None = None
    if floor_mode == FLOOR_MODE_SECURITY_ELSE_ZERO:
        universal_floor = position.coupon_floor if position.coupon_floor is not None else 0.0
    path: dict[int, float] = {}
    floored_quarters: list[int] = []
    for quarter in PROJECTION_QUARTERS:
        coupon = margin + scenario.usd_3m_treasury[quarter]
        if quarter == 1 and projection_mode in (FLOAT_PROJECTION_NEG_HOLD_BLEND, FLOAT_PROJECTION_BLEND13,
                                                FLOAT_PROJECTION_POS_HOLD_BLEND):
            # Monthly-reset PQ1 (PID-SEC-10): the first month still accrues at the
            # launch coupon; the remaining two at the newly reset rate.
            coupon = position.coupon_rate / 3.0 + 2.0 * (margin + scenario.usd_3m_treasury[1]) / 3.0
        if universal_floor is not None:
            if coupon < universal_floor:
                coupon = universal_floor
                floored_quarters.append(quarter)
        elif negative_margin:
            if floor_mode == FLOOR_MODE_ZERO and coupon < 0.0:
                warnings.append(f"{position.security_id}: PQ{quarter} coupon {coupon:.6f} floored at 0 (mode 'zero')")
                coupon = 0.0
            elif floor_mode == FLOOR_MODE_SECURITY and position.coupon_floor is not None and coupon < position.coupon_floor:
                warnings.append(
                    f"{position.security_id}: PQ{quarter} coupon {coupon:.6f} floored at the "
                    f"security coupon floor {position.coupon_floor} (mode 'security_floor')"
                )
                coupon = position.coupon_floor
            # FLOOR_MODE_NONE (or security mode without a floor on file): raw value stands.
        path[quarter] = coupon
    if floored_quarters:
        source = "security floor" if position.coupon_floor is not None else "0 — no floor on file"
        warnings.append(
            f"{position.security_id}: coupon floored at {universal_floor} ({source}) in "
            f"quarters {floored_quarters} (mode 'security_floor_else_zero')"
        )
    return path


def straight_line_amount(face_launch: float, ac_launch: float, denominator_quarters: float) -> float:
    """(face(t=0) − AC(t=0)) ÷ denominator — A40's form and the stated fallback."""
    if denominator_quarters <= 0:
        raise ValidationFailure(f"straight-line denominator must be > 0 quarters, got {denominator_quarters}")
    return (face_launch - ac_launch) / denominator_quarters


def reference_accretion_step(
    face_prior: float,
    ac_prior: float,
    face_now: float,
    denominator_quarters: float,
    paydown: float = 0.0,
) -> tuple[float, float]:
    """[PID-SEC-8, user-verified 2026-07-24] One quarter of the reference AA/AC step.

    AA = 0 if this quarter's face is 0, else (prior face − prior AC) ÷ denominator
    (denominator in quarters: 4 × maturity years; 4 × WAL(t=0) for Agency MBS).
    New AC = prior AC + AA − principal paydown. Returns (accretion, ac_now)."""
    if denominator_quarters <= 0:
        raise ValidationFailure(f"accretion denominator must be > 0 quarters, got {denominator_quarters}")
    accretion = 0.0 if face_now == 0.0 else (face_prior - ac_prior) / denominator_quarters
    return accretion, ac_prior + accretion - paydown


def reinvestment_income(
    matured_face_by_quarter: Mapping[int, float],
    scenario: IncomeScenarioPaths,
) -> tuple[dict[int, float], dict[int, float]]:
    """The user-confirmed 1Y-Treasury reinvestment ledger.

    A tranche maturing in quarter m purchases a 1Y Treasury on the first day of
    m+1; its coupon usd_1y_treasury[m+1] is FIXED for quarters m+1..m+4; at
    m+5 it rolls at usd_1y_treasury[m+5]; and so on through PQ9. Purchased at
    face → no accretion; no hedges. Returns (income_by_quarter,
    earning_balance_by_quarter)."""
    income = {q: 0.0 for q in PROJECTION_QUARTERS}
    balance = {q: 0.0 for q in PROJECTION_QUARTERS}
    for matured_quarter, amount in sorted(matured_face_by_quarter.items()):
        if amount == 0.0:
            continue
        if amount < 0.0:
            raise ValidationFailure(f"matured face cannot be negative: PQ{matured_quarter} -> {amount}")
        purchase = matured_quarter + 1
        while purchase <= PROJECTION_QUARTERS[-1]:
            rate = scenario.usd_1y_treasury[purchase]      # fixed for the 4-quarter window
            window_end = min(purchase + 3, PROJECTION_QUARTERS[-1])
            for quarter in range(purchase, window_end + 1):
                income[quarter] += quarterly(amount, rate)
                balance[quarter] += amount
            purchase += 4                                   # roll again (OQ-025(a), user-confirmed)
    return income, balance


# ---------------------------------------------------------------------------
# Aggregation plumbing (generic — not Fed machinery)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class PerSecurityFlows:
    """One security's projected flows: cash-coupon and accretion legs per
    quarter, maturity and paydown events, and the last quarter it contributes."""

    security_id: str
    coupon_cash: Mapping[int, float]
    accretion: Mapping[int, float]
    matured_face: Mapping[int, float]
    alive_through: int
    paydown_face: Mapping[int, float] | None = None    # Agency prepayment paydowns (quarter -> USD mm)

    @property
    def total(self) -> Mapping[int, float]:
        return {q: self.coupon_cash.get(q, 0.0) + self.accretion.get(q, 0.0) for q in PROJECTION_QUARTERS}

    def reinvestment_events(self, include_paydowns: bool) -> dict[int, float]:
        events = dict(self.matured_face)
        if include_paydowns and self.paydown_face:
            for quarter, amount in self.paydown_face.items():
                events[quarter] = events.get(quarter, 0.0) + amount
        return events


def aggregate_model_result(
    model_id: str,
    firm_id: str,
    scenario: IncomeScenarioPaths,
    flows: Iterable[PerSecurityFlows],
    warnings: Iterable[str],
    *,
    reinvest_paydowns: bool = True,
) -> IncomeModelResult:
    """Sum per-security flows, run the component's reinvestment ledger on its
    pooled maturity AND paydown events (attribution stays in-component —
    OQ-025(b); paydowns per MRM p. 72, toggleable), and assemble the
    IncomeModelResult. rate/balance are None by design: the securities template
    has no single balance × rate decomposition — the decomposition lives in the
    typed diagnostics."""
    flow_list = list(flows)
    matured_total: dict[int, float] = {}
    for flow in flow_list:
        for quarter, amount in flow.reinvestment_events(reinvest_paydowns).items():
            matured_total[quarter] = matured_total.get(quarter, 0.0) + amount
    reinvested, reinvested_balance = reinvestment_income(matured_total, scenario)

    rows: list[IncomeQuarterResult] = []
    for quarter in PROJECTION_QUARTERS:
        coupon = sum(f.coupon_cash.get(quarter, 0.0) for f in flow_list)
        accretion = sum(f.accretion.get(quarter, 0.0) for f in flow_list)
        rows.append(
            IncomeQuarterResult(
                quarter=quarter,
                annualized_rate=None,
                average_balance=None,
                quarterly_income=coupon + accretion + reinvested[quarter],
                diagnostics=SecuritiesQuarterDiagnostics(
                    coupon_accrual=coupon,
                    accretion=accretion,
                    reinvested_income=reinvested[quarter],
                    reinvested_balance=reinvested_balance[quarter],
                    matured_face=matured_total.get(quarter, 0.0),
                    securities_alive=sum(1 for f in flow_list if quarter <= f.alive_through),
                ),
            )
        )
    return build_income_result(model_id, firm_id, scenario.scenario_id, rows, warnings)

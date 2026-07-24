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
component. Paydown proceeds are NOT reinvested yet — OQ-025(c) open, flagged."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping

from ..core.schemas import PROJECTION_QUARTERS, ValidationFailure
from .common import build_income_result
from .schemas import IncomeModelResult, IncomeQuarterResult, IncomeScenarioPaths
from .securities_schemas import (
    FLOOR_MODE_SECURITY,
    FLOOR_MODE_ZERO,
    FLOOR_MODES,
    SecuritiesQuarterDiagnostics,
    SecurityPosition,
)

# Interim implementation choices awaiting company-reference confirmation.
# Each maps to exactly one function below; swapping one never touches the rest.
INTERIM_CHOICES = {
    "agency_ac_recursion": "agency_accretion_step — AC scales with the survival ratio, then adds the A41 straight-line amount",
    "floating_accretion_straight_line": "other-MBS floaters use straight-line accretion (the constant-coupon effective-interest assumption does not hold)",
    "other_sec_floating_book_yield_shift": "ii_other_sec floaters shift book yield by the same 3M-Treasury delta as the coupon (chapter §6 step 3 [INT])",
    "paydown_reinvestment_on": "Agency paydown proceeds reinvest like maturities (MRM p. 72 covers 'decreasing in balance due to partial paydowns' [FACT]; purchase timing mirrors the maturity rule [INT]; config toggle reinvest_paydowns — resolves OQ-025(c) for implementation, 2026-07-24)",
}


def quarterly(amount_balance: float, annualized_rate: float) -> float:
    """balance × rate / 4 — the source-stated ÷4 inside Eqs A40–A42."""
    return amount_balance * annualized_rate / 4.0


def floating_coupon_path(
    position: SecurityPosition,
    scenario: IncomeScenarioPaths,
    floor_mode: str,
    warnings: list[str],
) -> dict[int, float]:
    """Imputed floating coupon (FACT, PPNR pp. 196/201) + PID-SEC-2 floor modes.

    margin = t0 coupon − t0 spot 3M; coupon(q) = margin + 3M(q). The floor is
    scoped to negative-launch-margin floaters (PID-SEC-2) and applied per the
    configured mode; every bind is logged, never silent."""
    if floor_mode not in FLOOR_MODES:
        raise ValidationFailure(f"floor_mode must be one of {FLOOR_MODES}, got {floor_mode!r}")
    if position.coupon_rate is None:
        raise ValidationFailure(f"{position.security_id}: floating security has no t=0 coupon for the margin imputation")
    margin = position.coupon_rate - scenario.usd_3m_treasury[0]
    negative_margin = margin < 0.0
    if negative_margin:
        warnings.append(
            f"{position.security_id}: negative imputed margin {margin:.6f} "
            f"(t0 coupon {position.coupon_rate} < t0 spot 3M {scenario.usd_3m_treasury[0]}) — "
            f"PID-SEC-2 floor_mode={floor_mode!r} governs"
        )
    path: dict[int, float] = {}
    for quarter in PROJECTION_QUARTERS:
        coupon = margin + scenario.usd_3m_treasury[quarter]
        if negative_margin:
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
    return path


def straight_line_amount(face_launch: float, ac_launch: float, denominator_quarters: float) -> float:
    """(face(t=0) − AC(t=0)) ÷ denominator — A40's form and the stated fallback."""
    if denominator_quarters <= 0:
        raise ValidationFailure(f"straight-line denominator must be > 0 quarters, got {denominator_quarters}")
    return (face_launch - ac_launch) / denominator_quarters


def agency_accretion_step(face_prior: float, ac_prior: float, face_now: float, wal_quarters: float) -> tuple[float, float]:
    """[INTERIM: agency_ac_recursion] One quarter of A41 Agency accretion.

    accretion = (face_prior − AC_prior) ÷ (4 × WAL(t=0)) — the printed A41 form
    on prior-quarter values; AC then scales with the survival ratio (paydowns
    reduce amortized cost proportionally) and absorbs the accretion. Returns
    (accretion, ac_now)."""
    accretion = (face_prior - ac_prior) / wal_quarters
    survival = (face_now / face_prior) if face_prior > 0.0 else 0.0
    ac_now = ac_prior * survival + accretion
    return accretion, ac_now


def effective_interest_step(ac_prior: float, book_yield: float, cash_coupon: float) -> tuple[float, float, float]:
    """One quarter of the effective-interest method (FACT: constant coupon and
    book yield): total = AC_prior × BY/4; accretion = total − cash coupon;
    AC accrues the accretion. Returns (total_income, accretion, ac_now)."""
    total = quarterly(ac_prior, book_yield)
    accretion = total - cash_coupon
    return total, accretion, ac_prior + accretion


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

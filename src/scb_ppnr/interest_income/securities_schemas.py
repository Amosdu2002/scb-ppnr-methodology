"""Canonical security-level contracts for the securities family (PID-SEC-1/5/6).

One `SecurityPosition` per held security, produced by the ingestion layer from
the native workbook (`specifications/interest-income/securities/
securities-input-contract.md`). Money is canonical USD millions (D-006 — the
loader converts the workbook's declared whole-dollar scale once); rates are
annualized decimals. Category → model assignment is the user-confirmed
PID-SEC-5 table: a closed map, and an unmapped category is a hard error —
surfaced and asked, never defaulted."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from ..core.schemas import (
    PROJECTION_QUARTERS,
    SCENARIO_QUARTERS_WITH_LAUNCH,
    ValidationFailure,
    check_balance,
    check_finite,
    check_rate,
    freeze_path,
    require_id,
)

MODEL_UST = "ii_ust"
MODEL_MBS = "ii_mbs"
MODEL_OTHER_SEC = "ii_other_sec"
OUT_OF_SCOPE = "out_of_scope"

RATE_FIXED = "fixed"
RATE_FLOATING = "floating"
RATE_ZERO_COUPON = "zero_coupon"
_RATE_TYPES = (RATE_FIXED, RATE_FLOATING, RATE_ZERO_COUPON)

# PID-SEC-2 (finalized 2026-07-24): config-switchable floater floor modes.
# The first three are scoped to negative-launch-margin floaters (the original
# user statement). Mode 4, security_floor_else_zero, is the reference-workbook
# rule inferred from the 2026-07-24 compare observations: EVERY floater's
# projected coupon is floored at the security's coupon floor when on file,
# else at 0 (reproduces "PQ1 bigger, PQ2–9 constant" and "constant PQ1–9").
FLOOR_MODE_ZERO = "zero"
FLOOR_MODE_SECURITY = "security_floor"
FLOOR_MODE_NONE = "none"
FLOOR_MODE_SECURITY_ELSE_ZERO = "security_floor_else_zero"
FLOOR_MODES = (FLOOR_MODE_ZERO, FLOOR_MODE_SECURITY, FLOOR_MODE_NONE, FLOOR_MODE_SECURITY_ELSE_ZERO)

# PID-SEC-10 (2026-07-27, reference-identified): floating-coupon projection modes.
# "spot" — coupon(q) = margin + 3M(q) every quarter (the original rule).
# "neg_hold" — a NEGATIVE-launch-margin floater is never re-projected: the launch
#   coupon holds flat PQ1–9 (reference-observed: implied coupons ≈ launch coupon;
#   equivalently the security's effective floor is its own current coupon).
# "neg_hold_blend13" — neg_hold plus the monthly-reset PQ1 for positive margins:
#   PQ1 = ⅓·launch coupon + ⅔·(margin + 3M(PQ1)), spot thereafter (the first month
#   of PQ1 still accrues at the coupon set before the launch date).
FLOAT_PROJECTION_SPOT = "spot"
FLOAT_PROJECTION_NEG_HOLD = "neg_hold"
FLOAT_PROJECTION_NEG_HOLD_BLEND = "neg_hold_blend13"
FLOAT_PROJECTION_BLEND13 = "blend13"          # monthly-reset PQ1 + spot after; NO negative-margin hold
FLOAT_PROJECTION_FLAT_C0 = "flat_c0"          # launch coupon held flat PQ1–9 for EVERY floater
FLOAT_PROJECTION_MODES = (FLOAT_PROJECTION_SPOT, FLOAT_PROJECTION_NEG_HOLD, FLOAT_PROJECTION_NEG_HOLD_BLEND,
                          FLOAT_PROJECTION_BLEND13, FLOAT_PROJECTION_FLAT_C0)

# PID-SEC-5 (user-confirmed): SECURITY_DESCRIPTION_1 -> (model, agency_prepayment).
# Exactly the confirmed categories; anything else errors (never defaulted).
CATEGORY_MODEL_MAP: Mapping[str, tuple[str, bool]] = {
    "US Treasuries & Agencies": (MODEL_UST, False),
    "Agency MBS": (MODEL_MBS, True),
    "CMBS": (MODEL_MBS, False),
    "Domestic Non-Agency RMBS (incl HEL ABS)": (MODEL_MBS, False),
    "Foreign RMBS": (MODEL_MBS, False),
    "Corporate Bond": (MODEL_OTHER_SEC, False),
    "Sovereign Bond": (MODEL_OTHER_SEC, False),
    "Municipal Bond": (MODEL_OTHER_SEC, False),
    "CLO": (MODEL_OTHER_SEC, False),
    "Auto ABS": (MODEL_OTHER_SEC, False),
    "Student Loan ABS": (MODEL_OTHER_SEC, False),
    "Other ABS (excl HEL ABS)": (MODEL_OTHER_SEC, False),
    "Auction Rate Securities": (MODEL_OTHER_SEC, False),
    "Mutual Fund": (OUT_OF_SCOPE, False),
    "Common Stock (Equity)": (OUT_OF_SCOPE, False),
}

ACCOUNTING_INTENT_EQUITY = "EQ"


def assign_model(category: str) -> tuple[str, bool]:
    """PID-SEC-5 assignment; unknown categories surface as hard errors."""
    key = category.strip()
    if key not in CATEGORY_MODEL_MAP:
        raise ValidationFailure(
            f"security_description_1 category {category!r} is not in the confirmed PID-SEC-5 "
            f"mapping — surfaced for user clarification, never defaulted "
            f"(known: {sorted(CATEGORY_MODEL_MAP)})"
        )
    return CATEGORY_MODEL_MAP[key]


@dataclass(frozen=True)
class SecurityPosition:
    """One security in canonical units.

    `coupon_rate` is the launch-point coupon (annualized decimal; user-stated
    never blank in the delivered data — a missing coupon on `ii_ust` errors,
    OQ-027). `maturity_quarters` is relative to PQ0 (>= 1). `face_path` exists
    only for Agency-prepayment securities (PID-MBS-1): PQ0..PQ9 projected
    current face in USD millions. `ac_proxied` marks PID-SEC-3 securities
    (amortized cost proxied from price/100 x face; accretion forced to zero)."""

    security_id: str
    model: str
    category: str
    rate_type: str
    accounting_intent: str
    current_face: float
    amortized_cost: float
    coupon_rate: float | None = None
    book_yield: float | None = None
    coupon_floor: float | None = None
    maturity_quarters: int | None = None   # event timing (maturity → reinvestment): ceil(4 × years)
    maturity_years: float | None = None    # PID-SEC-8 accretion denominators: day difference / 365
    wal_years: float | None = None
    face_path: Mapping[int, float] | None = None
    ac_proxied: bool = False
    reference_income: Mapping[int, float] | None = None   # verification only — the workbook's own
                                                          # per-security II_PQ1..PQ9 (USD millions);
                                                          # never consumed by the models
    excel_rate_label: str | None = None                   # verification only — the workbook's own
                                                          # float/fixed indicator (PID-SEC-9); never
                                                          # drives model assignment until a PID adopts it
    excel_coupon_rate: float | None = None                # verification only — the workbook's own
                                                          # coupon column (PID-SEC-9, decimal), carried
                                                          # even when the ITO coupon drives the model
                                                          # (source-difference diagnostics)

    def __post_init__(self) -> None:
        require_id("security_id", self.security_id)
        if self.model not in (MODEL_UST, MODEL_MBS, MODEL_OTHER_SEC):
            raise ValidationFailure(f"{self.security_id}: model must be one of the three securities models, got {self.model!r}")
        require_id("category", self.category)
        if self.rate_type not in _RATE_TYPES:
            raise ValidationFailure(f"{self.security_id}: rate_type must be one of {_RATE_TYPES}, got {self.rate_type!r}")
        if self.accounting_intent.strip().upper() == ACCOUNTING_INTENT_EQUITY:
            raise ValidationFailure(f"{self.security_id}: equity-intent positions are out of scope (PID-SEC-5) — exclude at the loader")
        object.__setattr__(self, "current_face", check_balance(f"{self.security_id}.current_face", self.current_face))
        object.__setattr__(self, "amortized_cost", check_balance(f"{self.security_id}.amortized_cost", self.amortized_cost))
        for name in ("coupon_rate", "book_yield", "coupon_floor", "excel_coupon_rate"):
            value = getattr(self, name)
            if value is not None:
                object.__setattr__(self, name, check_rate(f"{self.security_id}.{name}", value))
        if self.maturity_quarters is not None:
            m = check_finite(f"{self.security_id}.maturity_quarters", self.maturity_quarters)
            if m < 1 or m != int(m):
                raise ValidationFailure(f"{self.security_id}: maturity_quarters must be a whole number >= 1, got {m}")
            object.__setattr__(self, "maturity_quarters", int(m))
        if self.maturity_years is not None:
            years = check_finite(f"{self.security_id}.maturity_years", self.maturity_years)
            if years <= 0.0:
                raise ValidationFailure(f"{self.security_id}: maturity_years must be > 0, got {years}")
            object.__setattr__(self, "maturity_years", years)
        if self.wal_years is not None:
            w = check_finite(f"{self.security_id}.wal_years", self.wal_years)
            if w <= 0.0:
                raise ValidationFailure(
                    f"{self.security_id}: wal_years must be > 0 (negative/zero WAL rows are "
                    f"skipped with a highlighted warning at the loader — user-parked 2026-07-24)"
                )
            object.__setattr__(self, "wal_years", w)
        if self.face_path is not None:
            object.__setattr__(
                self, "face_path",
                freeze_path(f"{self.security_id}.face_path", self.face_path,
                            SCENARIO_QUARTERS_WITH_LAUNCH, check_balance),
            )
        if self.reference_income is not None:
            object.__setattr__(
                self, "reference_income",
                freeze_path(f"{self.security_id}.reference_income", self.reference_income,
                            PROJECTION_QUARTERS, check_finite),   # sign-unconstrained
            )
        if self.rate_type == RATE_ZERO_COUPON and self.coupon_rate not in (None, 0.0):
            raise ValidationFailure(f"{self.security_id}: zero-coupon security carries a nonzero coupon_rate {self.coupon_rate}")


@dataclass(frozen=True)
class SecuritiesInputs:
    """All in-scope positions for one firm run, grouped by model (loader output)."""

    firm_id: str
    ust: tuple[SecurityPosition, ...]
    mbs: tuple[SecurityPosition, ...]
    other_sec: tuple[SecurityPosition, ...]
    warnings: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        require_id("firm_id", self.firm_id)
        for group, model in (("ust", MODEL_UST), ("mbs", MODEL_MBS), ("other_sec", MODEL_OTHER_SEC)):
            positions = tuple(getattr(self, group))
            object.__setattr__(self, group, positions)
            for pos in positions:
                if pos.model != model:
                    raise ValidationFailure(f"{pos.security_id}: model {pos.model!r} placed in the {group!r} group")
            ids = [p.security_id for p in positions]
            if len(ids) != len(set(ids)):
                raise ValidationFailure(f"duplicate security_id in the {group!r} group")
        object.__setattr__(self, "warnings", tuple(str(w) for w in self.warnings))


@dataclass(frozen=True)
class SecuritiesQuarterDiagnostics:
    """Per-quarter aggregate decomposition for one securities model."""

    coupon_accrual: float                # cash-coupon leg (incl. floating/floored coupons)
    accretion: float                     # accretion/amortization leg (EI residual, SL, zero-coupon accrual)
    reinvested_income: float             # 1Y-Treasury reinvestment tranches (fixed coupon per tranche)
    reinvested_balance: float            # ledger balance earning in this quarter
    matured_face: float                  # face maturing THIS quarter (reinvests from the next quarter)
    securities_alive: int

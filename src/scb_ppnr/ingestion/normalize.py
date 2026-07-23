"""Normalization at the ingestion boundary: quarter arithmetic and declared-scale
conversion.

Percent vs decimal for rates, and millions vs billions for money (D-006), are metadata
the config or tidy sheet must declare — never guessed (conventions §2). TO_BE_CONFIRMED
placeholders are refused at load time, so open input gates (the PID-OB-4 BBB
confirmations, the OQ-023 FRB-total source) block execution instead of letting
unconfirmed data through."""

from __future__ import annotations

import datetime as _dt
import re
from dataclasses import dataclass

from ..core.schemas import ValidationFailure

TO_BE_CONFIRMED = "TO_BE_CONFIRMED"
SCALE_PERCENT = "percent"
SCALE_DECIMAL = "decimal"
SCALE_MILLIONS = "millions"
SCALE_BILLIONS = "billions"


@dataclass(frozen=True, order=True)
class Quarter:
    year: int
    quarter: int  # 1..4

    def offset_from(self, other: "Quarter") -> int:
        return (self.year - other.year) * 4 + (self.quarter - other.quarter)

    def __str__(self) -> str:
        return f"{self.year}Q{self.quarter}"


_YEAR_Q = re.compile(r"^\s*(\d{4})\s*[-_ ]?\s*[Qq]([1-4])\s*$")
_Q_YEAR = re.compile(r"^\s*[Qq]([1-4])\s*[-_ ]?\s*(\d{4})\s*$")
_ISO_DATE = re.compile(r"^\s*(\d{4})-(\d{2})(?:-(\d{2}))?\s*(?:[T ].*)?$")


def parse_quarter(value: object, *, context: str) -> Quarter:
    """Accepts quarter labels ('2025Q4', 'Q4 2025'), ISO dates ('2025-12' /
    '2025-12-31'), and date/datetime cells (as returned by workbook readers)."""
    if isinstance(value, (_dt.datetime, _dt.date)):
        return Quarter(value.year, (value.month - 1) // 3 + 1)
    if isinstance(value, str):
        match = _YEAR_Q.match(value)
        if match:
            return Quarter(int(match.group(1)), int(match.group(2)))
        match = _Q_YEAR.match(value)
        if match:
            return Quarter(int(match.group(2)), int(match.group(1)))
        match = _ISO_DATE.match(value)
        if match and 1 <= int(match.group(2)) <= 12:
            return Quarter(int(match.group(1)), (int(match.group(2)) - 1) // 3 + 1)
    raise ValidationFailure(
        f"{context}: cannot interpret {value!r} as a quarter "
        f"(accepted: 2025Q4, Q4 2025, 2025-12, 2025-12-31, or a date cell)"
    )


def require_confirmed(setting: str, value: object, *, gate: str) -> str:
    """Reject blank or TO_BE_CONFIRMED settings — unconfirmed physical mappings
    must block a run, never be guessed."""
    if not isinstance(value, str) or not value.strip() or value.strip().upper() == TO_BE_CONFIRMED:
        raise ValidationFailure(f"{setting} is {value!r} — must be confirmed before use ({gate}); refusing to guess")
    return value.strip()


def to_float(raw: object, *, context: str) -> float:
    if isinstance(raw, bool):
        raise ValidationFailure(f"{context}: {raw!r} is not a number")
    if isinstance(raw, (int, float)):
        return float(raw)
    if isinstance(raw, str):
        text = raw.strip().replace(",", "")
        if text:
            try:
                return float(text)
            except ValueError:
                pass
    raise ValidationFailure(f"{context}: {raw!r} is not a number")


def apply_rate_scale(scale: object, value: float, *, context: str) -> float:
    """Convert a rate/share/spread to the canonical annualized-decimal scale using
    its *declared* scale. Missing or unconfirmed scale is an error, not a default."""
    declared = require_confirmed(
        f"{context}: scale", scale, gate="rate scale is metadata-driven, never assumed — conventions §2"
    ).lower()
    if declared == SCALE_PERCENT:
        return value / 100.0
    if declared == SCALE_DECIMAL:
        return value
    raise ValidationFailure(f"{context}: scale must be '{SCALE_PERCENT}' or '{SCALE_DECIMAL}', got {scale!r}")


def apply_money_scale(scale: object, value: float, *, context: str) -> float:
    """Convert a balance or dollar amount to the canonical USD-millions unit using its
    *declared* unit (D-006). Physical sources disagree — Schedule G balances arrive in
    millions, FRB projection paths in billions — so an undeclared money unit is an
    error, never a default."""
    declared = require_confirmed(
        f"{context}: scale", scale, gate="money unit is metadata-driven, never assumed — D-006"
    ).lower()
    if declared == SCALE_MILLIONS:
        return value
    if declared == SCALE_BILLIONS:
        return value * 1000.0
    raise ValidationFailure(f"{context}: scale must be '{SCALE_MILLIONS}' or '{SCALE_BILLIONS}', got {scale!r}")

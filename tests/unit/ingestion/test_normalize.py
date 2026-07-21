"""Quarter parsing and declared-scale normalization at the ingestion boundary."""

from __future__ import annotations

import datetime

import pytest

from scb_ppnr.ingestion.normalize import (
    Quarter,
    apply_money_scale,
    apply_rate_scale,
    parse_quarter,
    to_float,
)
from scb_ppnr.interest_expense import ValidationFailure


@pytest.mark.parametrize(
    "value",
    ["2025Q4", "2025 Q4", "2025-Q4", "q4 2025", "Q4-2025", "2025-12", "2025-12-31",
     datetime.date(2025, 12, 31), datetime.datetime(2025, 10, 1, 12, 0)],
)
def test_parse_quarter_accepted_forms(value):
    assert parse_quarter(value, context="t") == Quarter(2025, 4)


@pytest.mark.parametrize("value", ["banana", "2025Q5", "2025-13-01", None, 20254])
def test_parse_quarter_rejects_garbage(value):
    with pytest.raises(ValidationFailure, match="cannot interpret"):
        parse_quarter(value, context="t")


def test_quarter_offsets():
    launch = Quarter(2025, 4)
    assert Quarter(2025, 4).offset_from(launch) == 0
    assert Quarter(2026, 1).offset_from(launch) == 1
    assert Quarter(2028, 1).offset_from(launch) == 9
    assert Quarter(2025, 2).offset_from(launch) == -2


def test_apply_rate_scale_percent_and_decimal():
    assert apply_rate_scale("percent", 4.25, context="t") == pytest.approx(0.0425)
    assert apply_rate_scale("decimal", 0.0425, context="t") == 0.0425
    assert apply_rate_scale("Percent", 100.0, context="t") == pytest.approx(1.0)


@pytest.mark.parametrize("scale", [None, "", "TO_BE_CONFIRMED", "to_be_confirmed"])
def test_apply_rate_scale_refuses_undeclared(scale):
    with pytest.raises(ValidationFailure, match="must be confirmed"):
        apply_rate_scale(scale, 1.0, context="t")


def test_apply_rate_scale_rejects_unknown_unit():
    with pytest.raises(ValidationFailure, match="percent.*decimal"):
        apply_rate_scale("bps", 1.0, context="t")


def test_apply_money_scale_millions_and_billions():
    assert apply_money_scale("millions", 1000.0, context="t") == 1000.0
    assert apply_money_scale("billions", 0.04, context="t") == pytest.approx(40.0)
    assert apply_money_scale("Billions", 2.0, context="t") == pytest.approx(2000.0)


@pytest.mark.parametrize("scale", [None, "", "TO_BE_CONFIRMED", "to_be_confirmed"])
def test_apply_money_scale_refuses_undeclared(scale):
    with pytest.raises(ValidationFailure, match="must be confirmed"):
        apply_money_scale(scale, 1.0, context="t")


def test_apply_money_scale_rejects_unknown_unit():
    with pytest.raises(ValidationFailure, match="millions.*billions"):
        apply_money_scale("thousands", 1.0, context="t")


def test_to_float():
    assert to_float("1,000.5", context="t") == 1000.5
    assert to_float(3, context="t") == 3.0
    for bad in ("x", "", None, True):
        with pytest.raises(ValidationFailure, match="not a number"):
            to_float(bad, context="t")

"""The shared PQ1..PQ9 report-table layout (core.common.format_path_row /
format_path_header): columns are space-joined so they can never fuse — the
regression this pins is the old fixed-width concatenation running five-digit
values together ("10000.0002000.000"). Also pinned: header/row alignment for
in-width values and thousands grouping."""

from __future__ import annotations

from scb_ppnr.core.common import format_path_header, format_path_row
from scb_ppnr.core.schemas import PROJECTION_QUARTERS


def _flat(value: float) -> dict[int, float]:
    return {q: value for q in PROJECTION_QUARTERS}


def test_five_digit_columns_stay_separated():
    path = {q: 10000.0 * q for q in PROJECTION_QUARTERS}  # 10,000 .. 90,000
    row = format_path_row("ii_loans", path)
    assert "10,000.000" in row and "20,000.000" in row
    assert "10,000.00020,000.000" not in row
    # label field, then exactly ten space-separated cells (nine quarters + total)
    assert len(row[22:].split()) == 10


def test_any_magnitude_keeps_ten_cells():
    path = dict(_flat(-1234567.891))
    path[5] = 0.0
    assert len(format_path_row("x", path)[22:].split()) == 10


def test_header_aligns_with_in_width_rows():
    header = format_path_header("model")
    row = format_path_row("ie_dom_time_dep", _flat(1234.5))
    assert len(header) == len(row)
    assert header.startswith("model")
    assert header.rstrip().endswith("total")
    assert "1,234.500" in row


def test_explicit_total_overrides_the_sum():
    row = format_path_row("gap", _flat(1.0), total=42.0)
    assert row.rstrip().endswith("42.000")

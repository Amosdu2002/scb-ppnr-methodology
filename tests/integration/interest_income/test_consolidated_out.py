"""run_nii --consolidated-out writes the results workbook (Summary / Income /
Expense sheets) and its flat CSV twin. Pinned here: both files appear on the
synthetic demo with the expected sheet set and row labels; the Income sheet's
'sum of siblings' row is the column-sum of the six sibling rows; every CSV data
row carries sheet, series, nine quarters, and a total equal to the row sum;
--skip-expense drops the Expense sheet; existing invocations without the flag
are untouched."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "examples"))

import run_nii  # noqa: E402

SIBLINGS = ("ii_loans", "ii_dep_banks_other", "ii_ust", "ii_mbs",
            "ii_other_sec", "ii_other_ida")


def _rows(sheet):
    return [[cell.value for cell in row] for row in sheet.iter_rows()]


def test_demo_writes_workbook_and_csv_twin(tmp_path):
    openpyxl = pytest.importorskip("openpyxl")
    target = tmp_path / "results.xlsx"
    assert run_nii.main(["--consolidated-out", str(target)]) == 0
    assert target.exists()
    assert (tmp_path / "results.csv").exists()

    book = openpyxl.load_workbook(target)
    assert book.sheetnames == ["Summary", "Income", "Expense"]

    income = {row[0]: row for row in _rows(book["Income"]) if row and row[0]}
    for label in (*SIBLINGS, "sum of siblings", "nii_trading_al (modeled)",
                  "implied trading (round-0 diagnostic)", "total interest income",
                  "frb_total_interest_income (target)"):
        assert label in income, label
    for column in range(1, 11):
        sibling_sum = sum(income[name][column] for name in SIBLINGS)
        assert income["sum of siblings"][column] == pytest.approx(sibling_sum)

    summary = {row[0] for row in _rows(book["Summary"]) if row and row[0]}
    assert "combined-NII monitor: within 1% identity guard" in summary
    assert "alpha_b — nii_trading_al (annualized, PID-TRD-3 basis)" in summary
    assert "alpha_b — ie_other_borrowing (annualized)" in summary

    expense = {row[0] for row in _rows(book["Expense"]) if row and row[0]}
    assert "ie_other_borrowing" in expense
    assert "frb_total_interest_expense (target)" in expense


def test_csv_rows_are_labeled_and_sum_to_their_total(tmp_path):
    target = tmp_path / "results.xlsx"
    run_nii.main(["--consolidated-out", str(target)])
    lines = (tmp_path / "results.csv").read_text(encoding="utf-8").splitlines()
    assert lines[0] == ("sheet,series," + ",".join(f"PQ{q}" for q in range(1, 10))
                       + ",total_9q")
    assert any(line.startswith("Income,ii_ust,") for line in lines)
    assert any(line.startswith("Expense,ie_dom_time_dep,") for line in lines)
    for line in lines[1:]:
        cells = line.split(",")
        assert len(cells) == 12, line
        quarters = [float(cell) for cell in cells[2:11]]
        # both sides are %.6f-rounded independently: allow nine half-ulps
        assert float(cells[11]) == pytest.approx(sum(quarters), abs=5e-6)


def test_skip_expense_drops_the_expense_sheet(tmp_path):
    openpyxl = pytest.importorskip("openpyxl")
    target = tmp_path / "results.xlsx"
    assert run_nii.main(["--skip-expense", "--consolidated-out", str(target)]) == 0
    book = openpyxl.load_workbook(target)
    assert book.sheetnames == ["Summary", "Income"]
    csv_text = (tmp_path / "results.csv").read_text(encoding="utf-8")
    assert "Expense," not in csv_text


def test_flag_absent_means_no_consolidated_files(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert run_nii.main([]) == 0
    assert not list(tmp_path.glob("results.*"))

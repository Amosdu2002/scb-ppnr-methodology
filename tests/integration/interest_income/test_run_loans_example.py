"""The loans runner's synthetic demo must stay runnable.

The demo is the smoke path a first company run follows — same code, invented
numbers — so it is executed here rather than trusted."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "examples"))


def test_synthetic_demo_runs_and_reports(tmp_path, capsys):
    import run_loans

    report = tmp_path / "loans_report.txt"
    assert run_loans.main(["--report", str(report)]) == 0

    printed = capsys.readouterr().out
    for marker in (
        "SYNTHETIC DEMO",
        "LOANS LOADER CENSUS",
        "LAUNCH-POINT DIAGNOSTICS",
        "MERGED 9/10/11 BUCKET",
        "PROJECTION DIAGNOSTICS",
        "PROJECTED CORPORATE LOAN INTEREST INCOME",
        "TOTAL",
    ):
        assert marker in printed
    # the merged bucket borrows the depository rate, not the 9% nondepository row
    assert "donor pool rate (depository floating) : 5.5000%" in printed
    assert report.exists()


def test_projection_quarter_index_matches_the_launch_point():
    import datetime as dt

    from scb_ppnr.interest_income.loans_schemas import projection_quarter_index

    assert projection_quarter_index(dt.date(2025, 2, 1), "2024Q4") == 1
    assert projection_quarter_index(dt.date(2027, 1, 15), "2024Q4") == 9
    assert projection_quarter_index(dt.date(2027, 4, 1), "2024Q4") is None   # PQ10
    assert projection_quarter_index(dt.date(2024, 11, 1), "2024Q4") is None  # PQ0 itself
    assert projection_quarter_index(dt.date(2019, 1, 1), "2024Q4") is None   # history

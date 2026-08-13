"""The NII compare runner's synthetic demo must stay runnable end-to-end, and
the family runners' --paths-out exports must produce CSVs it accepts — the
company round-1 workflow is exactly this chain, so it is executed here rather
than trusted."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "examples"))

from scb_ppnr.core.schemas import PROJECTION_QUARTERS, ValidationFailure  # noqa: E402


def test_synthetic_demo_runs_and_reports(tmp_path, capsys):
    import run_nii

    report = tmp_path / "nii_report.txt"
    assert run_nii.main(["--report", str(report)]) == 0

    printed = capsys.readouterr().out
    for marker in (
        "SYNTHETIC DEMO",
        "NetTA 1,000.0 (PID-TRD-2; flat)",
        "COMPONENT INCOME PATHS",
        "ROUND-0 DIAGNOSTIC",
        "implied TATL",
        "Trading NII calibration (PID-TRD-1, annualized basis PID-TRD-3)",
        "alpha_b",
        "NII TATL",                    # the reference tab's modeled row label
        "Implied FRB results",         # the reference tab's implied row label
        "Family reconciliation: seven-component total",
        "within tolerance: True",
        "Combined NII",
        "Cumulative gap within the 1% identity guard: True",
    ):
        assert marker in printed
    body = report.read_text(encoding="utf-8")
    assert "ROUND-0 DIAGNOSTIC" in body
    assert "Combined NII" in body


def test_demo_skip_expense_flag(capsys):
    import run_nii

    assert run_nii.main(["--skip-expense"]) == 0
    printed = capsys.readouterr().out
    assert "COMBINED NII: skipped (--skip-expense)" in printed
    assert "Family reconciliation" in printed


def test_company_run_requires_component_paths(tmp_path, capsys):
    import run_nii

    config = ROOT / "examples" / "synthetic_config.toml"
    assert run_nii.main(["--config", str(config)]) == 1
    printed = capsys.readouterr().out
    assert "--component-paths is required" in printed


def test_loans_paths_out_feeds_run_nii(tmp_path, capsys):
    import run_loans
    import run_nii

    loans_csv = tmp_path / "loans_paths.csv"
    assert run_loans.main(["--paths-out", str(loans_csv)]) == 0
    text = loans_csv.read_text(encoding="utf-8")
    assert text.splitlines()[0] == "component," + ",".join(f"PQ{q}" for q in PROJECTION_QUARTERS)
    assert "ii_loans_corporate," in text
    assert "ii_loans_cre," in text
    assert "\nii_loans," in text        # the total row (full wholesale demo run)
    capsys.readouterr()

    # The demo synthetic loans workbook has no retail sheets, so the CSV carries
    # wholesale parts + total; run_nii accepts it merged with securities-style
    # rows from the committed synthetic file.
    sec_csv = tmp_path / "securities_paths.csv"
    sec_csv.write_text(
        "component," + ",".join(f"PQ{q}" for q in PROJECTION_QUARTERS) + "\n"
        + "ii_ust," + ",".join(["12"] * 9) + "\n"
        + "ii_mbs," + ",".join(["6"] * 9) + "\n"
        + "ii_other_sec," + ",".join(["5"] * 9) + "\n",
        encoding="utf-8",
    )
    assert run_nii.main(["--component-paths", str(loans_csv), str(sec_csv)]) == 0
    printed = capsys.readouterr().out
    assert "using the total row" in printed
    assert "Family reconciliation: seven-component total" in printed


def test_component_paths_reader_rejects_defects(tmp_path):
    import run_nii

    header = "component," + ",".join(f"PQ{q}" for q in PROJECTION_QUARTERS) + "\n"
    bad_header = tmp_path / "bad_header.csv"
    bad_header.write_text("component,PQ1\nii_ust,1\n", encoding="utf-8")
    with pytest.raises(ValidationFailure, match="header"):
        run_nii.read_component_paths([bad_header])

    unknown = tmp_path / "unknown.csv"
    unknown.write_text(header + "ii_dep_banks_other," + ",".join(["1"] * 9) + "\n", encoding="utf-8")
    with pytest.raises(ValidationFailure, match="unknown component"):
        run_nii.read_component_paths([unknown])

    duplicate = tmp_path / "duplicate.csv"
    duplicate.write_text(
        header + "ii_ust," + ",".join(["1"] * 9) + "\n" + "ii_ust," + ",".join(["2"] * 9) + "\n",
        encoding="utf-8",
    )
    with pytest.raises(ValidationFailure, match="duplicate component"):
        run_nii.read_component_paths([duplicate])


def test_securities_paths_out_bases(tmp_path, capsys):
    pytest.importorskip("openpyxl")
    import run_securities

    xr_csv = tmp_path / "sec_xr.csv"
    full_csv = tmp_path / "sec_full.csv"
    run_securities.main(["--paths-out", str(xr_csv)])                       # default basis: xr
    run_securities.main(["--paths-out", str(full_csv), "--paths-basis", "full"])
    capsys.readouterr()

    import run_nii
    xr = run_nii.read_component_paths([xr_csv])
    full = run_nii.read_component_paths([full_csv])
    assert set(xr) == {"ii_ust", "ii_mbs", "ii_other_sec"}
    # full ≥ xr in every quarter (full adds reinvestment income back).
    for model_id in xr:
        for q in PROJECTION_QUARTERS:
            assert full[model_id][q] >= xr[model_id][q] - 1e-9
    # The demo UST matures inside the horizon and reinvests, so the two bases
    # genuinely differ somewhere.
    assert any(
        full[m][q] > xr[m][q] + 1e-9 for m in xr for q in PROJECTION_QUARTERS
    )

"""run.py chains the four stage runners in-process (loans -> securities ->
expense -> nii) into one artifact directory. Pinned here: the synthetic demo
chain exits 0 with every artifact present and each stage's signature marker in
the stream; --check validates without running anything; --only subsets keep the
canonical order; a config that fits none of the asset stages fails those stages,
still runs expense, skips nii (missing CSVs), and exits 1; --quiet moves stage
bodies into out/<stage>.log. The per-stage OUTPUT content is pinned by the
stage runners' own tests (test_run_loans_example / test_run_nii_example) — this
file pins only the chaining contract."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

import run  # noqa: E402  (run.py bootstraps src/ and examples/ itself)

EXPECTED_ARTIFACTS = (
    "loans_report.txt", "loans_paths.csv",
    "securities_report.txt", "securities_paths.csv",
    "expense_report.txt", "nii_report.txt",
    "results.xlsx", "results.csv",
    "effective_config.txt", "run_summary.txt",
)


def test_synthetic_chain_runs_all_stages(tmp_path, capsys):
    pytest.importorskip("openpyxl")
    out = tmp_path / "r1"
    assert run.main(["--out", str(out)]) == 0
    stream = capsys.readouterr().out
    for marker in (
        "SYNTHETIC DEMO CHAIN",
        "PROJECTED CORPORATE LOAN INTEREST INCOME",   # loans
        "9-quarter cumulative income:",               # securities
        "alpha_b",                                    # expense (family_report)
        "Cumulative gap within the 1% identity guard: True",  # nii monitor
        "PIPELINE: OK",
    ):
        assert marker in stream, marker
    for name in EXPECTED_ARTIFACTS:
        assert (out / name).exists(), name
    header = (out / "loans_paths.csv").read_text(encoding="utf-8").splitlines()[0]
    assert header == "component,PQ1,PQ2,PQ3,PQ4,PQ5,PQ6,PQ7,PQ8,PQ9"


def test_check_mode_validates_without_running(tmp_path, capsys):
    out = tmp_path / "never"
    assert run.main(["--check", "--out", str(out)]) == 0
    stream = capsys.readouterr().out
    assert "EFFECTIVE CONFIG" in stream
    assert "synthetic_severely_adverse" in stream
    assert "CONFIG OK" in stream
    assert not out.exists()

    bad = tmp_path / "bad.toml"
    bad.write_text("[bogus]\nx = 1\n", encoding="utf-8")
    assert run.main(["--check", "--config", str(bad)]) == 1
    assert "CONFIG CHECK FAILED" in capsys.readouterr().out


def test_only_subset_runs_selected_stage(tmp_path, capsys):
    out = tmp_path / "r2"
    assert run.main(["--out", str(out), "--only", "expense"]) == 0
    stream = capsys.readouterr().out
    assert "skipped (not selected)" in stream
    assert "PIPELINE: OK" in stream
    assert (out / "expense_report.txt").exists()
    assert not (out / "loans_report.txt").exists()


def test_company_config_failure_propagation(tmp_path, capsys):
    # synthetic_config.toml has [mev] + spot/quarterly but no [firm_data.loans]
    # or [firm_data.securities]: both asset stages fail before touching any
    # workbook, expense still runs, nii is gated off by the missing CSVs.
    out = tmp_path / "r3"
    rc = run.main(["--out", str(out),
                   "--config", str(ROOT / "examples" / "synthetic_config.toml")])
    assert rc == 1
    stream = capsys.readouterr().out
    assert "no [firm_data.loans] section" in stream
    assert "VALIDATION FAILURE" in stream
    assert "skipped (missing" in stream
    assert "PIPELINE: FAILED" in stream
    assert (out / "expense_report.txt").exists()
    assert not (out / "loans_paths.csv").exists()
    assert not (out / "securities_paths.csv").exists()


def test_quiet_redirects_stage_output_to_logs(tmp_path, capsys):
    pytest.importorskip("openpyxl")
    out = tmp_path / "r4"
    assert run.main(["--out", str(out), "--only", "loans", "--quiet"]) == 0
    stream = capsys.readouterr().out
    assert "LOANS LOADER CENSUS" not in stream
    assert "RUN SUMMARY" in stream
    log = (out / "loans.log").read_text(encoding="utf-8")
    assert "LOANS LOADER CENSUS" in log

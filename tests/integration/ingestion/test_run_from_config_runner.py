"""The modernized expense runner contract: examples/run_from_config.py exposes
main(argv) -> int like its pipeline siblings, prints the family report for the
synthetic demo, writes --report (even content on success), and turns a config
without [mev] into exit 1 with the standard VALIDATION FAILURE trailer instead
of a bare SystemExit."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "examples"))

import run_from_config  # noqa: E402


def test_synthetic_demo_exits_zero_and_prints_the_family_report(capsys):
    assert run_from_config.main([]) == 0
    stream = capsys.readouterr().out
    assert "firm=SYNTHETIC_FIRM" in stream
    assert "alpha_b" in stream


def test_report_flag_writes_the_report_file(tmp_path, capsys):
    report = tmp_path / "expense_report.txt"
    assert run_from_config.main(["--report", str(report)]) == 0
    body = report.read_text(encoding="utf-8")
    assert "alpha_b" in body
    assert "generated " in body
    assert "report written to" in capsys.readouterr().out


def test_config_without_mev_fails_with_validation_trailer(tmp_path, capsys):
    config = tmp_path / "no_mev.toml"
    config.write_text('[firm_data]\nfirm_id = "X"\n', encoding="utf-8")
    assert run_from_config.main(["--config", str(config)]) == 1
    stream = capsys.readouterr().out
    assert "VALIDATION FAILURE" in stream
    assert "no [mev] section" in stream

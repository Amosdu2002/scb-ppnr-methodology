"""The [firm_data.loans] config section (PID-LOAN-8).

Everything physical is config — workbook path, sheet names, header geometry,
unit scales, launch point, scenario — so a run is reproducible from its config
file alone and nothing load-bearing hides in CLI flags."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

from scb_ppnr.core.schemas import ValidationFailure
from scb_ppnr.ingestion.config import load_config
from scb_ppnr.ingestion.firm_data_loader import load_family_inputs

ROOT = Path(__file__).resolve().parents[3]


def _config(tmp_path: Path, body: str) -> Path:
    path = tmp_path / "company.toml"
    path.write_text(body, encoding="utf-8")
    return path


LOANS_BLOCK = """
[firm_data]
firm_id = "SYNTH"

[firm_data.loans]
workbook = "corp.xlsx"
launch_point = "2024Q4"
scenario = "Supervisory Severely Adverse"
h1_sheet = "CORP H.1 v2"
h1_header_row = 6
m1_domestic_value_column_indices = [4, 6]
col_facility_id = "Obligor ID"
"""


def test_full_section_parses_with_coercions_and_resolved_workbook(tmp_path):
    config = load_config(_config(tmp_path, LOANS_BLOCK))
    loans = config.firm_data.loans

    assert loans.spec.workbook == tmp_path / "corp.xlsx"     # resolved against the config dir
    assert loans.spec.h1_sheet == "CORP H.1 v2"
    assert loans.spec.h1_header_row == 6                     # int coerced
    assert loans.spec.m1_domestic_value_column_indices == (4, 6)   # array -> tuple
    assert loans.spec.col_facility_id == "Obligor ID"
    assert loans.spec.mev_history_scenario == "Actual"       # untouched default
    assert loans.scenario == "Supervisory Severely Adverse"
    assert loans.launch_point == "2024Q4"
    assert loans.floor_collapse == "balance_weighted"        # default


def test_launch_point_is_required_because_it_is_data_tied(tmp_path):
    body = '[firm_data]\nfirm_id = "S"\n[firm_data.loans]\nworkbook = "corp.xlsx"\n'
    with pytest.raises(ValidationFailure, match="launch_point"):
        load_config(_config(tmp_path, body))


def test_a_typoed_sheet_key_is_refused_not_ignored(tmp_path):
    """The whole point of config-first: a typo'd key must never look configured
    while the default quietly loads instead."""
    body = LOANS_BLOCK + 'h1_shet = "CORP H.1"\n'
    with pytest.raises(ValidationFailure, match="unknown key 'h1_shet'"):
        load_config(_config(tmp_path, body))


def test_an_invalid_floor_collapse_is_refused(tmp_path):
    body = LOANS_BLOCK + 'floor_collapse = "median"\n'
    with pytest.raises(ValidationFailure, match="floor_collapse"):
        load_config(_config(tmp_path, body))


def test_a_loans_only_config_needs_no_expense_sheets(tmp_path):
    """The D-007 spot/quarterly pair belongs to the expense family; a loans-only
    config legitimately omits it — but the expense loader still refuses to run."""
    config = load_config(_config(tmp_path, LOANS_BLOCK))
    assert config.firm_data.spot is None and config.firm_data.quarterly is None

    with pytest.raises(ValidationFailure, match="expense-family run needs"):
        load_family_inputs(config)


def test_half_of_the_spot_quarterly_pair_is_still_an_error(tmp_path):
    body = (
        '[firm_data]\nfirm_id = "S"\n'
        '[firm_data.spot]\npath = "spot.csv"\n'
    )
    with pytest.raises(ValidationFailure, match=r"missing \[firm_data.quarterly\]"):
        load_config(_config(tmp_path, body))


def test_the_committed_template_carries_a_parseable_loans_section():
    config = load_config(ROOT / "config" / "company.template.toml")
    loans = config.firm_data.loans

    assert loans is not None
    assert loans.launch_point == "2024Q4"
    assert loans.spec.h1_sheet == "CORP H.1"
    assert loans.spec.mev_3m_column == "3-month Treasury rate"


def test_the_run_manifest_composes_bindings_and_the_methodology_switch():
    """Template supplies the physical bindings, models/loans.toml the
    floor_collapse switch; the merge produces one section with both."""
    config = load_config(ROOT / "config" / "runs" / "example.toml")
    loans = config.firm_data.loans

    assert loans.spec.h1_sheet == "CORP H.1"
    assert loans.floor_collapse == "balance_weighted"
    assert config.provenance["firm_data.loans.floor_collapse"] == "loans.toml"
    assert config.provenance["firm_data.loans.workbook"] == "company.template.toml"


def test_runner_takes_the_workbook_from_config_not_cli(tmp_path, capsys):
    sys.path.insert(0, str(ROOT / "examples"))
    import run_loans

    workbook = run_loans._synthetic_workbook(tmp_path)
    config = _config(tmp_path, f"""
[firm_data]
firm_id = "SYNTH"

[firm_data.loans]
workbook = "{workbook.name}"
launch_point = "2024Q4"
""")
    assert run_loans.main(["--config", str(config)]) == 0

    printed = capsys.readouterr().out
    assert "EFFECTIVE CONFIG" in printed
    assert "PROJECTED CORPORATE LOAN INTEREST INCOME" in printed
    assert "scenario      : Supervisory Severely Adverse" in printed


def test_runner_without_a_loans_section_points_at_the_template(tmp_path, capsys):
    """main() no longer raises: a ValidationFailure prints AFTER the sections
    that already emitted (so a deep failure can never hide the censuses that
    explain it), and the exit code is 1."""
    sys.path.insert(0, str(ROOT / "examples"))
    import run_loans

    config = _config(tmp_path, '[firm_data]\nfirm_id = "S"\n')
    assert run_loans.main(["--config", str(config)]) == 1
    printed = capsys.readouterr().out
    assert "VALIDATION FAILURE" in printed
    assert "no [firm_data.loans] section" in printed


def test_a_mid_run_failure_still_prints_the_census_and_writes_the_report(tmp_path, capsys):
    """The bug that hid the diagnostics on the company machine: sections used to
    print only at the very end, so a launch-point refusal showed nothing. Every
    section now prints as produced and lands in the report even on failure."""
    sys.path.insert(0, str(ROOT / "examples"))
    import run_loans

    workbook = run_loans._synthetic_workbook(tmp_path)   # lacks the outstanding columns
    report = tmp_path / "loans_report.txt"
    config = _config(tmp_path, f"""
[firm_data]
firm_id = "SYNTH"

[firm_data.loans]
workbook = "{workbook.name}"
launch_point = "2024Q4"
share_basis = "outstanding"
""")
    assert run_loans.main(["--config", str(config), "--report", str(report)]) == 1

    printed = capsys.readouterr().out
    assert "LOANS LOADER CENSUS" in printed                  # emitted BEFORE the failure
    assert "col_outstanding / col_value" in printed          # the configuration hint
    assert "VALIDATION FAILURE" in printed
    body = report.read_text()
    assert "LOANS LOADER CENSUS" in body and "VALIDATION FAILURE" in body


def test_balance_source_is_config_and_validated(tmp_path):
    config = load_config(_config(tmp_path, LOANS_BLOCK + 'balance_source = "h1_sum"\n'))
    assert config.firm_data.loans.balance_source == "h1_sum"

    with pytest.raises(ValidationFailure, match="balance_source must be"):
        load_config(_config(tmp_path, LOANS_BLOCK + 'balance_source = "schM"\n'))


def test_apply_scalar_and_results_sheet_are_config(tmp_path):
    """Reference-matching runs: the workbook's results carry no industry scalar
    (verified 2026-08-12), so the scalar is switchable and the results sheet
    nameable — both in config, not CLI."""
    body = LOANS_BLOCK + 'apply_scalar = false\nresults_sheet = "Results"\n'
    config = load_config(_config(tmp_path, body))

    assert config.firm_data.loans.apply_scalar is False
    assert config.firm_data.loans.spec.results_sheet == "Results"

    with pytest.raises(ValidationFailure, match="apply_scalar must be true or false"):
        load_config(_config(tmp_path, LOANS_BLOCK + 'apply_scalar = "yes"\n'))


def test_runner_compare_section_prints_when_results_sheet_is_configured(tmp_path, capsys):
    sys.path.insert(0, str(ROOT / "examples"))
    import openpyxl
    import run_loans

    workbook = run_loans._synthetic_workbook(tmp_path)
    book = openpyxl.load_workbook(workbook)
    sheet = book.create_sheet("Results")
    sheet.append([None, None, None] + [f"PQ{q}" for q in range(10)])
    sheet.append(["1 - HFI"])
    sheet.append([None, "x", "Fixed Income"] + [20e6] * 10)
    sheet.append([None, "x", "Variable Rate Income"] + [30e6, 25e6] + [20e6] * 8)
    sheet.append([None, "x", "Total"] + [55e6, 48e6] + [42e6] * 8)   # hidden mixed inside
    book.save(workbook)

    config = _config(tmp_path, f"""
[firm_data]
firm_id = "SYNTH"

[firm_data.loans]
workbook = "{workbook.name}"
launch_point = "2024Q4"
apply_scalar = false
results_sheet = "Results"
""")
    assert run_loans.main(["--config", str(config)]) == 0

    printed = capsys.readouterr().out
    assert "UNSCALED — apply_scalar = false" in printed
    assert "LOANS COMPARE" in printed
    assert "IMPLIED FROM THE PQ1->PQ2 SLOPE" in printed
    assert "GRAND (blocks present on both sides)" in printed


def test_share_basis_is_config_and_validated(tmp_path):
    config = load_config(_config(tmp_path, LOANS_BLOCK + 'share_basis = "outstanding"\n'))
    assert config.firm_data.loans.share_basis == "outstanding"

    config = load_config(_config(tmp_path, LOANS_BLOCK + 'share_basis = "utilized"\n'))
    assert config.firm_data.loans.share_basis == "utilized"

    with pytest.raises(ValidationFailure, match="share_basis must be"):
        load_config(_config(tmp_path, LOANS_BLOCK + 'share_basis = "drawn"\n'))

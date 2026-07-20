"""File-driven end-to-end: the committed synthetic config + CSVs must reproduce the
directly-constructed conftest fixture run, and the company template must refuse to
run while its gates say TO_BE_CONFIRMED."""

from __future__ import annotations

from pathlib import Path

import pytest

from scb_ppnr.ingestion import load_config, load_family_inputs, load_mev_scenario
from scb_ppnr.interest_expense import (
    MODEL_EXECUTION_ORDER,
    ValidationFailure,
    family_report,
    run_interest_expense_family,
)
from scb_ppnr.interest_expense.schemas import PROJECTION_QUARTERS

ROOT = Path(__file__).resolve().parents[3]


def test_synthetic_config_reproduces_direct_construction(make_family, make_scenario):
    config = load_config(ROOT / "examples" / "synthetic_config.toml")
    scenario = load_mev_scenario(config, "synthetic_severely_adverse").interest_expense_scenario_paths()
    family = load_family_inputs(config)
    from_files = run_interest_expense_family(family, scenario)

    reference = run_interest_expense_family(
        make_family(firm_id="SYNTHETIC_FIRM"),
        make_scenario(scenario_id="synthetic_severely_adverse"),
    )

    assert from_files.reconciliation.within_tolerance
    assert from_files.reconciliation.frb_total_cumulative == pytest.approx(360.0)
    for model_id in MODEL_EXECUTION_ORDER:
        for quarter in PROJECTION_QUARTERS:
            assert from_files.results[model_id].expense_path()[quarter] == pytest.approx(
                reference.results[model_id].expense_path()[quarter], rel=1e-12
            )
    assert from_files.calibration.alpha_b == pytest.approx(reference.calibration.alpha_b, rel=1e-12)

    report = family_report(from_files, family.frb_total_interest_expense)
    assert "alpha_b" in report and "SYNTHETIC_FIRM" in report


def test_company_template_parses_but_gates_block_execution():
    config = load_config(ROOT / "config" / "company.template.toml")
    assert config.mev is not None
    with pytest.raises(ValidationFailure, match="must be confirmed"):
        load_mev_scenario(config, "severely_adverse")

"""File-driven income run: the committed synthetic config + CSVs must reproduce
hand-calculated Family A goldens (dep-banks: 1000 × T3m/4; other-IDA: 2000 ×
[0.6·T3m + 0.4·T10y]/4 with the CSV percent paths), and the company template
must declare the four income series so its TO_BE_CONFIRMED gates cover them."""

from __future__ import annotations

from pathlib import Path

import pytest

from scb_ppnr.ingestion import load_config, load_income_inputs, load_mev_scenario
from scb_ppnr.interest_income import project_dep_banks_other, project_other_ida
from scb_ppnr.interest_income.schemas import PROJECTION_QUARTERS

ROOT = Path(__file__).resolve().parents[3]

# The severely-adverse CSV paths, percent → annualized decimal.
T3M = {1: 0.0400, 2: 0.0350, 3: 0.0350, 4: 0.0300, 5: 0.0250, 6: 0.0250, 7: 0.0300, 8: 0.0350, 9: 0.0400}
T10Y = {1: 0.0450, 2: 0.0445, 3: 0.0440, 4: 0.0435, 5: 0.0430, 6: 0.0430, 7: 0.0435, 8: 0.0440, 9: 0.0445}


def test_synthetic_income_run_reproduces_hand_goldens():
    config = load_config(ROOT / "examples" / "synthetic_config.toml")
    scenario = load_mev_scenario(config, "synthetic_severely_adverse").interest_income_scenario_paths()
    family = load_income_inputs(config)

    dep = project_dep_banks_other(family.dep_banks_other, scenario)
    ida = project_other_ida(family.other_ida, scenario)

    for q in PROJECTION_QUARTERS:
        assert dep.income_path()[q] == pytest.approx(1000.0 * T3M[q] / 4.0, rel=1e-12)
        blended = 0.6 * T3M[q] + 0.4 * T10Y[q]
        assert ida.income_path()[q] == pytest.approx(2000.0 * blended / 4.0, rel=1e-12)

    assert dep.income_path()[1] == pytest.approx(10.0)   # 1000 · 0.04 / 4
    assert ida.income_path()[1] == pytest.approx(21.0)   # 2000 · (0.6·0.04 + 0.4·0.045) / 4
    assert dep.validation_status == "passed"
    assert ida.validation_status == "passed"
    assert dep.cumulative_income == pytest.approx(sum(1000.0 * T3M[q] / 4.0 for q in PROJECTION_QUARTERS))


def test_company_template_declares_income_series():
    config = load_config(ROOT / "config" / "company.template.toml")
    assert config.mev is not None
    declared = set(config.mev.series)
    assert {"usd_3m_treasury", "usd_10y_treasury", "prime_rate", "mortgage_rate"} <= declared

"""ie_dom_time_dep (Eq A44) — hand-calculable fixture:
WAL 12 months → ρ = 3/12 = 0.25; seed 2%, 1-year Treasury flat 4%:
PQ1 = 0.25·0.04 + 0.75·0.02 = 0.025; PQ2 = 0.02875; PQ3 = 0.0315625."""

from __future__ import annotations

import pytest

from scb_ppnr.interest_expense import DomTimeDepInputs, ValidationFailure, project_dom_time_dep
from conftest import flat

FIRM = DomTimeDepInputs("FIRM_A", rate_launchpoint=0.0200, wal_months=12.0, balance=1000.0)


def test_wal_month_to_quarter_conversion_and_rho(make_scenario):
    result = project_dom_time_dep(FIRM, make_scenario())
    diag = result.quarters[0].diagnostics
    assert diag.rho == pytest.approx(0.25)
    assert diag.wal_quarters == pytest.approx(4.0)
    assert diag.wal_months == pytest.approx(12.0)


def test_pq1_recursion_from_launch_point_seed(make_scenario):
    result = project_dom_time_dep(FIRM, make_scenario(t1y=flat(0.0400)))
    pq1 = result.quarters[0]
    assert pq1.diagnostics.previous_rate == pytest.approx(0.0200)  # item 42E seed
    assert pq1.annualized_rate == pytest.approx(0.0250)


def test_pq2_uses_pq1_projected_rate(make_scenario):
    result = project_dom_time_dep(FIRM, make_scenario(t1y=flat(0.0400)))
    pq2, pq3 = result.quarters[1], result.quarters[2]
    assert pq2.diagnostics.previous_rate == pytest.approx(0.0250)
    assert pq2.annualized_rate == pytest.approx(0.028750)
    assert pq3.annualized_rate == pytest.approx(0.0315625)


def test_flat_balance_and_quarterly_conversion(make_scenario):
    result = project_dom_time_dep(FIRM, make_scenario(t1y=flat(0.0400)))
    assert all(q.average_balance == 1000.0 for q in result.quarters)
    assert result.quarters[0].quarterly_expense == pytest.approx(6.25)  # 1000 × 0.025 / 4


def test_invalid_wal_fails(make_scenario):
    for bad in (0.0, -3.0):
        with pytest.raises(ValidationFailure):
            DomTimeDepInputs("FIRM_A", 0.02, bad, 1000.0)
    with pytest.raises(ValidationFailure, match=r"outside \(0, 1\]"):
        project_dom_time_dep(DomTimeDepInputs("FIRM_A", 0.02, 2.0, 1000.0), make_scenario())


def test_negative_rate_logged_never_clamped(make_scenario):
    firm = DomTimeDepInputs("FIRM_A", rate_launchpoint=-0.0100, wal_months=12.0, balance=1000.0)
    result = project_dom_time_dep(firm, make_scenario(t1y=flat(-0.0200)))
    assert result.quarters[0].annualized_rate == pytest.approx(-0.0125)
    assert result.validation_status == "passed_with_warnings"
    assert any("negative projected rate" in w for w in result.warnings)

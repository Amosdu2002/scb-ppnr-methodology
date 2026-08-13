"""Combined-NII monitor: income − expense roll-up, FRB-NII gaps under the 1%
identity guard, and the report-never-force discipline. The round fixture is the
committed synthetic family: income 100, expense 40, NII 60 per quarter."""

from __future__ import annotations

import pytest

from scb_ppnr.core.schemas import PROJECTION_QUARTERS, ValidationFailure
from scb_ppnr.nii_monitor import combined_nii_monitor, combined_nii_report_text


def flat(value: float) -> dict[int, float]:
    return {q: value for q in PROJECTION_QUARTERS}


def test_modeled_nii_and_cumulatives():
    report = combined_nii_monitor(flat(100.0), flat(40.0))
    assert all(report.nii_path[q] == pytest.approx(60.0) for q in PROJECTION_QUARTERS)
    assert report.cumulative_income == pytest.approx(900.0)
    assert report.cumulative_expense == pytest.approx(360.0)
    assert report.cumulative_nii == pytest.approx(540.0)
    assert report.frb_net_interest_income is None
    assert report.within_identity_guard is None
    assert report.notes == ()


def test_frb_nii_within_guard():
    report = combined_nii_monitor(flat(100.0), flat(40.0), frb_net_interest_income=flat(60.0))
    assert all(report.per_quarter_gap[q] == pytest.approx(0.0) for q in PROJECTION_QUARTERS)
    assert report.cumulative_gap == pytest.approx(0.0)
    assert report.within_identity_guard is True
    assert report.notes == ()


def test_quarterly_shape_divergence_alone_is_not_a_breach():
    # Both calibrations match cumulatives only, so quarterly modeled-vs-FRB
    # divergence is structural: ±10 swings that cancel cumulatively stay True.
    income = {**flat(100.0), 1: 110.0, 2: 90.0}
    report = combined_nii_monitor(income, flat(40.0), frb_net_interest_income=flat(60.0))
    assert report.per_quarter_gap[1] == pytest.approx(10.0)
    assert report.per_quarter_gap[2] == pytest.approx(-10.0)
    assert report.cumulative_gap == pytest.approx(0.0)
    assert report.within_identity_guard is True
    assert report.notes == ()


def test_frb_nii_cumulative_breach_reported_never_forced():
    # Cumulative gap 90 vs guard 0.01·max(1, 900, 360) = 9 → breach; values
    # untouched, nothing raises — reported only (conventions §10).
    report = combined_nii_monitor(flat(100.0), flat(40.0), frb_net_interest_income=flat(50.0))
    assert report.within_identity_guard is False
    assert len(report.notes) == 1
    assert "cumulative" in report.notes[0]
    assert all(report.nii_path[q] == pytest.approx(60.0) for q in PROJECTION_QUARTERS)
    assert report.cumulative_gap == pytest.approx(90.0)


def test_negative_nii_is_legal_and_reported_plainly():
    report = combined_nii_monitor(flat(30.0), flat(40.0))
    assert all(report.nii_path[q] == pytest.approx(-10.0) for q in PROJECTION_QUARTERS)


def test_structural_path_defects_surface():
    partial = {q: 100.0 for q in PROJECTION_QUARTERS[:-1]}
    with pytest.raises(ValidationFailure, match="missing projection quarter"):
        combined_nii_monitor(partial, flat(40.0))


def test_report_text_layout():
    report = combined_nii_monitor(flat(100.0), flat(40.0), frb_net_interest_income=flat(60.0))
    text = combined_nii_report_text(report)
    assert "total_income" in text
    assert "modeled_nii" in text
    assert "frb_nii (target)" in text
    assert "identity guard: True" in text
    assert "structural under cumulative-only calibration" in text

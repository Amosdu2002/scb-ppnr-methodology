"""Canonical tidy-sheet firm-data loader: happy round-trip against the conftest
fixture, scale rules, and every refusal path."""

from __future__ import annotations

import csv
from pathlib import Path

import pytest

from scb_ppnr.ingestion import FirmDataConfig, IngestionConfig, TableSource, load_family_inputs
from scb_ppnr.interest_expense import ValidationFailure

COLUMNS = ["model", "field", "subcomponent", "quarter", "scale", "value"]

# Canonical rows replicating tests/conftest.py make_family() exactly — decimal scales
# for rates, millions for money (both pass values through untouched; D-006).
BASE_ROWS: list[tuple[str, str, str, str, str, str]] = [
    ("ie_dom_time_dep", "rate_launchpoint", "", "", "decimal", "0.02"),
    ("ie_dom_time_dep", "wal_months", "", "", "", "12"),
    ("ie_dom_time_dep", "balance", "", "", "millions", "1000"),
    ("ie_other_dom_dep", "rate_launchpoint", "mma", "", "decimal", "0.01"),
    ("ie_other_dom_dep", "balance", "mma", "", "millions", "600"),
    ("ie_other_dom_dep", "elb_spread", "mma", "", "decimal", "0.001"),
    ("ie_other_dom_dep", "rate_launchpoint", "savings", "", "decimal", "0.005"),
    ("ie_other_dom_dep", "balance", "savings", "", "millions", "300"),
    ("ie_other_dom_dep", "elb_spread", "savings", "", "decimal", "0.001"),
    ("ie_other_dom_dep", "rate_launchpoint", "transaction", "", "decimal", "0.002"),
    ("ie_other_dom_dep", "balance", "transaction", "", "millions", "100"),
    ("ie_other_dom_dep", "elb_spread", "transaction", "", "decimal", "0.001"),
    ("ie_other_dom_dep", "total_average_balance", "", "", "millions", "1050"),
    ("ie_foreign_dep", "rate_launchpoint", "foreign_nontime", "", "decimal", "0.008"),
    ("ie_foreign_dep", "balance", "foreign_nontime", "", "millions", "500"),
    ("ie_foreign_dep", "elb_spread", "foreign_nontime", "", "decimal", "0.0004"),
    ("ie_foreign_dep", "rate_launchpoint", "foreign_time", "", "decimal", "0.012"),
    ("ie_foreign_dep", "balance", "foreign_time", "", "millions", "500"),
    ("ie_foreign_dep", "elb_spread", "foreign_time", "", "decimal", "0.0006"),
    ("ie_fed_funds_repo", "fed_funds_purchased_balance", "", "", "millions", "600"),
    ("ie_fed_funds_repo", "repo_sold_balance", "", "", "millions", "400"),
    ("ie_other_borrowing", "total_balance", "", "", "millions", "1000"),
    ("ie_other_borrowing", "cp_share", "", "", "decimal", "0.10"),
    ("ie_other_borrowing", "subdebt_share", "", "", "decimal", "0.20"),
] + [("family", "frb_total_interest_expense", "", str(q), "millions", "40") for q in range(1, 10)]


def _write(tmp_path: Path, rows) -> IngestionConfig:
    with (tmp_path / "firm.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(COLUMNS)
        writer.writerows(rows)
    return IngestionConfig(base_dir=tmp_path, firm_data=FirmDataConfig("FIRM_A", TableSource(Path("firm.csv"))))


def test_round_trip_equals_directly_constructed_inputs(tmp_path, make_family):
    loaded = load_family_inputs(_write(tmp_path, BASE_ROWS))
    assert loaded == make_family()   # exact — decimal and millions scales pass values through untouched


def test_percent_scale_converted(tmp_path):
    rows = [row for row in BASE_ROWS if row[:2] != ("ie_dom_time_dep", "rate_launchpoint")]
    rows.append(("ie_dom_time_dep", "rate_launchpoint", "", "", "percent", "2.00"))
    loaded = load_family_inputs(_write(tmp_path, rows))
    assert loaded.dom_time_dep.rate_launchpoint == pytest.approx(0.02)


def test_missing_inputs_listed(tmp_path):
    rows = [row for row in BASE_ROWS if row[:2] != ("ie_fed_funds_repo", "repo_sold_balance")]
    rows = [row for row in rows if not (row[0] == "family" and row[3] == "9")]
    with pytest.raises(ValidationFailure) as excinfo:
        load_family_inputs(_write(tmp_path, rows))
    assert "ie_fed_funds_repo.repo_sold_balance" in str(excinfo.value)
    assert "family.frb_total_interest_expense PQ9" in str(excinfo.value)


def test_unknown_model_field_and_subcomponent(tmp_path):
    with pytest.raises(ValidationFailure, match="unknown model"):
        load_family_inputs(_write(tmp_path, BASE_ROWS + [("ie_loans", "balance", "", "", "", "1")]))
    with pytest.raises(ValidationFailure, match="unknown field"):
        load_family_inputs(_write(tmp_path, BASE_ROWS + [("ie_dom_time_dep", "spread", "", "", "decimal", "1")]))
    with pytest.raises(ValidationFailure, match="unknown subcomponent"):
        load_family_inputs(_write(tmp_path, BASE_ROWS + [("ie_other_dom_dep", "balance", "cds", "", "", "1")]))


def test_subcomponent_required_where_dimensioned(tmp_path):
    with pytest.raises(ValidationFailure, match="subcomponent required"):
        load_family_inputs(_write(tmp_path, BASE_ROWS + [("ie_foreign_dep", "balance", "", "", "", "1")]))


def test_rate_without_scale_refused(tmp_path):
    rows = [row for row in BASE_ROWS if row[:2] != ("ie_dom_time_dep", "rate_launchpoint")]
    rows.append(("ie_dom_time_dep", "rate_launchpoint", "", "", "", "0.02"))
    with pytest.raises(ValidationFailure, match="must be confirmed"):
        load_family_inputs(_write(tmp_path, rows))


def test_billions_scale_converted_to_canonical_millions(tmp_path):
    rows = [row for row in BASE_ROWS if row[:2] != ("ie_other_borrowing", "total_balance")]
    rows.append(("ie_other_borrowing", "total_balance", "", "", "billions", "1"))
    rows = [row if not (row[0] == "family" and row[3] == "1") else (*row[:4], "billions", "0.04") for row in rows]
    loaded = load_family_inputs(_write(tmp_path, rows))
    assert loaded.other_borrowing.total_balance == pytest.approx(1000.0)
    assert loaded.frb_total_interest_expense[1] == pytest.approx(40.0)


def test_balance_without_scale_refused(tmp_path):
    rows = [row for row in BASE_ROWS if row[:2] != ("ie_dom_time_dep", "balance")]
    rows.append(("ie_dom_time_dep", "balance", "", "", "", "1000"))
    with pytest.raises(ValidationFailure, match="must be confirmed"):
        load_family_inputs(_write(tmp_path, rows))


def test_balance_with_rate_scale_refused(tmp_path):
    rows = [row for row in BASE_ROWS if row[:2] != ("ie_dom_time_dep", "balance")]
    rows.append(("ie_dom_time_dep", "balance", "", "", "percent", "1000"))
    with pytest.raises(ValidationFailure, match="millions.*billions"):
        load_family_inputs(_write(tmp_path, rows))


def test_months_with_scale_refused(tmp_path):
    rows = [row for row in BASE_ROWS if row[:2] != ("ie_dom_time_dep", "wal_months")]
    rows.append(("ie_dom_time_dep", "wal_months", "", "", "millions", "12"))
    with pytest.raises(ValidationFailure, match="already canonical"):
        load_family_inputs(_write(tmp_path, rows))


def test_duplicate_row_refused(tmp_path):
    with pytest.raises(ValidationFailure, match="duplicate row"):
        load_family_inputs(_write(tmp_path, BASE_ROWS + [BASE_ROWS[0]]))


def test_quarter_rules(tmp_path):
    with pytest.raises(ValidationFailure, match="quarter not allowed"):
        load_family_inputs(_write(tmp_path, BASE_ROWS + [("ie_dom_time_dep", "wal_months", "", "3", "", "12")]))
    bad_quarter = [row for row in BASE_ROWS] + [("family", "frb_total_interest_expense", "", "10", "", "40")]
    with pytest.raises(ValidationFailure, match="must be 1..9"):
        load_family_inputs(_write(tmp_path, bad_quarter))


FRB_COMPANION_ROWS = [
    ("family", "frb_total_interest_income", "", str(q), "millions", "100") for q in range(1, 10)
] + [
    ("family", "frb_net_interest_income", "", str(q), "millions", "60") for q in range(1, 10)
]


def test_optional_frb_income_and_nii_paths_loaded(tmp_path, make_family, flat_path):
    loaded = load_family_inputs(_write(tmp_path, BASE_ROWS + FRB_COMPANION_ROWS))
    assert loaded == make_family(frb_income=flat_path(100.0), frb_nii=flat_path(60.0))
    assert loaded.frb_total_interest_income[5] == 100.0
    assert loaded.frb_net_interest_income[5] == 60.0


def test_frb_companions_absent_default_to_none(tmp_path):
    loaded = load_family_inputs(_write(tmp_path, BASE_ROWS))
    assert loaded.frb_total_interest_income is None
    assert loaded.frb_net_interest_income is None


def test_partial_frb_companion_path_fails(tmp_path):
    partial = [row for row in FRB_COMPANION_ROWS if not (row[1] == "frb_total_interest_income" and row[3] == "6")]
    with pytest.raises(ValidationFailure, match=r"partially supplied.*PQ6"):
        load_family_inputs(_write(tmp_path, BASE_ROWS + partial))


def test_frb_identity_wiring_guard(tmp_path):
    bad_nii = [row if row[1] != "frb_net_interest_income" else (*row[:5], "75") for row in FRB_COMPANION_ROWS]
    with pytest.raises(ValidationFailure, match="FRB identity violated"):
        load_family_inputs(_write(tmp_path, BASE_ROWS + bad_nii))   # 100 − 40 = 60, not 75


def test_missing_required_columns(tmp_path):
    with (tmp_path / "firm.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["model", "value"])
        writer.writerow(["ie_dom_time_dep", "1"])
    config = IngestionConfig(base_dir=tmp_path, firm_data=FirmDataConfig("FIRM_A", TableSource(Path("firm.csv"))))
    with pytest.raises(ValidationFailure, match=r"missing required columns \['field'\]"):
        load_family_inputs(config)

"""Two-sheet firm-data loader (D-007): happy round-trip against the conftest fixture,
sheet-placement rules, scale rules, and every refusal path."""

from __future__ import annotations

import csv
from pathlib import Path

import pytest

from scb_ppnr.ingestion import FirmDataConfig, IngestionConfig, TableSource, load_config, load_family_inputs
from scb_ppnr.interest_expense import ValidationFailure

SPOT_COLUMNS = ["model", "field", "subcomponent", "scale", "value"]
QUARTERLY_COLUMNS = ["model", "field", "subcomponent", "scale"] + [f"PQ{q}" for q in range(1, 10)]

# Canonical spot rows replicating tests/conftest.py make_family() exactly — decimal
# scales for rates, millions for money (both pass values through untouched; D-006).
SPOT_ROWS: list[tuple[str, str, str, str, str]] = [
    ("ie_dom_time_dep", "rate_launchpoint", "", "decimal", "0.02"),
    ("ie_dom_time_dep", "wal_months", "", "", "12"),
    ("ie_dom_time_dep", "balance", "", "millions", "1000"),
    ("ie_other_dom_dep", "rate_launchpoint", "mma", "decimal", "0.01"),
    ("ie_other_dom_dep", "balance", "mma", "millions", "600"),
    ("ie_other_dom_dep", "elb_spread", "mma", "decimal", "0.001"),
    ("ie_other_dom_dep", "rate_launchpoint", "savings", "decimal", "0.005"),
    ("ie_other_dom_dep", "balance", "savings", "millions", "300"),
    ("ie_other_dom_dep", "elb_spread", "savings", "decimal", "0.001"),
    ("ie_other_dom_dep", "rate_launchpoint", "transaction", "decimal", "0.002"),
    ("ie_other_dom_dep", "balance", "transaction", "millions", "100"),
    ("ie_other_dom_dep", "elb_spread", "transaction", "decimal", "0.001"),
    ("ie_other_dom_dep", "total_average_balance", "", "millions", "1050"),
    ("ie_foreign_dep", "rate_launchpoint", "foreign_nontime", "decimal", "0.008"),
    ("ie_foreign_dep", "balance", "foreign_nontime", "millions", "500"),
    ("ie_foreign_dep", "elb_spread", "foreign_nontime", "decimal", "0.0004"),
    ("ie_foreign_dep", "rate_launchpoint", "foreign_time", "decimal", "0.012"),
    ("ie_foreign_dep", "balance", "foreign_time", "millions", "500"),
    ("ie_foreign_dep", "elb_spread", "foreign_time", "decimal", "0.0006"),
    ("ie_fed_funds_repo", "fed_funds_purchased_balance", "", "millions", "600"),
    ("ie_fed_funds_repo", "repo_sold_balance", "", "millions", "400"),
    ("ie_other_borrowing", "total_balance", "", "millions", "1000"),
    ("ie_other_borrowing", "cp_share", "", "decimal", "0.10"),
    ("ie_other_borrowing", "subdebt_share", "", "decimal", "0.20"),
]

# Wide quarterly rows: one row per series, scale declared once, PQ1..PQ9 columns.
QUARTERLY_ROWS: list[tuple[str, ...]] = [
    ("family", "frb_total_interest_expense", "", "millions") + ("40",) * 9,
]
COMPANION_ROWS: list[tuple[str, ...]] = [
    ("family", "frb_total_interest_income", "", "millions") + ("100",) * 9,
    ("family", "frb_net_interest_income", "", "millions") + ("60",) * 9,
]


def _write(tmp_path: Path, spot_rows, quarterly_rows, frb_expense_sign: str = "positive") -> IngestionConfig:
    for name, columns, rows in (
        ("spot.csv", SPOT_COLUMNS, spot_rows),
        ("quarterly.csv", QUARTERLY_COLUMNS, quarterly_rows),
    ):
        with (tmp_path / name).open("w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow(columns)
            writer.writerows(rows)
    return IngestionConfig(
        base_dir=tmp_path,
        firm_data=FirmDataConfig(
            "FIRM_A",
            spot=TableSource(Path("spot.csv")),
            quarterly=TableSource(Path("quarterly.csv")),
            frb_expense_sign=frb_expense_sign,
        ),
    )


def test_round_trip_equals_directly_constructed_inputs(tmp_path, make_family):
    loaded = load_family_inputs(_write(tmp_path, SPOT_ROWS, QUARTERLY_ROWS))
    assert loaded == make_family()   # exact — decimal and millions scales pass values through untouched


def test_percent_scale_converted(tmp_path):
    rows = [row for row in SPOT_ROWS if row[:2] != ("ie_dom_time_dep", "rate_launchpoint")]
    rows.append(("ie_dom_time_dep", "rate_launchpoint", "", "percent", "2.00"))
    loaded = load_family_inputs(_write(tmp_path, rows, QUARTERLY_ROWS))
    assert loaded.dom_time_dep.rate_launchpoint == pytest.approx(0.02)


def test_billions_scale_converted_to_canonical_millions(tmp_path):
    rows = [row for row in SPOT_ROWS if row[:2] != ("ie_other_borrowing", "total_balance")]
    rows.append(("ie_other_borrowing", "total_balance", "", "billions", "1"))
    quarterly = [("family", "frb_total_interest_expense", "", "billions") + ("0.04",) * 9]
    loaded = load_family_inputs(_write(tmp_path, rows, quarterly))
    assert loaded.other_borrowing.total_balance == pytest.approx(1000.0)
    assert loaded.frb_total_interest_expense[1] == pytest.approx(40.0)


def test_total_average_balance_row_is_optional(tmp_path):
    rows = [row for row in SPOT_ROWS if row[:2] != ("ie_other_dom_dep", "total_average_balance")]
    loaded = load_family_inputs(_write(tmp_path, rows, QUARTERLY_ROWS))
    assert loaded.other_dom_dep.total_average_balance is None   # PID-ODD-3 — monitor reference only


def test_missing_inputs_listed(tmp_path):
    rows = [row for row in SPOT_ROWS if row[:2] != ("ie_fed_funds_repo", "repo_sold_balance")]
    with pytest.raises(ValidationFailure) as excinfo:
        load_family_inputs(_write(tmp_path, rows, [COMPANION_ROWS[0]]))
    assert "ie_fed_funds_repo.repo_sold_balance" in str(excinfo.value)
    assert "family.frb_total_interest_expense (quarterly sheet)" in str(excinfo.value)


def test_unknown_model_field_and_subcomponent(tmp_path):
    with pytest.raises(ValidationFailure, match="unknown model"):
        load_family_inputs(_write(tmp_path, SPOT_ROWS + [("ie_loans", "balance", "", "", "1")], QUARTERLY_ROWS))
    with pytest.raises(ValidationFailure, match="unknown field"):
        load_family_inputs(_write(tmp_path, SPOT_ROWS + [("ie_dom_time_dep", "spread", "", "decimal", "1")], QUARTERLY_ROWS))
    with pytest.raises(ValidationFailure, match="unknown subcomponent"):
        load_family_inputs(_write(tmp_path, SPOT_ROWS + [("ie_other_dom_dep", "balance", "cds", "millions", "1")], QUARTERLY_ROWS))


def test_subcomponent_required_where_dimensioned(tmp_path):
    with pytest.raises(ValidationFailure, match="subcomponent required"):
        load_family_inputs(_write(tmp_path, SPOT_ROWS + [("ie_foreign_dep", "balance", "", "millions", "1")], QUARTERLY_ROWS))


def test_rate_without_scale_refused(tmp_path):
    rows = [row for row in SPOT_ROWS if row[:2] != ("ie_dom_time_dep", "rate_launchpoint")]
    rows.append(("ie_dom_time_dep", "rate_launchpoint", "", "", "0.02"))
    with pytest.raises(ValidationFailure, match="must be confirmed"):
        load_family_inputs(_write(tmp_path, rows, QUARTERLY_ROWS))


def test_balance_without_scale_refused(tmp_path):
    rows = [row for row in SPOT_ROWS if row[:2] != ("ie_dom_time_dep", "balance")]
    rows.append(("ie_dom_time_dep", "balance", "", "", "1000"))
    with pytest.raises(ValidationFailure, match="must be confirmed"):
        load_family_inputs(_write(tmp_path, rows, QUARTERLY_ROWS))


def test_balance_with_rate_scale_refused(tmp_path):
    rows = [row for row in SPOT_ROWS if row[:2] != ("ie_dom_time_dep", "balance")]
    rows.append(("ie_dom_time_dep", "balance", "", "percent", "1000"))
    with pytest.raises(ValidationFailure, match="millions.*billions"):
        load_family_inputs(_write(tmp_path, rows, QUARTERLY_ROWS))


def test_months_with_scale_refused(tmp_path):
    rows = [row for row in SPOT_ROWS if row[:2] != ("ie_dom_time_dep", "wal_months")]
    rows.append(("ie_dom_time_dep", "wal_months", "", "millions", "12"))
    with pytest.raises(ValidationFailure, match="already canonical"):
        load_family_inputs(_write(tmp_path, rows, QUARTERLY_ROWS))


def test_duplicate_rows_refused(tmp_path):
    with pytest.raises(ValidationFailure, match="duplicate row"):
        load_family_inputs(_write(tmp_path, SPOT_ROWS + [SPOT_ROWS[0]], QUARTERLY_ROWS))
    with pytest.raises(ValidationFailure, match="duplicate row"):
        load_family_inputs(_write(tmp_path, SPOT_ROWS, QUARTERLY_ROWS + QUARTERLY_ROWS))


def test_quarterly_field_in_spot_sheet_refused(tmp_path):
    rows = SPOT_ROWS + [("family", "frb_total_interest_expense", "", "millions", "40")]
    with pytest.raises(ValidationFailure, match="belongs in the quarterly sheet"):
        load_family_inputs(_write(tmp_path, rows, QUARTERLY_ROWS))


def test_spot_field_in_quarterly_sheet_refused(tmp_path):
    quarterly = QUARTERLY_ROWS + [("ie_dom_time_dep", "balance", "", "millions") + ("1000",) * 9]
    with pytest.raises(ValidationFailure, match="belongs in .*the spot sheet"):
        load_family_inputs(_write(tmp_path, SPOT_ROWS, quarterly))


def test_unknown_quarterly_field_refused(tmp_path):
    quarterly = QUARTERLY_ROWS + [("family", "frb_something_else", "", "millions") + ("1",) * 9]
    with pytest.raises(ValidationFailure, match="unknown quarterly field"):
        load_family_inputs(_write(tmp_path, SPOT_ROWS, quarterly))


def test_subcomponent_on_quarterly_row_refused(tmp_path):
    quarterly = [("family", "frb_total_interest_expense", "mma", "millions") + ("40",) * 9]
    with pytest.raises(ValidationFailure, match="subcomponent not allowed"):
        load_family_inputs(_write(tmp_path, SPOT_ROWS, quarterly))


def test_blank_quarter_cell_refused(tmp_path):
    quarterly = QUARTERLY_ROWS + [
        ("family", "frb_total_interest_income", "", "millions") + ("100",) * 5 + ("",) + ("100",) * 3
    ]
    with pytest.raises(ValidationFailure, match=r"PQ6 is blank"):
        load_family_inputs(_write(tmp_path, SPOT_ROWS, quarterly))


def test_optional_frb_income_and_nii_paths_loaded(tmp_path, make_family, flat_path):
    loaded = load_family_inputs(_write(tmp_path, SPOT_ROWS, QUARTERLY_ROWS + COMPANION_ROWS))
    assert loaded == make_family(frb_income=flat_path(100.0), frb_nii=flat_path(60.0))
    assert loaded.frb_total_interest_income[5] == 100.0
    assert loaded.frb_net_interest_income[5] == 60.0


def test_frb_companions_absent_default_to_none(tmp_path):
    loaded = load_family_inputs(_write(tmp_path, SPOT_ROWS, QUARTERLY_ROWS))
    assert loaded.frb_total_interest_income is None
    assert loaded.frb_net_interest_income is None


def test_frb_identity_wiring_guard(tmp_path):
    bad = QUARTERLY_ROWS + [
        COMPANION_ROWS[0],
        ("family", "frb_net_interest_income", "", "millions") + ("75",) * 9,   # 100 − 40 = 60, not 75
    ]
    with pytest.raises(ValidationFailure, match="FRB identity violated"):
        load_family_inputs(_write(tmp_path, SPOT_ROWS, bad))


NEGATIVE_EXPENSE_ROW: list[tuple[str, ...]] = [
    ("family", "frb_total_interest_expense", "", "millions") + ("-40",) * 9,
]


def test_negative_sign_convention_normalized_to_positive_canonical(tmp_path, make_family):
    loaded = load_family_inputs(_write(tmp_path, SPOT_ROWS, NEGATIVE_EXPENSE_ROW, frb_expense_sign="negative"))
    assert loaded == make_family()   # identical to entering +40 under the default convention
    assert loaded.frb_total_interest_expense[1] == pytest.approx(40.0)


def test_negative_entries_without_declaration_refused(tmp_path):
    with pytest.raises(ValidationFailure, match="frb_expense_sign"):
        load_family_inputs(_write(tmp_path, SPOT_ROWS, NEGATIVE_EXPENSE_ROW))


def test_negative_declaration_with_positive_entries_refused(tmp_path):
    with pytest.raises(ValidationFailure, match="frb_expense_sign"):
        load_family_inputs(_write(tmp_path, SPOT_ROWS, QUARTERLY_ROWS, frb_expense_sign="negative"))


def test_identity_guard_consistent_under_negative_convention(tmp_path, make_family, flat_path):
    rows = NEGATIVE_EXPENSE_ROW + COMPANION_ROWS   # income +100, NII +60, expense −40: 100 + (−40) = 60
    loaded = load_family_inputs(_write(tmp_path, SPOT_ROWS, rows, frb_expense_sign="negative"))
    assert loaded == make_family(frb_income=flat_path(100.0), frb_nii=flat_path(60.0))


def test_frb_expense_sign_config_value_validated(tmp_path):
    (tmp_path / "c.toml").write_text(
        "\n".join(
            [
                "[firm_data]",
                'firm_id = "F"',
                'frb_expense_sign = "flipped"',
                "[firm_data.spot]",
                'path = "spot.csv"',
                "[firm_data.quarterly]",
                'path = "quarterly.csv"',
            ]
        ),
        encoding="utf-8",
    )
    with pytest.raises(ValidationFailure, match="frb_expense_sign must be"):
        load_config(tmp_path / "c.toml")


def test_missing_required_columns_per_sheet(tmp_path):
    config = _write(tmp_path, SPOT_ROWS, QUARTERLY_ROWS)
    with (tmp_path / "spot.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["model", "value"])
        writer.writerow(["ie_dom_time_dep", "1"])
    with pytest.raises(ValidationFailure, match=r"spot sheet is missing required columns \['field'\]"):
        load_family_inputs(config)

    config = _write(tmp_path, SPOT_ROWS, QUARTERLY_ROWS)
    with (tmp_path / "quarterly.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["model", "field", "PQ1"])
        writer.writerow(["family", "frb_total_interest_expense", "40"])
    with pytest.raises(ValidationFailure, match=r"quarterly sheet is missing required columns \['PQ2'"):
        load_family_inputs(config)

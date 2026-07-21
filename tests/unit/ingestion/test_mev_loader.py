"""Generic MEV loader: window slicing, declared-scale conversion, open-ended series
registry, and the refuse-to-guess gates."""

from __future__ import annotations

from pathlib import Path

import pytest

from scb_ppnr.ingestion import (
    IngestionConfig,
    MevConfig,
    ScenarioSource,
    SeriesSpec,
    load_config,
    load_mev_scenario,
)
from scb_ppnr.interest_expense import ValidationFailure

HEADER = "Date,T3M,T1Y,BBB,TENY"
WINDOW = [
    ("2025Q2", "4.10", "4.20", "6.10", "4.60"),   # history — ignored
    ("2025Q4", "3.00", "4.00", "6.00", "4.50"),   # PQ0
    ("2026Q1", "4.00", "4.00", "6.00", "4.50"),
    ("2026Q2", "3.50", "4.00", "6.00", "4.45"),
    ("2026Q3", "3.50", "4.00", "6.00", "4.40"),
    ("2026Q4", "3.00", "4.00", "6.00", "4.35"),
    ("2027Q1", "2.50", "4.00", "6.00", "4.30"),
    ("2027Q2", "2.50", "4.00", "6.00", "4.30"),
    ("2027Q3", "3.00", "4.00", "6.00", "4.35"),
    ("2027Q4", "3.50", "4.00", "6.00", "4.40"),
    ("2028Q1", "4.00", "4.00", "6.00", "4.45"),
]

DEFAULT_SERIES = {
    "usd_3m_treasury": SeriesSpec("T3M", "percent"),
    "usd_1y_treasury": SeriesSpec("T1Y", "percent"),
    "bbb_corporate_yield": SeriesSpec("BBB", "percent"),
}


def _write_csv(tmp_path: Path, rows=WINDOW, header: str = HEADER, name: str = "mev.csv") -> None:
    lines = [header] + [",".join(row) for row in rows]
    (tmp_path / name).write_text("\n".join(lines) + "\n", encoding="utf-8")


def _config(tmp_path: Path, series=None) -> IngestionConfig:
    return IngestionConfig(
        base_dir=tmp_path,
        mev=MevConfig(
            date_column="Date",
            launch_point="2025Q4",
            scenarios={"sev": ScenarioSource(Path("mev.csv"))},
            series=dict(series or DEFAULT_SERIES),
        ),
    )


def test_window_slicing_and_percent_conversion(tmp_path):
    _write_csv(tmp_path)
    scenario = load_mev_scenario(_config(tmp_path), "sev")
    t3m = scenario.series_window("usd_3m_treasury", (0, 1, 2))
    assert t3m[0] == pytest.approx(0.0300)   # PQ0 = launch-point row; history row ignored
    assert t3m[1] == pytest.approx(0.0400)
    assert t3m[2] == pytest.approx(0.0350)
    paths = scenario.interest_expense_scenario_paths()
    assert paths.scenario_id == "sev"
    assert paths.usd_1y_treasury[9] == pytest.approx(0.0400)


def test_level_series_loaded_raw_and_registry_is_open_ended(tmp_path):
    _write_csv(tmp_path)
    series = dict(DEFAULT_SERIES)
    series["usd_10y_treasury"] = SeriesSpec("TENY", kind="level")   # one entry, no code change
    scenario = load_mev_scenario(_config(tmp_path, series), "sev")
    assert scenario.series_window("usd_10y_treasury", (1,))[1] == pytest.approx(4.50)  # not /100


def test_undeclared_columns_are_simply_not_loaded(tmp_path):
    _write_csv(tmp_path)
    scenario = load_mev_scenario(_config(tmp_path), "sev")
    assert "usd_10y_treasury" not in scenario.series
    with pytest.raises(ValidationFailure, match="not declared"):
        scenario.series_window("usd_10y_treasury", (1,))


def test_to_be_confirmed_column_blocks_before_any_file_read(tmp_path):
    series = dict(DEFAULT_SERIES)
    series["bbb_corporate_yield"] = SeriesSpec("TO_BE_CONFIRMED", "TO_BE_CONFIRMED")
    # no CSV written — the gate must fire before I/O
    with pytest.raises(ValidationFailure, match="must be confirmed"):
        load_mev_scenario(_config(tmp_path, series), "sev")


def test_rate_series_requires_scale(tmp_path):
    _write_csv(tmp_path)
    series = dict(DEFAULT_SERIES)
    series["usd_3m_treasury"] = SeriesSpec("T3M", None)
    with pytest.raises(ValidationFailure, match="scale"):
        load_mev_scenario(_config(tmp_path, series), "sev")


def test_level_series_must_not_declare_scale(tmp_path):
    _write_csv(tmp_path)
    series = dict(DEFAULT_SERIES)
    series["usd_10y_treasury"] = SeriesSpec("TENY", "percent", kind="level")
    with pytest.raises(ValidationFailure, match="must not declare a scale"):
        load_mev_scenario(_config(tmp_path, series), "sev")


def test_missing_declared_column_fails(tmp_path):
    _write_csv(tmp_path)
    series = dict(DEFAULT_SERIES)
    series["prime_rate"] = SeriesSpec("PRIME", "percent")
    with pytest.raises(ValidationFailure, match="'PRIME'.*not found"):
        load_mev_scenario(_config(tmp_path, series), "sev")


def test_missing_window_quarter_surfaces_on_demand(tmp_path):
    rows = [row for row in WINDOW if row[0] != "2027Q1"]   # drop PQ5
    _write_csv(tmp_path, rows)
    scenario = load_mev_scenario(_config(tmp_path), "sev")
    with pytest.raises(ValidationFailure, match=r"missing quarters \['PQ5'\]"):
        scenario.interest_expense_scenario_paths()


def test_blank_cell_is_missing_only_if_demanded(tmp_path):
    rows = [list(row) for row in WINDOW]
    rows[1][2] = ""   # blank T1Y at PQ0 — the IE family never demands t1y PQ0
    _write_csv(tmp_path, [tuple(row) for row in rows])
    scenario = load_mev_scenario(_config(tmp_path), "sev")
    assert scenario.interest_expense_scenario_paths().usd_1y_treasury[1] == pytest.approx(0.0400)


def test_duplicate_quarter_fails(tmp_path):
    _write_csv(tmp_path, WINDOW + [("2026-03-31", "9.99", "9.99", "9.99", "9.99")])  # PQ1 again, ISO form
    with pytest.raises(ValidationFailure, match="duplicate quarter"):
        load_mev_scenario(_config(tmp_path), "sev")


def test_unknown_scenario_lists_available(tmp_path):
    _write_csv(tmp_path)
    with pytest.raises(ValidationFailure, match="not configured.*sev"):
        load_mev_scenario(_config(tmp_path), "baseline")


def test_load_config_parses_toml_and_resolves_paths(tmp_path):
    (tmp_path / "run.toml").write_text(
        "\n".join(
            [
                "[mev]",
                'date_column = "Date"',
                'launch_point = "2025Q4"',
                "[mev.scenarios.sev]",
                'path = "mev.csv"',
                "[mev.series.usd_3m_treasury]",
                'column = "T3M"',
                'scale = "percent"',
                "[firm_data]",
                'firm_id = "F"',
                "[firm_data.spot]",
                'path = "firm_spot.csv"',
                "[firm_data.quarterly]",
                'path = "firm_quarterly.csv"',
            ]
        ),
        encoding="utf-8",
    )
    config = load_config(tmp_path / "run.toml")
    assert config.mev is not None and config.firm_data is not None
    assert config.mev.series["usd_3m_treasury"].column == "T3M"
    assert config.resolve("mev.csv") == tmp_path.resolve() / "mev.csv"
    assert config.firm_data.firm_id == "F"
    assert config.firm_data.spot.path == Path("firm_spot.csv")
    assert config.firm_data.quarterly.path == Path("firm_quarterly.csv")


LONG_HEADER = "Scenario Name,Date,T3M,T1Y,BBB"
LONG_ROWS = [
    ("Actual", "2025Q3", "3.80", "4.10", "6.05"),                       # history — ignored
    ("Actual", "2025Q4", "3.00", "4.00", "6.00"),                       # PQ0 from actuals
    ("Supervisory Severely Adverse", "2025Q4", "9.99", "9.99", "9.99"), # scenario-labeled PQ0 — ignored
] + [
    ("Supervisory Severely Adverse", f"{2026 + (q - 1) // 4}Q{(q - 1) % 4 + 1}", "4.00", "4.00", "6.00")
    for q in range(1, 10)
] + [
    ("Supervisory Baseline", f"{2026 + (q - 1) // 4}Q{(q - 1) % 4 + 1}", "2.00", "3.00", "5.00")
    for q in range(1, 10)
]


def _long_config(tmp_path: Path, scenarios=None) -> IngestionConfig:
    scenarios = scenarios or {
        "sev": ScenarioSource(Path("mev.csv"), label="Supervisory Severely Adverse"),
        "base": ScenarioSource(Path("mev.csv"), label="supervisory baseline"),  # case-insensitive match
    }
    return IngestionConfig(
        base_dir=tmp_path,
        mev=MevConfig(
            date_column="Date",
            launch_point="2025Q4",
            scenarios=scenarios,
            series=dict(DEFAULT_SERIES),
            scenario_name_column="Scenario Name",
            actuals_label="Actual",
        ),
    )


def test_long_format_takes_pq0_from_actuals_and_pq1_on_from_the_labeled_rows(tmp_path):
    _write_csv(tmp_path, LONG_ROWS, header=LONG_HEADER)
    scenario = load_mev_scenario(_long_config(tmp_path), "sev")
    t3m = scenario.series_window("usd_3m_treasury", (0, 1, 9))
    assert t3m[0] == pytest.approx(0.0300)   # from the "Actual" row, not the 9.99 scenario row
    assert t3m[1] == pytest.approx(0.0400)
    assert t3m[9] == pytest.approx(0.0400)


def test_long_format_scenarios_share_one_sheet(tmp_path):
    _write_csv(tmp_path, LONG_ROWS, header=LONG_HEADER)
    base = load_mev_scenario(_long_config(tmp_path), "base")
    assert base.series_window("usd_3m_treasury", (0,))[0] == pytest.approx(0.0300)  # same actuals PQ0
    assert base.series_window("usd_3m_treasury", (1,))[1] == pytest.approx(0.0200)  # baseline rows
    assert base.series_window("bbb_corporate_yield", (5,))[5] == pytest.approx(0.0500)


def test_long_format_missing_actuals_pq0_surfaces_on_demand(tmp_path):
    rows = [row for row in LONG_ROWS if row[:2] != ("Actual", "2025Q4")]
    _write_csv(tmp_path, rows, header=LONG_HEADER)
    scenario = load_mev_scenario(_long_config(tmp_path), "sev")
    with pytest.raises(ValidationFailure, match=r"missing quarters \['PQ0'\]"):
        scenario.interest_expense_scenario_paths()


def test_long_format_missing_scenario_name_column_fails(tmp_path):
    _write_csv(tmp_path)   # plain single-scenario file without the column
    with pytest.raises(ValidationFailure, match="scenario-name column"):
        load_mev_scenario(_long_config(tmp_path), "sev")


def test_config_requires_labels_iff_scenario_name_column(tmp_path):
    base = [
        "[mev]",
        'date_column = "Date"',
        'launch_point = "2025Q4"',
        "[mev.scenarios.sev]",
        'path = "mev.csv"',
        "[mev.series.usd_3m_treasury]",
        'column = "T3M"',
        'scale = "percent"',
    ]
    with_column = base[:3] + ['scenario_name_column = "Scenario Name"'] + base[3:]
    (tmp_path / "a.toml").write_text("\n".join(with_column), encoding="utf-8")
    with pytest.raises(ValidationFailure, match="'label' is required"):
        load_config(tmp_path / "a.toml")

    with_orphan_label = base[:5] + ['label = "Supervisory Severely Adverse"'] + base[5:]
    (tmp_path / "b.toml").write_text("\n".join(with_orphan_label), encoding="utf-8")
    with pytest.raises(ValidationFailure, match="scenario_name_column is not"):
        load_config(tmp_path / "b.toml")


def test_xlsx_backend_matches_csv(tmp_path):
    openpyxl = pytest.importorskip("openpyxl")
    _write_csv(tmp_path)
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "MEV"
    sheet.append(HEADER.split(","))
    import datetime

    quarter_end = {1: (3, 31), 2: (6, 30), 3: (9, 30), 4: (12, 31)}
    for row in WINDOW:
        year, quarter = int(row[0][:4]), int(row[0][-1])
        month, day = quarter_end[quarter]
        sheet.append([datetime.date(year, month, day), *[float(v) for v in row[1:]]])
    workbook.save(tmp_path / "mev.xlsx")

    config = IngestionConfig(
        base_dir=tmp_path,
        mev=MevConfig("Date", "2025Q4", {"sev": ScenarioSource(Path("mev.xlsx"), "MEV")}, dict(DEFAULT_SERIES)),
    )
    from_xlsx = load_mev_scenario(config, "sev").interest_expense_scenario_paths()
    from_csv = load_mev_scenario(_config(tmp_path), "sev").interest_expense_scenario_paths()
    assert dict(from_xlsx.usd_3m_treasury) == pytest.approx(dict(from_csv.usd_3m_treasury))
    assert dict(from_xlsx.bbb_corporate_yield) == pytest.approx(dict(from_csv.bbb_corporate_yield))

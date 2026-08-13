"""The retail keys ride the generic [firm_data.loans] parser (PID-LOAN-31/32/33/34)."""

from __future__ import annotations

import textwrap

from scb_ppnr.ingestion.config import load_config


def _write(tmp_path, body: str):
    path = tmp_path / "company.toml"
    path.write_text(textwrap.dedent(body), encoding="utf-8")
    return path


def test_retail_keys_parse(tmp_path):
    config = load_config(_write(tmp_path, """
        [firm_data]
        firm_id = "TEST"

        [firm_data.loans]
        workbook = "book.xlsx"
        launch_point = "2024Q4"
        m1_sheet = "M.1 Balances"
        mev_sheet = "MEV Data"
        mortgage_query_sheet = "Mortgage query"
        mortgage_window = "quarter"
        card_query_sheet = "Card query"
        card_spread_mode = "reported"
        auto_pivot_sheet = "Auto 4Q24 pivot"
        auto_pivot_workbook = "auto.xlsx"
        retail_auto_scalar = "0.948"
        oc_sheet = "OTHER"
        oc_balance_column = 6
        line_items_sheet = "Peer results"
        mev_prime_column = "Prime rate"
        mev_mortgage_column = "Mortgage rate"
    """))
    spec = config.firm_data.loans.spec
    assert spec.mortgage_query_sheet == "Mortgage query"
    assert spec.card_query_sheet == "Card query"
    assert spec.auto_pivot_sheet == "Auto 4Q24 pivot"
    assert spec.auto_pivot_workbook == "auto.xlsx"
    assert spec.retail_auto_scalar == "0.948"
    assert spec.oc_balance_column == 6
    assert spec.line_items_sheet == "Peer results"
    assert spec.mev_prime_column == "Prime rate"
    assert spec.mev_mortgage_column == "Mortgage rate"
    assert spec.mortgage_window == "quarter"
    assert spec.card_spread_mode == "reported"

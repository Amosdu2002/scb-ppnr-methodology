"""Retail loan families: loaders + engines against a hand-checked synthetic workbook.

Every number below is invented and chosen so the Equation A33/A38 arithmetic can
be verified by hand in the comments. The workbook layout mirrors the PID-LOAN-26..34
contracts: the M.1 retail rows with role labels, the two-variant Mortgage query
(the second variant must be IGNORED), the Card query, the Auto pivot summary with
its P..X weight columns, the other-consumer product block, the line-item rates
sheet with decoy sections, and the MEV Data columns."""

from __future__ import annotations

from pathlib import Path

import pytest

openpyxl = pytest.importorskip("openpyxl")

from scb_ppnr.core.schemas import ValidationFailure
from scb_ppnr.ingestion.loans_loader import LoansSheetSpec
from scb_ppnr.ingestion.retail_loader import (
    load_auto_pivot,
    load_card_query,
    load_line_item_rates,
    load_mev_series,
    load_mortgage_query,
    load_oc_products,
    load_retail_m1,
)
from scb_ppnr.interest_income.loans_retail import (
    RetailDiagnostics,
    build_auto,
    build_card,
    build_mortgage,
    build_other_consumer,
    family_summary,
    parse_auto_scalar,
)

QUARTERS = tuple(range(1, 10))

# Scenario paths, percent on the sheet -> decimals in canon.
# Prime: PQ0 8, PQ1 5, PQ2..9 3.  Mortgage rate: PQ0 6, PQ1 4, PQ2..9 4.
PRIME = {0: 0.08, 1: 0.05, **{q: 0.03 for q in range(2, 10)}}
MORTGAGE = {0: 0.06, **{q: 0.04 for q in range(1, 10)}}


def _quarter_labels():
    labels = [("Actual", "2024 Q4")]
    year, quarter = 2025, 1
    for _ in range(9):
        labels.append(("Supervisory Severely Adverse", f"{year} Q{quarter}"))
        quarter += 1
        if quarter == 5:
            quarter, year = 1, year + 1
    return labels


def _write_m1(workbook):
    sheet = workbook.create_sheet("M.1 Balances")
    # (label, dom role, int role, E, G, I, K) — data starts at row 11; labels in C.
    rows = [
        ("(a) First mortgages.....", "Retail - mortgage - first lien", "Retail - noncore",
         1000, 100, 20, 5),
        ("(b) First lien HELOANs...", "Retail - mortgage - home equity", "Retail - noncore",
         50, 0, 0, 0),
        ("(a) Junior lien HELOANs..", "Retail - mortgage - home equity", "Retail - noncore",
         30, 10, 0, 0),
        ("(b) HELOCs...............", "Retail - mortgage - HELOC", "Retail - noncore",
         200, 0, 4, 0),
        ("b. Small business........", "Retail - noncore", "Retail - noncore", 80, 0, 0, 0),
        ("c. SME cards and corporate cards", "Retail - SM credit card", "Retail - SM credit card",
         60, 0, 0, 0),
        ("a. Bank cards............", "Retail - consumer credit card", "Retail - noncore",
         500, 0, 2, 0),
        ("b. Charge cards..........", "Retail - consumer credit card", "Retail - noncore",
         0, 0, 0, 0),
        ("a. Auto loans............", "Retail - Auto", "Retail - noncore", 300, 0, 0, 0),
        ("b. Student loans.........", "Retail - noncore", "Retail - noncore", 0, 40, 0, 0),
        ("c. Non-purpose lending...", "Retail - noncore", "Retail - noncore", 90, 0, 10, 0),
        ("e. Other consumer loans..", "Retail - noncore", "Retail - noncore", 120, 0, 6, 0),
    ]
    for offset, (label, dom, intl, e, g, i, k) in enumerate(rows, start=11):
        sheet.cell(row=offset, column=1, value=dom)
        sheet.cell(row=offset, column=2, value=intl)
        sheet.cell(row=offset, column=3, value=label)
        sheet.cell(row=offset, column=5, value=e)
        sheet.cell(row=offset, column=7, value=g)
        sheet.cell(row=offset, column=9, value=i)
        sheet.cell(row=offset, column=11, value=k)


def _write_mortgage_query(workbook):
    sheet = workbook.create_sheet("Mortgage query")
    launch_headers = ["Lien Position", "Loan Type", "Interest Rate Type", "TOTAL_UPB",
                      "WEIGHTED_AVERAGE_RATE", "WEIGHTED_AVERAGE_RATE_AFTER_20241130",
                      "WEIGHTED_AVERAGE_RATE_AFTER_20240930", "WEIGHTED_ARM_FLOOR"]
    for column, text in enumerate(launch_headers, start=1):
        sheet.cell(row=1, column=column, value=text)
    schedule_headers = ["Lien Position", "Loan Type", "Interest Rate Type", "PQ", "TOTAL_UPB"]
    for column, text in enumerate(schedule_headers, start=10):
        sheet.cell(row=1, column=column, value=text)
    # A second classification variant further right — MUST be ignored (PID-LOAN-33).
    for column, text in enumerate(launch_headers, start=16):
        sheet.cell(row=1, column=column, value=text)
    sheet.cell(row=2, column=16, value="First lien")
    sheet.cell(row=2, column=17, value="HFI")
    sheet.cell(row=2, column=18, value="Fixed")
    sheet.cell(row=2, column=19, value=999e9)     # absurd on purpose
    sheet.cell(row=2, column=20, value=0.4)

    launch_rows = [
        # month window 0.062, quarter window 0.070 -> spread 0.01 under "quarter"
        ("First lien", "HFI", "Fixed", 600e6, 0.04, 0.062, 0.070, None),
        ("First lien", "HFI", "Variable", 400e6, 0.045, None, None, 0.035),
        ("HELOC", "HFI", "Fixed", 100e6, 0.039, "x", "x", None),
        ("HELOC", "HFI", "Variable", 100e6, 0.077, None, None, 0.04),
    ]
    for offset, values in enumerate(launch_rows, start=2):
        for column, value in enumerate(values, start=1):
            if value is not None:
                sheet.cell(row=offset, column=column, value=value)
    schedule_rows = [
        ("First lien", "HFI", "Fixed", "PQ1", 60e6),    # wt1 = 60/600 = 0.10
        ("First lien", "HFI", "Fixed", "PQ2", 120e6),   # wt2 = 0.20
    ]
    for offset, values in enumerate(schedule_rows, start=2):
        for column, value in enumerate(values, start=10):
            sheet.cell(row=offset, column=column, value=value)


def _write_card_query(workbook):
    sheet = workbook.create_sheet("Card query")
    headers = ["", "TOTAL_OS", "WEIGHTED_AVERAGE_APR", "WEIGHTED_MAX_APR", "WEIGHTED_SPRD",
               "TOTAL_OTST_REVOLVER", "WEIGHTED_AVERAGE_APR_revolver", "WEIGHTED_SPRD_revolver"]
    for column, text in enumerate(headers, start=1):
        if text:
            sheet.cell(row=1, column=column, value=text)
    rows = [
        (1, 400e6, 20.0, 29.0, 12.0, 200e6, 22.0, 14.0),
        (2, None, 0.0, None, 0.0, None, 0.0, 0.0),
        (3, 100e6, 16.0, 27.0, 10.0, 50e6, 18.0, 12.0),
        (4, None, 0.0, None, 0.0, None, 0.0, 0.0),
    ]
    for offset, values in enumerate(rows, start=2):
        for column, value in enumerate(values, start=1):
            if value is not None:
                sheet.cell(row=offset, column=column, value=value)


def _write_auto_pivot(workbook):
    sheet = workbook.create_sheet("Auto 4Q24 pivot")
    sheet.cell(row=1, column=12, value="20241231")
    labels = [("New auto loans", 300, 0.05, 0.052, [0.0, 0.1, 0.2, 0, 0, 0, 0, 0, 0]),
              ("Used auto loans", 100, 0.07, 0.09, [0.0, 0.0, 0.5, 0, 0, 0, 0, 0, 0]),
              ("Auto leases", 0, None, None, None)]
    for offset, (label, balance, rate, new_orig, weights) in enumerate(labels, start=2):
        sheet.cell(row=offset, column=12, value=label)
        sheet.cell(row=offset, column=13, value=balance)
        if rate is not None:
            sheet.cell(row=offset, column=14, value=rate)
            sheet.cell(row=offset, column=15, value=new_orig)
        if weights is not None:
            for quarter, weight in enumerate(weights, start=1):
                sheet.cell(row=offset, column=15 + quarter, value=weight)


def _write_oc(workbook):
    sheet = workbook.create_sheet("OTHER")
    rows = [
        ("A.7", "Secured-Revolving", 2e6, "Card"),
        ("A.7", "Secured-Installment", 1e6, "Other consumer"),
        ("A.7", "Unsecured-Revolving", 1e6, "Card"),
        ("A.7", "Unsecured-Installment", None, "Other consumer"),
        ("A.7", "Overdraft", None, None),
        ("A.9", "Line of Credit", 3e6, "C&I"),
        ("A.9", "Term Loan", 1e6, "C&I"),
        ("A.9", "Other", None, "C&I"),
        ("X.1", "Other", 5e6, "C&I"),   # decoy: wrong schedule tag, must be skipped
    ]
    for offset, (schedule, product, balance, line) in enumerate(rows, start=3):
        sheet.cell(row=offset, column=2, value=schedule)
        sheet.cell(row=offset, column=4, value=product)
        if balance is not None:
            sheet.cell(row=offset, column=6, value=balance)
        if line is not None:
            sheet.cell(row=offset, column=7, value=line)


def _write_line_items(workbook):
    sheet = workbook.create_sheet("Peer results")
    # decoy PQ header at DIFFERENT columns — the anchoring must ignore it in
    # favor of the header nearest the rates section
    for quarter in range(10):
        sheet.cell(row=1, column=8 + quarter, value=f"PQ{quarter}")
    for quarter in range(10):
        sheet.cell(row=3, column=4 + quarter, value=f"PQ{quarter}")
    sheet.cell(row=4, column=2, value="Average Asset Balances ($Millions)")
    sheet.cell(row=5, column=2, value="Credit Cards")          # decoy: balances section
    sheet.cell(row=5, column=4, value=123456.0)
    sheet.cell(row=7, column=2, value="Average Rates Earned (%)")
    rates = [("First Lien Residential Mortgages (in Domestic Offices)", 0.0415),
             ("HELOCs", 0.08),
             ("C&I Loans (7)", 0.077),
             ("Credit Cards", 0.14),
             ("Auto Loans", 0.0574),
             ("Student Loans", 0.10),
             ("Other, incl. loans backed by securities (non-purpose lending)", 0.06)]
    for offset, (label, value) in enumerate(rates, start=8):
        sheet.cell(row=offset, column=2, value=label)
        sheet.cell(row=offset, column=4, value=value)
    sheet.cell(row=16, column=2, value="Total Interest Income")
    sheet.cell(row=18, column=2, value="Credit Cards")         # decoy: GII section, after the end
    sheet.cell(row=18, column=4, value=9.99)
    # a SECOND stacked section (the MORT stacking precedent) with its own header
    # and different values — read only under line_items_section = 2
    for quarter in range(10):
        sheet.cell(row=20, column=4 + quarter, value=f"PQ{quarter}")
    sheet.cell(row=21, column=2, value="Average Rates Earned (%)")
    for offset, (label, _) in enumerate(rates, start=22):
        sheet.cell(row=offset, column=2, value=label)
        sheet.cell(row=offset, column=4, value=0.05)
    sheet.cell(row=30, column=2, value="Total Interest Income")


def _write_mev(workbook):
    sheet = workbook.create_sheet("MEV Data")
    for column, text in enumerate(
        ["Scenario Name", "Date", "3-month Treasury rate", "Mortgage rate", "Prime rate"],
        start=1,
    ):
        sheet.cell(row=1, column=column, value=text)
    three_m = {0: 4.4, 1: 1.8, **{q: 0.1 for q in range(2, 10)}}
    for index, (scenario, label) in enumerate(_quarter_labels()):
        row = 2 + index
        quarter = index    # 0 = the launch row
        sheet.cell(row=row, column=1, value=scenario)
        sheet.cell(row=row, column=2, value=label)
        sheet.cell(row=row, column=3, value=three_m[quarter])
        sheet.cell(row=row, column=4, value=MORTGAGE[quarter] * 100)
        sheet.cell(row=row, column=5, value=PRIME[quarter] * 100)


@pytest.fixture(scope="module")
def spec(tmp_path_factory) -> LoansSheetSpec:
    """The user's real topology: the retail sheets live in their OWN workbook,
    separate from the wholesale one; the auto pivot in a third file. The
    wholesale workbook here deliberately carries NO retail sheet, so any loader
    that wrongly touched it would fail with sheet-not-found; `retail_workbook`
    and `auto_pivot_workbook` are RELATIVE paths, resolving against the main
    workbook's directory."""
    directory = tmp_path_factory.mktemp("retail")

    wholesale_path = directory / "wholesale.xlsx"
    wholesale = openpyxl.Workbook()
    wholesale.active.title = "CORP H.1"          # wholesale-only content
    wholesale.save(wholesale_path)

    retail_path = directory / "retail.xlsx"
    retail = openpyxl.Workbook()
    retail.remove(retail.active)
    _write_m1(retail)
    _write_mortgage_query(retail)
    _write_card_query(retail)
    _write_oc(retail)
    _write_line_items(retail)
    _write_mev(retail)
    retail.save(retail_path)

    auto_path = directory / "auto.xlsx"
    auto = openpyxl.Workbook()
    auto.remove(auto.active)
    _write_auto_pivot(auto)
    auto.save(auto_path)

    return LoansSheetSpec(
        workbook=wholesale_path,
        retail_workbook="retail.xlsx",           # relative to the main workbook's folder
        mortgage_query_sheet="Mortgage query",
        card_query_sheet="Card query",
        auto_pivot_sheet="Auto 4Q24 pivot",
        auto_pivot_workbook="auto.xlsx",         # the third file
        oc_sheet="OTHER",
        line_items_sheet="Peer results",
        oc_schedule_column=2, oc_product_type_column=4,
        oc_balance_column=6, oc_line_column=7,
    )


@pytest.fixture(scope="module")
def m1(spec):
    rows, _ = load_retail_m1(spec)
    return rows


def test_retail_m1_rows_and_roles(spec, m1):
    assert m1["first_mortgages"].dom_hfi == 1000.0
    assert m1["first_mortgages"].intl == 25.0
    assert m1["charge_cards"].total == 0.0
    assert m1["non_purpose_lending"].total == 100.0
    assert m1["auto_loans"].dom == 300.0
    _, census = load_retail_m1(spec)
    assert census.counters["rows matched"] == 12
    assert not any(note.startswith("WARN") for note in census.notes)


def test_mev_series(spec):
    _, prime, prime0 = load_mev_series(spec, spec.mev_prime_column, "Supervisory Severely Adverse",
                                       QUARTERS, "2024Q4")
    assert prime0 == pytest.approx(0.08)
    assert prime[1] == pytest.approx(0.05)
    assert prime[9] == pytest.approx(0.03)
    _, mortgage, mortgage0 = load_mev_series(spec, spec.mev_mortgage_column,
                                             "Supervisory Severely Adverse", QUARTERS, "2024Q4")
    assert mortgage0 == pytest.approx(0.06)
    assert mortgage[5] == pytest.approx(0.04)


def test_mortgage_query_reads_first_variant_only(spec):
    query = load_mortgage_query(spec)
    fixed = query.segments[("first_lien", "HFI", "fixed")]
    assert fixed.upb == pytest.approx(600.0)              # dollars -> millions
    assert fixed.new_origination_rate == pytest.approx(0.070)   # the QUARTER window
    assert not fixed.new_origination_fallback
    heloc_fixed = query.segments[("heloc", "HFI", "fixed")]
    assert heloc_fixed.new_origination_fallback           # "x" -> own rate (PID-LOAN-33)
    assert heloc_fixed.new_origination_rate == pytest.approx(0.039)
    assert query.schedules[("first_lien", "HFI", "fixed")][2] == pytest.approx(120.0)
    # the absurd second-variant row must not be visible anywhere
    assert all(segment.upb < 1e6 for segment in query.segments.values())


def test_mortgage_month_window(spec):
    from dataclasses import replace
    query = load_mortgage_query(replace(spec, mortgage_window="month"))
    fixed = query.segments[("first_lien", "HFI", "fixed")]
    assert fixed.new_origination_rate == pytest.approx(0.062)


def test_mortgage_engine_hand_golden(spec, m1):
    query = load_mortgage_query(spec)
    diagnostics = RetailDiagnostics()
    blocks = build_mortgage(
        query, m1,
        base_paths={"mortgage_rate": {q: MORTGAGE[q] for q in QUARTERS},
                    "prime_rate": {q: PRIME[q] for q in QUARTERS}},
        base_launch={"mortgage_rate": 0.06, "prime_rate": 0.08},
        quarters=QUARTERS, diagnostics=diagnostics,
    )
    by_name = {block.name: block for block in blocks}
    fl = by_name["first_lien/HFI"]
    fixed = next(s for s in fl.streams if s.name == "fixed")
    variable = next(s for s in fl.streams if s.name == "variable")
    # fixed: balance = 1000 x 600/1000 = 600; spread = 0.070 - 0.06 = 0.01;
    # PQ1 = 0.9 x 0.04 + 0.1 x (0.04 + 0.01) = 0.041
    # PQ2 = 0.8 x 0.041 + 0.2 x 0.05     = 0.0428, flat thereafter (wt = 0)
    assert fixed.balance == pytest.approx(600.0)
    assert fixed.rate_path[1] == pytest.approx(0.041)
    assert fixed.rate_path[2] == pytest.approx(0.0428)
    assert fixed.rate_path[9] == pytest.approx(0.0428)
    assert fixed.income_path[1] == pytest.approx(600 * 0.041 / 4)
    # variable: spread = 0.045 - 0.06 = -0.015; unfloored 0.025 every quarter,
    # floored at the ARM floor 0.035 in ALL nine quarters
    assert variable.balance == pytest.approx(400.0)
    assert variable.rate_path[1] == pytest.approx(0.035)
    assert variable.floor_binds == QUARTERS
    assert variable.income_path[9] == pytest.approx(400 * 0.035 / 4)
    # HELOC runs on the MORTGAGE rate too (PID-LOAN-33 as amended, round 1 —
    # a recorded divergence from the Fed's HELOC-on-Prime register entry):
    # variable spread = 0.077 - 0.06 = 0.017; path = 0.04 + 0.017 = 0.057 every
    # quarter; the 0.04 floor never binds
    heloc = by_name["heloc/HFI"]
    heloc_variable = next(s for s in heloc.streams if s.name == "variable")
    assert heloc_variable.spread == pytest.approx(0.017)
    assert heloc_variable.rate_path[1] == pytest.approx(0.057)
    assert heloc_variable.rate_path[9] == pytest.approx(0.057)
    assert heloc_variable.floor_binds == ()
    # the block total applies the Mortgage scalar 1.014 (PID-LOAN-32)
    totals = fl.total_path(QUARTERS)
    unscaled = fl.unscaled_path(QUARTERS)
    assert totals[3] == pytest.approx(unscaled[3] * 1.014)
    # home-equity blocks carry M.1 balance but no query rows -> a note, no block
    assert any("home_equity/HFI" in note for note in diagnostics.notes)
    assert diagnostics.fallbacks == 1


def test_card_engine_hand_golden(spec, m1):
    segments, _ = load_card_query(spec)
    assert segments[1].revolver_share == pytest.approx(0.5)
    diagnostics = RetailDiagnostics()
    blocks = build_card(segments, m1, {q: PRIME[q] for q in QUARTERS}, 0.08,
                        "reported", QUARTERS, diagnostics)
    by_name = {block.name: block for block in blocks}
    consumer = by_name["consumer"]
    bank = next(s for s in consumer.streams if s.name == "consumer_bank")
    # revolving balance = M.1 consumer 500 x OS-share 1.0 x revolver 0.5 = 250;
    # rate PQ1 = 0.05 + 0.12 = 0.17; PQ2 = 0.03 + 0.12 = 0.15
    assert bank.balance == pytest.approx(250.0)
    assert bank.income_path[1] == pytest.approx(250 * 0.17 / 4)
    assert bank.income_path[2] == pytest.approx(250 * 0.15 / 4)
    assert consumer.scalar == pytest.approx(0.969)
    sme = by_name["sme"]
    assert sme.scalar == pytest.approx(1.033)
    sme_bank = next(s for s in sme.streams if s.name == "sme_bank")
    assert sme_bank.balance == pytest.approx(60 * 1.0 * 0.5)
    assert sme_bank.income_path[1] == pytest.approx(30 * 0.15 / 4)


def test_card_calculated_mode(spec, m1):
    segments, _ = load_card_query(spec)
    blocks = build_card(segments, m1, {q: PRIME[q] for q in QUARTERS}, 0.08,
                        "calculated", QUARTERS, RetailDiagnostics())
    bank = next(s for b in blocks for s in b.streams if s.name == "consumer_bank")
    assert bank.spread == pytest.approx(0.20 - 0.08)


def test_auto_engine_hand_golden(spec, m1):
    summary = load_auto_pivot(spec)
    assert summary.new_outstanding == pytest.approx(300.0)
    assert summary.weights_new[3] == pytest.approx(0.2)
    diagnostics = RetailDiagnostics()
    block = build_auto(summary, m1, {q: PRIME[q] for q in QUARTERS}, 0.08,
                       parse_auto_scalar("0.865"), QUARTERS, diagnostics)
    new = next(s for s in block.streams if s.name == "new_vehicle")
    # balance = M.1 auto 300 x pivot share 300/400 = 225
    # spread = 0.052 - 0.08 = -0.028; new-orig rate PQ2 = 0.03 - 0.028 = 0.002
    # PQ1 (wt 0)   = 0.05
    # PQ2 (wt 0.1) = 0.9 x 0.05  + 0.1 x 0.002 = 0.0452
    # PQ3 (wt 0.2) = 0.8 x 0.0452 + 0.2 x 0.002 = 0.03656, flat thereafter
    assert new.balance == pytest.approx(225.0)
    assert new.rate_path[1] == pytest.approx(0.05)
    assert new.rate_path[2] == pytest.approx(0.0452)
    assert new.rate_path[3] == pytest.approx(0.03656)
    assert new.rate_path[9] == pytest.approx(0.03656)
    assert block.scalar == pytest.approx(0.865)
    # the pivot-vs-M.1 reconciliation monitor is a note, never an adjustment
    assert any("auto pivot-D_OS vs M.1" in note for note in diagnostics.notes)


def test_auto_scalar_bounds():
    assert parse_auto_scalar("0.948") == pytest.approx(0.948)
    with pytest.raises(ValidationFailure):
        parse_auto_scalar("8.65")
    with pytest.raises(ValidationFailure):
        parse_auto_scalar("published")


def test_oc_products_and_line_rates(spec):
    products, census = load_oc_products(spec)
    names = {(p.schedule, p.name) for p in products}
    assert ("A.7", "secured-revolving") in names
    assert ("A.9", "other") in names
    assert ("X.1", "other") not in {(p.schedule, p.name) for p in products}
    overdraft = next(p for p in products if p.name == "overdraft")
    assert overdraft.line_key is None
    rates, _ = load_line_item_rates(spec)
    # the balances-section and GII-section "Credit Cards" decoys must not match
    assert rates["credit_cards"] == pytest.approx(0.14)
    assert rates["non_purpose"] == pytest.approx(0.06)
    assert len(rates) == 7


def test_line_items_section_selection(spec):
    from dataclasses import replace
    rates, census = load_line_item_rates(replace(spec, line_items_section=2))
    assert rates["credit_cards"] == pytest.approx(0.05)
    assert all(v == pytest.approx(0.05) for v in rates.values())
    assert any("reading section 2" in note for note in census.notes)


def test_other_consumer_engine_hand_golden(spec, m1):
    products, _ = load_oc_products(spec)
    rates, _ = load_line_item_rates(spec)
    diagnostics = RetailDiagnostics()
    blocks = build_other_consumer(products, rates, m1, {q: PRIME[q] for q in QUARTERS},
                                  0.08, QUARTERS, diagnostics)
    by_name = {block.name: block for block in blocks}
    us_oc = by_name["us_other_consumer"]
    assert us_oc.scalar == pytest.approx(1.072)
    secured_rev = next(s for s in us_oc.streams if s.name == "secured-revolving")
    # balance = M.1 OC dom 120 x share 2/4 = 60; spread = 0.14 - 0.08 = 0.06
    # PQ1 = 0.05 + 0.06 = 0.11 -> income 60 x 0.11 / 4 = 1.65
    assert secured_rev.balance == pytest.approx(60.0)
    assert secured_rev.income_path[1] == pytest.approx(1.65)
    overdraft = next(s for s in us_oc.streams if s.name == "overdraft")
    assert overdraft.total_income == 0.0
    sb = by_name["us_small_business"]
    assert sb.scalar == pytest.approx(1.033)
    loc = next(s for s in sb.streams if s.name == "line of credit")
    # balance = M.1 SB dom 80 x share 3/4 = 60; spread = 0.077 - 0.08 = -0.003
    assert loc.balance == pytest.approx(60.0)
    assert loc.income_path[1] == pytest.approx(60 * (0.05 - 0.003) / 4)
    singles = by_name["m1_direct"]
    first_lien = next(s for s in singles.streams if s.name == "intl_first_lien")
    # balance = first-mortgages intl 25; spread = 0.0415 - 0.08 = -0.0385
    # PQ1 = 0.0115; PQ2 = -0.0085 -> floored at ZERO (the observed rule)
    assert first_lien.balance == pytest.approx(25.0)
    assert first_lien.rate_path[1] == pytest.approx(0.0115)
    assert first_lien.rate_path[2] == 0.0
    assert first_lien.floor_binds == tuple(range(2, 10))
    non_purpose = next(s for s in singles.streams if s.name == "non_purpose_lending")
    assert non_purpose.balance == pytest.approx(100.0)   # dom 90 + intl 10


def test_family_summary_shape(spec, m1):
    segments, _ = load_card_query(spec)
    blocks = build_card(segments, m1, {q: PRIME[q] for q in QUARTERS}, 0.08,
                        "reported", QUARTERS, RetailDiagnostics())
    summary = family_summary(blocks, QUARTERS)
    card = summary["card"]
    # consumer: 250 x (0.17 + 0.15 x 3)/4 x 0.969 over PQ1..4, etc. — just check
    # 4Q < 9Q and both positive, plus the exact PQ1..4 consumer piece
    consumer_4q = (250 * 0.17 / 4 + 3 * (250 * 0.15 / 4)) * 0.969
    sme_4q = (30 * 0.15 / 4 + 3 * (30 * 0.13 / 4)) * 1.033
    assert card["cum_4q"] == pytest.approx(consumer_4q + sme_4q)
    assert card["cum_9q"] > card["cum_4q"]

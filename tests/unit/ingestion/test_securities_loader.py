"""Securities workbook loader (PID-SEC-6): synthetic workbook built in-test →
canonical positions; policy errors (unmapped category, unmatched enrichment);
PID-SEC-3 proxy; parked WAL skip; prepayment pivot parsing; dollars→millions."""

from __future__ import annotations

import datetime as dt
from pathlib import Path

import pytest

openpyxl = pytest.importorskip("openpyxl")

from scb_ppnr.ingestion import load_config, load_securities_inputs
from scb_ppnr.ingestion.config import (
    FirmDataConfig,
    IngestionConfig,
    SecuritiesConfig,
    SecuritiesEnrichmentSheet,
    TableSource,
)
from scb_ppnr.interest_income import (
    FLOOR_MODE_SECURITY,
    ValidationFailure,
    project_mbs,
    project_other_sec,
    project_ust,
)

EPOCH = dt.date(1899, 12, 30)
REPORT = 20241231


def serial(year: int, month: int, day: int) -> int:
    return (dt.date(year, month, day) - EPOCH).days


MDRM = ["D_DT", "CQSCP083", "CQSCP084", "CQSCP087", "CQSCP089", "CQSCP090", "CQSCP092", "CQSCP094", "CQSCJH21"]


def build_workbook(path: Path, positions: list[list], enrichment: list[list], prepay: list[list] | None,
                   extra_headers: list[str] | None = None) -> None:
    header = MDRM + (extra_headers or [])               # PID-SEC-9 technical columns share the MDRM row
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Positions"
    ws.append([None] * len(header))                     # blank row
    ws.append(["tech"] * len(header))                   # tech-name row (unused by the loader)
    ws.append(["desc"] * len(header))                   # description row
    ws.append(header)                                   # MDRM header row
    for row in positions:
        ws.append(row)
    ito = wb.create_sheet("ITO")
    ito.append(["CUSIP", "Maturity Date", "Coupon Rate", "CPN_TYP", "CPN_Floor", "WAL", "Formula"])
    for row in enrichment:
        ito.append(row)
    if prepay is not None:
        ps = wb.create_sheet("prepay")
        ps.append(["Sum of current_face", "Column Labels"])
        ps.append(["Row Labels", 0, 3, 6, 9, 12, 15, 18, 21, 24, 27, "Grand Total"])
        for row in prepay:
            ps.append(row)
    wb.save(path)


def make_config(tmp_path: Path, *, prepayment: bool = True, tech: bool = False) -> IngestionConfig:
    return IngestionConfig(
        base_dir=tmp_path,
        firm_data=FirmDataConfig(
            firm_id="FIRM_T",
            spot=TableSource(Path("unused_spot.csv")),
            quarterly=TableSource(Path("unused_quarterly.csv")),
            securities=SecuritiesConfig(
                workbook=Path("securities.xlsx"),
                positions_sheet="Positions",
                money_scale="dollars",
                coupon_scale="percent",
                book_yield_scale="percent",
                floor_mode=FLOOR_MODE_SECURITY,
                positions_maturity_years_column="Maturity (yr)" if tech else None,
                positions_coupon_column="Coupon Rate (decimal)" if tech else None,
                positions_floor_column="Coupon Rate Floor (decimal)" if tech else None,
                positions_rate_type_column="Float or fixed indicator" if tech else None,
                prepayment_sheet="prepay" if prepayment else None,
                enrichment=(
                    SecuritiesEnrichmentSheet(
                        sheet="ITO", key_column="CUSIP", maturity_column="Maturity Date",
                        coupon_column="Coupon Rate", rate_type_column="CPN_TYP",
                        wal_column="WAL", floor_column="CPN_Floor",
                        floater_indicator_column="Formula", header_row=1,
                    ),
                ),
            ),
        ),
    )


def standard_workbook(tmp_path: Path) -> None:
    positions = [
        # D_DT, id, category, AC$, face$, orig face$, intent, BY%, price
        [REPORT, "UST00001A", "US Treasuries & Agencies", 960e6, 1000e6, 1000e6, "AFS", 4.2, None],
        [REPORT, "AGY00001A", "Agency MBS", 950e6, 1000e6, 1200e6, "AFS", 5.0, None],
        [REPORT, "AGY00002B", "Agency MBS", 500e6, 500e6, 500e6, "HTM", 5.0, None],
        [REPORT, "CMB00001A", "CMBS", 900e6, 1000e6, 1000e6, "AFS", 8.0, None],
        [REPORT, "OTH00001A", "Corporate Bond", 2000e6, 2000e6, 2000e6, "AFS", 5.0, None],
        [REPORT, "EQY00001A", "Common Stock (Equity)", 10e6, 10e6, 10e6, "EQ", None, None],
        [REPORT, "UNS00001A", "Sovereign Bond", 0, 100e6, 100e6, "AFS", None, 99.5],
        [REPORT, "WAL00001A", "Municipal Bond", 90e6, 100e6, 100e6, "AFS", 5.0, None],
    ]
    enrichment = [
        ["UST00001A", serial(2025, 12, 31), 4.0, "FIXED", None, None, "N"],
        ["AGY00001A", None, 5.0, "FIXED", None, 2.5, "N"],
        ["AGY00002B", None, 5.0, "FIXED", None, 3.0, "N"],
        ["CMB00001A", serial(2035, 12, 31), 4.0, "FIXED", None, None, "N"],
        ["OTH00001A", serial(2035, 6, 30), 5.0, "FIXED", None, None, "N"],
        ["UNS00001A", None, 5.0, "FIXED", None, None, "Y"],       # deliberate flag mismatch
        ["WAL00001A", serial(2030, 12, 31), 3.0, "FIXED", None, -0.1, "N"],
    ]
    prepay = [
        ["AGY00001A", 1000e6, 800e6, 800e6, 800e6, 800e6, 800e6, 800e6, 800e6, 800e6, 800e6, 7200e6],
        ["ZRO00001Z", 500e6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],       # PQ1 = 0 → skipped at load
        ["BLK00001B", None, None, None, None, None, None, None, None, None, None, None],  # all blank → PQ1 reads 0 → skipped
    ]
    build_workbook(tmp_path / "securities.xlsx", positions, enrichment, prepay)


def test_loader_end_to_end(tmp_path, make_income_scenario):
    standard_workbook(tmp_path)
    inputs = load_securities_inputs(make_config(tmp_path))

    assert [p.security_id for p in inputs.ust] == ["UST00001A"]
    assert sorted(p.security_id for p in inputs.mbs) == ["AGY00001A", "AGY00002B", "CMB00001A"]
    assert sorted(p.security_id for p in inputs.other_sec) == ["OTH00001A", "UNS00001A"]

    ust = inputs.ust[0]
    assert ust.current_face == pytest.approx(1000.0)              # dollars → millions
    assert ust.coupon_rate == pytest.approx(0.04)                 # percent → decimal
    assert ust.maturity_quarters == 4                             # 365 days → 4 quarters
    assert ust.maturity_years == pytest.approx(1.0)               # PID-SEC-8: day difference / 365

    agency = next(p for p in inputs.mbs if p.security_id == "AGY00001A")
    assert agency.face_path is not None and agency.face_path[0] == pytest.approx(1000.0)
    assert agency.face_path[1] == pytest.approx(800.0)
    assert agency.maturity_quarters == 10                         # PID-SEC-7: ceil(4 × WAL 2.5)
    multifam = next(p for p in inputs.mbs if p.security_id == "AGY00002B")
    assert multifam.face_path is None
    assert multifam.maturity_quarters == 12                       # PID-SEC-7: ceil(4 × WAL 3.0)
    assert any("multi-family" in w for w in inputs.warnings)
    assert sum("PID-SEC-7" in w for w in inputs.warnings) == 2    # WAL-as-maturity fallback logged

    unsettled = next(p for p in inputs.other_sec if p.security_id == "UNS00001A")
    assert unsettled.ac_proxied and unsettled.amortized_cost == pytest.approx(99.5)   # 99.5/100 × 100
    assert any("PID-SEC-3" in w for w in inputs.warnings)
    assert any(w.startswith("HIGHLIGHT WAL00001A") for w in inputs.warnings)          # parked skip
    assert any("out-of-scope" in w for w in inputs.warnings)
    mismatches = [w for w in inputs.warnings if "floater-indicator" in w]
    assert len(mismatches) == 1 and "UNS00001A" in mismatches[0]                      # monitor, not fatal
    pq1_skips = [w for w in inputs.warnings if "PQ1 face is 0" in w]
    assert len(pq1_skips) == 2                                                        # numeric 0 AND blank PQ1
    assert any("ZRO00001Z" in w for w in pq1_skips) and any("BLK00001B" in w for w in pq1_skips)
    assert not any("matches no in-scope" in w for w in inputs.warnings)               # skipped ≠ leftover

    scenario = make_income_scenario()
    ust_result = project_ust(inputs.ust, scenario, firm_id=inputs.firm_id)
    assert ust_result.income_path()[1] == pytest.approx(20.0)     # 10 coupon + 10 accretion
    assert ust_result.income_path()[5] == pytest.approx(10.0)     # reinvested at 4%
    mbs_result = project_mbs(inputs.mbs, scenario, firm_id=inputs.firm_id, floor_mode="security_floor")
    assert mbs_result.quarters[0].diagnostics.coupon_accrual == pytest.approx(12.5 + 6.25 + 10.0)
    other_result = project_other_sec(inputs.other_sec, scenario, firm_id=inputs.firm_id, floor_mode="security_floor")
    assert other_result.income_path()[1] == pytest.approx(25.0 + (0.05 * 100.0 / 4))  # clean + proxied coupon


def test_prepayment_blank_cells_read_as_zero(tmp_path, make_income_scenario):
    positions = [[REPORT, "AGY00009X", "Agency MBS", 450e6, 500e6, 500e6, "AFS", 5.0, None]]
    enrichment = [["AGY00009X", None, 5.0, "FIXED", None, 2.5, "N"]]
    prepay = [["AGY00009X", 500e6, 400e6, 300e6, None, None, None, None, None, None, None, 0]]
    build_workbook(tmp_path / "securities.xlsx", positions, enrichment, prepay)
    inputs = load_securities_inputs(make_config(tmp_path))
    agency = inputs.mbs[0]
    assert agency.face_path is not None
    assert agency.face_path[1] == pytest.approx(400.0)
    assert agency.face_path[2] == pytest.approx(300.0)
    assert all(agency.face_path[q] == 0.0 for q in range(3, 10))                      # blanks → 0
    assert not any("read as 0" in w for w in inputs.warnings)                         # silent per user 2026-07-24
    result = project_mbs(inputs.mbs, make_income_scenario(), firm_id=inputs.firm_id, floor_mode="security_floor")
    assert result.quarters[2].diagnostics.coupon_accrual == pytest.approx(0.05 * 300.0 / 4)   # PQ3 on PQ2 EOP face
    assert result.quarters[3].diagnostics.coupon_accrual == 0.0                       # PQ3 EOP face is 0 → PQ4 accrues nothing


def test_price_column_fallback_by_technical_name(tmp_path):
    # MDRM row lacks CQSCJH21; the technical-name row carries "Price" in that slot.
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Positions"
    mdrm_row = ["D_DT", "CQSCP083", "CQSCP084", "CQSCP087", "CQSCP089", "CQSCP090", "CQSCP092", "CQSCP094", "XXNOCODE"]
    tech_row = ["D_DT", "ID", "DESC1", "AC", "FACE", "OFACE", "INTENT", "BY", "Price"]
    ws.append([None] * 9)
    ws.append(tech_row)
    ws.append(["desc"] * 9)
    ws.append(mdrm_row)
    ws.append([REPORT, "PRX00001A", "Sovereign Bond", 0, 100e6, 100e6, "AFS", None, 99.5])
    ito = wb.create_sheet("ITO")
    ito.append(["CUSIP", "Maturity Date", "Coupon Rate", "CPN_TYP", "CPN_Floor", "WAL", "Formula"])
    ito.append(["PRX00001A", None, 5.0, "FIXED", None, None, "N"])
    wb.save(tmp_path / "securities.xlsx")

    inputs = load_securities_inputs(make_config(tmp_path, prepayment=False))
    position = inputs.other_sec[0]
    assert position.ac_proxied and position.amortized_cost == pytest.approx(99.5)
    assert any("located by technical name 'Price'" in w for w in inputs.warnings)


def test_unmapped_category_is_a_hard_error(tmp_path):
    positions = [[REPORT, "COV00001A", "Covered Bond", 100e6, 100e6, 100e6, "AFS", 5.0, None]]
    enrichment = [["COV00001A", serial(2030, 1, 1), 4.0, "FIXED", None, None]]
    build_workbook(tmp_path / "securities.xlsx", positions, enrichment, None)
    with pytest.raises(ValidationFailure, match="not in the confirmed PID-SEC-5 mapping"):
        load_securities_inputs(make_config(tmp_path, prepayment=False))


def test_unmatched_enrichment_skips_with_highlight(tmp_path):
    positions = [[REPORT, "NOE00001A", "Corporate Bond", 100e6, 100e6, 100e6, "AFS", 5.0, None]]
    build_workbook(tmp_path / "securities.xlsx", positions, [], None)
    inputs = load_securities_inputs(make_config(tmp_path, prepayment=False))
    assert inputs.other_sec == ()
    assert any(w.startswith("HIGHLIGHT NOE00001A") and "no enrichment match" in w for w in inputs.warnings)
    assert any("skipped for missing enrichment" in w for w in inputs.warnings)


def test_multi_lot_cusip_apportions_prepayment_and_step_variable_vocab(tmp_path, make_income_scenario):
    # Two lots of one Agency CUSIP (600/400) + one VARIABLE and one STEP CPN security.
    positions = [
        [REPORT, "AGY00005X", "Agency MBS", 570e6, 600e6, 600e6, "AFS", 5.0, None],
        [REPORT, "AGY00005X", "Agency MBS", 380e6, 400e6, 400e6, "HTM", 5.0, None],
        [REPORT, "VAR00001X", "Agency MBS", 200e6, 200e6, 200e6, "AFS", 5.0, None],
        [REPORT, "STP00001X", "Agency MBS", 100e6, 100e6, 100e6, "AFS", 5.0, None],
    ]
    enrichment = [
        ["AGY00005X", None, 5.0, "FIXED", None, 2.5, "N"],
        ["VAR00001X", None, 4.0, "VARIABLE", None, 2.0, "Y"],
        ["STP00001X", None, 3.0, "STEP CPN", None, 2.0, "N"],
    ]
    prepay = [["AGY00005X", 1000e6, 900e6, 800e6, 800e6, 800e6, 800e6, 800e6, 800e6, 800e6, 800e6, 0]]
    build_workbook(tmp_path / "securities.xlsx", positions, enrichment, prepay)
    inputs = load_securities_inputs(make_config(tmp_path))

    lots = [p for p in inputs.mbs if p.security_id.startswith("AGY00005X")]
    assert len(lots) == 2 and lots[0].security_id != lots[1].security_id       # fallback ids unique
    big = next(p for p in lots if p.current_face == pytest.approx(600.0))
    small = next(p for p in lots if p.current_face == pytest.approx(400.0))
    assert big.face_path[0] == pytest.approx(600.0)                            # factor form: row face × path/path0
    assert big.face_path[1] == pytest.approx(540.0)                            # 600 × 900/1000
    assert small.face_path[1] == pytest.approx(360.0)                          # 400 × 900/1000
    assert any("survival factor" in w for w in inputs.warnings)

    variable = next(p for p in inputs.mbs if p.security_id.startswith("VAR"))
    assert variable.rate_type == "floating"                                    # VARIABLE mapped
    step = next(p for p in inputs.mbs if p.security_id.startswith("STP"))
    assert step.rate_type == "fixed"                                           # STEP CPN interim-fixed
    assert any("step-coupon" in w and "confirmed" in w for w in inputs.warnings)


def test_positions_sheet_technical_columns_pid_sec9(tmp_path):
    # Extra cells beyond the 9 MDRM columns: Maturity (yr), Coupon Rate (decimal),
    # Floor (decimal), Float or fixed indicator.
    positions = [
        [REPORT, "MUN00009A", "Municipal Bond", 90e6, 100e6, 100e6, "AFS", 5.0, None, 4.5, None, None, "Fixed"],
        [REPORT, "FLT00009A", "CLO", 100e6, 100e6, 100e6, "AFS", 5.0, None, None, 0.052, 0.048, "Fixed"],
    ]
    enrichment = [
        ["MUN00009A", None, 3.0, "FIXED", None, None, "N"],        # maturity date missing → years fallback
        ["FLT00009A", None, None, "FLOATING", 2.0, None, "Y"],     # blank coupon; ITO floor 2% (percent)
    ]
    build_workbook(tmp_path / "securities.xlsx", positions, enrichment, None,
                   extra_headers=["Maturity (yr)", "Coupon Rate (decimal)", "Coupon Rate Floor (decimal)",
                                  "Float or fixed indicator"])
    inputs = load_securities_inputs(make_config(tmp_path, prepayment=False, tech=True))

    muni = next(p for p in inputs.other_sec if p.security_id == "MUN00009A")
    assert muni.maturity_years == pytest.approx(4.5)               # positions-sheet years fallback
    assert muni.maturity_quarters == 18                            # ceil(4 × 4.5)
    assert muni.coupon_rate == pytest.approx(0.03)                 # enrichment coupon stays primary
    assert muni.excel_rate_label == "Fixed"                        # carried verification-only

    floater = next(p for p in inputs.other_sec if p.security_id == "FLT00009A")
    assert floater.coupon_rate == pytest.approx(0.052)             # blank ITO coupon → positions column
    assert floater.coupon_floor == pytest.approx(0.048)            # positions floor PREFERRED over ITO 0.02
    assert floater.rate_type == "floating"                         # ITO still governs the model
    assert floater.excel_rate_label == "Fixed"                     # sheet disagrees — monitor fires
    assert any("PID-SEC-9" in w and "maturity" in w for w in inputs.warnings)
    assert any("PID-SEC-9" in w and "coupon column" in w for w in inputs.warnings)
    assert any("indicator disagrees" in w for w in inputs.warnings)


def test_technical_column_missing_from_header_is_hard_error(tmp_path):
    positions = [[REPORT, "MUN00009A", "Municipal Bond", 90e6, 100e6, 100e6, "AFS", 5.0, None]]
    enrichment = [["MUN00009A", serial(2030, 1, 1), 3.0, "FIXED", None, None, "N"]]
    build_workbook(tmp_path / "securities.xlsx", positions, enrichment, None)   # no extra headers
    with pytest.raises(ValidationFailure, match="PID-SEC-9"):
        load_securities_inputs(make_config(tmp_path, prepayment=False, tech=True))


def test_floor_suspect_monitor_logs_never_clamps(tmp_path):
    # ITO floor cell 30 (percent scale → 0.30): under the 0.5 hard guard but implausible.
    positions = [[REPORT, "FLR00001A", "CLO", 100e6, 100e6, 100e6, "AFS", 5.0, None]]
    enrichment = [["FLR00001A", serial(2030, 1, 1), 6.0, "FLOATING", 30.0, None, "Y"]]
    build_workbook(tmp_path / "securities.xlsx", positions, enrichment, None)
    inputs = load_securities_inputs(make_config(tmp_path, prepayment=False))
    clo = inputs.other_sec[0]
    assert clo.coupon_floor == pytest.approx(0.30)                 # applied AS-IS, never clamped
    assert any(w.startswith("HIGHLIGHT FLR00001A") and "suspect source-cell units" in w
               for w in inputs.warnings)


def test_excel_error_literals_treated_as_missing(tmp_path):
    # The reference sheet's derived columns error to #VALUE! when their own inputs
    # are missing (user-directed 2026-07-27): treated as missing, never a hard stop.
    positions = [
        [REPORT, "ERR00001A", "Municipal Bond", 90e6, 100e6, 100e6, "AFS", 5.0, None,
         "#VALUE!", "#VALUE!", "#VALUE!"],
    ]
    enrichment = [["ERR00001A", None, 3.0, "FIXED", None, "#N/A", "N"]]   # WAL error cell too
    build_workbook(tmp_path / "securities.xlsx", positions, enrichment, None,
                   extra_headers=["Maturity (yr)", "Coupon Rate (decimal)", "Coupon Rate Floor (decimal)",
                                  "Float or fixed indicator"])
    inputs = load_securities_inputs(make_config(tmp_path, prepayment=False, tech=True))

    muni = inputs.other_sec[0]
    assert muni.maturity_years is None and muni.maturity_quarters is None   # #VALUE! → missing
    assert muni.coupon_floor is None and muni.wal_years is None
    assert muni.coupon_rate == pytest.approx(0.03)                          # enrichment coupon unaffected
    census = [w for w in inputs.warnings if "Excel error cell" in w]
    assert len(census) == 1 and "4 " in census[0]                           # 3 positions + 1 enrichment


def test_config_parses_pid_sec9_columns_and_new_floor_mode(tmp_path):
    (tmp_path / "c.toml").write_text(
        '[firm_data]\nfirm_id = "F"\n'
        '[firm_data.spot]\npath = "s.csv"\n'
        '[firm_data.quarterly]\npath = "q.csv"\n'
        '[firm_data.securities]\nworkbook = "w.xlsx"\npositions_sheet = "P"\n'
        'money_scale = "dollars"\ncoupon_scale = "percent"\nbook_yield_scale = "percent"\n'
        'floor_mode = "security_floor_else_zero"\n'
        'positions_maturity_years_column = "Maturity (yr)"\n'
        'positions_coupon_column = "Coupon Rate (decimal)"\n'
        'positions_floor_column = "Coupon Rate Floor (decimal)"\n'
        'positions_rate_type_column = "Float or fixed indicator"\n'
        'floating_projection = "neg_hold_blend13"\n'
        'book_yield_categories = ["Municipal Bond"]\n'
        '[firm_data.securities.floating_projection_overrides]\n'
        '"CLO" = "blend13"\n'
        '"Domestic Non-Agency RMBS (incl HEL ABS)" = "flat_c0"\n'
    )
    sc = load_config(tmp_path / "c.toml").firm_data.securities
    assert sc.floor_mode == "security_floor_else_zero"
    assert sc.floating_projection == "neg_hold_blend13"
    assert sc.book_yield_categories == ("Municipal Bond",)
    assert dict(sc.floating_projection_overrides) == {
        "CLO": "blend13", "Domestic Non-Agency RMBS (incl HEL ABS)": "flat_c0",
    }
    assert sc.positions_maturity_years_column == "Maturity (yr)"
    assert sc.positions_coupon_column == "Coupon Rate (decimal)"
    assert sc.positions_floor_column == "Coupon Rate Floor (decimal)"
    assert sc.positions_rate_type_column == "Float or fixed indicator"

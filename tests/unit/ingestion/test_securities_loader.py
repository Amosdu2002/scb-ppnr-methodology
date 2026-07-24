"""Securities workbook loader (PID-SEC-6): synthetic workbook built in-test →
canonical positions; policy errors (unmapped category, unmatched enrichment);
PID-SEC-3 proxy; parked WAL skip; prepayment pivot parsing; dollars→millions."""

from __future__ import annotations

import datetime as dt
from pathlib import Path

import pytest

openpyxl = pytest.importorskip("openpyxl")

from scb_ppnr.ingestion import load_securities_inputs
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


def build_workbook(path: Path, positions: list[list], enrichment: list[list], prepay: list[list] | None) -> None:
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Positions"
    ws.append([None] * len(MDRM))                       # blank row
    ws.append(["tech"] * len(MDRM))                     # tech-name row (unused by the loader)
    ws.append(["desc"] * len(MDRM))                     # description row
    ws.append(MDRM)                                     # MDRM header row
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


def make_config(tmp_path: Path, *, prepayment: bool = True) -> IngestionConfig:
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

    agency = next(p for p in inputs.mbs if p.security_id == "AGY00001A")
    assert agency.face_path is not None and agency.face_path[0] == pytest.approx(1000.0)
    assert agency.face_path[1] == pytest.approx(800.0)
    multifam = next(p for p in inputs.mbs if p.security_id == "AGY00002B")
    assert multifam.face_path is None
    assert any("multi-family" in w for w in inputs.warnings)

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
    assert any("read as 0" in w and "AGY00009X" in w for w in inputs.warnings)
    result = project_mbs(inputs.mbs, make_income_scenario(), firm_id=inputs.firm_id, floor_mode="security_floor")
    assert result.quarters[2].diagnostics.coupon_accrual == pytest.approx(0.05 * 300.0 / 4)   # PQ3 on PQ2 EOP face
    assert result.quarters[3].diagnostics.coupon_accrual == 0.0                       # PQ3 EOP face is 0 → PQ4 accrues nothing


def test_unmapped_category_is_a_hard_error(tmp_path):
    positions = [[REPORT, "COV00001A", "Covered Bond", 100e6, 100e6, 100e6, "AFS", 5.0, None]]
    enrichment = [["COV00001A", serial(2030, 1, 1), 4.0, "FIXED", None, None]]
    build_workbook(tmp_path / "securities.xlsx", positions, enrichment, None)
    with pytest.raises(ValidationFailure, match="not in the confirmed PID-SEC-5 mapping"):
        load_securities_inputs(make_config(tmp_path, prepayment=False))


def test_unmatched_enrichment_is_a_hard_error(tmp_path):
    positions = [[REPORT, "NOE00001A", "Corporate Bond", 100e6, 100e6, 100e6, "AFS", 5.0, None]]
    build_workbook(tmp_path / "securities.xlsx", positions, [], None)
    with pytest.raises(ValidationFailure, match="no enrichment match"):
        load_securities_inputs(make_config(tmp_path, prepayment=False))

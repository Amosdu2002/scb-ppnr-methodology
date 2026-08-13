"""The CRE H.2 workbook binding (PID-LOAN-18/19/20).

Synthetic workbooks built in a temp directory — no company data. Pins the
loader-level rules: DO-NOT-USE line codes excluded and censused, blank
Outstanding Balance read as a genuine zero, optional identifier columns, the
header-alias substitutions, and the row-wired M.1 side balances with the
role-label sanity warning."""

from __future__ import annotations

from pathlib import Path

import pytest

openpyxl = pytest.importorskip("openpyxl")

from scb_ppnr.core.schemas import ValidationFailure
from scb_ppnr.ingestion.loans_cre_mapping import CRE_CATEGORY_NAMES
from scb_ppnr.ingestion.loans_loader import (
    LoansSheetSpec,
    load_cre_facilities,
    load_cre_side_balances,
    load_reference_results,
)


def _workbook(path: Path, code_header: str = "Line Reported on FR Y-9C") -> Path:
    book = openpyxl.Workbook()
    h2 = book.active
    h2.title = "CRE H.2"
    headers = [
        code_header, "Interest Rate Variability", "Lower of Cost or Market Flag",
        "Interest Rate", "Committed Balance", "Outstanding Balance",
        "Interest Rate Floor", "Origination Date", "Maturity Date",
    ]
    for _ in range(3):
        h2.append([None] * len(headers))
    h2.append(headers)
    h2.append([1, 2, 3, 0.07, 200e6, 150e6, 0.05, "15-Oct-2024", "15-Oct-2027"])
    h2.append([3, 1, 3, 0.05, 300e6, None, None, "15-May-2021", "15-Feb-2026"])   # blank outstanding
    h2.append([6, 2, 3, 0.06, 50e6, 40e6, None, None, None])                      # DO NOT USE code
    h2.append([7, 2, 1, 0.09, 90e6, 70e6, None, None, None])                      # international, HFS

    m1 = book.create_sheet("M.1 Balance")
    for _ in range(4):
        m1.append([None] * 11)
    m1.append(["Wholesale - CRE - construction", "Wholesale - CRE - international",
               "1.b(1)", "M", 210.0, "M", 20.0, "M", 15.0, "M", None])            # row 5
    m1.append(["Wholesale - CRE - multi fam", "Wholesale - CRE - international",
               "1.b(2)", "M", 380.0, "M", 0.0, "M", 40.0, "M", 5.0])              # row 6
    m1.append(["Wholesale - CRE - non owner occupied", "Wholesale - CRE - international",
               "1.b(3)(b)", "M", 0.0, "M", 110.0, "M", 30.0, "M", 0.0])           # row 7
    m1.append(["Wholesale - Corp - C&I and others", "Wholesale - Corp - C&I and others",
               "2.a", "M", 700.0, "M", 90.0, "M", 180.0, "M", 10.0])              # row 8 — NOT CRE

    target = path / "cre.xlsx"
    book.save(target)
    return target


def _spec(workbook: Path, **overrides) -> LoansSheetSpec:
    kwargs = dict(
        workbook=workbook,
        cre_h2_sheet="CRE H.2",
        cre_m1_construction_row=5,
        cre_m1_multifamily_row=6,
        cre_m1_non_owner_occupied_row=7,
    )
    kwargs.update(overrides)
    return LoansSheetSpec(**kwargs)


def test_do_not_use_line_codes_are_excluded_and_censused(tmp_path):
    facilities, census = load_cre_facilities(_spec(_workbook(tmp_path)))
    assert len(facilities) == 3                       # the code-6 row never becomes a facility
    assert census.excluded_line_codes[6] == 1
    assert census.excluded_line_code_exposure == pytest.approx(50.0)   # canonical millions
    assert "6_2_3" not in census.reference_keys


def test_blank_outstanding_is_a_genuine_zero_not_a_refusal(tmp_path):
    facilities, census = load_cre_facilities(_spec(_workbook(tmp_path)))
    fixed = next(f for f in facilities if f.segment.variable_type == 1)
    assert fixed.outstanding_balance == 0.0
    assert census.blank_outstanding == 1


def test_missing_identifier_columns_synthesize_row_labels(tmp_path):
    facilities, census = load_cre_facilities(_spec(_workbook(tmp_path)))
    assert all(f.facility_id.startswith("UNIDENTIFIED-ROW-") for f in facilities)
    assert census.id_sources["synthesized"] == 3


def test_the_h2_code_header_alias_is_accepted_and_reported(tmp_path):
    workbook = _workbook(tmp_path, code_header="Line Reported on FR Y9C")
    facilities, census = load_cre_facilities(_spec(workbook))
    assert len(facilities) == 3
    assert any("line-code column read as" in note for note in census.column_substitutions)


def test_cre_side_balances_wire_by_row_and_sum_international(tmp_path):
    balances, notes = load_cre_side_balances(_spec(_workbook(tmp_path)))
    construction = CRE_CATEGORY_NAMES[1]
    international = CRE_CATEGORY_NAMES[4]
    assert balances[(construction, "HFI")] == pytest.approx(210.0)
    assert balances[(construction, "FVO_HFS")] == pytest.approx(20.0)
    assert balances[(international, "HFI")] == pytest.approx(15.0 + 40.0 + 30.0)
    assert balances[(international, "FVO_HFS")] == pytest.approx(0.0 + 5.0 + 0.0)  # blank = 0
    assert not any(note.startswith("WARN") for note in notes)


def test_a_misconfigured_m1_row_earns_a_role_warning(tmp_path):
    # row 8 is a Corporate role — summing it silently would be the failure mode
    balances, notes = load_cre_side_balances(
        _spec(_workbook(tmp_path), cre_m1_multifamily_row=8)
    )
    assert any("WARN" in note and "row 8" in note for note in notes)
    assert balances[(CRE_CATEGORY_NAMES[2], "HFI")] == pytest.approx(700.0)   # summed, but flagged


def test_cre_reference_results_read_the_cre_markers_without_a_merged_block(tmp_path):
    book = openpyxl.Workbook()
    sheet = book.active
    sheet.title = "CRE results"
    sheet.append([None, *[f"PQ{q}" for q in range(10)]])
    sheet.append(["4 - HFI"])
    sheet.append(["Fixed Income", *[0.0] * 10])
    sheet.append(["Variable Rate Income", *[1e6] * 10])
    sheet.append(["Total", *[1.113e6] * 10])
    target = tmp_path / "results.xlsx"
    book.save(target)

    spec = LoansSheetSpec(workbook=target, cre_results_sheet="CRE results")
    results = load_reference_results(
        spec, sheet=spec.cre_results_sheet,
        category_names=CRE_CATEGORY_NAMES, include_merged=False,
    )
    block = results[(CRE_CATEGORY_NAMES[4], "HFI")]
    assert block["variable"][1] == pytest.approx(1.0)          # USD millions
    assert block["total"][1] == pytest.approx(1.113)
    with pytest.raises(ValidationFailure):
        # the sheet's "4 - HFI" marker is outside a map holding only category 1 —
        # refused, never guessed
        load_reference_results(spec, sheet=spec.cre_results_sheet,
                               category_names={1: "only one"}, include_merged=False)


# --- float NaN: the pandas-blank encoding (first real CRE run, 2026-08-12) ---
# openpyxl itself cannot round-trip a float NaN through .xlsx (it writes an
# empty cell), so the fake sheet below feeds the loader NaNs exactly as the
# company workbook's reader delivered them: row 15899's Interest Rate Floor
# arrived as float('nan') and crashed validation instead of meaning "no floor".


class _FakeBook:
    def __init__(self, sheets):
        self._sheets = sheets
        self.sheetnames = list(sheets)

    def __getitem__(self, name):
        class _Sheet:
            def __init__(self, rows):
                self.values = iter(rows)
        return _Sheet(self._sheets[name])

    def close(self):
        pass


def test_a_float_nan_floor_means_no_floor_and_is_censused(monkeypatch, tmp_path):
    from scb_ppnr.ingestion import loans_loader

    headers = [
        "Line Reported on FR Y-9C", "Interest Rate Variability",
        "Lower of Cost or Market Flag", "Interest Rate", "Committed Balance",
        "Outstanding Balance", "Interest Rate Floor", "Origination Date", "Maturity Date",
    ]
    rows = [
        [None] * len(headers), [None] * len(headers), [None] * len(headers),
        headers,
        # floor and maturity arrive as float NaN; the row must load with NO floor
        [1, 2, 3, 0.07, 200e6, 150e6, float("nan"), "15-Oct-2024", float("nan")],
        # outstanding arrives as NaN: a blank -> genuine zero, censused twice
        [3, 1, 3, 0.05, 300e6, float("nan"), None, "15-May-2021", "15-Feb-2026"],
        # a string "NaN" rate is the same blank in text form
        [7, 2, 3, "NaN", 90e6, 70e6, None, None, None],
    ]
    monkeypatch.setattr(loans_loader, "_open", lambda path: _FakeBook({"CRE H.2": rows}))

    facilities, census = load_cre_facilities(
        LoansSheetSpec(workbook=tmp_path / "fake.xlsx", cre_h2_sheet="CRE H.2")
    )
    assert len(facilities) == 3
    floating = next(f for f in facilities if f.segment.variable_type == 2 and f.committed_exposure == 200.0)
    assert floating.interest_rate_floor is None
    assert floating.maturity_date is None
    fixed = next(f for f in facilities if f.segment.variable_type == 1)
    assert fixed.outstanding_balance == 0.0
    assert census.nan_cells == {"floor": 1, "maturity date": 1, "outstanding": 1}
    assert census.blank_outstanding == 1
    international = next(f for f in facilities if f.committed_exposure == 90.0)
    assert international.interest_rate is None            # string "NaN" = missing token
    assert "float-NaN cells as missing" in census.render()


def test_is_missing_treats_non_finite_floats_as_absent():
    from scb_ppnr.ingestion.loans_loader import _is_missing

    assert _is_missing(float("nan"))
    assert _is_missing(float("inf"))
    assert _is_missing("NaN")
    assert not _is_missing(0.0)
    assert not _is_missing(-1.5)

"""Workbook binding for the Corporate wholesale loan model (PID-LOAN-8/9/10).

Reads the firm's single workbook and produces canonical objects the model layers
already consume: `LoanFacility` rows, the merged 9/10/11 bucket balance, and the
3-month Treasury history and projection. Every decision this file makes was
settled before it was written — decoding lives in `loans_mapping`, arithmetic in
`interest_income.loans_launchpoint` / `loans_projection`. This module only binds
physical cells to those.

Sheet names, header rows and column headers are configuration; only the logical
contract is committed here. The workbook itself never enters this repository.

Scales are declared and never guessed (D-006), which matters more than usual
because four different ones live in this one file: H.1 rates are decimals, H.1
exposures are whole dollars, the FR Y-9C extract is in thousands, and the MEV
rates are percentages."""

from __future__ import annotations

import datetime as _dt
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from types import MappingProxyType
from typing import Iterable, Mapping, Sequence

from ..core.schemas import ValidationFailure
from ..interest_income.loans_schemas import LoanFacility, check_quarter_label
from .loans_mapping import (
    FED_CATEGORY_NAMES,
    decode_segment,
    m1_role_category,
    parse_h1_code,
    reference_key,
)
from .normalize import (
    SCALE_DOLLARS,
    SCALE_PERCENT,
    SCALE_THOUSANDS,
    apply_money_scale,
    apply_rate_scale,
    to_float,
)

# Values that all mean "absent". `[NULL]` is the workbook's own token; the Excel
# formula errors follow the PID-SEC-6 amendment — a derived cell that errors
# because its own inputs are missing is a missing value, not a parse failure.
_EXCEL_ERRORS = {"#VALUE!", "#N/A", "#REF!", "#DIV/0!", "#NAME?", "#NULL!", "#NUM!"}
_MISSING_TOKENS = {"", "NA", "N/A", "NONE", "[NULL]", "NULL", "-"} | _EXCEL_ERRORS

# The merged-bucket MDRMs (PID-LOAN-10).
MDRM_PURCHASING_CARRYING_SECURITIES = "BHCK1545"
MDRM_FARMLAND = "BHDM1420"
MERGED_BUCKET_MDRMS = (MDRM_PURCHASING_CARRYING_SECURITIES, MDRM_FARMLAND)

# The sheet spells this correctly (user-confirmed 2026-08-07 — the misspelling
# was in the message, not the workbook). The variant is still accepted second,
# because an extract that does carry it is not worth a failed run, and any
# substitution is reported rather than applied silently.
_VARIABILITY_ALIASES = ("Interest Rate Variability", "Interest Rate Variablility")


@dataclass(frozen=True)
class LoansSheetSpec:
    """Where the Corporate inputs live. Every field is company-local config."""

    workbook: Path
    h1_sheet: str = "CORP H.1"
    h1_header_row: int = 4
    fry9c_sheet: str = "FR-Y9C 4Q 2024"
    fry9c_header_row: int = 8
    fry9c_id_column: str = "ID_RSSD"
    fry9c_value_column_index: int = 3       # 1-based; "the third column"
    m1_sheet: str = "M.1 Balance"
    m1_first_data_row: int = 11
    m1_domestic_role_column_index: int = 1    # 1-based; column A carries the domestic role
    m1_international_role_column_index: int = 2               # column B, the international role
    m1_domestic_value_column_indices: tuple[int, ...] = (5, 7)    # E = HFI at AC, G = HFS/FVO
    m1_international_value_column_indices: tuple[int, ...] = (9, 11)   # I = HFI at AC, K = HFS/FVO
    m1_scale: str = "millions"
    mev_sheet: str = "MEV"
    mev_header_row: int = 1
    mev_scenario_column: str = "Scenario Name"
    mev_date_column: str = "Date"
    mev_3m_column: str = "3-month Treasury rate"
    mev_history_scenario: str = "Actual"
    # declared scales — the loader refuses to run without them
    rate_scale: str = "decimal"
    exposure_scale: str = SCALE_DOLLARS
    fry9c_scale: str = SCALE_THOUSANDS
    mev_rate_scale: str = SCALE_PERCENT
    # H.1 column headers
    col_facility_id: str = "Customer ID"
    col_h1_code: str = "Line Reported on FR Y9C"
    col_variability: str | None = None      # None -> try the aliases
    col_locom: str = "Lower of Cost or Market Flag"
    col_interest_rate: str = "Interest Rate"
    col_committed: str = "Committed Exposure Global"
    col_utilized: str = "Utilized Exposure Global"
    col_floor: str = "Interest Rate Floor"
    col_origination: str = "Origination Date"
    col_maturity: str = "Maturity Date"


@dataclass
class LoaderCensus:
    """What the load found, reported rather than assumed.

    Missing rates and floors are expected and benign; a large count is not, so
    the exposure behind each is carried alongside the count."""

    rows_read: int = 0
    missing_interest_rate: int = 0
    missing_interest_rate_exposure: float = 0.0
    missing_floor: int = 0
    missing_origination_date: int = 0
    missing_maturity_date: int = 0
    reference_keys: Counter = field(default_factory=Counter)
    column_substitutions: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def render(self) -> str:
        lines = ["LOANS LOADER CENSUS"]
        lines.append(f"  rows read                   : {self.rows_read}")
        lines.append(
            f"  missing Interest Rate       : {self.missing_interest_rate}"
            f"  (exposure {self.missing_interest_rate_exposure:,.2f})"
        )
        lines.append(f"  no floor on file            : {self.missing_floor}")
        lines.append(f"  missing Origination Date    : {self.missing_origination_date}")
        lines.append(f"  missing Maturity Date       : {self.missing_maturity_date}")
        lines.append(f"  distinct reference keys     : {len(self.reference_keys)}")
        for key, count in sorted(self.reference_keys.items()):
            lines.append(f"      {key:<14} {count}")
        for note in self.column_substitutions + self.warnings:
            lines.append(f"  NOTE: {note}")
        return "\n".join(lines)


def _open(path: Path):
    try:
        import openpyxl
    except ImportError as exc:  # pragma: no cover - environment guard
        raise ValidationFailure("reading the loans workbook requires openpyxl") from exc
    if not path.exists():
        raise ValidationFailure(f"loans workbook not found: {path}")
    return openpyxl.load_workbook(path, read_only=True, data_only=True)


def _sheet(workbook, name: str, path: Path):
    if name not in workbook.sheetnames:
        raise ValidationFailure(
            f"{path}: sheet {name!r} not found; available: {sorted(workbook.sheetnames)}"
        )
    return workbook[name]


def _header_index(rows: Sequence[Sequence[object]], header_row: int, context: str) -> dict[str, int]:
    if len(rows) < header_row:
        raise ValidationFailure(f"{context}: header row {header_row} is beyond the end of the sheet")
    return {
        str(cell).strip(): index
        for index, cell in enumerate(rows[header_row - 1])
        if cell is not None and str(cell).strip()
    }


def _column(header: Mapping[str, int], name: str, context: str) -> int:
    if name not in header:
        raise ValidationFailure(
            f"{context}: column {name!r} not found on the header row; available: {sorted(header)}"
        )
    return header[name]


def _is_missing(value: object) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return value.strip().upper() in _MISSING_TOKENS
    return False


def _optional_rate(value: object, scale: str, *, context: str) -> float | None:
    if _is_missing(value):
        return None
    return apply_rate_scale(scale, to_float(value, context=context), context=context)


def _parse_date(value: object, *, context: str) -> _dt.date:
    """Coerce the workbook's date encodings, `15-Oct-2024` chief among them."""
    if isinstance(value, _dt.datetime):
        return value.date()
    if isinstance(value, _dt.date):
        return value
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        number = float(value)
        if 10_000_000.0 <= number <= 99_991_231.0:              # yyyymmdd
            text = str(int(number))
            return _dt.date(int(text[:4]), int(text[4:6]), int(text[6:8]))
        if 0.0 < number < 200_000.0:                            # Excel serial
            return _dt.date(1899, 12, 30) + _dt.timedelta(days=int(round(number)))
    if isinstance(value, str):
        text = value.strip()
        for fmt in ("%d-%b-%Y", "%d-%B-%Y", "%m/%d/%Y", "%Y-%m-%d"):
            try:
                return _dt.datetime.strptime(text, fmt).date()
            except ValueError:
                continue
    raise ValidationFailure(
        f"{context}: cannot interpret {value!r} as a date (expected 15-Oct-2024, "
        f"mm/dd/yyyy, yyyy-mm-dd, yyyymmdd, or an Excel serial)"
    )


def _optional_date(value: object, *, context: str) -> _dt.date | None:
    return None if _is_missing(value) else _parse_date(value, context=context)


def _resolve_variability_column(header: Mapping[str, int], spec: LoansSheetSpec,
                                census: LoaderCensus, context: str) -> int:
    if spec.col_variability is not None:
        return _column(header, spec.col_variability, context)
    for candidate in _VARIABILITY_ALIASES:
        if candidate in header:
            if candidate != _VARIABILITY_ALIASES[0]:
                census.column_substitutions.append(
                    f"rate-variability column read as {candidate!r} (the sheet's usual spelling is "
                    f"{_VARIABILITY_ALIASES[0]!r})"
                )
            return header[candidate]
    raise ValidationFailure(
        f"{context}: none of the rate-variability column names {list(_VARIABILITY_ALIASES)} were "
        f"found; available: {sorted(header)}. Declare the exact header in config rather than "
        f"letting the loader guess."
    )


def load_facilities(spec: LoansSheetSpec) -> tuple[list[LoanFacility], LoaderCensus]:
    """Read `CORP H.1` into canonical facilities.

    Rows whose Fed Category has no H.1 code cannot appear here by construction —
    Categories 9, 10 and 11 carry no code at all and arrive via
    `load_merged_bucket_balance` instead (PID-LOAN-10)."""
    workbook = _open(spec.workbook)
    try:
        rows = [list(row) for row in _sheet(workbook, spec.h1_sheet, spec.workbook).values]
    finally:
        workbook.close()

    context = f"{spec.workbook.name}:{spec.h1_sheet}"
    census = LoaderCensus()
    header = _header_index(rows, spec.h1_header_row, context)

    idx_id = _column(header, spec.col_facility_id, context)
    idx_code = _column(header, spec.col_h1_code, context)
    idx_var = _resolve_variability_column(header, spec, census, context)
    idx_locom = _column(header, spec.col_locom, context)
    idx_rate = _column(header, spec.col_interest_rate, context)
    idx_committed = _column(header, spec.col_committed, context)
    idx_utilized = _column(header, spec.col_utilized, context)
    idx_floor = _column(header, spec.col_floor, context)
    idx_orig = _column(header, spec.col_origination, context)
    idx_mat = _column(header, spec.col_maturity, context)

    def cell(row: Sequence[object], index: int) -> object:
        return row[index] if index < len(row) else None

    facilities: list[LoanFacility] = []
    for offset, row in enumerate(rows[spec.h1_header_row:], start=spec.h1_header_row + 1):
        if all(_is_missing(value) for value in row):
            continue
        where = f"{context} row {offset}"
        facility_id = cell(row, idx_id)
        if _is_missing(facility_id):
            raise ValidationFailure(f"{where}: {spec.col_facility_id!r} is empty — no row may be unidentified")

        raw_code, raw_var, raw_locom = cell(row, idx_code), cell(row, idx_var), cell(row, idx_locom)
        segment = decode_segment(raw_code, raw_var, raw_locom)
        census.reference_keys[reference_key(raw_code, raw_var, raw_locom)] += 1

        committed = apply_money_scale(
            spec.exposure_scale, to_float(cell(row, idx_committed), context=f"{where}: committed"),
            context=f"{where}: committed",
        )
        utilized = apply_money_scale(
            spec.exposure_scale, to_float(cell(row, idx_utilized), context=f"{where}: utilized"),
            context=f"{where}: utilized",
        )
        rate = _optional_rate(cell(row, idx_rate), spec.rate_scale, context=f"{where}: interest rate")
        floor = _optional_rate(cell(row, idx_floor), spec.rate_scale, context=f"{where}: floor")
        originated = _optional_date(cell(row, idx_orig), context=f"{where}: origination date")
        matures = _optional_date(cell(row, idx_mat), context=f"{where}: maturity date")

        census.rows_read += 1
        if rate is None:
            census.missing_interest_rate += 1
            census.missing_interest_rate_exposure += committed
        if floor is None:
            census.missing_floor += 1
        if originated is None:
            census.missing_origination_date += 1
        if matures is None:
            census.missing_maturity_date += 1

        facilities.append(
            LoanFacility(
                facility_id=str(facility_id).strip(),
                segment=segment,
                committed_exposure=committed,
                utilized_exposure=utilized,
                interest_rate=rate,
                interest_rate_floor=floor,
                origination_date=originated,
                maturity_date=matures,
                h1_code=parse_h1_code(raw_code),
            )
        )

    if not facilities:
        raise ValidationFailure(f"{context}: no data rows found below header row {spec.h1_header_row}")
    return facilities, census


def load_merged_bucket_balance(spec: LoansSheetSpec) -> tuple[float, Mapping[str, float]]:
    """Read the Fed Category 9/10/11 balance from the FR Y-9C extract (PID-LOAN-10).

    Those three portfolios carry no H.1 code, so their balance comes from the two
    MDRM line items and they are modelled as ONE merged bucket. Returns the total
    in canonical USD millions plus the per-MDRM parts for the census."""
    workbook = _open(spec.workbook)
    try:
        rows = [list(row) for row in _sheet(workbook, spec.fry9c_sheet, spec.workbook).values]
    finally:
        workbook.close()

    context = f"{spec.workbook.name}:{spec.fry9c_sheet}"
    header = _header_index(rows, spec.fry9c_header_row, context)
    if spec.fry9c_id_column not in header:
        raise ValidationFailure(
            f"{context}: expected {spec.fry9c_id_column!r} on header row {spec.fry9c_header_row}; "
            f"available: {sorted(header)}"
        )
    idx_id = header[spec.fry9c_id_column]
    idx_value = spec.fry9c_value_column_index - 1

    parts: dict[str, float] = {}
    for row in rows[spec.fry9c_header_row:]:
        if idx_id >= len(row):
            continue
        key = row[idx_id]
        if not isinstance(key, str):
            continue
        token = key.strip().upper()
        if token not in MERGED_BUCKET_MDRMS:
            continue
        if idx_value >= len(row):
            raise ValidationFailure(
                f"{context}: {token} has no value in column {spec.fry9c_value_column_index}"
            )
        parts[token] = apply_money_scale(
            spec.fry9c_scale, to_float(row[idx_value], context=f"{context}: {token}"),
            context=f"{context}: {token}",
        )

    missing = [code for code in MERGED_BUCKET_MDRMS if code not in parts]
    if missing:
        raise ValidationFailure(
            f"{context}: MDRM line item(s) {missing} not found under {spec.fry9c_id_column!r}. "
            f"The merged 9/10/11 bucket has no other source, so this is refused rather than "
            f"treated as a zero balance."
        )
    return sum(parts.values()), parts


def load_category_balances(spec: LoansSheetSpec) -> tuple[Mapping[str, float], LoaderCensus]:
    """Read the per-Fed-Category portfolio balance from `M.1 Balance`.

    The sheet carries its own FRB NII model role per row — column A for the
    domestic side, column B for the international one — so the FR Y-9C line to
    Fed Category wiring is in the workbook and nothing has to be supplied.

    Domestic value columns are attributed to column A's role and international
    ones to column B's, which is how a single FR Y-9C line feeds two categories:
    "c. Secured by farmland" sends its domestic balance to Domestic farmland and
    its international balance to International farmland. Retail and Wholesale-CRE
    rows belong to other models and are skipped.

    Cross-check available to the reader: these totals should reproduce the
    `Sch M bal` column on the FRB SCALARS sheet."""
    workbook = _open(spec.workbook)
    try:
        rows = [list(row) for row in _sheet(workbook, spec.m1_sheet, spec.workbook).values]
    finally:
        workbook.close()

    context = f"{spec.workbook.name}:{spec.m1_sheet}"
    census = LoaderCensus()
    totals: dict[int, float] = {}
    skipped = 0

    sides = (
        (spec.m1_domestic_role_column_index - 1, spec.m1_domestic_value_column_indices),
        (spec.m1_international_role_column_index - 1, spec.m1_international_value_column_indices),
    )

    for offset, row in enumerate(rows[spec.m1_first_data_row - 1:], start=spec.m1_first_data_row):
        for role_index, value_indices in sides:
            if role_index >= len(row) or _is_missing(row[role_index]):
                continue
            category = m1_role_category(row[role_index])
            if category is None:
                skipped += 1
                continue
            for value_index in value_indices:
                cell = row[value_index - 1] if value_index - 1 < len(row) else None
                if _is_missing(cell):
                    continue
                where = f"{context} row {offset} col {value_index}"
                totals[category] = totals.get(category, 0.0) + apply_money_scale(
                    spec.m1_scale, to_float(cell, context=where), context=where
                )

    if not totals:
        raise ValidationFailure(
            f"{context}: no 'Wholesale - Corp' roles found from row {spec.m1_first_data_row}. "
            f"Check m1_first_data_row and the role column indices before trusting a zero balance."
        )

    missing = sorted(set(FED_CATEGORY_NAMES) - set(totals))
    if missing:
        census.warnings.append(
            f"M.1 supplied no balance for Fed Category {missing} "
            f"({[FED_CATEGORY_NAMES[c] for c in missing]}) — those categories project zero income"
        )
    census.rows_read = len(totals)
    census.warnings.append(f"skipped {skipped} non-Corporate role cells (Retail and Wholesale-CRE)")
    return MappingProxyType({FED_CATEGORY_NAMES[c]: v for c, v in totals.items()}), census


def load_3m_treasury(
    spec: LoansSheetSpec, scenario: str, quarters: Sequence[int], launch_point: str
) -> tuple[Mapping[str, float], Mapping[int, float], float]:
    """Read the 3-month Treasury history and projection from `MEV`.

    History rows carry the scenario name `Actual` and are keyed by calendar
    quarter for the median-origination lookup; projection rows carry `scenario`
    and are mapped onto PQ1..PQn in sheet order. Also returns the launch-point
    value, read from the history at `launch_point` (e.g. `2024Q4`)."""
    workbook = _open(spec.workbook)
    try:
        rows = [list(row) for row in _sheet(workbook, spec.mev_sheet, spec.workbook).values]
    finally:
        workbook.close()

    context = f"{spec.workbook.name}:{spec.mev_sheet}"
    header = _header_index(rows, spec.mev_header_row, context)
    idx_scenario = _column(header, spec.mev_scenario_column, context)
    idx_date = _column(header, spec.mev_date_column, context)
    idx_rate = _column(header, spec.mev_3m_column, context)

    launch_label = check_quarter_label(f"{context}: launch point", launch_point)
    launch_year, launch_quarter = int(launch_label[:4]), int(launch_label[5])

    def quarters_since_launch(label: str) -> int:
        return (int(label[:4]) - launch_year) * 4 + int(label[5]) - launch_quarter

    history: dict[str, float] = {}
    projection: dict[int, float] = {}
    seen_scenario_labels: set[str] = set()
    for row in rows[spec.mev_header_row:]:
        if max(idx_scenario, idx_date, idx_rate) >= len(row):
            continue
        name, raw_date, raw_rate = row[idx_scenario], row[idx_date], row[idx_rate]
        if _is_missing(name) or _is_missing(raw_date) or _is_missing(raw_rate):
            continue
        rate = apply_rate_scale(
            spec.mev_rate_scale, to_float(raw_rate, context=f"{context}: 3M"), context=f"{context}: 3M"
        )
        label = check_quarter_label(
            f"{context}: date", str(raw_date).strip().replace(" ", "").upper()
        )
        if str(name).strip() == spec.mev_history_scenario:
            # A duplicated history quarter with a DIFFERENT value is the silent-bug
            # case: dict assignment would keep whichever came last with no trace.
            if label in history and history[label] != rate:
                raise ValidationFailure(
                    f"{context}: {spec.mev_history_scenario!r} carries {label} twice with "
                    f"different values ({history[label]!r} vs {rate!r})"
                )
            history[label] = rate
        elif str(name).strip() == scenario:
            # Projection rows are mapped to PQ indices BY THEIR DATE, never by
            # sheet order: the sheet says which quarter each row is, so use it.
            # Rows outside PQ1..PQn (a 13-quarter supervisory path has a tail we
            # do not need) are simply out of horizon, not errors.
            if label in seen_scenario_labels:
                raise ValidationFailure(f"{context}: scenario {scenario!r} carries {label} twice")
            seen_scenario_labels.add(label)
            index = quarters_since_launch(label)
            if index in quarters:
                projection[index] = rate

    if not history:
        raise ValidationFailure(
            f"{context}: no rows under scenario {spec.mev_history_scenario!r} — the fixed-rate "
            f"spread needs the 3M history back to the earliest median origination quarter"
        )
    missing = [q for q in quarters if q not in projection]
    if missing:
        expected = [
            f"PQ{q} ({launch_year + (launch_quarter + q - 1) // 4}"
            f"Q{(launch_quarter + q - 1) % 4 + 1})"
            for q in missing
        ]
        available = sorted(seen_scenario_labels) or ["<none>"]
        raise ValidationFailure(
            f"{context}: scenario {scenario!r} is missing {', '.join(expected)} relative to "
            f"launch point {launch_label}; scenario rows found: {', '.join(available)}. "
            f"Check the --scenario spelling against the sheet and the launch point."
        )
    if launch_point not in history:
        raise ValidationFailure(
            f"{context}: launch point {launch_point!r} is absent from the {spec.mev_history_scenario!r} "
            f"history — the floating spread is measured against it"
        )

    return history, projection, history[launch_point]

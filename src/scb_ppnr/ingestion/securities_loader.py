"""Securities workbook loader (PID-SEC-6): the native multi-sheet workbook →
canonical `SecurityPosition`s grouped by model.

Contract: `specifications/interest-income/securities/securities-input-contract.md`.
Positions sheet is located by its MDRM header row (the row containing CQSCP084);
enrichment tabs are merged by CUSIP/ISIN; the prepayment pivot (PID-MBS-1) is
located by its "Row Labels" header with month-offset columns 0,3,…,27 ≙ PQ0..PQ9
(Grand Total ignored). Three date encodings are normalized here (yyyymmdd
integers; Excel serials; mm/dd/yyyy strings); scales are declared, never guessed
(D-006). Policy: unmapped categories and unmatched enrichment are hard errors
(PID-SEC-5 — surface and ask); equity-intent and out-of-scope positions are
excluded with a count; non-positive WAL rows are skipped with a highlighted
warning (user-parked 2026-07-24); PID-SEC-3 proxies amortized cost from
price/100 × current face when maturity/book-yield/AC are missing or zero."""

from __future__ import annotations

import datetime as _dt
import math
from pathlib import Path

from ..core.schemas import PROJECTION_QUARTERS, ValidationFailure
from ..interest_income.securities_schemas import (
    MODEL_MBS,
    MODEL_OTHER_SEC,
    MODEL_UST,
    OUT_OF_SCOPE,
    RATE_FIXED,
    RATE_FLOATING,
    RATE_ZERO_COUPON,
    SecuritiesInputs,
    SecurityPosition,
    assign_model,
)
from .config import IngestionConfig, SecuritiesConfig, SecuritiesEnrichmentSheet
from .normalize import apply_money_scale, apply_rate_scale, to_float

_EXCEL_EPOCH = _dt.date(1899, 12, 30)
_DAYS_PER_QUARTER = 91.3125          # 365.25 / 4 — quarters rounded up ([CODE], logged in contract §6)

# Positions-sheet columns located via the MDRM header row (contract §2).
_POSITIONS_MDRM = {
    "D_DT": "report_date",
    "CQSCP083": "identifier_value",
    "CQSCP084": "security_description_1",
    "CQSCP087": "amortized_cost",
    "CQSCP089": "current_face_value",
    "CQSCP090": "original_face_value",
    "CQSCP092": "accounting_intent",
    "CQSCP094": "book_yield",
    "CQSCJH21": "price",
}
_REQUIRED_MDRM = ("CQSCP083", "CQSCP084", "CQSCP087", "CQSCP089", "CQSCP092")

_RATE_TYPE_MAP = {
    "FIXED": RATE_FIXED,
    "FLOATING": RATE_FLOATING,
    "FLOAT": RATE_FLOATING,
    "ZERO COUPON": RATE_ZERO_COUPON,
    "ZERO_COUPON": RATE_ZERO_COUPON,
    "ZERO-COUPON": RATE_ZERO_COUPON,
}

_MISSING_STRINGS = {"", "(BLANK)", "N/A", "NA", "-"}


def _load_workbook(path: Path):
    try:
        import openpyxl
    except ImportError:
        raise ValidationFailure(
            f"{path}: reading the securities workbook requires the optional 'openpyxl' "
            f"dependency (pip install openpyxl, or install with the [excel] extra)"
        ) from None
    if not path.exists():
        raise ValidationFailure(f"securities workbook not found: {path}")
    return openpyxl.load_workbook(path, read_only=True, data_only=True)


def _sheet(workbook, name: str, path: Path):
    if name not in workbook.sheetnames:
        raise ValidationFailure(f"{path}: sheet {name!r} not found; available: {workbook.sheetnames}")
    return workbook[name]


def _blank(value: object) -> bool:
    return value is None or (isinstance(value, str) and value.strip().upper() in _MISSING_STRINGS)


def _parse_date(value: object, *, context: str) -> _dt.date:
    """Normalize the contract's three date encodings (§6)."""
    if isinstance(value, _dt.datetime):
        return value.date()
    if isinstance(value, _dt.date):
        return value
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        number = float(value)
        if 10_000_000.0 <= number <= 99_991_231.0:       # yyyymmdd integer
            text = str(int(number))
            return _dt.date(int(text[:4]), int(text[4:6]), int(text[6:8]))
        if 0.0 < number < 200_000.0:                      # Excel serial
            return _EXCEL_EPOCH + _dt.timedelta(days=int(round(number)))
    if isinstance(value, str):
        text = value.strip()
        for fmt in ("%m/%d/%Y", "%Y-%m-%d"):
            try:
                return _dt.datetime.strptime(text, fmt).date()
            except ValueError:
                continue
        try:
            return _parse_date(float(text.replace(",", "")), context=context)
        except (ValueError, ValidationFailure):
            pass
    raise ValidationFailure(f"{context}: cannot interpret {value!r} as a date (yyyymmdd, Excel serial, or mm/dd/yyyy)")


def _positions_rows(worksheet, path: Path) -> tuple[list[dict[str, object]], dict[str, int]]:
    rows = list(worksheet.iter_rows(values_only=True))
    header_index: int | None = None
    columns: dict[str, int] = {}
    for index, row in enumerate(rows):
        cells = {str(c).strip(): i for i, c in enumerate(row) if c is not None and str(c).strip()}
        if "CQSCP084" in cells:
            header_index = index
            for mdrm, field in _POSITIONS_MDRM.items():
                if mdrm in cells:
                    columns[field] = cells[mdrm]
            break
    if header_index is None:
        raise ValidationFailure(f"{path}: positions sheet has no MDRM header row (looked for CQSCP084)")
    missing = [m for m in _REQUIRED_MDRM if _POSITIONS_MDRM[m] not in columns]
    if missing:
        raise ValidationFailure(f"{path}: positions MDRM header lacks required columns {missing}")

    parsed: list[dict[str, object]] = []
    for row in rows[header_index + 1:]:
        record = {field: (row[i] if i < len(row) else None) for field, i in columns.items()}
        if _blank(record.get("identifier_value")):
            continue
        parsed.append(record)
    return parsed, columns


def _enrichment_map(workbook, spec: SecuritiesEnrichmentSheet, path: Path) -> dict[str, dict[str, object]]:
    worksheet = _sheet(workbook, spec.sheet, path)
    rows = list(worksheet.iter_rows(values_only=True))
    if len(rows) < spec.header_row:
        raise ValidationFailure(f"{path}:{spec.sheet}: header_row {spec.header_row} beyond sheet end")
    header = {str(c).strip(): i for i, c in enumerate(rows[spec.header_row - 1]) if c is not None and str(c).strip()}
    needed = {"key": spec.key_column, "maturity": spec.maturity_column, "coupon": spec.coupon_column,
              "rate_type": spec.rate_type_column, "wal": spec.wal_column}
    if spec.floor_column is not None:
        needed["floor"] = spec.floor_column
    columns: dict[str, int] = {}
    for role, name in needed.items():
        if name not in header:
            raise ValidationFailure(
                f"{path}:{spec.sheet}: column {name!r} ({role}) not found in header row "
                f"{spec.header_row}; available: {sorted(header)}"
            )
        columns[role] = header[name]

    result: dict[str, dict[str, object]] = {}
    for row in rows[spec.header_row:]:
        key_raw = row[columns["key"]] if columns["key"] < len(row) else None
        if _blank(key_raw):
            continue
        key = str(key_raw).strip()
        result[key] = {role: (row[i] if i < len(row) else None) for role, i in columns.items()}
    return result


def _prepayment_map(worksheet, path: Path, money_scale: str) -> dict[str, dict[int, float]]:
    rows = list(worksheet.iter_rows(values_only=True))
    header_index = None
    for index, row in enumerate(rows):
        first = row[0] if row else None
        if isinstance(first, str) and first.strip().lower() == "row labels":
            header_index = index
            break
    if header_index is None:
        raise ValidationFailure(f"{path}: prepayment sheet has no 'Row Labels' header row (pivot layout, contract §4)")
    month_columns: dict[int, int] = {}
    for i, cell in enumerate(rows[header_index][1:], start=1):
        if cell is None or (isinstance(cell, str) and not cell.strip().lstrip("-").isdigit()):
            continue
        months = int(float(cell)) if not isinstance(cell, int) else cell
        if months % 3 == 0 and 0 <= months <= 27:
            month_columns[months // 3] = i
    missing_quarters = [q for q in (0, *PROJECTION_QUARTERS) if q not in month_columns]
    if missing_quarters:
        raise ValidationFailure(
            f"{path}: prepayment header lacks month-offset columns for PQ{missing_quarters} "
            f"(expected 0,3,…,27)"
        )

    faces: dict[str, dict[int, float]] = {}
    for line, row in enumerate(rows[header_index + 1:], start=header_index + 2):
        label = row[0] if row else None
        if _blank(label) or str(label).strip().lower() == "grand total":
            continue
        cusip = str(label).strip()
        path_values: dict[int, float] = {}
        for quarter, column in month_columns.items():
            raw = row[column] if column < len(row) else None
            if _blank(raw):
                raise ValidationFailure(f"{path}: prepayment row {line} ({cusip}): PQ{quarter} cell is blank")
            value = to_float(raw, context=f"{path} prepayment {cusip} PQ{quarter}")
            path_values[quarter] = apply_money_scale(money_scale, value, context=f"{path} prepayment {cusip} PQ{quarter}")
        faces[cusip] = path_values
    return faces


def load_securities_inputs(config: IngestionConfig) -> SecuritiesInputs:
    if config.firm_data is None or config.firm_data.securities is None:
        raise ValidationFailure("config has no [firm_data.securities] section (PID-SEC-6)")
    sc: SecuritiesConfig = config.firm_data.securities
    path = config.resolve(sc.workbook)
    workbook = _load_workbook(path)
    try:
        records, _ = _positions_rows(_sheet(workbook, sc.positions_sheet, path), path)
        if not records:
            raise ValidationFailure(f"{path}: positions sheet has no data rows")
        enrichment: dict[str, dict[str, object]] = {}
        for spec in sc.enrichment:
            for key, fields in _enrichment_map(workbook, spec, path).items():
                enrichment.setdefault(key, fields)      # first tab wins on duplicates
        prepayment: dict[str, dict[int, float]] = {}
        if sc.prepayment_sheet is not None:
            prepayment = _prepayment_map(_sheet(workbook, sc.prepayment_sheet, path), path, sc.money_scale)
    finally:
        workbook.close()

    report_date = _parse_date(records[0]["report_date"], context=f"{path} D_DT") if "report_date" in records[0] and not _blank(records[0].get("report_date")) else None

    warnings: list[str] = []
    skipped_out_of_scope = 0
    skipped_wal = 0
    unmatched: list[str] = []
    grouped: dict[str, list[SecurityPosition]] = {MODEL_UST: [], MODEL_MBS: [], MODEL_OTHER_SEC: []}

    for record in records:
        security_id = str(record["identifier_value"]).strip()
        context = f"{path} security {security_id}"
        intent = "" if _blank(record.get("accounting_intent")) else str(record["accounting_intent"]).strip()
        category = str(record["security_description_1"]).strip() if not _blank(record.get("security_description_1")) else ""
        if not category:
            raise ValidationFailure(f"{context}: security_description_1 is blank")
        model, agency_prepay = assign_model(category)
        if model == OUT_OF_SCOPE or intent.upper() == "EQ":
            skipped_out_of_scope += 1
            continue

        fields = enrichment.get(security_id)
        if fields is None:
            unmatched.append(security_id)
            continue

        rate_type_raw = "" if _blank(fields.get("rate_type")) else str(fields["rate_type"]).strip().upper()
        if rate_type_raw not in _RATE_TYPE_MAP:
            raise ValidationFailure(f"{context}: unknown rate type {fields.get('rate_type')!r} (known: {sorted(_RATE_TYPE_MAP)})")
        rate_type = _RATE_TYPE_MAP[rate_type_raw]

        coupon = None
        if not _blank(fields.get("coupon")):
            coupon = apply_rate_scale(sc.coupon_scale, to_float(fields["coupon"], context=f"{context} coupon"), context=f"{context} coupon")
        if rate_type == RATE_ZERO_COUPON:
            coupon = None                                   # zero-coupon: cash coupon is identically zero
        floor = None
        if "floor" in (fields or {}) and not _blank(fields.get("floor")):
            floor = apply_rate_scale(sc.coupon_scale, to_float(fields["floor"], context=f"{context} floor"), context=f"{context} floor")

        wal = None
        if not _blank(fields.get("wal")):
            wal = to_float(fields["wal"], context=f"{context} wal")
            if wal <= 0.0:
                skipped_wal += 1
                warnings.append(
                    f"HIGHLIGHT {security_id}: non-positive WAL {wal} — row skipped "
                    f"(user-parked 2026-07-24; treatment to be decided)"
                )
                continue

        maturity_quarters = None
        if not _blank(fields.get("maturity")) and report_date is not None:
            maturity_date = _parse_date(fields["maturity"], context=f"{context} maturity")
            days = (maturity_date - report_date).days
            if days <= 0:
                warnings.append(f"{security_id}: maturity {maturity_date} not after the report date {report_date} — treated as missing (PID-SEC-3 may proxy)")
            else:
                maturity_quarters = max(1, math.ceil(days / _DAYS_PER_QUARTER))

        face = apply_money_scale(sc.money_scale, to_float(record["current_face_value"], context=f"{context} current_face"), context=f"{context} current_face")
        ac_raw = None if _blank(record.get("amortized_cost")) else to_float(record["amortized_cost"], context=f"{context} amortized_cost")
        amortized_cost = None if ac_raw is None else apply_money_scale(sc.money_scale, ac_raw, context=f"{context} amortized_cost")
        book_yield = None
        if not _blank(record.get("book_yield")):
            by = to_float(record["book_yield"], context=f"{context} book_yield")
            book_yield = apply_rate_scale(sc.book_yield_scale, by, context=f"{context} book_yield") if by != 0.0 else 0.0

        # PID-SEC-3: unsettled-transaction AC proxy.
        ac_proxied = False
        trigger = maturity_quarters is None or book_yield in (None, 0.0) or amortized_cost in (None, 0.0)
        if trigger and amortized_cost in (None, 0.0):
            if _blank(record.get("price")):
                raise ValidationFailure(
                    f"{context}: PID-SEC-3 trigger (maturity/book yield/amortized cost missing or zero) "
                    f"but no price to proxy from — surfaced, never defaulted"
                )
            price = to_float(record["price"], context=f"{context} price")
            amortized_cost = price / 100.0 * face          # per-100 price × notional (current face, TBC)
            ac_proxied = True
            warnings.append(f"{security_id}: PID-SEC-3 amortized-cost proxy applied (price/100 × current face); accretion held at 0")
        if book_yield == 0.0:
            book_yield = None

        face_path = None
        if agency_prepay and security_id in prepayment:
            face_path = prepayment.pop(security_id)
        elif agency_prepay:
            warnings.append(f"{security_id}: Agency MBS absent from the prepayment sheet — no prepayment, face held flat (multi-family, PID-SEC-5)")

        grouped[model].append(
            SecurityPosition(
                security_id=security_id,
                model=model,
                category=category,
                rate_type=rate_type,
                accounting_intent=intent or "AFS",
                current_face=face,
                amortized_cost=amortized_cost if amortized_cost is not None else 0.0,
                coupon_rate=coupon,
                book_yield=book_yield,
                coupon_floor=floor,
                maturity_quarters=maturity_quarters,
                wal_years=wal,
                face_path=face_path,
                ac_proxied=ac_proxied,
            )
        )

    if unmatched:
        raise ValidationFailure(
            f"{path}: {len(unmatched)} position(s) have no enrichment match (maturity/coupon/rate-type "
            f"unavailable) — surfaced for clarification, never defaulted: {sorted(unmatched)[:20]}"
        )
    for leftover in sorted(prepayment):
        warnings.append(f"prepayment sheet row {leftover} matches no in-scope Agency MBS position (ignored, logged)")
    if skipped_out_of_scope:
        warnings.append(f"{skipped_out_of_scope} equity-intent/out-of-scope position(s) excluded (PID-SEC-5)")
    if skipped_wal:
        warnings.append(f"{skipped_wal} position(s) skipped for non-positive WAL — HIGHLIGHTED for later decision")

    return SecuritiesInputs(
        firm_id=config.firm_data.firm_id,
        ust=tuple(grouped[MODEL_UST]),
        mbs=tuple(grouped[MODEL_MBS]),
        other_sec=tuple(grouped[MODEL_OTHER_SEC]),
        warnings=tuple(warnings),
    )

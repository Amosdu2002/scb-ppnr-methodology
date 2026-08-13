"""Workbook binding for the Retail loan families (PID-LOAN-26..34).

Reads the retail input surfaces the user supplied 2026-08-12/13 and produces
canonical objects for `interest_income.loans_retail`:

- the M.1 Balances retail rows, matched by their FR Y-14Q M.1 line labels and
  cross-checked against the sheet's own "FRB NII model" role labels
  (PID-LOAN-26: values through column M only; the role labels per side are the
  wiring — domestic roles feed the four domestic families, every international
  side is noncore)
- the "Mortgage query" 12-segment launch table + per-segment maturing-balance
  schedules (PID-LOAN-27; the FIRST launch/schedule block pair is the
  production MORT variant, PID-LOAN-33)
- the "Card query" four-row segment table (PID-LOAN-28)
- the "Auto 4Q24 pivot" summary block, possibly in a SEPARATE workbook
  (PID-LOAN-29: columns M/N/O = outstanding / average rate / new-origination
  rate; the re-origination weights sit in columns P..X, rows 2/3 = New/Used)
- the other-consumer product block on the workbook's own construction sheet
  (PID-LOAN-30: A.7/A.9 sub-product balances give SHARES; rates come from the
  PPNR line-item projections sheet's PQ0 average-rate column)
- the Prime and Mortgage-rate MEV series (PID-LOAN-31: "MEV Data" columns
  "Prime rate" / "Mortgage rate", percent)

Sheet names, workbook paths, column anchors and scales are configuration; only
the logical contract is committed here. Institution-referencing sheet names
(the line-item results sheet) stay in the gitignored local config. No firm
values appear in this module or its tests' committed fixtures."""

from __future__ import annotations

import datetime as _dt
import re
from dataclasses import dataclass, field
from pathlib import Path
from types import MappingProxyType
from typing import Mapping, Sequence

from ..core.schemas import ValidationFailure
from ..interest_income.loans_schemas import check_quarter_label
from .loans_loader import (
    LoansSheetSpec,
    _column,
    _header_index,
    _is_missing,
    _load_rows,
)
from .normalize import apply_money_scale, apply_rate_scale, to_float

# The query sheets print a literal "x" where a window holds no observation
# (PID-LOAN-27). This is a RETAIL token only — "X" is not added to the shared
# missing-token set, because a lone X elsewhere could be a legitimate value.
_RETAIL_MISSING_EXTRA = {"X"}


def _retail_missing(value: object) -> bool:
    if _is_missing(value):
        return True
    return isinstance(value, str) and value.strip().upper() in _RETAIL_MISSING_EXTRA


def _resolve_workbook(spec: LoansSheetSpec, override: str | None) -> Path:
    """Resolve a retail sheet's workbook (PID-LOAN-31, user-stated topology):

        per-sheet override  ->  retail_workbook  ->  the main (wholesale) workbook

    The retail inputs live in their own file, distinct from the wholesale
    workbook; the auto pivot sits in a third. A relative path resolves against
    the MAIN workbook's directory, so the company config can keep its files
    side by side."""
    chosen = override if override is not None else spec.retail_workbook
    if chosen is None:
        return spec.workbook
    path = Path(chosen)
    if not path.is_absolute():
        path = spec.workbook.parent / path
    return path


# --- census -----------------------------------------------------------------


@dataclass
class RetailCensus:
    """What the retail load found, reported rather than assumed."""

    title: str = "RETAIL LOADER CENSUS"
    counters: dict[str, int] = field(default_factory=dict)
    notes: list[str] = field(default_factory=list)

    def bump(self, name: str, by: int = 1) -> None:
        self.counters[name] = self.counters.get(name, 0) + by

    def render(self) -> str:
        lines = [self.title]
        for name, count in sorted(self.counters.items()):
            lines.append(f"  {name:<34}: {count}")
        for note in self.notes:
            lines.append(f"  NOTE: {note}")
        return "\n".join(lines)


# --- M.1 retail rows (PID-LOAN-26) -----------------------------------------

# Matched against the M.1 line labels (column C), normalized: lowercased,
# enumeration prefixes and trailing dot leaders stripped. The labels are the
# FR Y-14Q Schedule M.1 line names, which are schedule-standard — unlike row
# numbers, they survive a re-export that inserts a row.
M1_RETAIL_LABELS: Mapping[str, str] = MappingProxyType({
    "first_mortgages": "first mortgages",
    "first_lien_heloans": "first lien heloan",
    "junior_lien_heloans": "junior lien heloan",
    "helocs": "helocs",
    "small_business": "small business",
    "sme_cards": "sme cards and corporate cards",
    "bank_cards": "bank cards",
    "charge_cards": "charge cards",
    "auto_loans": "auto loans",
    "student_loans": "student loans",
    "non_purpose_lending": "non-purpose lending",
    "other_consumer_loans": "other consumer loans",
})

# Expected dom-side role prefixes per label — a mismatch WARNS, never blocks:
# the role labels are the wiring authority, so disagreement means the label
# match or the sheet changed and a person should look (PID-LOAN-26).
_EXPECTED_DOM_ROLE: Mapping[str, str] = MappingProxyType({
    "first_mortgages": "retail - mortgage - first lien",
    "first_lien_heloans": "retail - mortgage - home equity",
    "junior_lien_heloans": "retail - mortgage - home equity",
    "helocs": "retail - mortgage - heloc",
    "small_business": "retail - noncore",
    "sme_cards": "retail - sm credit card",
    "bank_cards": "retail - consumer credit card",
    "charge_cards": "retail - consumer credit card",
    "auto_loans": "retail - auto",
    "student_loans": "retail - noncore",
    "non_purpose_lending": "retail - noncore",
    "other_consumer_loans": "retail - noncore",
})


def _normalize_m1_label(value: object) -> str:
    text = str(value).strip().lower()
    text = re.sub(r"^[0-9a-z]{0,3}[.)]\s*", "", text)      # "a. " / "(b) " / "1. "
    text = re.sub(r"^\([0-9a-z]{1,3}\)\s*", "", text)
    return text.rstrip(". ").strip()


@dataclass(frozen=True)
class M1RetailRow:
    """One M.1 retail line: the four value cells plus the two role labels.

    Values are canonical USD millions. Blank cells are genuine zeros here — an
    empty side (the workbook's charge-card row, the auto HFS cell) is a real
    zero balance, not a refusal."""

    label_key: str
    sheet_row: int
    dom_hfi: float
    dom_hfs: float
    int_hfi: float
    int_hfs: float
    dom_role: str | None
    int_role: str | None

    @property
    def dom(self) -> float:
        return self.dom_hfi + self.dom_hfs

    @property
    def intl(self) -> float:
        return self.int_hfi + self.int_hfs

    @property
    def total(self) -> float:
        return self.dom + self.intl


def load_retail_m1(spec: LoansSheetSpec) -> tuple[Mapping[str, M1RetailRow], RetailCensus]:
    """Read the twelve retail M.1 rows by line label (PID-LOAN-26).

    Every pattern must match exactly one row; zero or several is refused —
    a silently missing balance row would understate a family multiplicand.

    Reads the RETAIL workbook's own M.1 sheet (`retail_m1_sheet`) — the retail
    inputs live in a different file from the wholesale workbook."""
    workbook = _resolve_workbook(spec, None)
    rows, quieted = _load_rows(workbook, spec.retail_m1_sheet)
    context = f"{workbook.name}:{spec.retail_m1_sheet}"
    census = RetailCensus(title="RETAIL M.1 CENSUS")
    if quieted:
        census.notes.append(
            f"{quieted} openpyxl cell warning(s) quieted while reading {spec.retail_m1_sheet!r}"
        )

    label_index = spec.m1_label_column_index - 1
    dom_role_index = spec.m1_domestic_role_column_index - 1
    int_role_index = spec.m1_international_role_column_index - 1
    dom_hfi_col, dom_hfs_col = spec.m1_domestic_value_column_indices
    intl_hfi_col, intl_hfs_col = spec.m1_international_value_column_indices

    def amount(row: Sequence[object], column_index: int, where: str) -> float:
        cell = row[column_index - 1] if column_index - 1 < len(row) else None
        if _is_missing(cell):
            return 0.0
        return apply_money_scale(spec.m1_scale, to_float(cell, context=where), context=where)

    matches: dict[str, list[tuple[int, Sequence[object]]]] = {key: [] for key in M1_RETAIL_LABELS}
    for offset, row in enumerate(rows[spec.m1_first_data_row - 1:], start=spec.m1_first_data_row):
        if label_index >= len(row) or _is_missing(row[label_index]):
            continue
        normalized = _normalize_m1_label(row[label_index])
        for key, pattern in M1_RETAIL_LABELS.items():
            if pattern in normalized:
                matches[key].append((offset, row))

    result: dict[str, M1RetailRow] = {}
    for key, hits in matches.items():
        if len(hits) != 1:
            raise ValidationFailure(
                f"{context}: M.1 line label pattern {M1_RETAIL_LABELS[key]!r} matched "
                f"{len(hits)} row(s) ({[r for r, _ in hits]}) — each retail line must match "
                f"exactly once (check m1_label_column_index / m1_first_data_row)"
            )
        sheet_row, row = hits[0]
        where = f"{context} row {sheet_row}"
        dom_role = None if dom_role_index >= len(row) or _is_missing(row[dom_role_index]) else str(row[dom_role_index]).strip()
        int_role = None if int_role_index >= len(row) or _is_missing(row[int_role_index]) else str(row[int_role_index]).strip()
        record = M1RetailRow(
            label_key=key,
            sheet_row=sheet_row,
            dom_hfi=amount(row, dom_hfi_col, f"{where} dom HFI"),
            dom_hfs=amount(row, dom_hfs_col, f"{where} dom HFS/FVO"),
            int_hfi=amount(row, intl_hfi_col, f"{where} int HFI"),
            int_hfs=amount(row, intl_hfs_col, f"{where} int HFS/FVO"),
            dom_role=dom_role,
            int_role=int_role,
        )
        result[key] = record
        census.bump("rows matched")
        expected = _EXPECTED_DOM_ROLE[key]
        if dom_role is not None and not dom_role.strip().lower().startswith(expected):
            census.notes.append(
                f"WARN: M.1 row {sheet_row} ({key}) domestic role {dom_role!r} does not look like "
                f"{expected!r} — the role labels are the wiring authority (PID-LOAN-26); "
                f"check the label match before trusting this row's family assignment"
            )
        # Every retail row's international side is noncore (PID-LOAN-26) with one
        # observed exception: the SME-cards row carries its own role on BOTH sides.
        expected_int = "retail - sm credit card" if key == "sme_cards" else "retail - noncore"
        if int_role is not None and not int_role.strip().lower().startswith(expected_int):
            census.notes.append(
                f"WARN: M.1 row {sheet_row} ({key}) international role {int_role!r} does not "
                f"look like {expected_int!r} (PID-LOAN-26); check the sheet"
            )
    return MappingProxyType(result), census


# --- Mortgage query (PID-LOAN-27) ------------------------------------------

PRODUCT_FIRST_LIEN = "first_lien"
PRODUCT_HOME_EQUITY = "home_equity"
PRODUCT_HELOC = "heloc"
MORTGAGE_PRODUCTS = (PRODUCT_FIRST_LIEN, PRODUCT_HOME_EQUITY, PRODUCT_HELOC)

_LIEN_BY_TOKEN = {
    "first lien": PRODUCT_FIRST_LIEN,
    "home equity": PRODUCT_HOME_EQUITY,
    "heloc": PRODUCT_HELOC,
}
_SIDE_BY_TOKEN = {"hfi": "HFI", "hfs/fvo": "FVO_HFS", "fvo/hfs": "FVO_HFS"}
_RATE_TYPE_BY_TOKEN = {"fixed": "fixed", "variable": "variable"}

_AFTER_PREFIX = "WEIGHTED_AVERAGE_RATE_AFTER_"


@dataclass(frozen=True)
class MortgageSegment:
    """One launch-table row of the production (first) block."""

    product: str
    side: str                      # "HFI" | "FVO_HFS"
    rate_type: str                 # "fixed" | "variable"
    upb: float                     # canonical USD millions
    rate: float                    # WEIGHTED_AVERAGE_RATE, decimal
    new_origination_rate: float | None    # the ACTIVE window's value; None = "x"
    new_origination_fallback: bool        # True when the rate above fell back to `rate`
    arm_floor: float | None


@dataclass(frozen=True)
class MortgageQuery:
    segments: Mapping[tuple[str, str, str], MortgageSegment]
    # (product, side, rate_type) -> {PQ index -> maturing balance, USD millions}
    schedules: Mapping[tuple[str, str, str], Mapping[int, float]]
    window_cutoff: _dt.date
    census: RetailCensus


def _blocks_of(header_row: Sequence[object], anchor: str) -> list[dict[str, int]]:
    """Split a multi-block header row into per-block header->index maps.

    The query sheet lays several tables side by side, each starting with an
    `anchor` column ("Lien Position"); duplicate headers across blocks make a
    flat index ambiguous, so each block is indexed separately."""
    cells = [
        (index, str(cell).strip())
        for index, cell in enumerate(header_row)
        if not _is_missing(cell)
    ]
    starts = [index for index, text in cells if text == anchor]
    blocks: list[dict[str, int]] = []
    for position, start in enumerate(starts):
        end = starts[position + 1] if position + 1 < len(starts) else len(header_row)
        blocks.append({text: index for index, text in cells if start <= index < end})
    return blocks


def load_mortgage_query(spec: LoansSheetSpec) -> MortgageQuery:
    """Read the production launch table and its maturing-balance schedules.

    The sheet carries two classification variants side by side; the FIRST
    launch block and the FIRST schedule block are the MORT variant that drives
    production (PID-LOAN-33) — the alternative blocks are ignored, and that
    choice is printed in the census rather than silently applied."""
    if spec.mortgage_query_sheet is None:
        raise ValidationFailure("mortgage_query_sheet is not configured")
    if spec.mortgage_window not in ("quarter", "month"):
        raise ValidationFailure(
            f"mortgage_window must be 'quarter' or 'month' (PID-LOAN-33), got {spec.mortgage_window!r}"
        )
    workbook = _resolve_workbook(spec, spec.mortgage_query_workbook)
    rows, quieted = _load_rows(workbook, spec.mortgage_query_sheet)
    context = f"{workbook.name}:{spec.mortgage_query_sheet}"
    census = RetailCensus(title="MORTGAGE QUERY CENSUS")
    if quieted:
        census.notes.append(f"{quieted} openpyxl cell warning(s) quieted")
    if not rows:
        raise ValidationFailure(f"{context}: the sheet is empty")

    blocks = _blocks_of(rows[0], "Lien Position")
    launch_blocks = [b for b in blocks if "WEIGHTED_AVERAGE_RATE" in b]
    schedule_blocks = [b for b in blocks if "PQ" in b]
    if not launch_blocks:
        raise ValidationFailure(
            f"{context}: no launch block found (a 'Lien Position' block carrying "
            f"'WEIGHTED_AVERAGE_RATE' on the first row)"
        )
    if not schedule_blocks:
        raise ValidationFailure(
            f"{context}: no schedule block found (a 'Lien Position' block carrying a 'PQ' column)"
        )
    census.notes.append(
        f"{len(launch_blocks)} launch and {len(schedule_blocks)} schedule block(s) on the sheet; "
        f"the FIRST of each drives (the MORT variant, PID-LOAN-33) — the alternative "
        f"classification blocks are not read"
    )
    launch = launch_blocks[0]
    schedule = schedule_blocks[0]

    after_columns: dict[_dt.date, int] = {}
    for text, index in launch.items():
        if text.upper().startswith(_AFTER_PREFIX):
            suffix = text[len(_AFTER_PREFIX):].strip()
            if not re.fullmatch(r"\d{8}", suffix):
                raise ValidationFailure(
                    f"{context}: cannot parse the cutoff date from column {text!r}"
                )
            after_columns[_dt.date(int(suffix[:4]), int(suffix[4:6]), int(suffix[6:8]))] = index
    if len(after_columns) < 1:
        raise ValidationFailure(
            f"{context}: no {_AFTER_PREFIX}<yyyymmdd> column found — the Eq A36 "
            f"new-origination window has no source"
        )
    cutoffs = sorted(after_columns)
    # Two windows: the EARLIER cutoff opens the jump-off-quarter window, the
    # later one the final-month window (PID-LOAN-27). With a single column on
    # the sheet, it serves either setting and the census says so.
    if spec.mortgage_window == "quarter":
        cutoff = cutoffs[0]
    else:
        cutoff = cutoffs[-1]
        if len(cutoffs) == 1:
            census.notes.append(
                "WARN: mortgage_window = 'month' but the sheet carries a single AFTER column — "
                "using it as supplied"
            )
    idx_after = after_columns[cutoff]
    census.notes.append(
        f"new-origination window: '{spec.mortgage_window}' -> originations after {cutoff.isoformat()}"
    )

    def block_cell(row: Sequence[object], block: Mapping[str, int], name: str) -> object:
        index = block.get(name)
        if index is None or index >= len(row):
            return None
        return row[index]

    def parse_token(raw: object, table: Mapping[str, str], what: str, where: str) -> str:
        token = str(raw).strip().lower()
        if token not in table:
            raise ValidationFailure(
                f"{where}: {what} {raw!r} is not one of {sorted(table)} — an unmapped value "
                f"is refused, never defaulted"
            )
        return table[token]

    segments: dict[tuple[str, str, str], MortgageSegment] = {}
    schedules: dict[tuple[str, str, str], dict[int, float]] = {}

    for offset, row in enumerate(rows[1:], start=2):
        where = f"{context} row {offset}"
        raw_lien = block_cell(row, launch, "Lien Position")
        if not _is_missing(raw_lien):
            key = (
                parse_token(raw_lien, _LIEN_BY_TOKEN, "Lien Position", where),
                parse_token(block_cell(row, launch, "Loan Type"), _SIDE_BY_TOKEN, "Loan Type", where),
                parse_token(block_cell(row, launch, "Interest Rate Type"), _RATE_TYPE_BY_TOKEN,
                            "Interest Rate Type", where),
            )
            if key in segments:
                raise ValidationFailure(f"{where}: duplicate launch-table segment {key}")
            upb = apply_money_scale(
                spec.mortgage_upb_scale,
                to_float(block_cell(row, launch, "TOTAL_UPB"), context=f"{where}: TOTAL_UPB"),
                context=f"{where}: TOTAL_UPB",
            )
            rate = apply_rate_scale(
                spec.rate_scale,
                to_float(block_cell(row, launch, "WEIGHTED_AVERAGE_RATE"), context=f"{where}: rate"),
                context=f"{where}: rate",
            )
            raw_after = block_cell(row, launch, next(
                text for text in launch if text.upper().startswith(_AFTER_PREFIX)
                and launch[text] == idx_after
            ))
            fallback = False
            if _retail_missing(raw_after):
                # The hardcoded query prints "x" for an empty window; the adopted
                # working assumption (PID-LOAN-33) is the segment's own current
                # rate — censused per segment, never silent.
                new_origination: float | None = rate if key[2] == "fixed" else None
                fallback = key[2] == "fixed"
                if fallback:
                    census.bump("new-origination fallback (x -> own rate)")
                    census.notes.append(
                        f"{key}: no observation in the window — new-origination rate falls back "
                        f"to the segment's own current rate (PID-LOAN-33 working assumption)"
                    )
            else:
                new_origination = apply_rate_scale(
                    spec.rate_scale,
                    to_float(raw_after, context=f"{where}: new-origination rate"),
                    context=f"{where}: new-origination rate",
                )
            raw_floor = block_cell(row, launch, "WEIGHTED_ARM_FLOOR")
            floor = None
            if not _retail_missing(raw_floor):
                floor = apply_rate_scale(
                    spec.rate_scale,
                    to_float(raw_floor, context=f"{where}: ARM floor"),
                    context=f"{where}: ARM floor",
                )
            segments[key] = MortgageSegment(
                product=key[0], side=key[1], rate_type=key[2],
                upb=upb, rate=rate,
                new_origination_rate=new_origination,
                new_origination_fallback=fallback,
                arm_floor=floor,
            )
            census.bump("launch segments")

        raw_lien = block_cell(row, schedule, "Lien Position")
        if not _is_missing(raw_lien):
            where = f"{context} row {offset} (schedule)"
            key = (
                parse_token(raw_lien, _LIEN_BY_TOKEN, "Lien Position", where),
                parse_token(block_cell(row, schedule, "Loan Type"), _SIDE_BY_TOKEN, "Loan Type", where),
                parse_token(block_cell(row, schedule, "Interest Rate Type"), _RATE_TYPE_BY_TOKEN,
                            "Interest Rate Type", where),
            )
            raw_pq = str(block_cell(row, schedule, "PQ")).strip().upper()
            match = re.fullmatch(r"PQ([1-9])", raw_pq)
            if match is None:
                raise ValidationFailure(f"{where}: PQ label {raw_pq!r} is not PQ1..PQ9")
            quarter = int(match.group(1))
            raw_amount = block_cell(row, schedule, "TOTAL_UPB")
            amount = 0.0 if _retail_missing(raw_amount) else apply_money_scale(
                spec.mortgage_upb_scale,
                to_float(raw_amount, context=f"{where}: maturing UPB"),
                context=f"{where}: maturing UPB",
            )
            per_key = schedules.setdefault(key, {})
            if quarter in per_key:
                raise ValidationFailure(f"{where}: duplicate schedule cell for {key} PQ{quarter}")
            per_key[quarter] = amount
            census.bump("schedule cells")

    if not segments:
        raise ValidationFailure(f"{context}: the launch block yielded no segments")
    return MortgageQuery(
        segments=MappingProxyType(segments),
        schedules=MappingProxyType({k: MappingProxyType(v) for k, v in schedules.items()}),
        window_cutoff=cutoff,
        census=census,
    )


# --- Card query (PID-LOAN-28) ----------------------------------------------

CARD_SEGMENTS: Mapping[int, tuple[str, str]] = MappingProxyType({
    1: ("consumer", "bank"),
    2: ("consumer", "charge"),
    3: ("sme", "bank"),
    4: ("sme", "charge"),
})


@dataclass(frozen=True)
class CardSegment:
    row_id: int
    block: str                     # "consumer" | "sme"
    product: str                   # "bank" | "charge"
    total_outstanding: float       # USD millions
    apr: float                     # decimal
    max_apr: float | None          # carried, never applied (card brief §0.2 (k))
    spread: float                  # reported spread, decimal
    revolver_outstanding: float    # USD millions
    apr_revolver: float
    spread_revolver: float

    @property
    def revolver_share(self) -> float:
        if self.total_outstanding <= 0.0:
            return 0.0
        return self.revolver_outstanding / self.total_outstanding


def load_card_query(spec: LoansSheetSpec) -> tuple[Mapping[int, CardSegment], RetailCensus]:
    if spec.card_query_sheet is None:
        raise ValidationFailure("card_query_sheet is not configured")
    workbook = _resolve_workbook(spec, spec.card_query_workbook)
    rows, quieted = _load_rows(workbook, spec.card_query_sheet)
    context = f"{workbook.name}:{spec.card_query_sheet}"
    census = RetailCensus(title="CARD QUERY CENSUS")
    if quieted:
        census.notes.append(f"{quieted} openpyxl cell warning(s) quieted")
    header = _header_index(rows, 1, context)
    idx = {name: _column(header, name, context) for name in (
        "TOTAL_OS", "WEIGHTED_AVERAGE_APR", "WEIGHTED_SPRD",
        "TOTAL_OTST_REVOLVER", "WEIGHTED_AVERAGE_APR_revolver", "WEIGHTED_SPRD_revolver",
    )}
    idx_max = header.get("WEIGHTED_MAX_APR")

    def number(row: Sequence[object], name: str, where: str, money: bool) -> float:
        cell = row[idx[name]] if idx[name] < len(row) else None
        if _retail_missing(cell):
            return 0.0
        value = to_float(cell, context=f"{where}: {name}")
        if money:
            return apply_money_scale(spec.card_money_scale, value, context=f"{where}: {name}")
        return apply_rate_scale(spec.card_rate_scale, value, context=f"{where}: {name}")

    segments: dict[int, CardSegment] = {}
    for offset, row in enumerate(rows[1:], start=2):
        raw_id = row[0] if row else None
        if _is_missing(raw_id):
            continue
        try:
            row_id = int(str(raw_id).strip())
        except ValueError:
            continue
        if row_id not in CARD_SEGMENTS:
            raise ValidationFailure(
                f"{context} row {offset}: segment id {row_id!r} is not one of "
                f"{sorted(CARD_SEGMENTS)} (PID-LOAN-28) — refused, never guessed"
            )
        if row_id in segments:
            raise ValidationFailure(f"{context} row {offset}: duplicate segment id {row_id}")
        where = f"{context} row {offset}"
        block, product = CARD_SEGMENTS[row_id]
        max_apr = None
        if idx_max is not None and idx_max < len(row) and not _retail_missing(row[idx_max]):
            max_apr = apply_rate_scale(
                spec.card_rate_scale, to_float(row[idx_max], context=f"{where}: WEIGHTED_MAX_APR"),
                context=f"{where}: WEIGHTED_MAX_APR",
            )
        segments[row_id] = CardSegment(
            row_id=row_id, block=block, product=product,
            total_outstanding=number(row, "TOTAL_OS", where, money=True),
            apr=number(row, "WEIGHTED_AVERAGE_APR", where, money=False),
            max_apr=max_apr,
            spread=number(row, "WEIGHTED_SPRD", where, money=False),
            revolver_outstanding=number(row, "TOTAL_OTST_REVOLVER", where, money=True),
            apr_revolver=number(row, "WEIGHTED_AVERAGE_APR_revolver", where, money=False),
            spread_revolver=number(row, "WEIGHTED_SPRD_revolver", where, money=False),
        )
        census.bump("segments read")
        if segments[row_id].total_outstanding == 0.0:
            census.bump("empty sub-segments (vacuous)")
    if not segments:
        raise ValidationFailure(f"{context}: no segment rows found (ids 1..4 in column A)")
    return MappingProxyType(segments), census


# --- Auto pivot (PID-LOAN-29) ----------------------------------------------

_AUTO_LABELS = ("new auto loans", "used auto loans", "auto leases")


@dataclass(frozen=True)
class AutoSummary:
    """The pivot sheet's summary block: rows New / Used (+ a zero leases row)."""

    new_outstanding: float          # USD millions
    used_outstanding: float
    new_rate: float                 # column N, decimal
    used_rate: float
    new_origination_rate_new: float     # column O
    new_origination_rate_used: float
    weights_new: Mapping[int, float]    # columns P..X = PQ1..PQ9 (PID-LOAN-29 as amended)
    weights_used: Mapping[int, float]
    leases_outstanding: float
    census: RetailCensus


def load_auto_pivot(spec: LoansSheetSpec) -> AutoSummary:
    if spec.auto_pivot_sheet is None:
        raise ValidationFailure("auto_pivot_sheet is not configured")
    workbook = _resolve_workbook(spec, spec.auto_pivot_workbook)
    rows, quieted = _load_rows(workbook, spec.auto_pivot_sheet)
    context = f"{workbook.name}:{spec.auto_pivot_sheet}"
    census = RetailCensus(title="AUTO PIVOT CENSUS")
    if quieted:
        census.notes.append(f"{quieted} openpyxl cell warning(s) quieted")

    label_col = spec.auto_summary_label_column - 1
    first_row = spec.auto_summary_first_row

    def row_at(number: int) -> Sequence[object]:
        if number > len(rows):
            raise ValidationFailure(f"{context}: summary row {number} is beyond the end of the sheet")
        return rows[number - 1]

    def label_of(row: Sequence[object], expected: str, number: int) -> None:
        raw = row[label_col] if label_col < len(row) else None
        text = "" if _is_missing(raw) else str(raw).strip().lower()
        if expected not in text:
            raise ValidationFailure(
                f"{context} row {number}: expected the {expected!r} label in column "
                f"{spec.auto_summary_label_column} but found {raw!r} — check "
                f"auto_summary_label_column / auto_summary_first_row (PID-LOAN-29: the summary "
                f"block anchors at the product-type labels)"
            )

    def money(row: Sequence[object], column: int, where: str) -> float:
        cell = row[column] if column < len(row) else None
        if _retail_missing(cell):
            return 0.0
        return apply_money_scale(
            spec.auto_balance_scale, to_float(cell, context=where), context=where
        )

    def rate(row: Sequence[object], column: int, where: str) -> float:
        cell = row[column] if column < len(row) else None
        return apply_rate_scale(spec.rate_scale, to_float(cell, context=where), context=where)

    def weights(row: Sequence[object], where: str) -> Mapping[int, float]:
        # Columns P..X = PQ1..PQ9 (user-stated 2026-08-13): four columns to the
        # right of the label anchor, nine wide.
        start = label_col + 4
        values: dict[int, float] = {}
        for quarter in range(1, 10):
            column = start + quarter - 1
            cell = row[column] if column < len(row) else None
            value = 0.0 if _retail_missing(cell) else apply_rate_scale(
                spec.auto_wt_scale, to_float(cell, context=f"{where} PQ{quarter}"),
                context=f"{where} PQ{quarter}",
            )
            if not 0.0 <= value <= 1.0:
                raise ValidationFailure(
                    f"{where} PQ{quarter}: re-origination weight {value} is outside [0, 1] — "
                    f"check auto_wt_scale (Equation A38 is non-convex beyond 1)"
                )
            values[quarter] = value
        return MappingProxyType(values)

    new_row, used_row = row_at(first_row), row_at(first_row + 1)
    label_of(new_row, _AUTO_LABELS[0], first_row)
    label_of(used_row, _AUTO_LABELS[1], first_row + 1)

    leases_outstanding = 0.0
    if first_row + 2 <= len(rows):
        leases_row = row_at(first_row + 2)
        raw = leases_row[label_col] if label_col < len(leases_row) else None
        if not _is_missing(raw) and _AUTO_LABELS[2] in str(raw).strip().lower():
            leases_outstanding = money(leases_row, label_col + 1, f"{context}: auto leases outstanding")
            if leases_outstanding > 0.0:
                census.notes.append(
                    f"WARN: the Auto leases row carries a nonzero balance "
                    f"({leases_outstanding:,.2f}mm) — lease rows are excluded from every family "
                    f"(PID-LOAN-26 as amended); surface and ask before modeling them"
                )
        census.bump("leases row present")

    summary = AutoSummary(
        new_outstanding=money(new_row, label_col + 1, f"{context}: new outstanding"),
        used_outstanding=money(used_row, label_col + 1, f"{context}: used outstanding"),
        new_rate=rate(new_row, label_col + 2, f"{context}: new average rate"),
        used_rate=rate(used_row, label_col + 2, f"{context}: used average rate"),
        new_origination_rate_new=rate(new_row, label_col + 3, f"{context}: new new-orig rate"),
        new_origination_rate_used=rate(used_row, label_col + 3, f"{context}: used new-orig rate"),
        weights_new=weights(new_row, f"{context}: new wt"),
        weights_used=weights(used_row, f"{context}: used wt"),
        leases_outstanding=leases_outstanding,
        census=census,
    )
    census.bump("summary rows read", 2)
    return summary


# --- Other-consumer product block (PID-LOAN-30) -----------------------------

# The construction sheet's own product-mapping tokens -> line keys.
_OC_LINE_TOKENS: Mapping[str, str] = MappingProxyType({
    "card": "credit_cards",
    "other consumer": "non_purpose",
    "c&i": "ci",
    "auto": "auto",
    "heloc": "helocs",
    "first liens mortgages": "first_lien",
    "first lien mortgages": "first_lien",
    "student": "student",
})

_OC_US_PRODUCTS = ("secured-revolving", "secured-installment",
                   "unsecured-revolving", "unsecured-installment", "overdraft")
_SB_PRODUCTS = ("line of credit", "term loan", "other")


@dataclass(frozen=True)
class OcProductRow:
    name: str
    schedule: str                  # "A.7" | "A.9"
    balance: float                 # the schedule's own balance, USD millions — SHARES only
    line_key: str | None           # None = a zero-rate row (Overdraft)


def load_oc_products(spec: LoansSheetSpec) -> tuple[tuple[OcProductRow, ...], RetailCensus]:
    """Read the A.7 / A.9 sub-product rows off the construction sheet.

    Only the input columns are read (schedule tag, product type, balance, the
    workbook's own line-mapping token); everything downstream is recomputed.
    The balances give SHARES within their M.1 block — the multiplicand stays
    M.1 (PID-LOAN-30)."""
    if spec.oc_sheet is None:
        raise ValidationFailure("oc_sheet is not configured")
    workbook = _resolve_workbook(spec, spec.oc_workbook)
    rows, quieted = _load_rows(workbook, spec.oc_sheet)
    context = f"{workbook.name}:{spec.oc_sheet}"
    census = RetailCensus(title="OTHER-CONSUMER PRODUCT CENSUS")
    if quieted:
        census.notes.append(f"{quieted} openpyxl cell warning(s) quieted")

    idx_sch = spec.oc_schedule_column - 1
    idx_product = spec.oc_product_type_column - 1
    idx_balance = spec.oc_balance_column - 1
    idx_line = spec.oc_line_column - 1

    known = {name: "A.7" for name in _OC_US_PRODUCTS}
    known.update({name: "A.9" for name in _SB_PRODUCTS})

    products: list[OcProductRow] = []
    seen: set[str] = set()
    for offset, row in enumerate(rows, start=1):
        raw_product = row[idx_product] if idx_product < len(row) else None
        if _is_missing(raw_product):
            continue
        name = str(raw_product).strip().lower()
        if name not in known:
            continue
        raw_sch = row[idx_sch] if idx_sch < len(row) else None
        schedule = "" if _is_missing(raw_sch) else str(raw_sch).strip().upper()
        if schedule != known[name]:
            continue    # the same label may appear elsewhere on the sheet; the
                        # schedule tag disambiguates (the "Other" trap)
        if name in seen:
            raise ValidationFailure(
                f"{context} row {offset}: duplicate product row {raw_product!r} under {schedule}"
            )
        seen.add(name)
        where = f"{context} row {offset}"
        raw_balance = row[idx_balance] if idx_balance < len(row) else None
        balance = 0.0 if _retail_missing(raw_balance) else apply_money_scale(
            spec.oc_balance_scale, to_float(raw_balance, context=f"{where}: balance"),
            context=f"{where}: balance",
        )
        raw_line = row[idx_line] if idx_line < len(row) else None
        line_key: str | None
        if name == "overdraft":
            line_key = None     # a zero-rate row by construction (observed)
        else:
            token = "" if _is_missing(raw_line) else str(raw_line).strip().lower()
            if token not in _OC_LINE_TOKENS:
                raise ValidationFailure(
                    f"{where}: line-mapping token {raw_line!r} is not one of "
                    f"{sorted(_OC_LINE_TOKENS)} — the mapping column drives the rate lookup "
                    f"(PID-LOAN-30) and an unmapped token is refused, never defaulted"
                )
            line_key = _OC_LINE_TOKENS[token]
        products.append(OcProductRow(name=name, schedule=schedule, balance=balance, line_key=line_key))
        census.bump(f"{schedule} product rows")

    missing = sorted(set(known) - seen)
    if missing:
        census.notes.append(
            f"product rows not found on the sheet: {missing} — those sub-products contribute "
            f"no share (check oc_* column anchors if this is unexpected)"
        )
    if not products:
        raise ValidationFailure(
            f"{context}: no A.7/A.9 product rows found — check oc_product_type_column / "
            f"oc_schedule_column against the sheet"
        )
    return tuple(products), census


# --- PPNR line-item rates (PID-LOAN-30) ------------------------------------

# Normalized contains-patterns for the Average Rates Earned section. The labels
# are the FR Y-14A PPNR Projections worksheet's line names.
LINE_LABEL_PATTERNS: Mapping[str, str] = MappingProxyType({
    "first_lien": "first lien residential mortgages",
    "helocs": "helocs",
    "ci": "c&i loans",
    "credit_cards": "credit cards",
    "auto": "auto loans",
    "student": "student loans",
    "non_purpose": "non-purpose lending",
})


def load_line_item_rates(spec: LoansSheetSpec) -> tuple[Mapping[str, float], RetailCensus]:
    """Read each mapped line's PQ0 average rate from the line-item sheet.

    The sheet is an FR Y-14A PPNR Projections layout; only the rows between
    "Average Rates Earned" and "Total Interest Income" are searched, so the
    identically-named balance rows can never be picked up. The PQ0 column is
    located from the sheet's own PQ0..PQ9 header row."""
    if spec.line_items_sheet is None:
        raise ValidationFailure("line_items_sheet is not configured")
    workbook = _resolve_workbook(spec, spec.line_items_workbook)
    rows, quieted = _load_rows(workbook, spec.line_items_sheet)
    context = f"{workbook.name}:{spec.line_items_sheet}"
    census = RetailCensus(title="LINE-ITEM RATES CENSUS")
    if quieted:
        census.notes.append(f"{quieted} openpyxl cell warning(s) quieted")

    def row_text(row: Sequence[object]) -> str:
        return " ".join(str(cell).strip() for cell in row if not _is_missing(cell)).lower()

    def column_letter(index: int) -> str:
        letters = ""
        index += 1
        while index:
            index, remainder = divmod(index - 1, 26)
            letters = chr(65 + remainder) + letters
        return letters

    # Every PQ0..PQ9 header row on the sheet — these workbooks stack sections
    # (the MORT precedent), and different sections may lay their columns out
    # differently, so the header is chosen NEAREST the rates section below,
    # never simply the first one on the sheet.
    header_rows: list[tuple[int, int]] = []      # (row index, PQ0 column)
    for index, row in enumerate(rows):
        found = {
            str(cell).strip().upper(): column
            for column, cell in enumerate(row)
            if isinstance(cell, str) and re.fullmatch(r"PQ[0-9]", str(cell).strip())
        }
        if len(found) >= 10:
            header_rows.append((index, found["PQ0"]))
    if not header_rows:
        raise ValidationFailure(f"{context}: no PQ0..PQ9 header row found anywhere on the sheet")

    # The requested "Average Rates Earned" occurrence (line_items_section,
    # 1-based), ended by the next "Total Interest Income" AFTER it.
    titles = [index for index, row in enumerate(rows) if "average rates earned" in row_text(row)]
    if not titles:
        raise ValidationFailure(f"{context}: no 'Average Rates Earned' section header found")
    if spec.line_items_section < 1 or spec.line_items_section > len(titles):
        raise ValidationFailure(
            f"{context}: line_items_section = {spec.line_items_section} but the sheet carries "
            f"{len(titles)} 'Average Rates Earned' section(s) (at sheet rows "
            f"{[t + 1 for t in titles]})"
        )
    title_index = titles[spec.line_items_section - 1]
    start = title_index + 1
    end_index = next(
        (index for index, row in enumerate(rows[start:], start=start)
         if "total interest income" in row_text(row)),
        len(rows),
    )
    section = list(enumerate(rows))[start:end_index]

    _, pq0_column = min(header_rows, key=lambda entry: abs(entry[0] - title_index))
    if len(titles) > 1:
        census.notes.append(
            f"{len(titles)} 'Average Rates Earned' sections on the sheet (rows "
            f"{[t + 1 for t in titles]}); reading section {spec.line_items_section} "
            f"(line_items_section)"
        )
    census.notes.append(
        f"Average Rates Earned section: sheet rows {start + 1}..{end_index}; "
        f"PQ0 column {column_letter(pq0_column)} (header nearest the section, of "
        f"{len(header_rows)} PQ header row(s))"
    )

    rates: dict[str, float] = {}
    for key, pattern in LINE_LABEL_PATTERNS.items():
        hits = [(index, row) for index, row in section if pattern in row_text(row)]
        if len(hits) != 1:
            raise ValidationFailure(
                f"{context}: line pattern {pattern!r} matched {len(hits)} row(s) inside the "
                f"Average Rates Earned section — each mapped line must match exactly once"
            )
        row_index, row = hits[0]
        cell = row[pq0_column] if pq0_column < len(row) else None
        value = apply_rate_scale(
            spec.line_items_rate_scale, to_float(cell, context=f"{context}: {key} PQ0"),
            context=f"{context}: {key} PQ0",
        )
        if not 0.0 <= value < 1.0:
            raise ValidationFailure(
                f"{context}: {key} PQ0 rate {value} is outside [0, 1) — check "
                f"line_items_rate_scale (percent-formatted cells store decimals)"
            )
        rates[key] = value
        census.bump("lines read")
        # Per-line provenance: which physical cell fed each rate. When a rate
        # reads 0 or junk, this line points at the exact cell to inspect.
        label = next((str(c).strip() for c in row if not _is_missing(c)), "<no label>")
        census.notes.append(
            f"{key:<14} <- sheet row {row_index + 1}, cell "
            f"{column_letter(pq0_column)}{row_index + 1} = {value:.4%}  ({label[:60]!r})"
        )
    return MappingProxyType(rates), census


# --- MEV series (PID-LOAN-31) ----------------------------------------------


def load_mev_series(
    spec: LoansSheetSpec,
    column: str,
    scenario: str,
    quarters: Sequence[int],
    launch_point: str,
) -> tuple[Mapping[str, float], Mapping[int, float], float]:
    """Read one MEV column's history, projection, and launch-point value.

    The generic sibling of `loans_loader.load_3m_treasury` (that function is
    wholesale-frozen and stays untouched): history rows carry the `Actual`
    scenario keyed by calendar quarter; projection rows carry `scenario` and
    are mapped onto PQ1..PQn BY DATE, never sheet order. Retail needs no
    pre-PQ0 history (the A36 branch is spot-only) but the launch value is read
    from the history block, so the same three-part return shape is kept.

    Reads the RETAIL workbook's own scenario sheet (`retail_mev_sheet`)."""
    workbook = _resolve_workbook(spec, None)
    rows, _ = _load_rows(workbook, spec.retail_mev_sheet)
    context = f"{workbook.name}:{spec.retail_mev_sheet}"
    header = _header_index(rows, spec.mev_header_row, context)
    idx_scenario = _column(header, spec.mev_scenario_column, context)
    idx_date = _column(header, spec.mev_date_column, context)
    idx_rate = _column(header, column, context)

    launch_label = check_quarter_label(f"{context}: launch point", launch_point)
    launch_year, launch_quarter = int(launch_label[:4]), int(launch_label[5])

    history: dict[str, float] = {}
    projection: dict[int, float] = {}
    seen: set[str] = set()
    for row in rows[spec.mev_header_row:]:
        if max(idx_scenario, idx_date, idx_rate) >= len(row):
            continue
        name, raw_date, raw_rate = row[idx_scenario], row[idx_date], row[idx_rate]
        if _is_missing(name) or _is_missing(raw_date) or _is_missing(raw_rate):
            continue
        value = apply_rate_scale(
            spec.mev_rate_scale, to_float(raw_rate, context=f"{context}: {column}"),
            context=f"{context}: {column}",
        )
        label = check_quarter_label(
            f"{context}: date", str(raw_date).strip().replace(" ", "").upper()
        )
        scenario_name = str(name).strip()
        if scenario_name == spec.mev_history_scenario:
            if label in history and history[label] != value:
                raise ValidationFailure(
                    f"{context}: {spec.mev_history_scenario!r} carries {label} twice with "
                    f"different {column!r} values"
                )
            history[label] = value
        elif scenario_name == scenario:
            if label in seen:
                raise ValidationFailure(f"{context}: scenario {scenario!r} carries {label} twice")
            seen.add(label)
            index = (int(label[:4]) - launch_year) * 4 + int(label[5]) - launch_quarter
            if index in quarters:
                projection[index] = value

    missing = [q for q in quarters if q not in projection]
    if missing:
        raise ValidationFailure(
            f"{context}: scenario {scenario!r} is missing PQ{missing} for column {column!r} "
            f"relative to launch point {launch_label}"
        )
    if launch_point not in history:
        raise ValidationFailure(
            f"{context}: launch point {launch_point!r} is absent from the "
            f"{spec.mev_history_scenario!r} history for column {column!r} — every retail spread "
            f"is measured against it"
        )
    return MappingProxyType(history), MappingProxyType(projection), history[launch_point]

"""CRE H.2 reference-key decoding for the CRE loan model (PID-LOAN-18/19/21).

The workbook composes the CRE key exactly as it does the Corporate one —
`{Line Reported on FR Y-9C}_{Interest Rate Variability}_{LOCOM}` — and the
variable-type and LOCOM vocabularies are identical to H.1's, so those parsers
are reused from `loans_mapping`. What is CRE-specific is the line-code side:

    H.2 code -> workbook category   Codes 1 and 2 are both domestic
                                    construction (many-to-one, like the H.1
                                    collapses). Code 7 is ALL non-domestic CRE
                                    excluding owner-occupied, so the Federal
                                    Reserve's three international portfolios —
                                    construction, multifamily, non-owner-
                                    occupied — are DATA-INDISTINGUISHABLE and
                                    modeled as ONE merged category.

    Codes 4 and 6                   "DO NOT USE" per the mapping sheet (working
                                    reading: the owner-occupied FR Y-9C lines,
                                    which are modeled in CORPORATE via H.1 codes
                                    10/11). Rows carrying them fall outside
                                    every CRE category: excluded and censused,
                                    never allocated balance.

The Fed-side census is six portfolios and 24 stated segments (PDF pp. 176-177)
— preserved as [FACT] in `docs/handbook/models/ii_loans_cre.source-brief.md`; the
four-category realization is a recorded, data-forced divergence (PID-LOAN-19).
The Fed names NO FR Y-14Q schedule for CRE at all ("H.2" appears nowhere in the
document — OQ-039), so nothing in this module is Federal Reserve methodology.

Unmapped values are refused, never defaulted."""

from __future__ import annotations

from types import MappingProxyType
from typing import Mapping

from ..core.schemas import ValidationFailure
from ..interest_income.loans_schemas import SegmentKey, VT_DO_NOT_USE
from .loans_mapping import (
    LOCOM_TO_CLASS,
    TABLE_A8_SCALARS,
    VARIABLE_TYPE_NULL_TOKEN,
    parse_locom,
    parse_variable_type,
)

# --- Workbook categories ---------------------------------------------------
# Four, not six: the merged international category carries the Fed portfolios
# (4)-(6) and must stay labeled as such in every output (PID-LOAN-19).
CRE_CATEGORY_NAMES: Mapping[int, str] = MappingProxyType({
    1: "CRE Dom construction",
    2: "CRE Dom multifamily",
    3: "CRE Dom non-owner-occupied",
    4: "CRE International (Fed 4-6 merged)",
})

# The Fed's own six-portfolio census (PDF p. 176, verbatim order), kept so the
# divergence is auditable in code as well as in the brief.
FED_CRE_PORTFOLIOS: Mapping[int, str] = MappingProxyType({
    1: "domestic construction loans",
    2: "domestic multifamily loans",
    3: "domestic non-owner occupied commercial real estate loans",
    4: "international construction loans",
    5: "international multifamily loans",
    6: "international non-owner occupied commercial real estate loans",
})

# H.2 code -> workbook category, from the firm's "H.2 Mapping" sheet
# (user-supplied 2026-08-12). Codes 4 and 6 are deliberately absent: they are
# DO NOT USE, not unknown.
H2_CODE_TO_CRE_CATEGORY: Mapping[int, int] = MappingProxyType({
    1: 1,    # 1-4 family residential construction, domestic (FR Y-9C HC-C 1.a(1))
    2: 1,    # other construction and land development, domestic (1.a(2))
    3: 2,    # multifamily (5+) residential, domestic (1.d)
    5: 3,    # other nonfarm nonresidential (non-owner-occupied), domestic (1.e(2))
    7: 4,    # ALL non-domestic CRE excluding owner-occupied (HC-C item 1) — the
             # Fed's three international portfolios, indivisible in this field
})

# Marked DO NOT USE on the mapping sheet. Working reading (flagged in the CRE
# brief §4.3): the owner-occupied lines, already modeled in Corporate.
H2_DO_NOT_USE_CODES: tuple[int, ...] = (4, 6)

_KNOWN_H2_CODES = tuple(sorted(set(H2_CODE_TO_CRE_CATEGORY) | set(H2_DO_NOT_USE_CODES)))


def parse_h2_code(raw: object) -> int:
    """Decode a `Line Reported on FR Y-9C` cell to an H.2 code.

    DO-NOT-USE codes (4 and 6) parse successfully — they are declared by the
    mapping sheet, so the LOADER excludes and censuses them; refusing them here
    would turn a declared exclusion into a crash. A code outside 1-7 is
    genuinely unknown and is refused."""
    if isinstance(raw, str):
        raw = raw.strip()
        if not raw:
            raise ValidationFailure(
                "Line Reported on FR Y-9C is blank — no CRE category can be assigned"
            )
        try:
            raw = int(raw)
        except ValueError:
            raise ValidationFailure(
                f"Line Reported on FR Y-9C {raw!r} is not a whole-number code"
            ) from None
    if raw is None or isinstance(raw, bool) or not isinstance(raw, (int, float)) or int(raw) != raw:
        raise ValidationFailure(f"Line Reported on FR Y-9C {raw!r} is not a whole-number code")
    code = int(raw)
    if code not in _KNOWN_H2_CODES:
        raise ValidationFailure(
            f"H.2 code {code} is not in the mapping (known codes {list(_KNOWN_H2_CODES)}, of "
            f"which {list(H2_DO_NOT_USE_CODES)} are DO NOT USE). Refused rather than defaulted — "
            f"an invented category assignment is invisible in the output."
        )
    return code


def is_h2_do_not_use(raw: object) -> bool:
    """Whether a line code is one the mapping sheet marks DO NOT USE."""
    return parse_h2_code(raw) in H2_DO_NOT_USE_CODES


def cre_reference_key(h2_code: object, variable_type: object, locom: object) -> str:
    """Render the workbook's composite key for diagnostics (`1_2_3`, `7_[NULL]_1`)."""
    vt = parse_variable_type(variable_type)
    token = VARIABLE_TYPE_NULL_TOKEN if vt == VT_DO_NOT_USE else str(vt)
    return f"{parse_h2_code(h2_code)}_{token}_{parse_locom(locom)}"


def decode_cre_segment(h2_code: object, variable_type: object, locom: object) -> SegmentKey:
    """Map one H.2 row's three raw values to the model's segment key.

    A DO-NOT-USE line code has no category and must be excluded by the caller
    BEFORE decoding; reaching here with one is a programming error surfaced as
    a refusal, not a silent bucket."""
    code = parse_h2_code(h2_code)
    if code in H2_DO_NOT_USE_CODES:
        raise ValidationFailure(
            f"H.2 code {code} is DO NOT USE and belongs to no CRE category — the loader must "
            f"exclude and census it, never decode it"
        )
    category = H2_CODE_TO_CRE_CATEGORY[code]
    return SegmentKey(
        category=CRE_CATEGORY_NAMES[category],
        locom=LOCOM_TO_CLASS[parse_locom(locom)],
        variable_type=parse_variable_type(variable_type),
    )


# --- Industry scalars: the CRE assignment (PID-LOAN-21) ---------------------
# [PID-LOAN-21 — USER-CONFIRMED 2026-08-12]. NOT a Federal Reserve statement:
# no Table A8 row is assigned to any CRE portfolio in the source, and no row
# names international CRE at all (OQ-010 stays open on the source side and for
# Retail). The assignment below reproduced the workbook's own results blocks
# exactly — Total = (Fixed + Variable) x 1.081 for the three domestic
# categories and x 1.113 for the merged international block.
TABLE_A8_BY_CRE_CATEGORY: Mapping[int, str] = MappingProxyType({
    1: "Domestic CRE",
    2: "Domestic CRE",
    3: "Domestic CRE",
    4: "Rest of wholesale",   # a DOMESTIC row cannot apply to international CRE
})


def cre_scalars_by_category_name() -> Mapping[str, float]:
    """The {CRE category name -> Table A8 scalar} map the projection consumes."""
    return MappingProxyType({
        CRE_CATEGORY_NAMES[category]: TABLE_A8_SCALARS[row]
        for category, row in TABLE_A8_BY_CRE_CATEGORY.items()
    })


# --- M.1 role verification ---------------------------------------------------
# The CRE multiplicand is wired by ROW (PID-LOAN-20: M.1 rows 17/18/21), not by
# role label — the user confirmed the cells directly. The role columns are still
# read on those rows so a misconfigured row number is visible: a configured CRE
# row whose domestic role does not look like a Wholesale-CRE label is warned
# about, never silently summed.
M1_CRE_ROLE_PREFIX = "wholesale - cre"

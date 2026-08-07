"""CORP H.1 reference-key decoding for the Corporate loan model (PID-LOAN-9).

The workbook composes a key from three H.1 columns — `Line Reported on FR Y9C`,
`Interest Rate Variablility` (the sheet's own spelling), and `Lower of Cost or
Market Flag` — as `{H.1 code}_{variable type}_{LOCOM}`. Decoding it applies two
collapses that the model's segment key depends on, so both live here rather than
being scattered through the loader:

    H.1 code -> Fed Category   MANY-TO-ONE. Codes 4 and 5 are both Commercial and
                               industrial; codes 1, 2 and 7 are all Loans to
                               Financial Institutions.

    LOCOM     -> asset class   THREE-VALUED, collapsing to the Fed's two. Flag 3
                               is HFI; flags 1 (LOCOM/HFS) and 2 (FVO) both roll
                               into FVO/HFS (PDF p. 175).

Nothing here is Federal Reserve methodology: the Board names the eleven Corporate
portfolios but never states the form that defines them (OQ-038). This table is the
firm's own "H.1 Mapping" sheet, transcribed, and is the project's binding.

Unmapped values are refused, never defaulted. The value vocabulary is only
evidenced for what the mapping sheet lists, so a silent default would be an
invention — and an invented category assignment is invisible in the output."""

from __future__ import annotations

from types import MappingProxyType
from typing import Mapping

from ..core.schemas import ValidationFailure
from ..interest_income.loans_schemas import (
    VT_DO_NOT_USE,
    VT_ENTRY_FEE,
    VT_FIXED,
    VT_FLOATING,
    VT_MIXED,
    SegmentKey,
)

# --- Fed Categories -------------------------------------------------------
# The eleven Corporate portfolios, in the source's own order (PDF p. 175).
FED_CATEGORY_NAMES: Mapping[int, str] = MappingProxyType({
    1: "Commercial and industrial",
    2: "Domestic owner-occupied CRE",
    3: "Other Non-consumer",
    4: "Other leases",
    5: "Loans to Foreign Governments",
    6: "International Owner-Occupied CRE",
    7: "Agriculture Loans",
    8: "Loans to Financial Institutions",
    9: "Loans for Purchasing and Carrying Securities",
    10: "Domestic farmland",
    11: "International farmland",
})

# H.1 code -> Fed Category, from the workbook's "H.1 Mapping" sheet.
H1_CODE_TO_FED_CATEGORY: Mapping[int, int] = MappingProxyType({
    1: 8,    # Loans to U.S. banks and other U.S. depository institutions
    2: 8,    # Loans to foreign banks
    3: 7,    # Loans to finance agricultural production
    4: 1,    # C&I loans to U.S. addressees
    5: 1,    # C&I loans to non-U.S. addressees
    6: 5,    # Loans to foreign governments and official institutions
    7: 8,    # Loans to nondepository financial institutions
    8: 3,    # All other loans, excluding consumer loans
    9: 4,    # All other leases, excluding consumer leases
    10: 2,   # Owner-occupied nonfarm nonresidential, domestic offices
    11: 6,   # Owner-occupied nonfarm nonresidential, non-domestic offices
})

# The H.1 codes that make up "Loans to Depository Institutions" — the proxy-spread
# slice for the merged 9/10/11 bucket (PID-LOAN-10). Strictly NARROWER than Fed
# Category 8, which also contains code 7 (nondepository financial institutions):
# the Fed writes "depository institutions" while its portfolio list says
# "financial institutions", and this is what that gap resolves to.
DEPOSITORY_INSTITUTION_H1_CODES: tuple[int, ...] = (1, 2)

# Fed Categories with no H.1 code at all. The Board states these portfolios "have
# no loan-level data on the FR Y-14Q H.1 schedule" (PDF p. 176); the mapping sheet
# leaves their H.1 Code cell blank, which is the same fact in physical form. They
# are merged into one bucket sourced from FR Y-9C (PID-LOAN-10).
CATEGORIES_WITHOUT_H1 = (9, 10, 11)
MERGED_H1_LESS_CATEGORY = 9   # the merged bucket is carried under the first of the three

# --- Asset classification -------------------------------------------------
LOCOM_HFS = 1        # LOCOM (HFS)
LOCOM_FVO = 2        # FVO
LOCOM_HFI = 3        # HFI

CLASS_HFI = "HFI"
CLASS_FVO_HFS = "FVO_HFS"

LOCOM_TO_CLASS: Mapping[int, str] = MappingProxyType({
    LOCOM_HFS: CLASS_FVO_HFS,
    LOCOM_FVO: CLASS_FVO_HFS,
    LOCOM_HFI: CLASS_HFI,
})

# --- Variable type --------------------------------------------------------
# The data carries only 1, 2, 3, 4 and the literal string "[NULL]" (user-verified
# 2026-08-07: never a literal 0, never blank). "[NULL]" IS the DO NOT USE class,
# which the mapping sheet numbers 0 — so the string maps onto the model's code 0
# and a literal 0 or a blank is an anomaly worth stopping for.
VARIABLE_TYPE_NULL_TOKEN = "[NULL]"

VARIABLE_TYPE_LABELS: Mapping[int, str] = MappingProxyType({
    VT_DO_NOT_USE: "DO NOT USE",
    VT_FIXED: "Fixed",
    VT_FLOATING: "Floating",
    VT_MIXED: "Mixed",
    VT_ENTRY_FEE: "Entirely Fee base",
})


def parse_variable_type(raw: object) -> int:
    """Decode an `Interest Rate Variablility` cell to a model rate-type code.

    The literal `[NULL]` is DO NOT USE. A blank cell is NOT accepted: the user
    verified the column never contains one, so a blank means something changed
    upstream, and quietly folding it into DO NOT USE would move balance out of
    the income-earning segments without a trace."""
    if isinstance(raw, str):
        token = raw.strip()
        if token.upper() == VARIABLE_TYPE_NULL_TOKEN:
            return VT_DO_NOT_USE
        if not token:
            raise ValidationFailure(
                "Interest Rate Variablility is blank. The column is expected to carry only "
                "1, 2, 3, 4 or the literal '[NULL]' (user-verified 2026-08-07), so a blank is "
                "an upstream change rather than a value — refused instead of being folded "
                "into DO NOT USE, which would silently move balance out of the earning segments."
            )
        try:
            raw = int(token)
        except ValueError:
            raise ValidationFailure(
                f"Interest Rate Variablility {raw!r} is not a recognized rate type. Expected "
                f"1, 2, 3, 4 or '[NULL]'."
            ) from None
    if raw is None:
        raise ValidationFailure(
            "Interest Rate Variablility is empty. Expected 1, 2, 3, 4 or the literal '[NULL]'."
        )
    if isinstance(raw, bool) or not isinstance(raw, (int, float)) or int(raw) != raw:
        raise ValidationFailure(f"Interest Rate Variablility {raw!r} is not a whole-number code")
    code = int(raw)
    if code not in VARIABLE_TYPE_LABELS:
        raise ValidationFailure(
            f"Interest Rate Variablility {code} is not a mapped rate type "
            f"(expected {sorted(VARIABLE_TYPE_LABELS)} or '[NULL]')"
        )
    return code


def parse_h1_code(raw: object) -> int:
    """Decode a `Line Reported on FR Y9C` cell to an H.1 code."""
    if isinstance(raw, str):
        raw = raw.strip()
        if not raw:
            raise ValidationFailure("Line Reported on FR Y9C is blank — no Fed Category can be assigned")
        try:
            raw = int(raw)
        except ValueError:
            raise ValidationFailure(f"Line Reported on FR Y9C {raw!r} is not a whole-number code") from None
    if raw is None or isinstance(raw, bool) or not isinstance(raw, (int, float)) or int(raw) != raw:
        raise ValidationFailure(f"Line Reported on FR Y9C {raw!r} is not a whole-number code")
    code = int(raw)
    if code not in H1_CODE_TO_FED_CATEGORY:
        raise ValidationFailure(
            f"H.1 code {code} has no Fed Category in the mapping (known codes "
            f"{sorted(H1_CODE_TO_FED_CATEGORY)}). Refused rather than defaulted — an invented "
            f"category assignment is invisible in the output."
        )
    return code


def parse_locom(raw: object) -> int:
    """Decode a `Lower of Cost or Market Flag` cell."""
    if isinstance(raw, str):
        raw = raw.strip()
        if not raw:
            raise ValidationFailure("Lower of Cost or Market Flag is blank — no asset class can be assigned")
        try:
            raw = int(raw)
        except ValueError:
            raise ValidationFailure(f"Lower of Cost or Market Flag {raw!r} is not a whole-number code") from None
    if raw is None or isinstance(raw, bool) or not isinstance(raw, (int, float)) or int(raw) != raw:
        raise ValidationFailure(f"Lower of Cost or Market Flag {raw!r} is not a whole-number code")
    flag = int(raw)
    if flag not in LOCOM_TO_CLASS:
        raise ValidationFailure(
            f"Lower of Cost or Market Flag {flag} is not mapped (expected "
            f"{sorted(LOCOM_TO_CLASS)}: 1 LOCOM/HFS, 2 FVO, 3 HFI)"
        )
    return flag


def reference_key(h1_code: object, variable_type: object, locom: object) -> str:
    """Render the workbook's own composite key, for traceability in diagnostics.

    Mirrors the sheet's spelling exactly — `4_1_3`, and `4_[NULL]_3` for DO NOT
    USE — so a row can be matched back to the reference-key sheet by eye."""
    vt = parse_variable_type(variable_type)
    token = VARIABLE_TYPE_NULL_TOKEN if vt == VT_DO_NOT_USE else str(vt)
    return f"{parse_h1_code(h1_code)}_{token}_{parse_locom(locom)}"


def decode_segment(h1_code: object, variable_type: object, locom: object) -> SegmentKey:
    """Map one row's three raw H.1 values to the model's segment key.

    This is where the two collapses happen: many H.1 codes fold into one Fed
    Category, and three LOCOM flags fold into the Fed's two asset classes."""
    category = H1_CODE_TO_FED_CATEGORY[parse_h1_code(h1_code)]
    return SegmentKey(
        category=FED_CATEGORY_NAMES[category],
        locom=LOCOM_TO_CLASS[parse_locom(locom)],
        variable_type=parse_variable_type(variable_type),
    )


def is_depository_institution_row(h1_code: object) -> bool:
    """Whether a row belongs to the proxy-spread slice for the merged bucket."""
    return parse_h1_code(h1_code) in DEPOSITORY_INSTITUTION_H1_CODES

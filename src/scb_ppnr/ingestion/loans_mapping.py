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


# --- M.1 Balance roles ----------------------------------------------------
# The M.1 sheet carries its own FRB NII model role per row: column A for the
# domestic side, column B for the international one. That IS the wiring from an
# FR Y-9C line to a Fed Category — nothing needs to be supplied separately.
#
# Only "Wholesale - Corp" rows belong to this model; the sheet's Retail and
# "Wholesale - CRE" rows are other models' business and are skipped.
M1_CORPORATE_ROLE_PREFIX = "wholesale - corp"

# Normalized role suffix -> Fed Category. Matching is exact on the normalized
# suffix, never a substring: "int farmland" and "farmland" are different
# categories and a substring match would silently merge them.
M1_ROLE_TO_FED_CATEGORY: Mapping[str, int] = MappingProxyType({
    "c&i and others": 1,
    "owned occupied cre": 2,
    "other nonconsumer": 3,
    "other leases": 4,
    "foreign gov": 5,
    "int owned occupied cre": 6,
    "agricultural": 7,
    "fi": 8,
    "securities": 9,
    "farmland": 10,
    "int farmland": 11,
})


def normalize_role(label: object) -> str:
    """Reduce an M.1 role label to a comparable form (case and spacing only)."""
    return " ".join(str(label).strip().lower().split()) if label is not None else ""


def m1_role_category(label: object) -> int | None:
    """Map an M.1 role label to a Fed Category, or None if it is not Corporate.

    Returns None for the sheet's Retail and Wholesale-CRE rows, which belong to
    other models. Raises for a Corporate row whose suffix is unrecognized — the
    label text is truncated in the workbook's display width, so an unmatched
    Corporate role means the transcribed suffix is wrong and the run should say
    so rather than drop that category's balance to zero."""
    normalized = normalize_role(label)
    if not normalized.startswith(M1_CORPORATE_ROLE_PREFIX):
        return None
    suffix = normalized[len(M1_CORPORATE_ROLE_PREFIX):].lstrip(" -")
    if suffix not in M1_ROLE_TO_FED_CATEGORY:
        raise ValidationFailure(
            f"M.1 role {label!r} is a Corporate row but its suffix {suffix!r} is not one of "
            f"{sorted(M1_ROLE_TO_FED_CATEGORY)}. Refused rather than skipped — skipping would "
            f"silently zero that category's balance."
        )
    return M1_ROLE_TO_FED_CATEGORY[suffix]


def is_depository_institution_row(h1_code: object) -> bool:
    """Whether a row belongs to the proxy-spread slice for the merged bucket."""
    return parse_h1_code(h1_code) in DEPOSITORY_INSTITUTION_H1_CODES


# --- Industry scalars: Table A8 (PID-LOAN-11) -----------------------------
# Federal Reserve published values, Table A8 "Scalars for Proposed Interest
# Income on Loans Model" (PDF p. 220; md sec-209). Image-verified 2026-07-16 and
# re-verified 2026-08-03; identical to the workbook's FRB scalar column, which is
# why the values are taken from the source directly rather than parsed.
#
# [FACT] These seven values are the Fed's. Everything below about WHICH loan
# portfolio each one multiplies is [INT] — see TABLE_A8_BY_FED_CATEGORY.
TABLE_A8_SCALARS: Mapping[str, float] = MappingProxyType({
    "Auto": 0.865,
    "C&I, noncore SME loan and card": 1.033,
    "Credit Card": 0.969,
    "Domestic CRE": 1.081,
    "Mortgage": 1.014,
    "Noncore": 1.072,
    "Rest of wholesale": 1.113,
})

# The four retail rows are out of Corporate's scope and are listed only so the
# census can show that nothing silently fell into them.
TABLE_A8_RETAIL_ROWS = ("Auto", "Credit Card", "Mortgage", "Noncore")

# Fed Category -> Table A8 row.
#
# [PID-LOAN-11, amended — USER-CONFIRMED 2026-08-07]. NOT a Federal Reserve
# statement: Table A8 has seven portfolio rows while the model works in eleven
# Fed Categories, and the source states no correspondence (footnote 63 even
# lists EIGHT categories against the table's seven — SQ-11). The assignment
# below is the project's, confirmed by the user, and OQ-010 remains open on the
# source side and for the CRE and Retail portfolios.
#
# Only three rows are wholesale-relevant: Category 1 takes the row that names
# it, Category 2 takes Domestic CRE, and every remaining Corporate category
# takes "Rest of wholesale" — including Category 6, since a DOMESTIC row cannot
# apply to international owner-occupied CRE, and the merged 9/10/11 bucket.
TABLE_A8_BY_FED_CATEGORY: Mapping[int, str] = MappingProxyType({
    1: "C&I, noncore SME loan and card",
    2: "Domestic CRE",
    3: "Rest of wholesale",
    4: "Rest of wholesale",
    5: "Rest of wholesale",
    6: "Rest of wholesale",
    7: "Rest of wholesale",
    8: "Rest of wholesale",
    9: "Rest of wholesale",
    10: "Rest of wholesale",
    11: "Rest of wholesale",
})

# Assignments the project has NOT had confirmed. Empty for Corporate since
# 2026-08-07; the machinery stays because CRE and Retail reach the same table
# with the same seven rows and the same unstated correspondence.
UNCERTAIN_SCALAR_CATEGORIES: tuple[int, ...] = ()


def scalars_by_category_name(
    overrides: Mapping[int, str] | None = None,
) -> tuple[Mapping[str, float], tuple[str, ...]]:
    """Build the {Fed Category name -> scalar} map the projection consumes.

    `overrides` replaces individual Category -> Table A8 row assignments once the
    correspondence is settled. Returns the map plus warning lines naming every
    assignment the source does not support, so the run reports its own soft spots
    rather than presenting an interpretation as a fact."""
    assignments = dict(TABLE_A8_BY_FED_CATEGORY)
    if overrides:
        for category, row in overrides.items():
            if category not in FED_CATEGORY_NAMES:
                raise ValidationFailure(
                    f"scalar override names Fed Category {category}, which does not exist "
                    f"(expected {sorted(FED_CATEGORY_NAMES)})"
                )
            if row not in TABLE_A8_SCALARS:
                raise ValidationFailure(
                    f"scalar override for Fed Category {category} names Table A8 row {row!r}, "
                    f"which is not one of {sorted(TABLE_A8_SCALARS)}"
                )
            assignments[category] = row

    mapping = {FED_CATEGORY_NAMES[c]: TABLE_A8_SCALARS[row] for c, row in assignments.items()}

    warnings: list[str] = []
    for category in UNCERTAIN_SCALAR_CATEGORIES:
        if overrides and category in overrides:
            continue
        warnings.append(
            f"OQ-010: Fed Category {category} ({FED_CATEGORY_NAMES[category]}) is assigned "
            f"Table A8 row {assignments[category]!r} by interpretation — the source states no "
            f"category-to-row correspondence. Confirm or override."
        )
    retail = sorted({row for row in assignments.values()} & set(TABLE_A8_RETAIL_ROWS))
    if retail:
        warnings.append(f"a Corporate category is mapped to a RETAIL Table A8 row: {retail}")
    return MappingProxyType(mapping), tuple(warnings)

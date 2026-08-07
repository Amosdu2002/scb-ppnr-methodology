"""CORP H.1 reference-key decoding (PID-LOAN-9).

The two collapses tested here — many H.1 codes into one Fed Category, three LOCOM
flags into the Fed's two asset classes — are where a loader silently puts balance
in the wrong bucket, so they are pinned independently of any workbook I/O."""

from __future__ import annotations

import pytest

from scb_ppnr.core.schemas import ValidationFailure
from scb_ppnr.ingestion.loans_mapping import (
    CATEGORIES_WITHOUT_H1,
    CLASS_FVO_HFS,
    CLASS_HFI,
    DEPOSITORY_INSTITUTION_H1_CODES,
    FED_CATEGORY_NAMES,
    H1_CODE_TO_FED_CATEGORY,
    decode_segment,
    is_depository_institution_row,
    parse_locom,
    parse_variable_type,
    reference_key,
)
from scb_ppnr.interest_income.loans_schemas import (
    TREATMENT_NO_INCOME,
    VT_DO_NOT_USE,
    VT_FIXED,
    VT_FLOATING,
)


# --- H.1 code -> Fed Category is many-to-one ------------------------------

def test_codes_four_and_five_both_land_in_commercial_and_industrial():
    assert decode_segment(4, 1, 3).category == "Commercial and industrial"
    assert decode_segment(5, 1, 3).category == "Commercial and industrial"
    assert decode_segment(4, 1, 3) == decode_segment(5, 1, 3)


def test_codes_one_two_and_seven_all_land_in_loans_to_financial_institutions():
    for code in (1, 2, 7):
        assert decode_segment(code, 2, 3).category == "Loans to Financial Institutions"


def test_every_h1_code_maps_and_no_category_is_invented():
    assert sorted(H1_CODE_TO_FED_CATEGORY) == list(range(1, 12))
    assert set(H1_CODE_TO_FED_CATEGORY.values()) <= set(FED_CATEGORY_NAMES)
    # the three data-limited portfolios are reachable from no H.1 code at all
    assert set(CATEGORIES_WITHOUT_H1).isdisjoint(H1_CODE_TO_FED_CATEGORY.values())


def test_unmapped_h1_code_is_refused():
    with pytest.raises(ValidationFailure, match="no Fed Category in the mapping"):
        decode_segment(12, 1, 3)


# --- LOCOM collapses three values into two --------------------------------

def test_locom_flags_one_and_two_both_mean_fvo_hfs_while_three_is_hfi():
    assert decode_segment(4, 1, 1).locom == CLASS_FVO_HFS   # LOCOM (HFS)
    assert decode_segment(4, 1, 2).locom == CLASS_FVO_HFS   # FVO
    assert decode_segment(4, 1, 3).locom == CLASS_HFI


def test_hfs_and_fvo_rows_share_one_segment():
    assert decode_segment(4, 1, 1) == decode_segment(4, 1, 2)


def test_unmapped_locom_flag_is_refused():
    with pytest.raises(ValidationFailure, match="not mapped"):
        parse_locom(4)


# --- variable type, including the [NULL] token ----------------------------

def test_the_literal_null_token_is_the_do_not_use_class():
    assert parse_variable_type("[NULL]") == VT_DO_NOT_USE
    assert parse_variable_type(" [null] ") == VT_DO_NOT_USE
    assert decode_segment(4, "[NULL]", 3).treatment == TREATMENT_NO_INCOME


def test_numeric_rate_types_decode():
    assert parse_variable_type(1) == VT_FIXED
    assert parse_variable_type("2") == VT_FLOATING


def test_a_blank_cell_is_refused_rather_than_folded_into_do_not_use():
    """The user verified the column never contains a blank, so one means an
    upstream change — and folding it into DO NOT USE would move balance out of
    the income-earning segments without a trace."""
    with pytest.raises(ValidationFailure, match="blank"):
        parse_variable_type("")
    with pytest.raises(ValidationFailure, match="empty"):
        parse_variable_type(None)


def test_an_unknown_rate_type_is_refused():
    with pytest.raises(ValidationFailure, match="not a mapped rate type"):
        parse_variable_type(9)


# --- composite key --------------------------------------------------------

def test_reference_key_matches_the_workbook_spelling():
    assert reference_key(4, 1, 3) == "4_1_3"
    assert reference_key(5, 4, 1) == "5_4_1"
    assert reference_key(4, "[NULL]", 3) == "4_[NULL]_3"


# --- the depository-institutions slice (PID-LOAN-10) ----------------------

def test_depository_slice_is_narrower_than_loans_to_financial_institutions():
    """The Fed writes 'lending to depository institutions' while its portfolio
    list says 'financial institutions'; the workbook resolves that gap by
    excluding code 7, nondepository financial institutions."""
    assert DEPOSITORY_INSTITUTION_H1_CODES == (1, 2)
    assert is_depository_institution_row(1) and is_depository_institution_row(2)
    assert not is_depository_institution_row(7)
    # ... yet all three sit inside the same Fed Category
    assert {H1_CODE_TO_FED_CATEGORY[c] for c in (1, 2, 7)} == {8}


# --- Table A8 scalars (PID-LOAN-11) ---------------------------------------

def test_table_a8_values_match_the_published_table():
    """PDF p. 220, image-verified. The workbook's FRB column is identical, which
    is why the values come from the source rather than being parsed."""
    from scb_ppnr.ingestion.loans_mapping import TABLE_A8_SCALARS

    assert TABLE_A8_SCALARS == {
        "Auto": 0.865,
        "C&I, noncore SME loan and card": 1.033,
        "Credit Card": 0.969,
        "Domestic CRE": 1.081,
        "Mortgage": 1.014,
        "Noncore": 1.072,
        "Rest of wholesale": 1.113,
    }


def test_every_fed_category_gets_a_scalar_and_none_lands_in_a_retail_row():
    from scb_ppnr.ingestion.loans_mapping import (
        TABLE_A8_BY_FED_CATEGORY,
        TABLE_A8_RETAIL_ROWS,
        scalars_by_category_name,
    )

    assert sorted(TABLE_A8_BY_FED_CATEGORY) == list(range(1, 12))
    mapping, _ = scalars_by_category_name()
    assert set(mapping) == set(FED_CATEGORY_NAMES.values())
    assert not set(TABLE_A8_BY_FED_CATEGORY.values()) & set(TABLE_A8_RETAIL_ROWS)


def test_the_uncertain_assignment_warns_on_every_run():
    """OQ-010 is unresolved, so the interpretation announces itself rather than
    passing as a fact."""
    from scb_ppnr.ingestion.loans_mapping import scalars_by_category_name

    mapping, warnings = scalars_by_category_name()
    assert mapping["Domestic owner-occupied CRE"] == pytest.approx(1.081)
    assert any("OQ-010" in w and "Domestic owner-occupied CRE" in w for w in warnings)


def test_an_override_settles_the_assignment_and_silences_its_warning():
    from scb_ppnr.ingestion.loans_mapping import scalars_by_category_name

    mapping, warnings = scalars_by_category_name({2: "Rest of wholesale"})
    assert mapping["Domestic owner-occupied CRE"] == pytest.approx(1.113)
    assert not any("OQ-010" in w for w in warnings)


def test_a_bad_override_is_refused():
    from scb_ppnr.ingestion.loans_mapping import scalars_by_category_name

    with pytest.raises(ValidationFailure, match="does not exist"):
        scalars_by_category_name({99: "Rest of wholesale"})
    with pytest.raises(ValidationFailure, match="not one of"):
        scalars_by_category_name({2: "Not A Row"})

"""Proposed 2026 Fed PPNR interest-income model family — canonical-input reference
implementation. Increment 1: the two Family A calculators. Later increments add
the securities family (shared three-term engine), the loans subpackage, trading
NII (mirroring the ie_other_borrowing calibration factoring), and the income
orchestrator. See architecture/interest-income-design.md."""

from ..core.schemas import PROJECTION_QUARTERS, ValidationFailure
from .common import build_income_result, quarterly_income
from .ii_dep_banks_other import project_dep_banks_other
from .ii_mbs import project_mbs
from .ii_other_ida import project_other_ida
from .ii_other_sec import project_other_sec
from .ii_ust import project_ust
from .schemas import (
    DepBanksOtherInputs,
    DepBanksOtherQuarterDiagnostics,
    IncomeFamilyInputs,
    IncomeModelResult,
    IncomeQuarterResult,
    IncomeScenarioPaths,
    OtherIdaInputs,
    OtherIdaQuarterDiagnostics,
)
from .securities_engine import INTERIM_CHOICES, reinvestment_income
from .securities_schemas import (
    FLOAT_PROJECTION_MODES,
    FLOAT_PROJECTION_NEG_HOLD,
    FLOAT_PROJECTION_NEG_HOLD_BLEND,
    FLOAT_PROJECTION_SPOT,
    CATEGORY_MODEL_MAP,
    FLOOR_MODE_NONE,
    FLOOR_MODE_SECURITY,
    FLOOR_MODE_SECURITY_ELSE_ZERO,
    FLOOR_MODE_ZERO,
    FLOOR_MODES,
    MODEL_MBS,
    MODEL_OTHER_SEC,
    MODEL_UST,
    OUT_OF_SCOPE,
    RATE_FIXED,
    RATE_FLOATING,
    RATE_ZERO_COUPON,
    SecuritiesInputs,
    SecuritiesQuarterDiagnostics,
    SecurityPosition,
    assign_model,
)

__all__ = [
    "CATEGORY_MODEL_MAP",
    "DepBanksOtherInputs",
    "DepBanksOtherQuarterDiagnostics",
    "FLOAT_PROJECTION_MODES",
    "FLOAT_PROJECTION_NEG_HOLD",
    "FLOAT_PROJECTION_NEG_HOLD_BLEND",
    "FLOAT_PROJECTION_SPOT",
    "FLOOR_MODES",
    "FLOOR_MODE_NONE",
    "FLOOR_MODE_SECURITY",
    "FLOOR_MODE_SECURITY_ELSE_ZERO",
    "FLOOR_MODE_ZERO",
    "INTERIM_CHOICES",
    "IncomeFamilyInputs",
    "IncomeModelResult",
    "IncomeQuarterResult",
    "IncomeScenarioPaths",
    "MODEL_MBS",
    "MODEL_OTHER_SEC",
    "MODEL_UST",
    "OUT_OF_SCOPE",
    "OtherIdaInputs",
    "OtherIdaQuarterDiagnostics",
    "PROJECTION_QUARTERS",
    "RATE_FIXED",
    "RATE_FLOATING",
    "RATE_ZERO_COUPON",
    "SecuritiesInputs",
    "SecuritiesQuarterDiagnostics",
    "SecurityPosition",
    "ValidationFailure",
    "assign_model",
    "build_income_result",
    "project_dep_banks_other",
    "project_mbs",
    "project_other_ida",
    "project_other_sec",
    "project_ust",
    "quarterly_income",
    "reinvestment_income",
]

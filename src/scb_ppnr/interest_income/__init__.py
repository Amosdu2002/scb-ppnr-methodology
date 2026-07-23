"""Proposed 2026 Fed PPNR interest-income model family — canonical-input reference
implementation. Increment 1: the two Family A calculators. Later increments add
the securities family (shared three-term engine), the loans subpackage, trading
NII (mirroring the ie_other_borrowing calibration factoring), and the income
orchestrator. See architecture/interest-income-design.md."""

from ..core.schemas import PROJECTION_QUARTERS, ValidationFailure
from .common import build_income_result, quarterly_income
from .ii_dep_banks_other import project_dep_banks_other
from .ii_other_ida import project_other_ida
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

__all__ = [
    "DepBanksOtherInputs",
    "DepBanksOtherQuarterDiagnostics",
    "IncomeFamilyInputs",
    "IncomeModelResult",
    "IncomeQuarterResult",
    "IncomeScenarioPaths",
    "OtherIdaInputs",
    "OtherIdaQuarterDiagnostics",
    "PROJECTION_QUARTERS",
    "ValidationFailure",
    "build_income_result",
    "project_dep_banks_other",
    "project_other_ida",
    "quarterly_income",
]

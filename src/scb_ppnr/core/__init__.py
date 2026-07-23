"""Side-neutral core shared by every model family: canonical-boundary conventions
(`schemas`) and cross-family mechanics (`common`). Holds no model semantics —
scenario containers, per-model inputs, parameters, engines, and result types stay
in their family packages (interest_expense, interest_income)."""

from .common import (
    RECONCILIATION_TOLERANCE_REL,
    RunIdentified,
    build_result,
    freeze_projection_path,
    quarterly_flow,
    reconciliation_tolerance,
    require_same_run,
    sum_path,
)
from .schemas import (
    LAUNCH_QUARTER,
    PROJECTION_QUARTERS,
    RATE_SCALE_GUARD,
    SCENARIO_QUARTERS_WITH_LAUNCH,
    ValidationFailure,
    check_balance,
    check_finite,
    check_rate,
    check_share,
    freeze_path,
    require_id,
)

__all__ = [
    "LAUNCH_QUARTER",
    "PROJECTION_QUARTERS",
    "RATE_SCALE_GUARD",
    "RECONCILIATION_TOLERANCE_REL",
    "RunIdentified",
    "SCENARIO_QUARTERS_WITH_LAUNCH",
    "ValidationFailure",
    "build_result",
    "check_balance",
    "check_finite",
    "check_rate",
    "check_share",
    "freeze_path",
    "freeze_projection_path",
    "quarterly_flow",
    "reconciliation_tolerance",
    "require_id",
    "require_same_run",
    "sum_path",
]

"""Two-sheet firm-data loader (D-007): a spot sheet and a wide quarterly sheet.

Interchange layout — extra columns are ignored on both sheets:

    spot sheet      model, field, subcomponent, scale, value       (one row per input)
    quarterly sheet model, field, subcomponent, scale, PQ1..PQ9    (one row per series)

Spot rows carry one-time launch-point scalars (rates, balances, WAL, shares, ELB
spreads); quarterly rows carry PQ1..PQ9 paths with the scale declared once per row.
Inside the company, formula-built workbook tabs assemble both from the confidential
workbook; only these tidy tables cross the boundary, so no sheet or cell reference
ever appears in code. Scale rules (D-006): rate/spread/share values declare `scale`
percent | decimal; balances and dollar amounts declare `scale` millions | billions
and are normalized here to the canonical USD-millions unit (Schedule G reports
millions while the FRB projection paths arrive in billions — mixing them undeclared
would be silently absorbed into the α_b calibration); months values leave `scale`
blank (already canonical).

The Fed provides three firm-level projection paths (OQ-023, narrowed 2026-07-20) as
quarterly-sheet rows under model `family`: `frb_total_interest_expense` is REQUIRED
(the PID-OB-5 calibration target); `frb_total_interest_income` and
`frb_net_interest_income` are optional companions (a supplied row carries all nine
quarters) — no interest-expense model consumes them, but when both accompany the
expense path the NII = income − expense identity is checked as a wiring guard.

Sign convention (D-008): the FRB file enters the expense path as **negative** amounts
(income positive; NII = income + expense under that entry convention). Declare
`[firm_data].frb_expense_sign = "negative"` and this loader negates the expense path
to the canonical positive-magnitude convention — income and NII pass through
as-entered, and the identity guard is convention-consistent after the flip. The
physical file mapping remains to be confirmed inside the company before reliance."""

from __future__ import annotations

from pathlib import Path

from ..core.schemas import PROJECTION_QUARTERS, ValidationFailure
from ..interest_income.schemas import (
    DepBanksOtherInputs,
    IncomeFamilyInputs,
    OtherIdaInputs,
    TradingNiiInputs,
)
from ..interest_expense.schemas import (
    FOREIGN_SUBCOMPONENTS,
    OTHER_DOM_SUBCOMPONENTS,
    DepositSubcomponent,
    DomTimeDepInputs,
    FamilyInputs,
    FedFundsRepoInputs,
    ForeignDepInputs,
    OtherBorrowingInputs,
    OtherDomDepInputs,
)
from .config import EXPENSE_SIGN_NEGATIVE, IngestionConfig, TableSource
from .normalize import apply_money_scale, apply_rate_scale, to_float
from .tables import read_table

_RATE = "rate"
_BALANCE = "balance"
_SHARE = "share"
_MONTHS = "months"
_MONEY = "usd_per_quarter"

_PLAIN_FIELDS: dict[str, dict[str, str]] = {
    "ie_dom_time_dep": {"rate_launchpoint": _RATE, "wal_months": _MONTHS, "balance": _BALANCE},
    "ie_other_dom_dep": {"total_average_balance": _BALANCE},
    "ie_foreign_dep": {},
    "ie_fed_funds_repo": {"fed_funds_purchased_balance": _BALANCE, "repo_sold_balance": _BALANCE},
    "ie_other_borrowing": {"total_balance": _BALANCE, "cp_share": _SHARE, "subdebt_share": _SHARE},
    # Interest-income models (asset side) share the same two-sheet contract and
    # registry; one physical spot/quarterly sheet pair serves both families, and
    # each loader consumes only its own rows.
    "ii_dep_banks_other": {"balance": _BALANCE},
    "ii_other_ida": {"total_balance": _BALANCE, "short_rate_share": _SHARE},
    # nii_trading_al (Increment 4, PID-TRD-2): the Schedule G trading assets /
    # trading liabilities average balances at the launch point (reference cells
    # "14Q Sch G" R30 / R112; the Fed names the worksheet but no line items).
    "nii_trading_al": {
        "trading_assets_avg_balance": _BALANCE,
        "trading_liabilities_avg_balance": _BALANCE,
    },
    "family": {},
}
_SUBCOMPONENT_FIELDS: dict[str, str] = {"rate_launchpoint": _RATE, "balance": _BALANCE, "elb_spread": _RATE}
_MODEL_SUBCOMPONENTS: dict[str, tuple[str, ...]] = {
    "ie_other_dom_dep": OTHER_DOM_SUBCOMPONENTS,
    "ie_foreign_dep": FOREIGN_SUBCOMPONENTS,
}
_QUARTERLY_FIELDS: dict[tuple[str, str], str] = {
    ("family", "frb_total_interest_expense"): _MONEY,   # required — PID-OB-5 calibration target
    ("family", "frb_total_interest_income"): _MONEY,    # optional — future asset-side counterpart
    ("family", "frb_net_interest_income"): _MONEY,      # optional — enables the NII = II − IE wiring guard
}
_PQ_COLUMNS: tuple[str, ...] = tuple(f"PQ{q}" for q in PROJECTION_QUARTERS)

_SpotKey = tuple[str, str, str | None]


def _cell(row: dict[str, object], column: str) -> str:
    raw = row.get(column)
    return "" if raw is None else str(raw).strip()


def _read_sheet(config: IngestionConfig, source: TableSource, *, role: str, required_columns: set[str]) -> tuple[Path, list[dict[str, object]]]:
    path = config.resolve(source.path)
    rows = read_table(path, source.sheet)
    if not rows:
        raise ValidationFailure(f"{path}: {role} sheet has no data rows")
    missing_columns = sorted(required_columns - set(rows[0].keys()))
    if missing_columns:
        raise ValidationFailure(
            f"{path}: {role} sheet is missing required columns {missing_columns} "
            f"(spot layout: model, field, subcomponent, scale, value; "
            f"quarterly layout: model, field, subcomponent, scale, PQ1..PQ9)"
        )
    return path, rows


def _is_spot_field(model: str, fld: str) -> bool:
    return fld in _PLAIN_FIELDS[model] or (model in _MODEL_SUBCOMPONENTS and fld in _SUBCOMPONENT_FIELDS)


def _parse_spot_rows(rows: list[dict[str, object]], path: Path) -> dict[_SpotKey, float]:
    values: dict[_SpotKey, float] = {}
    for line, row in enumerate(rows, start=2):
        model = _cell(row, "model")
        fld = _cell(row, "field")
        if not model and not fld:
            continue
        context = f"{path} row {line} ({model}.{fld})"
        if model not in _PLAIN_FIELDS:
            raise ValidationFailure(f"{context}: unknown model {model!r}; known: {sorted(_PLAIN_FIELDS)}")
        if (model, fld) in _QUARTERLY_FIELDS:
            raise ValidationFailure(
                f"{context}: {fld!r} is a quarterly path — it belongs in the quarterly sheet "
                f"(wide layout, columns PQ1..PQ9), not the spot sheet"
            )
        subcomponent = _cell(row, "subcomponent") or None
        scale = _cell(row, "scale") or None

        if model in _MODEL_SUBCOMPONENTS and fld in _SUBCOMPONENT_FIELDS:
            kind = _SUBCOMPONENT_FIELDS[fld]
            allowed = _MODEL_SUBCOMPONENTS[model]
            if subcomponent is None:
                raise ValidationFailure(f"{context}: subcomponent required (one of {list(allowed)})")
            if subcomponent not in allowed:
                raise ValidationFailure(f"{context}: unknown subcomponent {subcomponent!r} (one of {list(allowed)})")
        elif fld in _PLAIN_FIELDS[model]:
            kind = _PLAIN_FIELDS[model][fld]
            if subcomponent:
                raise ValidationFailure(f"{context}: subcomponent not allowed for {fld!r}")
        else:
            raise ValidationFailure(f"{context}: unknown field {fld!r} for model {model!r}")

        value = to_float(row.get("value"), context=context)
        if kind in (_RATE, _SHARE):
            value = apply_rate_scale(scale, value, context=context)
        elif kind in (_BALANCE, _MONEY):
            value = apply_money_scale(scale, value, context=context)
        elif scale:
            raise ValidationFailure(
                f"{context}: scale applies only to rate/spread/share and balance/money fields — "
                f"{kind!r} values are already canonical"
            )
        key: _SpotKey = (model, fld, subcomponent)
        if key in values:
            raise ValidationFailure(f"{context}: duplicate row for this input")
        values[key] = value
    return values


def _parse_quarterly_rows(rows: list[dict[str, object]], path: Path) -> dict[tuple[str, str], dict[int, float]]:
    series: dict[tuple[str, str], dict[int, float]] = {}
    for line, row in enumerate(rows, start=2):
        model = _cell(row, "model")
        fld = _cell(row, "field")
        if not model and not fld:
            continue
        context = f"{path} row {line} ({model}.{fld})"
        if model not in _PLAIN_FIELDS:
            raise ValidationFailure(f"{context}: unknown model {model!r}; known: {sorted(_PLAIN_FIELDS)}")
        key = (model, fld)
        if key not in _QUARTERLY_FIELDS:
            if _is_spot_field(model, fld):
                raise ValidationFailure(
                    f"{context}: {fld!r} is a one-time spot (launch-point) input — it belongs in "
                    f"the spot sheet, not the quarterly sheet"
                )
            known = sorted(f for m, f in _QUARTERLY_FIELDS if m == model)
            raise ValidationFailure(f"{context}: unknown quarterly field {fld!r} for model {model!r}; known: {known}")
        if _cell(row, "subcomponent"):
            raise ValidationFailure(f"{context}: subcomponent not allowed on {fld!r}")
        if key in series:
            raise ValidationFailure(f"{context}: duplicate row for this series")
        kind = _QUARTERLY_FIELDS[key]
        scale = _cell(row, "scale") or None
        values: dict[int, float] = {}
        for quarter in PROJECTION_QUARTERS:
            column = f"PQ{quarter}"
            if not _cell(row, column):
                raise ValidationFailure(
                    f"{context}: {column} is blank — a supplied quarterly row carries all nine "
                    f"quarters (fill PQ1..PQ9 or drop the row)"
                )
            value = to_float(row.get(column), context=f"{context} {column}")
            if kind == _MONEY:
                value = apply_money_scale(scale, value, context=f"{context} {column}")
            values[quarter] = value
        series[key] = values
    return series


def load_family_inputs(config: IngestionConfig) -> FamilyInputs:
    if config.firm_data is None:
        raise ValidationFailure("config has no [firm_data] section")
    if config.firm_data.spot is None or config.firm_data.quarterly is None:
        raise ValidationFailure(
            "config [firm_data] declares neither [firm_data.spot] nor [firm_data.quarterly] — "
            "the expense-family run needs the D-007 two-sheet contract (a loans-/securities-only "
            "config legitimately omits it, but then this loader cannot run)"
        )
    spot_path, spot_rows = _read_sheet(
        config, config.firm_data.spot, role="spot", required_columns={"model", "field", "value"}
    )
    quarterly_path, quarterly_rows = _read_sheet(
        config, config.firm_data.quarterly, role="quarterly", required_columns={"model", "field", *_PQ_COLUMNS}
    )
    values = _parse_spot_rows(spot_rows, spot_path)
    paths = _parse_quarterly_rows(quarterly_rows, quarterly_path)

    missing: list[str] = []

    def need(model: str, fld: str, subcomponent: str | None = None) -> float:
        key: _SpotKey = (model, fld, subcomponent)
        if key not in values:
            missing.append(f"{model}.{fld}" + (f"[{subcomponent}]" if subcomponent else ""))
            return 0.0
        return values[key]

    dom_time = {f: need("ie_dom_time_dep", f) for f in _PLAIN_FIELDS["ie_dom_time_dep"]}
    other_dom_subs = {
        sub: {f: need("ie_other_dom_dep", f, sub) for f in _SUBCOMPONENT_FIELDS}
        for sub in OTHER_DOM_SUBCOMPONENTS
    }
    # PID-ODD-3: optional — consistency-monitor reference only, never the expense multiplicand
    other_dom_total = values.get(("ie_other_dom_dep", "total_average_balance", None))
    foreign_subs = {
        sub: {f: need("ie_foreign_dep", f, sub) for f in _SUBCOMPONENT_FIELDS}
        for sub in FOREIGN_SUBCOMPONENTS
    }
    fed_funds = {f: need("ie_fed_funds_repo", f) for f in _PLAIN_FIELDS["ie_fed_funds_repo"]}
    other_borrowing = {f: need("ie_other_borrowing", f) for f in _PLAIN_FIELDS["ie_other_borrowing"]}
    frb_total = paths.get(("family", "frb_total_interest_expense"))
    if frb_total is None:
        missing.append("family.frb_total_interest_expense (quarterly sheet)")
        frb_total = {q: 0.0 for q in PROJECTION_QUARTERS}
    if missing:
        raise ValidationFailure(f"{spot_path}: missing required inputs: {', '.join(missing)}")

    if config.firm_data.frb_expense_sign == EXPENSE_SIGN_NEGATIVE:
        # D-008: source enters expense as negatives; canonical convention is
        # positive-magnitude expense, matching the five models' outputs.
        frb_total = {q: -value for q, value in frb_total.items()}

    firm_id = config.firm_data.firm_id
    return FamilyInputs(
        firm_id=firm_id,
        dom_time_dep=DomTimeDepInputs(firm_id, **dom_time),
        other_dom_dep=OtherDomDepInputs(
            firm_id,
            subcomponents={
                sub: DepositSubcomponent(fields["rate_launchpoint"], fields["balance"], fields["elb_spread"])
                for sub, fields in other_dom_subs.items()
            },
            total_average_balance=other_dom_total,
        ),
        foreign_dep=ForeignDepInputs(
            firm_id,
            subcomponents={
                sub: DepositSubcomponent(fields["rate_launchpoint"], fields["balance"], fields["elb_spread"])
                for sub, fields in foreign_subs.items()
            },
        ),
        fed_funds_repo=FedFundsRepoInputs(firm_id, **fed_funds),
        other_borrowing=OtherBorrowingInputs(firm_id, **other_borrowing),
        frb_total_interest_expense=frb_total,
        frb_total_interest_income=paths.get(("family", "frb_total_interest_income")),
        frb_net_interest_income=paths.get(("family", "frb_net_interest_income")),
    )


def load_income_inputs(config: IngestionConfig) -> IncomeFamilyInputs:
    """Income-family inputs from the same two-sheet contract.

    The spot sheet carries the Family A calculator inputs (required) and the
    `nii_trading_al` trading balances (optional as a pair — both rows or
    neither, PID-TRD-2; the income orchestrator requires them at run time).
    When [firm_data.quarterly] is declared, the FRB family income/NII paths are
    read from it (`frb_total_interest_income` — the PID-TRD-1 calibration
    target — and `frb_net_interest_income` for the combined-NII monitor); both
    pass through as-entered (D-008: only the expense path carries the sign
    setting, and that path stays on the expense-side family bundle)."""
    if config.firm_data is None:
        raise ValidationFailure("config has no [firm_data] section")
    if config.firm_data.spot is None:
        raise ValidationFailure(
            "config [firm_data] declares no [firm_data.spot] — the calculator-income run needs "
            "the D-007 spot sheet (a loans-/securities-only config legitimately omits it, but "
            "then this loader cannot run)"
        )
    spot_path, spot_rows = _read_sheet(
        config, config.firm_data.spot, role="spot", required_columns={"model", "field", "value"}
    )
    values = _parse_spot_rows(spot_rows, spot_path)

    missing: list[str] = []

    def need(model: str, fld: str) -> float:
        key: _SpotKey = (model, fld, None)
        if key not in values:
            missing.append(f"{model}.{fld}")
            return 0.0
        return values[key]

    dep_banks = {f: need("ii_dep_banks_other", f) for f in _PLAIN_FIELDS["ii_dep_banks_other"]}
    other_ida = {f: need("ii_other_ida", f) for f in _PLAIN_FIELDS["ii_other_ida"]}
    if missing:
        raise ValidationFailure(f"{spot_path}: missing required inputs: {', '.join(missing)}")

    # Trading balances: an optional PAIR — one row without the other is a hard
    # error (a lone leg would silently misstate the net), absence of both is a
    # legal calculator-only run (the orchestrator enforces presence at run time).
    trading_values = {
        fld: values.get(("nii_trading_al", fld, None)) for fld in _PLAIN_FIELDS["nii_trading_al"]
    }
    supplied = [fld for fld, value in trading_values.items() if value is not None]
    trading = None
    if supplied:
        absent = sorted(fld for fld, value in trading_values.items() if value is None)
        if absent:
            raise ValidationFailure(
                f"{spot_path}: nii_trading_al rows are a pair — got {sorted(supplied)} without "
                f"{absent}; supply both trading balances or neither (PID-TRD-2)"
            )

    paths: dict[tuple[str, str], dict[int, float]] = {}
    if config.firm_data.quarterly is not None:
        quarterly_path, quarterly_rows = _read_sheet(
            config, config.firm_data.quarterly, role="quarterly",
            required_columns={"model", "field", *_PQ_COLUMNS},
        )
        paths = _parse_quarterly_rows(quarterly_rows, quarterly_path)

    firm_id = config.firm_data.firm_id
    if supplied:
        trading = TradingNiiInputs(
            firm_id,
            trading_assets_avg_balance=trading_values["trading_assets_avg_balance"],
            trading_liabilities_avg_balance=trading_values["trading_liabilities_avg_balance"],
        )
    return IncomeFamilyInputs(
        firm_id=firm_id,
        dep_banks_other=DepBanksOtherInputs(firm_id, **dep_banks),
        other_ida=OtherIdaInputs(firm_id, **other_ida),
        trading=trading,
        frb_total_interest_income=paths.get(("family", "frb_total_interest_income")),
        frb_net_interest_income=paths.get(("family", "frb_net_interest_income")),
    )

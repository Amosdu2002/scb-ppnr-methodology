"""Canonical tidy-sheet firm-data loader.

Interchange layout — one row per input; extra columns are ignored:

    model, field, subcomponent, quarter, scale, value

Inside the company, a single workbook tab assembles these rows from the confidential
workbook with plain formulas; only that tidy table crosses this boundary, so no
sheet or cell reference ever appears in code. Scale rules (D-006): rate/spread/share
values declare `scale` percent | decimal; balances and dollar amounts declare `scale`
millions | billions and are normalized here to the canonical USD-millions unit
(Schedule G reports millions while the FRB projection paths arrive in billions —
mixing them undeclared would be silently absorbed into the α_b calibration); months
values leave `scale` blank (already canonical).

The Fed provides three firm-level projection paths (OQ-023, narrowed 2026-07-20):
interest income, total interest expense, and net interest income. Their quarterly rows
use model `family`, quarters 1..9: `frb_total_interest_expense` is REQUIRED (the
PID-OB-5 calibration target); `frb_total_interest_income` and `frb_net_interest_income`
are optional companions (all nine quarters or none) — no interest-expense model consumes
them, but when both accompany the expense path the NII = income − expense identity is
checked as a wiring guard. The physical file mapping remains to be confirmed inside the
company before reliance."""

from __future__ import annotations

from ..interest_expense.schemas import (
    FOREIGN_SUBCOMPONENTS,
    OTHER_DOM_SUBCOMPONENTS,
    PROJECTION_QUARTERS,
    DepositSubcomponent,
    DomTimeDepInputs,
    FamilyInputs,
    FedFundsRepoInputs,
    ForeignDepInputs,
    OtherBorrowingInputs,
    OtherDomDepInputs,
    ValidationFailure,
)
from .config import IngestionConfig
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

_Key = tuple[str, str, str | None, int | None]


def _cell(row: dict[str, object], column: str) -> str:
    raw = row.get(column)
    return "" if raw is None else str(raw).strip()


def _parse_rows(rows: list[dict[str, object]], path) -> dict[_Key, float]:
    values: dict[_Key, float] = {}
    for line, row in enumerate(rows, start=2):
        model = _cell(row, "model")
        fld = _cell(row, "field")
        if not model and not fld:
            continue
        context = f"{path} row {line} ({model}.{fld})"
        if model not in _PLAIN_FIELDS:
            raise ValidationFailure(f"{context}: unknown model {model!r}; known: {sorted(_PLAIN_FIELDS)}")
        subcomponent = _cell(row, "subcomponent") or None
        quarter_text = _cell(row, "quarter")
        scale = _cell(row, "scale") or None
        quarter: int | None = None

        if (model, fld) in _QUARTERLY_FIELDS:
            kind = _QUARTERLY_FIELDS[(model, fld)]
            if subcomponent:
                raise ValidationFailure(f"{context}: subcomponent not allowed on {fld!r}")
            if not quarter_text:
                raise ValidationFailure(f"{context}: quarterly field requires a quarter (1..9)")
            try:
                quarter = int(float(quarter_text))
            except ValueError:
                raise ValidationFailure(f"{context}: quarter {quarter_text!r} is not an integer") from None
            if quarter not in PROJECTION_QUARTERS:
                raise ValidationFailure(f"{context}: quarter must be 1..9, got {quarter}")
        elif model in _MODEL_SUBCOMPONENTS and fld in _SUBCOMPONENT_FIELDS:
            kind = _SUBCOMPONENT_FIELDS[fld]
            allowed = _MODEL_SUBCOMPONENTS[model]
            if subcomponent is None:
                raise ValidationFailure(f"{context}: subcomponent required (one of {list(allowed)})")
            if subcomponent not in allowed:
                raise ValidationFailure(f"{context}: unknown subcomponent {subcomponent!r} (one of {list(allowed)})")
            if quarter_text:
                raise ValidationFailure(f"{context}: quarter not allowed on launch-point fields")
        elif fld in _PLAIN_FIELDS[model]:
            kind = _PLAIN_FIELDS[model][fld]
            if subcomponent:
                raise ValidationFailure(f"{context}: subcomponent not allowed for {fld!r}")
            if quarter_text:
                raise ValidationFailure(f"{context}: quarter not allowed on launch-point fields")
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
        key: _Key = (model, fld, subcomponent, quarter)
        if key in values:
            raise ValidationFailure(f"{context}: duplicate row for this input")
        values[key] = value
    return values


def load_family_inputs(config: IngestionConfig) -> FamilyInputs:
    if config.firm_data is None:
        raise ValidationFailure("config has no [firm_data] section")
    source = config.firm_data.source
    path = config.resolve(source.path)
    rows = read_table(path, source.sheet)
    if not rows:
        raise ValidationFailure(f"{path}: no data rows")
    header = set(rows[0].keys())
    missing_columns = sorted({"model", "field", "value"} - header)
    if missing_columns:
        raise ValidationFailure(
            f"{path}: tidy sheet is missing required columns {missing_columns} "
            f"(layout: model, field, subcomponent, quarter, scale, value)"
        )

    values = _parse_rows(rows, path)
    missing: list[str] = []

    def need(model: str, fld: str, subcomponent: str | None = None, quarter: int | None = None) -> float:
        key: _Key = (model, fld, subcomponent, quarter)
        if key not in values:
            label = f"{model}.{fld}" + (f"[{subcomponent}]" if subcomponent else "") + (
                f" PQ{quarter}" if quarter is not None else ""
            )
            missing.append(label)
            return 0.0
        return values[key]

    dom_time = {f: need("ie_dom_time_dep", f) for f in _PLAIN_FIELDS["ie_dom_time_dep"]}
    other_dom_subs = {
        sub: {f: need("ie_other_dom_dep", f, sub) for f in _SUBCOMPONENT_FIELDS}
        for sub in OTHER_DOM_SUBCOMPONENTS
    }
    other_dom_total = need("ie_other_dom_dep", "total_average_balance")
    foreign_subs = {
        sub: {f: need("ie_foreign_dep", f, sub) for f in _SUBCOMPONENT_FIELDS}
        for sub in FOREIGN_SUBCOMPONENTS
    }
    fed_funds = {f: need("ie_fed_funds_repo", f) for f in _PLAIN_FIELDS["ie_fed_funds_repo"]}
    other_borrowing = {f: need("ie_other_borrowing", f) for f in _PLAIN_FIELDS["ie_other_borrowing"]}
    frb_total = {q: need("family", "frb_total_interest_expense", None, q) for q in PROJECTION_QUARTERS}
    if missing:
        raise ValidationFailure(f"{path}: missing required inputs: {', '.join(missing)}")

    def take_quarterly_optional(model: str, fld: str) -> dict[int, float] | None:
        present = {
            q: values[(model, fld, None, q)]
            for q in PROJECTION_QUARTERS
            if (model, fld, None, q) in values
        }
        if not present:
            return None
        absent = [q for q in PROJECTION_QUARTERS if q not in present]
        if absent:
            raise ValidationFailure(
                f"{path}: {model}.{fld} is partially supplied — missing quarters "
                f"{[f'PQ{q}' for q in absent]}; supply all nine quarters or none"
            )
        return present

    frb_income = take_quarterly_optional("family", "frb_total_interest_income")
    frb_net = take_quarterly_optional("family", "frb_net_interest_income")

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
        frb_total_interest_income=frb_income,
        frb_net_interest_income=frb_net,
    )

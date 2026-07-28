"""Typed ingestion configuration, parsed from TOML (stdlib `tomllib` — no dependency).

The company-local config file carries every physical detail: workbook paths, sheet
names, column names, unit scales, the launch-point quarter. This module only defines
the shape. Relative paths resolve against the config file's own directory, so a
config plus its data folder travels as a unit. Template with placeholders:
`config/company.template.toml` — the filled copy stays company-local (gitignored
`config/local/`) and never enters a public repository."""

from __future__ import annotations

import tomllib
from dataclasses import dataclass, field, fields
from pathlib import Path
from types import MappingProxyType
from typing import Mapping

from ..core.schemas import ValidationFailure

SERIES_KIND_RATE = "rate"    # scale-normalized to annualized decimal (scale required)
SERIES_KIND_LEVEL = "level"  # taken as-is, e.g. an index level (scale must be absent)

EXPENSE_SIGN_POSITIVE = "positive"  # expense path entered as positive magnitudes (canonical)
EXPENSE_SIGN_NEGATIVE = "negative"  # expense path entered as negative amounts (FRB file convention, D-008)


@dataclass(frozen=True)
class TableSource:
    path: Path
    sheet: str | None = None


@dataclass(frozen=True)
class ScenarioSource:
    """One MEV scenario. `label` identifies this scenario's PQ1..PQ9 rows in a
    long-format file (a scenario-name column); None for one-scenario-per-sheet files."""

    path: Path
    sheet: str | None = None
    label: str | None = None


@dataclass(frozen=True)
class SeriesSpec:
    column: str
    scale: str | None = None
    kind: str = SERIES_KIND_RATE


@dataclass(frozen=True)
class MevConfig:
    date_column: str
    launch_point: str                       # PQ0 label, e.g. "2025Q4" (D-005; the jump-off quarter)
    scenarios: Mapping[str, ScenarioSource]
    series: Mapping[str, SeriesSpec]
    scenario_name_column: str | None = None  # long-format files: column naming each row's scenario
    actuals_label: str = "Actual"            # label on history + launch-point (PQ0) rows


@dataclass(frozen=True)
class SecuritiesEnrichmentSheet:
    """One enrichment tab of the securities workbook (PID-SEC-6): per-security
    maturity/coupon/rate-type/floor/WAL keyed by CUSIP or ISIN. Column names are
    per-tab (the physical tabs spell headers differently); `header_row` is the
    1-based row carrying those names."""

    sheet: str
    key_column: str
    maturity_column: str
    coupon_column: str
    rate_type_column: str
    wal_column: str
    floor_column: str | None = None
    floater_indicator_column: str | None = None   # optional Y/N cross-check vs rate_type (monitor)
    header_row: int = 1


# PID-SEC-2 floor modes (mirrored from interest_income.securities_schemas —
# config stays free of model imports; the loader re-validates against the model set).
# "security_floor_else_zero" (2026-07-24) is the reference-workbook rule: every
# floater floored at its security floor when on file, else at 0.
_FLOOR_MODES = ("zero", "security_floor", "none", "security_floor_else_zero")
# PID-SEC-10 floating projection modes (mirrored): "neg_hold" holds negative-margin
# floaters at the launch coupon; "neg_hold_blend13" adds the monthly-reset PQ1 blend;
# "blend13" = the PQ1 blend WITHOUT the hold; "flat_c0" holds every floater flat.
_FLOAT_PROJECTION_MODES = ("spot", "neg_hold", "neg_hold_blend13", "blend13", "flat_c0", "freeze1")
# PID-SEC-13 blank-amortized-cost treatments (see SecuritiesConfig.missing_ac_mode).
_MISSING_AC_MODES = ("price_proxy_no_accretion", "price_proxy_accrete", "zero_accrete")


@dataclass(frozen=True)
class SecuritiesConfig:
    """The securities workbook contract (PID-SEC-6): a Schedule B.1-layout
    positions sheet, optional prepayment pivot sheet (PID-MBS-1), and enrichment
    tabs. All scales are declared, never guessed (D-006); `floor_mode` selects
    the PID-SEC-2 negative-margin treatment."""

    workbook: Path
    positions_sheet: str
    money_scale: str
    coupon_scale: str
    book_yield_scale: str
    floor_mode: str
    prepayment_sheet: str | None = None
    enrichment: tuple[SecuritiesEnrichmentSheet, ...] = ()
    price_mdrm: str = "CQSCJH21"        # PID-SEC-3 price column MDRM; override if the workbook differs.
                                        # Fallback: a header cell whose technical name is exactly "Price"
    on_security_error: str = "stop"     # "stop" (strict default) | "skip" — skip mode isolates a
                                        # failing security with a HIGHLIGHT warning instead of
                                        # halting the run (debugging/company-reference phase)
    reinvest_paydowns: bool = True      # MRM p. 72: paydown proceeds reinvest like maturities
                                        # (default ON); toggle for A/B against the reference
    # PID-SEC-9 (2026-07-24): optional positions-sheet technical columns — the
    # reference workbook's own model-input columns on the MDRM header row.
    # Header names are exact cell text (e.g. "Maturity (yr)"). All three carry
    # DECIMAL rates / decimal years (no scale applied). Precedence: maturity
    # date (enrichment) stays primary, the years column is the fallback;
    # enrichment coupon stays primary, the coupon column fills blanks; the
    # floor column is PREFERRED over the enrichment floor when non-blank.
    positions_maturity_years_column: str | None = None
    positions_coupon_column: str | None = None
    positions_floor_column: str | None = None
    positions_rate_type_column: str | None = None   # the sheet's own float/fixed indicator —
                                                    # verification-only (bake-off + monitor);
                                                    # ITO rate type still drives the models
    # PID-SEC-10 (2026-07-27): floating-coupon projection mode — "spot" (original) |
    # "neg_hold" (negative margin → launch coupon held flat) | "neg_hold_blend13"
    # (neg_hold + monthly-reset PQ1 blend) | "blend13" (PQ1 blend, no hold) |
    # "flat_c0" (every floater held at the launch coupon). The reference treats
    # categories differently (2026-07-27 bake-off) — `floating_projection_overrides`
    # maps SECURITY_DESCRIPTION_1 categories to modes, overriding the default.
    floating_projection: str = "spot"
    floating_projection_overrides: Mapping[str, str] = field(default_factory=dict)
    # PID-SEC-11 (2026-07-27): categories whose securities accrue at BOOK YIELD
    # instead of the coupon (reference-identified for Municipal Bond: floaters match
    # book-yield-flat exactly; fixed implied multiplier constant at BY/coupon).
    # Zero-coupon rows are never affected; missing book yield falls back to coupon.
    book_yield_categories: tuple[str, ...] = ()
    # OQ-030 (2026-07-27): which maturity feeds the PID-SEC-8 AA denominator —
    # "enrichment_first" (ITO maturity date ÷ 365, positions years column as
    # fallback; the original order) | "positions_first" (the sheet's own
    # "Maturity (yr)" column primary — the reference's actual divisor, which for
    # callable munis can be the call-adjusted maturity — ITO date as fallback).
    maturity_source: str = "enrichment_first"
    # PID-SEC-12 (2026-07-27, user-directed to match the reference): categories
    # whose ZERO-COUPON rows book NO accretion (reference GII blank for sovereign
    # ZCBs). The Fed-stated A42 accretion is preserved as [FACT]; this switch
    # records the reference divergence. Coupon rows are never affected.
    zcb_no_accretion_categories: tuple[str, ...] = ()
    # PID-SEC-14 (2026-07-28, reference-verified): categories computed by the
    # PRINTED Equation A42 — income(q) = AmortizedCost × BookYield / 4, constant,
    # with no separate accretion leg. Municipal Bond matched 20 reference rows to
    # within book-yield display rounding (the same amount against FACE is out by
    # up to 29%). Recommended: ["Municipal Bond"].
    a42_collapsed_categories: tuple[str, ...] = ()
    # PID-SEC-13 (2026-07-28, user-directed): treatment of a BLANK amortized cost
    # on rows that are NOT genuine unsettled trades — "price_proxy_no_accretion"
    # (the original PID-SEC-3 behavior; default, so numbers never move silently) |
    # "price_proxy_accrete" (price proxy, accretion runs) | "zero_accrete" (blank
    # read as zero and accreted — what the reference workbook does).
    # `unsettled_window_days` scopes the ORIGINAL PID-SEC-3 treatment to rows whose
    # PURCHASE_DATE (CQSCP095) is within that many days of the report date; those
    # always take the price proxy with accretion suppressed, whatever the mode.
    # With no purchase-date column on the sheet, no row can be classified as
    # near-settle and every blank-AC row follows `missing_ac_mode`.
    missing_ac_mode: str = "price_proxy_no_accretion"
    unsettled_window_days: int = 7
    # PID-SEC-13 amendment (2026-07-28): the reference does NOT treat blank
    # amortized costs uniformly — one Agency MBS row accretes the whole face
    # while ten CLO rows carrying the same blank book NO income at all. So the
    # mode is per-category, exactly like `floating_projection_overrides`; a
    # global setting is what turned the Agency fix into a CLO regression.
    missing_ac_mode_overrides: Mapping[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class FirmDataConfig:
    """Two-sheet firm-input contract (D-007): `spot` holds one-time launch-point
    scalars (no quarter dimension), `quarterly` holds PQ1..PQ9 paths in wide layout
    (one row per series, columns PQ1..PQ9). CSV sources use two files; XLSX sources
    typically use two tabs of one workbook. `frb_expense_sign` (D-008) declares how
    the FRB total-interest-expense path is entered — "negative" makes the loader
    negate it to the canonical positive-magnitude convention. `securities` adds the
    PID-SEC-6 securities workbook (Increment 2, asset side)."""

    firm_id: str
    spot: TableSource
    quarterly: TableSource
    frb_expense_sign: str = EXPENSE_SIGN_POSITIVE
    securities: SecuritiesConfig | None = None


@dataclass(frozen=True)
class IngestionConfig:
    base_dir: Path
    mev: MevConfig | None = None
    firm_data: FirmDataConfig | None = None

    def resolve(self, path: Path | str) -> Path:
        candidate = Path(path)
        return candidate if candidate.is_absolute() else self.base_dir / candidate


def _require(section: Mapping[str, object], key: str, context: str) -> object:
    if key not in section:
        raise ValidationFailure(f"config {context}: missing required key {key!r}")
    return section[key]


def _table_source(section: Mapping[str, object], context: str) -> TableSource:
    path = str(_require(section, "path", context))
    sheet = section.get("sheet")
    return TableSource(path=Path(path), sheet=str(sheet) if sheet is not None else None)


def _reject_misplaced_key(table: str, key: str) -> None:
    """Catch the TOML scoping trap before it surfaces as a nonsense mode error.

    Once `[firm_data.securities.<table>]` opens, every bare key after it belongs
    to THAT table — so a scalar setting appended at the end of the file silently
    becomes an override entry, and the mode validator then complains that a
    setting name is not a valid mode. If an override key is itself the name of a
    securities setting, that is what happened."""
    if key in {f.name for f in fields(SecuritiesConfig)}:
        raise ValidationFailure(
            f"config [firm_data.securities.{table}]: {key!r} is a [firm_data.securities] SETTING, "
            f"not a security category. In TOML every bare key after a [table] header belongs to "
            f"that table, so {key!r} was written below [firm_data.securities.{table}] instead of "
            f"above it. Move the {key} = ... line up, so it sits with the other scalar settings "
            f"BEFORE any [firm_data.securities.*] sub-table or [[...enrichment]] block."
        )


def load_config(path: Path | str) -> IngestionConfig:
    path = Path(path)
    if not path.exists():
        raise ValidationFailure(f"config file not found: {path}")
    with path.open("rb") as handle:
        raw = tomllib.load(handle)

    mev: MevConfig | None = None
    if "mev" in raw:
        section = raw["mev"]
        scenario_name_column = section.get("scenario_name_column")
        scenarios: dict[str, ScenarioSource] = {}
        for name, entry in section.get("scenarios", {}).items():
            base = _table_source(entry, f"[mev.scenarios.{name}]")
            label = entry.get("label")
            scenarios[name] = ScenarioSource(
                path=base.path, sheet=base.sheet, label=str(label) if label is not None else None
            )
            if scenario_name_column and scenarios[name].label is None:
                raise ValidationFailure(
                    f"config [mev.scenarios.{name}]: 'label' is required when [mev].scenario_name_column is set"
                )
            if not scenario_name_column and scenarios[name].label is not None:
                raise ValidationFailure(
                    f"config [mev.scenarios.{name}]: 'label' is set but [mev].scenario_name_column is not — "
                    f"set scenario_name_column to the header of the scenario-name column"
                )
        if not scenarios:
            raise ValidationFailure("config [mev]: at least one [mev.scenarios.<id>] entry is required")
        series: dict[str, SeriesSpec] = {}
        for name, entry in section.get("series", {}).items():
            kind = str(entry.get("kind", SERIES_KIND_RATE))
            if kind not in (SERIES_KIND_RATE, SERIES_KIND_LEVEL):
                raise ValidationFailure(
                    f"config [mev.series.{name}]: kind must be '{SERIES_KIND_RATE}' or '{SERIES_KIND_LEVEL}', got {kind!r}"
                )
            scale = entry.get("scale")
            series[name] = SeriesSpec(
                column=str(_require(entry, "column", f"[mev.series.{name}]")),
                scale=str(scale) if scale is not None else None,
                kind=kind,
            )
        if not series:
            raise ValidationFailure("config [mev]: at least one [mev.series.<name>] entry is required")
        mev = MevConfig(
            date_column=str(_require(section, "date_column", "[mev]")),
            launch_point=str(_require(section, "launch_point", "[mev]")),
            scenarios=MappingProxyType(scenarios),
            series=MappingProxyType(series),
            scenario_name_column=str(scenario_name_column) if scenario_name_column is not None else None,
            actuals_label=str(section.get("actuals_label", "Actual")),
        )

    firm_data: FirmDataConfig | None = None
    if "firm_data" in raw:
        section = raw["firm_data"]
        for sub in ("spot", "quarterly"):
            if sub not in section:
                raise ValidationFailure(
                    f"config [firm_data]: missing [firm_data.{sub}] — the firm-input contract is "
                    f"two sheets (D-007): 'spot' for launch-point scalars, 'quarterly' for wide "
                    f"PQ1..PQ9 paths"
                )
        frb_expense_sign = str(section.get("frb_expense_sign", EXPENSE_SIGN_POSITIVE)).strip().lower()
        if frb_expense_sign not in (EXPENSE_SIGN_POSITIVE, EXPENSE_SIGN_NEGATIVE):
            raise ValidationFailure(
                f"config [firm_data]: frb_expense_sign must be '{EXPENSE_SIGN_POSITIVE}' or "
                f"'{EXPENSE_SIGN_NEGATIVE}', got {section.get('frb_expense_sign')!r} (D-008)"
            )
        securities: SecuritiesConfig | None = None
        if "securities" in section:
            sec = section["securities"]
            floor_mode = str(_require(sec, "floor_mode", "[firm_data.securities]")).strip().lower()
            if floor_mode not in _FLOOR_MODES:
                raise ValidationFailure(
                    f"config [firm_data.securities]: floor_mode must be one of {_FLOOR_MODES} "
                    f"(PID-SEC-2), got {sec.get('floor_mode')!r}"
                )
            enrichment: list[SecuritiesEnrichmentSheet] = []
            for index, entry in enumerate(sec.get("enrichment", [])):
                context = f"[[firm_data.securities.enrichment]] #{index + 1}"
                floor_column = entry.get("floor_column")
                floater_column = entry.get("floater_indicator_column")
                enrichment.append(
                    SecuritiesEnrichmentSheet(
                        sheet=str(_require(entry, "sheet", context)),
                        key_column=str(_require(entry, "key_column", context)),
                        maturity_column=str(_require(entry, "maturity_column", context)),
                        coupon_column=str(_require(entry, "coupon_column", context)),
                        rate_type_column=str(_require(entry, "rate_type_column", context)),
                        wal_column=str(_require(entry, "wal_column", context)),
                        floor_column=str(floor_column) if floor_column is not None else None,
                        floater_indicator_column=str(floater_column) if floater_column is not None else None,
                        header_row=int(entry.get("header_row", 1)),
                    )
                )
            prepayment_sheet = sec.get("prepayment_sheet")
            securities = SecuritiesConfig(
                workbook=Path(str(_require(sec, "workbook", "[firm_data.securities]"))),
                positions_sheet=str(_require(sec, "positions_sheet", "[firm_data.securities]")),
                money_scale=str(_require(sec, "money_scale", "[firm_data.securities]")),
                coupon_scale=str(_require(sec, "coupon_scale", "[firm_data.securities]")),
                book_yield_scale=str(_require(sec, "book_yield_scale", "[firm_data.securities]")),
                floor_mode=floor_mode,
                prepayment_sheet=str(prepayment_sheet) if prepayment_sheet is not None else None,
                enrichment=tuple(enrichment),
                price_mdrm=str(sec.get("price_mdrm", "CQSCJH21")),
                on_security_error=str(sec.get("on_security_error", "stop")).strip().lower(),
                reinvest_paydowns=bool(sec.get("reinvest_paydowns", True)),
                positions_maturity_years_column=(
                    str(sec["positions_maturity_years_column"]) if "positions_maturity_years_column" in sec else None
                ),
                positions_coupon_column=(
                    str(sec["positions_coupon_column"]) if "positions_coupon_column" in sec else None
                ),
                positions_floor_column=(
                    str(sec["positions_floor_column"]) if "positions_floor_column" in sec else None
                ),
                positions_rate_type_column=(
                    str(sec["positions_rate_type_column"]) if "positions_rate_type_column" in sec else None
                ),
                floating_projection=str(sec.get("floating_projection", "spot")).strip().lower(),
                floating_projection_overrides=MappingProxyType({
                    str(category): str(mode).strip().lower()
                    for category, mode in sec.get("floating_projection_overrides", {}).items()
                }),
                book_yield_categories=tuple(str(c) for c in sec.get("book_yield_categories", [])),
                maturity_source=str(sec.get("maturity_source", "enrichment_first")).strip().lower(),
                zcb_no_accretion_categories=tuple(str(c) for c in sec.get("zcb_no_accretion_categories", [])),
                a42_collapsed_categories=tuple(str(c) for c in sec.get("a42_collapsed_categories", [])),
                missing_ac_mode=str(sec.get("missing_ac_mode", "price_proxy_no_accretion")).strip().lower(),
                unsettled_window_days=int(sec.get("unsettled_window_days", 7)),
                missing_ac_mode_overrides=MappingProxyType({
                    str(category): str(mode).strip().lower()
                    for category, mode in sec.get("missing_ac_mode_overrides", {}).items()
                }),
            )
            if securities.missing_ac_mode not in _MISSING_AC_MODES:
                raise ValidationFailure(
                    f"config [firm_data.securities]: missing_ac_mode must be one of {_MISSING_AC_MODES} "
                    f"(PID-SEC-13), got {sec.get('missing_ac_mode')!r}"
                )
            for category, mode in securities.missing_ac_mode_overrides.items():
                _reject_misplaced_key("missing_ac_mode_overrides", category)
                if mode not in _MISSING_AC_MODES:
                    raise ValidationFailure(
                        f"config [firm_data.securities.missing_ac_mode_overrides]: mode for {category!r} "
                        f"must be one of {_MISSING_AC_MODES} (PID-SEC-13), got {mode!r}"
                    )
            if securities.unsettled_window_days < 0:
                raise ValidationFailure(
                    f"config [firm_data.securities]: unsettled_window_days must be >= 0 (PID-SEC-13), "
                    f"got {sec.get('unsettled_window_days')!r}"
                )
            if securities.maturity_source not in ("enrichment_first", "positions_first"):
                raise ValidationFailure(
                    f"config [firm_data.securities]: maturity_source must be 'enrichment_first' or "
                    f"'positions_first' (OQ-030), got {sec.get('maturity_source')!r}"
                )
            if securities.floating_projection not in _FLOAT_PROJECTION_MODES:
                raise ValidationFailure(
                    f"config [firm_data.securities]: floating_projection must be one of "
                    f"{_FLOAT_PROJECTION_MODES} (PID-SEC-10), got {sec.get('floating_projection')!r}"
                )
            for category, mode in securities.floating_projection_overrides.items():
                _reject_misplaced_key("floating_projection_overrides", category)
                if mode not in _FLOAT_PROJECTION_MODES:
                    raise ValidationFailure(
                        f"config [firm_data.securities.floating_projection_overrides]: mode for "
                        f"{category!r} must be one of {_FLOAT_PROJECTION_MODES} (PID-SEC-10), got {mode!r}"
                    )
            if securities.on_security_error not in ("stop", "skip"):
                raise ValidationFailure(
                    f"config [firm_data.securities]: on_security_error must be 'stop' or 'skip', "
                    f"got {sec.get('on_security_error')!r}"
                )
        firm_data = FirmDataConfig(
            firm_id=str(_require(section, "firm_id", "[firm_data]")),
            spot=_table_source(section["spot"], "[firm_data.spot]"),
            quarterly=_table_source(section["quarterly"], "[firm_data.quarterly]"),
            frb_expense_sign=frb_expense_sign,
            securities=securities,
        )

    return IngestionConfig(base_dir=path.parent.resolve(), mev=mev, firm_data=firm_data)

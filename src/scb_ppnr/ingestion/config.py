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
from ..interest_income.loans_schemas import (
    FLOOR_COLLAPSES,
    ORIG_DATE_STATISTICS,
    check_quarter_label,
)
from .loans_loader import LoansSheetSpec

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
    margin_column: str | None = None              # PID-SEC-17: enrichment-tab margin, if it lives there
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
_FLOAT_PROJECTION_MODES = ("spot", "neg_hold", "neg_hold_blend13", "blend13", "flat_c0", "freeze1",
                            "pos_hold", "pos_hold_blend13")
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
    positions_margin_column: str | None = None      # PID-SEC-17: the sheet's own MARGIN column
                                                    # (decimal spread over the index). Where present
                                                    # it replaces the c0 - 3M(0) imputation.
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
    # PID-SEC-15 (2026-07-28, reference-observed on Sovereign Bond): how many
    # quarters a security accrues. 'ceil' (default, unchanged) books
    # ceil(4 x maturity_years); 'floor' books only FULL quarters. Reference rows
    # with 4 x years = 3.233 accrue 3 quarters and 2.773 accrue 2 -- i.e. floor.
    # Global switch, so A/B it: the Agency MBS WAL-as-maturity path (PID-SEC-7)
    # keeps ceil either way, since those rows already end too EARLY.
    maturity_quarters_rounding: str = "ceil"
    # Per-category override (2026-07-28). Applying floor GLOBALLY was a regression:
    # it fixed Sovereign Bond (fixed rows went to xr/ref 1.0006) but cost US
    # Treasuries 544 USD mm (0.9985 -> 0.9766, 181 rows newly truncating) because
    # their maturity_quarters also feeds the Eq A40 straight-line DENOMINATOR.
    # Only Sovereign Bond is evidenced; keep the global default at ceil.
    maturity_quarters_rounding_overrides: Mapping[str, str] = field(default_factory=dict)
    # PID-SEC-16 (2026-07-28): for Agency MBS carrying a vendor prepayment face
    # path, let that PATH decide how long the security lives instead of the
    # PID-SEC-7 WAL-as-maturity. A WAL is an average life, not a maturity: a
    # pass-through with WAL 1.5y has a legal maturity decades out and the vendor
    # path still carries balance at PQ9, yet we currently zero it at ceil(4xWAL).
    # The reference zeroes a face only when the security actually MATURES, so
    # these rows should not stop at all. Default False (unchanged).
    agency_face_path_survival: bool = False
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
    spot: TableSource | None = None
    quarterly: TableSource | None = None
    frb_expense_sign: str = EXPENSE_SIGN_POSITIVE
    securities: SecuritiesConfig | None = None
    loans: "LoansConfig | None" = None


@dataclass(frozen=True)
class LoansConfig:
    """The `[firm_data.loans]` section: one workbook, every sheet name, header
    row and column header in config (PID-LOAN-8) — nothing is passed as a CLI
    path. `spec` carries the physical binding; `scenario` names the MEV
    projection block exactly as the sheet spells it (history rows are matched
    separately, under the spec's `mev_history_scenario`, default `Actual`);
    `launch_point` is the PQ0 calendar quarter and is REQUIRED because it is
    tied to the data vintage, not a stable default; `floor_collapse` is the one
    methodology switch (PID-LOAN-7)."""

    spec: LoansSheetSpec
    scenario: str
    launch_point: str
    floor_collapse: str
    apply_scalar: bool = True   # false = reference-matching runs: the workbook's own
                                # results carry NO industry scalar (verified 2026-08-12:
                                # the grand total is the plain sum of the blocks)
    engine: str = "pid"              # "pid" = the PID-registered construction; "reference" =
                                # the workbook's cell formulas (2026-08-12): per LOCOM side,
                                # Fixed = M.1(side) x out-share(v1) x A38 floored at 0;
                                # Variable = M.1(side) x out-share(v2+v3) x max(floor, base +
                                # FLOATING spread), floor = out-weighted incl blanks-as-zero;
                                # Total = (F + V) x Table A8. Use share_basis =
                                # "utilized" (no extra columns needed)
    balance_source: str = "m1"       # Equation A32 multiplicand: "m1" (share x M.1 category
                                # balance) or "h1_sum" (the segment's own H.1 exposure sum,
                                # no M.1 normalization — the reference workbook sums
                                # Committed Exposure Global per reference key directly,
                                # user cell-reading 2026-08-12)
    share_basis: str = "committed"   # which column weights segment shares, balances, floors
                                # and the wt denominator: "committed" (the original flagged
                                # choice), "utilized" (Utilized Exposure Global — the
                                # workbook's "Launchpoint Outstanding Balance" IS the sum
                                # of this column over a segment's reference keys,
                                # user-clarified 2026-08-12), or "outstanding" (a separate
                                # per-row column, if an extract ever carries one)
    cre_orig_date_statistic: str = "weighted_mean"
                                # PID-LOAN-22 (CRE only): the workbook weights origination
                                # dates by OUTSTANDING balance; whether its statistic is a
                                # median or a mean is a cell-formula detail still unread.
                                # "weighted_mean" (default — the sheet carries a sumproduct
                                # column, direct evidence of a mean) | "weighted_median".
                                # The CRE compare settles it. Corporate is unaffected
                                # (PID-LOAN-4's unweighted median stands there).


_LOANS_RUN_KEYS = ("workbook", "scenario", "launch_point", "floor_collapse", "apply_scalar", "share_basis", "balance_source", "engine", "cre_orig_date_statistic")


def _parse_loans(section: Mapping[str, object], base_dir: Path) -> LoansConfig:
    context = "[firm_data.loans]"
    spec_fields = {f.name: f for f in fields(LoansSheetSpec)}

    workbook = Path(str(_require(section, "workbook", context)))
    if not workbook.is_absolute():
        workbook = base_dir / workbook

    launch_point = check_quarter_label(
        f"config {context}: launch_point",
        str(_require(section, "launch_point", context)),
    )
    scenario = str(section.get("scenario", "Supervisory Severely Adverse"))
    apply_scalar = section.get("apply_scalar", True)
    if not isinstance(apply_scalar, bool):
        raise ValidationFailure(f"config {context}: apply_scalar must be true or false, got {apply_scalar!r}")
    engine = str(section.get("engine", "pid")).strip().lower()
    if engine not in ("pid", "reference"):
        raise ValidationFailure(
            f"config {context}: engine must be 'pid' or 'reference', got {section.get('engine')!r}"
        )
    balance_source = str(section.get("balance_source", "m1")).strip().lower()
    if balance_source not in ("m1", "h1_sum"):
        raise ValidationFailure(
            f"config {context}: balance_source must be 'm1' or 'h1_sum', "
            f"got {section.get('balance_source')!r}"
        )
    share_basis = str(section.get("share_basis", "committed")).strip().lower()
    if share_basis not in ("committed", "utilized", "outstanding"):
        raise ValidationFailure(
            f"config {context}: share_basis must be 'committed', 'utilized', or 'outstanding', "
            f"got {section.get('share_basis')!r}"
        )
    floor_collapse = str(section.get("floor_collapse", "balance_weighted")).strip().lower()
    if floor_collapse not in FLOOR_COLLAPSES:
        raise ValidationFailure(
            f"config {context}: floor_collapse must be one of {FLOOR_COLLAPSES} "
            f"(PID-LOAN-7), got {section.get('floor_collapse')!r}"
        )
    cre_orig_date_statistic = str(
        section.get("cre_orig_date_statistic", "weighted_mean")
    ).strip().lower()
    if cre_orig_date_statistic not in ORIG_DATE_STATISTICS:
        raise ValidationFailure(
            f"config {context}: cre_orig_date_statistic must be one of {ORIG_DATE_STATISTICS} "
            f"(PID-LOAN-22), got {section.get('cre_orig_date_statistic')!r}"
        )

    spec_kwargs: dict[str, object] = {"workbook": workbook}
    for key, value in section.items():
        if key in _LOANS_RUN_KEYS:
            continue
        if key not in spec_fields or key == "workbook":
            raise ValidationFailure(
                f"config {context}: unknown key {key!r}. Valid keys: "
                f"{sorted((*_LOANS_RUN_KEYS, *(n for n in spec_fields if n != 'workbook')))}. "
                f"Refused rather than ignored, so a typo'd sheet name can never look "
                f"configured while the default quietly loads instead."
            )
        default = spec_fields[key].default
        if isinstance(default, bool):
            raise ValidationFailure(f"config {context}: {key!r} is not configurable")
        if isinstance(default, int):
            spec_kwargs[key] = int(value)  # type: ignore[call-overload]
        elif isinstance(default, tuple):
            if not isinstance(value, (list, tuple)):
                raise ValidationFailure(
                    f"config {context}: {key} must be an array of 1-based column numbers"
                )
            spec_kwargs[key] = tuple(int(v) for v in value)
        else:
            spec_kwargs[key] = str(value)

    return LoansConfig(
        spec=LoansSheetSpec(**spec_kwargs),  # type: ignore[arg-type]
        scenario=scenario,
        launch_point=launch_point,
        floor_collapse=floor_collapse,
        apply_scalar=bool(apply_scalar),
        share_basis=share_basis,
        balance_source=balance_source,
        engine=engine,
        cre_orig_date_statistic=cre_orig_date_statistic,
    )


@dataclass(frozen=True)
class IngestionConfig:
    base_dir: Path
    mev: MevConfig | None = None
    firm_data: FirmDataConfig | None = None
    provenance: Mapping[str, str] = field(default_factory=dict)

    def resolve(self, path: Path | str) -> Path:
        candidate = Path(path)
        return candidate if candidate.is_absolute() else self.base_dir / candidate


INCLUDE_KEY = "include"
_ALLOWED_TOP_LEVEL = frozenset({INCLUDE_KEY, "mev", "firm_data"})


def _merge_into(
    base: dict[str, object],
    incoming: Mapping[str, object],
    provenance: dict[str, str],
    source: str,
    prefix: str = "",
) -> None:
    """Deep-merge `incoming` into `base`, recording where every leaf came from.

    Tables merge recursively so one logical table can be assembled from several
    files — the methodology switches for `[firm_data.securities]` live in a
    committed file while its workbook path lives in the gitignored local one.

    A LEAF (scalar, array, or array-of-tables) defined in two files is a HARD
    ERROR naming both, never a last-wins override. Silent precedence is the
    failure mode this project keeps paying for: a value that looks set, is set,
    and is not the one in effect."""
    for key, value in incoming.items():
        path = f"{prefix}{key}"
        if isinstance(value, dict) and isinstance(base.get(key), dict):
            _merge_into(base[key], value, provenance, source, prefix=f"{path}.")  # type: ignore[arg-type]
            continue
        if key in base:
            raise ValidationFailure(
                f"config: {path!r} is defined in two files — {provenance.get(path, '<unknown>')} "
                f"and {source}. Duplicate keys are refused rather than silently overridden; "
                f"delete one of the two definitions."
            )
        base[key] = value
        if isinstance(value, dict):
            _record_subtree(value, provenance, source, prefix=f"{path}.")
        provenance[path] = source


def _record_subtree(
    table: Mapping[str, object], provenance: dict[str, str], source: str, prefix: str
) -> None:
    for key, value in table.items():
        path = f"{prefix}{key}"
        provenance[path] = source
        if isinstance(value, dict):
            _record_subtree(value, provenance, source, prefix=f"{path}.")


def _read_toml(path: Path) -> dict[str, object]:
    if not path.exists():
        raise ValidationFailure(f"config file not found: {path}")
    with path.open("rb") as handle:
        return tomllib.load(handle)


def compose_config(path: Path) -> tuple[dict[str, object], dict[str, str]]:
    """Read a config file, resolving an `include = [...]` manifest one level deep.

    Returns the merged mapping plus a leaf-path -> source-file provenance map.
    Included paths resolve against the manifest's own directory, and are merged
    in listed order before the manifest's own keys. An included file may not
    itself include: one level keeps the precedence story short enough to hold
    in your head."""
    raw = _read_toml(path)
    includes = raw.pop(INCLUDE_KEY, None)
    merged: dict[str, object] = {}
    provenance: dict[str, str] = {}

    if includes is not None:
        if not isinstance(includes, list) or not all(isinstance(entry, str) for entry in includes):
            raise ValidationFailure(f"config {path.name}: {INCLUDE_KEY!r} must be a list of file paths")
        for entry in includes:
            child_path = (path.parent / entry).resolve()
            child = _read_toml(child_path)
            if INCLUDE_KEY in child:
                raise ValidationFailure(
                    f"config {child_path.name}: nested {INCLUDE_KEY!r} is not supported — "
                    f"list every file in the top-level manifest ({path.name}) instead"
                )
            _merge_into(merged, child, provenance, child_path.name)

    _merge_into(merged, raw, provenance, path.name)

    unknown = sorted(set(merged) - _ALLOWED_TOP_LEVEL)
    if unknown:
        raise ValidationFailure(
            f"config: unknown top-level key(s) {unknown} — expected one of "
            f"{sorted(_ALLOWED_TOP_LEVEL)}. A typo'd section is refused rather than ignored, "
            f"so a setting can never look applied while doing nothing."
        )
    return merged, provenance


def format_effective_config(config: IngestionConfig) -> str:
    """Render the composed settings with their source file, one line per key.

    Printed at the head of a run so the numbers in the output can always be tied
    to the settings that produced them — the question the securities compare loop
    had to answer by inspection more than once."""
    if not config.provenance:
        return "EFFECTIVE CONFIG: (single file; no provenance recorded)"
    width = max(len(key) for key in config.provenance)
    lines = ["EFFECTIVE CONFIG (key -> source file)"]
    lines += [f"  {key:<{width}}  {source}" for key, source in sorted(config.provenance.items())]
    return "\n".join(lines)


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
    raw, provenance = compose_config(path)

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
        # The D-007 two-sheet contract is a PAIR: one of spot/quarterly without the
        # other is almost certainly a mistake and stays an error. BOTH absent is a
        # legitimate loans-/securities-only config; the expense-family loader guards
        # at the point of use instead.
        if ("spot" in section) != ("quarterly" in section):
            missing = "quarterly" if "spot" in section else "spot"
            raise ValidationFailure(
                f"config [firm_data]: missing [firm_data.{missing}] — the firm-input contract is "
                f"two sheets (D-007): 'spot' for launch-point scalars, 'quarterly' for wide "
                f"PQ1..PQ9 paths. Declare both, or neither for a loans-/securities-only config."
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
                positions_margin_column=(
                    str(sec["positions_margin_column"]) if "positions_margin_column" in sec else None
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
                maturity_quarters_rounding=str(sec.get("maturity_quarters_rounding", "ceil")).strip().lower(),
                maturity_quarters_rounding_overrides=MappingProxyType({
                    str(category): str(mode).strip().lower()
                    for category, mode in sec.get("maturity_quarters_rounding_overrides", {}).items()
                }),
                agency_face_path_survival=bool(sec.get("agency_face_path_survival", False)),
                missing_ac_mode=str(sec.get("missing_ac_mode", "price_proxy_no_accretion")).strip().lower(),
                unsettled_window_days=int(sec.get("unsettled_window_days", 7)),
                missing_ac_mode_overrides=MappingProxyType({
                    str(category): str(mode).strip().lower()
                    for category, mode in sec.get("missing_ac_mode_overrides", {}).items()
                }),
            )
            for category, mode in securities.maturity_quarters_rounding_overrides.items():
                _reject_misplaced_key("maturity_quarters_rounding_overrides", category)
                if mode not in ("ceil", "floor"):
                    raise ValidationFailure(
                        f"config [firm_data.securities.maturity_quarters_rounding_overrides]: mode for "
                        f"{category!r} must be 'ceil' or 'floor' (PID-SEC-15), got {mode!r}"
                    )
            if securities.maturity_quarters_rounding not in ("ceil", "floor"):
                raise ValidationFailure(
                    f"config [firm_data.securities]: maturity_quarters_rounding must be 'ceil' or "
                    f"'floor' (PID-SEC-15), got {sec.get('maturity_quarters_rounding')!r}"
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
        loans = _parse_loans(section["loans"], path.parent.resolve()) if "loans" in section else None
        firm_data = FirmDataConfig(
            firm_id=str(_require(section, "firm_id", "[firm_data]")),
            spot=_table_source(section["spot"], "[firm_data.spot]") if "spot" in section else None,
            quarterly=(
                _table_source(section["quarterly"], "[firm_data.quarterly]")
                if "quarterly" in section else None
            ),
            frb_expense_sign=frb_expense_sign,
            securities=securities,
            loans=loans,
        )

    return IngestionConfig(
        base_dir=path.parent.resolve(),
        mev=mev,
        firm_data=firm_data,
        provenance=MappingProxyType(dict(provenance)),
    )

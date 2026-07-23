"""Typed ingestion configuration, parsed from TOML (stdlib `tomllib` — no dependency).

The company-local config file carries every physical detail: workbook paths, sheet
names, column names, unit scales, the launch-point quarter. This module only defines
the shape. Relative paths resolve against the config file's own directory, so a
config plus its data folder travels as a unit. Template with placeholders:
`config/company.template.toml` — the filled copy stays company-local (gitignored
`config/local/`) and never enters a public repository."""

from __future__ import annotations

import tomllib
from dataclasses import dataclass, field
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
class FirmDataConfig:
    """Two-sheet firm-input contract (D-007): `spot` holds one-time launch-point
    scalars (no quarter dimension), `quarterly` holds PQ1..PQ9 paths in wide layout
    (one row per series, columns PQ1..PQ9). CSV sources use two files; XLSX sources
    typically use two tabs of one workbook. `frb_expense_sign` (D-008) declares how
    the FRB total-interest-expense path is entered — "negative" makes the loader
    negate it to the canonical positive-magnitude convention."""

    firm_id: str
    spot: TableSource
    quarterly: TableSource
    frb_expense_sign: str = EXPENSE_SIGN_POSITIVE


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
        firm_data = FirmDataConfig(
            firm_id=str(_require(section, "firm_id", "[firm_data]")),
            spot=_table_source(section["spot"], "[firm_data.spot]"),
            quarterly=_table_source(section["quarterly"], "[firm_data.quarterly]"),
            frb_expense_sign=frb_expense_sign,
        )

    return IngestionConfig(base_dir=path.parent.resolve(), mev=mev, firm_data=firm_data)

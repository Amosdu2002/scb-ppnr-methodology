"""Generic MEV scenario loader (PID-5 pattern: a Date column + one column per MEV).

The series set is open-ended and declared entirely in configuration — adding an MEV
for a future model family (prime rate, mortgage rate, 10-year Treasury, …) is one
`[mev.series.<name>]` config entry with no code change. Each declared series is
sliced to the PQ0..PQ9 window around the configured launch point (real MEV files
carry long histories; out-of-window rows are ignored) and normalized per its
declared scale. Unconfirmed mappings (TO_BE_CONFIRMED) refuse to load — this is how
the PID-OB-4 BBB gates and the OQ-023 FRB-total gate block a run.

Two file layouts are supported: one scenario per file/sheet (just a Date column plus
MEV columns), or a **long format** where one sheet holds several scenarios under a
scenario-name column ([mev].scenario_name_column). In the long format, history and
launch-point (PQ0) rows carry the actuals label ([mev].actuals_label, default
"Actual") and each scenario's PQ1..PQ9 rows carry its own label
([mev.scenarios.<id>].label); rows belonging to other scenarios are simply ignored,
so several configured scenarios can share one sheet. Label matching is
whitespace-trimmed and case-insensitive.

`MevScenario.interest_expense_scenario_paths()` selects the three canonical series
the interest-expense family consumes; other families will select their own."""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping, Sequence

from ..core.schemas import (
    PROJECTION_QUARTERS,
    SCENARIO_QUARTERS_WITH_LAUNCH,
    ValidationFailure,
)
from ..interest_expense.schemas import ScenarioPaths
from .config import SERIES_KIND_RATE, IngestionConfig
from .normalize import Quarter, apply_rate_scale, parse_quarter, require_confirmed, to_float
from .tables import read_table


@dataclass(frozen=True)
class MevScenario:
    scenario_id: str
    launch_point: Quarter
    series: Mapping[str, Mapping[int, float]]   # series name -> {PQ index: value}, window 0..9

    def series_window(self, name: str, quarters: Sequence[int]) -> dict[int, float]:
        if name not in self.series:
            raise ValidationFailure(
                f"scenario {self.scenario_id!r}: series {name!r} is not declared in [mev.series] "
                f"(declared: {sorted(self.series)})"
            )
        data = self.series[name]
        missing = [q for q in quarters if q not in data]
        if missing:
            raise ValidationFailure(
                f"scenario {self.scenario_id!r}: series {name!r} is missing quarters "
                f"{[f'PQ{q}' for q in missing]} relative to launch point {self.launch_point}"
            )
        return {q: data[q] for q in quarters}

    def interest_expense_scenario_paths(self) -> ScenarioPaths:
        return ScenarioPaths(
            scenario_id=self.scenario_id,
            usd_3m_treasury=self.series_window("usd_3m_treasury", SCENARIO_QUARTERS_WITH_LAUNCH),
            usd_1y_treasury=self.series_window("usd_1y_treasury", PROJECTION_QUARTERS),
            bbb_corporate_yield=self.series_window("bbb_corporate_yield", PROJECTION_QUARTERS),
        )


def _normalize_label(value: object) -> str:
    return "" if value is None else str(value).strip().casefold()


def load_mev_scenario(config: IngestionConfig, scenario_id: str) -> MevScenario:
    if config.mev is None:
        raise ValidationFailure("config has no [mev] section")
    mev = config.mev
    if scenario_id not in mev.scenarios:
        raise ValidationFailure(
            f"scenario {scenario_id!r} not configured; available: {sorted(mev.scenarios)}"
        )

    # Confirm every declared mapping before touching any file, so unfilled gates
    # (PID-OB-4, OQ-023, PID-5 column names) fail fast and unambiguously.
    for name, spec in mev.series.items():
        require_confirmed(
            f"[mev.series.{name}].column", spec.column,
            gate="physical MEV column mapping must be user-confirmed (PID-5 pattern; BBB gated by PID-OB-4)",
        )
        if spec.kind == SERIES_KIND_RATE:
            require_confirmed(
                f"[mev.series.{name}].scale", spec.scale,
                gate="rate scale is metadata-driven, never assumed — conventions §2",
            )
        elif spec.scale:
            raise ValidationFailure(f"[mev.series.{name}]: 'level' series must not declare a scale")

    source = mev.scenarios[scenario_id]
    path = config.resolve(source.path)
    rows = read_table(path, source.sheet)
    if not rows:
        raise ValidationFailure(f"{path}: no data rows")
    header = set(rows[0].keys())
    if mev.date_column not in header:
        raise ValidationFailure(f"{path}: date column {mev.date_column!r} not found; header: {sorted(header)}")
    if mev.scenario_name_column and mev.scenario_name_column not in header:
        raise ValidationFailure(
            f"{path}: scenario-name column {mev.scenario_name_column!r} not found; header: {sorted(header)}"
        )
    for name, spec in mev.series.items():
        if spec.column not in header:
            raise ValidationFailure(
                f"{path}: column {spec.column!r} for series {name!r} not found; header: {sorted(header)}"
            )

    launch = parse_quarter(mev.launch_point, context="[mev].launch_point")
    series_data: dict[str, dict[int, float]] = {name: {} for name in mev.series}
    seen_quarters: set[int] = set()
    for line, row in enumerate(rows, start=2):
        row_quarter = parse_quarter(row.get(mev.date_column), context=f"{path} row {line}, column {mev.date_column!r}")
        pq = row_quarter.offset_from(launch)
        if not 0 <= pq <= 9:
            continue
        if mev.scenario_name_column is not None:
            # Long format: PQ0 comes from the actuals rows, PQ1..PQ9 from this
            # scenario's labeled rows; everything else in the sheet is not this run's data.
            wanted = mev.actuals_label if pq == 0 else source.label
            if _normalize_label(row.get(mev.scenario_name_column)) != _normalize_label(wanted):
                continue
        if pq in seen_quarters:
            raise ValidationFailure(f"{path} row {line}: duplicate quarter {row_quarter} (PQ{pq})")
        seen_quarters.add(pq)
        for name, spec in mev.series.items():
            raw = row.get(spec.column)
            if raw is None or (isinstance(raw, str) and not raw.strip()):
                continue  # blank cell = missing; surfaces later only if a consumer demands this quarter
            context = f"{path} row {line}, series {name!r}"
            value = to_float(raw, context=context)
            if spec.kind == SERIES_KIND_RATE:
                value = apply_rate_scale(spec.scale, value, context=context)
            series_data[name][pq] = value

    frozen = {
        name: MappingProxyType(dict(sorted(values.items())))
        for name, values in series_data.items()
    }
    return MevScenario(scenario_id=scenario_id, launch_point=launch, series=MappingProxyType(frozen))

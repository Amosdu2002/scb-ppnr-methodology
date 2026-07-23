"""Ingestion layer: config-driven loaders that turn physical files (CSV/XLSX) into
the canonical inputs the models consume. Company-specific details (paths, sheets,
columns, scales) live only in a company-local config file — see
config/company.template.toml. Models never import from this package."""

from .config import (
    SERIES_KIND_LEVEL,
    SERIES_KIND_RATE,
    FirmDataConfig,
    IngestionConfig,
    MevConfig,
    ScenarioSource,
    SeriesSpec,
    TableSource,
    load_config,
)
from .firm_data_loader import load_family_inputs, load_income_inputs
from .mev_loader import MevScenario, load_mev_scenario
from .normalize import Quarter, parse_quarter
from .tables import read_table

__all__ = [
    "FirmDataConfig",
    "IngestionConfig",
    "MevConfig",
    "MevScenario",
    "Quarter",
    "ScenarioSource",
    "SERIES_KIND_LEVEL",
    "SERIES_KIND_RATE",
    "SeriesSpec",
    "TableSource",
    "load_config",
    "load_family_inputs",
    "load_income_inputs",
    "load_mev_scenario",
    "parse_quarter",
    "read_table",
]

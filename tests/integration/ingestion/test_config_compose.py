"""Composition guards for multi-file config.

The split exists so methodology switches stay reviewable in git while physical
bindings stay out of it. Splitting introduces one new way to be wrong — the same
key in two files — so the merge refuses it outright rather than picking a winner,
and records where every leaf came from."""

from __future__ import annotations

from pathlib import Path

import pytest

from scb_ppnr.core.schemas import ValidationFailure
from scb_ppnr.ingestion.config import compose_config, format_effective_config, load_config

ROOT = Path(__file__).resolve().parents[3]


def _write(directory: Path, name: str, body: str) -> Path:
    path = directory / name
    path.write_text(body, encoding="utf-8")
    return path


def test_tables_merge_across_files_and_record_provenance(tmp_path: Path) -> None:
    _write(tmp_path, "methodology.toml", '[firm_data.securities]\nfloor_mode = "zero"\n')
    _write(tmp_path, "local.toml", '[firm_data.securities]\nworkbook = "book.xlsx"\n')
    manifest = _write(tmp_path, "run.toml", 'include = ["methodology.toml", "local.toml"]\n')

    merged, provenance = compose_config(manifest)

    securities = merged["firm_data"]["securities"]  # type: ignore[index]
    assert securities == {"floor_mode": "zero", "workbook": "book.xlsx"}
    assert provenance["firm_data.securities.floor_mode"] == "methodology.toml"
    assert provenance["firm_data.securities.workbook"] == "local.toml"


def test_duplicate_leaf_across_files_is_refused_not_overridden(tmp_path: Path) -> None:
    _write(tmp_path, "a.toml", '[firm_data.securities]\nfloor_mode = "zero"\n')
    _write(tmp_path, "b.toml", '[firm_data.securities]\nfloor_mode = "security_floor"\n')
    manifest = _write(tmp_path, "run.toml", 'include = ["a.toml", "b.toml"]\n')

    with pytest.raises(ValidationFailure) as excinfo:
        compose_config(manifest)

    message = str(excinfo.value)
    assert "firm_data.securities.floor_mode" in message
    assert "a.toml" in message and "b.toml" in message


def test_unknown_top_level_section_is_refused(tmp_path: Path) -> None:
    manifest = _write(tmp_path, "run.toml", '[firm_dat]\nfirm_id = "TYPO"\n')

    with pytest.raises(ValidationFailure, match="unknown top-level key"):
        compose_config(manifest)


def test_nested_include_is_refused(tmp_path: Path) -> None:
    _write(tmp_path, "leaf.toml", "[mev]\n")
    _write(tmp_path, "middle.toml", 'include = ["leaf.toml"]\n')
    manifest = _write(tmp_path, "run.toml", 'include = ["middle.toml"]\n')

    with pytest.raises(ValidationFailure, match="nested"):
        compose_config(manifest)


def test_single_file_config_still_loads_unchanged() -> None:
    """Backward compatibility: an existing company-local config keeps working."""
    config = load_config(ROOT / "config" / "company.template.toml")
    assert config.mev is not None
    assert config.provenance["mev"] == "company.template.toml"


def test_example_manifest_composes_the_committed_files() -> None:
    config = load_config(ROOT / "config" / "runs" / "example.toml")
    assert config.mev is not None
    dump = format_effective_config(config)
    assert "company.template.toml" in dump
    assert "loans.toml" in dump

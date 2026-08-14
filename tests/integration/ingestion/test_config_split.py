"""The 2026-08-14 config split: company.template.toml carries bindings only,
config/models/*.toml carry the methodology switches, and the committed
config/runs/company.toml manifest composes a gitignored config/local/sources.toml
with the models files. Pinned here: the manifest's include spelling (it must
fail by NAMING the absent sources file on a clean checkout); that the template
used as the sources file composes with both models files with zero duplicate
leaves; that composition and an equivalent single file produce identical typed
configs; and the models files' exact active-leaf inventory — activating a new
switch is a conscious commit that updates that inventory test."""

from __future__ import annotations

import shutil
import tomllib
from pathlib import Path

import pytest

from scb_ppnr.core.schemas import ValidationFailure
from scb_ppnr.ingestion.config import format_effective_config, load_config

ROOT = Path(__file__).resolve().parents[3]
TEMPLATE = ROOT / "config" / "company.template.toml"


def _replica(tmp_path: Path) -> Path:
    """Copy the committed structure into tmp with the template as sources.toml."""
    (tmp_path / "runs").mkdir()
    (tmp_path / "models").mkdir()
    (tmp_path / "local").mkdir()
    shutil.copy(ROOT / "config" / "runs" / "company.toml", tmp_path / "runs" / "company.toml")
    shutil.copy(ROOT / "config" / "models" / "loans.toml", tmp_path / "models" / "loans.toml")
    shutil.copy(ROOT / "config" / "models" / "securities.toml",
                tmp_path / "models" / "securities.toml")
    shutil.copy(TEMPLATE, tmp_path / "local" / "sources.toml")
    return tmp_path / "runs" / "company.toml"


def test_company_manifest_names_the_gitignored_sources_file():
    # config/local/ is gitignored and absent on a clean checkout: the manifest
    # must fail by naming the missing file, pinning its include spelling.
    with pytest.raises(ValidationFailure, match="sources.toml"):
        load_config(ROOT / "config" / "runs" / "company.toml")


def test_template_as_sources_composes_with_the_models_files(tmp_path):
    config = load_config(_replica(tmp_path))
    assert config.provenance["firm_data.loans.workbook"] == "sources.toml"
    assert config.provenance["firm_data.loans.floor_collapse"] == "loans.toml"
    assert config.provenance["firm_data.loans.cre_orig_date_statistic"] == "loans.toml"
    assert config.provenance["firm_data.securities.floating_projection"] == "securities.toml"
    assert config.firm_data.loans.cre_orig_date_statistic == "weighted_median"
    assert config.firm_data.securities.floating_projection == "spot"
    assert config.firm_data.securities.floor_mode == "security_floor_else_zero"
    dump = format_effective_config(config)
    for name in ("sources.toml", "loans.toml", "securities.toml"):
        assert name in dump, name


def test_composed_structure_equals_the_single_file(tmp_path):
    # A single file carrying the same values as the composition must produce an
    # identical typed config (provenance differs by design, so compare the
    # mev/firm_data payloads, in the same directory so path resolution matches).
    template_text = TEMPLATE.read_text(encoding="utf-8")
    single = tmp_path / "single.toml"
    # [firm_data.loans] is the template's final table, so an EOF append lands
    # there — guarded below. floating_projection = "spot" equals the code
    # default and needs no line for the typed configs to match.
    single.write_text(
        template_text
        + '\ncre_orig_date_statistic = "weighted_median"\nfloor_collapse = "balance_weighted"\n',
        encoding="utf-8")
    raw = tomllib.loads(single.read_text(encoding="utf-8"))
    assert raw["firm_data"]["loans"]["cre_orig_date_statistic"] == "weighted_median"
    assert raw["firm_data"]["loans"]["floor_collapse"] == "balance_weighted"

    (tmp_path / "sources_copy.toml").write_text(template_text, encoding="utf-8")
    manifest = tmp_path / "manifest.toml"
    manifest.write_text(
        "include = [\n"
        '    "sources_copy.toml",\n'
        f'    "{ROOT / "config" / "models" / "loans.toml"}",\n'
        f'    "{ROOT / "config" / "models" / "securities.toml"}",\n'
        "]\n",
        encoding="utf-8")

    a = load_config(single)
    b = load_config(manifest)
    assert a.mev == b.mev
    assert a.firm_data == b.firm_data


def test_models_files_carry_exactly_the_pinned_active_leaves():
    # The models files are decision RECORDS: everything stays commented until a
    # value is confirmed. Activating a switch must consciously extend this
    # inventory (and step 3 of the company.toml migration checklist covers any
    # collision with a local sources file).
    def leaves(path: Path, prefix: str = "") -> set[str]:
        def walk(node, at):
            if isinstance(node, dict):
                for key, value in node.items():
                    yield from walk(value, f"{at}.{key}" if at else key)
            else:
                yield at
        return set(walk(tomllib.loads(path.read_text(encoding="utf-8")), prefix))

    assert leaves(ROOT / "config" / "models" / "loans.toml") == {
        "firm_data.loans.floor_collapse",
        "firm_data.loans.cre_orig_date_statistic",
    }
    assert leaves(ROOT / "config" / "models" / "securities.toml") == {
        "firm_data.securities.floating_projection",
    }

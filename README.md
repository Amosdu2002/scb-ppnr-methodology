# Federal Reserve Proposed 2026 PPNR Net-Interest Methodology Handbook

Documentation-first repository translating the public Federal Reserve proposal for
the 2026 PPNR model suite (Section v of `sources/fed/pre-provision-net-revenue-models.pdf`,
the authoritative source) into a coding-friendly handbook, plus a reference Python
implementation of both net-interest sides: the liability-side interest-expense family
and the asset-side interest-income family (loans, securities, calculators, trading
NII) with a combined-NII monitor. All proposed models are **public-comment stage,
NOT adopted**. The repository contains only public Federal Reserve material,
original nonconfidential documentation, and synthetic examples — no confidential
data, workbooks, or firm-specific details.

## Layout

| Path | Content |
|---|---|
| `sources/fed/` | Authoritative PDF + searchable Markdown conversion (never edited) |
| `docs/handbook/` | Model chapters, cross-cutting conventions, open-question/decision log |
| `docs/specifications/` | Machine-readable YAML spec per model (implementation contracts) |
| `docs/inventory/` | Model inventory, source map, integrity review, per-side model matrices |
| `docs/reviews/` | Independent source-grounding review reports |
| `docs/architecture/` | Design notes: expense side, income side, `run-and-config.md` (runners + config) |
| `config/` | Bindings template, committed methodology switches (`models/`), run manifests (`runs/`) |
| `src/scb_ppnr/` | Reference implementation (canonical inputs; stdlib models, openpyxl for XLSX ingestion) |
| `tests/` | Synthetic deterministic unit + integration tests |
| `examples/` | Per-family runners and diagnostic sidecars (chained by `run.py` at the root) |

## Implemented model families

**Interest expense** — `ie_dom_time_dep` (Eq A44 WAL recursion), `ie_other_dom_dep`
and `ie_foreign_dep` (Eqs A45–A47 two-regime deposit betas), `ie_fed_funds_repo`
(Eq A48 direct calculator), and `ie_other_borrowing` (Eq A53 regression rate with
the PID-OB-5 nine-quarter alpha calibration against a project-supplied FRB
total-interest-expense path).

**Interest income** — `ii_loans` (corporate, CRE, and the four retail families),
`ii_ust` / `ii_mbs` / `ii_other_sec` (securities), the `ii_dep_banks_other` /
`ii_other_ida` calculators, and `nii_trading_al` (the PID-TRD-1 residual backsolve
against the FRB total-interest-income path, run last). The combined-NII monitor
(`nii_monitor.py`) checks NII = income − expense against the FRB path (1%
cumulative guard; reports, never forces).

All outputs are pre-hedge; the Section v.c hedge adjustment is an external
downstream interface.

## Quickstart

```bash
# environment (Python >= 3.11; pytest + openpyxl are the dev dependencies)
python3 -m venv .venv && .venv/bin/pip install -e ".[dev]"
.venv/bin/python -m pytest tests/ -q

# the whole pipeline, synthetic end to end (no PYTHONPATH needed)
.venv/bin/python run.py
```

## Running the pipeline

`run.py` chains the validated family runners in order — loans → securities →
expense → nii — into one artifact directory (`out/<timestamp>/`, gitignored:
reports, component CSVs, the consolidated `results.xlsx` workbook with its
`results.csv` twin, `effective_config.txt`, `run_summary.txt`):

```bash
python3 run.py --config config/runs/company.toml      # company run, all stages
python3 run.py --check --config <cfg>                 # validate config, run nothing
python3 run.py --only loans securities --config <cfg> # subset
```

Company setup: copy `config/company.template.toml` to `config/local/sources.toml`
(gitignored), fill the placeholders, run through `config/runs/company.toml` — the
manifest composes your bindings with the committed methodology switches in
`config/models/`. The per-family runners in `examples/` remain the granular path
(`run_loans.py --retail-only`, `diagnose_securities.py --explain`, ...); see
`docs/architecture/run-and-config.md`.

New to the suite? **[`FIELD_GUIDE.md`](FIELD_GUIDE.md)** is the onboarding
reference: system overview, input-to-model mapping, configuration,
execution, and the reconciliation procedure.

## Where decisions live

Project-wide decisions (D-xxx), component decisions (PID-xxx), and open questions
(OQ-xxx) are registered in `docs/handbook/open-questions.md`; chapters and YAML specs cite
them inline. Nothing labeled PID/D is ever attributable to the Federal Reserve.

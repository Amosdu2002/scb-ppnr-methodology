# Run and Config Architecture

Status: landed 2026-08-14 (the orchestration/config-UX increment recorded as
"next planned" in `inventory/asset-side-model-matrix.md`). Behavior-preserving
by construction: the three pinned family runners were not edited, all
pre-existing tests pass with zero test-file edits, and the synthetic pipeline
outputs byte-match the standalone runners' outputs.

## Runner hierarchy

One user-facing command; the per-family runners stay as the granular and
diagnostic layer beneath it.

```
run.py                            the pipeline: loans -> securities -> expense -> nii
└── examples/
    run_loans.py                  wholesale + retail loans (census, compare mode, --paths-out)
    run_securities.py             ust/mbs/other_sec (--paths-out, --paths-basis xr|full)
    run_from_config.py            the expense family report (modernized: main(argv) -> int, --report)
    run_nii.py                    component assembly + trading backsolve + combined-NII monitor
    run_income_calculators.py     Family A calculators standalone (superseded by run_nii for pipeline use)
    run_synthetic_family.py       hardcoded synthetic expense demo (no CLI)
    diagnose_securities.py        per-security compare/explain sidecar
    diagnose_deposits.py          deposit-model debugger sidecar
```

`run.py` executes the stage runners **in-process** with the exact argv the
manual commands would use (each stage banner prints that command), so stage
reports are byte-identical with the 3-command workflow documented in
`run_nii.py`'s header — which remains valid and is what the pipeline automates:
loans `--paths-out` and securities `--paths-out` feed `run_nii
--component-paths`.

Stage semantics:

- loans, securities, expense are mutually independent — each runs even if
  another failed (both asset reports are wanted when reconciling);
- nii is gated on **file existence** of both component CSVs in the `--out`
  directory (loans skips its CSV on failure; securities dies before writing —
  so existence ⟺ producer success). `--only nii --out <previous-run-dir>`
  therefore reuses earlier CSVs;
- exit 0 iff every selected stage ran and returned 0; a selected-but-gated nii
  is a failure;
- with no `--config`, every stage runs its own self-contained synthetic demo —
  no cross-feeding, so demo outputs stay diffable against the standalone demos.

Failure normalization: the runners disagree on conventions (`main(argv) -> int`
for loans/nii/expense, `-> None` for securities; securities raises
`SystemExit(str)` on a missing `[mev]` and lets `ValidationFailure` propagate).
`run.py::_call` folds every outcome — int returns, None returns, SystemExit,
ValidationFailure (message, no traceback), and unexpected exceptions
(traceback) — into a per-stage (rc, detail), so one stage can never kill the
chain.

SCENARIO NAMESPACES: `run.py --scenario` is a `[mev.scenarios.<id>]` config id
and is forwarded to securities/expense/nii only. The loans runner's
`--scenario` is a projection-block NAME inside the loans workbook's own MEV
sheet (default `[firm_data.loans].scenario`) — a different namespace; run.py
never forwards to it. Use `run_loans.py --scenario` directly for a one-off
override.

## Artifact convention

Everything a run produces lands in `--out` (default `out/<timestamp>/`,
gitignored — these files carry firm amounts on company runs):
`loans_report.txt`, `loans_paths.csv`, `securities_report.txt`,
`securities_paths.csv`, `expense_report.txt`, `nii_report.txt`,
`results.xlsx` + `results.csv` (the consolidated results — see below),
`effective_config.txt`, `run_summary.txt`, a `README.txt` reading guide, and
`<stage>.log` under `--quiet`. `out/latest` points at the newest
default-location run (symlink; `LATEST.txt` fallback where symlinks are
unavailable). Report tables share one layout (`core.common.format_path_row`):
space-joined, comma-grouped columns that cannot fuse at any magnitude —
replacing the fixed-width concatenation that ran five-digit values together.

`results.xlsx` (written by the nii stage via `run_nii --consolidated-out`,
built in side-neutral `src/scb_ppnr/consolidated.py`) consolidates the run:
a Summary sheet (headline income/expense/NII vs the FRB targets, both alpha_b
calibrations, the monitor verdict, per-component nine-quarter cumulatives) and
full quarterly-path sheets for Income and Expense. `results.csv` is its flat
stdlib-only twin — every quarterly-path row at the `--paths-out` %.6f
convention — for machine reads and run-to-run diffs. The Expense sheet is
omitted under `--skip-expense`; a missing openpyxl degrades to the CSV with a
printed note.

`effective_config.txt` (also printed by `--check`) is a
`key = value  # source-file` dump built on `compose_config`'s provenance — the
values complement to `format_effective_config` (sources only, printed by
run_loans at every company run). Archive it with each run's results; diffing
two dumps is the value-for-value proof that a config restructuring changed
nothing (the mechanism the 2026-08-14 migration checklist in
`config/runs/company.toml` relies on).

## Config composition

The mechanism (commit b6571fd, 2026-08-03; `src/scb_ppnr/ingestion/config.py`,
unchanged by this increment): a manifest's top-level `include = [...]` merges
files in order, tables recursively; a leaf defined twice is a hard error naming
both files (no override semantics); unknown top-level sections are refused;
includes are one level deep; every leaf gets file-basename provenance.
Single-file configs load unchanged — composition is optional.

The structure (migrated 2026-08-14, the "break between runs" the b6571fd
commit message required):

```
config/
  company.template.toml     BINDINGS template (~320 lines): [mev], firm core,
                            spot/quarterly, securities bindings + enrichment +
                            the load-required floor_mode, loans bindings +
                            compare-mode toggles. Copy to config/local/sources.toml.
  models/loans.toml         loans methodology switches. Active: floor_collapse,
                            cre_orig_date_statistic (PID-LOAN-22, user-confirmed
                            2026-08-14). Commented decision records: engine,
                            share_basis, balance_source, mortgage_window,
                            card_spread_mode, retail_auto_scalar, heloc_spread_anchor.
  models/securities.toml    securities methodology switches. Active:
                            floating_projection = "spot" (PID-SEC-10/18,
                            user-confirmed). Commented: everything else incl.
                            the per-category override sub-tables.
  runs/company.toml         THE company manifest: sources.toml + the two models
                            files; header carries the migration checklist.
  runs/example.toml         same shape composing the template instead of a
                            local file (test fixture + demonstration).
  local/                    gitignored; holds sources.toml on a company machine.
```

Boundary rule of the split: **bindings** (paths, sheet names, column headers,
scales — company-local, gitignored) vs **methodology decisions** (PID-pinned
switches — committed, reviewed in git next to the registry that justifies
them). `floor_mode` is the one switch that lives with the bindings because
`load_config` requires it whenever `[firm_data.securities]` exists.
`test_config_split.py` pins the models files' exact active-leaf inventory, so
activating a switch is always a conscious, test-visible commit.

Two guardrails inherited from the merge rules: relative paths in composed files
resolve against the MANIFEST's directory (prefer absolute workbook paths in
sources.toml), and provenance records basenames — keep included files' basenames
distinct.

## Known follow-ups (recorded, not blocking)

- `_parse_loans`'s absent-key fallback for `cre_orig_date_statistic` is
  `"weighted_mean"` while the dataclass default is `"weighted_median"`
  (config.py); the committed activation in models/loans.toml makes the fallback
  unreachable for composed runs, but aligning the code default deserves its own
  change with its own test.
- Pre-existing latent gaps in the securities config parsing: enrichment
  `margin_column` is a declared field the loader never parses; unknown scalar
  keys inside `[firm_data.securities]` are silently ignored (loans refuses
  them by name).
- The `INCLUDE_KEY` entry in `_ALLOWED_TOP_LEVEL` is unreachable (compose pops
  `include` before the check).

# scb_ppnr Field Guide

Setup and operating reference for the `scb_ppnr` net-interest projection suite
(Federal Reserve proposed 2026 methodology), written for practitioners who know
the SCB PPNR framework but are new to this implementation.

## Scope of the repository

The repository serves two functions. It is a **methodology handbook** that
translates the Federal Reserve's proposed 2026 PPNR net-interest models into
implementable specifications, with every interpretation registered under a
decision ID (the models are at public-comment stage and must not be described
as adopted). It is also the **reference Python implementation** of both sides
of net interest, reconciled component by component against the firm's reference
workbook: Corporate 0.9979, CRE 1.0006, retail exact, securities ≈0.999 on the
xr basis, trading NII exact by construction.

Version-control policy: the repository itself carries only public Federal
Reserve material, generic specifications, and synthetic examples. Firm inputs,
filled configuration, and run outputs remain in gitignored locations
(`config/local/`, `out/`, all workbooks) and are never committed.

## 1. System overview

Thirteen component models project PQ1–PQ9 from the PQ0 launch point — USD
millions, pre-hedge, constant balances and composition. One structural property
governs execution order: each side ends in a **residual backsolve**. Other
Borrowing (expense) and Trading NII (income) run last, calibrating an intercept
α so the family's nine-quarter *cumulative* total equals the corresponding
FRB-provided path exactly. Per-quarter deviations from the FRB paths are
therefore structural, not errors; the reconciliation verdicts are cumulative.

```
loans workbooks ───────────▶ Stage 1: loans ──────── loans_paths.csv ──────┐
securities workbook ───────▶ Stage 2: securities ─── securities_paths.csv ─┤
                                                                           ▼
spot + quarterly tabs ── calculator inputs + FRB income target ──▶ Stage 4: nii
     │                                     assembles the six sibling paths and
     │ deposit rows                        computes the two calculators in-stage;
     │                                     TRADING NII RUNS LAST — α backsolved so
     │                                     the 9Q cumulative equals
     ▼                                     frb_total_interest_income (exact by
MEV ▶ Stage 3: expense                     construction; implied path printed
     four deposit/funding models;          first as the round-0 diagnostic)
     OTHER BORROWING RUNS LAST —                          │
     α vs frb_total_interest_expense                      │ income total
                │                                         ▼
                │                              combined-NII monitor
                └───── expense total ────────▶ cumulative |NII − FRB NII|
                                               within 1%; reports, never forces
```

Stages 1–3 are mutually independent; Stage 4 requires both component CSVs. The
MEV scenario file also feeds Stages 2 and 4 (rate paths); the loans family
reads its MEV series from its own workbook instead.

## 2. Installation and verification

```bash
git clone <repo> && cd scb-ppnr-methodology
python3 -m venv .venv && .venv/bin/pip install -e ".[dev]"   # Python >= 3.11
.venv/bin/python -m pytest tests/ -q                          # expected: 442 passed
.venv/bin/python run.py                                       # synthetic end-to-end run
```

The final command requires no firm data and no PYTHONPATH: every stage
generates hand-checkable synthetic inputs, and the run ends with
`PIPELINE: OK`. The artifact set it writes to `out/<timestamp>/` has the same
structure as company-run output and serves as the format reference for the
sections below.

## 3. Inputs — what is required, what it feeds, where it is declared

A company run draws on the six input groups below. The single file to edit is
`config/local/sources.toml`: it declares where every workbook and sheet lives.
The two canonical tabs then carry row-level inputs inside the workbook itself,
and the committed `config/models/` files carry the methodology switches.

| Input | Feeds | Declared / supplied in |
|---|---|---|
| **Wholesale loans workbook** | Corporate and CRE loan interest income. | Path and all sheet bindings (CORP H.1, CRE H.2, M.1 Balance, FR-Y9C extract, MEV sheet, header rows, column names, unit scales) under `[firm_data.loans]` in `sources.toml`. Naming `cre_h2_sheet` enables the CRE run; `results_sheet` / `cre_results_sheet` enable compare mode. |
| **Retail loans workbooks** | Mortgage (incl. HELOC), Card, Auto, Other Consumer income. | Retail keys of `[firm_data.loans]`: `retail_workbook` (M.1 Balances, MEV Data, Mortgage query, Card query, OTHER, line-item projections sheet) and `auto_pivot_workbook` / `auto_pivot_sheet`. Each family runs when its sheet is named. |
| **Securities workbook** | U.S. Treasuries, Agency MBS, Other Securities income. | `[firm_data.securities]` in `sources.toml`: workbook path, positions sheet (located by its MDRM header row), prepayment pivot, unit scales, `floor_mode`, and one `[[firm_data.securities.enrichment]]` block per enrichment tab. |
| **MEV scenario file** | Scenario rate paths for Securities, the Expense family, the two calculators, and Trading NII. (Loans reads its MEV series from the loans workbook instead.) | `[mev]`, `[mev.scenarios.<id>]`, and one `[mev.series.*]` entry per series (3M/1Y/10Y Treasury, BBB, Prime, mortgage rate) in `sources.toml`. Column names and unit scales are declared per series. |
| **Spot tab** (launch-point scalars) | All five expense models — Domestic Time, Other Domestic, and Foreign Deposits, Fed Funds/Repo, Other Borrowing (rates, balances, WAL, shares, ELB spreads); the two calculators (Deposits-with-Banks, Other IDA); the Trading NII balance pair. | Sheet location under `[firm_data.spot]`. The inputs themselves are sheet *rows* keyed `model, field, subcomponent, scale, value` — not config keys. Worked layout: `examples/synthetic_data/firm_inputs_spot.csv`. |
| **Quarterly tab** (PQ1–PQ9 paths) | The calibration targets and the identity check: Other Borrowing calibrates to `frb_total_interest_expense` (required); Trading NII calibrates to `frb_total_interest_income` (required for income runs); `frb_net_interest_income` (optional) enables the combined-NII monitor. | Sheet location under `[firm_data.quarterly]`; the paths are rows under model `family`, nine quarters wide, with the unit scale declared per row. Worked layout: `examples/synthetic_data/firm_inputs_quarterly.csv`. |
| **Methodology switches** | Model behavior common to every run — e.g. floater floor rule and projection mode (Securities), origination-date statistic and engine selection (Loans). | Committed in `config/models/loans.toml` and `config/models/securities.toml`, pinned to the values that reconciled and annotated with their PIDs. Reviewed in git; not edited per run. |

## 4. Configuration

```bash
cp config/company.template.toml config/local/sources.toml
# fill every <PLACEHOLDER> and TO_BE_CONFIRMED, then validate:
python3 run.py --check --config config/runs/company.toml      # repeat until CONFIG OK
```

The committed manifest `config/runs/company.toml` composes `sources.toml` with
the two `config/models/` files. One file is edited; the manifest and the models
files stay as committed.

- **The loaders refuse rather than guess.** A remaining `TO_BE_CONFIRMED`, an
  undeclared unit scale, or an unrecognized key under `[firm_data.loans]` stops
  the run and names the item. Resolve the message; do not work around it.
- **A key set in two composed files is a hard error naming both files** —
  never a silent override. Keep each switch in exactly one place.
- `--check` prints the effective configuration as `key = value  # source-file`.
  Every run also writes it to `out/…/effective_config.txt`; archive it with the
  run's results so any later reconciliation can be tied to the exact settings
  that produced it.

## 5. Execution

```bash
python3 run.py --config config/runs/company.toml              # all stages, correct order
python3 run.py --config … --scenario severely_adverse         # select a [mev.scenarios] id
python3 run.py --config … --only loans                        # single stage
python3 run.py --config … --only nii --out out/<earlier-run>  # reuse earlier component CSVs
```

| Artifact in `out/<stamp>/` | Contents |
|---|---|
| `run_summary.txt` | Per-stage status, timings, and the pipeline verdict. Read first. |
| `loans_report.txt` | Loader censuses (row counts, unidentified rows, fallbacks), then projected income per family; compare blocks when compare mode is enabled. |
| `securities_report.txt` | Per-model income with coupon, accretion, and reinvestment legs; bucketed warning summary. |
| `expense_report.txt` | The five expense paths, the FRB target row, and the Other-Borrowing α calibration block. |
| `nii_report.txt` | Component-paths table, the round-0 implied-trading diagnostic, the α calibration and family reconciliation, and the combined-NII monitor verdict. |
| `*_paths.csv` | Component hand-off files (`component, PQ1…PQ9`, USD millions); also usable with the per-stage runners directly. |

**Operational notes.** (1) `--scenario` applies to the securities, expense, and
NII stages. The loans stage's scenario is a projection-block *name* inside the
loans workbook's own MEV sheet — a separate namespace — and is set in
`[firm_data.loans].scenario`. (2) The monitor's verdict is cumulative only;
per-quarter divergence from the FRB paths is structural under cumulative-only
calibration and does not indicate an error.

## 6. Reconciliation against the reference workbook

Three practices carried every family to convergence and remain the standard
procedure:

- **Match the basis before judging numbers.** The reference components sheet
  carries unscaled, reinvestment-excluded figures: loans compare runs use
  `apply_scalar = false` (production runs use `true`), auto comparisons use the
  workbook's 0.948 panel scalar versus the published 0.865, and securities
  exports default to the `xr` basis (reinvestment income excluded, PID-SEC-8).
- **Judge the implied path before judging α.** The NII report prints the
  round-0 implied trading path first because it inherits every sibling
  component's convergence error. Compare it to the reference "Implied FRB
  results" row, then the modeled "NII TATL" row; the report rows are labeled
  for one-for-one paste comparison.
- **Escalate to the targeted tools.** Loans compare mode (`results_sheet` with
  `engine = "reference"`, `share_basis = "utilized"`) prints both sides per
  block with implied balances and spreads.
  `diagnose_securities.py --compare / --gaps / --explain` works per security
  with masked identifiers and a relay-safe summary block.
  `diagnose_deposits.py` traces the two deposit-beta models input by input.

## Operating conventions

- **Proposed, not adopted.** Outputs and documents state that the methodology
  is the Federal Reserve's proposal; retain that framing in derived material.
- **Decisions carry IDs.** Project decisions (D-xxx), component implementation
  decisions (PID-xxx), and open questions (OQ-xxx) are registered in
  `handbook/open-questions.md`, append-only. No PID/D item is attributable to
  the Federal Reserve. Methodology changes receive an ID before implementation.
- **Refuse, never guess; log, never clamp.** Missing or unconfirmed inputs stop
  the run by name. Suspicious but legal inputs (wt > 1, floor outliers, NaN
  cells) are surfaced and counted, never silently adjusted.
- **Zero-test-edit refactors.** The validated suites are frozen: shared-code
  changes must keep all 442 tests green without modifying a test file.
- **Outputs remain local.** `out/`, report files, component CSVs,
  `config/local/`, and all workbooks are gitignored. Confirm `git status` is
  clean after a company run.

## Reference documents

| Document | Purpose |
|---|---|
| `README.md` | Repository overview and quickstart. |
| `architecture/run-and-config.md` | Runner hierarchy, stage semantics, and the configuration composition design — Sections 1 and 4 of this guide, in full. |
| `architecture/interest-expense-design.md` / `interest-income-design.md` | Package design per side: validation tiers, execution order, testing discipline. |
| `handbook/` chapters and cross-cutting conventions | The methodology itself, per model, with source-page citations. |
| `specifications/**/*.spec.md` | Implementation contracts and convergence records: what matched the reference, to what ratio, under which decisions. |
| `inventory/asset-side-model-matrix.md` / `liability-side-model-matrix.md` | Status ledger per model: methodology at a glance, gates, outstanding items. |
| `handbook/open-questions.md` | The complete D- / PID- / OQ- registry. |

---

Reflects repository state as of 2026-08-14 (442 tests; unified `run.py` and
composed configuration). Convergence ratios and test counts are as recorded in
the repository's matrices and specification convergence records.

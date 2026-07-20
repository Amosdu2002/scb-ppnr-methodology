# Interest-Expense Calculation Framework — Design Note

Scope: the five proposed 2026 liability-side interest-expense models
(`ie_dom_time_dep`, `ie_other_dom_dep`, `ie_foreign_dep`, `ie_fed_funds_repo`,
`ie_other_borrowing`) as a generic Python package on canonical inputs and synthetic
data. The handbook chapters and YAML specifications are the implementation contracts;
this note covers only how the code realizes them. No confidential inputs, Excel
ingestion, MDRM lookup logic, asset-side models, or hedge calculations exist here.

Code: `src/scb_ppnr/interest_expense/` · Tests: `tests/` · Example:
`examples/run_synthetic_family.py` · Run: `python -m pytest tests/ -q` (stdlib-only
runtime; pytest is the sole dev dependency; `pythonpath` is configured in
`pyproject.toml`, so no install step is needed).

## Input contracts (`schemas.py`)

Model functions accept only canonical, validated, immutable inputs (frozen
dataclasses; mappings defensively copied behind read-only views). They cannot tell
whether a value originated in an Excel worksheet, an MDRM table, a CSV, a database,
or a test fixture — physical sourcing lives in the YAML specs' `fed_item` /
`project_mapping` layers and future input adapters, never in model code.

Canonical units, enforced at the schema boundary:

- balances: USD, `>= 0` (Other Borrowing total strictly `> 0` — share denominators);
- rates/spreads/betas: annualized decimal rates; a magnitude `>= 0.5`
  (`RATE_SCALE_GUARD`) is rejected as percent-scale leakage — percent→decimal
  normalization is metadata-driven at ingestion, never assumed in models;
- horizon: exactly PQ1..PQ9, ordered, no gaps or extras; `usd_3m_treasury` also
  carries PQ0 (consumed only by the A46 ΔTreasury3m seed at t=1, OQ-018);
- quarterly dollars: `balance × annualized_rate / 4`, applied once in
  `common.quarterly_expense` (D-004) and nowhere else;
- shares: in [0, 1] with `cp + subdebt <= 1` (violations surface, never clipped).

Parameters are published constants shipped as verified frozen instances:
`TABLE_A7_OTHER_DOM`, `TABLE_A7_FOREIGN` (median deposit betas + 25 bp ELB
threshold), `TABLE_A9_OTHER_BORROWING` (β1 = 0.254, β2 = −0.036, β3 = 0.066).
α_b is deliberately **not** a parameter — it is calibrated per firm (PID-OB-5).

## Model boundaries — five engines, deliberately not harmonized

| Module | Equation(s) | Engine |
|---|---|---|
| `ie_dom_time_dep.py` | A44 | WAL repricing recursion: ρ = 3/WAL_months ∈ (0, 1], `Rate_t = ρ·T1y_t + (1−ρ)·Rate_{t−1}`, seeded by the item 42E launch-point rate |
| `ie_other_dom_dep.py` | A45–A47 | two-regime deposit beta over {mma, savings, transaction}; expense multiplicand is a different physical source than the A47 weights (consistency monitor, 10 % [CODE] threshold — logs, never alters) |
| `ie_foreign_dep.py` | A45–A47 by reference | same engine over {foreign_nontime, foreign_time}; 35A+35B serve as both weights and multiplicand |
| `ie_fed_funds_repo.py` | A48 | direct calculator: rate = contemporaneous 3M Treasury, zero parameters |
| `ie_other_borrowing.py` | A53 + PID-OB-5 | OLS-coefficient rate + nine-quarter closed-form α calibration |

`deposit_regime_engine.py` is shared by exactly the two A45–A47 models — the Fed
states foreign reuses the other-domestic framework by reference, so one code path is
the faithful design; it is never reused for A44/A48/A53. Engine details: ELB when
Treasury3m < 25 bp (A45 is an equality — no floor; sub-floor/negative rates legal,
logged); non-ELB when above; exactly-25 bp is unassigned in the source (OQ-013) and
takes the documented non-ELB working branch with a logged event;
`first_elb_treasury3m` is the first sub-threshold observation of the supplied
scenario path scanned PQ0→PQ9, else the threshold ([CODE] choice: PQ0 is scanned as
part of the supplied series).

Only genuinely common operations are shared (`common.py`): the single ÷4 conversion,
projection-path helpers, result assembly, firm/scenario alignment checks.

## Execution order and the Other Borrowing calibration (`orchestrator.py`)

`run_interest_expense_family(FamilyInputs, ScenarioPaths) -> FamilyResult`:

1–4. The four structural/deposit models — mutually independent (no Fed-suite model
     consumes another's output); order immaterial, parallelizable.
5.   `implied_other_borrowing_path`: ImpliedOB(q) = FRBTotal(q) − the four completed
     expense paths, q = 1..9 (alignment-checked; negative quarters legal, logged).
6.   `calibrate_alpha_b` (PID-OB-5, closed form — the objective is linear, no
     optimizer): with R0 the pre-α A53 rate and B the (flat) balance path,
     `α_b = (4·Σ ImpliedOB − Σ B·R0) / Σ B` — one α per firm, constant PQ1..PQ9;
     betas untouched; no floor/cap; `Σ B` zero or invalid raises, no fallback.
7.   `project_other_borrowing`: R(q) = R0(q) + α_b; expense = B·R/4. Guards verify
     the calibration corresponds to these exact inputs/scenario.
8.   Reconciliation: Σ of all five components over PQ1..PQ9 equals the FRB
     nine-quarter cumulative total — exact by construction, asserted within a
     1e-9-relative float tolerance; only the cumulative matches, and the per-quarter
     modeled-vs-implied differences are preserved as diagnostics.

No circular dependency: Other Borrowing consumes the four finished paths plus the
project-supplied `frb_total_interest_expense` (physical source OQ-023), never the
reverse. PQ0 actual expense is never used and has no field anywhere in the API
(PID-OB-5 superseded the PID-OB-1/PID-OB-3 backsolve).

## Validation approach

Two tiers, per the conventions chapter:

- **Hard failures raise `ValidationFailure`** — missing/extra quarters, percent-scale
  rates, non-finite values, share/balance violations, subcomponent-set mismatches,
  zero A47 weights, zero cumulative calibration balance, misaligned firm/scenario
  identities, calibration/input mismatches, reconciliation breaks. No fallback is
  ever substituted; nothing defaults silently.
- **Log, never clamp** — negative rates, ELB sub-floor rates, negative Treasury3m,
  negative implied Other Borrowing quarters, the ==25 bp regime boundary, the
  |α_b| magnitude screen, the ODD dual-balance divergence monitor. These land in
  `warnings` on the result (`validation_status: "passed_with_warnings"`), with
  values always preserved.

## Output contract

Every model returns a `ModelResult`: `model_id`, `firm_id`, `scenario_id`, exactly
nine ordered `QuarterResult`s (`quarter`, `annualized_rate`, `average_balance`,
`quarterly_expense`, typed per-model `diagnostics`), `validation_status`, `warnings`.
Per-model diagnostics carry the traceability intermediates named in the specs
(dom-time: WAL months/quarters, ρ, lagged rate, 1Y Treasury; deposits:
per-subcomponent regime, applied beta, ΔT3m, spread, floor, floor-binding flag,
unfloored rate; fed-funds: balance components, 3M Treasury; Other Borrowing: term
contributions, R0, α_b, implied vs modeled expense and their difference). The family
adds `AlphaCalibration` (both quarterly paths, differences, cumulative
reconciliation) and `FamilyReconciliation`.

## Future adapter boundaries

- **Excel / MDRM ingestion**: a future input-adapter layer materializes the schema
  types from physical sources using the YAML `project_mapping` / MEV-workbook
  configuration (PID-5 pattern; PID-OB-4 BBB gates; OQ-023 FRB-total source). No
  workbook path, sheet name, or MDRM lookup may appear inside model code.
- **Hedge adjustment (Section v.c, Eqs A49–A51)**: external and downstream. All
  outputs here are pre-hedge expense paths; each model only *exposes* its path
  (OQ-005 allocation open; the calibrated α_b already absorbs the residual to the
  FRB total, including any embedded hedge effects — double-counting caution).

## Tests

Synthetic and deterministic; at least one hand-calculable fixture per model
(documented in each test module's docstring): dom-time WAL 12 → ρ 0.25, PQ1 2.5 %;
ODD Table A7 hand path incl. floor binding at 0.0025; foreign time-beta 1.000
one-for-one tracking; fed-funds 1000 × 4 % / 4 = 10; Other Borrowing α_b =
(4·180 − 9000·0.06504)/9000 with an exact nine-quarter match and unequal quarterly
paths. Integration: full family run reconciling to the FRB total, determinism, and
input immutability.

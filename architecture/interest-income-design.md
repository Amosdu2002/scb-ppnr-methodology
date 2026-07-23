# Interest-Income Python Design (asset side)

Started at asset-side Increment 1, 2026-07-23 (Family A code). Companion to
`architecture/interest-expense-design.md`; the roadmap and gate decisions live in
`inventory/asset-side-model-matrix.md`, the methodology conventions in
`handbook/cross-cutting/asset-side-common-conventions.md`.

## Core extraction (2026-07-23, refactor-only commit)

The side-neutral conventions moved verbatim from `interest_expense` to
`src/scb_ppnr/core/`: validation vocabulary (`ValidationFailure`, `check_*`,
`freeze_path`, `require_id`), the PQ grid constants, `RATE_SCALE_GUARD`
(`core/schemas.py`); the single D-004 ÷4 (`quarterly_flow`), path helpers, the
generic `build_result(result_cls, …)` and Protocol-typed `require_same_run`
(`core/common.py`). `interest_expense` re-imports everything under its
established names (`_finite`, `_require_id`, `quarterly_expense` aliases), so its
public API is unchanged. **Gate held: the full suite stayed green with zero
test-file edits** — the expense goldens are bit-exact, so green is proof of
behavioral identity. Core holds conventions, never model semantics: scenario
containers, inputs, parameters, engines, and result types stay in their family
packages.

## Package layout

```
src/scb_ppnr/interest_income/
  __init__.py            public API, grows per increment
  schemas.py             IncomeScenarioPaths (4 series), Family A inputs,
                         diagnostics, IncomeQuarterResult / IncomeModelResult,
                         IncomeFamilyInputs (grows per increment)
  common.py              quarterly_income = core.quarterly_flow; build_income_result
  ii_dep_banks_other.py  Eq A39 calculator (mirror of ie_fed_funds_repo)
  ii_other_ida.py        Eq A43 two-rate blend calculator
  securities_engine.py   Increment 2 — ONLY the Fed-shared three-term template
  ii_ust.py / ii_mbs.py / ii_other_sec.py     Increment 2 — thin models over the engine
  loans/                 Increment 3 — subpackage: schemas, rate_machinery (A33–A38),
                         segmentation (six portfolio definitions as data), ii_loans
  nii_trading_al.py      Increment 4 — mirrors ie_other_borrowing's factoring
                         (pre-α path → calibrate → project); calibration policy
                         isolated in one function so the Increment 4 gate decision
                         (launch-point backsolve vs cumulative calibration) is a swap
  orchestrator.py        Increment 4 — INCOME_MODEL_EXECUTION_ORDER, trading NII last;
                         reconciliation ships MONITOR-mode vs frb_total_interest_income
  reporting.py           Increment 4 — USD MILLIONS, pre-hedge labels
```

Sharing rule (deposit-engine precedent, asset conventions §1/§11): **share exactly
what the Fed shares** — the securities three-term template within Family B and the
A33–A38 machinery within loans; the two Family A calculators stay independent
modules despite their similar form; nothing is harmonized across families.

## Result types — parallel, not generalized

`IncomeQuarterResult` / `IncomeModelResult` deliberately parallel the verified
expense shapes (same six-field positional contract consumed by
`core.build_result`) rather than renaming the expense fields or introducing a
generic `amount`: the verified expense classes stay untouched, and the sides
differ where it matters — `quarterly_income` has **no sign constraint** (trading
NII is legitimately negative) and rate/balance are Optional (the securities
template has no single balance × rate decomposition; the true decomposition lives
in typed diagnostics). The eventual combined-NII layer always knows which side it
holds and calls `expense_path()` / `income_path()` explicitly.

## Scenario container

`IncomeScenarioPaths` carries all four family series from day one
(`usd_3m_treasury` over PQ0..PQ9 — the securities floating-margin imputation
needs the t = 0 spot; `usd_10y_treasury`, `prime_rate`, `mortgage_rate` over
PQ1..PQ9), mirroring the expense precedent of requiring the full family set and
avoiding constructor churn when later families land. Pre-PQ0 **history** never
enters the container — the Eq A37 wholesale-spread anchors are supplied
launch-point firm inputs (the `elb_spread` precedent). New MEVs are config-only
(`[mev.series.*]`); `MevScenario.interest_income_scenario_paths()` sits beside
the expense selector.

## Ingestion growth (additive per family)

One physical spot/quarterly sheet pair serves both families; the loader
registries are data, and each loader consumes only its own rows. Increment 1
added two `_PLAIN_FIELDS` entries and `load_income_inputs()` (spot sheet only).
Planned: Increment 2 — closed subcomponent bucket sets per securities model via
the existing `subcomponent` mechanism; vendor-prepayment and hedge terms as
declared quarterly input paths; a reserved third `[firm_data.positions]` sheet if
security-level granularity is ever chosen (never a change to the two existing
sheets). Increment 3 — compound segment ids and the one real loader surgery
(subcomponents on quarterly rows for the time-varying `wt` paths), preceded by a
message-pinning test commit and a pure-move split of parse machinery into
`firm_sheets.py`. Increment 4 — `nii_trading_al` spot inputs;
`family`/`frb_total_interest_income` already loads today.

## Testing

Same discipline as the expense side: hand-calculated golden fixtures per model
(dep-banks: 1000 × 4%/4 = 10; other-IDA: 2000 × [0.6·4% + 0.4·5%]/4 = 22 with
12 + 10 legs), structural invariants (proportionality, blend bounds,
bilinearity, flat balance/share), log-never-clamp warning coverage, and a
file-driven integration test reproducing the goldens from the committed
synthetic CSVs. The expense suite is frozen-verified: any refactor touching
shared code must keep it green with zero test edits.

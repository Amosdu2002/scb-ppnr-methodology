# Liability-Side Common Conventions

> **STATUS: The underlying models are proposed for the 2026 stress test — public-comment stage, NOT adopted.**
> Created at the liability-side integration gate, 2026-07-17. Scope: the five interest-expense
> models `ie_dom_time_dep`, `ie_other_dom_dep`, `ie_foreign_dep`, `ie_fed_funds_repo`,
> `ie_other_borrowing`. This chapter records only conventions genuinely shared across those
> models; individual model equations live in the model chapters and are **not** repeated here.
> Navigation: `inventory/liability-side-model-matrix.md`. Decisions cited (D-/PID-) are
> user-confirmed project implementation decisions registered in `handbook/open-questions.md` —
> never attributable to the Federal Reserve.

## 1. Launch-point terminology (D-005)

- **Launch point (PQ0)** is the handbook's term for the last quarter before the projection
  horizon. The source's own words — "lift-off", "jump-off quarter", "$q0$", "$t=0$" — are
  preserved verbatim inside quotations and equation transcriptions and are never rewritten.
- Coding identifiers use the `_launchpoint` suffix for PQ0 snapshots.
- Projection quarters are t (or q) = 1…9 — the nine-quarter horizon (FACT, PDF p. 6; md sec-2).

## 2. Canonical inputs and normalization

- Scenario series carry shared canonical names across models: `usd_3m_treasury`,
  `usd_1y_treasury`, `bbb_corporate_yield`. Firm inputs are model-prefixed; primary outputs end
  in `_interest_expense`.
- **Rate-scale normalization**: whether a raw rate is percent or decimal is metadata-driven at
  ingestion, never assumed, and applied identically to firm-reported rates and MEV series before
  any model logic (regime triggers such as the 25 bp ELB threshold must be expressed in the
  normalized scale). [CODE]
- Physical scenario sourcing follows the PID-5 pattern — an MEV workbook with a Date column and
  one column per MEV. Confirmed column name so far: "USD 1Y Treasury" (`ie_dom_time_dep`). The
  3-month Treasury and BBB column names are **UNCONFIRMED** working assumptions (the BBB input
  additionally carries the four PID-OB-4 confirmation gates).

## 3. Annualized rates and the single ÷4 (D-004)

- All interest rates in the project are **annualized**; model equations and recursions operate
  entirely in annualized units.
- A quarterly dollar expense divides the annualized rate by four **only at the final
  quarterly-dollar conversion step** (simple nominal quarterization, not effective compounding).
  Nothing is divided by four inside any recursion, regression, spread, or regime logic.
- The same convention runs in reverse where a quarterly actual is annualized (the
  `ie_other_borrowing` backsolve: R_actual = 4 × PQ0 expense ÷ PQ0 balance, PID-OB-3).
- This convention is a project implementation decision (OQ-006 resolution). The source states
  **no** annual→quarterly conversion for any of the five components — a preserved fact of
  absence; where the source states its own conversion elsewhere (securities ÷4, hedge N/360,
  trading-NII ÷4), the source statement governs.

## 4. Projection-quarter alignment

- Scenario paths are aligned to PQ1…PQ9 per scenario, with no gaps, before any model runs.
- PQ0 scenario values are consumed only where a model's mechanics require them: the ΔTreasury3m
  seed at t = 1 in the Equations A45–A47 models (INT, OQ-018) and the `ie_other_borrowing`
  backsolve. `ie_dom_time_dep` seeds from firm data (item 42E), and `ie_fed_funds_repo` needs no
  PQ0 value at all — these differences stay explicit per chapter.
- Outputs are dimensioned firm × scenario × quarter.

## 5. Separation of data retrieval from model calculation

- Every input carries two layers, kept separate in chapters and specs: the **Fed-stated** source
  (`fed_item` — or UNKNOWN as a preserved fact of absence) and the **project physical mapping**
  (`project_mapping`, PID-labeled, user-confirmed). The physical layer governs implementation;
  the Fed-stated layer is never silently corrected (e.g. PID-FFR-1, PID-OB-2 preserve the
  source's 44A/44B and 44C/46/47 wording as FACT while mapping physically to 36A/36B and
  36C/38/39).
- Model calculation consumes canonical inputs only; retrieval, normalization, and mapping happen
  before the model layer. No model reads a raw report field directly.

## 6. Common validation principles

- Required inputs present per firm; a failure **surfaces as an error — no fallback value is
  invented** and nothing defaults silently.
- Supplied parameters (Table A7 betas, Table A9 coefficients) are verified against the PDF page
  values, never retyped copies; significance stars are metadata, never numeric inputs.
- Edge monitors **log, never clamp**: negative projected rates, ELB sub-floor rates, sign flips
  under negative scenario rates are legal model outputs wherever no constraint exists in the
  source.
- Flat-balance and constancy invariants are asserted (balances identical across quarters; frozen
  shares; constant ρ/betas/spreads).

## 7. Cross-cutting hedge-adjustment boundary (OQ-005)

- None of the five models contains a hedge term (FACT — absence in each section). Each model
  **exposes its expense path** and computes no hedge adjustment internally.
- The proposed Section v.c adjustment (Equations A49–A51; qualified accounting hedges;
  contingent on the proposed FR Y-14Q B.2/B.3 collection; PDF pp. 220–223) is a separate,
  cross-cutting calculation owned by the planned hedge chapter. Two data states are presented in
  every chapter: current (no component-level adjustment computable) and proposed-collection
  (v.c computable).
- Allocation of the v.c adjustment across components is unresolved — **OQ-005, OPEN**.
- `ie_other_borrowing` caveat: the Fed's rationale says α_b absorbs cross-firm hedging
  intensity, so applying v.c to that component later risks double counting [CODE].

## 8. What is deliberately not shared

The five models keep four distinct calculation forms (WAL recursion; two-regime beta ×2 — one by
reference; direct calculator; OLS regression), different scenario drivers, different balance
sourcing, and different parameter sets. See `inventory/liability-side-model-matrix.md` §3 —
these are genuine methodology differences and must never be harmonized into a common formula.

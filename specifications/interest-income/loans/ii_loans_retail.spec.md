# Computation Spec — Interest Income on Loans: Retail Families (`ii_loans` — retail)

> **STATUS: implementation spec for the PROPOSED 2026 model — the Federal Reserve model is
> at public-comment stage, NOT adopted.** Fed methodology lives in the five approved retail
> source briefs (`handbook/models/ii_loans_retail.source-brief.md` + the four family briefs,
> all APPROVED 2026-08-13); this spec records the **project implementation** — the
> PID-LOAN-26..34 constructions — for the code in `src/scb_ppnr/ingestion/retail_loader.py`
> and `src/scb_ppnr/interest_income/loans_retail.py`. Every divergence from the Fed text is
> in §7. **Review state: DRAFT — awaiting user review; the first company compare arbitrates
> the flagged working assumptions (§8).**
> Canonical units: USD millions, annualized decimal rates, PQ0 = launch quarter (D-004/D-006).
> No firm values, no institution names — those stay in the gitignored local config.

## 1. Scope and engines

Four families, each enabled by naming its sheet in `[firm_data.loans]`; all reuse the
wholesale Equation A33/A38 machinery (`loans_projection.project_variable_rate` /
`project_fixed_rate`) — engines are wired per family, never re-derived:

| Family | Engine(s) | Base rate | Grain |
|---|---|---|---|
| Mortgage | fixed (A38) + variable (A33) per block | **mortgage rate for ALL blocks incl. HELOC** (PID-LOAN-33 as amended, round 1 — diverges from the Fed's HELOC-on-Prime register entry, §7.7; OQ-040 resolved-for-project) | {first lien, home equity, HELOC} × {HFI, FVO/HFS} × {fixed, variable} — 12 segments (PID-LOAN-27) |
| Auto | fixed only (A33 never runs) | Prime | New / Used vehicle (PID-LOAN-29) |
| Card | variable only (A38 never runs) | Prime | consumer / SME × bank / charge (PID-LOAN-28) |
| Other consumer | variable only, floored at zero | Prime | product types: A.7 + A.9 sub-products + the M.1-direct rows (PID-LOAN-30) |

## 2. Input contract (all company-local config; multi-workbook per PID-LOAN-31)

**Workbook topology (user-stated 2026-08-13):** the retail sheets live in their **own
workbook**, separate from the wholesale one; the auto pivot in a **third** file. Per sheet
the loader resolves: its `*_workbook` override → `retail_workbook` → the main workbook;
relative paths resolve against the main workbook's directory. Retail reads its own
`retail_m1_sheet` ("M.1 Balances") and `retail_mev_sheet` ("MEV Data") — never the wholesale
`m1_sheet`/`mev_sheet`.

| Input | Sheet (config key) | What is read |
|---|---|---|
| M.1 retail rows | `retail_m1_sheet` (in `retail_workbook`) | Twelve rows matched by their **M.1 line labels** (label column, default C); values E/G/I/K per side, millions; the per-side **role labels** (cols A/B) are cross-checked — they are the wiring authority (PID-LOAN-26). Family multiplicands: mortgage = first-mortgages / HELOAN-pair / HELOCs rows per side; card = bank + charge + SME-cards rows; auto = auto-loans row; noncore = the four dom-noncore rows + the international side of every retail row. Lease rows are excluded (role-less, zero) |
| Mortgage query | `mortgage_query_sheet` (+`_workbook`) | The **first** launch block (Lien Position / Loan Type=classification / Interest Rate Type / TOTAL_UPB $ / WEIGHTED_AVERAGE_RATE / WEIGHTED_AVERAGE_RATE_AFTER_<yyyymmdd> ×2 / WEIGHTED_ARM_FLOOR) and the **first** PQ-schedule block — the MORT variant (PID-LOAN-33); the alternative classification blocks are ignored, censused. `"x"` = missing (PID-LOAN-27) |
| Card query | `card_query_sheet` (+`_workbook`) | Rows ids 1–4 (consumer/SME × bank/charge); TOTAL_OS, APR/spread pairs (all-book + revolver-only, percent), TOTAL_OTST_REVOLVER; WEIGHTED_MAX_APR carried, **never applied** (card brief §0.2 (k)) |
| Auto pivot | `auto_pivot_sheet` (+`_workbook`, typically a separate file) | Summary rows New/Used(/leases) anchored at the label column (default L): M/N/O = outstanding (millions) / average rate / **new-origination rate**; P..X = **supplied** re-origination weights PQ1..PQ9 (PID-LOAN-29 as amended) |
| Other-consumer products | `oc_sheet` (+`_workbook`) | The A.7/A.9 input rows (schedule tag + product type + balance + the workbook's own line-mapping token); balances give **shares only** — multiplicands stay M.1 (PID-LOAN-30) |
| Line-item rates | `line_items_sheet` (+`_workbook`; institution-named — config-local) | Each mapped line's **PQ0** value inside the *Average Rates Earned* section (scoped between the section header and *Total Interest Income*, so the balance/GII sections can never match); PQ0 column from the sheet's own PQ0..PQ9 header row |
| Scenario | `retail_mev_sheet` (in `retail_workbook`), columns `mev_prime_column` = "Prime rate", `mev_mortgage_column` = "Mortgage rate" | Percent; `Actual` history (launch value) + the scenario block mapped to PQ1..PQ9 **by date**. Retail needs no pre-PQ0 history — every retail spread is spot-measured |

## 3. Constructions (per family)

**Mortgage (PID-LOAN-27/33).** Per block: balance = M.1 sub-family row sum of its side ×
query-UPB shares (fixed vs variable). Fixed leg: Eq A38 seeded at the segment
WEIGHTED_AVERAGE_RATE; new-origination spread = window rate − base(PQ0), window per
`mortgage_window` ("quarter" = the earlier AFTER cutoff, production); wt(q) = maturing UPB(q)
÷ segment UPB (guarded ≤ 1); no fixed-leg floor. **Missing-window fallback:** a fixed segment
with "x" in the active window takes its **own current rate** as the new-origination rate
(PID-LOAN-33 working assumption — hardcoded query lineage, no formula to audit; censused per
segment). Variable leg: Eq A33 at spread = WAR − base(PQ0), floored at WEIGHTED_ARM_FLOOR — for HELOC:
max(mortgage(t) + spread, query floor), user-stated round 1, with the spread anchored per
`heloc_spread_anchor`: **"prime_pq9" (WAR − the terminal Prime) reproduces the reference
HELOC 4Q/9Q exactly and the calc sheet's rising 8.6/8.3/8.4 path** (round-2 arithmetic
identification — at a 4Q24 launch that anchor is NOT the launch Prime, so it may be a
workbook mislink to the other launch section's Prime PQ0; reproduce first, confirm with the
spread cell, and flag to the workbook owners if confirmed — the CRE grand-row precedent).
Block Total = (fixed + variable) × **1.014**.

**Auto (PID-LOAN-29/32).** Balances = M.1 auto row × pivot D_OS shares. Fixed leg per segment:
launch = column N; spread = column O (new-origination rate) − Prime(PQ0); wt = the supplied
P..X schedule; no floor. Block Total = Σ × `retail_auto_scalar` (**0.865 published,
user-directed**; the reference workbook's own panel applies 0.948 — a reference-matching run
sets "0.948", and at 0.865 the compare should expect auto Totals ≈ 0.91 of the reference).

**Card (PID-LOAN-28/34).** Per sub-segment: revolving balance = M.1 block balance × OS-share
within block × revolver share (TOTAL_OTST_REVOLVER ÷ TOTAL_OS — the 3-month finance-charge
condition only, the 12-month activity field NOT applied; flagged, compare arbitrates); rate(q)
= max(Prime(q) + spread, 0) with spread per `card_spread_mode` (**"reported"** = the Y-14M
FED_VAR_PURCH_APR_SPRD_RT column — production; the OQ-043 project answer). Income = revolving
balance × rate ÷ 4. Block totals × **0.969** (consumer) / **1.033** (SME — the merged
"C&I, noncore SME loan and card" row).

**Other consumer (PID-LOAN-30).** Every row variable at spread = line PQ0 rate − Prime(PQ0),
floored at zero. Blocks: US other consumer = M.1 OC-loans dom × A.7 shares (revolving
sub-products → the Credit Cards line; installment → the non-purpose line; Overdraft = zero
row); US small business = M.1 small-business dom × A.9 shares → the C&I line, scalar
**1.033**; the M.1-direct rows (all internationals per their M.1 rows, student dom+int,
non-purpose dom+int) → their closest lines, scalar **1.072** (as is every consumer row).

## 4. Outputs

Per family: blocks of streams (balance, launch rate, spread, rate path, unscaled income path)
and scaled Totals; `family_summary` = the 4Q-cum / 9Q-cum per family — the shape of the
results summary the compare targets (framework brief §0.2). Runner: censuses FIRST, then
per-block tables, diagnostics, and the RETAIL SUMMARY; `--retail-only` skips the wholesale run.

## 5. Validation and censuses (every run)

M.1 label matches exactly 1 per pattern (refuse otherwise) + role-label WARN cross-checks;
reconciliation monitors (never adjustments): mortgage query-UPB vs M.1 per block, auto pivot
vs M.1 (the sheet's own 0.9998-style cell), card OS vs M.1, A.7/A.9 sums vs M.1; fallback and
floor-bind counts; wt ≤ 1; line rates bounded [0, 1); empty sub-segments vacuous-and-censused;
lease rows excluded with a WARN if ever nonzero; unknown vocabulary (lien/side/rate-type/line
tokens, card ids) refused by name, never defaulted.

## 6. Fed-faithful points

Eq A32 income = balance × rate with the D-004 single ÷4; A33 spreads constant from PQ0; A36
measured on new originations at the jump-off (spot-only — no t−a history anywhere in retail);
A38 blend seeded at the balance-weighted launch rate; all-variable cards / all-fixed auto per
the stated Board assumptions; Prime-except-mortgages base rule (p. 185); flat balances; block
scalars constant every quarter (PID-LOAN-16 semantics).

## 7. Recorded divergences from the Fed text (project ↔ source)

| # | Divergence | Direction |
|---|---|---|
| 1 | Mortgage wt is **maturity-only** (the query schedules) where the Fed derives wt from default + prepayment + maturity (p. 183) — for a prepayment-dominated family this understates re-origination most of all the loan parts (OQ-001 source side open) | fewer re-originations → carried rate dominates |
| 2 | Other consumer runs **all-variable** where p. 183 counts "most non-core loans" as fixed (OQ-041 source side open) | full repricing sensitivity |
| 3 | Card revolver share applies the **3-month condition only**; the Fed's rule adds 12-month activity (p. 179) — flagged, compare arbitrates | share ≥ the Fed's construction |
| 4 | Auto scalar = published **0.865** while the reference workbook's own panel applies 0.948 (PID-LOAN-32, user-directed) — a compare-basis divergence, not a Fed one | auto Totals ≈ 0.91 × reference |
| 5 | The missing-window fallback (own current rate as the new-origination rate) is a project convention; the Fed defines no empty-window behavior | spread ≈ 0 vs base for those segments |
| 6 | Line-item jump-off rates come from a projections-format sheet's PQ0 column; the Fed says "the FR Y-14Q pre-provision net revenue line-item report" (OQ-011 source side open) | as observed in the workbook |
| 7 | **HELOC reprices on the MORTGAGE rate** (round-1 elicitation, user-stated) where the Fed's base-rate register puts HELOC on **Prime** (PDF p. 181) | HELOC keeps a mortgage-rate sensitivity |

## 8. Open items for the first compare round

(a) the flagged assumptions above (esp. §7.3 card share and §3's window/fallback settings);
(b) the mortgage fixed-leg floor (none implemented; Corporate's reference engine floors at 0 —
adopt if the compare shows it); (c) the results-sheet compare mode (round 1 uses the printed
RETAIL SUMMARY against the user's summary table via paste-back; a sheet reader follows if
wanted); (d) whether HFS/FVO mortgage blocks reproduce (the query "Loan Type" column is the
classification — naming trap documented in the loader).

## 9. Convergence record (compare vs the firm's reference results, 2026-08-13)

Three rounds, same-day. **Round 3: mortgage, card, and other consumer all match the
reference EXACTLY at the summary's display precision (family 4Q-cum and 9Q-cum ratios
≈ 1.000)** — mortgage converged under `heloc_spread_anchor = "prime_pq9"` (the round-2
arithmetic identification; the HELOC spread-cell reference confirmation is still owed) and
other consumer under the leftmost-PQ0-group fix (the sheet's header carries NINE PQ0..PQ9
groups; the rates live under the first). **Auto: ours/reference = 0.912 on both horizons —
scalar-only by construction**: the machinery reproduces the workbook's unscaled New/Old
streams, and the workbook multiplies by **0.948 — user-confirmed at the scalar cell (round 3)** — the
firm-computed true-up, not Table A8's published 0.865 that production uses per PID-LOAN-32;
`retail_auto_scalar = "0.948"` reproduces the reference exactly — **verification run
CONFIRMED by the user (round 4, 2026-08-13): all four families match** — and the
published-vs-computed inconsistency (auto alone off Table A8) is flagged for the workbook
owners. Production setting: the published "0.865" per the standing PID-LOAN-32 direction
(one config line flips the basis). **RETAIL CONVERGED.** Round-1/2 fix history: HELOC base and spread anchor
(§3); the line-item PQ-column anchoring (§2). Floor binds fell 82 → 27 once HELOC left the
Prime path (its ARM floor no longer binds).

## 10. Test anchors

`tests/unit/interest_income/test_loans_retail.py` — hand-computed goldens per family (A38
blend arithmetic, ARM-floor binds, own-rate fallback, revolver arithmetic, zero-floor binds,
scalar application, variant-block exclusion, window switch, M.1 label/role census, line-item
section scoping, MEV columns); `tests/unit/ingestion/test_retail_config.py` — the config keys.
Full suite green with zero edits to wholesale tests (387 passed at landing).

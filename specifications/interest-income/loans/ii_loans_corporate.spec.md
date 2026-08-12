# Computation Specification — Interest Income on Loans: Corporate (`ii_loans` — Corporate)

> **STATUS: The underlying Federal Reserve model is proposed for the 2026 stress test — public-comment stage, NOT adopted.**
> This document is a **project implementation specification**, not a description of Federal Reserve methodology. Every rule below is either a user-confirmed project implementation decision (PID-LOAN-*) or an explicitly flagged working assumption. Where it diverges from the Fed source, §7 says so in plain terms.
> Fed-side methodology lives in `handbook/models/ii_loans_common.source-brief.md`, `ii_loans_wholesale.source-brief.md`, and `ii_loans_corporate.source-brief.md`. PIDs are registered canonically in `handbook/open-questions.md`.
> Created 2026-08-03 from user-supplied implementation detail. Review state: **DRAFT — awaiting user review.** No code has been written against it.

---

## 1. Scope

Corporate wholesale loans only — the 11 Fed Categories of `ii_loans_corporate.source-brief.md` §3.1. CRE and Retail are out of scope for this document.

## 2. Input contract [PID-LOAN-8]

One workbook, multiple sheets. Layout is company-local configuration; only the logical contract is recorded here. **No confidential content appears in this repository.**

| Sheet | Supplies | Used by |
|---|---|---|
| **CORP H.1** | Facility-level records: `Interest Rate`, `Committed Exposure Global`, `Utilized Exposure Global`, `Interest Rate Floor`, `Maturity Date`, origination date, and the three mapping columns | §4, §5, §6 |
| **H.1 mapping** | The three-part reference key: Fed Category (1–11), Variable Type code (0–4), Lower-of-Cost-or-Market flag | §3 |
| **M.1 Balance** | Portfolio balance by category — the Equation A32 multiplicand | §6 |
| ~~**FRB Scalars**~~ | **No longer a workbook input** (user-directed 2026-08-07): the scalars are taken from the Federal Reserve's **Table A8** directly (PDF p. 220), whose seven values are identical to the sheet's FRB column. Removes a parsing dependency and a chance to drift from the published values | §6 |
| **MEVs** | 3-month Treasury path for PQ1–PQ9 **and history back to 1976 Q1** (§5.2) | §5 |
| **FR Y-9C** | Category reconciliation at the launch point | validation |

**Units — TO_BE_CONFIRMED, refuses to run while unconfirmed** (D-006 discipline): whether `Interest Rate` and `Interest Rate Floor` are percent or decimal, and the money scale of the exposure and balance columns. Never inferred from magnitude.

## 3. Segment key [PID-LOAN-2]

```
segment = Fed Category (1–11) × LOCOM flag {HFI, HFS} × Variable Type code {0,1,2,3,4}
```

The LOCOM flag is the physical realization of the Fed's HFI versus FVO/HFS asset classification. Rate pools and spreads are computed **per Fed Category × LOCOM**, separately for each rate type — i.e. Commercial and Industrial is split into HFI and HFS, and within each the five rate types are handled separately.

Variable Type vocabulary [FACT of the data]: `0` = DO NOT USE, `1` = Fixed, `2` = Floating, `3` = Mixed, `4` = Entry Fee Based. **There is no demand-loan code**, so the Fed's "demand loans are treated as variable-rate" rule has no counterpart in this data and is recorded as inapplicable rather than mapped.

## 4. Initial interest rates — rate pools [PID-LOAN-3]

Per Fed Category × LOCOM, over rows whose `Interest Rate` is populated. **A row with `Interest Rate` NA or [NULL] leaves both the numerator and the denominator** — it never dilutes the average toward zero.

```
FloatPoolRate = Σ(Committed Exposure Global × Interest Rate)  over v ∈ {2 Floating, 3 Mixed}
              ÷ Σ(Committed Exposure Global)                  over v ∈ {2 Floating, 3 Mixed}

FixedPoolRate = Σ(Committed Exposure Global × Interest Rate)  over v ∈ {1 Fixed}
              ÷ Σ(Committed Exposure Global)                  over v ∈ {1 Fixed}
```

Note the weighting field is **committed** exposure, while §6's wt uses **utilized** exposure. Both are as specified; the column name is carried explicitly everywhere so the two are never conflated.

## 5. Spreads [PID-LOAN-4]

### 5.1 By rate type

| Rate type | Initial rate used | Base rate subtracted | Spread |
|---|---|---|---|
| `2` Floating | FloatPoolRate | 3M Treasury at **PQ0** | FloatPoolRate − 3M(PQ0) |
| `1` Fixed | FixedPoolRate | 3M Treasury at the **median origination quarter of the v=1 rows** | FixedPoolRate − 3M(median orig quarter, v=1) |
| `3` Mixed | **FixedPoolRate** | 3M Treasury at the **median origination quarter of the v=3 rows** | FixedPoolRate − 3M(median orig quarter, v=3) |
| `0`, `4` | — | — | none — no income (§6.4) |

Mixed is deliberately hybrid: its exposures and rates feed the **Floating** pool, while its own spread is built from the **Fixed** pool's rate less **its own** median-origination base rate. The economic reading is that a mixed loan's current rate was set during its fixed period, so the fixed pool is the better level proxy, while its own origination timing sets the reference date.

### 5.2 Median origination date → base rate

A median origination **month** maps to its calendar quarter, and that quarter's 3M Treasury is used (e.g. May 2022 → 2022Q2). This is the project's operationalization of the Fed's Equation A37 `t−a`.

**History coverage and fallback [PID-LOAN-4, amended 2026-08-03 — user-directed].** The MEV sheet supplies the 3M Treasury back to **1976 Q1**. If a segment's median-origination base rate cannot be found, the base rate **defaults to 0**.

Two distinct causes produce a lookup miss, and they are counted separately because 1976 Q1 coverage only addresses the first:

| Cause | Expected frequency | Handling |
|---|---|---|
| Median origination quarter lies outside the MEV range | Near zero — a corporate book holds nothing originated before 1976, so this fires only on a corrupt or future-dated origination date | base rate = 0, counted |
| The origination date itself is missing, unparseable, or the segment has no rows with dates | The realistic trigger | base rate = 0, counted; an entirely empty segment produces no income regardless |

**Consequence, stated plainly because it is not neutral:** with the base rate at 0 the spread collapses to the full pool rate, `Spread = FixedPoolRate − 0 = FixedPoolRate`, so the projected new-origination rate becomes `3M(t) + FixedPoolRate` — higher than intended by roughly the level of the base rate that should have been subtracted. On a 6 % pool rate against a 4 % historical base, the new-origination rate is overstated by about 4 percentage points for that segment. The fallback is therefore implemented as specified but **never silently**: §8 requires a per-run census naming every affected segment, its cause, and the exposure behind it, so a fallback that fires on a material segment is visible on the first run rather than discovered in reconciliation.

## 6. Projection

### 6.1 Variable engine — rate types `2` and `3`

```
IR(segment, t) = max( 3M(t) + Spread(segment), Floor(segment) )        t = PQ1…PQ9
```

Mixed projects here despite deriving its spread on the fixed convention: wt is scoped to the Fixed balance (§6.2), so Mixed has no re-origination weight and cannot run the Equation A38 blend. This also agrees with the Fed, which treats mixed-rate loans as variable-rate.

### 6.2 Fixed engine — rate type `1` [PID-LOAN-6]

```
wt(category, LOCOM, PQx) = Σ Utilized Exposure Global for facilities matching the reference key
                             whose Maturity Date falls in PQx
                           ÷ launch-point Fixed balance for that category × LOCOM
                             (HFI: Outstanding Balance · HFS: Value)

IR_new(t)      = 3M(t) + Spread(v=1)
IR(t)          = (1 − wt(t)) × IR(t−1) + wt(t) × IR_new(t)          Equation A38
IR(t)          = max(IR(t), Floor)                                   floor applied after blending
```

`IR(PQ0)` seeds from FixedPoolRate. The numerator column (`Utilized Exposure Global`) differs from the denominator column (`Outstanding Balance` / `Value`); §8 carries a first-run diagnostic comparing them so any mismatch surfaces as a number rather than a quietly mis-scaled wt.

### 6.3 Balances and output

```
segment balance     = M.1 portfolio balance(category) × segment share
segment share       = segment exposure ÷ total category exposure, over ALL rate types
                      including 0 and 4
quarterly income    = segment balance × IR(segment, t) ÷ 4          (D-004)
category income     = Σ over segments, × FRB scalar(category)
```

### 6.4 Rate types `0` and `4` — balance only, no income [PID-LOAN-5]

`0` (DO NOT USE) and `4` (Entry Fee Based) **count toward the total portfolio balance** — so they enter the share denominator and reduce every other segment's share — but they are **never incorporated into fixed income or variable income**. They contribute zero.

This supersedes two earlier readings taken during elicitation: that fee-based loans inherit the Floating pool's initial rate and earn income, and that v=0 income is `Σ(Utilized Exposure Global × Interest Rate Floor)`. Neither flows into income. If the workbook's v=0 floor column feeds anything downstream, the §8 reconciliation is where it will show up.

## 7. Divergences from the Federal Reserve source

Recorded so they are visible, never smoothed over. Each is a legitimate company convention; none is attributable to the Board.

| # | Fed source states | This implementation | Direction of effect |
|---|---|---|---|
| 1 | Fee-only loans' "outstanding balance percentages are excluded from the total balances calculation" (PDF p. 176) | `4` Entry Fee Based balances **stay in** the share denominator | **Lowers** projected income — income-earning segments receive smaller shares of the same portfolio balance |
| 2 | Fee-only loans "generate no interest income" and are "not used to calculate the average interest rate" (PDF p. 176) | Same — `4` earns nothing and is outside the rate pools | **Matches** |
| 3 | wt "is derived from the default rate, prepayment rate, and maturity rate" (PDF p. 183) | wt from **contractual maturity dates only**; no default or prepayment component | Understates re-origination where defaults and prepayments are material, so fixed-rate segments stay closer to their launch rates |
| 4 | The three data-limited portfolios take a bank-level NPML proxy spread (PDF p. 176) | Spreads computed directly from H.1 for **all 11** categories | Moot **if** categories 9–11 carry H.1 rows; §8 counts rows per category so this is answered on the first run |
| 5 | Mixed-rate loans "treated as variable-rate" (PDF p. 176) | Variable engine ✓, but the launch spread is derived on the **fixed** convention | Matches on projection; the spread derivation is a refinement the source does not describe |

## 8. Validation and first-run diagnostics

- **Row census by Fed Category × LOCOM × Variable Type** — answers divergence 4 above and shows whether any category is empty.
- **wt denominator check** — the launch-point `Outstanding Balance`/`Value` against Σ `Utilized Exposure Global` for the same Fixed rows; a material gap means the two columns are not the same quantity.
- **wt ≤ 1 per quarter** — a maturity concentration exceeding the launch-point Fixed balance makes Equation A38 a non-convex combination and `(1 − wt)` negative. Surface, never clamp silently.
- **Segment shares** sum to 1 within each category over all five rate types; validated in [0,1], never clipped.
- **Floor census by source** — counts of populated, zero, and NA/NULL/NONE floors, and how often a floor binds per segment-quarter. Direct lesson from PID-SEC-18, where a literal zero in a floor column silently overrode a real floor and cost several diagnostic rounds.
- **Rows dropped from rate pools** for missing `Interest Rate`, counted per segment, with their exposure — so a large silent dropout is visible.
- **Historical 3M coverage and base-rate fallback census** — the earliest median origination quarter required versus the earliest MEV quarter available (supplied from 1976 Q1), plus every segment that took the **base rate = 0** fallback, split by cause (outside MEV range · missing or unparseable origination date) with the exposure behind each. A fallback on a material segment overstates that segment's new-origination rate by the omitted base-rate level (§5.2), so this census is a required first-run output, not an optional log line.
- **Unmapped Variable Type or Fed Category values** — hard error, surfaced, never defaulted.

## 9. Open items

| Item | Status |
|---|---|
| Floors are per facility; the model projects one rate per segment | Working treatment: balance-weighted floor per segment with within-segment dispersion logged — **flagged, awaiting confirmation** |
| **Which rate carries forward through the Equation A38 recursion when a floor binds** | §6.2 says only "floor applied after blending". Implemented so the **floored** rate carries forward — a binding floor means the portfolio really is earning its floor, so the next quarter's carried component is that rate rather than a shadow value the loans never earned. The unfloored path is returned alongside so the cost of a bind is measurable. **Flagged decision, awaiting confirmation** |
| **Which exposure measure weights segment shares** | The Fed says "percentage of **outstanding** balance" (PDF p. 174), which points at utilized; the rate pools use committed. Implemented as a parameter defaulting to **committed**, for consistency with the pools. **Flagged, awaiting confirmation** |
| **Median origination date weighting** | Implemented as an unweighted row median (`median_low`, so the quarter is one a loan was really originated in). The Fed says only "the median origination date … for that portfolio" (PDF p. 182) — a balance-weighted median is the other defensible reading |
| Rows with NA `Interest Rate` leave the rate pool; their balances remain in the portfolio balance and so implicitly earn the segment rate | Flagged working assumption; the §8 dropout census quantifies it |
| Rate and money unit scales | **CONFIRMED 2026-08-07** (user-stated): H.1 rates/floors decimal; H.1 exposures whole dollars; M.1 millions; FR Y-9C thousands; MEV percent — all declared in `LoansSheetSpec` |
| **Mixed segment with no Fixed siblings in its category/LOCOM cell** | Mixed borrows the Fixed pool's rate (PID-LOAN-4); a cell holding Mixed rows but **no Fixed rows** has no pool to borrow, and the run **stops with a named error** rather than defaulting. What the workbook itself does in that case is UNKNOWN — surfaced by the synthetic demo 2026-08-12; ask if the first real run hits it |
| OQ-037 (NPML proxy data slice) | May be moot for this project — see divergence 4 |
| OQ-010 (scalar row → category mapping) | Open; the FRB Scalars sheet may resolve it physically |

## 10. Implementation status

| Layer | Module | State |
|---|---|---|
| Canonical containers | `interest_income/loans_schemas.py` | **Landed** — Variable Type vocabulary, pool membership, the two differing spread lookups, facility and segment containers |
| Launch point (§3–§5, §6.2 wt, floors) | `interest_income/loans_launchpoint.py` | **Landed** — pool rates, spreads, median-origination lookup with the zero fallback censused by cause, shares, floor collapse, wt |
| Projection (§6.1–§6.4) | `interest_income/loans_projection.py` | **Landed** — A33 variable engine, A34/A38 fixed engine, no-income routing, scalar roll-up |
| Diagnostics (§8) | both modules | **Landed** — base-rate fallbacks by cause, dropped rate rows by pool, floor dispersion, wt > 1, floor binds, negative rates, dormant balance, scalars applied |
| Reference-key decoding + Table A8 (PID-LOAN-9/11) | `ingestion/loans_mapping.py` | **Landed** — the two collapses (H.1 code→Fed Category many-to-one; LOCOM 3→2), `[NULL]` = DO NOT USE, the depository slice, the user-confirmed scalar assignment |
| Workbook binding (§2, PID-LOAN-8/10) | `ingestion/loans_loader.py` | **Landed** — CORP H.1 (header row 4), M.1 Balance (role columns A/B wire FR Y-9C lines to categories), FR-Y9C merged-bucket MDRMs, MEV history/projection split; four declared unit scales |
| Runner | `examples/run_loans.py` | **Landed** — synthetic demo + company run; censuses print before results; `--report` (gitignored `loans_report*.txt`) |
| Reference comparison | — | **Not started** — waits on whether the workbook carries reference results for loans (the securities `II_PQ` pattern) |

Tests: `tests/unit/interest_income/test_loans_launchpoint.py`, `test_loans_projection.py`, and `tests/integration/interest_income/test_loans_corporate_end_to_end.py` — synthetic inputs only, arithmetic worked by hand in the assertions.

## 11. PID index

| ID | Covers |
|---|---|
| PID-LOAN-1 | The three data-limited portfolios are floating (registered 2026-08-03) |
| PID-LOAN-2 | Segment key and computation granularity — §3 |
| PID-LOAN-3 | Rate pools and initial interest rates — §4 |
| PID-LOAN-4 | Spread construction by rate type, median-origination base rate — §5 |
| PID-LOAN-5 | Engine assignment; `0`/`4` balance-only treatment — §6.1, §6.4 |
| PID-LOAN-6 | wt from contractual maturities — §6.2 |
| PID-LOAN-7 | Interest-rate floors from H.1 — §6, §9 |
| PID-LOAN-8 | Corporate input contract — §2 |

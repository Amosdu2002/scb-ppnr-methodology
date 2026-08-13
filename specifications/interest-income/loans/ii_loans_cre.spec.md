# Computation Specification — Interest Income on Loans: CRE (`ii_loans` — CRE)

> **STATUS: The underlying Federal Reserve model is proposed for the 2026 stress test — public-comment stage, NOT adopted.**
> This document is a **project implementation specification**, not a description of Federal Reserve methodology. Every rule below is either a user-confirmed project implementation decision (PID-LOAN-18..25, all confirmed 2026-08-12) or an explicitly flagged working construction. Where it diverges from the Fed source, §7 says so in plain terms.
> Fed-side methodology lives in `handbook/models/ii_loans_cre.source-brief.md` (APPROVED 2026-08-12) and its common/wholesale parents. PIDs are registered canonically in `handbook/open-questions.md`.
> Created 2026-08-12 alongside the engine extension. Review state: **DRAFT — awaiting user review.** Code is landed and green (§10); the reference compare awaits the first real run.

---

## 1. Scope

CRE wholesale loans only — the four workbook categories of PID-LOAN-19 realizing the Fed's six CRE portfolios (`ii_loans_cre.source-brief.md` §3–§4). Corporate and Retail are out of scope for this document. **The CRE construction is deliberately NOT either Corporate engine** (`pid` / `reference`): the two wholesale parts differ on evidence, per PID-LOAN-22/23, and the code keeps them separate (`build_cre_launch_point`).

## 2. Input contract [PID-LOAN-18 / PID-LOAN-20]

Same single workbook as Corporate; the CRE run is **enabled by naming the H.2 sheet** (`cre_h2_sheet` in `[firm_data.loans]`) and stays off otherwise. **No confidential content appears in this repository.**

| Sheet | Supplies | Used by |
|---|---|---|
| **CRE H.2** (header row 4) | Facility-level records: `Interest Rate`, `Committed Balance`, `Outstanding Balance`, `Interest Rate Floor`, `Origination Date`, `Maturity Date`, `Line Reported on FR Y-9C` (alias "…FR Y9C" accepted and reported), `Interest Rate Variability`, `Lower of Cost or Market Flag`. Identifier columns are optional — the PID-LOAN-12 chain applies where present; otherwise rows are labeled `UNIDENTIFIED-ROW-<n>` and censused. **No `Utilized Exposure Global` exists on H.2**; the facility's utilized field is carried as 0 and nothing may weight by it | §3–§6 |
| **M.1 Balance** | The Eq A32 multiplicand, wired **by row** (PID-LOAN-20): E/G of the construction / multifamily / non-owner-occupied rows (company sheet: 17 / 18 / 21, config `cre_m1_*_row`) = each domestic category's HFI / HFS-FVO balances; the merged international category = Σ I/K over the same three rows. Blank cells are genuine zeros (the international HFS/FVO side is empty in the company book). The role labels on the configured rows are printed, and a row whose role does not look like "Wholesale - CRE" earns a WARN | §6 |
| **MEVs** | 3-month Treasury path PQ1–PQ9 **and history** (shared with Corporate; the weighted origination quarters need the same depth) | §5 |
| ~~FRB Scalars~~ | Not an input: Table A8 values are read from the source (PID-LOAN-11 pattern); the CRE assignment is PID-LOAN-21 (§6.4) | §6 |
| **CRE results sheet** (optional, `cre_results_sheet`) | The workbook's own CRE projected income for the compare: blocks `1 - HFI` … `4 - HFS/FVO` (no merged block), Fixed Income / Variable Rate Income / Total rows over PQ0..PQ9 | compare |

**Units:** the loader reuses the `[firm_data.loans]` scales confirmed for Corporate on 2026-08-07 (rates/floors decimal; exposures whole dollars; M.1 millions; MEV percent). **The H.2 columns are presumed to share them (same workbook) — confirm on the first real run's censuses before reliance** (D-006 discipline; §9).

## 3. Segment key and mapping [PID-LOAN-19]

```
segment = CRE category (1–4) × LOCOM {HFI, HFS/FVO} × Variable Type {0,1,2,3,4}
```

Key composed exactly as Corporate's: `{Line Reported on FR Y-9C}_{Interest Rate Variability}_{LOCOM}`. LOCOM and Variable Type vocabularies are identical to H.1 ([NULL] = DO NOT USE; **no demand-loan code** — the Fed's demand rule is again inapplicable, OQ-035 physical note).

Line-code mapping (the firm's "H.2 Mapping" sheet, user-supplied 2026-08-12):

| H.2 code | CRE category | Note |
|---|---|---|
| 1, 2 | 1 — CRE Dom construction | many-to-one, like the H.1 collapses |
| 3 | 2 — CRE Dom multifamily | |
| 5 | 3 — CRE Dom non-owner-occupied | |
| 7 | 4 — **CRE International (Fed 4-6 merged)** | one code for ALL non-domestic CRE ex-owner-occupied: the Fed's three international portfolios are **data-indistinguishable** and modeled as one merged category — a recorded, data-forced divergence (§7.1) |
| 4, 6 | **DO NOT USE** | outside every CRE category: excluded and censused with exposure, never decoded, never allocated balance (working reading: the owner-occupied lines, already Corporate's) |

An unknown code (outside 1–7) is a hard error. The Fed-side census — six portfolios, stated 24 segments — is preserved in the brief; outputs label the merged block as Fed portfolios (4)–(6).

## 4. Initial interest rates — rate pools

Per CRE category × LOCOM, identical machinery to Corporate (PID-LOAN-3 pattern; `compute_pool_rates` reused): Float pool = {2 Floating, 3 Mixed}, Fixed pool = {1 Fixed}, weighted by **Committed Balance**; a row with NA/[NULL] `Interest Rate` leaves both sides. **The committed weighting is residual item (i)** — observed on the CRE launch sheet (initial rate = exposure×rate ÷ launch-point committed balance) but not yet user-confirmed in words (§9).

## 5. Spreads [PID-LOAN-22 / PID-LOAN-23]

| Rate type | Initial rate used | Base rate subtracted | Spread |
|---|---|---|---|
| `2` Floating | FloatPoolRate | 3M Treasury at **PQ0** | FloatPoolRate − 3M(PQ0) |
| `1` Fixed | FixedPoolRate | 3M at the v1 rows' **outstanding-weighted median origination quarter** | FixedPoolRate − 3M(weighted median qtr, v1) |
| `3` Mixed | **FloatPoolRate** *(amended)* | 3M Treasury at **PQ0** | FloatPoolRate − 3M(PQ0) — same rate as the block's floating segment |
| `0`, `4` | — | — | none — no income (§6.2) |

- **Mixed at the floating spread — PID-LOAN-23 as AMENDED by the first real compare (2026-08-12, grand 1.0008).** The reference's implied variable spread equalled the pure v2 spread exactly (multifamily/HFI: theirs 2.3486% vs our hybrid blend 2.3545%, ratio 1.0022 on the only block carrying mixed balance) — the launch sheet's hybrid mixed-spread columns (fixed pool at mixed's own quarter) are **computed but unused** in the income, precisely the pattern by which PID-LOAN-15 superseded PID-LOAN-4's hybrid for Corporate. Mixed keeps its own segment for visibility; since it feeds the float pool itself, a block with mixed rows but no fixed rows now prices normally — the run stops only if the pool has no usable rate at all.
- **The origination-date statistic is the outstanding-weighted MEDIAN — PID-LOAN-22 as amended by the same compare.** The reference's median-date cells are actually observed dates, and the mean missed construction/HFI fixed by one quarter (ratio 1.0447: mean → 2022Q2 base 1.1%, reference 8/29/2022 → 2022Q3 base 2.7%). `cre_orig_date_statistic` defaults to `weighted_median` (the first observed date whose cumulative weight reaches half); `weighted_mean` is kept for A/B only. Zero-weight dated rows degenerate to the unweighted row median — the limit of the weighted form.
- Base-rate lookup misses fall back to **0 with a censused cause** (outside-MEV vs missing date), exactly as Corporate's PID-LOAN-4 amendment — the fallback overstates that segment's new-origination rate by the omitted base-rate level and must be visible.

## 6. Projection

### 6.1 Balances and shares [PID-LOAN-20 / PID-LOAN-24]

```
side exposure       = Σ Outstanding Balance over ALL rate types in (category, LOCOM)
segment share       = segment outstanding ÷ side exposure
segment balance     = share × M.1 side balance                       (PID-LOAN-20)
quarterly income    = balance × IR(segment, t) ÷ 4                   (D-004)
category income     = Σ over segments, × Table A8 scalar             (PID-LOAN-21)
```

HFS/FVO rows weight by the distinct `Value` column **only if one is configured** (`cre_col_value` — the "Launchpoint Value" residual, §9); otherwise `Outstanding Balance` weights both sides. A **blank Outstanding Balance is a genuine zero** (an undrawn facility), censused, never refused.

### 6.2 Rate types `0` and `4` — balance only, no income [PID-LOAN-24]

As Corporate's PID-LOAN-5: they enter the share denominator (diluting every earning segment) and contribute zero income. Same recorded divergence direction from the Fed's fee-only denominator exclusion — it **lowers** projected income; the Fed rule's CRE applicability is itself OQ-035.

### 6.3 Variable engine — rate types `2` and `3` [PID-LOAN-25]

```
IR(segment, t) = max( 3M(t) + Spread(segment), BlockFloor(category, LOCOM) )

BlockFloor = Σ(Outstanding × floor, blanks counting as ZERO, over the block's v2+v3 rows)
             ÷ Σ(Outstanding over v2+v3), then max(.., 0)
```

One floor per category × LOCOM block, shared by its floating and mixed segments (the sheet's "floor (variable)" row; the PID-LOAN-15 floor family — zeros-included and max-0 carried from that family, re-verified on the first run's floor census).

### 6.4 Fixed engine — rate type `1`

```
wt(category, LOCOM, PQx) = Σ Outstanding Balance of v1 facilities whose Maturity Date
                           falls in PQx ÷ the block's launch-point v1 Outstanding Balance
IR_new(t) = 3M(t) + Spread(v1)
IR(t)     = (1 − wt(t)) × IR(t−1) + wt(t) × IR_new(t)                 Equation A38
IR(t)     = max(IR(t), 0)                                             fixed floor = exactly 0
```

`IR(PQ0)` seeds from FixedPoolRate. The fixed floor at exactly 0 is carried from the PID-LOAN-15 family (residual iii). **The wt construction is the flagged working analogue of PID-LOAN-6** — maturity-only, on the CRE share basis — because **OQ-001 remains OPEN for CRE**: nothing user-stated yet pins the CRE re-origination inputs; the compare will judge it (§9).

### 6.5 Scalar roll-up [PID-LOAN-21]

Domestic construction / multifamily / non-owner-occupied → **"Domestic CRE" (1.081)**; the merged international category → **"Rest of wholesale" (1.113)** — user-confirmed; reproduced the workbook's Total = (Fixed + Variable) × scalar exactly on every screenshot block. Applied every quarter (`apply_scalar` false for reference-matching runs, exactly as Corporate). The Board states no correspondence (OQ-010 stays open source-side and for Retail).

## 7. Divergences from the Federal Reserve source

| # | Fed source states | This implementation | Direction of effect |
|---|---|---|---|
| 1 | Six CRE portfolios; 24 segments (PDF pp. 176–177) | Four categories, 16 cells — H.2 code 7 cannot distinguish the three international portfolios (PID-LOAN-19, data-forced) | Granularity only: one spread/pool where the Fed census has three international portfolios; outputs stay labeled "Fed 4-6 merged" |
| 2 | Fee-only loans' balances excluded from the total-balances calculation (PDF p. 176, Corporate-located; CRE applicability = OQ-035) | `4` (and `[NULL]`) stay **in** the share denominator (PID-LOAN-24) | **Lowers** projected income |
| 3 | wt "derived from the default rate, prepayment rate, and maturity rate" (PDF p. 183) | Maturity only, outstanding-weighted (working construction; OQ-001-CRE open) | Understates re-origination where defaults/prepayments are material |
| 4 | "the median origination date … for that portfolio" (PDF p. 182) | Outstanding-**weighted** statistic, mean by default (PID-LOAN-22) | Operationalization of an unstated mechanic, recorded not smoothed; differs from Corporate's PID-LOAN-4 unweighted median |
| 5 | "portfolio-specific interest rate floor … the stated floor" (PDF p. 180; values unstated) | Block-level outstanding-weighted floor over floating+mixed, blanks as zero, max 0; fixed floored at exactly 0 (PID-LOAN-25) | Company convention; the Fed names no floor source at all |
| 6 | Mixed-rate loans "treated as variable-rate" (PDF p. 176, Corporate-located) | Variable engine ✓ at the hybrid spread (PID-LOAN-23) | Matches on projection; the spread derivation is a refinement the source does not describe |

## 8. Validation and first-run diagnostics

- **Reference-key census** per category × LOCOM × Variable Type — shows empty categories and the key universe against the mapping panel.
- **DO-NOT-USE line-code census** — count and committed exposure of excluded code-4/6 rows; a large number means the extract carries owner-occupied lines.
- **Blank-Outstanding census** — rows read as genuine zeros.
- **Float-NaN census per column** — the H.2 sheet encodes blanks as float NaN in places (pandas-produced; found on the first real run, where a NaN floor crashed row 15899). NaN and the string "NaN" now read as MISSING for optional fields — a NaN floor is "no floor", a NaN date is "no date", a NaN outstanding is the blank-zero — counted per column, never silent; a NaN in a REQUIRED money column (committed) still surfaces by facility id.
- **Base-rate fallback census by cause** (outside-MEV vs missing date), with the §5 consequence stated.
- **Floor census** — block floors, dispersion across populated floors, and per-segment-quarter binds (the PID-SEC-18 lesson).
- **wt ≤ 1 per quarter** — surfaced, never clamped.
- **M.1 role-label check** — the configured rows' role labels print; a non-"Wholesale - CRE" label warns (a misconfigured row number is the silent failure mode of row-wired balances).
- **Compare mode** (`cre_results_sheet`): ours vs the workbook's blocks, fixed/variable raw and Total × Table A8, with implied balance and spread from the PQ1→PQ2 slope — the same machinery that converged Corporate.

## 9. Open items

| Item | Status |
|---|---|
| **Weighted origination statistic** | **RESOLVED 2026-08-12 (compare round 1): weighted MEDIAN** — PID-LOAN-22 amended; `weighted_mean` retained for A/B only |
| **Mixed spread** | **RESOLVED 2026-08-12 (compare round 1): floating spread** — PID-LOAN-23 amended; the lone-mixed hard stop is obsolete (mixed feeds its own float pool) |
| **Rate pools committed-weighted** (residual i) | **Compare-corroborated round 1**: every floating stream's implied spread matched the reference to the digit, so the pool construction agrees; formally still a flagged observation |
| **HFS/FVO "Launchpoint Value" column** (residual ii) | Round 1: every FVO_HFS block landed 1.0000 with Outstanding weighting both sides — the distinct Value column, if it exists, is numerically equivalent here; `cre_col_value` stays available |
| **Fixed floor exactly 0** (residual iii) | Round 1: no fixed floor bind occurred either side; carried from the PID-LOAN-15 family, still unobserved directly |
| **H.2 unit scales** (residual iv) | Round-1 censuses clean at the Corporate-confirmed scales — consistent with same-workbook reuse; watch on future extracts (D-006) |
| **wt construction for CRE** | OQ-001-CRE formally open; round 1 corroborates it — the fixed blocks whose base rates matched landed 1.0000/0.9991 with nonzero wt (multifamily sum-wt 0.015, non-OO 0.071) |

## 10. Implementation status

| Layer | Module | State |
|---|---|---|
| H.2 decode + scalar assignment (PID-LOAN-18/19/21) | `ingestion/loans_cre_mapping.py` | **Landed 2026-08-12** — code collapses, DO-NOT-USE handling, CRE reference key, PID-LOAN-21 map |
| Workbook binding (PID-LOAN-18/20) | `ingestion/loans_loader.py` (`load_cre_facilities`, `load_cre_side_balances`; `load_reference_results` parametrized) | **Landed** — alias headers, optional IDs, blank-outstanding zeros, row-wired M.1 with role warnings |
| Launch point (PID-LOAN-22/23/24/25) | `interest_income/loans_launchpoint.py` (`build_cre_launch_point`, `weighted_origination_quarter`) | **Landed** — Corporate paths untouched (`compute_reorigination_weights` gained a measure parameter, default unchanged) |
| Projection | `interest_income/loans_projection.py` | **Reused unchanged** — the A33/A38 engines and scalar roll-up are category-agnostic |
| Config | `ingestion/config.py` (`cre_orig_date_statistic`), `[firm_data.loans]` cre_* keys | **Landed** |
| Runner + compare | `examples/run_loans.py` (CRE section; `_compare` takes the scalar map) | **Landed** — synthetic demo runs Corporate + CRE end to end |
| Tests | `tests/unit/interest_income/test_loans_cre.py`, `tests/unit/ingestion/test_loans_cre_loader.py`, integration demo markers | **370 passed** (2026-08-12); arithmetic worked by hand in the assertions |
| Reference compare vs the company workbook | — | **Round 1 (2026-08-12): GRAND 1.0008** — every implied balance identical to the digit; most blocks 1.0000; the two residual ratios (construction fixed 1.0447; multifamily variable 1.0022) identified the two amendments above. **Round 2 after the amendments expected ≈ 1.0000** |

## 11. PID index

| ID | Covers |
|---|---|
| PID-LOAN-18 | CRE H.2 input contract and reference key — §2, §3 |
| PID-LOAN-19 | Four categories; code mapping; the data-forced international merge; DO-NOT-USE codes — §3 |
| PID-LOAN-20 | M.1 rows 17/18/21 multiplicand wiring — §2, §6.1 |
| PID-LOAN-21 | Scalar assignment (domestic → 1.081; international → 1.113) — §6.5 |
| PID-LOAN-22 | Outstanding-weighted origination date; mean-vs-median switch — §5 |
| PID-LOAN-23 | Mixed on the variable engine at the hybrid spread; engines per wholesale part — §5 |
| PID-LOAN-24 | Fee/DO-NOT-USE rows balance-only in the share denominator — §6.2 |
| PID-LOAN-25 | Block-level outstanding-weighted variable floor, blanks as zero, max 0 — §6.3 |

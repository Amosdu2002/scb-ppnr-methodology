# Source Brief — Interest Income on Loans: CRE (`ii_loans` — wholesale/CRE)

> **STATUS: Proposed for the 2026 stress test — public-comment stage, NOT adopted.**
> Component: **Interest Income on Loans**, Section v.a(1) (PDF pp. 173–188; md sec-150–172); this brief covers the **CRE** part of Wholesale (PDF pp. 176–177; md sec-155), plus the CRE-relevant passages elsewhere in v.a(1): the fixed-rate prevalence note (PDF p. 183; md sec-165), the industry-scalar worked example (PDF pp. 183–184; md sec-166), Question A153 (PDF p. 187; md sec-172), Table A8 (PDF p. 220; md sec-209), and footnote 63 (PDF p. 184 footer; md 5354). Model type per Table A6: **Structural**.
> Deliverable: loans workstream (asset-side Increment 3), slice 3 per the approved plan of 2026-08-12 — fourth of the sibling set {common, wholesale, corporate, **CRE**}. Review state: **APPROVED 2026-08-12** *(user review the same day; banner updated at approval)*.
> Scope: **CRE only.** Corporate and Retail appear solely where the source draws an explicit boundary (§2.3); wholesale-shared mechanics are cited from `ii_loans_wholesale.source-brief.md`, never restated; equations are **not** transcribed (D-010(b) — all of Equations A32–A38 live verbatim in `ii_loans_common.source-brief.md` §7).
> Integrity flags relevant here: SQ-5 (truncated "sourced from FR.", p. 175), SQ-6 (A37 typography), SQ-18/OQ-033 (fixed-rate subscripts), SQ-22 (owner-occupancy naming variants, pp. 175–176), footnotes 61–62. **No new source quirk was found in the CRE passage.** Open questions: OQ-001 and OQ-033 (open CRE legs), OQ-035, and **OQ-039, filed with this brief** (CRE loan-level schedule unnamed); the OQ-002 and OQ-010 CRE legs are **resolved for project implementation** by PID-LOAN-25/18 and PID-LOAN-21 (registered with this brief), and OQ-003's CRE weighting basis is confirmed by PID-LOAN-22 (formula detail at spec stage) — all source-side gaps preserved.
> Verification: **PDF pp. 176–177 read as page images at high zoom 2026-08-12** — the six-item enumeration is complete, numbering intact, and the 24-segment sentence exact; **pp. 183 and 187 re-read as page images 2026-08-12** (this brief's load-bearing lines); **full-document absence searches 2026-08-12** ("H.2", "committed", "undrawn", "workout", loan-sense "renewal", "income-producing", "multifamily", "construction"); pp. 173–188 had a full image pass 2026-07-30; Table A8 image-verified 2026-07-16 and 2026-08-03. Citation format: (PDF p. N; md sec-M).

---

## 0. Classification legend and cross-reference discipline

Labels [FACT] / [PID] / [INT] / [CODE] / [OQ] / [ALT] per `ii_loans_common.source-brief.md` §0.

### 0.1 Project implementation decision register (user-confirmed)

Eight CRE PIDs were confirmed with this brief (2026-08-12) from user-supplied workbook context (column lists, the H.2 mapping sheet, the M.1 wiring statement, and launch-point/results screenshots; PID-LOAN-21..25 were first recorded as flagged observations (a)–(e) and **user-confirmed the same day**). Full text in `handbook/open-questions.md`; they are company conventions, **never attributable to the Federal Reserve**. No confidential values, sheet names, or firm data appear in this repository — only the logical contract.

| ID | Decision (one line) | Fed-source status of the same point |
|---|---|---|
| **PID-LOAN-18** | CRE facility data = the "CRE H.2" sheet (header row 4, like CORP H.1): columns Outstanding Balance, Line Reported on FR Y-9C, Committed Balance, Origination Date, Maturity Date, Interest Rate Variability, Interest Rate, Interest Rate Floor, Lower of Cost or Market Flag; reference key = `{Line Reported on FR Y-9C}_{Interest Rate Variability}_{LOCOM}`; vocabularies match H.1 — variable type {1 Fixed, 2 Floating, 3 Mixed, 4 Entirely Fee Based, [NULL] = DO NOT USE}, **no demand-loan code**; LOCOM {1 LOCOM/HFS, 2 FVO, 3 HFI} with 1 and 2 rolling into FVO/HFS | The source names **no FR Y-14Q schedule for CRE** (**OQ-039**); footnote 61's facility-level statement is the only stated data basis |
| **PID-LOAN-19** | Four workbook categories; H.2 line-code mapping {1, 2} → domestic construction, {3} → domestic multifamily, {5} → domestic non-owner-occupied, {7} → **international, merged** — one code covers all non-domestic CRE excluding owner-occupied, so the Fed's three international portfolios are data-indistinguishable; codes {4, 6} are DO NOT USE (rows outside the reference-key universe are excluded and censused); segment universe = the reference-key panel, handled as for Corporate (user-stated) | The Fed census is **six portfolios and 24 stated segments** [FACT], preserved in full (§3–§4); the merge is a **recorded, data-forced divergence** |
| **PID-LOAN-20** | Eq A32 multiplicand from the M.1 Balance sheet: domestic construction = E17/G17 (HFI / HFS-FVO; MDRM CALBP344/345), domestic multifamily = E18/G18 (CALBP348/349), domestic non-owner-occupied = E21/G21 (CALBP356/357); international (merged) = Σ of the international-office columns I/K over the same three rows (CALBP346/347, 350/351, 358/359); M.1 values in millions; owner-occupied (row 20) and farmland (row 22) rows remain Corporate's (PID-LOAN-9/17) | The common framework states only "the portfolio balance from FR Y-14 Schedules" (PDF p. 174; md sec-151); no M.1 line is named anywhere in v.a(1) |

| **PID-LOAN-21** | Industry-scalar assignment: domestic construction / multifamily / non-owner-occupied → **"Domestic CRE" (1.081)**; international (merged) → **"Rest of wholesale" (1.113)**; applied as Total = (Fixed + Variable) × scalar per block (PID-LOAN-16 semantics) — block arithmetic exact on the reference results before confirmation | **Resolves OQ-010 for CRE project implementation** (§10); the Board states no category-to-row correspondence anywhere (SQ-11), so the source side and Retail stay open |
| **PID-LOAN-22** | The Eq A37 origination-date statistic is **outstanding-balance-weighted** (sheet-stated: "balance weighted orig date based on: outstanding") — unlike Corporate's PID-LOAN-4 unweighted row median; whether the weighted statistic is a median or a mean is a cell-formula detail TO CONFIRM at spec stage | The Fed states only "the median origination date … for that portfolio" (PDF p. 182); advances the **OQ-003 CRE leg** to the weighting basis; source-side gap preserved |
| **PID-LOAN-23** | Mixed facilities project on the **variable engine at their own hybrid spread** (fixed-pool rate − base rate at mixed's own weighted origination date — the PID-LOAN-4-style construction, which Corporate's converged reference engine superseded via PID-LOAN-15); **engine constructions are per wholesale part** | The Fed states only that mixed-rate loans are "treated as variable-rate" (PDF p. 176, Corporate-located); CRE applicability of that rule itself is **OQ-035** |
| **PID-LOAN-24** | Fee-based (4) and DO-NOT-USE ([NULL]) rows **count toward the balance-share denominator but earn nothing** (the Corporate PID-LOAN-5 pattern) | Same half-match/half-divergence as PID-LOAN-5: the Fed's fee-only rule excludes those balances from the denominator (PDF p. 176, Corporate-located; CRE scope = OQ-035) — the divergence **lowers** projected income (§6.3) |
| **PID-LOAN-25** | The **variable floor** = outstanding-weighted average of `Interest Rate Floor` over floating + mixed rows per category × LOCOM block (the sheet's "floor (variable)" row; PID-LOAN-15 floor-family construction — zeros-included, max(·, 0) carried from that family, re-verified on the first CRE run's floor census) | With PID-LOAN-18's floor column, **resolves OQ-002 for CRE project implementation**; the Fed names no floor source or values (PDF p. 180) — absence preserved |

**Residual flagged items (spec stage; observed, not yet confirmed):** (i) rate pools appear **committed-weighted** (initial rate = Σ exposure × rate ÷ launch-point committed balance — the PID-LOAN-3 pattern); (ii) the HFS/FVO blocks weight by a "Launchpoint Value" quantity — whether a distinct H.2 `Value` column exists (as on H.1) is TO CONFIRM at load; (iii) the fixed-engine floor treatment for CRE is unobserved (Corporate's reference engine floors the A38 recursion at 0); (iv) exact header spellings and unit scales (D-006 — refuse-to-run while unconfirmed).

---

## 1. Executive summary

**What CRE is.** [FACT] "The CRE section of loan-level interest income is first segmented into six disclosure loan types (also referred to as portfolios) as defined in FR Y-9C" (PDF p. 176; md sec-155): domestic and international construction, multifamily, and non-owner-occupied commercial real estate (§3). It is one of the two wholesale parts, the other being Corporate.

**How CRE segments.** [FACT] "CRE segmentation is similar to Corporate segmentation where interest rate variability splits the portfolio by fixed-rate and variable-rate interest rates. With the asset classification segmentation, the total number of CRE segments is 24." (PDF pp. 176–177; md sec-155). Unlike Corporate, **every** CRE portfolio participates in the rate split — no CRE portfolio is named data-limited, and the stated 24 reconciles only as 6 × 2 rate types × 2 asset classifications (§4).

**What CRE adds beyond the shared machinery.** Almost nothing — and that is the finding. The CRE-specific prose is one paragraph; every rate mechanic (3M Treasury base rate, Equation A33 variable path, Equation A37 t−a wholesale spread, Equations A34/A35/A38 fixed machinery, floors, wt, the industry scalar) is inherited from the common and wholesale briefs (§9). The remaining CRE-specific facts are scattered single lines: fixed-rate products "are more common for CRE income-producing loans" (PDF p. 183; §7), the scalar worked example is stated on "the domestic CRE portfolio" (PDF pp. 183–184; §10), and Question A153 names corporate and CRE floors (PDF p. 187; §11).

**What is unresolved.** On the source side: the FR Y-14Q schedule carrying CRE facility data is never named — "H.2" appears nowhere in the document (**OQ-039**, the mirror of Corporate's OQ-038 asymmetry); whether the Corporate-stated mixed-rate/demand/fee-only rules reach CRE remains formally UNKNOWN (**OQ-035**, wholesale-owned); and no Table A8 row is assigned to any CRE portfolio (**OQ-010**, source side). For project implementation, the PID set registered with this brief (PID-LOAN-18..25) supplies the H.2 contract, the category mapping, the multiplicand wiring, the scalar assignment, the weighted origination date, the mixed and fee/DO-NOT-USE treatments, and the variable-floor collapse — leaving **OQ-001 (wt inputs) as the one Corporate-resolved gap still open for CRE**, plus the §0.1 residual items, for the CRE spec stage.

---

## 2. CRE scope and boundaries

### 2.1 Position in the hierarchy

[FACT] Wholesale is "organized into two parts: Corporate and Commercial Real Estate (CRE)" (PDF p. 175; md sec-153). CRE is a **section**, not a Table A6 component — the Table A6 row is the single "Loans" component (PDF pp. 168–169; md sec-148), and D-003 keeps all six portfolio families in one chapter.

### 2.2 What the source states about CRE's own definition

[FACT] CRE names its defining authority: the six loan types are "as defined in FR Y-9C" (PDF p. 176; md sec-155) — the attribution Corporate lacks (OQ-038 records that asymmetry from the Corporate side).

[FACT — the mirrored asymmetry, **OQ-039**, filed with this brief] The source **never names the FR Y-14Q schedule carrying CRE facility-level data**. Full-document searches (2026-08-12): "H.2" and "Schedule H.2" have **zero occurrences**; the proposed-suite data basis names "FR Y-14Q, Schedule G; FR Y-14Q, Schedule B; FR Y-14Q, Schedule M; and FR Y-14M" only — no Schedule H at all (PDF p. 172; md sec-149); Schedule H.1 appears solely inside the Corporate data-limited-portfolios paragraph (PDF p. 176; md sec-154). The only stated CRE data basis is wholesale-generic: the SQ-5-truncated "sourced from FR." sentence and footnote 61's facility-level statement (PDF p. 175; md sec-153). The project's H.2 sourcing is therefore **PID-LOAN-18 project context, never a Fed statement**.

[FACT of absence] The FR Y-9C form itself is not in `sources/`; the six type definitions are not verified against the form here. The workbook's mapping sheet anchors the codes to FR Y-9C Schedule HC-C item 1 subitems (project context under PID-LOAN-19; non-normative, §13).

### 2.3 Explicit boundaries against Corporate and Retail

Recorded because the source draws them; neither neighbour is analyzed here.

| Boundary | Source statement | Label |
|---|---|---|
| **Owner-occupied CRE is Corporate** | Corporate portfolios (2) "domestic owner-occupied CRE loans" and (6) "international owner-occupied CRE loans" (PDF p. 175; md sec-154) | [FACT] |
| **Non-owner-occupied CRE is CRE** | CRE portfolios (3) and (6) (PDF p. 176; md sec-155); naming variants across the two sections are SQ-22 (cosmetic) | [FACT] |
| **Farmland is Corporate** | Corporate portfolios (10) and (11) (PDF p. 175; md sec-154) — agricultural real estate never enters the CRE section | [FACT] |
| Retail is a separate hierarchy | "Retail interest income projections are organized into four sections" (PDF p. 177; md sec-156) | [FACT] |

[INT — carried from the Corporate brief §2.3] The Corporate/CRE line is **owner-occupancy, not property type**: two commercial-real-estate exposures take the Corporate treatment. A naive "all CRE goes to the CRE section" grouping misroutes them. The placement is source-stated; the characterization of the dividing line is the interpretation.

---

## 3. CRE portfolio census

### 3.1 The six loan types (verbatim, source order)

[FACT] (PDF p. 176; md sec-155; enumeration re-verified at high zoom 2026-08-12 — all six items present, numbering intact, no merged entries): "The CRE section of loan-level interest income is first segmented into six disclosure loan types (also referred to as portfolios) as defined in FR Y-9C: (1) domestic construction loans, (2) domestic multifamily loans, (3) domestic non-owner occupied commercial real estate loans, (4) international construction loans, (5) international multifamily loans, and (6) international non-owner occupied commercial real estate loans."

Wording note [FACT]: CRE writes "(also referred to as portfolios)" where Corporate writes "(referenced as a portfolio)" (PDF p. 175) — same convention, cosmetic variation, no quirk filed.

### 3.2 Per-portfolio attribute register

Coding-friendly names are this project's, not the Fed's. "Loan-level data?" and "Rate-split?" carry no per-portfolio source statement for CRE — see the notes below the table.

| # | Fed portfolio name | Coding-friendly name | Loan-level data? | Rate-split? | Physically separable in firm data? |
|---|---|---|---|---|---|
| 1 | domestic construction loans | `cre_construction_dom` | [INT] yes | [INT] yes | Yes — H.2 line codes 1, 2 [PID-LOAN-19] |
| 2 | domestic multifamily loans | `cre_multifamily_dom` | [INT] yes | [INT] yes | Yes — code 3 |
| 3 | domestic non-owner occupied commercial real estate loans | `cre_nonoo_dom` | [INT] yes | [INT] yes | Yes — code 5 |
| 4 | international construction loans | `cre_construction_intl` | [INT] yes | [INT] yes | **No — code 7 is one undivided international bucket** |
| 5 | international multifamily loans | `cre_multifamily_intl` | [INT] yes | [INT] yes | **No — as above** |
| 6 | international non-owner occupied commercial real estate loans | `cre_nonoo_intl` | [INT] yes | [INT] yes | **No — as above** |

- [FACT of absence] **No CRE portfolio is named data-limited.** The Corporate section names exactly three portfolios "not segmented by interest rate variability because they have no loan-level data on the FR Y-14Q H.1 schedule" (PDF p. 176; md sec-154) — all three Corporate. The CRE section states no exception, and no NPML-style proxy exists for CRE (§8).
- [INT] "Loan-level data: yes" and "Rate-split: yes" for all six are read from that absence together with the stated total: 24 reconciles only if all six types carry the rate split (§4.2). The source asserts neither claim portfolio-by-portfolio.
- The "physically separable" column is **project context** ([PID-LOAN-19]), not Fed methodology: the firm's H.2 line-code field cannot distinguish the three international portfolios (§4.3).

---

## 4. CRE segmentation hierarchy

### 4.1 The dimensions

| Level | Dimension | Values | Source |
|---|---|---|---|
| 0 | Wholesale part | CRE | [FACT] PDF p. 175; md sec-153 |
| 1 | Portfolio `p` | the 6 of §3.1 | [FACT] PDF p. 176; md sec-155 |
| 2 | Rate type | fixed-rate; variable-rate | [FACT] PDF pp. 176–177; md sec-155 ("similar to Corporate segmentation where interest rate variability splits the portfolio") |
| 3 | Asset classification | HFI; FVO/HFS | [FACT] PDF p. 175; md sec-153 (stated for each wholesale section); "With the asset classification segmentation…" (PDF p. 177; md sec-155) |

[INT — ordering note] The CRE sentence order is types → rate variability → asset classification, while Corporate's "16 out of 22" only reconciles with classification applied before the rate split (Corporate brief §4.1). For CRE the grid is full, so the two orderings commute and nothing turns on the difference; recorded only so the asymmetry is not mistaken for substance.

### 4.2 The 24-segment grid

[FACT] "With the asset classification segmentation, the total number of CRE segments is 24." (PDF p. 177; md sec-155)

> **⚠ [INT] — the multiplication is this project's restatement.** The source states the segmentation steps and the total; it never prints "6 × 2 × 2". The reading is anchored by the stated 24 — no other combination of the named dimensions reaches it — which makes this materially stronger than the Corporate grid reconstruction (OQ-034, where no total is stated), but it remains a restatement, not a quotation.

[INT] 6 portfolios × 2 rate types × 2 asset classifications = **24**, matching the stated total exactly. Contrast with Corporate ([FACT]): CRE's total **is** stated; Corporate's is not (Corporate brief §4.2; OQ-034). Consequence of the reconciliation: **all six portfolios carry the rate split** — the fact-of-absence in §3.2 and the arithmetic agree.

[INT] Wholesale total under the OQ-034 working reading: 38 Corporate + 24 CRE = 62 segments. Carried for planning only.

### 4.3 The physical realization (project context — [PID-LOAN-19]; never Fed methodology)

The firm's H.2 "Line Reported on FR Y-9C" field distinguishes the three **domestic** portfolios (codes 1, 2 → construction; 3 → multifamily; 5 → non-owner-occupied) but carries a **single code (7) for all non-domestic CRE excluding owner-occupied** — the three international portfolios are data-indistinguishable. The workbook therefore models **four categories** (three domestic + one merged international), each × {HFI, FVO/HFS} × the rate-type vocabulary.

| Fed-side grid | Physical grid |
|---|---|
| 6 portfolios × 2 rate types × 2 classifications = **24 segments** [FACT + INT restatement] | 4 categories × 2 rate types × 2 classifications = **16 cells** [PID-LOAN-19] |

**Recorded divergence, data-forced.** The Fed-side census stands as [FACT]; the merge coarsens the international spread/rate granularity from three portfolios to one (the Fed's spread "varies by firm, product, and segment", PDF p. 181; md sec-164 — with product ≈ portfolio, three products become one). Model outputs must label the merged block as "international — Fed portfolios (4)–(6), merged (data-forced)", never as a single Fed portfolio (§13). Precedent: the Corporate 9/10/11 merged bucket (PID-LOAN-10/17), with the difference that Corporate's merge answered missing loan-level data while CRE's answers an indivisible reporting code.

[FACT of absence] Codes 4 and 6 exist in the mapping vocabulary only as "DO NOT USE" entries; no Fed statement corresponds. [INT — working reading, flagged] they are the owner-occupied FR Y-9C lines, whose exposures are modeled in Corporate (H.1 codes 10/11 → Fed Categories 2/6 per PID-LOAN-9); rows carrying them, if any appear, fall outside every CRE segment and are excluded and censused (§13).

---

## 5. Data inputs and classifications to capture

Every row states whether the source names the item. **No field name, code, or value vocabulary is invented** — physical realizations are PID-cited project context.

| # | Item to capture | Source status | Physical realization (project context) | Notes |
|---|---|---|---|---|
| 1 | Facility-level records | [FACT] wholesale data are facility-level (footnote 61, PDF p. 175); **schedule UNNAMED** | "CRE H.2" sheet, header row 4 [PID-LOAN-18] | **OQ-039** |
| 2 | Portfolio assignment (facility → the 6 types) | [FACT] six types "as defined in FR Y-9C"; no field named | `Line Reported on FR Y-9C` codes {1,2,3,5,7}; {4,6} DO NOT USE [PID-LOAN-19] | International merge — §4.3 |
| 3 | Asset classification (HFI; FVO/HFS) | [FACT] (PDF p. 175); no field named | `Lower of Cost or Market Flag` {1 LOCOM/HFS, 2 FVO, 3 HFI} → {FVO/HFS, HFI} [PID-LOAN-18] | Same collapse as Corporate (PID-LOAN-9) |
| 4 | Interest-rate-variability value | [FACT] fixed/variable split; reported variable-rate value "is floating" (footnote 62) | `Interest Rate Variability` {1 Fixed, 2 Floating, 3 Mixed, 4 Entirely Fee Based, [NULL] DO NOT USE} [PID-LOAN-18] | **No demand code** — OQ-035 physical note (§6.2) |
| 5 | Facility balance measures | [FACT] balance-weighted averages and outstanding-balance percentages (common §6, §7.2); no measures named | `Outstanding Balance`; `Committed Balance`; HFS/FVO blocks weight by a "Launchpoint Value" quantity — **whether a distinct H.2 `Value` column exists (as on H.1) is TO CONFIRM at load** | Flagged (§0.1 note; §13) |
| 6 | Facility interest rate | [FACT] via the common jump-off construction (common §7.2) | `Interest Rate` column | Pool weighting observed committed-based — residual flagged item §0.1(i), spec stage |
| 7 | Interest-rate floor | [FACT] the rule; values/source UNKNOWN (common §7.1) | `Interest Rate Floor` column | **OQ-002 resolved for CRE project implementation** (PID-LOAN-18 column + PID-LOAN-25 collapse); source-side absence preserved |
| 8 | Origination date (Eq A37 t−a) | [FACT] "median origination date" (PDF p. 182); mechanics unstated | `Origination Date` column | **OQ-003 CRE leg:** weighting basis confirmed (PID-LOAN-22); median-vs-mean formula spec-stage |
| 9 | Maturity date (wt inputs) | [FACT] wt from default/prepayment/maturity rates (PDF p. 183); delivery unstated | `Maturity Date` column | **OQ-001 open for CRE**; Corporate precedent PID-LOAN-6 (maturity-only) is the likely analogue, unconfirmed |
| 10 | Portfolio balance (Eq A32 multiplicand) | [FACT] "the portfolio balance from FR Y-14 Schedules" (PDF p. 174); no line named | M.1 rows 17/18/21, E/G domestic + Σ I/K international [PID-LOAN-20] | M.1 in millions (D-006 as for Corporate) |
| 11 | Scenario base rate | [FACT] 3M Treasury (wholesale §5) | MEV sheet, projection + history (Corporate contract reused) | — |
| 12 | Industry scalar | [FACT] Table A8 values (common §8); CRE row assignment unstated | Table A8 direct (PID-LOAN-11 machinery); assignment per **PID-LOAN-21** | **OQ-010 resolved for CRE project implementation** (§10); source side open |

[FACT absence] The source names **no H.2 field, MDRM code, or value list** for any row above; every physical entry is project context. Launch point: the reference results carry PQ0 = 12/31/2024 with PQ1–PQ9 quarterly through 3/31/2027 — same launch quarter as the Corporate contract [PID-LOAN-8 context, confirmed on the CRE results sheet 2026-08-12].

---

## 6. Rate-type treatment for CRE

### 6.1 What the source states

[FACT] The whole of CRE's stated rate-type treatment is one sentence: "CRE segmentation is similar to Corporate segmentation where interest rate variability splits the portfolio by fixed-rate and variable-rate interest rates" (PDF pp. 176–177; md sec-155). Footnote 62's "floating" reporting-value statement is wholesale-scoped and applies (wholesale §4).

### 6.2 The OQ-035 scope question (wholesale-owned)

[FACT] The mixed-rate/demand-loan and fee-only rules are stated **inside the Corporate subsection only** (PDF p. 176; md sec-154); the CRE section does not restate them. Whether "similar to Corporate" imports them is not stated — **OQ-035**, owned by the wholesale brief §4, whose flagged working assumption (wholesale-wide applicability) applies here and is never source-attributed.

**Physical context recorded 2026-08-12 (project context; does not resolve the source question):** the H.2 vocabulary contains Mixed and Entirely Fee Based codes and **no demand-loan code** [PID-LOAN-18] — so, exactly as for Corporate (PID-LOAN-2), the demand rule has no counterpart in this data, and the mixed and fee cases are the operative ones for CRE. Confirmed workbook treatments [PID-LOAN-23/24]: mixed facilities project on the variable engine at their own hybrid spread — mixed income rides inside the results blocks' "Variable Rate Income" row, consistent with the Corporate-stated mixed→variable rule — and fee-based/DO-NOT-USE rows hold balance shares while earning nothing.

### 6.3 The fee-only denominator question

[FACT — Corporate-stated] Fee-only loans are excluded from the average rate **and** from the total-balances calculation (PDF p. 176; md sec-154) — the loan model's only stated balance-denominator exclusion (Corporate brief §8). Under OQ-035 its CRE applicability is UNKNOWN. The confirmed workbook treatment [**PID-LOAN-24**] keeps fee-based balances **in** the share denominator — the same recorded divergence direction as Corporate's PID-LOAN-5 (it lowers projected income).

---

## 7. Fixed-rate prevalence — the "income-producing" note

[FACT] "In wholesale, fixed-rate products are more common for CRE income-producing loans." (PDF p. 183; md sec-165; page image re-read 2026-08-12; full-document search 2026-08-12 — the phrase "income-producing" appears **exactly once** in the document.)

[INT — carried from wholesale §7, unchanged] "CRE income-producing loans" is not one of the six disclosure types; it reads as a business characterization (multifamily and non-owner-occupied income-producing property lending, as against construction). No mapping from the phrase to the six portfolios is stated, and none is invented here. Practical consequence [INT]: the Equations A34/A38 fixed machinery and the conservative fixed roll-off statement (wholesale §9) matter most for CRE among the wholesale portfolios; nothing quantitative follows.

---

## 8. Fact-of-absence register

Each row is a [FACT] of absence for the CRE part of v.a(1), verified on the 2026-07-30 full image pass and the 2026-08-12 searches.

| # | Absent for CRE | Contrast / nearest statement |
|---|---|---|
| 1 | **No data-limited portfolio; no NPML-style proxy; no bank-level spread exception; no merged treatment** | Corporate's three data-limited portfolios and NPML proxy (PDF p. 176; md sec-154) are Corporate-only |
| 2 | **No CRE-specific base rate, floor value, assumption, or limitation subsection** | The (c) block is Assumptions / Limitations / Retail Portfolio / Wholesale Portfolio only (PDF pp. 184–186; md sec-167–171) |
| 3 | **No FR Y-14Q schedule named for CRE data** | OQ-039 (§2.2) |
| 4 | **No committed/undrawn/utilization treatment stated anywhere in v.a(1)** — "committed" and "undrawn" have zero occurrences in the document | Relevant because construction facilities draw over time; the stated machinery is flat balances with same-type replacement (common §6) plus the wholesale revolver-draw limitation (§12 row 5) |
| 5 | **No loan renewal, workout, or modification treatment** — loan-sense "renewal"/"workout" absent (the document's two "renewal" hits are hedge renewals, PDF pp. 221–223; A35's "modification" modifies an equation, not loans) | Constant roll-off statements, wholesale §9 |
| 6 | **No Board question on CRE data granularity or the international portfolios** | §11 |

---

## 9. Inheritance register — what CRE does not restate

Auditable boundary; each row is governed by the cited brief and applies to CRE unchanged. (Same discipline as Corporate brief §9.)

| Rule | Governed by | CRE-specific note |
|---|---|---|
| Eq A32 income identity; 9 quarters; (b,p,i,t) | common §7.0 | — |
| Balance construction; flat balances; same-quarter replenishment | common §6 | Multiplicand wiring = PID-LOAN-20 (§5 row 10) |
| Rate type as the primary segmentation principle | common §7.2 | Realized as level 2 of §4.1 |
| Eq A33 variable-rate path | common §7.3 | Carries mixed facilities under the OQ-035 working assumption (§6.2) |
| Base rate = 3M Treasury | wholesale §5 | No CRE-specific base rate exists (§8 row 2) |
| Eqs A34/A35/A38 fixed-rate machinery; wt | common §7.6 | OQ-033 (firm dimension) applies; prevalence note §7 |
| Eq A37 wholesale spread; median origination date t−a | wholesale §6 | **OQ-003 open for CRE** (Corporate's PID-LOAN-4 does not extend automatically; observed CRE weighting differs — §0.1 b) |
| Spread definition and constancy | common §7.5 | Granularity consequence of the international merge — §4.3 |
| Interest-rate floors | common §7.1; wholesale §8 | Question A153 names CRE (§11); **OQ-002 open for CRE** |
| Industry-scalar mechanism; Table A8 values | common §8 | Row applicability §10 |
| Assumptions (1)–(7); general limitations | common §12 | No CRE-specific assumption list exists (§8 row 2) |
| Quarterly compounding versus D-004 | common §7.7 | Unresolved at project level |
| Hedge exclusion (Question A159) | common §11 | Loans exclude hedges entirely; OQ-005 |
| Scope of the mixed/demand/fee-only rules | wholesale §4 (OQ-035) | This brief records the CRE-side physical context only (§6.2) |
| Constant roll-off; conservative fixed roll-off; NPML; revolver draws | wholesale §9, §12 | NPML row is Corporate-only; the rest apply (§12) |

---

## 10. Table A8 rows touching CRE

[FACT] Table A8 (PDF p. 220; md sec-209; values verified 2026-07-16 and 2026-08-03): the wholesale-relevant rows are **"Domestic CRE" (1.081)** and **"Rest of wholesale" (1.113)**. Footnote 63 lists "domestic CRE" as its own scalar category (PDF p. 184 footer; md 5354). The scalar mechanism's only worked example is stated on CRE: "if the calculated interest income in the domestic CRE portfolio is 95% of the value reported in the FR Y-14Q, Schedule G2, then the Board proposes to use a scalar of 1/0.95 = 1.05…" (PDF pp. 183–184; md sec-166) — the single place v.a(1) names a specific portfolio inside the scalar discussion.

Open mapping problems, all under **OQ-010** (source side unchanged):

1. **No scalar row is assigned to any CRE portfolio.** Whether "Domestic CRE" multiplies this section's three domestic portfolios, and what multiplies the international ones, is unstated.
2. **No row names international CRE** (wholesale brief §11 row 6 sub-question) — "Rest of wholesale" is the residual candidate by elimination, which is inference.
3. **The owner-occupied interaction:** PID-LOAN-11 assigned the "Domestic CRE" row to Corporate's domestic owner-occupied CRE for project implementation. If the same row also multiplies this section's domestic portfolios (the candidate below), one published scalar spans exposures on both sides of the Corporate/CRE boundary — internally consistent with footnote 63's "domestic CRE" being a category cutting across the two wholesale parts, but nowhere stated.

**RESOLVED FOR PROJECT IMPLEMENTATION (2026-08-12) — [PID-LOAN-21], user-confirmed:** the reference results blocks reproduce Total = (Fixed + Variable) × **1.081** for the three domestic categories and × **1.113** for the merged international block, exactly, on the 2026-08-12 screenshots; the confirmed mapping is domestic construction / multifamily / non-owner-occupied → "Domestic CRE" and international → "Rest of wholesale". The Board states no correspondence anywhere, so **OQ-010 remains open on the source side and for Retail** regardless.

[CODE] The scalar multiplies every quarter's output, so a misassignment is systematic; the category→row map stays configuration with an unmapped-category hard error (Corporate brief §10 [CODE], unchanged).

---

## 11. Board questions touching CRE

Verbatim census in common §13; pointers only here.

- **A153** — the only question naming CRE (verbatim in common §13; page image re-read 2026-08-12): "Should corporate and CRE variable-rate balances be further segmented to vary the interest rate floor? …" (PDF p. 187; md sec-172). The Fed itself treats wholesale floor granularity as open; bears on §5 row 7 and OQ-002.
- **A154** — segmentation comment request covering "both wholesale and retail portfolios", which includes the §3–§4 structure.
- **A152**, **A155**, **A157**, **A159** — inherited (wholesale base rate; wholesale fixed-rate spread approach; scalar granularity; hedges); see the wholesale and common briefs.

[FACT absence] No Board question asks about CRE data availability, the international portfolios' granularity, or the CRE type definitions — the Fed does not itself flag them as open.

---

## 12. Fed-stated limitations bearing on CRE

The Wholesale Portfolio limitations subsection (PDF pp. 185–186; md sec-171) is owned by the wholesale brief §12; its CRE-relevant items:

1. [FACT] **Index proxy and granularity** — the 3M Treasury "is a strong proxy"; loan-level projection would add accuracy over segment cuts. Applies to CRE unchanged.
2. [FACT] **Fixed-rate precision** — a more precise measure of when the jump-off rate was set; actual maturity dates and facility-specific PDs would improve re-origination timing. [INT] Bites CRE most among wholesale portfolios, given §7's fixed-rate prevalence note; nothing quantitative is stated.
3. [FACT] **Variable-rate floors** — "a more granular approach would improve the accuracy of the interest rate floor." Pairs with Question A153 (§11).
4. [FACT] **Constant roll-off and its defense** — including "applying a conservative roll-off rate for fixed-rate loans" (quoted in full, wholesale §9). [INT] Same CRE salience as item 2.
5. [FACT] **Revolver draws not increased** — wholesale-located (wholesale §12 item 6). [INT] The nearest statement to construction-facility draw behavior the section contains (§8 row 4); the source nowhere addresses construction draws as such.
6. The **NPML proxy** item is Corporate-specific and does not touch CRE (§8 row 1).

[FACT absence] There is no CRE-specific assumptions or limitations subsection (§8 row 2).

---

## 13. Coding considerations — [CODE], non-normative

Nothing in this section is Fed methodology. No production Python in this phase; the engine extension is the follow-on gated task.

- **Two grids, one labeling rule.** Configuration carries the Fed-side census (6 portfolios × 2 × 2 = 24 cells) and the physical grid (4 categories × 2 × 2 = 16 cells) with an explicit portfolio→category map; the merged international block is labeled "Fed portfolios (4)–(6), merged (data-forced)" in every output, so the divergence is visible downstream rather than flattened into a fake single portfolio (§4.3).
- **Reference-key universe drives the segment census** (Corporate pattern, user-stated "the way we did similar for Corp"): only keys in the mapping panel are consumed; rows whose line code is outside it (including DO-NOT-USE codes 4/6) are **excluded and censused with exposure, never silently dropped** — and never allocated balance, since they belong to no CRE category (contrast the within-category variable-type 0/4 rows, which the observed construction keeps as balance-only, §0.1 d).
- **Loader parallels with declared differences.** Header row 4; exact header spellings confirmed at load (the H.1 sheet's "Variablility" spelling precedent — never assume, name misses); the HFS/FVO weighting quantity ("Launchpoint Value") needs its column identified before the spec is written (§5 row 5); unit scales D-006 TO_BE_CONFIRMED, refuse-to-run, never inferred from magnitude.
- **Do not assume Corporate's converged engine semantics.** The CRE constructions are registered PIDs and differ from the Corporate reference engine on two points: the hybrid mixed spread (PID-LOAN-23 vs. Corporate's PID-LOAN-15 merge at the floating spread) and the outstanding-weighted origination date (PID-LOAN-22 vs. Corporate's PID-LOAN-4 unweighted median). The engine selector must permit per-wholesale-part constructions; the §0.1 residual items (i)–(iv) close at spec stage.
- **Scalar as configuration** with the PID-LOAN-11 override path and unmapped-category hard error; the PID-LOAN-21 assignment enters config as user-confirmed.
- **Non-normative FR Y-9C anchor (unverified).** The workbook's mapping sheet ties the H.2 codes to FR Y-9C Schedule HC-C item 1 subitems (1.a(1) and 1.a(2) construction and land development; 1.d multifamily; 1.e(2) non-owner-occupied nonfarm nonresidential; the international code as HC-C item 1 in non-domestic offices excluding owner-occupied nonfarm nonresidential). The FR Y-9C is not in `sources/`; this is recorded to speed the later mapping confirmation, never as methodology (cf. Corporate brief §13's cross-walk caution; OQ-038/OQ-039).

---

## 14. Open questions

| ID | Status | Relevance to this brief |
|---|---|---|
| **OQ-039** | OPEN — **filed 2026-08-12 with this brief** | The FR Y-14Q schedule carrying CRE facility data is unnamed; "H.2" appears nowhere in the document; the suite-level schedule list omits Schedule H entirely (§2.2) |
| **OQ-035** | OPEN | Whether the Corporate-stated mixed/demand/fee-only rules reach CRE — wholesale-owned; this brief records the physical context (no demand code; mixed/fee codes exist; confirmed treatments PID-LOAN-23/24) without resolving the source question (§6.2–§6.3) |
| **OQ-010** | CRE leg **RESOLVED FOR PROJECT IMPLEMENTATION 2026-08-12 (PID-LOAN-21)** — source side and Retail OPEN | No scalar row is assigned to any CRE portfolio in the source, and no row names international CRE; the confirmed project mapping is §10 |
| **OQ-001** | **OPEN for CRE** | wt inputs — resolved for Corporate only (PID-LOAN-6); the CRE analogue is a spec-stage decision (§5 row 9); the one Corporate-resolved gap still open for CRE |
| **OQ-002** | CRE leg **RESOLVED FOR PROJECT IMPLEMENTATION 2026-08-12 (PID-LOAN-18 + PID-LOAN-25)** — source-side absence preserved; Retail OPEN | Floor values from the H.2 floor column; variable-floor collapse per PID-LOAN-25 with a first-run floor census; fixed-engine floor treatment is residual item §0.1(iii) |
| **OQ-003** | CRE weighting basis **confirmed (PID-LOAN-22)**; median-vs-mean formula spec-stage; source side preserved | Outstanding-weighted origination-date statistic (§5 row 8) — differs from Corporate's PID-LOAN-4 unweighted median; the wholesale parts legitimately diverge |
| **OQ-033** | OPEN | Firm dimension of the fixed-rate machinery; applies to CRE fixed segments (common §7.6) |
| OQ-034 / OQ-038 | OPEN — Corporate-owned | Cited here only as contrasts (§2.2, §4.2); no CRE content |

---

## 15. Source traceability table

| # | Claim / element | Class | PDF p. | md anchor | Verification |
|---|---|---|---|---|---|
| 1 | CRE is one of the two wholesale parts | FACT | 175 | sec-153 | Page image 2026-07-30 |
| 2 | HFI vs. FVO/HFS stated for each wholesale section | FACT | 175 | sec-153 | Page image 2026-07-30 |
| 3 | Six-type enumeration, verbatim and complete; "as defined in FR Y-9C"; "(also referred to as portfolios)" | FACT | 176 | sec-155 | **Page image at high zoom 2026-08-12** |
| 4 | Rate-variability split "similar to Corporate" | FACT | 176–177 | sec-155 | Page image 2026-08-12 |
| 5 | "the total number of CRE segments is 24" | FACT | 177 | sec-155 | Page image 2026-08-12; 6×2×2 is [INT] (§4.2) |
| 6 | Footnote 61 (facility level); footnote 62 ("floating") | FACT | 175 (footer) | md 5350, 5352 | Integrity review + page images 2026-07-30 |
| 7 | No CRE portfolio named data-limited (Corporate names exactly three) | FACT absence | 176 | sec-154, sec-155 | Page images 2026-08-03 / 2026-08-12 |
| 8 | Owner-occupied CRE sits in Corporate; farmland sits in Corporate | FACT | 175 | sec-154 | Page image 2026-08-03 (Corporate brief rows 4, 3.1) |
| 9 | SQ-22 owner-occupancy naming variants | FACT (SQ-22) | 175–176 | sec-154, sec-155 | Page images 2026-08-03 |
| 10 | "In wholesale, fixed-rate products are more common for CRE income-producing loans." | FACT | 183 | sec-165 | Page image 2026-07-30; **re-read 2026-08-12**; uniqueness search 2026-08-12 |
| 11 | Scalar worked example names "the domestic CRE portfolio" | FACT | 183–184 | sec-166 | Page images 2026-07-30 |
| 12 | Footnote 63 lists "domestic CRE" as a scalar category | FACT | 184 (footer) | md 5354 | Integrity review + page image 2026-07-30 |
| 13 | Table A8 rows "Domestic CRE" 1.081; "Rest of wholesale" 1.113 | FACT | 220 | sec-209 | Page images 2026-07-16, 2026-08-03; OQ-010 |
| 14 | Question A153 names corporate and CRE (verbatim in common §13) | FACT | 187 | sec-172 | Page image 2026-07-30; **re-read 2026-08-12** |
| 15 | Wholesale Portfolio limitations (CRE-relevant items §12) | FACT | 185–186 | sec-171 | Page images 2026-07-30 |
| 16 | "H.2"/"Schedule H.2" zero occurrences; suite-level list = Schedules G/B/M + FR Y-14M; H.1 named only in the NPML paragraph | FACT absence | whole doc; 172; 176 | sec-149, sec-154 | **Full-document searches 2026-08-12**; OQ-039 |
| 17 | "committed", "undrawn", "workout", loan-sense "renewal" absent | FACT absence | whole doc | — | Full-document searches 2026-08-12 |
| 18 | PID-LOAN-18 / 19 / 20 (H.2 contract; four-category mapping and international merge; M.1 wiring) | **PID** | — | — | User confirmations 2026-08-12 — never attributable to the Federal Reserve |
| 19 | PID-LOAN-21 / 22 / 23 / 24 / 25 (scalar assignment; weighted origination date; hybrid mixed spread; fee/DNU balance-only; variable-floor collapse) | **PID** | — | — | Screenshot-evidenced and user-confirmed 2026-08-12 — never attributable to the Federal Reserve; residual items §0.1 (i)–(iv) remain flagged |

---

### Brief completion checklist

- [x] Status banner present; no adoption language anywhere.
- [x] Every material statement labeled [FACT]/[PID]/[INT]/[CODE]/[OQ]/[ALT]; unknowns stated UNKNOWN, never defaulted.
- [x] **Zero verbatim equation blocks** — equations cited from the common brief per D-010(b).
- [x] The six-type enumeration verified at high zoom against the PDF page image (2026-08-12).
- [x] The 24-segment grid restatement carries an unmissable [INT] banner; the Fed-side/physical-grid divergence is a labeled PID, never presented as Fed methodology.
- [x] Corporate and Retail appear only as explicit source-drawn boundaries (§2.3); neither is analyzed.
- [x] Inheritance register (§9) makes the common/wholesale boundary auditable; nothing owned elsewhere is restated; all four wholesale-brief §11 CRE deferrals (rows 4, 5, 6, 7) are absorbed (§3, §7, §10, §6).
- [x] Workbook context confined to PID citations and the §0.1 residual flagged items; **no confidential values, sheet names, or firm data** — logical contract only.
- [x] Source quirks preserved verbatim (SQ-22 cited); no silent corrections; no new quirks found in the CRE passage.
- [x] No production Python; the engine extension is the follow-on gated task.
- [x] Review state: **APPROVED 2026-08-12** (banner and checklist updated at approval).

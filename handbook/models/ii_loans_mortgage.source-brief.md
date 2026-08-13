# Source Brief — Interest Income on Loans: Mortgage (`ii_loans` — retail/mortgage)

> **STATUS: Proposed for the 2026 stress test — public-comment stage, NOT adopted.**
> Component: **Interest Income on Loans**, Section v.a(1) (PDF pp. 173–188; md sec-150–172); this brief covers the **Mortgage** family of Retail (PDF pp. 177–178; md sec-157), plus the mortgage-relevant passages elsewhere in v.a(1): the retail census entry (PDF p. 177; md sec-156), the base-rate entries (PDF p. 181; md sec-163), the fixed-rate prevalence note (PDF p. 183; md sec-165), the Retail Portfolio limitations' mortgage exception (PDF p. 185; md sec-170), Table A8's Mortgage row (PDF p. 220; md sec-209), and footnote 63's "mortgage" category (PDF p. 184 footer; md 5354). Model type per Table A6: **Structural**.
> Deliverable: loans workstream (asset-side Increment 3), retail wave 2 — drafted 2026-08-12 with the card and other-consumer briefs at the user's direction (accelerating the original per-family gate order; the framework + auto briefs were drafted the same day). Review state: **DRAFT — awaiting user review.**
> Scope: **Mortgage only.** Retail-shared rules are cited from `ii_loans_retail.source-brief.md`, never restated; equations are **not** transcribed (D-010(b)); other families appear solely where the source draws an explicit boundary.
> Integrity flags relevant here: SQ-23 (Prime-for-retail abbreviation), SQ-18/OQ-033 (fixed-rate subscripts). **No new source quirk in the mortgage passage.** Open questions: **OQ-040** (base-rate boundary — this family's central source gap), the retail legs of OQ-001 (wt), OQ-002 (floors), OQ-010 (scalar row); OQ-033.
> Physical context: the user supplied the **"Mortgage query"** input sheet and the **"M.1 Balances"** retail wiring 2026-08-12 (screenshots; logical contract registered as **PID-LOAN-27** and **PID-LOAN-26** — §0.1); interpretive readings are **flagged observations (a)–(e)**, not yet confirmed. No firm values appear in this repository.
> Verification: **PDF pp. 177–178 read as page images 2026-08-12** (the mortgage subsection confirmed verbatim; md faithful); p. 185 at high zoom the same day. Citation format: (PDF p. N; md sec-M).

---

## 0. Classification legend and cross-reference discipline

Labels [FACT] / [PID] / [INT] / [CODE] / [OQ] / [ALT] per `ii_loans_common.source-brief.md` §0.

### 0.1 Project implementation decision register (user-supplied input contracts) and flagged observations

Two PIDs registered with this brief record **input contracts the user supplied 2026-08-12** ("here are the inputs I will be providing as well as the sheet names"); full text in `handbook/open-questions.md`. They are company conventions, never attributable to the Federal Reserve; only the logical contract is recorded — no balances, rates, or firm data.

| ID | Decision (one line) | Fed-source status of the same point |
|---|---|---|
| **PID-LOAN-27** | **Mortgage input = the "Mortgage query" sheet**: segment key {Lien Position: First lien \| Home equity \| HELOC} × {Loan Type: **HFI \| HFS/FVO** — the asset classification, despite the column name} × {Interest Rate Type: Fixed \| Variable} = **12 segments**; per segment `TOTAL_UPB` (dollars), `WEIGHTED_AVERAGE_RATE` (decimal), `WEIGHTED_AVERAGE_RATE_AFTER_<yyyymmdd>` at two cutoffs (observed 20241130 and 20240930 — post-cutoff-**origination** rate windows), `WEIGHTED_ARM_FLOOR` (decimal, variable segments); companion per-segment × PQ1–PQ9 `TOTAL_UPB` **maturing-balance schedules**; the sheet carries **two classification variants** whose first-lien Fixed/Variable split differs materially (each with its own launch table and PQ schedule); a literal **"x"** cell = no observation in the window | The Fed states Y-14M loan-level weighted rates by segment and firm (PDF pp. 177–178) and names no physical layout; the lien-position dimension is the firm's refinement (§4.3) |
| **PID-LOAN-26** | **M.1 retail wiring** (shared with the card/other-consumer briefs): the M.1 Balances sheet carries an "FRB NII model" **role-label pair per data row** (domestic col A / international col B) and **four retail flag columns** headed "Mortgage (dom)", "Auto (dom)", "Card (dom)", "other consumer"; mortgage-family domestic roles observed: "Retail - mortgage - first lien" (First mortgages row), "Retail - mortgage - home equity" (First lien HELOANs; Junior lien HELOANs), "Retail - mortgage - HELOC" (HELOCs row); **the international role of every retail row is "Retail - noncore"**; values per side E (HFI dom) / G (HFS-FVO dom) / I (HFI int) / K (HFS-FVO int), millions (D-006 as confirmed for wholesale) | The common framework states only "the portfolio balance from FR Y-14 Schedules" (PDF p. 174); the Fed's international-consumer-in-noncore census (PDF p. 180) is **physically realized** by the international role labels |

**Flagged observations (a)–(e) — screenshot readings, TO CONFIRM at the review gate (the CRE (a)–(e) precedent):**

- **(a) Which classification variant drives the FRM/ARM split.** The two launch tables agree on every home-equity and HELOC segment but split first-lien balances between Fixed and Variable very differently — the signature of a **hybrid-ARM treatment choice** (ARMs inside their initial fixed period counted as Variable in one variant, Fixed in the other). Which variant feeds the model — and what rule separates them — decides the family's scenario sensitivity. [Also the physical form of the Fed's FRM-vs-ARM split, which the source states without a definition.]
- **(b) Which `AFTER` window is the Equation A36 numerator.** Two candidate new-origination windows exist (post-quarter-start ≈ the jump-off quarter's originations; post-final-month). A36 says "new originations at t=0" without a window; the workbook's spread cell decides. Ask alongside: what the spread cell **subtracts** — the mortgage rate or Prime, and at which date — which is exactly **OQ-040(a)** in physical form.
- **(c) wt = maturity-only, per segment.** The per-segment PQ schedules are contractual **maturing balances** — the PID-LOAN-6 pattern (maturity-only, no default/prepayment legs). For a prepayment-dominated family this repeats the recorded wholesale divergence at larger scale; confirm the schedule's meaning and the wt denominator (segment launch UPB).
- **(d) "x" = missing observation.** Sparse segments print a literal "x" in the `AFTER` columns (thin or empty origination windows). The loader must read "x" as MISSING with a per-segment census — never as zero (the PID-SEC-6 error-literal discipline; a fixed segment with no window observation needs a stated fallback, TO CONFIRM).
- **(e) Fixed-rate HELOC segments exist.** The 12-segment key gives HELOC × Fixed cells (fixed-rate draws/locks). Their engine (fixed machinery despite the HELOC-on-Prime base-rate entry) and their OQ-040 base-rate assignment need the user's reading.

### 0.2 Wave-3 engine observations (2026-08-13) — user-supplied calculation-sheet screenshots, TO CONFIRM at the gate

The user supplied the mortgage calculation sheets' layout the day after drafting ("here's how they calculate everything"). Readings below are screenshot observations — arithmetic-verified where stated — awaiting one-line confirmations at the combined gate; each names the §0.1 item or OQ it sharpens. **No firm values enter this repository.**

| # | Observation | Sharpens |
|---|---|---|
| (f) | **The two classification variants are two calc sheets** (a primary and an alternative; tab names config-local). The primary keys rate type off a FR Y-14M **"Interest Type - Current"** field (code M248), with M953 = the HFI/FVO-HFS flag, M197 = the UPB-weighted rate, M201 = segment UPB — the query is a Y-14M field-level aggregation | §0.1 (a) becomes a sheet-selection question — **RESOLVED 2026-08-13 (user-stated, PID-LOAN-33): the MORT-variant sheet drives production; the alternative sheet is unused** |
| (g) | **The A36 window is a declared switch** — a header cell reading "1=new origination in latest month; 0 = latest quarter", observed set to **0** (the jump-off-quarter origination window) | §0.1 (b) mechanism confirmed; production setting to confirm |
| (h) | **Base-rate assignment observed: the mortgage rate for the first-lien AND home-equity blocks (fixed and variable alike); Prime for the HELOC blocks** — each block's launch base equals that series' PQ0 value. Anomaly: the HE-HFI block heads its base column **"Median Date Base Rate"** (an Eq A37-style label) where every other block says "Base Rate at launch"; label meaning to confirm | **CONFIRMED 2026-08-13 (user-stated, PID-LOAN-33): mortgage rate for first-lien and home-equity blocks, Prime for HELOC — OQ-040 RESOLVED FOR PROJECT IMPLEMENTATION; "Median Date Base Rate" = the PQ0 mortgage rate (cosmetic label, no median-date lookup)** |
| (i) | **wt arithmetic-verified as maturity-only**: the engine's "Re-Origination Weight" equals the query's maturing-UPB schedule ÷ the segment's launch UPB (verified exactly on a first-lien PQ1 cell) | §0.1 (c) confirmed-as-observed; the prepayment-omission divergence (OQ-001 retail leg) is now concrete and stands as this family's recorded-divergence risk |
| (j) | **Missing-window fallback observed**: a fixed segment with "x" in both `AFTER` windows takes its **own current weighted rate** as the new-origination rate | §0.1 (d) sharpened into a stated rule; **still open — elaboration supplied to the user 2026-08-13, cell check pending** (the one §0.2 item not yet confirmed) |
| (k) | **Balance wiring and income arithmetic-verified**: each block's multiplicand = the M.1 sub-family row sum per side (first lien; the two HELOAN rows; HELOC) in dollars, allocated across segments by the query's UPB shares; the variable path is **floored at the query's ARM floor** (a binding quarter observed); income = fixed-weighted rate × fixed balance ÷ 4 + variable rate × variable balance ÷ 4; **Total = (Fixed + Variable) × 1.014** — the Table A8 Mortgage row on the PID-LOAN-16 semantics | Confirms the PID-LOAN-26 flag-sum reading at sub-family grain; the OQ-002 mortgage leg (ARM-floor source and bind) and the OQ-010 Mortgage-row assignment are observed; confirmation upgrades both |
| (l) | **The sheet stacks the next cycle's launch section below the current one** (a later-PQ0 copy of the same block structure) | [CODE] the loader must anchor on the configured `launch_point`, never on row order |

---

## 1. Executive summary

**What Mortgage is.** [FACT] The first retail section: "Mortgage (including first lien, home equity loans, and home equity lines of credit)" (PDF p. 177; md sec-156).

**How Mortgage segments.** [FACT] "The segmentation of mortgage and home equity products is driven primarily by asset classification, loan rate, and loan structure. They are segmented first by asset classification (HFI and FVO/HFS) and then rate structure (i.e., fixed-rate mortgage vs. adjustable-rate mortgage [ARM]). Additional segmentation variables, such as loan term (30-year vs. 15-year) and origination risk segments (FICO ≥ 720 vs. FICO < 720), were considered, but ultimately not adopted due to their immaterial impact on projected interest income. Balance-weighted average loan rates are calculated by segment and by firm based on the FR Y-14M loan-level data and used as inputs in interest income projections." (PDF pp. 177–178; md sec-157)

**How Mortgage prices.** [FACT] ARM products reprice on the **mortgage rate** (PDF p. 181; md sec-163); HELOC on **Prime** (same register entry); fixed segments run the A34/A35/A38 machinery with the Equation A36 new-originations spread. The Retail Portfolio limitations exempt "mortgages" from the Prime rule "in projecting variable-rate **and new origination** rates" (PDF p. 185; md sec-170) — making mortgage the only retail family with its own base rate.

**What is unresolved.** **OQ-040** — the base rate for FRM and fixed home-equity-loan new originations is never stated verbatim (working reading: the mortgage rate, per the p. 185 exception; HELOC on Prime as stated). Physically: the classification-variant choice (a), the A36 window and subtrahend (b), wt (c), and the retail legs of OQ-001/OQ-002/OQ-010.

---

## 2. Mortgage scope and boundaries

### 2.1 Position in the hierarchy

[FACT] Mortgage is the first of the four retail sections (PDF p. 177; md sec-156) — a **section**, not a Table A6 component; D-003 keeps all families in one chapter.

### 2.2 Explicit boundaries

| Boundary | Source statement | Label |
|---|---|---|
| **International mortgage and international home equity are Other Consumer** | The non-core census (PDF p. 180; md sec-160) | [FACT]; physically realized — every mortgage M.1 row's international role is "Retail - noncore" [PID-LOAN-26] |
| Mortgage is therefore a domestic family | Not printed; follows from the p. 180 census | [INT] (framework §2.3) |
| **Multifamily and other commercial real estate are Wholesale** | CRE portfolios (PDF p. 176; md sec-155); the mortgage section covers "Residential real estate (1-4 family)"-type products by its census (first lien, HEL, HELOC) | [FACT] placement; the 1-4-family characterization is the M.1 line structure, project context |
| HELOC is inside Mortgage but takes the Prime base rate | Census (PDF p. 177) + base-rate register (PDF p. 181) | [FACT]; OQ-040 boundary |

---

## 3. Mortgage census

### 3.1 The three product groups (verbatim)

[FACT] "Mortgage (including first lien, home equity loans, and home equity lines of credit)" (PDF p. 177; md sec-156); the subsection heading covers "mortgage and home equity products" (PDF p. 177; md sec-157).

### 3.2 Per-product attribute register

Coding-friendly names are this project's, not the Fed's. The Fed's stated grid does not name the product groups as a dimension (§4.3).

| # | Product group | Coding-friendly name | Base rate | Physical realization (project context) |
|---|---|---|---|---|
| 1 | first lien (mortgages) | `mtg_first_lien` | ARM: mortgage rate [FACT]; FRM new-orig: OQ-040(a) | Lien Position "First lien" [PID-LOAN-27]; M.1 First mortgages row, dom role "Retail - mortgage - first lien" [PID-LOAN-26] |
| 2 | home equity loans | `mtg_home_equity` | fixed HEL: OQ-040(b); variable HEL: unstated (Prime candidate via the register's HELOC entry vs mortgage-rate candidate via the p. 185 exception — same OQ) | Lien Position "Home equity"; M.1 First lien HELOANs + Junior lien HELOANs rows, dom role "Retail - mortgage - home equity" |
| 3 | home equity lines of credit | `mtg_heloc` | **Prime** [FACT, PDF p. 181] | Lien Position "HELOC"; M.1 HELOCs row, dom role "Retail - mortgage - HELOC"; fixed-rate HELOC cells exist — flagged (e) |

### 3.3 Rejected segmentation — [ALT]

[ALT] Loan term (30-year vs. 15-year) and origination risk (FICO ≥ 720 vs. < 720) "were considered, but ultimately not adopted due to their immaterial impact on projected interest income" (PDF pp. 177–178; md sec-157) — the mortgage counterpart of the auto brief's rejected risk segments.

---

## 4. Mortgage segmentation hierarchy

### 4.1 The Fed-stated dimensions

| Level | Dimension | Values | Source |
|---|---|---|---|
| 0 | Retail family | Mortgage | [FACT] PDF p. 177; md sec-156 |
| 1 | Asset classification | HFI; FVO/HFS | [FACT] "segmented **first** by asset classification (HFI and FVO/HFS)" (PDF p. 177; md sec-157) — the only retail family with a stated classification split |
| 2 | Rate structure | fixed-rate mortgage; adjustable-rate mortgage (ARM) | [FACT] PDF p. 177; md sec-157 |

[FACT of absence] The Fed states **no mortgage segment total** and does not print the product groups (first lien / HEL / HELOC) as a segmentation level — the census names them as contents, the grid names classification and rate structure only. No FRM/ARM definition is given (in particular, no treatment of hybrid ARMs in their initial fixed period).

### 4.2 The Fed-side grid restatement

[INT] Read literally, the stated grid is {HFI, FVO/HFS} × {FRM, ARM} per mortgage product = 4 cells per product group. No total is stated; the restatement exists only to anchor the physical comparison below.

### 4.3 The physical realization (project context — [PID-LOAN-27]; never Fed methodology)

The firm's query adds **lien position** as an explicit product dimension: {First lien, Home equity, HELOC} × {HFI, HFS/FVO} × {Fixed, Variable} = **12 segments**. This is **finer** than the Fed-stated grid — consistent with the retail drivers sentence ("rate structure …, **product type**, and credit risk", PDF p. 177; md sec-156) and with the census's three named product groups, but the 12-cell shape is the firm's, not the Board's.

| Fed-side grid | Physical grid |
|---|---|
| {HFI, FVO/HFS} × {FRM, ARM}; product groups named as contents, not cells [FACT] | {First lien, Home equity, HELOC} × {HFI, HFS/FVO} × {Fixed, Variable} = 12 cells [PID-LOAN-27] |

**Flagged observation (a) — the classification-variant question.** The query carries two parallel launch tables (each with its own PQ schedule) that agree on every home-equity and HELOC cell but split **first-lien** balances between Fixed and Variable very differently. [INT — reading, unconfirmed] The variants embody two hybrid-ARM conventions: ARMs still inside their initial fixed period counted as Variable (contract-type reading) versus Fixed (current-repricing reading). Which variant the model consumes is the physical form of the Fed's undefined FRM/ARM split and materially changes the family's scenario sensitivity — a gate question, then a PID.

---

## 5. Data inputs and classifications to capture

Every row states whether the source names the item; physical realizations are PID-cited project context. **No firm values appear here.**

| # | Item to capture | Source status | Physical realization (project context) | Notes |
|---|---|---|---|---|
| 1 | Loan-level data basis | [FACT] "based on the FR Y-14M loan-level data" (PDF p. 178) | The query is a **segment-level aggregation** of that loan-level base [PID-LOAN-27] | Grain consistent with the framework's data-basis register |
| 2 | Segment key | [FACT] classification + rate structure; product groups as contents | 12-cell key (§4.3) | Flagged (a) — variant choice |
| 3 | Jump-off balance-weighted rate per segment | [FACT] "Balance-weighted average loan rates … by segment and by firm" (PDF p. 178) | `WEIGHTED_AVERAGE_RATE` (decimal) | The Eq A32/A34 seed |
| 4 | Segment balances | [FACT] via the common balance construction | `TOTAL_UPB` (dollars) | Share basis within the family — spec stage |
| 5 | New-origination rate (Eq A36 numerator) | [FACT] "only new origination loans are used" (PDF p. 182); window undefined | `WEIGHTED_AVERAGE_RATE_AFTER_<yyyymmdd>`, two cutoffs | Flagged (b): which window; what the spread subtracts = **OQ-040(a)** physical form; "x" = missing — flagged (d) |
| 6 | Variable floors | [FACT] the common floor rule (PDF p. 180); no mortgage statement | `WEIGHTED_ARM_FLOOR` (decimal, variable segments) | **Candidate OQ-002 mortgage-leg resolution** — already segment-collapsed (weighted), unlike wholesale's per-facility floors; confirm weighting basis at the gate |
| 7 | wt inputs | [FACT] default/prepayment/maturity derivation (PDF p. 183) | Per-segment × PQ maturing-balance schedules | Flagged (c): maturity-only = PID-LOAN-6 pattern; prepayment omission is the recorded-divergence risk, largest for this family — **OQ-001 retail leg** |
| 8 | Portfolio balance (Eq A32 multiplicand) | [FACT] "the portfolio balance from FR Y-14 Schedules" (PDF p. 174) | M.1 mortgage-role rows per side (First mortgages; First lien HELOANs; Junior lien HELOANs; HELOCs), E/G domestic; family total = the "Mortgage (dom)" flag column [PID-LOAN-26; flag-sum construction TO CONFIRM] | International sides → noncore |
| 9 | Scenario base rates | [FACT] mortgage rate (ARM); Prime (HELOC) | `mortgage_rate`, `prime_rate`; MEV columns TO_BE_CONFIRMED | **OQ-040** for FRM/fixed-HEL new originations |
| 10 | Industry scalar | [FACT] Table A8 "Mortgage" 1.014; assignment unstated | Candidate: the whole family × 1.014 | **OQ-010 retail leg** (§11) |

[FACT of absence] The source names no Y-14M field, no aggregation rule, and no new-origination window; every physical entry above is project context under PID-LOAN-26/27.

---

## 6. Rate-type treatment for Mortgage

- [FACT] The family is the only retail family with **both** engines stated: ARM segments reprice (Eq A33 machinery, mortgage rate); fixed segments run Eqs A34/A35/A38 with the A36 spread (common §7.6; framework §7).
- [FACT] The base-rate register: "the mortgage rate is used for adjustable-rate mortgage products"; HELOC under Prime (PDF p. 181; md sec-163). The p. 185 exception extends the mortgage rate to "new origination rates" for "mortgages" — the **OQ-040** boundary (framework §5.3): FRM new originations [INT: mortgage rate]; fixed HELs [INT: mortgage rate, weaker]; HELOC [FACT: Prime].
- [FACT of absence] No FRM/ARM definition; no hybrid-ARM treatment; no reset-frequency statement for ARMs beyond the common "Most variable rates are repriced quarterly" (assumption (5)). Flagged (a) is the physical shadow of this absence.
- Flagged (e): fixed-rate HELOC cells exist physically; their engine and base rate need the user's reading (a fixed-rate balance inside the family whose stated base-rate entry is Prime-for-HELOC).

---

## 7. The re-origination weight for Mortgage

- [FACT] wt derives from "the default rate, prepayment rate, and maturity rate" (PDF p. 183) — **OQ-001 retail leg, OPEN**; no mortgage-specific statement exists.
- Flagged (c): the query's PQ schedules are contractual maturing balances — the maturity-only PID-LOAN-6 pattern. [INT] For 30-year collateral, contractual maturity inside a 9-quarter window is a tiny share of the book while prepayment is the dominant runoff channel; a maturity-only wt therefore understates re-origination far more for mortgage than it did for wholesale. Recorded as the family's principal divergence risk; the gate question asks whether the workbook adds any prepayment leg.

---

## 8. Floors for Mortgage

[FACT] The common rule applies (PDF p. 180); no mortgage floor statement exists. Physical context: `WEIGHTED_ARM_FLOOR` supplies a per-segment weighted floor for variable cells [PID-LOAN-27] — a **candidate OQ-002 mortgage-leg resolution** (the first retail floor source observed), pending confirmation of its weighting basis and of the fixed-engine floor treatment (Corporate's reference engine floors the A38 recursion at 0 — PID-LOAN-15; the retail analogue is unobserved).

---

## 9. Fact-of-absence register (mortgage)

| # | Absent for Mortgage | Contrast / nearest statement |
|---|---|---|
| 1 | **No FRM/ARM definition; no hybrid-ARM rule** | The split is the family's stated grid dimension (PDF p. 177) — flagged (a) is its physical shadow |
| 2 | **No mortgage segment total** | CRE's 24 is stated; Corporate's is not (OQ-034) — mortgage matches Corporate's silence |
| 3 | **No new-origination window definition** for Eq A36 | "only new origination loans" (PDF p. 182); flagged (b) |
| 4 | **No mortgage floor statement** | Common rule only (PDF p. 180); §8 |
| 5 | **No Board question names mortgage** | A156 is card-owned; A154 generic (PDF pp. 186–188) |
| 6 | **No servicing, escrow, points, or fee-income treatment** | The section is interest-income-only; nothing addresses mortgage fee income ([FACT] absence, cf. wholesale §10 pattern) |
| 7 | **No delinquency carve-out** beyond common assumption (2) | "delinquent loans generate interest income … immaterial" (PDF p. 184) |

---

## 10. Inheritance register — what Mortgage does not restate

| Rule | Governed by | Mortgage-specific note |
|---|---|---|
| Eq A32 income identity; 9 quarters; (b,p,i,t) | common §7.0 | — |
| Balance construction; flat balances; same-quarter replenishment | common §6 | Multiplicand wiring = PID-LOAN-26 (§5 row 8) |
| Rate type as the primary segmentation principle | common §7.2; framework §4.2 | Realized as level 2 of §4.1, after the stated classification-first ordering |
| Eq A33 variable path | common §7.3 | ARM on the mortgage rate; HELOC on Prime (§6) |
| Eqs A34/A35/A38 fixed machinery; Eq A36 spread | common §7.6; framework §7 | Window + subtrahend = flagged (b) / OQ-040 |
| Base-rate application incl. the mortgage exception | framework §5 | This family IS the exception; OQ-040 |
| Interest-rate floors | common §7.1; framework §8 | ARM-floor column = candidate resolution (§8) |
| Industry-scalar mechanism; Table A8 values | common §8; framework §10 | Row applicability §11 |
| Assumptions (1)–(7); general limitations | common §12 | No mortgage-specific assumption list exists |
| Retail Portfolio limitations | framework §12 | The ¶1 mortgage exception is this family's charter |
| Quarterly compounding versus D-004 | common §7.7 | Unresolved at project level |
| Hedge exclusion (Question A159) | common §11 | OQ-005 |

---

## 11. Table A8 row touching Mortgage

[FACT] Table A8 row **"Mortgage" = 1.014** (PDF p. 220; md sec-209); footnote 63 lists "mortgage" as its own category (PDF p. 184 footer). **OQ-010 retail leg:** no correspondence is stated; the natural reading (the whole family — first lien, HEL, HELOC — × 1.014) is an inference, and whether home-equity products fall under "Mortgage" or "rest of consumer"/"Noncore" is exactly the kind of boundary the Board never draws. Candidate PID at the gate; [CODE] config map with unmapped-family hard error.

---

## 12. Board questions touching Mortgage

[FACT of absence] No Board question names mortgage. Inherited: **A154** (segmentation, both hierarchies), **A157** (scalar), **A158** (spread factors), **A160** (general) — census in common §13.

---

## 13. Coding considerations — [CODE], non-normative

- **12-cell grid as configuration** with the classification-variant choice (flagged (a)) as a declared switch until the PID lands — never two hard-coded paths.
- **Query loader contract:** segment-level sheet; `Loan Type` column maps to the LOCOM/classification axis (naming trap — document the mapping in the loader); "x" → MISSING with per-segment census (flagged (d)); units D-006 (UPB dollars vs M.1 millions — declare both scales, refuse when unconfirmed).
- **A36 spread derivation as configuration:** window choice (which `AFTER` column) × subtrahend ({`mortgage_rate`, `prime_rate`} at a declared date) — the OQ-040 flag rides the config until confirmed; missing-window fixed segments need a stated fallback, surfaced never defaulted.
- **wt from the PQ schedules** (maturity-only) with the prepayment-omission divergence recorded per run; wt ≤ 1 guard as in wholesale.
- **Floors:** ARM-floor column per variable segment; fixed-engine floor treatment TO CONFIRM; floor census on first run (PID-SEC-18/PID-LOAN-25 lesson).
- **M.1 reconciliation monitor:** query family totals vs the M.1 "Mortgage (dom)" flag-sum — a consistency census, not an identity (different sources may differ; surface, never force).

---

## 14. Open questions

| ID | Status | Relevance to this brief |
|---|---|---|
| **OQ-040** | OPEN — framework-filed 2026-08-12 | The family's central gap: FRM/fixed-HEL new-origination base rate; HELOC-on-Prime stated; flagged (b) is its physical form (§6) |
| **OQ-001** | OPEN for retail | wt; maturity-only schedules observed — prepayment omission is the family's principal divergence risk (§7) |
| **OQ-002** | OPEN for retail — **candidate mortgage-leg resolution observed** | `WEIGHTED_ARM_FLOOR` (§8); confirm weighting basis + fixed-engine floor |
| **OQ-010** | OPEN for retail | "Mortgage" 1.014 assignment incl. the HEL/HELOC boundary (§11) |
| **OQ-033** | OPEN | Firm dimension; "by segment and by firm" (p. 178) already in the evidence set |
| OQ-041 / OQ-042 | OPEN — other-family-owned | Boundaries only; no mortgage content |

---

## 15. Source traceability table

| # | Claim / element | Class | PDF p. | md anchor | Verification |
|---|---|---|---|---|---|
| 1 | Census: first lien, HEL, HELOC | FACT | 177 | sec-156 | Page image 2026-08-12 |
| 2 | Classification-first, then FRM/ARM | FACT | 177 | sec-157 | Page image 2026-08-12 |
| 3 | Term and FICO splits considered, not adopted | **ALT** | 177–178 | sec-157 | Page images 2026-08-12 |
| 4 | Y-14M loan-level weighted rates by segment and firm | FACT | 178 | sec-157 | Page image 2026-08-12; OQ-033 evidence |
| 5 | Mortgage rate for ARM; HELOC under Prime | FACT | 181 | sec-163 | Page image 2026-07-30 |
| 6 | The p. 185 mortgage exception (variable + new origination) | FACT | 185 | sec-170 | Page image at high zoom 2026-08-12; OQ-040 |
| 7 | "fixed-rate mortgage and home loans" prevalence entry | FACT | 183 | sec-165 | Page image 2026-07-30; OQ-040(b) |
| 8 | Eq A36 retail branch | FACT | 182 | sec-165 | Transcription common §7.6 |
| 9 | Table A8 "Mortgage" 1.014; footnote 63 "mortgage" | FACT | 220, 184 | sec-209, md 5354 | Page images 2026-07-16 / 2026-08-03; OQ-010 |
| 10 | International mortgage/home equity in Other Consumer | FACT | 180 | sec-160 | Page image 2026-08-12 |
| 11 | PID-LOAN-26 / PID-LOAN-27 (M.1 wiring; Mortgage query contract) | **PID** | — | — | User-supplied 2026-08-12 — never attributable to the Federal Reserve; flagged observations (a)–(e) await the gate |

---

### Brief completion checklist

- [x] Status banner present; no adoption language anywhere.
- [x] Every material statement labeled; unknowns stated UNKNOWN; screenshot readings confined to PID contracts + flagged observations (a)–(e), no firm values.
- [x] **Zero verbatim equation blocks** (D-010(b)).
- [x] The mortgage subsection verified against page images (2026-08-12); [ALT] applied to the rejected splits.
- [x] Fed-stated grid preserved as [FACT]; the 12-cell physical grid labeled PID, never presented as Fed methodology.
- [x] Retail-shared rules cited from the framework brief; other families as boundaries only.
- [x] No production Python; no confidential values, formulas, or firm data — logical contract only.
- [ ] Review state: DRAFT — awaiting user review gate (combined retail gate).

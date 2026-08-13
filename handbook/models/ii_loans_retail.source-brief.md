# Source Brief — Interest Income on Loans: Retail Framework (`ii_loans` — retail)

> **STATUS: Proposed for the 2026 stress test — public-comment stage, NOT adopted.**
> Component: **Interest Income on Loans**, Section v.a(1) (PDF pp. 173–188; md sec-150–172); this brief covers the **methodology shared by the four Retail families — Mortgage, Auto Loan, Consumer and Small Business Credit Card, and Other Consumer Products** (PDF p. 177; md sec-156), plus the retail-located passages elsewhere in v.a(1): the retail base-rate entries (PDF p. 181; md sec-163), the Equation A36 retail spread branch and the retail fixed-rate prevalence note (PDF pp. 182–183; md sec-165), the non-core expert-judgment sentence (PDF p. 181; md sec-164), the Retail Portfolio limitations (PDF p. 185; md sec-170), Question A156 (PDF p. 187; md sec-172), Table A8's retail rows (PDF p. 220; md sec-209), and footnote 63's retail categories (PDF p. 184 footer; md 5354). Model type per Table A6: **Structural**.
> Deliverable: loans workstream (asset-side Increment 3), retail slice R1 per the approved plan of 2026-08-12 — **retail-framework brief**, fifth of the sibling set {common, wholesale, corporate, CRE, **retail** + family briefs}; drafted in one slice with `ii_loans_auto.source-brief.md` (user-confirmed bundling 2026-08-12). *(Amended same day: the user directed the mortgage, card, and other-consumer briefs be drafted immediately as well — all four family briefs now exist, drafted 2026-08-12, one combined review gate; SQ-25 and OQ-043 were filed with the card brief, and the user-supplied input contracts are PID-LOAN-26/27/28. Amendment recorded, not silent.)* Review state: **DRAFT — awaiting user review.**
> Scope rule: this brief carries only methodology the source states **for retail as a whole** or for more than one retail family; family-specific rules are identified, cited, and **deferred** to the four family briefs (§3 register — the placement authority for the retail sibling set). Wholesale content appears solely where the source draws an explicit boundary; nothing wholesale is analyzed. Equation-ownership rule (D-010(b)): **this brief transcribes no equations** — all of Equations A32–A38 live verbatim in `ii_loans_common.source-brief.md` §7.
> Integrity flags relevant here: SQ-20 (A33 where-list), SQ-18/OQ-033 (fixed-rate subscripts); **filed with this brief: SQ-23** (p. 182 names Prime as *the* retail base rate, omitting the mortgage exception) and **SQ-24** ("non-core retails products", p. 185). Related OQs: OQ-001, OQ-002, OQ-010, OQ-011, OQ-012, OQ-033 (evidence strengthened with this brief); **filed with this brief: OQ-040** (mortgage-family base-rate boundary) and **OQ-041** (other-consumer engine assignment); OQ-042 is filed with the auto brief.
> Verification: **PDF pp. 177–180 read as page images 2026-08-12** (retail scoping + this drafting session — census, all four family subsections, and the sec-161 boundary confirmed; md conversion faithful, no discrepancies) and **p. 185 re-read as a page image at high zoom 2026-08-12** (the Retail Portfolio limitations — this brief's load-bearing base-rate sentence confirmed verbatim; SQ-24 found); pp. 173–188 had a full image pass 2026-07-30. Citation format: (PDF p. N; md sec-M).

---

## 0. Classification legend and cross-reference discipline

Labels [FACT] / [PID] / [INT] / [CODE] / [OQ] / [ALT] per `ii_loans_common.source-brief.md` §0.

### 0.1 Project implementation decision register

**No PID affects this brief, and no retail loans PID exists yet.** No physical sheet, line-item, field, or scenario-column mapping has been user-confirmed for any retail family — every physical sourcing statement below is source-stated [FACT] or UNKNOWN. The register will populate at the family elicitation stages (the Corporate PID-LOAN-2..8 pattern); the input requests are itemized in the approved plan of 2026-08-12 (Required with the R1 gate: retail sheet inventory; M.1 retail rows; Prime/mortgage-rate MEV columns; auto specifics; materiality census).

Ownership rule for the sibling set (D-010, extended to retail at the approved 2026-08-12 plan):

| Layer | Owns | Brief |
|---|---|---|
| Common | Eqs A32–A38 verbatim; balance construction; segmentation principle; base-rate register (transcription); spread definition; floors rule; scalar mechanism and Table A8 values; assumptions (1)–(7); question census; hedge exclusion | `ii_loans_common.source-brief.md` |
| Wholesale | Corporate∩CRE shared framework (3M Treasury; Eq A37 t−a; H.1 facility basis; wholesale limitations) | `ii_loans_wholesale.source-brief.md` |
| **Retail framework (this brief)** | The four-section census and retail segmentation drivers; the retail data-basis statement; the retail base-rate application (Prime-except-mortgages); the Eq A36 retail-branch application; the retail fixed-rate prevalence note; the Retail Portfolio limitations; Table A8 retail-row census; the retail-boundary register (§3) | this file |
| Family briefs | Per-family census, grids, data grain, spread mechanics, family-specific rules and elicitation items | `ii_loans_auto`, `ii_loans_mortgage`, `ii_loans_card`, `ii_loans_other_consumer` — all drafted 2026-08-12 (same-day amendment; one combined gate) |

**No new model is proposed anywhere in this brief.** The model documented is the Federal Reserve's proposed structural model under Equations A32–A38, unchanged.

---

## 1. Executive summary

**What "retail" is in this model.** [FACT] "Retail interest income projections are organized into four sections: (1) Mortgage (including first lien, home equity loans, and home equity lines of credit), (2) auto loan, (3) consumer credit card, and (4) other non-core credit products such as small business loans, SME cards, private student loans, and consumer finance products." (PDF p. 177; md sec-156)

**How retail segments.** [FACT] "Segmentation within a retail portfolio is driven by the rate structure (i.e., fixed vs. variable rate), product type, and credit risk. Data used in the segmentation of retail products are sourced from regulatory reports including FR Y-14M and FR Y-14Q schedules and include both loan-level and segment-level attributes. Data limitations prevent further segmentation of the non-core products." (PDF p. 177; md sec-156)

**How retail rates project.** [FACT] Variable-rate retail segments follow Equation A33 with the **Prime Rate** as base rate — "including consumer and small business credit cards and home equity line of credit" — while "the mortgage rate is used for adjustable-rate mortgage products" (PDF p. 181; md sec-163). Fixed-rate retail segments follow the Equations A34/A35/A38 machinery with the **retail spread branch** (Equation A36): the spread is measured from **new originations only**, at the jump-off quarter, against the jump-off base rate — a spot-only construction, unlike wholesale's t−a historical anchor (PDF pp. 182–183; md sec-165). The Retail Portfolio limitations generalize the base-rate rule: "The model assumes that all retail products **(except for mortgages)** use Prime Rate as base rate and constant spread by product, segment, and firm in projecting variable-rate and new origination rates." (PDF p. 185; md sec-170)

**What is unresolved.** On the source side: the exact boundary of the mortgage exception — the base rate for fixed-rate-mortgage and fixed home-equity-loan new originations is never stated verbatim (**OQ-040**, filed with this brief); the engine assignment for the other-consumer family — "no segmentation" (p. 180) sits in tension with the expert-judgment fixed/variable split (p. 181) and the "most non-core loans" fixed-rate prevalence note (p. 183) (**OQ-041**, filed with this brief); and the retail legs of OQ-001 (wt inputs), OQ-002 (floor values), and OQ-010 (scalar row assignment) remain open, as do OQ-011 (other-consumer jump-off mapping) and OQ-012 (revolver-share constancy). No physical mapping exists yet for any retail family.

---

## 2. Retail scope and boundaries

### 2.1 Position in the hierarchy

[FACT] Retail is one of the two loan hierarchies: "Retail interest income projections are organized into four sections" (PDF p. 177; md sec-156), parallel to "Wholesale interest income projections are organized into two parts" (PDF p. 175; md sec-153). Retail is a **hierarchy of sections**, not a Table A6 component — the Table A6 row is the single "Loans" component (PDF pp. 168–169; md sec-148), and D-003 keeps all portfolio families in one chapter.

### 2.2 What the source states about retail's own definition

[FACT] Retail, like Corporate, is defined **extensionally** — by the list of four sections — with no stated inclusion principle and no named defining form (contrast CRE's "as defined in FR Y-9C"; cf. OQ-038/OQ-039 on the wholesale side). The fourth section is itself a residual ("other non-core credit products **such as**…" — an open-ended list).

[FACT — contrast worth recording] The retail data-basis sentence is **complete**: "Data used in the segmentation of retail products are sourced from regulatory reports including FR Y-14M and FR Y-14Q schedules and include both loan-level and segment-level attributes" (PDF p. 177; md sec-156) — where the wholesale counterpart is the truncated "sourced from FR." (SQ-5). No new quirk arises here.

### 2.3 Explicit boundaries

Recorded because the source draws them; nothing outside retail is analyzed.

| Boundary | Source statement | Label |
|---|---|---|
| Wholesale is a separate hierarchy | "Wholesale interest income projections are organized into two parts" (PDF p. 175; md sec-153) | [FACT] |
| **Small-business exposures are retail** | Section (4) covers "small business loans, SME cards"; small business **cards** are modeled inside the card section "separately but following a similar structure" (PDF pp. 177, 179; md sec-156, sec-159) — while Table A8's "C&I, noncore SME loan and card" row spans the wholesale and retail naming worlds (§10; OQ-010) | [FACT]; scalar consequence OQ-010 |
| **International consumer exposures are all Other Consumer** | The non-core census names "international auto loans, international mortgage, international home equity, international small business loans" (PDF p. 180; md sec-160) — no retail family except (4) carries an international slice | [FACT]; consequence [INT] below |
| Home-equity products are Mortgage | Section (1) is "Mortgage (including first lien, home equity loans, and home equity lines of credit)"; the mortgage subsection covers "mortgage and home equity products" (PDF p. 177; md sec-156–157) | [FACT]; base-rate boundary OQ-040 |

[INT] Consequence of the international boundary: the Mortgage, Auto, and Card families are **domestic** families — their international counterparts live in Other Consumer. The source never prints the word "domestic" in those three subsections; the reading follows from the p. 180 census and is recorded as interpretation. Contrast wholesale, where each part carries its own international portfolios.

---

## 3. Retail-boundary register

Placement rule (the common brief §3 discipline, applied to the retail hierarchy): a rule enters this framework brief only if the source states it for retail as a whole or for more than one family; otherwise it is assigned to the narrowest family the source states. Every retail-owned row of the common brief's §3 register (rows 13, 14, 22, 26, 30, 34, and the retail entries of rows 19 and 36) is accounted for below. "Owner" = where the rule is documented in full.

| # | Rule (short) | Stated at | Class | Owner |
|---|---|---|---|---|
| 1 | Four-section census (mortgage incl. HEL/HELOC; auto; consumer card; other non-core) | PDF p. 177; md sec-156 | FRAMEWORK | this brief §1, §4 |
| 2 | Segmentation drivers: rate structure, product type, credit risk | PDF p. 177; md sec-156 | FRAMEWORK | §4 |
| 3 | Data basis: FR Y-14M + FR Y-14Q; loan-level **and** segment-level attributes | PDF p. 177; md sec-156 | FRAMEWORK | §4.3 |
| 4 | Non-core: data limitations prevent further segmentation | PDF p. 177; md sec-156 | OTHER-CONSUMER (recorded here for the census) | other-consumer brief (drafted 2026-08-12); §4 |
| 5 | Mortgage segmentation (HFI/FVO-HFS × FRM/ARM; rejected term/FICO splits; Y-14M weighted rates) | PDF pp. 177–178; md sec-157 | MORTGAGE | `ii_loans_mortgage.source-brief.md` (drafted 2026-08-12) |
| 6 | Auto rules (A.2 segment level; all fixed; HFS→HFI; new/used; Prime spread) | PDF p. 178; md sec-158 | AUTO | `ii_loans_auto.source-brief.md` (this slice) |
| 7 | Card rules (bank/charge cards; all variable; revolver classification; reported rate and spread; SME cards separate-similar) | PDF pp. 178–179; md sec-159 | CARD | `ii_loans_card.source-brief.md` (drafted 2026-08-12); OQ-012 |
| 8 | Other-consumer rules (no segmentation; G.2-line jump-off rates; spread vs Prime) | PDF pp. 179–180; md sec-160 | OTHER-CONSUMER | `ii_loans_other_consumer.source-brief.md` (drafted 2026-08-12); OQ-011, OQ-041 |
| 9 | Expert judgment splits the non-core portfolio into variable- and fixed-rate products | PDF p. 181; md sec-164 | OTHER-CONSUMER (framework tension note §7.3) | other-consumer brief (drafted 2026-08-12); OQ-041 |
| 10 | Retail base-rate entries: Prime (retail variable incl. cards, HELOC); mortgage rate (ARM) | PDF p. 181; md sec-163 | FRAMEWORK application (common §7.4 owns the register transcription) | §5 |
| 11 | Eq A36 retail fixed spread from new originations | PDF pp. 182–183; md sec-165 | FRAMEWORK application (common §7.6 owns the transcription) | §7 |
| 12 | "The base rate applied is the same as the base rate for floating: the Prime Rate for retail…" | PDF p. 182; md sec-165 | FRAMEWORK — **SQ-23** (abbreviates away the mortgage exception) | §5.2 |
| 13 | Bias rationale for the new-originations approach | PDF p. 183; md sec-165 | COMMON (contrast recorded; common §7.6) | common brief |
| 14 | Retail fixed-rate prevalence: "fixed-rate mortgage and home loans, auto loans, and most non-core loans" | PDF p. 183; md sec-165 | FRAMEWORK (retail half of common §3 row 30) | §7.2 |
| 15 | Retail Portfolio limitations ¶1: Prime-except-mortgages, constant spread by product/segment/firm | PDF p. 185; md sec-170 | FRAMEWORK | §12; §5 |
| 16 | Retail Portfolio limitations ¶2: no rate data for most non-core; auto segment-level accuracy | PDF p. 185; md sec-170 | FRAMEWORK (owner); family pointers | §12; auto/other-consumer briefs |
| 17 | Question A156 (revolver classification alternatives) | PDF p. 187; md sec-172 | CARD | card brief (drafted 2026-08-12); §11 |
| 18 | Table A8 retail rows (Auto 0.865; Credit Card 0.969; Mortgage 1.014; Noncore 1.072) + footnote 63 retail categories | PDF pp. 184, 220; md 5354, sec-209 | FRAMEWORK census; per-row application per family | §10 |
| 19 | Revolver-draw limitation (no draw growth) — **wholesale-located**; revolving products also exist in retail | PDF p. 186; md sec-171 | Cross-reference only (wholesale §12 item 6 placement note) | §9 row 6 |
| 20 | wt from default/prepayment/maturity rates (credit-loss models) — retail leg | PDF pp. 174, 183; md sec-151, sec-165 | COMMON machinery; retail delivery **OQ-001 OPEN** | §7.4 |
| 21 | Portfolio-specific floors — retail leg | PDF p. 180; md sec-161 | COMMON rule; retail values **OQ-002 OPEN** | §8 |

---

## 4. Retail hierarchy and segmentation principles

### 4.1 The four families

Coding-friendly names are this project's, not the Fed's. Grid and rate-type summaries are [FACT] pointers into the family subsections; detail is family-owned.

| # | Fed section name | Coding-friendly name | Stated grid | Stated rate type | Data grain (stated) | Detail owner |
|---|---|---|---|---|---|---|
| 1 | Mortgage (incl. first lien, home equity loans, HELOC) | `ii_loans_mortgage` | HFI vs FVO/HFS, then FRM vs ARM | both | FR Y-14M loan-level | mortgage brief (drafted 2026-08-12) |
| 2 | Auto loan | `ii_loans_auto` | new vs used vehicle; HFS treated as HFI | **all fixed** (Board assumption) | FR Y-14Q Schedule A.2 **segment-level** | auto brief (this slice) |
| 3 | Consumer credit card (+ small business cards, separate-similar) | `ii_loans_card` | consumer bank vs charge cards; SME cards separately | **all variable** (Board assumption) | FR Y-14M (segment-level stated for SME cards) | card brief (drafted 2026-08-12) |
| 4 | Other non-core credit products | `ii_loans_other_consumer` | **none** ("no segmentation") | unresolved — OQ-041 | no rate data in the retail schedule; G.2-line jump-off | other-consumer brief (drafted 2026-08-12) |

### 4.2 Segmentation principles

- [FACT] "Segmentation within a retail portfolio is driven by the rate structure (i.e., fixed vs. variable rate), product type, and credit risk." (PDF p. 177; md sec-156) — consistent with the common principle that rate type is the primary split (common §7.2).
- [FACT] Credit-risk segmentation was **considered and rejected** where examined: mortgage FICO splits "were considered, but ultimately not adopted" (PDF p. 177; md sec-157) and auto "origination risk segments" are not proposed (PDF p. 178; md sec-158) — both [ALT], detailed in the family briefs. No adopted retail segmentation uses credit risk; the driver sentence names it as a consideration, not a mandate. [INT] The operative adopted drivers are asset classification (mortgage only), rate structure, and product type.
- [FACT of absence] **No retail-wide asset-classification statement exists.** HFI/FVO-HFS segmentation is stated for mortgage only (PDF p. 177; md sec-157); auto collapses HFS into HFI (PDF p. 178; md sec-158); the card and other-consumer subsections never mention asset classification. Contrast wholesale, where the classification is stated for each part (PDF p. 175; md sec-153).
- [FACT] Firm dimension: balance-weighted rates are computed "by segment and by firm" in the mortgage, auto, and card subsections (PDF pp. 177–179; md sec-157–159), and the Retail Portfolio limitations state "constant spread by product, segment, and firm" (PDF p. 185; md sec-170) — **evidence strengthening OQ-033's firm-level working reading** of the b-less A34/A35/A36/A38 subscripts (appended to the OQ-033 log entry with this brief).

### 4.3 Data basis

- [FACT] "Data used in the segmentation of retail products are sourced from regulatory reports including FR Y-14M and FR Y-14Q schedules and include both loan-level and segment-level attributes." (PDF p. 177; md sec-156) — the grain **varies by family**: Y-14M loan-level (mortgage; card), Y-14Q Schedule A.2 segment-level (auto), and no rate data at all (other consumer, whose jump-off rates come from "the FR Y-14Q pre-provision net revenue line-item report", PDF p. 180; md sec-160 — OQ-011).
- [FACT] The suite-level data statement names "FR Y-14Q, Schedule G; FR Y-14Q, Schedule B; FR Y-14Q, Schedule M; and FR Y-14M" (PDF p. 172; md sec-149). [FACT — recorded contrast] Schedule A.2, named in the auto subsection, is absent from that list (as Schedule H is — OQ-039's finding on the wholesale side); the auto brief records the pairing.
- [FACT of absence] No retail line item, field name, or extraction rule is stated anywhere in the retail subsections beyond the schedule names above. Physical mappings await elicitation (no retail PIDs yet — §0.1).

---

## 5. Retail base-rate application

Common §7.4 owns the base-rate register transcription; this section documents its retail application.

### 5.1 The register, retail side

| Product group | Base rate | Source | Label |
|---|---|---|---|
| Retail variable-rate products, "including consumer and small business credit cards and home equity line of credit" | **Prime Rate** (`prime_rate`) | PDF p. 181; md sec-163 | [FACT] |
| Adjustable-rate mortgage products | **mortgage rate** (`mortgage_rate`) | PDF p. 181; md sec-163 | [FACT] |
| All retail products **except mortgages** — "in projecting variable-rate **and new origination** rates" | **Prime Rate** | PDF p. 185; md sec-170 | [FACT] |
| Fixed-rate mortgage and fixed home-equity-loan **new originations** | mortgage rate **[INT — working reading]**; never stated verbatim | via the p. 185 exception | **OQ-040** |
| Auto new-origination spread benchmark | Prime Rate | PDF p. 178; md sec-158 | [FACT] (auto brief §7) |
| Other-consumer jump-off spread benchmark | Prime Rate | PDF p. 180; md sec-160 | [FACT] (other-consumer brief) |

- Scenario series: canonical names `prime_rate` and `mortgage_rate` (`IncomeScenarioPaths` carries both from Increment 1). **Physical MEV columns and scales are UNCONFIRMED** (template `TO_BE_CONFIRMED`; the PID-5 pattern applies — refuse to run until confirmed). [CODE]
- [INT — timing consequence] Every retail spread anchor is a **jump-off (PQ0) or projection-quarter value**: Equation A36 measures at t=0 and the other-consumer spread is "the difference between jump-off interest rate and Prime Rate" (PDF p. 180). **No pre-PQ0 base-rate history is required anywhere in retail** — the wholesale t−a anchor (Eq A37) has no retail counterpart. The MEV need is Prime and mortgage-rate values at PQ0 and PQ1–PQ9 only.

### 5.2 The abbreviated sentence — SQ-23

[FACT] Inside the fixed-rate spread paragraph: "The base rate applied is the same as the base rate for floating: the Prime Rate for retail and the three-month Treasury yield for wholesale." (PDF p. 182; md sec-165)

**SQ-23 (filed with this brief):** the sentence names the Prime Rate as *the* retail base rate, omitting the mortgage-rate exception that the base-rate assumptions state on the facing page (PDF p. 181) and the Retail Portfolio limitations state explicitly ("all retail products **(except for mortgages)** use Prime Rate", PDF p. 185). [INT — reconciliation, working reading] The sentence abbreviates; the mortgage exception governs, so mortgage-family spreads (ARM repricing and mortgage new originations) are measured against the mortgage rate and every other retail spread against Prime. The FRM/HEL new-origination boundary within that reading is **OQ-040** (§5.3).

### 5.3 The mortgage-exception boundary — OQ-040 (filed with this brief)

Three statements bound the question without closing it: the register assigns the mortgage rate to "adjustable-rate mortgage products" only (PDF p. 181); the limitations exempt "mortgages" from Prime "in projecting variable-rate and new origination rates" (PDF p. 185); and HELOC is explicitly Prime (PDF p. 181). Unstated: **(a)** the base rate for **fixed-rate mortgage** new originations (Eq A35/A36) — mortgage rate per the p. 185 exception [INT, working reading], never said verbatim; **(b)** whether fixed **home equity loans** count as "mortgages" for the exception — they sit inside the Mortgage section ("mortgage and home equity products", p. 177) and inside the prevalence note's "fixed-rate mortgage and home loans" (p. 183), but the register's mortgage-rate entry names ARM products only. Working reading [INT, flagged, never source-attributed]: the exception covers the Mortgage section's products, so FRM and fixed-HEL new-origination spreads are measured against the **mortgage rate**, with HELOC on Prime as stated. Owner: mortgage brief; resolution: Fed clarification, or workbook evidence at the mortgage slice (candidate PID).

---

## 6. Variable-rate application in retail

- [FACT] The Equation A33 machinery applies unchanged (common §7.3): base rate + constant launch-point spread, "Most variable rates reset quarterly" (assumption (5)).
- [FACT] Variable-rate retail populations as stated: **all card balances** ("the Board assumes that all credit card balances have variable rates", PDF p. 178; small business cards "also assumed to carry variable rates", PDF p. 179; md sec-159), **HELOC** (PDF p. 181; md sec-163), **ARM** (PDF p. 177; md sec-157). The card family's income additionally depends on the revolving balance share — family-owned machinery (card brief; OQ-012).
- [FACT of absence] No retail mixed-rate, demand-loan, or fee-only rule exists: those three rules are stated under **Corporate** only (PDF p. 176; md sec-154; their CRE reach is OQ-035). No retail subsection mentions mixed-rate loans, demand loans, or fee-only loans. Nothing is imported here.

---

## 7. Fixed-rate application in retail — the Equation A36 branch

Equations A34, A35, A36, and A38 are transcribed verbatim in the common brief §7.6; this section documents their retail application.

### 7.1 The retail spread branch

- [FACT] "The spread for fixed-rate balances is calculated differently than variable-rate balances. For retail, instead of using the average rate of all loans, only new origination loans are used." (PDF p. 182; md sec-165) — Equation A36: Spread(p,i,t=0) = weighted avg IIR for new originations(p,i,t=0) − Base rate(p,i,t=0).
- [FACT] Bias rationale (common §7.6): using only new originations "minimizes this bias but limits the number of loans used in the calculation … However, this assumes similar risk profiles for loans originating at the jump-off and in the previous quarter." (PDF p. 183; md sec-165)
- [INT — contrast with wholesale, load-bearing for implementation] The retail branch is **spot-only**: both terms of Equation A36 are t=0 quantities, so no historical base-rate series is needed (contrast Eq A37's t−a anchor; §5.1). What retail needs instead is a **new-origination rate observation** at the jump-off quarter per fixed segment — how each family's data supports that observation is family-owned (the auto case is OQ-042; mortgage and non-core at their slices).
- [FACT] **Question A155** treats the retail approach as the reference design: it asks whether wholesale "should … use the same approach as retail (i.e., only using new originations)" (PDF p. 187; md sec-172) — wholesale-owned (wholesale §6), recorded here as the Fed's own characterization of the retail branch.

### 7.2 Fixed-rate retail populations

[FACT] "Fixed-rate retail products include fixed-rate mortgage and home loans, auto loans, and most non-core loans." (PDF p. 183; md sec-165 — the retail half of common §3 row 30.) [INT] "home loans" reads as the home-equity loans of the Mortgage section's census (p. 177); the naming looseness feeds OQ-040(b).

### 7.3 The non-core split — OQ-041 (filed with this brief)

Three statements sit in tension for the other-consumer family: **(a)** "no segmentation is applied to these credit products", with one jump-off spread against Prime, held constant (PDF p. 180; md sec-160); **(b)** "the Board uses expert judgment to split it into variable rate and fixed-rate products" (PDF p. 181; md sec-164); **(c)** "most non-core loans" are fixed-rate (PDF p. 183; md sec-165). Unstated: whether the expert-judgment split operates **above** the no-segmentation statement (e.g., each aggregate product type assigned wholly to one engine) or contradicts it, and therefore which engine(s) — A33, or A34/A35/A38, or both — run the non-core products. Owner: other-consumer brief (with OQ-011's jump-off mapping); recorded at framework level because it is the one family whose **engine assignment** is open (§4.1 table).

### 7.4 The re-origination weight, retail leg

- [FACT] wt "is derived from the default rate, prepayment rate, and maturity rate" from the credit-loss models (PDF pp. 174, 183; md sec-151, sec-165) — **OQ-001 remains OPEN for every retail family** (resolved for Corporate only, via maturity-date PID-LOAN-6; CRE also open). No retail subsection states a wt source, and retail's fixed products (mortgage above all) are **prepayment-dominated**, so the Corporate maturity-only analogue may not transplant. Elicitation of the workbook's retail wt construction is the largest single open item per fixed-bearing family (approved-plan Required item; candidate PIDs at the family slices).

---

## 8. Floors in retail

- [FACT] The common rule applies: "All portfolios have a portfolio-specific interest rate floor that will bind if the projected interest rate decreases to the stated floor." (PDF p. 180; md sec-161; common §7.1)
- [FACT of absence] No retail subsection mentions floors, floor values, or a floor data source; Question A153's floor-segmentation discussion names **corporate and CRE only** (PDF p. 187; md sec-172). **OQ-002 remains OPEN for retail** (resolved for Corporate via PID-LOAN-7 and CRE via PID-LOAN-18/25; the physical retail floor source is an elicitation item).

---

## 9. Fact-of-absence register (retail framework level)

Each row is a [FACT] of absence for the retail portion of v.a(1), on the 2026-08-12 page-image passes (pp. 177–180, 185) and the 2026-07-30 full pass.

| # | Absent for retail | Contrast / nearest statement |
|---|---|---|
| 1 | **No retail-wide asset-classification statement** — HFI/FVO-HFS is mortgage-only; auto reclasses HFS→HFI; card and other-consumer are silent | Wholesale states it per part (PDF p. 175) |
| 2 | **No retail mixed-rate / demand-loan / fee-only rule** | Corporate-stated only (PDF p. 176; OQ-035 covers the CRE reach — retail is not in that question) |
| 3 | **No retail floor statement** (values, source, or segmentation) | Common rule p. 180; Question A153 names wholesale only |
| 4 | **No retail wt statement** beyond the common credit-loss derivation | PDF pp. 174, 183; OQ-001 retail leg |
| 5 | **No Board question names mortgage, auto, or other-consumer**; the single retail-directed question is A156 (revolver classification, card-owned) | PDF pp. 186–188; md sec-172 |
| 6 | **No retail revolver-draw statement** — the no-draw-growth limitation sits inside the Wholesale Portfolio subsection, while revolving products (cards, HELOC) are retail | PDF p. 186; md sec-171; wholesale §12 item 6 placement note ("possible loan-wide scope left to the integration review") |
| 7 | **No retail-specific assumptions subsection** — the (c) block is Assumptions / Limitations / Retail Portfolio / Wholesale Portfolio; retail's subsection carries limitations only | PDF pp. 184–186; md sec-167–171 |
| 8 | **No equation is printed anywhere in the retail subsections** — all machinery arrives by the common equations; the card income arrangement (rate × revolving share × balance) is implied, never written | PDF pp. 177–180; card brief will record the [INT] |

---

## 10. Industry scalar — Table A8 retail rows

- [FACT] Table A8 (PDF p. 220; md sec-209; values image-verified 2026-07-16/2026-08-03): the retail-relevant rows are **Auto 0.865**, **Credit Card 0.969**, **Mortgage 1.014**, **Noncore 1.072**; the merged **"C&I, noncore SME loan and card" 1.033** row spans the naming worlds (its "noncore SME loan and card" half is retail vocabulary — Corporate brief §10).
- [FACT] Footnote 63's eight categories include, on the retail side: "mortgage, auto, … small and median business loans and card, … consumer credit card, one category for rest of consumer loans" (PDF p. 184 footer; md 5354).
- **OQ-010 retail legs (open):** the Board states no category-to-row correspondence anywhere (SQ-11). Beyond the four natural pairings (mortgage→"Mortgage", auto→"Auto", consumer card→"Credit Card", other-consumer→"Noncore" — each an inference, not a statement), two questions have teeth: **(a)** which row multiplies **small business cards** — "Credit Card" 0.969 or the merged "C&I, noncore SME loan and card" 1.033 (footnote 63 places "small and median business loans and card" with C&I, not with consumer credit card); **(b)** whether "Noncore" and footnote 63's "rest of consumer" are the same category. Family-level assignments are candidate PIDs at the family slices, following PID-LOAN-11/21.
- [CODE] The scalar map stays configuration with an unmapped-family hard error (Corporate brief §10 [CODE] unchanged).

---

## 11. Board questions touching retail

Verbatim census in common §13; pointers only here.

- **A156** — the single retail-directed question: revolver-classification alternatives ("an account could be classified as revolver if the account has finance charges observed on FR Y-14M reports") — **card-owned** (card brief; the classification itself is PDF p. 179; md sec-159).
- **A154** — segmentation comment request covering "both wholesale and retail portfolios" (the §4 structure).
- **A155** — wholesale-directed, but characterizes the retail new-originations approach as the alternative design (§7.1).
- **A157**, **A158**, **A159**, **A160** — inherited (scalar granularity; spread factors; hedges; general); common brief §13.

[FACT absence] No Board question asks about the retail base-rate assignments, the non-core treatment, or the mortgage exception — the Fed does not itself flag them as open (§9 row 5).

---

## 12. Fed-stated Retail Portfolio limitations — [FACT] (PDF p. 185; md sec-170; page image at high zoom 2026-08-12)

Quoted in full; this brief owns the subsection (common §3 row 34), with family pointers.

1. **Base-rate simplification (framework — §5):** "The model assumes that all retail products (except for mortgages) use Prime Rate as base rate and constant spread by product, segment, and firm in projecting variable-rate and new origination rates. This assumption is to simplify the model structure and minimize firm and product variances."
2. **Data-availability limits (family pointers):** "Interest income projections for some retail products are limited by data availability and require assumptions on interest rate for each portfolio. There is no interest rate information for most non-core retails products including student loans, consumer finance products, international related loan products, and non-purpose loans. Auto loans are reported at the segment level with limited interest information. It also limits the accuracy of auto-loan interest income estimation." — the non-core sentences point at the other-consumer brief (OQ-011/OQ-041); the auto sentences at `ii_loans_auto.source-brief.md` §12.

**SQ-24 (filed with this brief):** "most non-core **retails** products" — the plural "retails" is in the published PDF itself (page image 2026-08-12), not a conversion artifact; read "retail products"; recorded verbatim, never corrected.

[FACT] Note the second paragraph's "non-purpose loans" — the other-consumer census on p. 180 writes "non-purpose lending"; same category, minor naming variance, no quirk filed (cf. the wholesale NPML naming, which is a different, wholesale-owned concept: non-purpose **margin** loans on Schedule H.1, PDF p. 176 — any relationship between retail "non-purpose lending" and wholesale NPML is **unstated**; nothing is inferred, and the other-consumer brief owns the question if elicitation surfaces one).

---

## 13. Coding considerations — [CODE], non-normative

Nothing here is Fed methodology. No production Python in this phase; family engines are follow-on gated tasks.

- **Family registry as configuration.** The four families, their coding names, grids, engine assignments (§4.1), and scalar rows belong in a data table feeding the existing category-agnostic A33/A38 machinery; the other-consumer engine assignment stays config-visible until OQ-041 resolves.
- **Per-family ingestion contracts.** The data grain varies by family (loan-level / segment-level / no-rate) — expect one declared input contract per family rather than a single retail loader; grain and column semantics are elicitation items (no retail PIDs yet).
- **Base-rate map as configuration with the OQ-040 boundary explicit.** Product-group → {`prime_rate`, `mortgage_rate`} as config; the FRM/fixed-HEL assignment carries the OQ-040 flag until a PID lands; MEV columns TO_BE_CONFIRMED refuse to run (D-006/PID-5 discipline).
- **A36 spread as data preparation or supplied input.** Mirror the wholesale A37 treatment: either supply {new-origination weighted IIR at PQ0, base rate at PQ0} or the derived spread itself; the per-family choice is an elicitation outcome.
- **Revolver share as a declared input** (card slice): the share × balance × rate arrangement is implied, not printed — the contract must name its own [INT] basis; OQ-012 constancy assumption config-visible.
- **wt contract, retail side:** per-family declared input path (or constituent rates); the Corporate maturity-only precedent must not be silently transplanted (§7.4).
- **Engines are per part** (the PID-LOAN-23 lesson): retail constructions are never assumed equal to the Corporate or CRE reference engines; the engine selector already permits per-part constructions.

---

## 14. Open questions

| ID | Status | Relevance to this brief |
|---|---|---|
| **OQ-040** | OPEN — **filed 2026-08-12 with this brief** | Mortgage-family base-rate boundary: FRM new-origination base rate never stated verbatim; fixed-HEL classification under the p. 185 "except for mortgages" exception (§5.3) |
| **OQ-041** | OPEN — **filed 2026-08-12 with this brief** | Other-consumer engine assignment: "no segmentation" vs the expert-judgment fixed/variable split vs the fixed-rate prevalence note (§7.3) |
| **OQ-042** | OPEN — filed with `ii_loans_auto.source-brief.md` | Auto new-origination spread measurement (A36 vs the trend-analysis sentence, on segment-level data) |
| **OQ-001** | OPEN for retail (Corporate resolved; CRE open) | wt inputs per retail family; prepayment-dominated fixed products (§7.4) |
| **OQ-002** | OPEN for retail | Floor values/source; no retail floor statement (§8) |
| **OQ-010** | OPEN for retail | Scalar row assignments; SME-card row; "Noncore" vs "rest of consumer" (§10) |
| **OQ-011** | OPEN | Other-consumer jump-off mapping (G.2 "most closely aligned business line") — other-consumer brief |
| **OQ-012** | OPEN (minor) | Revolver-share constancy — card brief |
| **OQ-033** | OPEN — evidence appended 2026-08-12 | Retail text repeats "by segment and by firm" and "by product, segment, and firm" — supports the firm-level working reading (§4.2) |
| **OQ-035** | OPEN — wholesale-owned | Cited only as a boundary: the mixed/demand/fee rules are not retail-relevant (§6, §9 row 2) |

---

## 15. Source traceability table

| # | Claim / element | Class | PDF p. | md anchor | Verification |
|---|---|---|---|---|---|
| 1 | Four-section retail census, verbatim | FACT | 177 | sec-156 | Page image 2026-08-12 |
| 2 | Segmentation drivers (rate structure, product type, credit risk) | FACT | 177 | sec-156 | Page image 2026-08-12 |
| 3 | Data basis: Y-14M + Y-14Q, loan-level and segment-level attributes | FACT | 177 | sec-156 | Page image 2026-08-12 |
| 4 | Non-core: data limitations prevent further segmentation | FACT | 177 | sec-156 | Page image 2026-08-12 |
| 5 | Mortgage subsection (grid; rejected splits; Y-14M rates) — deferral pointer | FACT | 177–178 | sec-157 | Page images 2026-08-12 |
| 6 | Auto subsection — deferral pointer to this slice's auto brief | FACT | 178 | sec-158 | Page image 2026-08-12 |
| 7 | Card subsection incl. revolver classification and SME cards — deferral pointer | FACT | 178–179 | sec-159 | Page images 2026-08-12 |
| 8 | Other-consumer subsection (census; no segmentation; G.2 jump-off; Prime spread) — deferral pointer | FACT | 179–180 | sec-160 | Page images 2026-08-12 |
| 9 | Retail base-rate entries (Prime incl. cards and HELOC; mortgage rate for ARM) | FACT | 181 | sec-163 | Page image 2026-07-30; common §7.4 |
| 10 | Expert-judgment non-core split sentence | FACT | 181 | sec-164 | Page image 2026-07-30; OQ-041 |
| 11 | Eq A36 retail branch ("only new origination loans are used") | FACT | 182 | sec-165 | Page image 2026-07-30; transcription in common §7.6 |
| 12 | "the Prime Rate for retail" abbreviated sentence | FACT (**SQ-23**) | 182 | sec-165 | Page image 2026-07-30; §5.2 |
| 13 | Retail fixed-rate prevalence note ("mortgage and home loans, auto loans, most non-core") | FACT | 183 | sec-165 | Page image 2026-07-30 |
| 14 | Retail Portfolio limitations, both paragraphs verbatim | FACT | 185 | sec-170 | **Page image at high zoom 2026-08-12**; SQ-24 |
| 15 | "non-core retails products" plural | FACT (**SQ-24**) | 185 | sec-170 | Page image 2026-08-12 — present in the PDF |
| 16 | Question A156 (card-owned); no other retail-named question | FACT + FACT absence | 186–188 | sec-172 | Page images 2026-07-30 |
| 17 | Table A8 retail rows and values; footnote 63 retail categories | FACT | 184, 220 | md 5354, sec-209 | Page images 2026-07-16 / 2026-08-03; OQ-010 |
| 18 | Suite-level schedule list omits Schedule A (auto's named schedule) | FACT contrast | 172 vs 178 | sec-149 vs sec-158 | Page image 2026-08-12 (p. 178); integrity §9 |
| 19 | International consumer products sit in Other Consumer | FACT | 180 | sec-160 | Page image 2026-08-12 |
| 20 | No retail PIDs exist; elicitation list = approved plan 2026-08-12 | project record | — | — | §0.1 |

---

### Brief completion checklist

- [x] Status banner present; no adoption language anywhere.
- [x] Every material statement labeled [FACT]/[PID]/[INT]/[CODE]/[OQ]/[ALT]; unknowns stated UNKNOWN, never defaulted (PID register empty — no retail PIDs exist).
- [x] **Zero verbatim equation blocks** — equations cited from the common brief per D-010(b).
- [x] Retail-boundary register (§3) accounts for every retail-owned row of the common brief's §3 register; nothing family-specific elaborated here.
- [x] pp. 177–180 and p. 185 verified as page images 2026-08-12; quirks SQ-23/SQ-24 filed verbatim, never corrected.
- [x] Wholesale appears only as explicit source-drawn boundaries; the mixed/demand/fee rules are recorded as not-retail, not imported.
- [x] Launch-point vs. projection-quarter timing explicit (§5.1 [INT] spot-only consequence); constancy per common §6.2 unchanged.
- [x] No production Python; no confidential workbook content (elicitation items named logically only).
- [ ] Review state: DRAFT — awaiting user review gate (bundled with `ii_loans_auto.source-brief.md`).

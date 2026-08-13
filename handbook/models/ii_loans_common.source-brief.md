# Source Brief — Interest Income on Loans: Loan Common Framework (`ii_loans` — common)

> **STATUS: Proposed for the 2026 stress test — public-comment stage, NOT adopted.**
> Component: **Interest Income on Loans**, Section v.a(1) (PDF pp. 173–188; md sec-150–172). Model type per Table A6: **Structural** (PDF pp. 168–169; md sec-148).
> Deliverable: loans workstream (asset-side Increment 3), slice 1 per the approved plan of 2026-07-30 — **common-framework brief**, first of the sibling set {common, wholesale, corporate, CRE}. Review state: **APPROVED 2026-08-03** *(recorded in `inventory/model-inventory.md` at approval; banner updated 2026-08-12 from "DRAFT — awaiting user review", per the user's 2026-08-12 confirmation — amendment recorded, not silent)*. This brief is not the handbook chapter; the eventual chapter remains **one chapter with six portfolio sections (decision D-003)**.
> Scope rule: this brief carries only methodology that is **actually common** across the loan portfolios — a rule is not common merely because it appears in the loan section (§3 register). Wholesale-shared rules live in `ii_loans_wholesale.source-brief.md`; Corporate/CRE/Retail-specific rules are identified, cited, and deferred.
> Integrity flags in v.a(1): SQ-5, SQ-6, SQ-7, SQ-11 (source quirks); CA-2b (md-only stray pipe); new this session: SQ-18, SQ-19, SQ-20 (filed 2026-07-30). Related OQs: OQ-001, OQ-002, OQ-003, OQ-010, OQ-011, OQ-012, OQ-014, OQ-015, OQ-033, OQ-034, OQ-035.
> Verification: **PDF pp. 173–188 read as page images 2026-07-30** (full fresh pass; §9 of `inventory/source-integrity-review.md` updated); equations A32–A38 and Table A8 previously verified 2026-07-16. Citation format: (PDF p. N; md sec-M).

---

## 0. Classification legend and project-context register

Every material statement carries exactly one of six labels (per the ie_dom_time_dep brief convention, user-confirmed 2026-07-30 for this workstream):

| Tag | Class | Meaning |
|---|---|---|
| **[FACT]** | FED SOURCE METHODOLOGY | Directly stated in the Fed PPNR source document; always cited |
| **[PID]** | PROJECT IMPLEMENTATION DECISION — USER CONFIRMED | Confirmed by the user; never attributable to the Federal Reserve unless the source independently states the same thing |
| **[INT]** | INTERPRETATION | A reading the source does not state verbatim; the basis is stated |
| **[CODE]** | CODING CONSIDERATION | Generic implementation guidance for the future Python phase; non-normative |
| **[OQ]** | OPEN QUESTION | Linked to `handbook/open-questions.md` by ID |
| **[ALT]** | ALTERNATIVE DISCUSSED BUT NOT PROPOSED | Discussed by the Fed in the source but explicitly not part of the proposed model |

### 0.1 Project implementation decision register

**No PID affects this brief.** One loans PID exists — **PID-LOAN-1** (2026-08-03), a Corporate-scoped modeling treatment registered in `handbook/models/ii_loans_corporate.source-brief.md` §0.1 and the `handbook/open-questions.md` PID registry; it does not change any common-framework rule. **No physical line-item, sheet, or scenario-column mapping has been user-confirmed for loans**; every input's physical sourcing below is either source-stated [FACT] or UNKNOWN. The register will be populated at the coding/mapping stage following the pattern of the deposit and securities families (D-004/D-005/D-006 project-wide decisions apply as cited). *(Amended 2026-08-03 — the original text read "No PIDs exist for the loans component yet," which PID-LOAN-1 superseded; amendment recorded rather than made silently.)*

**No new model is proposed anywhere in this brief.** The model documented is the Federal Reserve's proposed structural model under Equations A32–A38, unchanged.

---

## 1. Executive summary

**What the model projects.** [FACT] Nine quarters of interest income on loans, per firm `b`, product `p`, segment `i`, and projection quarter `t`: `Loan interest income(b,p,i,t) = Loan balance(b,p,i,t) × Interest income rate(b,p,i,t)` (Equation A32, PDF p. 173; md sec-151). Balances are held constant; all scenario sensitivity enters through the projected interest income rate.

**How the rate is projected.** [FACT] The model "does not estimate any components but simply calculates interest rates from the scenario, loan information, and estimated loss rates from the Retail and Wholesale models" (PDF p. 174; md sec-151). Each portfolio is segmented primarily by rate type. Variable-rate segments reprice with a scenario base rate plus a constant launch-point spread (Equation A33). Fixed-rate segments keep their existing rates (Equation A34) except for the fraction wt re-originated each quarter at a new-origination rate (Equation A35), producing a blended path (Equation A38); the new-origination spread is measured from new originations for retail (Equation A36) and from all loans at the jump-off quarter against the base rate at the median origination date for wholesale (Equation A37) (PDF pp. 180–183; md sec-161–165).

**Floors and true-up.** [FACT] "All portfolios have a portfolio-specific interest rate floor that will bind if the projected interest rate decreases to the stated floor" (PDF p. 180; md sec-161; values and data source unstated — OQ-002). Calculated income is trued up to reported FR Y-14Q Schedule G.2 interest income with a constant multiplicative industry scalar per loan category (Table A8, PDF pp. 183–184, 220; md sec-166, sec-209; OQ-010).

**What the model excludes.** [FACT] Interest-rate-risk hedges "have not been directly incorporated into the calculations … primarily due to data limitations" (Question A159, PDF p. 188; md sec-172; OQ-005).

---

## 2. Component scope and portfolio hierarchy

### 2.1 Component identity

- [FACT] Exact Federal Reserve component name: **"Interest Income on Loans"** — section heading v.a(1) (PDF p. 173; md sec-150).
- [FACT] Table A6 lists "Loans" under the proposed structural models for interest income (PDF pp. 168–169; md sec-148).
- [FACT] "interest income on loans" is first in the v.a list of 10 proposed structural components, based on "granular data reported in FR Y-14Q, Schedule G; FR Y-14Q, Schedule B; FR Y-14Q, Schedule M; and FR Y-14M" (PDF p. 172; md sec-149).
- Coding-friendly identifier (per `inventory/model-inventory.md` record #1): **`ii_loans`**.

### 2.2 Portfolio hierarchy ([FACT] structure; detail owned by sibling briefs)

| Level 1 | Level 2 (portfolio family) | Source | Detail owner |
|---|---|---|---|
| Wholesale | Corporate — 11 disclosure portfolios | (PDF pp. 175–176; md sec-153–154) | `ii_loans_wholesale` §2; corporate brief (deferred) |
| Wholesale | Commercial Real Estate (CRE) — 6 loan types, 24 segments | (PDF pp. 176–177; md sec-155) | `ii_loans_wholesale` §2; CRE brief (deferred) |
| Retail | Mortgage (incl. first lien, home equity loans, HELOC) | (PDF p. 177; md sec-156–157) | RETAIL — deferred |
| Retail | Auto loan | (PDF pp. 177–178; md sec-156, sec-158) | RETAIL — deferred |
| Retail | Consumer credit card (+ small business cards modeled separately, similar structure) | (PDF pp. 177–179; md sec-156, sec-159) | RETAIL — deferred |
| Retail | Other non-core credit products | (PDF pp. 177, 179–180; md sec-156, sec-160) | RETAIL — deferred |

- [FACT] "Wholesale interest income projections are organized into two parts: Corporate and Commercial Real Estate (CRE)" (PDF p. 175; md sec-153). "Retail interest income projections are organized into four sections" (PDF p. 177; md sec-156).
- [INT] Dimension reading: in the Equation A32 subscripts, `p` (product) corresponds to a portfolio in the above hierarchy and `i` (segment) to a cell within it (rate type × asset classification etc.); the source defines the letters only as "product" and "segment" (PDF pp. 173–174; md sec-151) — the correspondence to the named portfolios is not stated verbatim.
- [FACT] The reconciliation target of the true-up is the interest income "reported in the FR Y-14Q, Schedule G2" (PDF p. 184; md sec-166; the source also writes "FR Y-14Q, G.2 schedule", PDF p. 185; md sec-169 — same schedule, two spellings, recorded as-is).

---

## 3. Common-boundary register

Placement rule (this workstream's discipline): a rule is COMMON only if the source states it for the whole loan model or for both retail and wholesale; otherwise it is assigned to the narrowest scope the source states. Every subsection of v.a(1) is accounted for below. "Owner" = where the rule is documented in full.

| # | Rule (short) | Stated at | Class | Owner |
|---|---|---|---|---|
| 1 | Eq A32 income = balance × rate, (b,p,i,t), 9 quarters | PDF pp. 173–174; md sec-151 | COMMON | this brief §7.0, §5 |
| 2 | Balance = % of outstanding by segment × portfolio balance from FR Y-14 Schedules | PDF p. 174; md sec-151 | COMMON | §6 |
| 3 | Flat balances; run-off replenished by new originations within the same quarter | PDF p. 174; md sec-151 | COMMON | §6 |
| 4 | No estimated components; rates from scenario + loan information + estimated loss rates from Retail and Wholesale models | PDF p. 174; md sec-151 | COMMON | §4, §11 |
| 5 | Segmentation purpose: new-origination characteristics; jump-off balance-weighted average rate as segment starting point | PDF pp. 174–175; md sec-152 | COMMON | §7.2 |
| 6 | Rate type (fixed vs. variable) is the primary segmentation split for each retail or wholesale portfolio | PDF p. 175; md sec-152 | COMMON | §7.2 |
| 7 | Wholesale = Corporate + CRE; HFI vs. FVO/HFS classification; data "sourced from FR." (SQ-5) | PDF p. 175; md sec-153 | WHOLESALE | wholesale §2–§3 |
| 8 | Corporate 11 portfolios; 16-of-22 rate split | PDF pp. 175–176; md sec-154 | CORPORATE (summary in wholesale §2) | corporate brief (deferred) |
| 9 | Mixed-rate and demand loans treated as variable-rate | PDF p. 176; md sec-154 | CORPORATE-stated; wholesale-wide applicability OQ-035 | wholesale §4 |
| 10 | Fee-only loans: no interest income; excluded from average rate and balance percentages | PDF p. 176; md sec-154 | CORPORATE-stated; wholesale-wide applicability OQ-035 | wholesale §4, §10 |
| 11 | NPML-based treatment of 3 portfolios without loan-level data | PDF p. 176; md sec-154 (also pp. 186; sec-171) | CORPORATE | corporate brief (deferred); wholesale §11 |
| 12 | CRE 6 loan types; 24 segments | PDF pp. 176–177; md sec-155 | CRE (summary in wholesale §2) | CRE brief (deferred) |
| 13 | Retail four sections; retail segmentation drivers | PDF p. 177; md sec-156 | RETAIL | deferred |
| 14 | Mortgage / Auto / Card / Other-consumer portfolio rules (incl. revolver classification, OQ-011/OQ-012 subjects) | PDF pp. 177–180; md sec-157–160 | RETAIL | deferred |
| 15 | Income = existing portfolio + new originations; portfolios re-originate at different runoff rates per quarter | PDF p. 180; md sec-161 | COMMON | §7.1 |
| 16 | Fixed vs. variable rate paths modeled differently | PDF p. 180; md sec-161 | COMMON | §7.1 |
| 17 | Portfolio-specific interest-rate floor binds if the projected rate falls to it | PDF p. 180; md sec-161 | COMMON (OQ-002); wholesale floor discussion → wholesale §8 | §7.1 |
| 18 | Eq A33 variable-rate projection; spread constant at t=0 | PDF pp. 180–181; md sec-162 | COMMON | §7.3 |
| 19 | Base-rate register: Prime (retail variable incl. cards, HELOC), mortgage rate (ARM), 3M Treasury (wholesale) | PDF p. 181; md sec-163 | COMMON register; wholesale entry applied in wholesale §5 | §7.4 |
| 20 | "The majority of balances in wholesale are variable-rate…" | PDF p. 181; md sec-163 | WHOLESALE | wholesale §5 |
| 21 | Spread = balance-weighted average interest rate − base rate; varies by firm, product, segment | PDF p. 181; md sec-164 | COMMON | §7.5 |
| 22 | Spread granularity per data availability; alternative sources; expert judgment splits the non-core portfolio | PDF p. 181; md sec-164 | COMMON statement; non-core detail RETAIL | §7.5 |
| 23 | Variable-rate facilities that default/mature/run off replaced with the same loan type | PDF pp. 181–182; md sec-164 | COMMON | §7.5 |
| 24 | Fixed-rate: balance-weighted origination rate by firm/product/segment at jump-off; unchanged except termination (Eq A34) | PDF p. 182; md sec-165 | COMMON | §7.6 |
| 25 | Eq A35 new-origination rate | PDF p. 182; md sec-165 | COMMON | §7.6 |
| 26 | Eq A36 fixed-rate spread from new originations (retail branch) | PDF p. 182; md sec-165 | COMMON machinery; retail application RETAIL | §7.6 |
| 27 | Eq A37 wholesale fixed-rate spread (all loans at jump-off; base rate at median origination date t−a) | PDF p. 182; md sec-165 | COMMON transcription; WHOLESALE application (OQ-003) | §7.6; wholesale §6 |
| 28 | Bias rationale for the two spread approaches | PDF p. 183; md sec-165 | COMMON (contrast retail/wholesale) | §7.6; wholesale §6 |
| 29 | Eq A38 blended fixed rate; wt from default, prepayment, maturity rates | PDF p. 183; md sec-165 | COMMON (OQ-001) | §7.6 |
| 30 | Fixed-rate prevalence notes (retail: mortgage/home/auto/most non-core; wholesale: CRE income-producing) | PDF p. 183; md sec-165 | Split: retail note RETAIL; wholesale note → wholesale §7 | §7.6 (record) |
| 31 | Industry scalar mechanism; Table A8; footnote 63 | PDF pp. 183–184, 220; md sec-166, sec-209 | COMMON (OQ-010, OQ-014) | §8 |
| 32 | Assumptions (1)–(7) | PDF p. 184; md sec-167–168 | COMMON | §12 |
| 33 | General limitations (jump-off comparability; scalar mitigation) | PDF p. 185; md sec-169 | COMMON | §12 |
| 34 | Retail Portfolio limitations subsection | PDF p. 185; md sec-170 | RETAIL | deferred (existence noted §12.3) |
| 35 | Wholesale Portfolio limitations subsection (incl. constant roll-off, NPML proxy, revolver-draw paragraphs) | PDF pp. 185–186; md sec-171 | WHOLESALE | wholesale §12 |
| 36 | Questions A151–A160 | PDF pp. 186–188; md sec-172 | COMMON census with per-question tags | §13 |
| 37 | Footnote 61 (facility-level data), footnote 62 ("floating" terminology) | PDF p. 175 footers; md 5350, 5352 | WHOLESALE | wholesale §3–§4 |
| 38 | Footnote 63 (8 scalar categories) | PDF p. 184 footer; md 5354 | COMMON | §8 |

---

## 4. Model classification

- **Classification: structural model (granular bottom-up calculator).** [FACT] Table A6 assigns "Structural" (PDF pp. 168–169; md sec-148); "the proposed loan interest income model is developed using a granular, bottom-up approach with data from the FR Y-14M and FR Y-14Q regulatory reports" (PDF p. 173; md sec-151).
- **Stated benefits.** [FACT] The bottom-up approach "is closer to the business-as-usual calculations performed by institutions for accounting and forecasting purposes," "would more accurately reflect the income impact of loan characteristics within a scenario," enables "easier interpretation of results," and "results in a model with the appropriate sensitivity to projected scenarios" (PDF p. 173; md sec-151).
- **Parameter character.** [FACT] "The proposed loan interest income model does not estimate any components but simply calculates interest rates from the scenario, loan information, and estimated loss rates from the Retail and Wholesale models. The interest rate reset indices provide a direct link between the scenario and the projected interest rates." (PDF p. 174; md sec-151). The only published parameter table is the Table A8 scalar set (§8, §10).
- **Replaces.** [FACT] "interest income on loans is currently modeled using a panel regression model with an autoregressive term. The Board proposes an alternative set of models" (PDF p. 173; md sec-151). The current 2025 model is out of this brief's scope (COMPARISON policy).

---

## 5. Dimensions and time conventions

### 5.1 Dimension register

| Dimension | Applies? | Basis | Label |
|---|---|---|---|
| Firm `b` | Yes | Eq A32 where-list: "b = firm" (PDF pp. 173–174; md sec-151) | [FACT] |
| Product `p` | Yes | "p = product" (PDF p. 174) | [FACT]; [INT] p ≈ portfolio (§2.2) |
| Segment `i` | Yes | "i = segment" (PDF p. 174) | [FACT] |
| Projection quarter `t` = 1…9 | Yes | "projects 9 quarters of interest income" (PDF p. 173; md sec-151); "t = projection quarter" (PDF p. 174) | [FACT] |
| Scenario / exercise | Yes | Scenario base rates drive the rate paths (PDF pp. 180–181); the section carries no explicit scenario index | [INT] |

- Conversion note: the md renders the where-list's final bullet as "*t = projection quarter*\|" — the stray pipe is **md-only** (CA-2b; PDF p. 174 clean, confirmed on the page image 2026-07-30). Quotes here use the corrected reading per integrity-review §7 policy.
- Source-quirk note (**SQ-18**, filed 2026-07-30): the printed subscripts of Equations A34, A35, A36, and A38 **omit the firm dimension `b`** (and A38's weight is `wt(p,i,t)`), while Equations A33 and A37 include `b` and the fixed-rate prose says "balance-weighted origination rate **by firm, product, and segment** at jump-off" (PDF p. 182; md sec-165). Whether the fixed-rate machinery (especially the A36 retail spread and wt) operates per firm or pooled across firms is **OQ-033**; [INT, working reading] the omission is notational abbreviation and the machinery is firm-level, per the prose and the A33/A37 pattern.

### 5.2 Time conventions

- **Launch point (PQ0).** [FACT] The source's terms in v.a(1) are "jump-off" (rates, quarter, spread — PDF pp. 174, 180–184) — the handbook standardizes on **launch point, PQ0** (decision D-005); source words are preserved in quotes and equation transcriptions. `t=0` in Equations A33–A38 denotes the jump-off quarter [INT — consistent with "at the jump-off quarter" (PDF p. 182) and the framework's `q0` usage].
- **Projection horizon.** [FACT] Nine quarters (PDF p. 173; md sec-151; general horizon PDF p. 6; md sec-2).
- **Historical reference values.** [FACT] Equation A37 uses "the base rate from the median origination date (*t* - *a*) for that portfolio" (PDF p. 182; md sec-165) — a **pre-PQ0 historical** base-rate value (OQ-003: how `a` is measured). No other historical window exists in the model (fact of absence).
- **Contemporaneous vs. lagged.** [FACT] BaseRate(p,i,t) is contemporaneous in A33/A35; A38 uses the prior-quarter blended rate IR(existing,(p,i,t−1)); spreads are fixed at t=0.

### 5.3 Timing register

| Quantity | Quarter taken from | Label |
|---|---|---|
| % of outstanding balance by segment; portfolio balances | Launch point (jump-off), held flat | [FACT] flat (PDF p. 174); as-of wording not restated per input ([INT] launch point, consistent with the segmentation section) |
| Jump-off balance-weighted average interest rate per segment | PQ0 ("average jump-off interest rate weighted by outstanding balance", PDF p. 174; md sec-152) | [FACT] |
| Variable-rate spread Spread(b,p,i,t=0) | PQ0; constant thereafter | [FACT] (PDF p. 181; md sec-162) |
| Fixed-rate spread (A36/A37 branches) | PQ0 measurement; A37's base rate taken at t−a | [FACT]; OQ-003 |
| BaseRate(p,i,t) | Contemporaneous projection quarter | [FACT] |
| wt(p,i,t) | Per projection quarter (subscripted t) | [FACT] subscript; underlying rates' time-variation UNKNOWN (OQ-001; cf. wholesale "constant roll-off rate", wholesale §9) |
| Industry scalar | Computed at jump-off; multiplies every projection quarter | [FACT] (PDF p. 184; md sec-166) |
| Floors | Bind conditionally in any quarter | [FACT] rule; values/source UNKNOWN (OQ-002) |

---

## 6. Balance construction and constancy register

### 6.1 Balance construction

- [FACT] "Loan balance(b,p,i,t) is calculated by taking the percentage of outstanding balance for segment i by firm b and product p and then multiplying it by the portfolio balance from FR Y-14 Schedules." (PDF p. 174; md sec-151)
- [FACT] "Loan balances are held constant throughout the 9 projection quarters for all loan portfolios, consistent with the constant balance assumption for the stress test exercise. Any reduction in exposure arising from default, prepayment, or amortization will be replenished by newly originated loans within the same projection quarter, such that the portfolio balance remains unchanged. Adding newly originated loans in this manner is similar to loan re-origination done for the credit loss projections across the loan portfolio." (PDF p. 174; md sec-151)
- [FACT] Fee-only loans' "outstanding balance percentages are excluded from the total balances calculation" — stated under Corporate (PDF p. 176; md sec-154; OQ-035 for scope; owner: wholesale §4).

### 6.2 Constancy register

| Quantity | Constant or varying | Source statement | Label |
|---|---|---|---|
| Loan balances (b,p,i) | **Constant** all 9 quarters | PDF p. 174 (quoted above) | [FACT] |
| Segment composition (% of outstanding) | **Constant** | Not restated per quarter; implied by the flat-balance + same-type replenishment mechanism | [INT] |
| Variable-rate spreads | **Constant** (t=0 value) | Eq A33 where-list: "held constant over time" (PDF p. 181); assumption (4) (PDF p. 184) | [FACT] |
| Fixed-rate new-origination spreads | **Constant** (t=0 value) | Eqs A35–A37 subscripts (t=0); assumption (4) | [FACT] |
| Existing fixed rates | **Constant** except termination/re-origination | Eq A34; "assumed to remain unchanged … except if they terminate" (PDF p. 182); assumption (6) | [FACT] |
| Base rates | **Vary** with the scenario path | PDF p. 181 (sec-163) | [FACT] |
| Blended fixed-rate path | **Varies** via Eq A38 | PDF p. 183 | [FACT] |
| wt | Time-subscripted (see §5.3) | PDF p. 183 | [FACT] subscript; OQ-001 |
| Industry scalars | **Constant** ("This constant scalar…") | PDF p. 184 | [FACT] |
| Floors | Constant stated floors; binding varies | PDF p. 180 ("the stated floor") | [FACT] rule; OQ-002 values |
| Revolver share (credit card) | RETAIL-deferred | PDF p. 179; OQ-012 | deferred |

---

## 7. Rate machinery — the common equations (verbatim, transcribed once for the sibling set)

### 7.0 Equation A32 (verbatim)

[FACT] (PDF p. 173; md sec-151; page image 2026-07-30):

**Equation A32** – Interest Income on Loans Projection

$$Loan\ interest\ income_{b,p,i,t} = Loan\ balance_{b,p,i,t} * Interest\ income\ rate_{b,p,i,t}$$

*where:*

- *b = firm;*
- *p = product;*
- *i = segment;* and
- *t = projection quarter* (md appends a stray pipe here — CA-2b, md-only)

Symbol register: `loan_interest_income[b,p,i,t]`; `loan_balance[b,p,i,t]` (§6); `interest_income_rate[b,p,i,t]` (§§7.3–7.6).

### 7.1 Projected-rate framework

- [FACT] "Interest income consists of interest income from existing portfolios and from new originations during the projection periods under the flat balance assumption. Both wholesale and retail portfolios re-originate based on different runoff rate at each projection quarter. The Board proposes to model the interest rate path differently for fixed-rate and variable-rate products over the projection window. All portfolios have a portfolio-specific interest rate floor that will bind if the projected interest rate decreases to the stated floor." (PDF p. 180; md sec-161)
- [OQ-002] Where floor values come from (contract field? assumption?) is UNKNOWN. Wholesale floor granularity discussion: wholesale §8 (Question A153).

### 7.2 Segmentation principles

- [FACT] Segments "primarily … reflect new origination's interest income characteristics. For each segment, an average jump-off interest rate weighted by outstanding balance is used as the starting point for projecting the segment level interest rate." Differences in within-segment loan characteristics "such as risk profile, appear as differences in the weighted average." (PDF pp. 174–175; md sec-152)
- [FACT] "The primary determinant of the segmentation scheme is interest rate sensitivity. The key considerations to segment a portfolio's interest income is rate type: each retail or wholesale portfolio is segmented into fixed-rate and variable-rate exposures. This is a critical segmentation step to separately account for when interest rates change during the projection." (PDF p. 175; md sec-152)
- Portfolio-family segmentation grids (which further dimensions apply — asset classification, product type, credit risk) are portfolio-specific: wholesale §2; retail deferred.

### 7.3 Variable-rate products — Equation A33 (verbatim)

[FACT] "For variable-rate products, projected interest rates are determined using the base rate-related variables from the scenario file (discussed below), combined with an estimated spread. Most variable rates reset quarterly while balances of variable-rate products remain unchanged under the flat balance assumption." (PDF p. 180; md sec-162)

**Equation A33** – Variable-Rate Products Interest Rate Projection

$$IR_{(b,p,i,t)} = BaseRate_{(p,i,t)} + Spread_{(b,p,i,t=0)}$$

*where:*

- $IR_{(b,p,i,t)}$ represents interest rate for firm $b$, product $p$, and segment $i$ at time $t$;
- $BaseRate_{(p,i,t)}$ represents the scenario base rate at quarter *t for product p*; and
- $Spread_{(b,p,i,t=0)}$ represents the initial spread for firm $b$, product $p$, and segment $i$ which is held constant over time.

(PDF p. 181; md sec-162.) Source-quirk note **SQ-20** (filed 2026-07-30): the BaseRate where-list line names only "product p" while the subscript carries segment `i`; [INT] the base rate is assigned at the product/segment level per §7.4's product-group mapping — no per-firm base rate exists ([FACT] absence of `b` in the BaseRate subscript).

### 7.4 Base-rate register

[FACT] (PDF p. 181; md sec-163) "The base rate determines the magnitude of interest rate change in the scenario."

| Product group | Base rate (scenario variable) | Label |
|---|---|---|
| Retail variable-rate products, "including consumer and small business credit cards and home equity line of credit" | **Prime Rate** (`prime_rate`) | [FACT] |
| Adjustable-rate mortgage products | **mortgage rate** (`mortgage_rate`) | [FACT] |
| Wholesale | **three-month Treasury yield** (`usd_3m_treasury`) | [FACT]; applied in wholesale §5 |

- [FACT] The wholesale sentence context ("The majority of balances in wholesale are variable-rate, thus the projected base rate is most responsible for changes in the projected interest income") is wholesale-owned (wholesale §5). Board question on alternates (SOFR 1M, Prime for wholesale): Question A152, wholesale-tagged (§13).
- Retail base-rate application detail (which retail segments use which rate at what granularity): RETAIL-deferred.

### 7.5 Spread construction (variable-rate; common statements)

- [FACT] "The spread is defined as the difference between the balance-weighted average interest rate and the base rate, and it varies by firm, product, and segment. The level of granularity for spread estimation depends on the product segment and data availability. When data is limited, the Board proposes to determine spreads through other alternative data sources, especially for the non-core portfolio where the Board uses expert judgment to split it into variable rate and fixed-rate products." (PDF p. 181; md sec-164; the non-core application is RETAIL-deferred — cf. OQ-011.)
- [FACT] "Given that the stress test assumes constant balances, and the fact that the interest rate spread will not get updated during the projection horizon, the Board proposes replacing variable rate facilities that default, mature, or run-off with the same loan type. This allows the interest income equation above to calculate the interest rate at time *t*. Changes in the interest rate for variable-rate balances are completely determined by changes in the scenario variable." (PDF pp. 181–182; md sec-164)

### 7.6 Fixed-rate products — Equations A34–A38 (verbatim)

- [FACT] "For the fixed-rate products, the Board proposes to use the balance-weighted origination rate by firm, product, and segment at jump-off, and the rates are assumed to remain unchanged throughout the stress test projection horizon except if they terminate." (PDF p. 182; md sec-165)

**Equation A34** – Fixed-Rate Products Interest Rate Projection

$$IR_{(existing,t)} = IR_{(existing,t=0)}$$

- [FACT] "For new originations, origination interest rates are projected using a modification to the fixed-rate product interest rate equation:"

**Equation A35** – Origination Interest Rates Projection

$$IR_{(p,i,t,\ new\ orig)} = BaseRate_{(p,i,t)} + Spread_{(p,i,t=0)}$$

- [FACT] "The spread for fixed-rate balances is calculated differently than variable-rate balances. For retail, instead of using the average rate of all loans, only new origination loans are used." **[Retail branch]**

**Equation A36** – Spread for Fixed-Rate Projection

$$Spread_{(p,i,t=0)} = weighted\ avg\ IIR\ for\ new\ originations_{(p,i,t=0)} - Base\ rate_{(p,i,t=0)}$$

- [FACT] "For wholesale, the spread is calculated from the average rate of all loans at the jump-off quarter and the base rate from the median origination date ( *t* - *a*) for that portfolio. The base rate applied is the same as the base rate for floating: the Prime Rate for retail and the three-month Treasury yield for wholesale." **[Wholesale branch — application detail, t−a mechanics, and OQ-003 live in `ii_loans_wholesale` §6]**

**Equation A37** – Spread for Wholesale Projection

$$Spread_{(b,p,i,t=0)} = balance_{weighted}\,avg\ IIR_{(b,p,i,t=0)} - Base\ rate_{(t-a)}$$

(SQ-6: the source typesets "weighted" as a subscript of "balance"; read "balance-weighted average interest income rate".)

- [FACT] Bias rationale, restated faithfully: fixed rates "were set at some point in the past"; two same-risk loans set in different rate environments will likely differ, so "using the jump-off scenario variable will likely result in a biased calculation of the interest rate spread." Using only new originations (retail branch) "minimizes this bias but limits the number of loans used in the calculation … However, this assumes similar risk profiles for loans originating at the jump-off and in the previous quarter. Using the median origination date may better account for changing risk profiles but come at the expense of likely measurement error." (PDF p. 183; md sec-165)
- [FACT] "The projected fixed-rate interest rate is a weighted average of the existing interest rate, which is not updated, and the new origination rate calculated from the spread and base rate. Both interest rates are combined to calculate the fixed interest rate for that portfolio."

**Equation A38** – Projected Fixed-Rate Interest Rate

$$IR_{existing,(p,i,t)} = \left(1 - wt_{(p,i,t)}\right) * IR_{(existing,(p,i,t-1))} + wt_{(p,i,t)} * IR_{(new,p,i,t)}$$

(SQ-7: the left-hand side is named IR_existing although it defines the blended existing + new-origination path; the surrounding text confirms the blend intent — treat the LHS as the updated portfolio fixed rate.)

- [FACT] "The weight, $wt_{(p,i,t)}$, is the fraction of the portfolio that needs to be re-originated. This is derived from the default rate, prepayment rate, and maturity rate." (PDF p. 183; md sec-165) — the upstream rates come from the credit-loss models ([FACT] §4; granularity and delivery **OQ-001**).
- [FACT] Prevalence notes (recorded here; owners per §3 rows 30): "Fixed-rate retail products include fixed-rate mortgage and home loans, auto loans, and most non-core loans. In wholesale, fixed-rate products are more common for CRE income-producing loans. Fixed-rate products are less sensitive to changes in the base rate because only a fraction of the portfolio gets updated interest rates." (PDF p. 183; md sec-165)
- **SQ-18 / OQ-033** (§5.1): the printed subscripts of A34–A36 and A38 omit `b`; the working reading (firm-level machinery) is [INT], never presented as source-stated.

### 7.7 Compounding and rate basis

- [FACT] Assumption (3): "Interest income is quarterly compounded." (PDF p. 184; md sec-168) The rate basis (annualized vs. quarterly) and the operational meaning of "quarterly compounded" for the Equation A32 product are **not stated** — the OQ-006 source-side absence is preserved for this component.
- Project convention (D-004, project-wide, user-confirmed; never a Fed statement): all project rates are annualized; a quarterly dollar flow divides the annualized rate by four at the final step only. How D-004's simple quarterization interacts with the stated "quarterly compounded" assumption is recorded as UNRESOLVED at the interpretation level; [CODE] the final conversion must be a named, documented transform whose convention is settled at the chapter/spec stage, not a hidden literal.

---

## 8. Industry scalar and Table A8

- [FACT] Mechanism: the methodology "has several assumptions that are necessary primarily to address data limitations. The Board evaluates and adjusts for these data limitations by utilizing aggregated information from other reporting forms. Specifically, firms report interest income from each loan category in regulatory forms as well as financial statements. The Board proposes to 'true-up' the calculations to the reported values using a multiplicative scalar by industry for each loan category. For example, if the calculated interest income in the domestic CRE portfolio is 95% of the value reported in the FR Y-14Q, Schedule G2, then the Board proposes to use a scalar of 1/0.95 = 1.05 to adjust the calculated value. This constant scalar is used to multiply the calculated domestic CRE interest income in each quarter in the projection horizon and this true-up adjustment minimizes the potential impact of data limitations on the projections." (PDF pp. 183–184; md sec-166)
- [INT] Arithmetic note: 1/0.95 = 1.0526…; the printed "1.05" is the source's own rounding inside an illustration — the rule is the ratio formula, not the two-decimal value.
- [FACT] Footnote 63 (verbatim): "The Board calculates an industry-level scalar separately for mortgage, auto, corporate & investment, small and median business loans and card, domestic CRE, consumer credit card, one category for rest of consumer loans, and one for rest of wholesale exposures." (PDF p. 184 footer; md 5354) — **8 categories**.
- [FACT] **Table A8** – Scalars for Proposed Interest Income on Loans Model (PDF p. 220; md sec-209; all values verified against the page image, integrity review §5) — **7 rows**:

| Portfolio | Scalar |
|---|---|
| Auto | 0.865 |
| C&I, noncore SME loan and card | 1.033 |
| Credit Card | 0.969 |
| Domestic CRE | 1.081 |
| Mortgage | 1.014 |
| Noncore | 1.072 |
| Rest of wholesale | 1.113 |

- **SQ-11 / [OQ-010]**: 7 rows vs. footnote 63's 8 categories; "C&I, noncore SME loan and card" appears to merge two footnote categories ("median" likely intends "medium"). The exact category→row mapping, and **which portfolios each scalar multiplies**, is UNKNOWN.
- [OQ-014] Application granularity as proposed = industry-level constant per loan category, every projection quarter; Question A157 floats bank-level vs. portfolio-level alternatives (§13).
- [FACT] Limitations tie-in: "Scaling the model's jump-off interest income to the reported interest income in the FR Y-14Q, G.2 schedule using the scalar brings these two numbers closer together." (PDF p. 185; md sec-169)

---

## 9. Inputs

### 9.1 Input register — common-framework level

Physical line items are stated only where the source states them; portfolio-level input detail belongs to the sibling briefs.

| # | Input | Fed terminology | Coding-friendly name | Source | Unit | Dimensions | Timing | Constant? | Label |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Portfolio balances | "the portfolio balance from FR Y-14 Schedules" (PDF p. 174) | `loan_portfolio_balance` | FR Y-14 Schedules; item-level mapping per portfolio (sibling briefs); no single item named | USD (level) | b × p | PQ0, flat | **Constant** | [FACT] role; mapping UNKNOWN at common level |
| 2 | % of outstanding balance by segment | "the percentage of outstanding balance for segment i" (PDF p. 174) | `segment_balance_share` | Derived from FR Y-14 loan/facility/segment data per portfolio | share ∈ [0,1] | b × p × i | PQ0 | **Constant** [INT §6.2] | [FACT] role |
| 3 | Jump-off balance-weighted average interest rate | "average jump-off interest rate weighted by outstanding balance" (PDF p. 174) | `segment_rate_launchpoint` | Per-portfolio FR Y-14 data (wholesale: H.1 facility data — wholesale §3; retail: deferred) | Rate basis unstated (§7.7) | b × p × i | PQ0 | Seed value | [FACT] |
| 4 | Variable-rate spread | Eq A33 Spread(b,p,i,t=0) | `variable_spread_launchpoint` | Derived: weighted-average rate − base rate (§7.5) | Rate difference | b × p × i | PQ0 | **Constant** | [FACT] |
| 5 | Fixed-rate new-origination spread | Eq A36 / Eq A37 branch | `fixed_spread_launchpoint` | Derived per branch (retail: new originations; wholesale: all loans vs. base rate at t−a — wholesale §6) | Rate difference | (p,i) printed; b per [INT]/OQ-033 | PQ0 | **Constant** | [FACT] + OQ-033 |
| 6 | Scenario base rates | Prime Rate; mortgage rate; three-month Treasury yield (PDF p. 181) | `prime_rate`, `mortgage_rate`, `usd_3m_treasury` | Supervisory scenario (physical sourcing per PID-5 pattern at mapping stage — no loans PID yet) | Rate | scenario × t | PQ1…PQ9 | Vary | [FACT] roles |
| 7 | Re-origination weight inputs | "default rate, prepayment rate, and maturity rate" (PDF p. 183); "estimated loss rates from the Retail and Wholesale models" (PDF p. 174) | `wt_inputs` → `reorigination_weight` | **External** — Retail and Wholesale credit-loss models; granularity/format unstated | rates per quarter | (p,i,t) printed; OQ-033 | per t | OQ-001 | [FACT] dependency; **OQ-001** |
| 8 | Interest-rate floors | "portfolio-specific interest rate floor … the stated floor" (PDF p. 180) | `portfolio_rate_floor` | **UNKNOWN** — data source and values unstated | Rate | portfolio (segmentation per Question A153 open) | constant | Constant | [FACT] rule; **OQ-002** |
| 9 | Industry scalars | Table A8 (PDF p. 220) | `industry_scalar` | Supplied — Table A8 (§8) | Multiplicative factor | loan category | constant | **Constant** | [FACT]; OQ-010 mapping |
| 10 | Reported interest income by loan category | "the value reported in the FR Y-14Q, Schedule G2" (PDF p. 184) | `reported_loan_interest_income_g2` | FR Y-14Q Schedule G.2 (line-item mapping UNKNOWN) | USD | b × category | jump-off | n/a (scalar construction) | [FACT] role |

### 9.2 Inputs mandated for review that the common framework does not use

Each row is a [FACT] of absence for v.a(1).

| Input | Status | Evidence |
|---|---|---|
| **Hedge inputs (FR Y-14Q B.2/B.3)** | **NOT USED** — hedges "have not been directly incorporated into the calculations described above" | Question A159 (PDF p. 188; md sec-172); §11 |
| **Table A7 deposit betas** | **NOT APPLICABLE** — Table A7 serves the Equations A46 deposit models | PDF p. 219; md sec-209 |
| **1-year / 10-year Treasury yields** | **NOT USED** — the base-rate register is exactly Prime / mortgage rate / 3M Treasury | PDF p. 181; md sec-163 (fact of absence) |
| **Estimated regression coefficients** | **NONE EXIST** — "does not estimate any components" | PDF p. 174; md sec-151 |

---

## 10. Parameters

| Parameter | Definition | Value / source | Published or derived | Constant? | Label |
|---|---|---|---|---|---|
| Industry scalars | Multiplicative true-up per loan category | **Table A8, 7 values** (§8) | Published (PDF p. 220) | Constant [FACT] | [FACT]; OQ-010 row mapping |
| Spreads (variable; fixed-new-origination) | §7.5–7.6 | Derived from firm data at the launch point | Derived; not published | Constant [FACT] | [FACT] |
| Floors | §7.1 | **UNKNOWN** | Not published; source unstated | Constant stated floors | [FACT] rule; **OQ-002** |
| wt | §7.6 | Derived from credit-model rates | Not published | Time-subscripted | [FACT]; **OQ-001** |
| Estimated coefficients | — | **None exist for this model** | — | — | [FACT] absence (PDF p. 174) |

---

## 11. Dependencies and hedge boundary

| Dependency | Type | What depends on it | Status | Label |
|---|---|---|---|---|
| Retail and Wholesale credit-loss models | **Upstream supervisory models** | "estimated loss rates" (PDF p. 174); wt's default/prepayment/maturity rates (PDF p. 183) | The only proposed net-interest model with an upstream model dependency (inventory dependency summary); rates' granularity, definitions, and delivery **defined outside this document** | [FACT]; **OQ-001** (external dependency) |
| FR Y-14M / FR Y-14Q (G, B, M schedules) | Upstream data | Balances, segment shares, jump-off rates, revolver data (retail) | Named at suite level (PDF p. 172); portfolio-level items per sibling briefs | [FACT] |
| FR Y-14Q Schedule G.2 reported interest income | Upstream data | Scalar construction (§8) | Named (PDF p. 184) | [FACT] |
| Supervisory scenario (Prime, mortgage rate, 3M Treasury) | Scenario | Base rates (§7.4) | [FACT] roles; physical sourcing at mapping stage | [FACT] |
| Cross-cutting hedge adjustment (v.c) | Cross-cutting | Possible future hedge incorporation for loans via proposed updated Schedule B.2 (Question A159) | Loans currently **excluded**; v.c is contingent on the proposed collection | [FACT]; **OQ-005** |
| PPNR aggregation (Equation A1 identity) | Downstream | Component income rolls into net interest income / PPNR | PDF pp. 6–8; md sec-2 | [FACT] background |

**Hedge boundary.** [FACT] v.a(1) contains no hedge term anywhere in Equations A32–A38; Question A159 states hedges are not directly incorporated "primarily due to data limitations" and that the Board "is proposing additional data collection through an updated FR Y-14Q, Schedule B.2 to incorporate interest rate risk hedges for interest income on loans" (PDF p. 188; md sec-172). Division of responsibility between any future in-model incorporation and the v.c cross-cutting adjustment is **OQ-005** (both data states presented at chapter stage, per `handbook/cross-cutting/asset-side-common-conventions.md` §9).

**Blocking assessment.** OQ-001 (wt input contract) and OQ-002 (floor values) block a complete implementation of the fixed-rate blend and the floor clamp respectively; the remainder of the common framework is implementable from firm data + scenario + Table A8. This matches the Increment 3 gate list in `inventory/asset-side-model-matrix.md`.

---

## 12. Fed-stated assumptions and limitations

### 12.1 Assumptions — [FACT] (PDF p. 184; md sec-167–168, verbatim)

Intro: "This proposed model is comprehensive and covers all the retail and wholesale products covered in the stress test. Consistent with the principle of simplicity in the Policy Statement, the model incorporates the following assumptions and acknowledges certain limitations:"

1. "The model assumes a flat balance over the projection horizon, meaning that portfolio balances are held constant over time. The projected balance is the sum of remaining balances of the existing portfolio and the new originations which are due to prepay, maturity, and defaults."
2. "The model assumes that delinquent loans generate interest income. The impact of this assumption is tested and immaterial."
3. "Interest income is quarterly compounded."
4. "Interest spreads are assumed to be constant over projection quarters."
5. "Most variable rates are repriced quarterly, aligning with changes in the projected base rate."
6. "Balance-weighted segment-level fixed interest rates are assumed to remain unchanged throughout the projection window, except for new originations."
7. "To reduce complexity, the model groups various products with similar rate structures and applies consistent base rate and spread assumptions across products."

### 12.2 General limitations — [FACT] (PDF p. 185; md sec-169)

"Data availability imposes limitations on model accuracy and requires several assumptions for the interest income calculation. Differences in reporting instructions make comparisons between the model's jump-off interest income calculations and reported FR Y-9C and FR Y-14Q, G.2 schedule interest income difficult. Scaling the model's jump-off interest income to the reported interest income in the FR Y-14Q, G.2 schedule using the scalar brings these two numbers closer together."

### 12.3 Portfolio-scoped limitation subsections (owned elsewhere)

- [FACT] A "Retail Portfolio" limitations subsection exists (PDF p. 185; md sec-170) — **RETAIL-deferred**; not elaborated here per the workstream scope.
- [FACT] A "Wholesale Portfolio" limitations subsection exists (PDF pp. 185–186; md sec-171) — owned by `ii_loans_wholesale` §12.

---

## 13. Board-question census — A151–A160 ([FACT], verbatim; PDF pp. 186–188; md sec-172)

Intro: "The Board is requesting public input on this proposed model for interest income on loans, including, but not limited to, input on the following questions:"

| # | Question (verbatim) | Scope tag |
|---|---|---|
| A151 | "The Board seeks comment on the proposed approach to model interest income on loans, as compared to the Board's current panel regression model." | COMMON |
| A152 | "Should the SOFR one-month maturity and the Prime Rate be used as the base rate for wholesale instead of the three-month Treasury Yield? Is there a scenario variable that would more accurately project changes in variable-rate interest rates? What would be the advantages and disadvantages of using these rates?" | WHOLESALE (wholesale §5) |
| A153 | "Should corporate and CRE variable-rate balances be further segmented to vary the interest rate floor? The interest rate floor will bind if the projected scenario variable decreases the projected interest rate below the stated floor. Increases in segmentation will increase the accuracy of the interest rates by limiting interest rate movements when a floor should be binding." | WHOLESALE (wholesale §8) |
| A154 | "More generally, please provide comments on the segmentation described above for both wholesale and retail portfolios in the context of the calculation of interest income on loans." | COMMON (both hierarchies) |
| A155 | "Should wholesale fixed-rated balances use the same approach as retail (i.e., only using new originations), for calculation of the interest rate spread? The current approach of wholesale fixed-rated balances is to use the base variable at the median origination date." | WHOLESALE (wholesale §6) |
| A156 | "A specific approach to assess whether a particular account is a revolver is outlined above. Is there a better approach to determining whether a particular account is a revolver? For example, an account could be classified as revolver if the account has finance charges observed on FR Y-14M reports." | RETAIL — deferred |
| A157 | "The model uses a scalar to true-up at the jump-off quarter to account for data knowledge gaps and utilize the same scalar throughout the projection horizon. Is the use of the scalar reasonable? The scalar could be applied at the bank industry-wide level or at a portfolio level. Is one approach preferable to the other for any specific reason? Are there better approaches to address these data and knowledge gaps?" | COMMON (§8; OQ-014) |
| A158 | "Are there additional factors that the Board should consider to model changes to the interest rate spread?" | COMMON (§7.5–7.6) |
| A159 | "Interest rate risk hedges on loans have not been directly incorporated into the calculations described above, primarily due to data limitations. The Board is proposing additional data collection through an updated FR Y-14Q, Schedule B.2 to incorporate interest rate risk hedges for interest income on loans. Are there any special considerations that the Board should be aware of when considering how to account for interest rate risk hedges for interest income on loans?" | COMMON (§11; OQ-005) |
| A160 | "Are there additional factors that the Board should consider in modeling loan interest income?" | COMMON |

Numbering note: A151–A160 are unique in the document (the SQ-3 duplication affects A161/A162 in the sibling sections); cite with the section regardless, per the project's question-numbering rule.

---

## 14. Coding considerations — [CODE], non-normative

Nothing here is Fed methodology. No production Python in this phase.

- **Segment-cell registry as data.** Represent the portfolio/segment hierarchy (p, i) as configuration data (portfolio → segmentation dimensions → cells), not as code branches; wholesale and retail grids then plug into one Equation A32/A33/A38 engine. The wholesale grid is specified in the sibling briefs; retail comes later.
- **Two rate engines, one interface.** Variable (A33) and fixed (A34/A35/A38 with branch-specific spread) engines produce `interest_income_rate[b,p,i,t]`; segment metadata selects the engine via the rate-type dimension.
- **Floors as supplied inputs with a modeled clamp.** Per `asset-side-common-conventions.md` §8, the loans floor is a Fed-**stated** bind — implement as `max(projected_rate, floor)` with binding diagnostics per (b,p,i,t); floor values arrive as supplied inputs that refuse to run while UNKNOWN (OQ-002), never invented.
- **wt as an external input contract.** Define a declared input path for the (p,i,t)-dimensioned re-origination weight (or its three constituent rates) so the OQ-001 external dependency is an interface, not a hard-coded guess; the b-dimension question (OQ-033) makes the contract's dimensionality itself configurable.
- **Scalar as a final multiplicative step** with a Table A8 verification hook (reproduce the seven published values from config; significance metadata n/a here). The category→portfolio mapping is config pending OQ-010.
- **Spread derivation at PQ0 is data preparation**, upstream of the model layer (mirrors the deposit-family Spread(i,b) treatment); the model consumes derived spreads.
- **Rate-scale normalization** is metadata-driven per the established D-006/§12.6 pattern; the quarterly-conversion transform is named and documented (D-004 boundary; §7.7 unresolved interaction with "quarterly compounded" must be settled at spec stage).

---

## 15. Open questions

| ID | Status | Relevance to this brief |
|---|---|---|
| **OQ-001** | OPEN (external dependency) | wt inputs — default/prepayment/maturity rates from the credit-loss models: granularity, definitions, delivery (§7.6, §11) |
| **OQ-002** | OPEN | Floor values and data source unstated (§7.1); wholesale segmentation discussion in wholesale §8 |
| **OQ-003** | OPEN | Wholesale t−a median-origination-date mechanics — owned by wholesale §6; listed here because Eq A37 is transcribed in §7.6 |
| **OQ-006** | RESOLVED FOR PROJECT IMPLEMENTATION (D-004) — source-side absence preserved | Rate basis for "quarterly compounded" income unstated (§7.7) |
| **OQ-010** | OPEN | Table A8 7 rows vs. footnote 63's 8 categories; scalar→portfolio mapping (§8) |
| **OQ-011** | OPEN — RETAIL-deferred | Other-consumer jump-off mapping; listed for census completeness only |
| **OQ-012** | OPEN (minor) — RETAIL-deferred | Revolver-share constancy; census completeness only |
| **OQ-014** | OPEN (confirmation) | Scalar application granularity as-proposed vs. Question A157 alternatives (§8) |
| **OQ-015** | OPEN (minor) | SQ-5 truncation — owned by wholesale §3 |
| **OQ-033** | OPEN — **filed 2026-07-30** | Fixed-rate machinery firm dimension: A34/A35/A36/A38 subscripts omit b vs. "by firm, product, and segment" prose (§5.1, §7.6) |
| **OQ-034** | OPEN — **filed 2026-07-30** | Corporate segment-grid derivation — owned by wholesale §2 |
| **OQ-035** | OPEN — **filed 2026-07-30** | CRE applicability of the Corporate-stated mixed-rate/demand/fee-only rules — owned by wholesale §4 |

---

## 16. Source traceability table

| # | Claim / element | Class | PDF p. | md anchor | Eq/Table/Fn | Verification |
|---|---|---|---|---|---|---|
| 1 | Component name; v.a(1) heading | FACT | 173 | sec-150 | — | Page image 2026-07-30 |
| 2 | Table A6 row "Loans" — Structural | FACT | 168–169 | sec-148 | Table A6 | Integrity review 2026-07-16 |
| 3 | Listed first among 10 structural components; FR Y-14 data basis | FACT | 172 | sec-149 | — | Integrity review (p. 172 in verified set) |
| 4 | Current model = panel regression with AR term; proposal replaces it | FACT | 173 | sec-151 | — | Page image 2026-07-30 |
| 5 | Bottom-up approach and stated benefits | FACT | 173 | sec-151 | — | Page image 2026-07-30 |
| 6 | Eq A32 + where-list; 9-quarter projection | FACT | 173–174 | sec-151 | Eq A32 | Integrity review + page image 2026-07-30; CA-2b md-only |
| 7 | Balance construction; flat balances; same-quarter replenishment; credit-loss re-origination analogy | FACT | 174 | sec-151 | — | Page image 2026-07-30 |
| 8 | No estimated components; loss rates from Retail/Wholesale models; reset indices | FACT | 174 | sec-151 | — | Page image 2026-07-30 |
| 9 | Segmentation purpose; jump-off weighted-average rates; rate type primary | FACT | 174–175 | sec-152 | — | Page image 2026-07-30 |
| 10 | Wholesale/retail hierarchy census (two parts; four sections) | FACT | 175, 177 | sec-153, sec-156 | — | Page image 2026-07-30 |
| 11 | Projected-rate framework: existing + new; runoff; fixed/variable split; floors | FACT | 180 | sec-161 | — | Page image 2026-07-30 |
| 12 | Eq A33 + where-list; spread constant | FACT | 180–181 | sec-162 | Eq A33 | Integrity review + page image 2026-07-30; SQ-20 filed |
| 13 | Base-rate register (Prime; mortgage rate; 3M Treasury) | FACT | 181 | sec-163 | — | Page image 2026-07-30 |
| 14 | Spread definition and granularity; expert judgment (non-core) | FACT | 181 | sec-164 | — | Page image 2026-07-30 |
| 15 | Same-type replacement of run-off variable facilities | FACT | 181–182 | sec-164 | — | Page image 2026-07-30 |
| 16 | Fixed-rate origination-rate prose ("by firm, product, and segment") | FACT | 182 | sec-165 | — | Page image 2026-07-30; SQ-18/OQ-033 |
| 17 | Eqs A34, A35, A36, A37, A38 (verbatim) | FACT | 182–183 | sec-165 | A34–A38 | Integrity review 2026-07-16 + page images 2026-07-30; SQ-6, SQ-7 |
| 18 | Bias rationale paragraph | FACT | 183 | sec-165 | — | Page image 2026-07-30 |
| 19 | wt derivation (default/prepayment/maturity rates) | FACT | 183 | sec-165 | — | Page image 2026-07-30; OQ-001 |
| 20 | Fixed-rate prevalence notes (retail list; CRE income-producing) | FACT | 183 | sec-165 | — | Page image 2026-07-30 |
| 21 | Industry scalar mechanism + example + constancy | FACT | 183–184 | sec-166 | — | Page image 2026-07-30 |
| 22 | Footnote 63 — 8 categories | FACT | 184 (footer) | md 5354 | Fn 63 | Integrity review + page image 2026-07-30 |
| 23 | Table A8 — 7 rows, values | FACT | 220 | sec-209 | Table A8 | Integrity review 2026-07-16 (all values match); SQ-11/OQ-010 |
| 24 | Assumptions (1)–(7) | FACT | 184 | sec-167–168 | — | Page image 2026-07-30 |
| 25 | General limitations paragraph | FACT | 185 | sec-169 | — | Page image 2026-07-30 |
| 26 | Retail/Wholesale limitation subsections exist (ownership split) | FACT | 185–186 | sec-170, sec-171 | — | Page images 2026-07-30 |
| 27 | Questions A151–A160 (verbatim census) | FACT | 186–188 | sec-172 | — | Page images 2026-07-30 |
| 28 | Hedges not incorporated; proposed B.2 collection | FACT | 188 | sec-172 | Question A159 | Page image 2026-07-30; OQ-005 |
| 29 | Nine-quarter horizon (framework) | FACT | 6 | sec-2 | — | Prior verification (ie_dom_time_dep brief §14 row 16) |
| 30 | New quirks SQ-18/SQ-19/SQ-20; new OQ-033/034/035 | filing record | 175–186 | sec-153–171 | — | Filed 2026-07-30 (`inventory/source-integrity-review.md` §8/§9; `handbook/open-questions.md`) |

---

### Brief completion checklist

- [x] Status banner present; no adoption language anywhere.
- [x] Every material statement labeled [FACT]/[PID]/[INT]/[CODE]/[OQ]/[ALT]; unknowns stated UNKNOWN, never defaulted (PID register empty — no loans PIDs exist yet).
- [x] Equations A32–A38 transcribed verbatim from the md working source and verified against PDF page images (pp. 173–188 fresh pass 2026-07-30).
- [x] Common-boundary register (§3) accounts for every subsection of v.a(1); nothing placed in the common framework merely for appearing in the loan section.
- [x] Launch-point vs. projection-quarter timing explicit (§5.3); constancy register complete (§6.2).
- [x] Retail content identified + deferred only; wholesale detail delegated to `ii_loans_wholesale.source-brief.md`.
- [x] Conversion artifacts corrected per integrity review (CA-2b); source quirks preserved verbatim with [INT] notes (SQ-5/6/7/11/18/19/20).
- [x] No production Python; no confidential workbook content.
- [x] Review state: **APPROVED 2026-08-03** (banner and checklist updated 2026-08-12).

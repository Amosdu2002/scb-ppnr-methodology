# Source Brief — Interest Income on Loans: Corporate (`ii_loans` — wholesale/corporate)

> **STATUS: Proposed for the 2026 stress test — public-comment stage, NOT adopted.**
> Component: **Interest Income on Loans**, Section v.a(1) (PDF pp. 173–188; md sec-150–172); this brief covers the **Corporate** part of Wholesale (PDF pp. 175–176; md sec-154), plus the Corporate-relevant passages of the Wholesale Portfolio limitations (PDF p. 186; md sec-171), Question A153 (PDF p. 187; md sec-172), and Table A8 (PDF p. 220; md sec-209). Model type per Table A6: **Structural**.
> Deliverable: loans workstream (asset-side Increment 3), slice 2 per the approved plan of 2026-08-03 — third of the sibling set {common, wholesale, **corporate**, CRE}. Review state: **DRAFT — awaiting user review.**
> Scope: **Corporate only.** CRE and Retail appear solely where the source draws an explicit boundary against them (§2.3); neither is analyzed. Equations are **not** transcribed here — D-010(b) puts all of A32–A38 verbatim in `ii_loans_common.source-brief.md` §7; rules shared by Corporate and CRE live in `ii_loans_wholesale.source-brief.md`. This brief owns only what the source states for Corporate.
> Integrity flags: SQ-5 (truncated "sourced from FR.", p. 175), SQ-18/OQ-033 (fixed-rate subscripts), SQ-19 ("farm"/"farmland", p. 186), footnotes 61–62; **filed with this brief:** SQ-21 ("Schedule H.1 schedule" doubling), SQ-22 (owner-occupancy naming variants). Open questions: OQ-001, OQ-002, OQ-003, OQ-010, OQ-033, OQ-034, OQ-035, OQ-037, OQ-038; **OQ-036 resolved for project implementation** by **PID-LOAN-1** (§0.1) — the first loans PID.
> Verification: **PDF pp. 175–176 and 220 re-read as page images at high zoom 2026-08-03** for this brief (11-item enumeration, NPML paragraph, Table A8 row text, footnote 62); pp. 173–188 had a full image pass 2026-07-30. Citation format: (PDF p. N; md sec-M).

---

## 0. Classification legend and cross-reference discipline

Labels [FACT] / [PID] / [INT] / [CODE] / [OQ] / [ALT] per `ii_loans_common.source-brief.md` §0.

### 0.1 Project implementation decision register (user-confirmed)

| ID | Decision | Fed-source status of the same point |
|---|---|---|
| **PID-LOAN-1** (2026-08-03) | **The three data-limited Corporate portfolios are treated as floating (variable) rate.** Loans for purchasing and carrying securities, domestic farmland loans, and international farmland loans — the portfolios with no loan-level FR Y-14Q H.1 data and therefore no rate-type split — are all projected on the **variable-rate path** (Equation A33: 3-month Treasury base rate + constant launch-point spread), each as a single undivided block | **Partially concurs.** The source states the variable-rate conclusion for **loans for purchasing and carrying securities only**: "The majority of NPMLs were variable-rate, so the Board assumes loans for purchasing and carrying securities have variable rates" (PDF p. 176; md sec-154) — [FACT], and the PID agrees there. For **domestic and international farmland loans the source states no rate type at all**; that absence is preserved as [FACT] and the PID supplies the project treatment. Resolves **OQ-036** for project implementation |

| **PID-LOAN-2 … PID-LOAN-8** (2026-08-03) | **The Corporate implementation set** — segment key and granularity; rate pools and initial interest rates; spread construction by rate type; engine assignment with rate types `0`/`4` counting toward balance but earning nothing; wt from contractual maturities; floors from CORP H.1; and the input contract. Full text in `handbook/open-questions.md`; the computation is specified in **`specifications/interest-income/loans/ii_loans_corporate.spec.md`** | Mixed: PID-LOAN-6 (wt) and PID-LOAN-5 (fee-based balances in the denominator) are **recorded divergences** from the Fed text; the others operationalize rules the source states without mechanics. Resolve **OQ-001, OQ-002, OQ-003** for Corporate project implementation; all three source-side gaps preserved |

Terminology note [FACT]: "floating" is the FR Y-14Q reported value corresponding to this document's "variable-rate" — footnote 62, "The wholesale FR Y-14Q interest rate variability value for variable-rate is floating" (PDF p. 175 footer; md 5352). PID-LOAN-1 is therefore stated in the source's own reporting vocabulary and means the variable-rate treatment throughout this brief.

The PID register records a modeling treatment only; it contains no confidential workbook content, formulas, sheet names, or firm data. **No physical line-item or field mapping has been user-confirmed for loans yet.**

Ownership rule for the sibling set (D-010):

| Layer | Owns | Brief |
|---|---|---|
| Common | Eqs A32–A38 verbatim; balance construction; segmentation principle; base-rate register; spread definition; floors rule; industry-scalar mechanism and Table A8 values; assumptions (1)–(7); question census; hedge exclusion | `ii_loans_common.source-brief.md` |
| Wholesale | Two-part hierarchy; HFI/FVO-HFS; H.1 facility-level basis; 3M Treasury base rate; Eq A37 application (t−a); wholesale floor discussion; roll-off statements; Wholesale Portfolio limitations; the **scope** question on the rate-type/fee rules (OQ-035) | `ii_loans_wholesale.source-brief.md` |
| **Corporate (this brief)** | The 11-portfolio census; the Corporate segmentation grid; Corporate data classifications; the **mechanics** of the mixed-rate/demand/fee-only rules; the NPML proxy exception; Corporate-relevant scalar rows | this file |

Nothing owned above is restated here; §9 is the inheritance register that makes the boundary auditable.

---

## 1. Executive summary

**What Corporate is.** [FACT] "The corporate section of loan level interest income is segmented by 11 disclosure categories and loan types (referenced as a portfolio)" (PDF p. 175; md sec-154). It is one of the two wholesale parts, the other being CRE. Its 11 portfolios span commercial and industrial lending, leases, sovereign and financial-institution lending, agricultural and farmland lending, margin-type lending, **and owner-occupied commercial real estate** — the last of which makes owner-occupancy, not property type, the Corporate/CRE dividing line (§2.3).

**How Corporate segments.** [FACT] Each portfolio carries the wholesale asset classification (HFI; FVO/HFS), and "Most of the firm's corporate portfolios (16 out of 22) are further segmented by the interest rate variability" (PDF p. 175). Three portfolios — loans for purchasing and carrying securities, domestic farmland loans, and international farmland loans — are **not** rate-split "because they have no loan-level data on the FR Y-14Q H.1 schedule" (PDF p. 176).

**Corporate's three classification rules.** [FACT] Mixed-rate and demand loans are treated as variable-rate; fee-only loans generate no interest income and are removed from **both** the average-rate calculation and the total-balances calculation; and the three data-limited portfolios inherit "the same bank-level interest rate spread as reported in their variable-rate lending to depository institutions," justified by non-purpose margin loan (NPML) analysis (PDF p. 176).

**What is unresolved.** The data slice behind the proxy spread is ambiguous and its granularity is bank-level, unlike every other spread in the model (OQ-037); and unlike CRE, the source never names the form that defines the 11 Corporate categories (OQ-038). A third gap — the source states a rate type for only one of the three data-limited portfolios (OQ-036) — is **resolved for project implementation** by PID-LOAN-1 (§0.1): all three are treated as floating. The Fed-side absence stands.

---

## 2. Corporate scope and boundaries

### 2.1 Position in the hierarchy

[FACT] Wholesale is "organized into two parts: Corporate and Commercial Real Estate (CRE)" (PDF p. 175; md sec-153). Corporate is a **section**, not a Table A6 component — the Table A6 row is the single "Loans" component (PDF pp. 168–169; md sec-148), and D-003 keeps all six portfolio families in one chapter.

### 2.2 What the source states about Corporate's own definition

[FACT] Corporate is defined **extensionally** — by the list of 11 portfolios — not by a stated inclusion principle. The source gives no criterion by which a facility is judged "corporate," and names no form or schedule that defines the 11 categories.

[FACT — contrast, verified on the page image 2026-08-03] The CRE section, on the facing page, does name its authority: its six loan types are "as defined in FR Y-9C" (PDF p. 176; md sec-155). Corporate's parallel sentence carries no such attribution. This asymmetry is **OQ-038**.

### 2.3 Explicit boundaries against CRE and Retail

Recorded because the source draws them; neither neighbour is analyzed here.

| Boundary | Source statement | Label |
|---|---|---|
| **Owner-occupied CRE is Corporate** | Corporate portfolios (2) "domestic owner-occupied CRE loans" and (6) "international owner-occupied CRE loans" (PDF p. 175) | [FACT] |
| **Non-owner-occupied CRE is CRE** | CRE portfolios (3) "domestic non-owner occupied commercial real estate loans" and (6) "international non-owner occupied commercial real estate loans" (PDF p. 176) | [FACT] |
| Construction and multifamily are CRE | CRE portfolios (1), (2), (4), (5) (PDF p. 176) | [FACT] |
| Retail is a separate hierarchy | "Retail interest income projections are organized into four sections" (PDF p. 177; md sec-156) | [FACT] |
| Small-business exposures | Retail's fourth section covers "other non-core credit products such as small business loans, SME cards…" (PDF p. 177) — **retail-side**, though Table A8's "C&I, noncore SME loan and card" row spans both naming worlds (§10) | [FACT]; scalar consequence in OQ-010 |

[INT] Consequence worth carrying to the chapter: **the Corporate/CRE line is owner-occupancy, not asset type.** Two of the eleven Corporate portfolios are commercial-real-estate exposures that take the Corporate treatment, so a naive "all CRE goes to the CRE section" grouping would misroute them. The source states the placement; the characterization of the dividing line is the interpretation.

---

## 3. Corporate portfolio census

### 3.1 The 11 portfolios (verbatim, source order)

[FACT] (PDF p. 175; md sec-154; enumeration re-verified at high zoom 2026-08-03 — all eleven items present, numbering intact, no merged entries): "Portfolios included in the corporate section are: (1) commercial and industrial loans, (2) domestic owner-occupied CRE loans, (3) other non-consumer loans, (4) other leases, (5) loans to foreign governments, (6) international owner-occupied CRE loans, (7) agricultural loans, (8) loans to financial institutions, (9) loans for purchasing and carrying securities, (10) domestic farmland loans, and (11) international farmland loans."

### 3.2 Per-portfolio attribute register

Coding-friendly names are this project's, not the Fed's. "Rate-split?" and "Loan-level data?" are [FACT] per §4; "Rate type if unsplit" distinguishes the one portfolio the source assigns from the two it leaves unstated, both supplied by **PID-LOAN-1** (§0.1, §6.4).

| # | Fed portfolio name | Coding-friendly name | Loan-level data on H.1? | Rate-split? | Rate type if unsplit |
|---|---|---|---|---|---|
| 1 | commercial and industrial loans | `corp_ci` | Yes | Yes | — |
| 2 | domestic owner-occupied CRE loans | `corp_oocre_dom` | Yes | Yes | — |
| 3 | other non-consumer loans | `corp_other_nonconsumer` | Yes | Yes | — |
| 4 | other leases | `corp_other_leases` | Yes | Yes | — |
| 5 | loans to foreign governments | `corp_foreign_govt` | Yes | Yes | — |
| 6 | international owner-occupied CRE loans | `corp_oocre_intl` | Yes | Yes | — |
| 7 | agricultural loans | `corp_agricultural` | Yes | Yes | — |
| 8 | loans to financial institutions | `corp_fin_institutions` | Yes | Yes | — |
| 9 | loans for purchasing and carrying securities | `corp_purch_carry_sec` | **No** [FACT] | **No** [FACT] | **variable/floating** — [FACT, stated]; **[PID-LOAN-1]** concurs |
| 10 | domestic farmland loans | `corp_farmland_dom` | **No** [FACT] | **No** [FACT] | UNSTATED in source [FACT absence] → **variable/floating [PID-LOAN-1]** |
| 11 | international farmland loans | `corp_farmland_intl` | **No** [FACT] | **No** [FACT] | UNSTATED in source [FACT absence] → **variable/floating [PID-LOAN-1]** |

[INT] Rows 1–8 are marked "Yes" by elimination: the source names exactly three portfolios as lacking loan-level H.1 data, so the remaining eight have it. The source does not assert this positively for any individual portfolio.

### 3.3 Undefined and residual categories

- [FACT absence] "other non-consumer loans" (3) and "other leases" (4) are residual categories with **no definition, inclusion rule, or example** anywhere in the document. Their contents are UNKNOWN (OQ-038).
- [FACT absence] The source says nothing about how **lease** income is treated. Leases are placed in a portfolio of an interest-income model without comment; whether lease income is measured on the same interest-rate basis as loan interest is not addressed. Recorded as an absence — nothing is inferred.
- [FACT] "C&I" as an abbreviation appears **nowhere** in the loan section; it exists only in Table A8's row label (full-document search 2026-08-03). The link from that row to portfolio (1) is therefore inference, not a stated mapping (§10).

---

## 4. Corporate segmentation hierarchy

### 4.1 The dimensions and their order

| Level | Dimension | Values | Source |
|---|---|---|---|
| 0 | Wholesale part | Corporate | [FACT] PDF p. 175; md sec-153 |
| 1 | Portfolio `p` | the 11 of §3.1 | [FACT] PDF p. 175; md sec-154 |
| 2 | Asset classification | HFI; FVO/HFS | [FACT] PDF p. 175; md sec-153 (stated for each wholesale section) |
| 3 | Rate type | fixed-rate; variable-rate — **8 portfolios only** | [FACT] PDF pp. 175–176; md sec-154 |

[INT — ordering] Classification precedes rate type. Basis: the source describes the rate split as applying to portfolios that are "**further** segmented," and the count it uses ("16 out of 22") only reconciles if the 22 already carry the asset-classification dimension (§4.2). The source does not state the order explicitly.

### 4.2 The 22-cell grid

> **⚠ [INT] — THIS ENTIRE SUBSECTION IS INTERPRETATION, NOT SOURCE-STATED.**
> The Federal Reserve states only the phrase "16 out of 22" (PDF p. 175) and no total segment count for Corporate. The grid below is this project's reconstruction, recorded because the future specification needs an enumerable structure. It must not be cited as Fed methodology, and it must be re-derived if **OQ-034** resolves differently.

[INT] Reconstruction: 11 portfolios × 2 asset classifications = **22 portfolio-classification cells**. The three portfolios without loan-level H.1 data contribute 3 × 2 = **6** cells that are not rate-split; the remaining 8 portfolios contribute 8 × 2 = **16** cells that are — matching the source's "16 out of 22" **exactly**.

**Strength of the reading (new evidence, 2026-08-03):** the arithmetic reconciles on both sides simultaneously — the eight data-bearing portfolios produce exactly 16, and the three data-limited ones exactly 6. This is materially stronger than a plausible guess, since no other partition of 11 portfolios into two asset classifications yields 16 and 6 without contradicting the source's own list of exactly three data-limited portfolios. It remains [INT] because the source never states the multiplication, never names the 22, and never confirms that asset classification is the second dimension.

| Grid element | Count | Label |
|---|---|---|
| Portfolios | 11 | [FACT] |
| Asset classifications | 2 | [FACT] |
| Portfolio × classification cells | 22 | [INT] (source states the number 22 only inside "16 out of 22") |
| Cells further split by rate type | 16 | [FACT] (as a number); [INT] which cells |
| Cells not rate-split | 6 | [INT] |
| **Implied Corporate segments** | **16 × 2 + 6 = 38** | **[INT] — no Corporate total is stated** |

[FACT — contrast] CRE's total **is** stated: "the total number of CRE segments is 24" (PDF p. 177; md sec-155). The absence of a Corporate counterpart is a fact about the source, not an omission in this brief.

[INT] Wholesale total under this reading: 38 + 24 = 62 segments. Carried for planning only.

---

## 5. Data inputs and classifications to capture

Every row states whether the source names the item. **No field name, code, or value vocabulary is invented.**

| # | Item to capture | Source status | Granularity | Notes |
|---|---|---|---|---|
| 1 | Facility-level records, FR Y-14Q Schedule H.1 | [FACT] — schedule named (PDF p. 176); facility level per footnote 61 | facility | The document's "loan level" wording is a readability convention (fn 61) |
| 2 | Portfolio / disclosure-category assignment | [FACT] that 11 categories exist; **defining form UNSTATED** | facility → p | **OQ-038** |
| 3 | Asset classification (HFI, FVO/HFS) | [FACT] (PDF p. 175) | facility | No field named |
| 4 | Interest-rate-variability value | [FACT] — the reported value for variable-rate "is floating" (fn 62); mixed-rate and demand are named as distinct cases (PDF p. 176) | facility | Full value vocabulary UNKNOWN; only *floating*, *mixed*, *demand* are evidenced |
| 5 | Demand-loan indicator | [FACT] the class exists, with the source's own definition (§6) | facility | No field named |
| 6 | Fee-only indicator | [FACT] the class exists (PDF p. 176) | facility | No field named; drives a **balance** exclusion (§8) |
| 7 | NPML identifier | [FACT] "the FR Y-14Q Schedule H.1 schedule is able to identify NPMLs" (PDF p. 176) | facility | SQ-21 wording |
| 8 | Facility outstanding balance | [FACT] via the common balance construction | facility → segment share, portfolio balance | Common §6 |
| 9 | Facility interest rate | [FACT] via the common jump-off construction | facility → segment | Balance-weighted average per segment; common §7.2 |
| 10 | Bank-level spread on variable-rate lending to depository institutions | [FACT] the assumption; **source data slice ambiguous** | **bank** | **OQ-037**; §7 |
| 11 | Median origination date per portfolio | [FACT] required by Eq A37 | portfolio | Wholesale §6; OQ-003 |
| 12 | Portfolio interest-rate floor | [FACT] the rule; values/source UNKNOWN | portfolio (or finer — Question A153) | Common §7.1; OQ-002 |
| 13 | Re-origination weight inputs | [FACT] the dependency | (p,i,t); firm dimension open | Wholesale credit-loss models; OQ-001, OQ-033 |

[FACT absence] The source names **no H.1 field, MDRM code, or value list** for items 2–7. The schedule is identified; its contents are not.

---

## 6. Rate-type classification rules (Corporate mechanics)

The **scope** question — whether these rules reach CRE — is owned by the wholesale brief (OQ-035). This section documents the mechanics as stated.

### 6.1 The two broad types

[FACT] "The two broad types of interest rate variability, fixed-rate and variable-rate, are used to segment each portfolio." (PDF pp. 175–176; md sec-154) Footnote 62: "The wholesale FR Y-14Q interest rate variability value for variable-rate is floating. Using variable-rate in this document for ease of readability." — the **reported value is "floating"**; "variable-rate" is the document's term (re-verified on the page image 2026-08-03).

### 6.2 Mixed-rate and demand loans → variable-rate

[FACT] "The interest income model treats mixed-rate and demand loans (loans where the lender can demand full repayment at any time) as variable-rate." (PDF p. 176; md sec-154)

- The parenthetical defines **demand loans** only; **mixed-rate** is used without definition [FACT absence].
- [INT] Consequence: these facilities take the Equation A33 path (base rate + constant launch-point spread), so they reprice fully with the 3M Treasury despite not being contractually floating. The consequence follows from the classification; the source states only the classification.

### 6.3 Fee-only loans → excluded

Full treatment in §8.

### 6.4 The three data-limited portfolios

[FACT] "Loans for purchasing and carrying securities, domestic farmland loans, and international farmland loans are not segmented by interest rate variability because they have no loan-level data on the FR Y-14Q H.1 schedule. This limits further segmentation and requires additional assumptions to model interest income for these portfolios." (PDF p. 176; md sec-154)

[FACT] The rate-type conclusion the source draws: "The majority of NPMLs were variable-rate, so the Board assumes **loans for purchasing and carrying securities** have variable rates." (PDF p. 176; emphasis added)

**The gap — OQ-036 [filed 2026-08-03].** The concluding sentence names **only** portfolio (9). Portfolios (10) and (11) are included in the *spread* assumption of the preceding sentence ("The Board assumes, for these portfolios…") and in the p. 186 NPML-proxy restatement, but no sentence assigns them a rate type. Since an unsegmented portfolio still needs one engine or the other, this is load-bearing.

**Project treatment — [PID-LOAN-1], user-confirmed 2026-08-03 (§0.1).** All three data-limited portfolios are treated as **floating (variable) rate** and projected on the Equation A33 path, each as a single undivided block. This **resolves OQ-036 for project implementation**; it is never presented as a Federal Reserve statement for portfolios (10) and (11), whose rate type the source leaves unstated — that absence stands as [FACT].

Supporting reasoning, recorded so the decision is auditable rather than bare [INT]:

- The borrowed spread is drawn from **variable-rate** lending, and in this model a "base rate + constant spread" construct **is** the variable-rate form (Eq A33). A fixed-rate treatment would instead require the Equation A37 wholesale spread — the all-loan jump-off average rate less the base rate at the median origination date — so running a variable-rate-derived spread through the fixed engine would be internally incoherent.
- The p. 186 limitation groups all three portfolios under a single NPML proxy without distinguishing them (PDF p. 186; md sec-171).
- The wholesale section states that "the majority of balances in wholesale are variable-rate" (PDF p. 181; md sec-163).

[INT — countervailing consideration, recorded not resolved] Farmland and agricultural real-estate lending commonly carries a substantial fixed or long-reset component, so a fully-repricing treatment may overstate those balances' scenario sensitivity. The materiality of that effect depends on the firm's farmland balances and is UNKNOWN at handbook stage. The consideration does not change PID-LOAN-1; it is the reason the Fed-side absence is kept visible and OQ-036 remains open on the source side.

---

## 7. The NPML proxy exception (Corporate-specific)

### 7.1 What the source states

[FACT] (PDF p. 176; md sec-154, verbatim): "The Board assumes, for these portfolios, the same bank-level interest rate spread as reported in their variable-rate lending to depository institutions. This assumption is based on loan-level data on non-purpose margin loans (NPML), which have similar characteristics to loans for purchasing and carrying securities. Currently, the FR Y-14Q Schedule H.1 schedule is able to identify NPMLs."

[FACT] Restated among the Wholesale limitations (PDF p. 186; md sec-171): "The model assumes that non-purpose margin loans (NPML) are a good proxy for loans for purchasing and carrying securities, domestic farm loans, and international farm loans. The Board used the loan-level analysis with only NPML as guidance to how to treat these missing portfolios." (**SQ-19**: "farm loans" here versus "farmland loans" on p. 175 — same portfolios, source-internal naming variant, recorded, never corrected.)

### 7.2 What makes this an exception

| Aspect | Everywhere else in the model | Here | Label |
|---|---|---|---|
| Spread granularity | firm × product × segment — "it varies by firm, product, and segment" (PDF p. 181) | **bank-level** | [FACT] — a stated granularity exception |
| Spread source | the segment's own balance-weighted rate minus the base rate | another portfolio's variable-rate lending | [FACT] |
| Rate-type determination | reported rate-variability value per facility | assumed from NPML population statistics | [FACT] |

[INT] The exception's shape: for these three portfolios the model substitutes a **borrowed spread** for a measured one, because the measurement inputs do not exist on H.1. It is a data-gap workaround, and the source presents it as such ("requires additional assumptions").

### 7.3 The ambiguity — OQ-037 [filed 2026-08-03]

Two distinct unknowns in one sentence:

1. **Which data slice is "their variable-rate lending to depository institutions"?** "Depository institutions" is *narrower* than portfolio (8) "loans to financial institutions" — every depository institution is a financial institution, not conversely. The phrase may therefore denote a sub-slice of portfolio (8), the whole of it, or a dataset outside the 11-portfolio census. The source never links the two terms, and "depository institutions" appears nowhere else in the loan section (its only other Section v occurrence, PDF p. 190, is in the deposits-with-banks model and is unrelated — verified 2026-08-03).
2. **How does a bank-level spread enter a (b,p,i)-dimensioned rate?** Equation A33 consumes Spread(b,p,i,t=0). Whether the bank-level value is assigned to every affected segment unchanged, or aggregated/weighted first, is unstated.

[INT — working reading, flagged] The spread is taken from the variable-rate portion of the firm's lending to depository institutions and applied unchanged to each of the three portfolios' cells. Nothing stronger is available from the text.

### 7.4 The NPML logic chain

[FACT] The reasoning as printed: NPMLs are identifiable on H.1 → NPMLs "have similar characteristics to loans for purchasing and carrying securities" → the majority of NPMLs are variable-rate → portfolio (9) is assumed variable-rate.

[INT] Note the chain is argued for portfolio (9) alone; the similarity claim is made only for margin-type lending, and no equivalent similarity argument is offered for farmland lending. That the same proxy nonetheless covers farmland (p. 186) is the source's own extension — it is stated, not inferred here, but its rationale is not given. This is the qualitative counterpart to OQ-036.

---

## 8. Fee-only loans — the dual exclusion

[FACT] "Fee-only loans are assumed to generate no interest income. Hence, they are not used to calculate the average interest rate, and their outstanding balance percentages are excluded from the total balances calculation." (PDF p. 176; md sec-154)

Two separate removals, and the second is easy to miss:

| Removal | Effect | Label |
|---|---|---|
| From the average interest rate | Fee-only facilities do not dilute the segment's balance-weighted jump-off rate | [FACT] |
| From the total balances calculation | Their outstanding-balance percentages leave the **denominator** — so segment shares are computed over a base that excludes them | [FACT] |

[INT] Consequence for Equation A32: because "Loan balance(b,p,i,t) is calculated by taking the percentage of outstanding balance for segment i … and then multiplying it by the portfolio balance" (common §6), removing fee-only balances from the percentage base means the projected balances of the *remaining* segments are scaled up relative to a naive share. **This is the only stated balance-denominator exclusion anywhere in the loan model** — every other exclusion in v.a(1) affects rates alone.

[FACT absence] "Fee-only loan" is never defined, and no fee-income methodology is stated for wholesale (wholesale §10). Whether the excluded balances earn fee income recorded elsewhere in PPNR is outside this section.

---

## 9. Inheritance register — what Corporate does not restate

Auditable boundary; each row is governed by the cited brief and applies to Corporate unchanged.

| Rule | Governed by | Corporate-specific note |
|---|---|---|
| Eq A32 income identity; 9 quarters; (b,p,i,t) | common §7.0 | — |
| Balance construction; flat balances; same-quarter replenishment | common §6 | Modified only by the fee-only denominator exclusion (§8) |
| Rate type as the primary segmentation principle | common §7.2 | Realized as level 3 of §4.1 |
| Eq A33 variable-rate path | common §7.3 | Also carries mixed-rate and demand facilities (§6.2) |
| Base rate = 3M Treasury | wholesale §5 | No Corporate-specific base rate exists |
| Eqs A34/A35/A38 fixed-rate machinery; wt | common §7.6 | Firm-dimension question OQ-033 applies |
| Eq A37 wholesale spread; median origination date t−a | wholesale §6 | Applies per Corporate portfolio; OQ-003 |
| Spread definition and constancy | common §7.5 | Overridden **only** for the three data-limited portfolios (§7) |
| Interest-rate floors | common §7.1; wholesale §8 | Question A153 names corporate explicitly (§11) |
| Industry-scalar mechanism; Table A8 values | common §8 | Row applicability in §10 |
| Assumptions (1)–(7); general limitations | common §12 | No Corporate-specific assumption list exists in the source |
| Quarterly compounding versus D-004 | common §7.7 | Unresolved at project level |
| Hedge exclusion (Question A159) | common §11 | Loans exclude hedges entirely; OQ-005 |
| Scope of the mixed/demand/fee-only rules beyond Corporate | wholesale §4 | OQ-035 — this brief owns mechanics only |

---

## 10. Table A8 rows touching Corporate

[FACT] Table A8 values re-verified on the page image 2026-08-03 (PDF p. 220; md sec-209). The two rows whose names point at wholesale are **"C&I, noncore SME loan and card" (1.033)** and **"Rest of wholesale" (1.113)**; **"Domestic CRE" (1.081)** matters to Corporate only through the owner-occupied question below.

Open mapping problems, all under **OQ-010**:

1. **No row is named "Corporate."** Which of the 11 portfolios each scalar multiplies is unstated.
2. **"C&I" never appears in the loan section** (§3.3), so even the natural link to portfolio (1) is inference.
3. **The row merges naming worlds** — "C&I" is wholesale vocabulary while "noncore SME loan and card" is retail vocabulary (retail's fourth section covers small business loans and SME cards). A single scalar spanning both sides is what SQ-11 and footnote 63's eight-versus-seven mismatch describe.
4. **Owner-occupied CRE is unassigned** — portfolios (2) and (6) are Corporate-modeled CRE exposures. Whether the "Domestic CRE" scalar reaches domestic owner-occupied CRE, or whether those balances fall under a corporate row, is unstated. [Corporate-scoped sub-question of OQ-010; the international counterpart is the wholesale brief's sub-question.]
5. **Eight of eleven portfolios have no obvious row**, leaving "Rest of wholesale" as the residual candidate — inference, not a stated mapping.

[CODE] Because the scalar multiplies every quarter's output, a misassignment is a systematic error. The category→portfolio map must be configuration with an explicit "unmapped portfolio" hard error, never a silent default to the residual row.

---

## 11. Board questions touching Corporate

Verbatim census in common §13; pointers only here.

- **A153** — the only question naming corporate directly: "Should **corporate** and CRE variable-rate balances be further segmented to vary the interest rate floor?" (PDF p. 187; md sec-172). Bears on §5 item 12 and OQ-002; the Fed treats Corporate floor granularity as open.
- **A154** — segmentation comment request covering "both wholesale and retail portfolios," which includes the §3–§4 structure.
- **A152**, **A155**, **A157**, **A159** — inherited (base rate, wholesale fixed-rate spread, scalar granularity, hedges); see the wholesale and common briefs.

[FACT absence] No Board question asks about the NPML proxy, the fee-only exclusion, or the data-limited portfolios — the Fed does not itself flag them as open.

---

## 12. Fed-stated limitations bearing on Corporate

The Wholesale Portfolio limitations subsection is owned by the wholesale brief §12; two of its six items are Corporate-specific in substance:

1. [FACT] **The NPML proxy** (PDF p. 186; md sec-171) — quoted in §7.1. This is the only limitation that names Corporate portfolios.
2. [FACT] **Loan-level versus segment-level projection** — "More accuracy could be gained projecting interest income at the loan level instead of cutting the portfolio into segments" (PDF p. 185). [INT] Directly relevant to §4's grid: the segment grid is itself the acknowledged approximation.

[FACT absence] There is **no Corporate-specific assumptions or limitations subsection**; the (c) block is organized as Assumptions / Limitations / Retail Portfolio / Wholesale Portfolio only (PDF pp. 184–186; md sec-167–171).

---

## 13. Coding considerations — [CODE], non-normative

Nothing in this section is Fed methodology. No production Python.

- **Portfolio census as configuration.** The 11 portfolios, their coding names, and the §3.2 attributes belong in a data table, not in code branches — the engine then reads the grid rather than encoding Corporate's shape.
- **Rate-type mapping with a hard error.** Map the reported variability value to {fixed, variable, excluded}: *floating* → variable (fn 62), *mixed* → variable, *demand* → variable, *fee-only* → excluded. Any value outside the evidenced vocabulary must **surface and stop** — the value list is UNKNOWN (§5 item 4), so a default would be an invention (precedent: PID-SEC-5's unmapped-category hard error).
- **Fee-only exclusion must run before share computation.** Removing fee-only balances after the denominator is formed silently understates the surviving segments' balances (§8). Worth an explicit invariant: the segment shares within a portfolio sum to one over the fee-only-excluded base.
- **The proxy spread as a distinct input.** Give the bank-level spread its own named input rather than overloading the segment-spread container, so the OQ-037 granularity exception stays visible in the data model instead of being flattened into (b,p,i).
- **Unsegmented portfolios still need an engine.** Portfolios (9)–(11) carry no rate-type dimension; per **[PID-LOAN-1]** all three route to the variable/floating engine as single undivided blocks. Implement that routing as a **named, documented rule carrying the PID reference** — not a configurable switch and not an implicit default — so the decision stays visible in the code path (precedent: PID-6's treatment of the ÷4 conversion). The three portfolios should remain individually identifiable in outputs, since the source states the rate type for only one of them.
- **Non-normative category cross-walk (unverified).** The FR Y-9C is **not** in `sources/`, so nothing below is verified against a form: the Corporate names track the loan-category language of the FR Y-9C loans-and-leases schedule (commercial and industrial; loans to foreign governments and official institutions; loans to depository institutions; agricultural production; loans secured by farmland; owner-occupied nonfarm nonresidential real estate). This is **name similarity only** — no item numbers or MDRM codes are asserted, and the mapping must be confirmed against the form instructions in the approved environment before any use. Recorded to speed that later mapping, never as methodology (OQ-038).

---

## 14. Open questions

| ID | Status | Relevance |
|---|---|---|
| **OQ-036** | **RESOLVED FOR PROJECT IMPLEMENTATION 2026-08-03 (PID-LOAN-1)** — source-side absence preserved | Rate type of domestic and international farmland loans unstated; the variable-rate conclusion names only loans for purchasing and carrying securities (§6.4). Project treatment: all three floating/variable |
| **OQ-037** | OPEN — **filed 2026-08-03** | NPML proxy spread: which data slice "variable-rate lending to depository institutions" denotes, and how a bank-level spread enters a (b,p,i) rate (§7.3) |
| **OQ-038** | OPEN — **filed 2026-08-03** | The form defining the 11 Corporate disclosure categories is unstated, unlike CRE's "as defined in FR Y-9C"; "other non-consumer loans" and "other leases" undefined (§2.2, §3.3) |
| **OQ-034** | OPEN — evidence strengthened 2026-08-03 | The 22-cell reconstruction now reconciles on both sides (16 and 6) exactly; still [INT], and no Corporate segment total is stated (§4.2) |
| **OQ-010** | OPEN | Scalar row → portfolio mapping, including owner-occupied CRE and the eight unmapped portfolios (§10) |
| **OQ-033** | OPEN | Firm dimension of the fixed-rate machinery; applies to Corporate fixed-rate segments (common §7.6) |
| **OQ-035** | OPEN | Whether the §6 rules reach CRE — wholesale-owned; this brief owns mechanics only |
| **OQ-002** | OPEN | Floor values/source; Question A153 names corporate (§11) |
| **OQ-003** | OPEN | Median origination date mechanics for the Corporate Eq A37 spread |
| **OQ-001** | OPEN | Wholesale credit-model rates into wt |

---

## 15. Source traceability table

| # | Claim / element | Class | PDF p. | md anchor | Verification |
|---|---|---|---|---|---|
| 1 | Corporate is one of the two wholesale parts | FACT | 175 | sec-153 | Page image 2026-08-03 |
| 2 | "11 disclosure categories and loan types (referenced as a portfolio)" | FACT | 175 | sec-154 | Page image 2026-08-03 (high zoom) |
| 3 | The 11-portfolio enumeration, verbatim and complete | FACT | 175 | sec-154 | Page image 2026-08-03 — numbering and items confirmed intact |
| 4 | Owner-occupied CRE (2) and (6) sit in Corporate | FACT | 175 | sec-154 | Page image 2026-08-03 |
| 5 | CRE's six types are "as defined in FR Y-9C"; Corporate names no form | FACT + FACT absence | 176 vs. 175 | sec-155 vs. sec-154 | Page images 2026-08-03; OQ-038 |
| 6 | "16 out of 22" further segmented by interest rate variability | FACT | 175 | sec-154 | Page image 2026-08-03; grid reconstruction is INT (OQ-034) |
| 7 | Footnote 62 — reported variable-rate value is "floating" | FACT | 175 (footer) | md 5352 | Page image 2026-08-03 |
| 8 | Footnote 61 — wholesale data are facility level | FACT | 175 (footer) | md 5350 | Page image 2026-08-03 |
| 9 | Mixed-rate and demand loans → variable-rate; demand-loan definition | FACT | 176 | sec-154 | Page image 2026-08-03 |
| 10 | Fee-only: no interest income; excluded from the average rate **and** the total balances calculation | FACT | 176 | sec-154 | Page image 2026-08-03 |
| 11 | Three portfolios not rate-split; no loan-level data on H.1 | FACT | 176 | sec-154 | Page image 2026-08-03 |
| 12 | Bank-level proxy spread from variable-rate lending to depository institutions | FACT | 176 | sec-154 | Page image 2026-08-03; OQ-037 |
| 13 | "the FR Y-14Q Schedule H.1 schedule is able to identify NPMLs" | FACT (SQ-21) | 176 | sec-154 | Page image 2026-08-03 — doubling present in the PDF |
| 14 | Variable-rate conclusion names only loans for purchasing and carrying securities | FACT | 176 | sec-154 | Page image 2026-08-03; OQ-036 |
| 14a | All three data-limited portfolios treated as floating/variable | **PID-LOAN-1** | — | — | User confirmation 2026-08-03 — never attributable to the Fed for portfolios (10) and (11) |
| 15 | NPML proxy restated for "domestic farm loans, and international farm loans" | FACT (SQ-19) | 186 | sec-171 | Page image 2026-07-30 |
| 16 | Loan-level versus segment-level accuracy limitation | FACT | 185 | sec-171 | Page image 2026-07-30 |
| 17 | Question A153 names corporate | FACT | 187 | sec-172 | Page image 2026-07-30 |
| 18 | Table A8 rows and values; "C&I, noncore SME loan and card" = 1.033 | FACT | 220 | sec-209 | Page image 2026-08-03 (re-verified); OQ-010 |
| 19 | "C&I" absent from the loan section | FACT absence | 173–188 | sec-150–172 | Full-document search 2026-08-03 |
| 20 | "depository institutions" elsewhere in Section v is unrelated (deposits model) | FACT | 190 | sec-174 | Full-document search 2026-08-03 |
| 21 | Owner-occupancy naming variants across pp. 175–176 | FACT (SQ-22) | 175, 176 | sec-154, sec-155 | Page images 2026-08-03 |
| 22 | No Corporate-specific assumptions/limitations subsection exists | FACT absence | 184–186 | sec-167–171 | Page images 2026-07-30 |

---

### Brief completion checklist

- [x] Status banner present; no adoption language anywhere.
- [x] Every material statement labeled; unknowns stated UNKNOWN; working assumptions flagged and never source-attributed.
- [x] **Zero verbatim equation blocks** — equations cited from the common brief per D-010(b).
- [x] The 11-portfolio enumeration verified at high zoom against the PDF page image (2026-08-03).
- [x] The segmentation grid carries an unmissable [INT] banner; no Corporate segment total presented as fact.
- [x] CRE and Retail appear only as explicit source-drawn boundaries (§2.3); neither is analyzed.
- [x] Inheritance register (§9) makes the common/wholesale boundary auditable; nothing owned elsewhere is restated.
- [x] Source quirks preserved verbatim (SQ-19, SQ-21, SQ-22); no silent corrections.
- [x] The FR Y-9C cross-walk is confined to §13, labeled non-normative and unverified, with no item numbers or codes invented.
- [x] No production Python; no confidential workbook content.
- [ ] Review state: DRAFT — awaiting user review (closes at approval).

# Source Brief — Interest Income on Loans: Consumer and Small Business Credit Card (`ii_loans` — retail/card)

> **STATUS: Proposed for the 2026 stress test — public-comment stage, NOT adopted.**
> Component: **Interest Income on Loans**, Section v.a(1) (PDF pp. 173–188; md sec-150–172); this brief covers the **Consumer and Small Business Credit Card** family of Retail (PDF pp. 178–179; md sec-159) — consumer cards and small business cards as **two sub-portfolios in one brief**, matching the Fed's one section — plus the card-relevant passages elsewhere: the retail census entry (PDF p. 177; md sec-156), the Prime base-rate entry (PDF p. 181; md sec-163), Question A156 (PDF p. 187; md sec-172), the Retail Portfolio limitations (PDF p. 185; md sec-170), Table A8's Credit Card row and the merged "C&I, noncore SME loan and card" row (PDF p. 220; md sec-209), and footnote 63 (PDF p. 184 footer; md 5354). Model type per Table A6: **Structural**.
> Deliverable: loans workstream (asset-side Increment 3), retail wave 2 — drafted 2026-08-12 with the mortgage and other-consumer briefs at the user's direction. Review state: **DRAFT — awaiting user review.**
> Scope: **Card only.** Retail-shared rules cited from `ii_loans_retail.source-brief.md`; equations not transcribed (D-010(b)); other families appear solely at source-drawn boundaries.
> Integrity flags: **filed with this brief — SQ-25** ("reflected in the alternative model", p. 178, referent unstated). Open questions: **OQ-043, filed with this brief** (projected-spread construction: three inputs, no formula); **OQ-012** (revolver-share constancy); the retail legs of OQ-002 (floors) and OQ-010 (scalar rows — the SME-card row question has real teeth here); OQ-033.
> Physical context: the user supplied the **"Card query"** input sheet and the **"M.1 Balances"** retail wiring 2026-08-12 (screenshots; logical contracts registered as **PID-LOAN-28** and **PID-LOAN-26** — §0.1); interpretive readings are **flagged observations (a)–(e)**, not yet confirmed. No firm values appear in this repository.
> Verification: **PDF pp. 178–179 read as page images 2026-08-12** (all four card paragraphs confirmed verbatim; md faithful). Citation format: (PDF p. N; md sec-M).

---

## 0. Classification legend and cross-reference discipline

Labels [FACT] / [PID] / [INT] / [CODE] / [OQ] / [ALT] per `ii_loans_common.source-brief.md` §0.

### 0.1 Project implementation decision register (user-supplied input contracts) and flagged observations

| ID | Decision (one line) | Fed-source status of the same point |
|---|---|---|
| **PID-LOAN-28** | **Card input = the "Card query" sheet**: four numbered segment rows (1–4) with columns `TOTAL_OS`, `WEIGHTED_AVERAGE_APR`, `WEIGHTED_MAX_APR`, `WEIGHTED_SPRD`, `TOTAL_OTST_REVOLVER`, `WEIGHTED_AVERAGE_APR_revolver`, `WEIGHTED_SPRD_revolver` — segment-level; both an **all-book** and a **revolver-only** rate/spread pair per segment, plus the revolver balance; rate/spread units read as percent (D-006 TO CONFIRM at load) | The Fed states "balance-weighted average interest rate, interest spread, and percentage of balance revolving are calculated by segment and firm and used as inputs" (PDF p. 179) and names no layout; the revolver-share numerator/denominator arrive as balances, not a precomputed share |
| **PID-LOAN-26** | **M.1 retail wiring** (registered with the mortgage brief; card-relevant part): domestic roles "Retail - consumer credit card" on the Credit Cards **Bank cards** and **Charge cards** rows and "Retail - SM credit card" on the C&I block's **"SME cards and corporate cards"** row; all three rows flagged in the **"Card (dom)"** family column; the C&I block's separate **"Small business"** row is labeled "Retail - noncore" (NOT card); every retail row's international role is "Retail - noncore" | The Fed separates consumer cards (its own section) from small business cards ("separately but following a similar structure") and places "small business loans, SME cards" in the non-core census (PDF pp. 177–179) — the M.1 wiring realizes that three-way split physically: SME **cards** → Card, small business **loans** → noncore |

**Flagged observations (a)–(e) — screenshot readings, TO CONFIRM at the review gate:**

- **(a) Query row identity.** The four rows carry numeric ids only; by balance correspondence with the M.1 rows, row 1 = consumer bank cards, row 3 = small business cards, and rows 2/4 are empty (charge-card / corporate-card sub-segments with no balances). The id → segment mapping needs the user's statement, and empty sub-segments must load as vacuous-and-censused, never as errors.
- **(b) Revolver share = `TOTAL_OTST_REVOLVER ÷ TOTAL_OS`** per segment — derived at load, not a supplied percentage. Confirm, including whether the share is taken at the same as-of date as the balances.
- **(c) The income cell pair.** Candidates for the income construction: revolver balance × revolver-only rate path; total balance × share × all-book rate path; M.1 balance × share × a query rate. Which (balance, rate/spread) pair the workbook's income cells consume — and whether the M.1 balance or the query `TOTAL_OS` is the Eq A32 multiplicand — is the family's central elicitation item (with OQ-043 as its source-side shadow).
- **(d) `WEIGHTED_MAX_APR` role.** A cap candidate (the ceiling counterpart of a floor) or informational only; no Fed statement corresponds (the stated rule is a **floor**, PDF p. 180). If the workbook applies it as a cap, that is a project construction to record as its own PID.
- **(e) Spread column semantics.** `WEIGHTED_SPRD` reads as APR − Prime at some date (and `_revolver` its revolver-only counterpart); which spread column (all-book vs revolver-only; reported vs derived) seeds the Eq A33 projection is part of (c) and of OQ-043.

### 0.2 Wave-3 engine observations (2026-08-13) — user-supplied calculation-sheet screenshots, TO CONFIRM at the gate

| # | Observation | Sharpens |
|---|---|---|
| (f) | **Three engine switches observed** as header cells: floor mode ("1=floored at prior APR; 0=floor at zero", observed **0**); population ("1=revolver only; 0=full population", observed **0**); spread mode ("0=reported spreads (full population); 1=reported spreads (revolver only); 2=calculated spread", observed **0**) | §0.1 (e) resolved as a switch family. **Spread mode 0 = the REPORTED FR Y-14M spread drives the Eq A33 path — the OQ-043 project-side answer, observed** (the reported spread is not reconciled to APR − Prime; the "calculated" construction exists only as mode 2) |
| (g) | **Row identity confirmed by the calc sheet's own labels**: 1 Consumer Bank Card, 2 Consumer Charge Card, 3 Non-Consumer Bank Card, 4 Non-Consumer Charge Card — consumer/SME × bank/charge | §0.1 (a) resolved-as-observed; empty sub-segments (charge rows) carry zero balance and zero spread |
| (h) | **Income arithmetic-verified**: income(q) = M.1 block balance × revolver share × (Prime(q) + reported spread) ÷ 4, with revolver share = "Balance of accounts with non-zero Finance charge in recent 3 month / total balance" (the sheet's own formula note) | §0.1 (b)/(c) resolved-as-observed — the balance leg is the M.1 balance, the rate leg the reported spread on Prime; §7's [INT] arrangement confirmed in the revolving-balance form (Eq A32 with the revolving balance as the income-bearing balance) |
| (i) | **Scalars observed: consumer block × 0.969 ("Credit Card"); SME block × 1.033 (the merged "C&I, noncore SME loan and card" row)** | The §11 OQ-010 SME-row question answered in the observed engine — confirmation makes it the PID |
| (j) | **FR Y-14M field codes observed**: MDSE_APR_RT (APR), OTST_EOM_AM (balance), FED_FIN_CHG_NET_AM (finance charge), LAST_12MOS_ACTV_IN (12-month activity), FED_VAR_PURCH_APR_SPRD_RT (reported spread), FED_LND_TYPE_CD (lending type) | Contract context. **Working assumption adopted 2026-08-13 (user-directed, PID-LOAN-34): the revolver share applies the 3-month finance-charge condition only — the 12-month activity field is NOT applied** [flagged: the Fed's rule has both conditions, so this is a recorded candidate divergence until the compare arbitrates] |
| (k) | `WEIGHTED_MAX_APR` **does not appear in the engine** | §0.1 (d): the cap candidate is unused-as-observed; confirm informational-only |

---

## 1. Executive summary

**What Card is.** [FACT] "Consumer credit cards are segmented into two product types: consumer bank cards, where consumers can carry a balance; and consumer charge cards, which are historically expected to be paid off by the due date, but recent charge card products allow minimum payment with accrued interest income, which are reflected in the alternative model." (PDF p. 178; md sec-159 — **SQ-25** on the final clause.) Small business cards are modeled "separately but following a similar structure" (PDF p. 179).

**How Card prices.** [FACT] "Most credit cards have variable rates and approximately 10 percent have short-term fixed rates. Since the short-term rates change in the scenario, the Board assumes that all credit card balances have variable rates." Income "depends on both the portion of balance that revolves and the interest rate"; the revolver share is estimated by account classification — "active in the last 12 months and … at least one positive finance charge in any of the last 3 months"; "Currently all firms use the Prime Rate as the benchmark index to set credit card APR, and both the interest rate and interest spread are reported in FR Y-14M. The balance-weighted interest rate, interest spread, and the Prime rate are used to determine a constant projected spread at the segment level. The prime rate from the scenario is utilized as the benchmark variable rate." (PDF pp. 178–179; md sec-159)

**What is unresolved.** The **income arrangement is implied, never printed** — no equation composes balance × revolving share × rate ([INT], §7); the **projected-spread construction lists three inputs and no formula** (**OQ-043**, filed with this brief); the revolver share's constancy is OQ-012; the SME-card scalar row is the sharpest OQ-010 retail question (0.969 vs the merged 1.033 row); and the query's income cell pair is flagged (c).

---

## 2. Card scope and boundaries

### 2.1 Position in the hierarchy

[FACT] The third retail section (PDF p. 177; md sec-156); one section covering both consumer and small business cards — hence one brief with two sub-portfolios (the Fed's own granularity).

### 2.2 Explicit boundaries

| Boundary | Source statement | Label |
|---|---|---|
| **Small business cards are IN this family; small business loans are Other Consumer** | SME cards modeled here "separately but following a similar structure" (PDF p. 179) while the non-core census lists "small business loans, SME cards" (PDF p. 177) — the census's "SME cards" naming overlaps this section's subject | [FACT] both statements; the tension is physically resolved by the M.1 wiring: the "SME cards and corporate cards" row is Card-flagged, the "Small business" row is noncore [PID-LOAN-26 — project context, not a source-side resolution] |
| **International card exposures are Other Consumer** | The non-core census has no card entry, but the M.1 international roles are uniformly "Retail - noncore" | [FACT] p. 180 census pattern + [PID-LOAN-26] physical realization |
| Corporate cards | "corporate cards" appear only in the M.1 row label "SME cards and corporate cards" — the Fed section never mentions them | [FACT of absence] source-side; physically inside the Card family via that row [PID-LOAN-26]; flagged (a) covers the empty sub-segment |
| The merged Table A8 row spans naming worlds | "C&I, noncore SME loan and card" (PDF p. 220) | [FACT]; §11, OQ-010 |

---

## 3. Card census

### 3.1 Sub-portfolios (verbatim basis)

| # | Sub-portfolio | Coding-friendly name | Source basis | Label |
|---|---|---|---|---|
| 1 | consumer bank cards | `card_consumer_bank` | "where consumers can carry a balance" (PDF p. 178) | [FACT] |
| 2 | consumer charge cards | `card_consumer_charge` | "historically expected to be paid off by the due date"; recent products' minimum-payment income "reflected in the alternative model" (PDF p. 178; SQ-25) | [FACT] |
| 3 | small business cards | `card_small_business` | "modeled … separately but following a similar structure"; "also assumed to carry variable rates"; same transactor-revolver methodology; "Segment-level data from FR Y-14M, including interest rate and spreads" (PDF p. 179) | [FACT] |

[FACT of absence] No card sub-portfolio total, no product-type grid beyond bank/charge, and no asset-classification split is stated for cards (framework §4.2 — the classification statement is mortgage-only).

### 3.2 SQ-25 — "the alternative model"

[FACT] "…recent charge card products allow minimum payment with accrued interest income, which are reflected in the alternative model." (PDF p. 178; md sec-159; page image 2026-08-12.) The referent of "the alternative model" is unstated. [INT — working reading] It is the proposed suite itself — the document introduces the proposal as "an alternative set of models" (PDF p. 173; md sec-151) — i.e., the newer charge-card products' accrued interest **is** captured by this model. An alternative reading (some unspecified model variant) cannot be excluded from the text. Filed as **SQ-25**; recorded, never corrected.

---

## 4. Rate-type treatment for Card

- [FACT] **All card balances are treated as variable-rate**: "Most credit cards have variable rates and approximately 10 percent have short-term fixed rates. Since the short-term rates change in the scenario, the Board assumes that all credit card balances have variable rates." (PDF p. 178) Small business cards "are also assumed to carry variable rates" (PDF p. 179).
- [INT — consequence] The family runs **entirely on the Equation A33 machinery** (Prime + constant spread): no A34/A35/A36/A38 leg, no wt, no new-origination window — the mirror image of auto's all-fixed assumption. The ~10 percent short-term-fixed balances are absorbed into the variable treatment by the stated assumption.
- [FACT] Benchmark: "Currently all firms use the Prime Rate as the benchmark index to set credit card APR"; "The prime rate from the scenario is utilized as the benchmark variable rate." (PDF pp. 178–179; base-rate register entry, PDF p. 181 — framework §5).

---

## 5. The revolver machinery

### 5.1 The stated rule

[FACT] "Credit card interest income depends on both the portion of balance that revolves and the interest rate. The key modeling challenge lies in estimating the percentage of balances that revolve and bear interest charges. Balances paid in full prior to the due date do not incur interest charges and therefore do not contribute to interest income. … An account is primarily classified as a revolver if it has been active in the last 12 months and has had at least one positive finance charge in any of the last 3 months. This classification is used to estimate the percentage of balances revolving and therefore earning interest income." (PDF p. 179; md sec-159)

[FACT] "The transactor-revolver methodology applied to consumer cards is similarly used to estimate the revolving balance share for small business cards." (PDF p. 179)

[FACT] **Question A156** invites alternatives to the classification ("an account could be classified as revolver if the account has finance charges observed on FR Y-14M reports", PDF p. 187; md sec-172) — the single retail-directed Board question.

### 5.2 Constancy — OQ-012

[FACT] The share is "calculated by segment and firm and used as inputs" (PDF p. 179); nothing states whether it changes over the projection. [INT, per the OQ-012 filing] Constant from the launch point, consistent with the model's constancy conventions. Physical context corroborates without resolving: the query supplies **one launch-point revolver balance per segment** [PID-LOAN-28] — a single value has no time path to vary.

### 5.3 The wholesale-located revolver-draw limitation

[FACT] "The model does not increase draws from revolvers throughout the projection" sits inside the **Wholesale Portfolio** limitations (PDF p. 186; md sec-171; wholesale §12 item 6, placement flagged as possibly loan-wide). [INT] For cards the flat-balance assumption already fixes total balances; the nearest card-side analogue is the constant revolver share (OQ-012). Recorded as a cross-reference only.

---

## 6. Data inputs and classifications to capture

| # | Item to capture | Source status | Physical realization (project context) | Notes |
|---|---|---|---|---|
| 1 | Segment-level rate and spread data | [FACT] "both the interest rate and interest spread are reported in FR Y-14M" (PDF p. 179); SME cards: "Segment-level data from FR Y-14M, including interest rate and spreads" | `WEIGHTED_AVERAGE_APR`, `WEIGHTED_SPRD` (+ `_revolver` pair) [PID-LOAN-28] | The one family whose **spread is itself a reported input** — OQ-043 on how it enters |
| 2 | Revolver share | [FACT] "percentage of balance revolving … by segment and firm" (PDF p. 179) | `TOTAL_OTST_REVOLVER ÷ TOTAL_OS` — flagged (b) | OQ-012 constancy |
| 3 | Segment balances | [FACT] common balance construction | `TOTAL_OS` (dollars); M.1 Card-flagged rows (millions) | Flagged (c): which is the Eq A32 multiplicand |
| 4 | Sub-portfolio identification | [FACT] bank/charge; SME separate | Query rows 1–4 — flagged (a) | Empty sub-segments vacuous-and-censused |
| 5 | Scenario base rate | [FACT] Prime (PDF pp. 179, 181) | `prime_rate`; MEV column TO_BE_CONFIRMED | Framework §5 |
| 6 | Floors / caps | [FACT] the common floor rule (PDF p. 180); no card statement | No floor column observed; `WEIGHTED_MAX_APR` is a **cap** candidate — flagged (d) | **OQ-002 retail leg**; a cap has no Fed counterpart |
| 7 | Industry scalar | [FACT] Table A8 rows; assignment unstated | Consumer → "Credit Card" 0.969 candidate; SME → 0.969-vs-1.033 OPEN | **OQ-010** (§11) |

[FACT of absence] No Y-14M field, aggregation rule, or as-of convention is stated; every physical entry is project context under PID-LOAN-26/28.

---

## 7. The income arrangement — [INT], recorded

[FACT] The stated ingredients: income "depends on both the portion of balance that revolves and the interest rate"; non-revolving balances "do not contribute to interest income"; the inputs are the weighted rate, the spread, and the revolving share (PDF pp. 178–179). **No equation composes them** — the retail subsections print no equations at all (framework §9 row 8).

[INT — working reading, flagged, never source-attributed] Income(t) = revolving balance × IR(t) / 4, with IR(t) = Prime(t) + constant spread (Eq A33) and the revolving balance = segment balance × revolver share, both launch-point-constant. Equivalent forms (share on the balance vs a share-scaled rate) are arithmetically identical; the workbook's cell (flagged (c)) decides the recorded form. The Eq A32 identity is preserved by reading the revolving balance as the income-bearing `loan_balance`.

**OQ-043 (filed with this brief) — the projected-spread construction.** [FACT] "The balance-weighted interest rate, interest spread, and the Prime rate are used to determine a constant projected spread at the segment level." (PDF p. 179) Three inputs, no formula: with a reported spread in hand, rate − Prime is redundant to it (up to as-of and mix effects), and the source does not say whether the projected spread **is** the reported spread, is derived as rate − Prime, or blends the two (nor which as-of Prime). The query's two spread columns (all-book and revolver-only) sharpen the physical form of the same question — flagged (e). Resolves: Fed clarification; project-side, the workbook's spread cell (candidate PID).

---

## 8. Fact-of-absence register (card)

| # | Absent for Card | Contrast / nearest statement |
|---|---|---|
| 1 | **No printed income equation** (share × balance × rate is implied) | §7 [INT]; OQ-043 |
| 2 | **No card floor statement**; the stated common rule is a floor, not a cap | PDF p. 180; `WEIGHTED_MAX_APR` cap candidate is project-side — flagged (d) |
| 3 | **No asset-classification split** for cards | Mortgage-only statement (PDF p. 177); framework §9 row 1 |
| 4 | **No promotional-rate, teaser, or 0%-APR treatment** — the ~10 % short-term fixed rates are absorbed by assumption | PDF p. 178 |
| 5 | **No corporate-card mention** in the section | M.1 row label only [PID-LOAN-26]; §2.2 |
| 6 | **No charge-card income mechanics** beyond the SQ-25 clause | PDF p. 178 |
| 7 | **No fee/interchange income treatment** (annual fees, late fees, interchange) | Interest-income scope; finance charges enter only as the revolver classifier (PDF p. 179) |

---

## 9. Inheritance register — what Card does not restate

| Rule | Governed by | Card-specific note |
|---|---|---|
| Eq A32 income identity; 9 quarters; (b,p,i,t) | common §7.0 | Read with the revolving balance as the income-bearing balance (§7 [INT]) |
| Balance construction; flat balances; same-quarter replenishment | common §6 | Multiplicand candidates = flagged (c) |
| Eq A33 variable path; spread constancy | common §7.3, §7.5 | The whole family runs here (§4 [INT]); spread construction = OQ-043 |
| Eqs A34–A38 fixed machinery | common §7.6 | **Never runs for card** (§4 [INT]) — no wt, no A36 window |
| Base rate = Prime (retail rule) | framework §5 | Stated thrice for cards (pp. 178–179, 181, 185) |
| Interest-rate floors | common §7.1; framework §8 | OQ-002 retail leg; cap candidate flagged (d) |
| Industry-scalar mechanism; Table A8 values | common §8; framework §10 | §11 — the SME row question |
| Assumptions (1)–(7); general limitations | common §12 | No card-specific assumption list exists |
| Retail Portfolio limitations | framework §12 | No card sentence in ¶2 (the family's data are comparatively rich — rate AND spread reported) |
| Quarterly compounding versus D-004 | common §7.7 | Unresolved at project level |
| Hedge exclusion (Question A159) | common §11 | OQ-005 |

---

## 10. Board questions touching Card

- **A156** — the single retail-directed question, and it is card-owned: revolver-classification alternatives (verbatim in common §13; §5.1).
- **A154**, **A157**, **A158**, **A160** — inherited.

---

## 11. Table A8 rows touching Card

[FACT] **"Credit Card" = 0.969** (PDF p. 220); footnote 63 lists "consumer credit card" as its own category AND places "small and median business loans and card" with corporate & investment — the pair Table A8 merges into **"C&I, noncore SME loan and card" = 1.033** (SQ-11; PDF p. 184 footer).

**OQ-010 retail leg — the sharpest instance:** consumer cards → "Credit Card" 0.969 is the natural (inferred) pairing, but **small business cards** sit between two rows by the Board's own naming — "consumer credit card" excludes them, and footnote 63 files "small and median business … card" under the merged C&I row. Whether the SME sub-portfolio multiplies 0.969 or 1.033 is unstated and materially different. Candidate PID at the gate (the workbook's results blocks will show it); [CODE] config map, unmapped hard error.

---

## 12. Coding considerations — [CODE], non-normative

- **All-variable family:** engine assignment fixed to A33 in config; no wt/A36 code path for card (assert, don't silently skip).
- **Query loader:** numbered-row segment mapping as declared config (flagged (a)); empty sub-segments vacuous-and-censused; percent-unit scales D-006 TO CONFIRM (APR/spread percent vs decimal — refuse when undeclared); revolver share derived at load with both balances retained for the census (flagged (b)).
- **Income construction as configuration** until the cell is read: {balance source: M.1 flag-sum vs query `TOTAL_OS`} × {rate leg: Prime + `WEIGHTED_SPRD` vs Prime + `WEIGHTED_SPRD_revolver` vs APR-seeded} — one switch, censused, so flagged (c)/OQ-043 stay visible (the PID-LOAN-22/23 lesson: the workbook's cells decide).
- **Cap logic only if confirmed** (flagged (d)) — never apply `WEIGHTED_MAX_APR` speculatively; if adopted, record as its own PID with a bind census (floors lesson, PID-SEC-18).
- **M.1 reconciliation monitor:** query totals vs the "Card (dom)" flag-sum (bank + charge + SME-and-corporate rows) — consistency census, not identity.

---

## 13. Open questions

| ID | Status | Relevance to this brief |
|---|---|---|
| **OQ-043** | OPEN — **filed 2026-08-12 with this brief** | Projected-spread construction: three stated inputs, no formula; reported spread vs rate − Prime; physical form = flagged (c)/(e) (§7) |
| **OQ-012** | OPEN (minor) | Revolver-share constancy; single launch-point value observed — corroborates, does not resolve (§5.2) |
| **OQ-002** | OPEN for retail | No card floor; the observed `WEIGHTED_MAX_APR` is a cap candidate with no Fed counterpart (§8 row 2) |
| **OQ-010** | OPEN for retail — sharpest here | SME cards: 0.969 vs the merged 1.033 row (§11) |
| **OQ-033** | OPEN | "by segment and firm" (p. 179) already in the evidence set; card runs no fixed machinery, so the A36 leg is moot for this family |
| OQ-040 / OQ-041 / OQ-042 | OPEN — other-family-owned | Boundaries only |

---

## 14. Source traceability table

| # | Claim / element | Class | PDF p. | md anchor | Verification |
|---|---|---|---|---|---|
| 1 | Bank/charge card census; the "alternative model" clause | FACT (**SQ-25**) | 178 | sec-159 | Page image 2026-08-12 |
| 2 | ~10 % short-term fixed; all balances treated variable | FACT | 178 | sec-159 | Page image 2026-08-12 |
| 3 | Income depends on revolving portion × rate; paid-in-full balances earn nothing | FACT | 179 | sec-159 | Page image 2026-08-12 |
| 4 | Revolver classification (12-month active + finance charge in last 3) | FACT | 179 | sec-159 | Page image 2026-08-12 |
| 5 | Prime as APR benchmark; rate AND spread reported in Y-14M; three-input constant projected spread | FACT | 179 | sec-159 | Page image 2026-08-12; **OQ-043** |
| 6 | Small business cards separate-similar; same transactor-revolver method; Y-14M segment data | FACT | 179 | sec-159 | Page image 2026-08-12 |
| 7 | Prime base-rate register entry incl. "small business credit cards" | FACT | 181 | sec-163 | Page image 2026-07-30 |
| 8 | Question A156 (revolver alternatives) | FACT | 187 | sec-172 | Page image 2026-07-30 |
| 9 | Table A8 "Credit Card" 0.969; merged "C&I, noncore SME loan and card" 1.033; footnote 63 categories | FACT | 220, 184 | sec-209, md 5354 | Page images 2026-07-16 / 2026-08-03; OQ-010 |
| 10 | Revolver-draw limitation is wholesale-located | FACT | 186 | sec-171 | Page image 2026-07-30; §5.3 |
| 11 | PID-LOAN-26 / PID-LOAN-28 (M.1 wiring; Card query contract) | **PID** | — | — | User-supplied 2026-08-12; flagged observations (a)–(e) await the gate |

---

### Brief completion checklist

- [x] Status banner present; no adoption language anywhere.
- [x] Every material statement labeled; the income arrangement carried as [INT] with its basis; no firm values.
- [x] **Zero verbatim equation blocks** (D-010(b)).
- [x] All four card paragraphs verified against page images (2026-08-12); SQ-25 filed verbatim, never corrected.
- [x] Consumer and small business cards as two sub-portfolios in one brief — the Fed's own section granularity.
- [x] Retail-shared rules cited from the framework brief; the small-business-loans boundary recorded with its physical resolution labeled PID, never source-attributed.
- [x] No production Python; no confidential values, formulas, or firm data — logical contract only.
- [ ] Review state: DRAFT — awaiting user review gate (combined retail gate).

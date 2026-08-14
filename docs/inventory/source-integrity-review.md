# Source-Integrity Review — Fed PPNR Model Documentation (Proposed 2026 Net-Interest Scope)

**Deliverable 1 of Phase 1, Task 1.** Review date: 2026-07-16.
**Status of the reviewed methodology: PROPOSED for the 2026 stress test — out for public comment, NOT adopted.**

Purpose: establish whether the Markdown conversion is a faithful working copy of the authoritative PDF for the Phase 1 scope (Section B.v intro through v.e, PDF pp. 167–234, plus the Revisions section, pp. 4–5), and log every defect found — separating conversion artifacts (Markdown-only) from quirks present in the Fed's published PDF itself.

## 1. Files under review

| File | Size | Content | SHA-256 |
|---|---|---|---|
| `sources/fed/pre-provision-net-revenue-models.pdf` | 1,566,932 bytes, 255 pages | Authoritative source | `e7908fee59510ee265bdb462f91299abe5f55f6ee6545af0ae0a8582cfafb7f3` |
| `sources/fed/pre-provision-net-revenue-models.md` | 505,427 bytes, 5,375 lines | Searchable working copy | `38043f7ce0a3ac79319094fb37327a647535eb1e08a1cf3f6a4d70142028a49f` |

Document identity (verified from PDF metadata and page 1): *Supervisory Stress Test Model Documentation — Pre-Provision Net Revenue (PPNR) Model, October 2025 — Updated December 2025*. The Markdown is the **December 2025 updated version** (all December revision items present; see §3).

If either checksum changes, this review is void and must be rerun.

## 2. Page-numbering and navigation conventions (verified)

- **Printed page number = PDF sheet number, 1:1.** Verified on every page opened (pp. 4–5, 167–169, 173–175, 181–184, 189–191, 193, 196, 201, 206–207, 209–217, 219–220, 222, 225–226, 230–231, 234–235): the folio printed in the page header matches the PDF sheet index. All page citations in this project use this single number.
- **`<!-- page N -->` markers** mark the point where page N begins (a page break). 254 such markers, numbered continuously 1–255 with one gap: no `<!-- page 3 -->` (see CA-3).
- **`<!-- Source PDF page N -->` markers** accompany section starts, immediately before `<a id="sec-N"></a>` anchors (236 anchors in the file).
- **Citation format for all project deliverables:** `(PDF p. N; md sec-M)` or, where a heading has no anchor, `(PDF p. N; md line L)`.

## 3. December 2025 revision reconciliation (PDF pp. 4–5)

The Revisions section (verified against PDF pp. 4–5; md lines 262–291) lists 13 items. Status of each in the Markdown:

| # | Revision item (PDF pp. 4–5) | Status in md | Verified against PDF page |
|---|---|---|---|
| 1 | pp. 168–169: four-model-types paragraph + Table A6 added | Present (md 3337–3370) | Yes (pp. 168–169) |
| 2 | p. 175: Wholesale wording — "two parts", colon; Corporate pluralization; extraneous symbols removed | Present (md 3473, 3481) | Yes (p. 175) |
| 3 | p. 180: period added under "Projected Interest Income Rate" | Present (md 3560) | md only (trivial) |
| 4 | p. 209: "end of quarter" → "average" (domestic time deposits) | Present (md 4125) | Yes (p. 209) |
| 5 | p. 214: "end of quarter" → "average"; "FR Y-9C" → "FR Y-14Q"; subsection (a.) → (b); "contradicts" → "abstracts from" | Present (md 4246, 4250–4258) | Yes (p. 214) |
| 6 | p. 215: Questions subsection (b) → (c) | Present (md 4263–4265) | Yes (p. 215) |
| 7 | p. 216: "federal funds sold" → "federal funds purchased" | Present (md 4318–4329) | Yes (pp. 216–217) |
| 8 | pp. 219–220: "Estimated Parameters for Proposed Structural Models" added | Present (md 4374–4405) | Yes (pp. 219–220) |
| 9 | p. 234: "Estimated Parameters for Proposed Regression Models" added | Present (md 4707–4718) | Yes (p. 234) |
| 10 | p. 237: "asset servicing" → "investment servicing" | Not checked — outside Phase 1 scope (noninterest income) | No |
| 11 | pp. 240, 243: Equations A56/A57/A64 URQ wording | Not checked — outside Phase 1 scope | No |
| 12 | p. 243: Equation A64 Treasury10y wording | Not checked — outside Phase 1 scope | No |
| 13 | pp. 251–255: NII/expense parameters section added | Heading present (md 5179); content outside Phase 1 scope | No |

**Conclusion: the Markdown reflects the December 2025 update for the entire net-interest scope.**

## 4. Equation verification register (all in-scope equations, verified against PDF page images, 2026-07-16)

| Eq. | Title (abbreviated) | PDF p. | md lines | Verdict | Notes |
|---|---|---|---|---|---|
| A32 | Interest Income on Loans Projection | 173 | 3439–3441 | Verified | — |
| A33 | Variable-Rate Products Interest Rate Projection | 181 | 3571–3579 | Verified | — |
| A34 | Fixed-Rate Products Interest Rate Projection | 182 | 3610–3612 | Verified | — |
| A35 | Origination Interest Rates Projection | 182 | 3616–3618 | Verified | — |
| A36 | Spread for Fixed-Rate Projection | 182 | 3622–3624 | Verified | — |
| A37 | Spread for Wholesale Projection | 182 | 3628–3630 | Verified | Source typography quirk SQ-6 |
| A38 | Projected Fixed-Rate Interest Rate | 183 | 3638–3640 | Verified | LHS naming quirk SQ-7 |
| A39 | Interest Income on Deposits with Banks and Other | 189 | 3780–3792 | Verified | Incl. projection restatement F(b,q) |
| A40 | Interest Income on U.S. Treasuries Projection | 191 | 3838–3846 | Verified | Accretion uses t=0 face/cost over maturity-in-quarters(t=0) |
| A41 | Interest Income on MBS Projection | 196 | 3912–3920 | Verified | Accretion uses t-dated face/cost over 4 × WAL(t=0) |
| A42 | Interest Income on Other Securities Projection | 201 | 3997–4004 | Verified | Source spelling quirk SQ-8 ("Accrection") |
| A43 | Interest Income on Other Interest/Dividend-Bearing Assets | 207 | 4080–4093 | Verified | Incl. projection restatement and constant α |
| A44 | Interest Expense on Domestic Time Deposits Rate Projection | 209 | 4135–4145 | Verified | ρ ≡ 1/WAL; line items 42E, 71 verified |
| A45 | Other Domestic Deposits Rate, ELB Period | 212 | 4194–4209 | Verified | Source typo SQ-9 ("indicats") |
| A46 | Other Domestic Deposits Rate, Non-ELB Period | 213 | 4215–4231 | Verified | Betas/line items 42B–42D, 79A–81B verified |
| A47 | Other Domestic Deposits Rate Aggregation | 213 | 4235–4242 | Verified | — |
| A48 | Interest Expense on Fed Funds Purchased & Repo | 217 | 4333–4343 | Verified | Source caption typo SQ-10; md stray pipe CA-2f |
| A49 | Hedge Impact Projection | 222 | 4431–4439 | Verified | — |
| A50 | Accrued Interest, Fixed Leg | 222 | 4443–4450 | Verified | N/360 day count |
| A51 | Accrued Interest, Floating Leg | 222 | 4454–4462 | Verified | — |
| A52 | Net II on Trading Assets & Liabilities Regression | 225–226 | 4545–4556 | Verified | — |
| A53(1)/(2) | Interest Expense on Other Borrowing Regression | 230–231 | 4626–4662 | Verified | Incl. projection restatement with B(b,0) |

**No numerical, symbolic, or structural conversion damage was found in any in-scope equation.**

## 5. Table verification register

| Table | Content | PDF pp. | md lines | Verdict | Notes |
|---|---|---|---|---|---|
| A6 | PPNR components → proposed model types (23 components) | 168–169 | 3339–3370 | Verified — all rows/values match | md caption has stray pipe (CA-2a) |
| A7 | Median betas, proposed deposit models | 219 | 4378–4391 | Verified — all 10 beta values match | Down-row labels are internal variable names **in the PDF itself** (SQ-1) |
| A8 | Industry scalars, proposed loans model | 220 | 4395–4405 | Verified — all 7 values match | 7 rows vs. footnote 63's 8 categories (SQ-11) |
| A9 | Estimated parameters, proposed regression models | 234 | 4711–4718 | Verified — all coefficients/significance match | Firm fixed-effect estimates explicitly **not included** in the table (source statement, md 4709) |

Table A7 values (verified): MMA up 0.620 / down 0.645; Savings up 0.310 / down 0.335; Other transaction up 0.465 / down 0.490; Foreign non-time up 0.890 / down 0.790; Foreign time up 1.000 / down 1.000.
Table A8 values (verified): Auto 0.865; C&I, noncore SME loan and card 1.033; Credit Card 0.969; Domestic CRE 1.081; Mortgage 1.014; Noncore 1.072; Rest of wholesale 1.113.
Table A9 values (verified): trading NII — 3M Treasury 0.278***; other borrowing — BBB 0.254**, CP share −0.036***, subdebt share 0.066**; firm fixed effects "Yes" (values not disclosed).

## 6. Footnote verification (in-scope footnotes 61–66)

| Fn. | PDF p. | md line | Verdict | Notes |
|---|---|---|---|---|
| 61 | 175 | 5350 | Verified | Wholesale FR Y-14Q data is facility-level; document says "loan level" for readability |
| 62 | 175 | 5352 | Verified | FR Y-14Q variability value for variable-rate is "floating" |
| 63 | 184 | 5354 | Verified | Lists 8 scalar categories (see SQ-11) |
| 64 | 193 | 5356 | Verified | "*See* Securities Model Description." |
| 65 | 196 | 5358 | Verified | Vendor-model macro variables → Securities Model Description |
| 66 | 206 | 5360 | Verified with defect | PDF footnote ends at "…10-year Treasury yield."; md has Table A9's "Notes:" sentence glued on (CA-1) |

## 7. Conversion-artifact log (defects in the Markdown only; PDF is clean at these points)

The Markdown source file is read-only; none of these are corrected in place. Apply the corrected reading below when quoting.

| ID | md location | Defect | Corrected reading (per PDF) | Severity |
|---|---|---|---|---|
| CA-1 | line 5360 (footnote 66) | Sentence "Notes: Statistical significance levels…" appended to footnote 66 | Footnote 66 ends at "…the 10-year Treasury yield." The Notes sentence belongs to Table A9 (p. 234) and already appears correctly at md 4718 | Low |
| CA-2a | line 3339 | Stray `\|` at end of Table A6 caption | No pipe in PDF caption | Trivial |
| CA-2b | line 3450 | Stray `\|` after "*t = projection quarter*" | No pipe in PDF (p. 174) | Trivial |
| CA-2c/d/e | lines 3854, 3933, 4013 | Stray `\|` after "…will be zero." (three securities hedge paragraphs) | No pipe in PDF (pp. 192, 197, 203) | Trivial |
| CA-2f | line 4333 | Stray `\|` at end of Equation A48 caption | No pipe in PDF (p. 217) | Trivial |
| CA-2g | line 4645 | "at time\| *t*" | "at time *t*" (PDF p. 231) | Trivial |
| CA-2h | line 4646 | "credit spread;\|" | "credit spread;" (PDF p. 231) | Trivial |
| CA-3 | line 11 → 256 | No `<!-- page 3 -->` marker | Page 3 (TOC continuation) is covered by the `<!-- Source PDF page 3 -->` marker at line 15; no content loss | Trivial |
| CA-4 | lines 3999, 4003 | md carries the A42 "AccrectionAmortization" typo in **both** the main equation line and the where-list | The PDF (p. 201) has the typo in the **main equation line only**; the where-list is spelled correctly — settled 2026-07-23 by a text-layer glyph-count check (equation objects defeat image reading and plain extraction: each letter maps to the word's doubled first glyph, so letter counts distinguish the 21- vs 22-letter spellings). The md where-list therefore deviates from the PDF; quote each spot per the PDF | Trivial; discovered at the `ii_other_sec` chapter review |
| CA-4 | lines 3210, 4664 | Two headings lack `<a id="sec-N">` anchors: "(a.) Assumptions and Limitations" (iv.n(1)) and "(a.) Variable Selection" (v.d(2)) | Cite these by md line number | Trivial |

**No conversion artifact affects any numerical value, equation term, or table entry in scope.**

## 8. Source-document quirk log (present in the Fed's published PDF; record verbatim, never silently correct)

| ID | PDF p. | Quirk (SOURCE-STATED, verbatim) | INTERPRETATION (labeled as such) |
|---|---|---|---|
| SQ-1 | 219 | Table A7 "Down" rows show internal parameter names in the Deposit Type column: `median_beta_dom_mma_deposit_down`, `median_beta_dom_savings_deposit_down`, `median_beta_dom_other_trans_deposit_down`, `median_beta_for_nontime_deposit_down`, `median_beta_for_time_deposit_down` | Each Down row belongs to the deposit type of the preceding Up row; the embedded names self-identify (dom_mma, dom_savings, dom_other_trans, for_nontime, for_time). High confidence |
| SQ-2 | 219 | Table A7 caption cites "(Equations A46)" | The betas enter Equation A46; the same parameters serve the foreign-deposits model (which reuses A45–A47 by reference, PDF p. 215) |
| SQ-3 | 190, 194 | Question numbers A161 and A162 are each used twice — under v.a(2) (deposits with banks) and v.a(3) (U.S. Treasuries). Only duplicates in the document (verified by full-document scan) | Numbering error in source; disambiguate citations by section |
| SQ-4 | 190, 211 | Questions intro under v.a(2) says "…model for interest income on loans"; intro under v.a(7) says "…model for interest income on domestic time deposits" (an expense model) | Copy-paste errors in source; the questions themselves name the correct components |
| SQ-5 | 175 | "Data used in the segmentation of wholesale balances are sourced from FR." — sentence truncated before footnote 61 | Intended reference is FR Y-14Q (footnote 61 discusses wholesale FR Y-14Q data; December revision removed "extraneous symbols" here and the truncation remained). See OQ-015 |
| SQ-6 | 182 | Equation A37 typesets "balance_weighted avg IIR" with "weighted" as a subscript of "balance" | Reads as "balance-weighted average interest income rate" |
| SQ-7 | 183 | Equation A38's left-hand side is named IR_existing though it defines the blended (existing + new-origination) fixed-rate path | Surrounding text (PDF p. 183) confirms the blend intent; treat LHS as the updated portfolio fixed rate |
| SQ-8 | 201 | Equation A42's **main equation line** spells "AccrectionAmortization" — **refined 2026-07-23**: the where-list on the same page is spelled correctly (text-layer glyph-count check; see CA-4 for the md's deviation) | "AccretionAmortization" (spelled correctly in A40/A41 — re-confirmed via the same text-layer check, and in A42's own where-list) |
| SQ-9 | 212 | "t indicats the quarter" in Equation A45 where-list | "indicates" |
| SQ-10 | 217 | Equation A48 caption: "…Securities Sold under the Agreement to **Purchase**" | "…to Repurchase" (correct in the section heading, PDF p. 216) |
| SQ-11 | 184 vs. 220 | Footnote 63 lists 8 industry-scalar categories ("mortgage, auto, corporate & investment, small and median business loans and card, domestic CRE, consumer credit card, one category for rest of consumer loans, and one for rest of wholesale exposures"); Table A8 has 7 rows | Table A8's "C&I, noncore SME loan and card" appears to merge footnote 63's "corporate & investment" and "small and median business loans and card"; "median" likely intends "medium". Logged as OQ-010 |
| SQ-12 | 214 | Two consecutive assumptions both labeled "A third assumption" | The second should be a fourth assumption |
| SQ-13 | 231 | Subsection label "(a.) Variable Selection" follows "(a) Model Description" in v.d(2) | Labeling quirk (same "(a.)" style appears in current-suite iv.n(1), p. 162) |
| SQ-14 | 2 vs. 167 | Page 2 says the Board "intends to use" this PPNR model in the 2026 test; Section v (p. 167) and the B intro (p. 6) say the Board "is proposing" the new suite and seeks public input on both suites | Per project rules, all deliverables state the Section v suite is **proposed, not adopted**; do not rely on the page 2 phrasing |
| SQ-15 | 212 | "The firm-specific spread to the 3-month Treasury yield is empirically estimated as the average distance between the deposit rate paid by the firm during the most recent effective lower-bound period." — "between …" lacks its second endpoint | Omitted endpoint = "and the 3-month Treasury yield", per the sentence's own subject and the Eq A45 where-list (high confidence). Raised in the `ie_other_dom_dep`/`ie_foreign_dep` chapter reviews; filed at the liability-side integration gate 2026-07-17. See OQ-017 |
| SQ-16 | 216–217 | v.a(10): "the liabilities reported in line items 44A ('federal funds purchased') and 44B ('securities sold under agreements to repurchase') of the Net Interest Income Worksheet of FR Y-14Q, Schedule G" — 44A/44B are Schedule G liability *rate* items | Balance items are 36A/36B per PID-FFR-1 (user-confirmed project mapping, never a Fed statement). Also fixes the direction of the 44B double use with v.a(9) (44B = foreign-deposits–time rate item, p. 215): v.a(10)'s balance usage is the misname. Filed 2026-07-17. See OQ-019 |
| SQ-17 | 231 | Eq A53 where-list: "the sum of other short-term, borrowing, subordinated debt, and other interest-bearing liabilities" — comma inside "other short-term, borrowing", present in the PDF page image (not a conversion artifact) | Read as "other short-term borrowing" (line-break typo). Raised in the `ie_other_borrowing` chapter review; filed 2026-07-17 |
| SQ-18 | 182–183 | Equations A34, A35, A36, and A38 print no firm subscript b (A38's weight is wt_(p,i,t)), while Equations A33 and A37 include b and the fixed-rate prose states "the balance-weighted origination rate by firm, product, and segment at jump-off" (p. 182) | Working reading: notational abbreviation — the fixed-rate machinery is firm-level per the prose and the A33/A37 pattern. Filed 2026-07-30 at the loans workstream (slice 1). See OQ-033 |
| SQ-19 | 186 vs. 175 | Wholesale Portfolio limitations write "domestic farm loans, and international farm loans" where the Corporate portfolio list has "domestic farmland loans" and "international farmland loans" | Same portfolios; source-internal naming variant (cf. the SQ-10/agreements precedent) — recorded, never corrected. Filed 2026-07-30 |
| SQ-20 | 181 | Equation A33's where-list describes BaseRate_(p,i,t) as "the scenario base rate at quarter *t for product p*" — the segment subscript i goes unmentioned | Base rates are assigned at the product/segment level per the base-rate assumptions on the same page; no per-firm base rate exists (no b in the subscript). Filed 2026-07-30 |
| SQ-21 | 176 | "Currently, the FR Y-14Q Schedule H.1 schedule is able to identify NPMLs." — "Schedule … schedule" doubled; present in the PDF page image (not a conversion artifact) | Read as "the FR Y-14Q Schedule H.1". Filed 2026-08-03 at the Corporate brief |
| SQ-22 | 175 vs. 176 | Owner-occupancy naming varies between the two wholesale sections: Corporate prints "domestic owner-occupied CRE loans" / "international owner-occupied CRE loans" (hyphenated, abbreviated), while CRE prints "domestic non-owner occupied commercial real estate loans" / "international non-owner occupied commercial real estate loans" (unhyphenated, spelled out) | Cosmetic variants of the same owner-occupancy dimension — the substantive split (owner-occupied → Corporate; non-owner-occupied → CRE) is unaffected. Both verified on page images 2026-08-03. Filed 2026-08-03 |
| SQ-23 | 182 vs. 181, 185 | The fixed-rate spread paragraph states "The base rate applied is the same as the base rate for floating: **the Prime Rate for retail** and the three-month Treasury yield for wholesale" — naming Prime as *the* retail base rate, while the base-rate assumptions on the facing page assign the mortgage rate to adjustable-rate mortgage products (p. 181) and the Retail Portfolio limitations state "all retail products **(except for mortgages)** use Prime Rate" (p. 185) | The sentence abbreviates away the mortgage exception; the exception governs — mortgage-family spreads measure against the mortgage rate, all other retail against Prime. The FRM/fixed-HEL new-origination boundary within that reading is OQ-040. Filed 2026-08-12 at the retail framework brief |
| SQ-24 | 185 | Retail Portfolio limitations: "There is no interest rate information for most non-core **retails** products…" — plural "retails"; present in the PDF page image (not a conversion artifact) | Read as "retail products". Filed 2026-08-12 at the retail framework brief |
| SQ-25 | 178 | Card section: "…recent charge card products allow minimum payment with accrued interest income, which are reflected in **the alternative model**." — the referent of "the alternative model" is unstated | Working reading: the proposed suite itself — the document introduces the proposal as "an alternative set of models" (p. 173), so the newer charge-card products' accrued interest IS captured by this model; a narrower reading (an unspecified model variant) cannot be excluded. Filed 2026-08-12 at the card brief |
| SQ-26 | 225–226 | Equation A52's where-list defines only Treasury3m(t), α_b, and ε(b,t) — **the dependent variable Ratio(b,t) is not defined in the where-list** (its definition lives in the section prose: net quantity ÷ net trading assets, with the ÷4 numerator build). Contrast: the current-suite counterpart Eq A8 defines its Ratio inside its where-list (p. 66, image-verified) | The prose definition governs (p. 225); the ratio's **units** are additionally never stated — the quarterly-ratio reading (numerator is stated quarterly dollars) is an interpretation carried in the `nii_trading_al` chapter §5 with its basis. Filed 2026-08-13 at the trading-NII chapter |
| SQ-27 | 96 vs. 168–169, 231 | Current-suite iv.i(4) reorganization paragraph: "The Board also proposes to model the remaining subset … as interest expense on other borrowing jointly with interest expense on subordinated debt **using a structural approach**"; Question A66 likewise says "the alternative structural approach" — while Table A6 classifies the proposed other-borrowing model **Regression** (pp. 168–169) and v.d(2) states it is "estimated using ordinary least squares" (p. 231). Both p. 96 phrasings present in the PDF page image (not conversion artifacts) | Source-internal inconsistency; the proposed-suite sections govern — the other-borrowing successor is the Eq A53 OLS regression (model #12), exactly as built. Filed 2026-08-13 at the trading-NII chapter drafting; cross-referenced at inventory #11 and #12 |

## 9. Verification coverage and residual items

- **PDF pages visually verified (33):** 4–5, 167–169, 173–175, 181–184, 189–191, 193, 196, 201, 206–207, 209–217, 219–220, 222, 225–226, 230–231, 234–235.
- **Verified in full:** every in-scope equation (A32–A53), every in-scope table (A6–A9), footnotes 61–66, all December-revision items within scope, the Section v start boundary (p. 167) and end boundary (v.f begins p. 235).
- **Not verified (accepted residual):** current-suite sections B.i–iv beyond the heading census (BACKGROUND/COMPARISON use only — verify on demand when a chapter cites them); out-of-scope December-revision items (pp. 237, 240, 243, 251–255); footnotes 1–60 (outside scope).
- **Chapter-review re-verification (2026-07-17):** pp. 209–219 and 230–234 re-read as page images during the five liability-side chapter reviews; no new conversion defects found; source quirks SQ-15–SQ-17 added at the liability-side integration gate. Two duplicate filings were prevented at integration: the Equation A48 title typo was already logged as SQ-10, and the md stray pipes at lines 4645–4646 were already logged as CA-2g/CA-2h.
- **Chapter-review re-verification (2026-07-23):** pp. 188–190 and 205–208 re-read as page images during the two asset-side calculator chapter reviews (`ii_dep_banks_other`, `ii_other_ida`); no new conversion defects found. Confirmations: the SQ-4 v.a(2) Questions-intro misnomer ("interest income on loans", p. 190) is present in the PDF itself; the CA-1 footnote-66 glue is md-only (the authoritative footnote ends at "…the 10-year Treasury yield.", p. 206); Equation A43's display carries no time subscript on the Treasury terms while its projection form does — both faithful in the md.
- **Chapter-review re-verification (2026-07-23, securities):** pp. 191–193, 196–198, and 201–203 re-read as page images during the three securities chapter reviews (`ii_ust`, `ii_mbs`, `ii_other_sec`). New method: equation-object spelling settled via **PDF text-layer glyph counts** (the extraction doubles each letter as the word's first glyph, so letter counts distinguish spellings). Outcomes: A40/A41 "AccretionAmortization" correct (SQ-8 stays A42-only); **SQ-8 refined** (A42 typo confined to the main equation line); **CA-4 filed** (md typo'd A42's where-list too); A40 prints "Maturity in Quarter" (singular) — benign source notation, preserved verbatim; CA-2c/d/e stray pipes re-confirmed md-only (pp. 192, 197, 203 clean); the v.a(4) reinvestment paragraph lacks the "For additional details…" referral sentence present in v.a(3)/v.a(5) (faithful source difference, recorded in the `ii_mbs` chapter).
- **Source-brief re-verification (2026-08-03, loans slice 2 — Corporate):** pp. 175–176 and 220 re-read as page images at high zoom during the Corporate source-brief drafting. Confirmations: the 11-portfolio enumeration is complete with numbering intact (no dropped or merged item); the mixed-rate/demand and fee-only sentences; the NPML paragraph, including that the variable-rate conclusion names **only** loans for purchasing and carrying securities (OQ-036); footnote 62's "floating"; Table A8's seven rows and values, with the row label "C&I, noncore SME loan and card" confirmed verbatim. Source quirks **SQ-21** ("Schedule H.1 schedule" doubling, p. 176) and **SQ-22** (owner-occupancy naming variants across pp. 175–176) added. New open questions OQ-036–OQ-038 filed. No conversion defects: the Markdown matched the page images for every Corporate sentence.
- **Source-brief re-verification (2026-07-30, loans slice 1):** pp. 173–188 read as page images **in full** during the loans common/wholesale source-brief drafting — the first complete image pass over the loans prose (the initial 2026-07-16 set covered pp. 173–175 and 181–184 plus every equation, table, and in-scope footnote). No new conversion defects found; CA-2b re-confirmed md-only (p. 174 clean); SQ-5, SQ-6, SQ-7 and footnote 63's "median" wording re-confirmed present in the PDF itself. Source quirks **SQ-18–SQ-20 added**: the fixed-rate equations' b-subscript omission (OQ-033); the "farm"/"farmland" naming variant (pp. 186 vs. 175); the A33 where-list's unmentioned segment subscript. New open questions OQ-033–OQ-035 filed in `docs/handbook/open-questions.md`.
- **Source-brief re-verification (2026-08-12, loans slice 3 — CRE):** pp. 176–177 re-read as page images **at high zoom** during the CRE source-brief drafting — the six-item CRE loan-type enumeration confirmed complete with numbering intact (including "(also referred to as portfolios) as defined in FR Y-9C"), and the p. 177 sentence "the total number of CRE segments is 24" exact; pp. 183 and 187 re-read as page images the same day (the "CRE income-producing loans" sentence and Question A153 confirmed verbatim). **Full-document absence searches** (2026-08-12): "H.2"/"Schedule H.2" — **zero occurrences anywhere** (grounds the new **OQ-039**: the suite-level data list on p. 172 names Schedules G/B/M and FR Y-14M only, and Schedule H.1 appears solely in the Corporate NPML paragraph, p. 176); "committed", "undrawn", "workout" — zero occurrences; "renewal" — hedge-section hits only (pp. 221–223); "income-producing" — exactly one occurrence (p. 183); "multifamily" and CRE-sense "construction" — only in the p. 176 enumeration. No new conversion defects; **no new source quirks** (the "(also referred to as portfolios)" vs. "(referenced as a portfolio)" phrasing variation across pp. 175–176 is recorded in the CRE brief §3.1 as cosmetic, not filed). OQ-039 filed in `docs/handbook/open-questions.md`.
- **Source-brief re-verification (2026-08-12, retail slice R1 — framework + Auto):** pp. 177–180 read as page images during the retail scoping and drafting session — the four-section retail census, the Mortgage/Auto/Card/Other-Consumer subsections (including the revolver-classification rule and the p. 180 non-core product census), and the sec-161 boundary all confirmed; **the Markdown matched the page images for every retail sentence — no conversion defects**. The PDF's own spelling "heterogenous" (p. 179–180, "a heterogenous category") preserved as-is, not filed (legitimate spelling variant, no ambiguity). p. 185 re-read **at high zoom** (the Retail Portfolio limitations — this slice's load-bearing base-rate sentence confirmed verbatim). Source quirks **SQ-23** (p. 182's "the Prime Rate for retail" abbreviates away the mortgage exception) and **SQ-24** ("non-core retails products", p. 185) added. Recorded contrast, no quirk filed: the suite-level schedule list (p. 172) omits **Schedule A** while the auto subsection names "FR Y-14Q schedule A.2" directly (the polarity mirror of OQ-039's H.2 finding — the schedule *is* named for auto, so no gap arises); also noted, p. 185's "non-purpose loans" vs p. 180's "non-purpose lending" (same category, minor variance, framework brief §12). New open questions **OQ-040–OQ-042** filed in `docs/handbook/open-questions.md`; OQ-033's evidence appended (retail prose states the firm dimension four times).
- **Chapter-drafting re-verification (2026-08-13, Increment 4 — trading NII):** pp. 225–230 read as page images **in full** during the `nii_trading_al` chapter drafting — the **first image pass over pp. 227–229** (225–226 and 230 re-confirmed) — and p. 234 re-read (Table A9 row re-confirmed: trading NII 3M-Treasury 0.278***; empty BBB/CP/subdebt cells; firm fixed-effects "Yes"; Notes sentence). Confirmed facts of absence on the images: v.d(1) states **no projection mechanics** (no ratio→dollar step, no balance basis, no launch-point language — OQ-007) and **no estimation-window dates** ("relatively long time period", pp. 226/228 — contrast v.d(2)'s stated 2020:Q2–2021:Q4). Comparison pages read as page images the same day (**first current-suite image verification**, per the §9 verify-on-demand rule): pp. 65–68 (iv.g — Eq A8 and its where-list incl. the Ratio definition; footnotes 23/24 naming FR Y-9C BHCK4069/BHCK3545; the p. 68 net-model forward reference; Question A32) and p. 96 (the iv.i(4) reorganization paragraph and Question A66). **No conversion defects found anywhere checked — the md matched the images sentence-for-sentence.** Source quirks **SQ-26** (A52 where-list omits its dependent variable) and **SQ-27** (p. 96/A66 "structural approach" vs the Regression classification) added. Current-suite pp. 65–68 and 96 are now image-verified; the rest of iv.g/iv.i(4) (pp. 90–95, 97) remains verify-on-demand.
- **Source-brief re-verification (2026-08-12, retail wave 2 — Mortgage/Card/Other-Consumer briefs, same day):** pp. 177–180 already image-verified in the R1 pass; the mortgage (pp. 177–178), card (pp. 178–179), and other-consumer (pp. 179–180) subsections re-read against those images during drafting — all verbatim quotes confirmed. Source quirk **SQ-25** added ("the alternative model", p. 178 — referent unstated). New open question **OQ-043** filed (the card projected-spread sentence lists three inputs — balance-weighted interest rate, interest spread, Prime — and states no formula; the only spread construction in the loan model given as ingredients rather than a rule). Physical input contracts received the same day (M.1 retail wiring; Mortgage query; Card query) are recorded as **PID-LOAN-26/27/28** in `docs/handbook/open-questions.md` — project context, never source findings; no firm values enter this repository.

## 10. Fitness conclusion

The Markdown conversion is **faithful for the entire Phase 1 net-interest scope**: no equation, table value, or line-item reference was damaged in conversion. All defects found are either trivial markup artifacts (§7) or quirks present in the Fed's own PDF (§8). The Markdown is approved as the primary searchable working source, with the PDF remaining authoritative and the §7 corrected readings applied when quoting. Material claims in downstream deliverables must cite `(PDF p. N; md sec-M)`.

## 11. Second source collected (2026-07-23) — Market Risk Models volume (OQ-004)

| File | Size | Content | SHA-256 |
|---|---|---|---|
| `sources/fed/market-risk-models.pdf` | 2,280,184 bytes | Second source — *Supervisory Stress Test Model Documentation: Market Risk Models*, October 2025, **Updated January 2026** | `7e9f633b927d7d0b0d1c8137c3d5a77e942851e975fadf7a0a5fd5c562727770` |

- **Provenance:** downloaded 2026-07-23 from https://www.federalreserve.gov/supervisionreg/files/market-risk-models.pdf (linked from the Board's 2026 DFA stress-test model-documentation page). Collection user-approved at the asset-side roadmap decision (OQ-004 narrowing).
- **Why collected:** PPNR footnotes 64–65 ("See Securities Model Description") hold the reinvestment assumptions and the Agency RMBS vendor prepayment model needed by securities chapters #3–#5.
- **Identification [INT, strong basis]:** **Section A "Securities Model" (pp. 7–77)** is the referenced description — the running page header reads "Model Documentation: Securities Model"; no standalone securities volume exists in the 2026 documentation series; Section A documents the Agency MBS third-party vendor model (p. 10, page image verified); the PPNR source's own footnote 52 cross-references this same volume for the Yield Curve Model.
- **Verification status (updated 2026-07-23, Increment 2):** title page, preface, Table of Contents, and Section A pp. 7–10, **18–20 (vendor model), and 72–74 (Reinvestment Methodology)** read as page images; the delegated passages were additionally cross-checked against a `pdftotext` extraction of pp. 7–77. **Scoped markdown working copy created:** `sources/fed/market-risk-models-securities-extracts.md` — deliberately partial, covering only the passages the PPNR income models delegate (reinvestment; vendor model; constant-portfolio context; MRM Question A1). Citations into this source use `(MRM p. N)` — printed page = PDF sheet, verified on every page opened. **Equation-label collision:** MRM equations are hyphenated ("A-32", "A-41") and numerically collide with PPNR names ("A32", "A41") — never cite without the document prefix. A full Section A integrity review remains deliberately out of scope (fair-value/credit-loss/OCI machinery is outside the net-interest scope); extend the extracts file and this addendum if more passages are ever needed.
- **Scope note:** §§1–10 of this review cover the PPNR source only; this addendum tracks the second source separately. If the checksum above changes, this addendum is void and must be rerun.

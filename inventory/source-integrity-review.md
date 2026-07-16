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
| SQ-8 | 201 | Equation A42 spells "AccrectionAmortization" | "AccretionAmortization" (spelled correctly in A40/A41) |
| SQ-9 | 212 | "t indicats the quarter" in Equation A45 where-list | "indicates" |
| SQ-10 | 217 | Equation A48 caption: "…Securities Sold under the Agreement to **Purchase**" | "…to Repurchase" (correct in the section heading, PDF p. 216) |
| SQ-11 | 184 vs. 220 | Footnote 63 lists 8 industry-scalar categories ("mortgage, auto, corporate & investment, small and median business loans and card, domestic CRE, consumer credit card, one category for rest of consumer loans, and one for rest of wholesale exposures"); Table A8 has 7 rows | Table A8's "C&I, noncore SME loan and card" appears to merge footnote 63's "corporate & investment" and "small and median business loans and card"; "median" likely intends "medium". Logged as OQ-010 |
| SQ-12 | 214 | Two consecutive assumptions both labeled "A third assumption" | The second should be a fourth assumption |
| SQ-13 | 231 | Subsection label "(a.) Variable Selection" follows "(a) Model Description" in v.d(2) | Labeling quirk (same "(a.)" style appears in current-suite iv.n(1), p. 162) |
| SQ-14 | 2 vs. 167 | Page 2 says the Board "intends to use" this PPNR model in the 2026 test; Section v (p. 167) and the B intro (p. 6) say the Board "is proposing" the new suite and seeks public input on both suites | Per project rules, all deliverables state the Section v suite is **proposed, not adopted**; do not rely on the page 2 phrasing |

## 9. Verification coverage and residual items

- **PDF pages visually verified (33):** 4–5, 167–169, 173–175, 181–184, 189–191, 193, 196, 201, 206–207, 209–217, 219–220, 222, 225–226, 230–231, 234–235.
- **Verified in full:** every in-scope equation (A32–A53), every in-scope table (A6–A9), footnotes 61–66, all December-revision items within scope, the Section v start boundary (p. 167) and end boundary (v.f begins p. 235).
- **Not verified (accepted residual):** current-suite sections B.i–iv beyond the heading census (BACKGROUND/COMPARISON use only — verify on demand when a chapter cites them); out-of-scope December-revision items (pp. 237, 240, 243, 251–255); footnotes 1–60 (outside scope).

## 10. Fitness conclusion

The Markdown conversion is **faithful for the entire Phase 1 net-interest scope**: no equation, table value, or line-item reference was damaged in conversion. All defects found are either trivial markup artifacts (§7) or quirks present in the Fed's own PDF (§8). The Markdown is approved as the primary searchable working source, with the PDF remaining authoritative and the §7 corrected readings applied when quoting. Material claims in downstream deliverables must cite `(PDF p. N; md sec-M)`.

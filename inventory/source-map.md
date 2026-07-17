# Source Map — Fed PPNR Model Documentation (October 2025, updated December 2025)

**Deliverable 3 of Phase 1, Task 1.** Date: 2026-07-16.
Maps every section of `sources/fed/pre-provision-net-revenue-models.md` / `.pdf` to pages, anchors, contained artifacts, and Phase 1 scope status.

Conventions (established in `inventory/source-integrity-review.md`):
- Printed page number = PDF sheet number (verified 1:1).
- md locations cite the `<a id="sec-N">` anchor and/or line number; `<!-- page N -->` markers mark where page N begins.
- **Scope tags:** `PRIMARY` = Phase 1 subject matter (proposed net-interest models); `BACKGROUND` = read for interpretation only; `COMPARISON` = current-suite section that a proposed model explicitly compares itself with or depends on; `OUT-OF-SCOPE` = not used in Phase 1.
- **Verified** = section content checked against the PDF page image on 2026-07-16 (see integrity review §9 for the page list); unverified sections rely on the Markdown plus the heading census.
- Model IDs refer to `inventory/model-inventory.md`.

## 1. Front matter and revisions (PDF pp. 1–5)

| Section | Heading | md | PDF pp. | Content | Scope | Verified |
|---|---|---|---|---|---|---|
| — | Title block: "Supervisory Stress Test Model Documentation — PPNR Model, October 2025, Updated December 2025" | lines 1–15 | 1–2 | Document identity; note p. 2 phrasing "intends to use" (quirk SQ-14) | BACKGROUND | Yes (p. 2 text; title) |
| — | Table of Contents | line 17 | 2–4 | Navigation | BACKGROUND | No |
| A | A. Revisions | sec-0, line 262 | 4–5 | 13 December 2025 revision items | BACKGROUND (drives version control; reconciled in integrity review §3) | Yes |

## 2. General framework (PDF pp. 6–40) — read only where it helps interpret the proposed models

| Section | Heading | md | PDF pp. | Content | Scope | Models |
|---|---|---|---|---|---|---|
| B | B. Pre-Provision Net Revenue Model | sec-1, line 298 | 6 | States both suites exist; public input sought on both; proposed ≠ adopted | BACKGROUND (key status statement) | all |
| B.i | i. Statement of Purpose | sec-2, line 310 | 6–8 | Equation A1 (PPNR identity); 23-component census of the current suite | BACKGROUND | all |
| B.ii | ii. Model Framework | sec-3, line 358 | 8–12 | Model-type taxonomy | BACKGROUND | all |
| B.ii.a | a. Regression Models (+ 6 subsections, sec-4…sec-13) | sec-4, line 435 | 12–32 | Current regression conventions: AR terms, scaling balances, fixed effects, projection mechanics | BACKGROUND (helps read v.d) | nii_trading_al, ie_other_borrowing |
| B.ii.b | b. Structural Models (+ sec-15) | sec-14, line 717 | 32–33 | Definition and rationale for structural models; launch-point/contract framing (source: "lift-off") | BACKGROUND (core for v.a) | all structural |
| B.ii.c | c. Nonparametric Models (+ sec-17, sec-18) | sec-16, line 742 | 33–35 | Current-suite nonparametric approach | OUT-OF-SCOPE | — |
| B.ii.d | d. Data Sources and Treatment (+ sec-20, sec-21) | sec-19, line 773 | 35–39 | Pro forma adjustments; FR Y-14/Y-9C data conventions | BACKGROUND | all |
| B.ii.e | e. Subordinated Debt Data Construction | sec-22, line 857 | 39 | Current sub-debt data build | COMPARISON (context for ie_other_borrowing absorbing sub debt) | ie_other_borrowing |
| B.iii | iii. Questions | sec-23, line 865 | 39–41 | Framework-level Board questions | BACKGROUND | — |

## 3. Current (2025) model suite — Section B.iv (PDF pp. 41–166)

Mapped at model level; drill in only when a proposed model cites it. All are the models the proposed suite would replace.

| Section | Heading | md | PDF pp. | Scope | Related proposed model |
|---|---|---|---|---|---|
| iv.a | a. Regression Models for Interest Income | sec-25, line 885 | 41–42 | COMPARISON | — |
| iv.b | b. Interest Income on Loans | sec-26, line 910 | 42–47 | COMPARISON | ii_loans |
| iv.c | c. Interest Income on Interest-Bearing Balances | sec-32, line 1009 | 48–51 | COMPARISON | ii_dep_banks_other |
| iv.d | d. Interest Income on U.S. Treasuries | sec-38, line 1101 | 52–55 | COMPARISON | ii_ust |
| iv.e | e. Interest Income on Mortgage-Backed Securities | sec-44, line 1189 | 56–59 | COMPARISON | ii_mbs |
| iv.f | f. Interest Income on Other Securities | sec-49, line 1274 | 60–64 | COMPARISON | ii_other_sec |
| iv.g | g. Interest Income from Trading Assets | sec-54, line 1362 | 65–68 | COMPARISON | nii_trading_al |
| iv.h | h. All Other Interest Income | sec-59, line 1445 | 69–73 | COMPARISON | ii_other_ida |
| iv.i | i. Regression Models for Interest Expense | sec-64, line 1526 | 74 | COMPARISON | — |
| iv.i(1) | (1) IE on Domestic Time Deposits | sec-65, line 1551 | 75–79 | COMPARISON | ie_dom_time_dep |
| iv.i(2) | (2) IE on Other Domestic Deposits | sec-70, line 1641 | 80–84 | COMPARISON | ie_other_dom_dep |
| iv.i(3) | (3) IE on Foreign Deposits | sec-75, line 1739 | 85–89 | COMPARISON | ie_foreign_dep |
| iv.i(4) | (4) IE on Trading Liabilities, Other Borrowed Money and All Other Interest Expense | sec-80, line 1827 | 90–97 | COMPARISON | nii_trading_al, ie_other_borrowing |
| iv.j | j. Regression Models for Noninterest Income (5 components) | sec-88, line 1972 | 98–126 | OUT-OF-SCOPE | — |
| iv.k | k. Regression Models for Noninterest Expense (2 components) | sec-114, line 2502 | 127–141 | OUT-OF-SCOPE | — |
| iv.l | l. Estimated Parameters of Regression Models (current suite) | sec-126, line 2763 | 141–144 | COMPARISON (current-suite parameters; not inputs to the proposed suite) | — |
| iv.m | m. Structural Models | sec-127, line 2824 | 145 | COMPARISON | — |
| iv.m(1) | (1) II from Fed Funds Sold & Reverse Repo | sec-128, line 2836 | 145–148 | COMPARISON (absorbed into proposed other interest/dividend-bearing assets) | ii_other_ida |
| iv.m(2) | (2) IE on Fed Funds Purchased & Repo | sec-132, line 2928 | 149–152 | COMPARISON | ie_fed_funds_repo |
| iv.m(3) | (3) IE on Subordinated Debt | sec-136, line 3018 | 153–159 | COMPARISON (absorbed into proposed other borrowing; cf. Question A190) | ie_other_borrowing |
| iv.n | n. Nonparametric Models | sec-140, line 3156 | 160–166 | OUT-OF-SCOPE | — |

## 4. Proposed 2026 suite — Section B.v (PDF pp. 167–255) — PRIMARY through v.e

### 4.1 Section v introduction (PRIMARY)

| Section | Heading | md | PDF pp. | Content / artifacts | Verified |
|---|---|---|---|---|---|
| v | v. Proposed Models for 2026 PPNR Components | sec-148, line 3328 | 167–172 | Rationale for replacing regressions; four proposed model types; **Table A6** (pp. 168–169, md 3339–3370); NII/expense preview (pp. 170–172, background for v.f) | Yes (pp. 167–169) |

### 4.2 v.a Proposed Structural Models (PRIMARY, pp. 172–219)

| Section | Heading | md | PDF pp. | Artifacts | Model |
|---|---|---|---|---|---|
| v.a | a. Proposed Structural Models | sec-149, line 3401 | 172–173 | 10-component list; FR Y-14 data basis | all structural |
| v.a(1) | (1) Interest Income on Loans | sec-150, line 3427 | 173–188 | **Eq A32** | ii_loans |
| — (a) | Model Description | sec-151, line 3433 | 173–174 | Eq A32; constant balances; loss-rate dependency | ii_loans |
| — (b) | Portfolio Segmentation | sec-152, line 3460 | 174–175 | Jump-off weighted-average rates; fixed/variable split | ii_loans |
| — | Wholesale | sec-153, line 3471 | 175 | HFI vs. FVO/HFS; truncated "FR." sentence (SQ-5); footnotes 61–62 | ii_loans |
| — | Corporate | sec-154, line 3479 | 175–176 | 11 portfolios; 16/22 rate-split; mixed-rate/demand→variable; fee-only excluded; NPML proxy | ii_loans |
| — | CRE | sec-155, line 3492 | 176–177 | 6 loan types; 24 segments | ii_loans |
| — | Retail | sec-156, line 3503 | 177 | 4 retail sections; segmentation drivers | ii_loans |
| — | Mortgage | sec-157, line 3511 | 177–178 | HFI/FVO-HFS × FRM/ARM; rejected extra segmentation | ii_loans |
| — | Auto Loan | sec-158, line 3520 | 178 | All fixed-rate; new/used; Prime-based spread | ii_loans |
| — | Consumer and Small Business Credit Card | sec-159, line 3530 | 178–179 | Bank/charge cards; all variable; revolver classification; Prime + constant spread | ii_loans |
| — | Other Consumer Products | sec-160, line 3545 | 179–180 | No segmentation; jump-off rate from Y-14Q PPNR line-item report; spread vs. Prime | ii_loans |
| — | Projected Interest Income Rate | sec-161, line 3558 | 180 | Runoff/re-origination; rate floors | ii_loans |
| — | Variable-rate products | sec-162, line 3566 | 180–181 | **Eq A33** | ii_loans |
| — | Base rate assumptions | sec-163, line 3585 | 181 | Prime / mortgage rate / 3M Treasury | ii_loans |
| — | Spread Estimation | sec-164, line 3593 | 181–182 | Constant spreads; replacement of run-off | ii_loans |
| — | Fixed-Rate Products | sec-165, line 3606 | 182–183 | **Eqs A34–A38**; median origination date (t−a); wt from default/prepay/maturity | ii_loans |
| — | Industry Scalar | sec-166, line 3648 | 183–184 | True-up scalar; footnote 63 | ii_loans |
| — (c) | Model Assumptions and Limitations (+ Assumptions / Limitations / Retail / Wholesale) | sec-167…171, lines 3659–3729 | 184–186 | Assumptions (1)–(7) incl. quarterly compounding; NPML proxy; no revolver-draw growth | ii_loans |
| — (d) | Questions | sec-172, line 3735 | 186–188 | Questions A151–A160 (A159 = hedges not incorporated) | ii_loans |
| v.a(2) | (2) II on Deposits with Banks and Other | sec-173, line 3765 | 188–190 | **Eq A39**; Sched G line 14; quirks SQ-3/SQ-4 in Questions | ii_dep_banks_other |
| v.a(3) | (3) II on U.S. Treasuries | sec-177, line 3821 | 190–195 | **Eq A40**; Sched B.1 + vendor data; hedge income initially zero; reinvestment per Securities Model | ii_ust |
| v.a(4) | (4) II on Mortgage-Backed Securities | sec-181, line 3897 | 195–200 | **Eq A41**; vendor prepayment model (Agency RMBS); footnote 65 | ii_mbs |
| v.a(5) | (5) II on Other Securities | sec-185, line 3982 | 200–205 | **Eq A42**; book-yield method; no prepayments | ii_other_sec |
| v.a(6) | (6) II on Other Interest/Dividend-Bearing Assets | sec-189, line 4060 | 205–209 | **Eq A43**; Sched G.2 line 15; BHCK3365 cross-ref; footnote 66 | ii_other_ida |
| v.a(7) | (7) IE on Domestic Time Deposits | sec-193, line 4123 | 209–211 | **Eq A44**; items 42E, 71; "average" balance | ie_dom_time_dep |
| v.a(8) | (8) IE on Other Domestic Deposits | sec-197, line 4177 | 211–215 | **Eqs A45–A47**; items 42B–42D, 79A–81B; ELB regime; 2020:Q2–2021:Q4 spread window | ie_other_dom_dep |
| v.a(9) | (9) IE on Foreign Deposits | sec-201, line 4275 | 215–216 | Same framework by reference; items 43A/44B, 35A/35B, 83A–84B | ie_foreign_dep |
| v.a(10) | (10) IE on Fed Funds Purchased & Repo | sec-205, line 4314 | 216–219 | **Eq A48**; items 44A/44B (SQ-16 — misnamed as balances); caption typo SQ-10 | ie_fed_funds_repo |

### 4.3 v.b–v.e Parameters, hedges, regressions (PRIMARY, pp. 219–234)

| Section | Heading | md | PDF pp. | Artifacts | Model |
|---|---|---|---|---|---|
| v.b | b. Estimated Parameters for Proposed Structural Models | sec-209, line 4374 | 219–220 | **Table A7** (p. 219, SQ-1), **Table A8** (p. 220) | ie_other_dom_dep, ie_foreign_dep, ii_loans |
| v.c | c. Proposed Adjustments … Interest Rate Risk Hedges | sec-210, line 4411 | 220–225 | Accounting vs. non-accounting hedges | adj_irr_hedge |
| v.c(1) | (1) Model Specification | sec-211, line 4420 | 221–223 | **Eqs A49–A51**; proposed FR Y-14Q B.2/B.3 collection; terminated-hedge amortization | adj_irr_hedge |
| v.c(2) | (2) Assumptions and Limitations | sec-212, line 4469 | 223 | No renewals/terminations modeled | adj_irr_hedge |
| v.c(3) | (3) Questions | sec-213, line 4477 | 223–225 | Questions A181–A187 | adj_irr_hedge |
| v.d | d. Proposed Regression Models | sec-214, line 4525 | 225 | — | — |
| v.d(1) | (1) Net II on Trading Assets and Liabilities | sec-215, line 4531 | 225–230 | **Eq A52**; WLS on net trading assets; Sched G worksheet; ÷4 rate conversion | nii_trading_al |
| v.d(2) | (2) Interest Expense on Other Borrowing | sec-220, line 4614 | 230–234 | **Eq A53(1)/(2)**; items 44C/46/47; FR Y-9C BHDM4062, BHDMC699, BHCK2309; 2020:Q2–2021:Q4 sample; "(a.) Variable Selection" at line 4664 (no anchor, CA-4) | ie_other_borrowing |
| v.e | e. Estimated Parameters for Proposed Regression Models | sec-224, line 4707 | 234 | **Table A9**; firm fixed effects not disclosed | nii_trading_al, ie_other_borrowing |

### 4.4 Remainder of Section v (OUT-OF-SCOPE for Phase 1)

| Section | Heading | md | PDF pp. | Scope |
|---|---|---|---|---|
| v.f | f. Proposed Noninterest Income and Expense Models Using Firm Projections (discount factor + efficiency ratio models) | sec-225, line 4726 | 235–251 | OUT-OF-SCOPE (Phase 1 boundary verified: v.f begins p. 235) |
| v.g | g. Estimated Parameters for Proposed NII and Expense Models | sec-235, line 5179 | 251–255 | OUT-OF-SCOPE |

## 5. Footnotes block

| Heading | md | Notes |
|---|---|---|
| Footnotes | line 5230 | Footnotes 1–66 collected at file end. In-scope: 61–66 (verified; fn 66 carries conversion artifact CA-1). Footnotes render inline in the PDF page footers at their reference pages (61–62 → p. 175; 63 → p. 184; 64 → p. 193; 65 → p. 196; 66 → p. 206) |

## 6. Reconciliation

- Table A6 net-interest rows: 10 structural + 2 regression = **12 components**; + the cross-cutting hedge adjustment (v.c) = **13 PRIMARY items**, matching the 13 records in `inventory/model-inventory.md` and the PRIMARY sections in §4 above.
- Scope boundary: PRIMARY content spans PDF pp. 167–234 inclusive; p. 235 onward is out of scope.

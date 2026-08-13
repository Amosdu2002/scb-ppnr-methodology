# Model Inventory — Proposed 2026 PPNR Net-Interest Models

**Deliverable 2 of Phase 1, Task 1.** Date: 2026-07-16.
**Every model below is PROPOSED for the 2026 stress test (public-comment stage) — NOT adopted.** Source: Section B.v of the Fed PPNR model documentation (October 2025, updated December 2025). Citations are `(PDF p. N; md sec-M)`; page conventions per `inventory/source-integrity-review.md`.

## Census and reconciliation

Table A6 (PDF pp. 168–169; md sec-148) assigns the 23 PPNR components to four proposed model types. The net-interest portion is 10 structural components + 2 regression components = **12 components**; the cross-cutting interest-rate-risk hedge adjustment (v.c) makes **13 inventory records**. Reorganizations relative to the current 2025 suite (for orientation only):

- Fed funds sold & reverse repo income (current structural model iv.m(1)) is **absorbed into** other interest/dividend-bearing assets (#6) (PDF p. 217; md sec-206).
- Subordinated debt expense (current structural model iv.m(3)) is **absorbed into** other borrowing (#12) (PDF p. 230; md sec-220; Question A190).
- Trading-asset interest income (current iv.g) and the trading-liabilities part of current iv.i(4) become one **net** regression model (#11) (PDF p. 225; md sec-215).

Dimension notation used throughout: `b` = firm, `p` = product, `i` = segment, `t`/`q` = projection quarter, `PQ0` = launch point — the last quarter before the projection horizon (source terms "lift-off"/"jump-off"; source notation `q0`/`t=0` retained inside equation transcriptions; decision D-005).

---

## 1. `ii_loans` — Interest Income on Loans

| Field | Value |
|---|---|
| Fed name | Interest Income on Loans (PDF pp. 173–188; md sec-150) |
| Component / side | Loans — interest income (Table A6: Structural) |
| Model family | Common loan framework with portfolio-specific rules (per project decision D-001 scope treatment) |
| Projects | Quarterly dollar interest income by firm × product × segment × quarter, 9 quarters; `Loan interest income(b,p,i,t) = Loan balance(b,p,i,t) × Interest income rate(b,p,i,t)` — **Eq A32** (PDF p. 173) |
| Key equations | A32 (income); A33 (variable rate = BaseRate + Spread(t=0)); A34 (existing fixed rate unchanged); A35 (new-origination rate); A36 (fixed-rate spread, retail, from new originations at t=0); A37 (wholesale spread: all-loan jump-off average IIR minus base rate at median origination date t−a); A38 (blended fixed rate via re-origination weight wt) (PDF pp. 181–183) |
| Portfolio segmentation | Wholesale = Corporate (11 disclosure portfolios; 16 of 22 split fixed/variable; mixed-rate and demand loans treated variable; fee-only loans excluded entirely) + CRE (6 loan types; 24 segments with HFI vs. FVO/HFS and rate split). Retail = Mortgage (HFI/FVO-HFS × fixed/ARM), Auto (all fixed; new vs. used vehicle), Consumer & Small-Business Credit Card (all treated variable; revolver share from 12-month-active + finance-charge-in-last-3-months rule), Other Consumer Products (no segmentation; aggregate product-type jump-off rates) (PDF pp. 175–180) |
| Firm data inputs | FR Y-14M (mortgage, card loan-level); FR Y-14Q Schedule H.1 (wholesale facility-level, per footnote 61; identifies NPML), A.2 (auto segment-level), retail schedules; FR Y-14Q Schedule G.2 (reported interest income for scalar true-up; jump-off rates for other-consumer via "most closely aligned business line") |
| Scenario inputs | Prime Rate (retail variable incl. cards and HELOC; spread benchmark for auto and other-consumer), mortgage rate (ARMs), 3-month Treasury yield (wholesale) (PDF p. 181) |
| Parameters | Industry scalars — **Table A8** (PDF p. 220), 7 values, supplied; spreads — derived from firm data at the launch point, then constant; no estimated regression coefficients ("does not estimate any components", PDF p. 174) |
| Launch-point inputs | Balance-weighted average jump-off interest rates by segment; percentage of outstanding balance by segment; portfolio balances from FR Y-14 schedules; revolver shares; jump-off spreads |
| Constant over horizon | Balances (flat balance; run-off replenished by same-type new originations within the quarter); spreads; segment composition; revolver share (implied — OQ-012); scalars |
| Varies over horizon | Variable rates (reprice quarterly with base rate); fixed-rate portfolio rate via A38 blending (weight wt from default, prepayment, maturity rates); floors bind when scenario rates fall below stated floor (values unspecified — OQ-002) |
| Upstream dependencies | Retail and Wholesale credit-loss models supply estimated loss/runoff rates for wt (PDF p. 174; OQ-001) |
| Hedge treatment | **Not incorporated** — data limitations; proposed FR Y-14Q B.2 update would add it (Question A159, PDF p. 188) |
| Assumptions (source-stated, PDF p. 184) | (1) flat balance; (2) delinquent loans accrue (impact immaterial); (3) **interest income quarterly compounded**; (4) constant spreads; (5) most variable rates reprice quarterly; (6) segment fixed rates unchanged except new originations; (7) products grouped by similar rate structure |
| Integrity flags | SQ-5 (truncated "sourced from FR." p. 175), SQ-6/SQ-7 (A37/A38 notation), SQ-11 (Table A8 7 rows vs. footnote 63's 8 categories); **added 2026-07-30 (loans slice 1):** SQ-18 (A34/A35/A36/A38 print no firm subscript b), SQ-19 ("farm" p. 186 vs. "farmland" p. 175), SQ-20 (A33 where-list omits segment i); **added 2026-08-03 (loans slice 2):** SQ-21 ("Schedule H.1 schedule" doubling p. 176), SQ-22 (owner-occupancy naming variants pp. 175–176); **added 2026-08-12 (retail slice R1):** SQ-23 (p. 182 names Prime as *the* retail base rate, omitting the mortgage exception of pp. 181/185), SQ-24 ("non-core retails products" p. 185); **added 2026-08-12 (retail wave 2):** SQ-25 ("reflected in the alternative model" p. 178 — referent unstated) |
| Open questions | OQ-001, OQ-002, OQ-003, OQ-006, OQ-010, OQ-011, OQ-012, OQ-014 (scalar granularity — this component; added to this record 2026-07-30), OQ-015; **filed 2026-07-30:** OQ-033 (fixed-rate firm dimension), OQ-034 (corporate 16-of-22 derivation; segment total unstated), OQ-035 (CRE applicability of the Corporate-stated mixed-rate/demand/fee-only rules); **filed 2026-08-03:** OQ-036 (farmland rate type unstated — **RESOLVED FOR PROJECT IMPLEMENTATION** same day via PID-LOAN-1; source-side absence preserved), OQ-037 (NPML proxy spread data slice and bank-level granularity — **RESOLVED FOR PROJECT IMPLEMENTATION for Corporate 2026-08-07** via PID-LOAN-10; source-side ambiguity preserved), OQ-038 (Corporate defining form unstated; residual categories undefined); **filed 2026-08-12 (loans slice 3):** OQ-039 (CRE loan-level schedule unnamed — "H.2" appears nowhere in the document; suite-level list p. 172 names Schedules G/B/M + FR Y-14M only); **filed 2026-08-12 (retail slice R1):** OQ-040 (mortgage-family base-rate boundary — FRM new-origination base rate never stated verbatim; fixed-HEL classification under the p. 185 "except for mortgages" exception; SQ-23), OQ-041 (other-consumer engine assignment — "no segmentation" p. 180 vs the expert-judgment fixed/variable split p. 181 vs "most non-core loans" fixed p. 183), OQ-042 (auto Eq A36 spread measurement on segment-level A.2 data vs the p. 178 trend-analysis sentence); OQ-033 evidence appended (retail prose states the firm dimension four times: pp. 177–179 "by segment and by firm", p. 185 "by product, segment, and firm"); **filed 2026-08-12 (retail wave 2):** OQ-043 (card projected-spread sentence lists three inputs — weighted rate, reported spread, Prime — and no formula) |
| Project implementation decisions | **PID-LOAN-1 … PID-LOAN-8** (2026-08-03), all Corporate-scoped and user-confirmed. PID-LOAN-1: the three data-limited portfolios are **floating**. PID-LOAN-2: segment key = Fed Category (1–11) × LOCOM {HFI, HFS} × Variable Type {0 DO NOT USE, 1 Fixed, 2 Floating, 3 Mixed, 4 Entry Fee Based} — no demand-loan code exists, so the Fed's demand rule is inapplicable. PID-LOAN-3/4: rate pools (Float = v2+v3, Fixed = v1, weighted by committed exposure) and spreads (Floating vs PQ0 3M; Fixed and Mixed vs their own median-origination-quarter 3M, Mixed borrowing the Fixed pool rate). PID-LOAN-5: v2/v3 variable engine, v1 Eq A38 engine, **v0 and v4 count toward balance but earn no income**. PID-LOAN-6: wt from contractual maturities only. PID-LOAN-7: floors from CORP H.1. PID-LOAN-8: input contract. **Resolve OQ-001, OQ-002, OQ-003 for Corporate** (source-side gaps preserved; still open for CRE/Retail). **Two recorded divergences:** wt omits default and prepayment; fee-based balances stay in the share denominator where the Fed excludes them. Spec: `specifications/interest-income/loans/ii_loans_corporate.spec.md`. **PID-LOAN-9 … PID-LOAN-12** (2026-08-07 / 2026-08-12, Corporate): physical reference key and its collapses; the merged 9/10/11 bucket priced off the depository floating pool (resolves OQ-037 for Corporate); Table A8 read directly with the user-confirmed Corporate scalar mapping (resolves OQ-010 for Corporate); unidentified H.1 rows labeled and kept. **PID-LOAN-13 … PID-LOAN-17** (2026-08-12, Corporate): the reference-engine construction, **converged against the company reference (grand 0.9979)**. **PID-LOAN-18 … PID-LOAN-25** (2026-08-12, **CRE-scoped**, all user-confirmed): the CRE H.2 input contract and reference key (same vocabularies as H.1, no demand code); the four-category mapping with the **data-forced international merge** (H.2 code 7 cannot distinguish the Fed's three international portfolios); the M.1 rows 17/18/21 multiplicand wiring (E/G domestic per side; Σ I/K international); the scalar assignment domestic → "Domestic CRE" 1.081 / international → "Rest of wholesale" 1.113 (**resolves OQ-010 for CRE**); the outstanding-weighted origination date (OQ-003 CRE weighting basis; median-vs-mean formula at spec stage); mixed on the variable engine at the hybrid spread; fee/DO-NOT-USE rows balance-only; the outstanding-weighted variable floor (**resolves OQ-002 for CRE** with the H.2 floor column). **OQ-001 (wt) is the one Corporate-resolved gap still open for CRE.** **PID-LOAN-26 … PID-LOAN-28** (2026-08-12, **Retail-scoped**, user-supplied input contracts): the M.1 retail wiring (per-row "FRB NII model" role labels + four family flag columns "Mortgage (dom)"/"Auto (dom)"/"Card (dom)"/"other consumer"; **every retail row's international role is "Retail - noncore"** — the p. 180 international-in-noncore census physically realized; SME-cards row → Card, Small-business row → noncore); the "Mortgage query" contract (12 segments {First lien, Home equity, HELOC} × {HFI, HFS/FVO} × {Fixed, Variable}; portfolio + post-cutoff-origination weighted rates at two windows; WEIGHTED_ARM_FLOOR; per-segment × PQ maturing-balance schedules; two first-lien classification variants; "x" = missing); the "Card query" contract (4 numbered segment rows; all-book AND revolver-only APR/spread pairs + revolver balance; WEIGHTED_MAX_APR cap candidate). Interpretive readings ride as flagged observations in the family briefs — the gate confirms them. **PID-LOAN-29 … PID-LOAN-31** (2026-08-13, wave 3 — the full engine dump): the auto "Auto 4Q24 pivot" contract in a **separate workbook** (cols M/N/O = outstanding / average rate / **new-origination rate**; A.2 pivots + Y-14Q Retail A.2/A.7/A.9 extracts); the other-consumer construction (all-variable at product grain; jump-off rates = the PQ0 average-rate column of an institution-named PPNR line-item projections sheet via an explicit line mapping — the OQ-011 project implementation, observed; scalars 1.072 / small-business 1.033); the "MEV Data" contract (**columns "Prime rate" and "Mortgage rate" confirmed, percent** — template TBCs resolved), multi-workbook config direction, and the results targets (per-family FRB-model-vs-champion 4Q/9Q summary + {Fixed, Variable, Total × scalar} panels). Engine observations recorded per family brief §0.2 awaiting gate confirmation — highlights: mortgage window switch ("latest month vs latest quarter", set to quarter), **mortgage rate confirmed-as-observed for first-lien AND home-equity blocks with Prime for HELOC (OQ-040)**, wt arithmetic-verified maturity-only, missing-window fallback = own current rate; card switch family (floor-at-zero / full population / **reported spread — OQ-043 observed**), income = M.1 × revolver share × (Prime + reported spread)/4, **SME cards × 1.033 observed**; **auto scalar anomaly ×0.948 vs Table A8's 0.865 — open gate question**. **Wave-3 confirmations (2026-08-13, PID-LOAN-32/33/34 + amendments to 26/29): auto scalar = published 0.865 (user-directed; 0.948 = recorded compare-basis divergence); MORT sheet drives (alternative unused); "Median Date Base Rate" = PQ0 mortgage rate — OQ-040 RESOLVED for project implementation; auto wt = supplied schedule (pivot cols P–X, rows 2/3 = New/Used PQ1–9; OQ-001 auto leg); M.1 wiring confirmed (values through col M; role labels per side are the wiring, indicator columns the cross-check; lease rows excluded); card 0/0/0 + 3-month-only revolver share adopted as working assumptions (compare arbitrates).** The mortgage missing-window ("x") fallback closed 2026-08-13 as a flagged working assumption (the query's AFTER columns are hardcoded — no formula lineage; fallback = the segment's own current rate, censused, compare arbitrates). **No open elicitation items remain; the combined gate PASSED 2026-08-13 ("Looking good") — the retail set is fully specified and the spec/engine build is underway** |
| Wholesale portfolio detail | **Corporate** = 11 portfolios, of which 8 carry loan-level FR Y-14Q H.1 data and are rate-split (8 × 2 asset classifications = the source's "16 out of 22"); the 3 without loan-level data (loans for purchasing and carrying securities; domestic and international farmland) take a **bank-level** NPML proxy spread. **Owner-occupied CRE is modeled in Corporate** (portfolios 2 and 6) — the Corporate/CRE line is owner-occupancy, not property type. Fee-only loans are excluded from both the average rate **and** the total-balances denominator — the only stated balance-denominator exclusion in the loan model. No Corporate segment total is stated (CRE's 24 is) — implied 38 [INT, OQ-034]. **CRE** = 6 FR Y-9C-defined portfolios (domestic/international × construction, multifamily, non-owner-occupied), all rate-split, stated total **24 segments** (6 × 2 × 2 [INT], anchored by the stated 24); no data-limited exception and no NPML analogue exist for CRE; the FR Y-14Q schedule carrying CRE facility data is unnamed (OQ-039). Physical realization (PID-LOAN-19 — recorded, data-forced divergence): the firm's H.2 line code cannot distinguish the three international portfolios, which are modeled as one merged international category (4 categories × 2 × 2 = 16 cells) |
| Retail portfolio detail | **Four families** (PDF pp. 177–180): **Mortgage** — HFI/FVO-HFS × FRM/ARM, Y-14M loan-level weighted rates; term and FICO splits considered but NOT adopted [ALT]. **Auto** — FR Y-14Q Schedule A.2 **segment-level**; all-fixed Board assumption (Eq A33 never runs); immaterial HFS treated as HFI at the firm level; new/used grid; Prime spread benchmark (measurement = OQ-042). **Card** — consumer bank vs charge cards, small business cards separate-similar; all balances assumed variable (~10% short-term fixed absorbed); income depends on the **revolver share** (active 12 months + ≥1 positive finance charge in last 3 months); rate AND spread reported in Y-14M; Prime benchmark; OQ-012. **Other Consumer** — heterogeneous residual incl. all international consumer products; no segmentation; jump-off rates from the Y-14Q PPNR line-item report per "most closely aligned business line" (OQ-011); spread vs Prime held constant; engine assignment = OQ-041. Retail-wide: Prime-except-mortgages base-rate rule (p. 185; boundary = OQ-040); Eq A36 spread from **new originations only, spot-only** (no t−a history); no retail mixed/demand/fee-only rules, no retail floor statement (OQ-002 open), wt delivery unstated (OQ-001 open); the single retail-directed Board question is A156 (revolvers). No retail PIDs exist — physical mappings pending the R1 elicitation |
| Artifacts (loans slices 1–3 + retail R1) | Source briefs: `handbook/models/ii_loans_common.source-brief.md` (owns Eqs A32–A38 verbatim + the common-boundary register over PDF pp. 173–188) and `handbook/models/ii_loans_wholesale.source-brief.md` (Corporate∩CRE shared framework; cites equations, transcribes none) — **APPROVED 2026-08-03**; `handbook/models/ii_loans_corporate.source-brief.md` (11-portfolio census, Corporate segmentation grid, rate-type mechanics, NPML proxy exception, fee-only dual exclusion) — **APPROVED 2026-08-12** (user statement; banner updated same day, amendment recorded); `handbook/models/ii_loans_cre.source-brief.md` (6-type census, 24-segment grid, inheritance register, fact-of-absence register, OQ-039, PID-LOAN-18..25) — **APPROVED 2026-08-12**. Computation specs: `specifications/interest-income/loans/ii_loans_corporate.spec.md` (converged vs the company reference 2026-08-12) and `ii_loans_cre.spec.md` (created 2026-08-12 with the engine extension — `build_cre_launch_point`, H.2 loader/mapping, CRE compare mode; **reference compare CONVERGED 2026-08-12** — round 1 grand 1.0008, round 2 grand 1.0006 after the PID-LOAN-22/23 amendments; the round-3 grand line under the corrected config is owed for the spec record). **Retail briefs ALL APPROVED 2026-08-13 (combined gate):** `handbook/models/ii_loans_retail.source-brief.md` (retail framework — four-family census, retail-boundary register over sec-156–160 + sec-170, Prime-except-mortgages base-rate application, Eq A36 retail-branch application, Table A8 retail-row census; SQ-23/SQ-24, OQ-040/OQ-041 filed) and `handbook/models/ii_loans_auto.source-brief.md` (auto family — A.2 segment-level basis, all-fixed assumption, HFS→HFI reclass, new/used grid, Prime spread benchmark, elicitation register; OQ-042 filed); **Retail wave 2 (same day, approved at the same gate):** `ii_loans_mortgage.source-brief.md` (12-segment physical grid vs the Fed 2×2, classification-variant question, A36 windows, ARM floors, maturity-only wt risk; PID-LOAN-27), `ii_loans_card.source-brief.md` (two sub-portfolios, revolver machinery, income arrangement [INT], SQ-25 + OQ-043 filed, SME scalar question; PID-LOAN-28), `ii_loans_other_consumer.source-brief.md` (census + engine tension OQ-041, jump-off OQ-011, M.1 noncore wiring; **rate-side input still outstanding**). **Wave 3 (2026-08-13): the user supplied the remaining inputs and the full calculation-sheet layouts** — auto pivot contract, other-consumer construction + rate source, MEV columns, results targets (PID-LOAN-29/30/31; §0.2 addenda in all five briefs). **The retail input set is COMPLETE**; still to come: the combined retail gate + the §0.2 confirmation list (highlights: MORT-vs-alternative sheet selection; the auto ×0.948-vs-0.865 scalar; the card 12-month-activity condition), per-family specs/engines/compares, and the Wholesale integration review; no chapter exists yet (chapter granularity unchanged: one chapter, six portfolio sections per D-003) |

## 2. `ii_dep_banks_other` — Interest Income on Deposits with Banks and Other

| Field | Value |
|---|---|
| Fed name | Interest Income on Deposits with Banks and Other (PDF pp. 188–190; md sec-173) |
| Component / side | Deposits with banks and other — interest income (Table A6: Structural) |
| Model family | Short-rate calculator |
| Projects | Quarterly dollar income per firm: `F(b,t) = B(b,t) × Treasury3m(t)` — **Eq A39** (PDF p. 189). Rate = 3-month Treasury exactly (zero spread, source-stated) |
| Firm data inputs | Balances: FR Y-14Q Schedule G, Net Interest Income Worksheet, line item 14 (interest-bearing deposits incl. Federal Reserve and FHLB deposits) |
| Scenario inputs | 3-month Treasury yield |
| Parameters | None |
| Launch-point inputs | Balance B(b,q0) |
| Constant over horizon | Balance (B(b,q) = B(b,q0)) |
| Varies over horizon | 3-month Treasury path only |
| Upstream dependencies | None |
| Hedge treatment | Not addressed in this section |
| Integrity flags | SQ-3 (its Questions A161/A162 duplicated by #3), SQ-4 (Questions intro says "loans") |
| Open questions | OQ-006 |

## 3. `ii_ust` — Interest Income on U.S. Treasuries

| Field | Value |
|---|---|
| Fed name | Interest Income on U.S. Treasuries (PDF pp. 190–195; md sec-177) |
| Component / side | U.S. Treasuries (incl. U.S. Government agency obligations, excl. MBS) — interest income (Table A6: Structural) |
| Model family | Securities framework (coupon + accretion/amortization + hedge income) |
| Projects | Quarterly dollar income per security i (and derivative d): `Interest Income(i,t) = Coupon Accrual(i,t) + AccretionAmortization(i,t) + Hedge Income(d,t)` — **Eq A40** (PDF p. 191) |
| Calculation detail | Coupon accrual = CurrentFaceValue(i,t) × CouponRate(i,t)/4 (beginning-of-period face); accretion/amortization = (CurrentFaceValue(i,t=0) − AmortizedCost(i,t=0)) / MaturityInQuarters(i,t=0) — straight-line; hedge income = Notional(d,t) × (PayRate − ReceiveRate)/4 |
| Firm data inputs | FR Y-14Q Schedule B.1 (security-level); vendor data (coupon rate, maturity); FR Y-14Q Schedule B.2 (hedges — currently insufficient fields) |
| Scenario inputs | Interest-rate paths via reinvestment assumptions (Securities Model Description) |
| Parameters | None estimated |
| Launch-point inputs | t=0 face value, amortized cost, maturity |
| Constant over horizon | Balance via reinvestment assumption (maturing securities replaced; purchases assumed on first day of quarter after maturity) |
| Varies over horizon | Face values as securities mature/reinvest; hedge legs if data become available |
| Upstream dependencies | **Securities Model Description** (separate document): reinvestment assumptions (footnote 64) — OQ-004 |
| Hedge treatment | **Hedge Income initially assumed zero** — current Schedule B.2 lacks leg-level fields; proposed B.2/B.3 revisions would enable Eq A40's hedge term; Portfolio Layer Method hedges allocated to the most prevalent securities type in the closed portfolio (PDF p. 192) — OQ-005 |
| Known exclusions (source-stated) | OCI releases from AFS→HTM transfers; income from previously terminated hedges (PDF p. 194 — terminated hedges are covered by #13 if data collected) |
| Integrity flags | SQ-3 (Questions numbered A161–A164, colliding with #2) |
| Open questions | OQ-004, OQ-005, OQ-006 |

## 4. `ii_mbs` — Interest Income on Mortgage-Backed Securities

| Field | Value |
|---|---|
| Fed name | Interest Income on Mortgage-Backed Securities (PDF pp. 195–200; md sec-181) |
| Component / side | Mortgage-backed securities — interest income (Table A6: Structural) |
| Model family | Securities framework |
| Projects | Same three-term structure — **Eq A41** (PDF p. 196): coupon accrual = CurrentFaceValue(i,t) × CouponRate(i,t)/4; accretion/amortization = (CurrentFaceValue(i,t) − AmortizedCost(i,t)) / (4 × WeightedAverageLife(i,t=0)); hedge income as in #3 |
| Category-specific rules | **Agency residential MBS: vendor model** computes income to reflect prepayments (footnote 65). All other MBS: no prepayments modeled (mostly CMBS); coupon from vendor data, fallback to Schedule B.1 book yield; zero-coupon bonds accrue at book yield; floating-rate margin imputed as t=0 coupon minus t=0 spot 3M Treasury, then added to scenario 3M Treasury; accretion by effective interest method (constant coupon and book yield), fallback straight-line (PDF pp. 196–197) |
| Firm data inputs | FR Y-14Q Schedule B.1 + vendor data; Schedule B.2 (hedges) |
| Scenario inputs | 3M Treasury (floating margin index); scenario macro variables via vendor model (per footnote 65) |
| Constant over horizon | Balance via shared reinvestment assumption |
| Upstream dependencies | Securities Model Description (reinvestment + vendor prepayment model and its macro inputs) — OQ-004 |
| Hedge treatment | Hedge income initially zero (as #3) — OQ-005 |
| Known exclusions | Same as #3 (OCI releases; previously terminated hedges) |
| Open questions | OQ-004, OQ-005, OQ-006 |

## 5. `ii_other_sec` — Interest Income on Other Securities

| Field | Value |
|---|---|
| Fed name | Interest Income on Other Securities (PDF pp. 200–205; md sec-185) |
| Component / side | Other securities — interest income (Table A6: Structural) |
| Model family | Securities framework (book-yield variant) |
| Projects | **Eq A42** (PDF p. 201): combined `Coupon Accrual + AccretionAmortization = AmortizedCost(i,t) × BookYield(i,t)/4` (effective interest method; coupon and book yield assumed constant for the security's life; straight-line fallback if data missing); hedge income as in #3 |
| Category-specific rules | Floating-rate margin imputed vs. 3M Treasury as in #4; **no prepayments modeled** despite many prepayable asset classes (source-acknowledged limitation, PDF p. 202) |
| Firm data inputs | FR Y-14Q Schedule B.1 (book yield); Schedule B.2 (hedges); vendor data |
| Constant over horizon | Balance via shared reinvestment assumption |
| Upstream dependencies | Securities Model Description — OQ-004 |
| Hedge treatment | Hedge income initially zero — OQ-005 |
| Integrity flags | SQ-8 (source spells "AccrectionAmortization" in Eq A42) |
| Open questions | OQ-004, OQ-005, OQ-006 |

## 6. `ii_other_ida` — Interest Income on Other Interest/Dividend-Bearing Assets

| Field | Value |
|---|---|
| Fed name | Interest Income on Other Interest/Dividend-Bearing Assets (PDF pp. 205–209; md sec-189) |
| Component / side | Other interest/dividend-bearing assets — interest income (Table A6: Structural) |
| Model family | Short-rate calculator (two-rate blend) |
| Projects | `F(b,t) = α(b,t)·B(b,t)·Treasury3m + (1 − α(b,t))·B(b,t)·Treasury10y` — **Eq A43** (PDF p. 207). α = share of fed funds sold & reverse repos (short-duration, 3M-linked); remainder (e.g., Federal Reserve/FHLB stock) earns 10-year Treasury (footnote 66: Federal Reserve Bank stock yields the lesser of 6% and the 10Y Treasury — stated as rationale) |
| Firm data inputs | Balances: FR Y-14Q Schedule G (G.2) Net Interest Income Worksheet line item 15; α from worksheet footnote fields cross-referenced with FR Y-9C item BHCK3365 |
| Scenario inputs | 3-month and 10-year Treasury yields |
| Parameters | None |
| Launch-point inputs | B(b,q0) and α(b,q0) |
| Constant over horizon | Balance and share α |
| Absorbs | Current structural model iv.m(1) (fed funds sold & reverse repo income) — modeled jointly per Question A176 |
| Integrity flags | CA-1 (md footnote 66 has glued text) |
| Open questions | OQ-006 |

## 7. `ie_dom_time_dep` — Interest Expense on Domestic Time Deposits

| Field | Value |
|---|---|
| Fed name | Interest Expense on Domestic Time Deposits (PDF pp. 209–211; md sec-193) |
| Component / side | Domestic time deposits — interest expense (Table A6: Structural) |
| Model family | Deposit-rate framework (WAL repricing) |
| Projects | Rate path per firm: `Rate(b,t) = ρ(b) × Treasury1y(t) + (1 − ρ(b)) × Rate(b,t−1)` — **Eq A44** (PDF p. 209); expense = modeled rate × **average** balance on domestic time deposits per FR Y-14Q ("average" per December 2025 revision) |
| Firm data inputs | Initial rate: FR Y-14Q Schedule G line item 42E (Time Deposits), jump-off average rate; WAL: Schedule G line item 71 (Domestic Deposits – Time); average balances from FR Y-14Q — item unnamed in source; project mapping: item 34E [PID-1, user-confirmed 2026-07-17] |
| Scenario inputs | 1-year Treasury yield |
| Parameters | ρ(b) ≡ 1/WAL(b), computed from firm data — constant over horizon; no estimated coefficients |
| Launch-point inputs | Rate(b,0) = jump-off average rate (42E); WAL(b) |
| Constant over horizon | ρ (repricing fraction); balance |
| Varies over horizon | Rate recursion with 1Y Treasury |
| Assumptions (source-stated) | Constant repricing share; re-originations priced at 1Y Treasury (no market power); no contractual maturity structure (Call Report maturity-profile alternative discussed but not proposed, PDF pp. 210–211) |
| Integrity flags | SQ-4 (Questions intro says "interest income") |
| Open questions | OQ-005 open; OQ-006, OQ-008 resolved for project implementation (D-004/PID-6; PID-3/PID-4) |
| Artifacts (integration 2026-07-17) | Chapter `handbook/models/interest-expense/deposits/ie_dom_time_dep.md` — REVIEWED (review report artifact not preserved — follow-up focused review required); spec `specifications/interest-expense/deposits/ie_dom_time_dep.yaml` (created at integration); brief `research/source-briefs/interest-expense/deposits/ie_dom_time_dep.source-brief.md` |

## 8. `ie_other_dom_dep` — Interest Expense on Other Domestic Deposits

| Field | Value |
|---|---|
| Fed name | Interest Expense on Other Domestic Deposits (PDF pp. 211–215; md sec-197) |
| Component / side | Other domestic deposits — interest expense (Table A6: Structural) |
| Model family | Deposit-rate framework (two-regime beta model) |
| Projects | Rate per subcomponent i ∈ {MMA, Savings, Transaction}, then aggregated; expense = aggregate rate × average balance (FR Y-14Q) |
| Regime 1 — effective lower bound (3M Treasury < 25 bp) | `Rate(i,b,t) = floor(i,b,t) = Treasury3m(t) + Spread(i,b)` — **Eq A45** (PDF p. 212). Spread(i,b) = firm/deposit-type average distance to 3M Treasury during the most recent ELB period, **2020:Q2–2021:Q4** |
| Regime 2 — non-ELB (3M Treasury > 25 bp) | `Rate(i,b,t) = max(Rate(i,b,t−1) + δ(i,t), assumed_floor(i,b))` — **Eq A46** (PDF p. 213); δ(i,t) = max(ΔTreasury3m,0)·β_up(i) + min(ΔTreasury3m,0)·β_down(i); assumed_floor = First_ELB_Treasury3m + Spread(i,b), where First_ELB_Treasury3m = min(25 bp, first sub-25bp 3M Treasury observation in the scenario) |
| Aggregation | Balance-weighted across subcomponents — **Eq A47** (PDF p. 213) |
| Firm data inputs | Rates: Schedule G items 42B (MMA), 42C (Savings), 42D (Transaction); betas: items 79A/79B, 80A/80B, 81A/81B; balances per corresponding Y-14Q items — unnamed in source, project mapping 34B/34C/34D [PID-ODD-1], also the expense multiplicand since PID-ODD-3 (2026-07-23, company-reference confirmed); optional monitor reference — MDRM sum BHCB3187 + BHOD3187 + BHCB2389 + BHOD2389 [PID-ODD-2] |
| Scenario inputs | 3-month Treasury yield (level and change) |
| Parameters | β_up/β_down per deposit type = **median of firm-reported betas at the launch point** — **Table A7** (PDF p. 219; supplied); Spread(i,b) estimated from 2020:Q2–2021:Q4 data |
| Constant over horizon | Betas; spreads; balances |
| Varies over horizon | Rate path; regime switching on the 3M Treasury path |
| Integrity flags | SQ-1 (Table A7 down-row labels), SQ-2 (caption "(Equations A46)"), SQ-9, SQ-12, SQ-15 (truncated spread sentence, p. 212) |
| Open questions | OQ-005, OQ-013, OQ-017, OQ-018, OQ-021 open; OQ-006, OQ-016 resolved |
| Artifacts (integration 2026-07-17) | Chapter `handbook/models/interest-expense/deposits/ie_other_dom_dep.md` — REVIEWED; spec `specifications/interest-expense/deposits/ie_other_dom_dep.yaml`; review `reviews/interest-expense/deposits/ie_other_dom_dep.review.md` (PASS, no corrections) |

## 9. `ie_foreign_dep` — Interest Expense on Foreign Deposits

| Field | Value |
|---|---|
| Fed name | Interest Expense on Foreign Deposits (PDF pp. 215–216; md sec-201) |
| Component / side | Foreign deposits — interest expense (Table A6: Structural) |
| Model family | Deposit-rate framework (reuses #8's two-regime model **by reference** — "identical … with the exception" of line items, PDF p. 215) |
| Subcomponents | Foreign deposits (rate item 43A) and foreign deposits–time (rate item 44B); balances items 35A (non-time) and 35B (time); betas items 83A/83B, 84A/84B |
| Parameters | Median betas — **Table A7**: foreign non-time up 0.890 / down 0.790; foreign time up 1.000 / down 1.000 |
| Notable source-stated assumptions | Foreign time and non-time follow the same model (unlike domestic, where time deposits have their own model #7); re-originations priced at 3M Treasury (worldwide-recession scenario rationale); no exchange-rate effects (PDF p. 216) |
| Open questions | OQ-005, OQ-013, OQ-017, OQ-018, OQ-019, OQ-020, OQ-021 open; OQ-006 resolved |
| Artifacts (integration 2026-07-17) | Chapter `handbook/models/interest-expense/deposits/ie_foreign_dep.md` — REVIEWED; spec `specifications/interest-expense/deposits/ie_foreign_dep.yaml`; review `reviews/interest-expense/deposits/ie_foreign_dep.review.md` (source-faithful) |

## 10. `ie_fed_funds_repo` — Interest Expense on Federal Funds Purchased and Securities Sold under Agreements to Repurchase

| Field | Value |
|---|---|
| Fed name | Interest Expense on Federal Funds Purchased and Securities Sold under the Agreement to Repurchase — v.a(10) heading (PDF pp. 216–219; md sec-205); the Table A6 row and section prose use "…under agreements to repurchase" (plural) — source-internal variant, recorded, not corrected |
| Component / side | Fed funds purchased & repo — interest expense (Table A6: Structural) |
| Model family | Short-rate calculator |
| Projects | `F(b,t) = B(b,t) × Treasury3m(t)` — **Eq A48** (PDF p. 217); asset-side mirror is inside #6 (source-stated equivalence) |
| Firm data inputs | Source-stated: Schedule G NII Worksheet items 44A + 44B — misnamed *rate* items (SQ-16); physical balance items **36A + 36B** [PID-FFR-1, user-confirmed 2026-07-17] |
| Constant over horizon | Balance at PQ0 |
| Integrity flags | SQ-10 (Eq A48 caption "Purchase"); SQ-16 (44A/44B named as balances); CA-2f |
| Open questions | OQ-005, OQ-019 open; OQ-006 resolved (D-004) |
| Artifacts (integration 2026-07-17) | Chapter `handbook/models/interest-expense/funding/ie_fed_funds_repo.md` — REVIEWED; spec `specifications/interest-expense/funding/ie_fed_funds_repo.yaml`; review `reviews/interest-expense/funding/ie_fed_funds_repo.review.md` (APPROVE) |

## 11. `nii_trading_al` — Net Interest Income on Trading Assets and Liabilities

| Field | Value |
|---|---|
| Fed name | Net Interest Income on Trading Assets and Liabilities (PDF pp. 225–230; md sec-215) |
| Component / side | Trading assets and liabilities — **NET item** (interest income minus interest expense; classified under neither side alone). Table A6: Regression |
| Model family | Proposed regression |
| Model | `Ratio(b,t) = β·Treasury3m(t) + α_b + ε(b,t)` — **Eq A52** (PDF p. 225); Ratio = net trading interest income / net trading assets (assets − liabilities); estimated by **WLS weighted by net trading asset balance** per firm-quarter on an unbalanced panel of all FR Y-14Q reporters |
| Data construction (source-stated) | Income/expense numerators = reported average asset (liability) balance × reported average asset (liability) rate ÷ 4 (annual→quarterly), from FR Y-14Q Schedule G NII Worksheet (PDF p. 225) |
| Scenario inputs | 3-month Treasury yield (term spread and BBB spread examined and rejected — collinearity; PDF pp. 226–227) |
| Parameters | β = **0.278\*\*\*** — 1% level (Table A9, PDF p. 234; star-escaping fixed 2026-08-13 — the cell previously rendered as "0.278*"). **Firm fixed effects α_b: estimated but NOT disclosed** (source-stated, PDF p. 234) |
| Projection to dollars | INTERPRETATION — **narrowed 2026-08-13 (PID-TRD-1)**: projected dollars = Ratio(b,q) × net trading assets at PQ0 (constant), with **no further ÷4** (the ÷4 is source-stated inside the ratio's data construction, PDF p. 225); the source states **no projection mechanics at all** (pp. 225–230 image-verified) — OQ-007, narrowed; multiplicand physical rows pending elicitation |
| Fixed-effect values | **PROJECT IMPLEMENTATION DECISION (PID-TRD-1, user-confirmed 2026-08-13; supersedes D-002, which now has no remaining scope):** α_b calibrated in closed form so the nine-quarter cumulative net trading NII equals the residual implied by `frb_total_interest_income` minus the six sibling income models — the PID-OB-5 income-side mirror; PQ0 actuals never used; quarterly-ratio units, **no ×4**; requires the six sibling income paths (project-level execution order) — resolves OQ-009 for this model |
| Rationale for net treatment | Avoids cross-firm comparability issues from balance-sheet offsetting in reported trading assets/liabilities (PDF p. 225) |
| Replaces | Current iv.g (trading-asset income regression, FR Y-9C data BHCK4069/BHCK3545 per footnotes 23–24) + trading-liabilities portion of iv.i(4) (reorganization stated PDF pp. 68, 96; the p. 96 "structural approach" wording for the other-borrowing remainder = SQ-27) |
| Integrity flags | **SQ-26** (Eq A52 where-list omits its dependent variable Ratio(b,t); ratio units also unstated), **SQ-27** (p. 96/A66 "structural approach" vs Regression classification — cross-referenced at #12); both filed 2026-08-13; pp. 225–230 + 234 and comparison pp. 65–68 + 96 image-verified 2026-08-13 |
| Open questions | OQ-005, OQ-007 (narrowed 2026-08-13), OQ-023 (extended 2026-08-13) open; **OQ-009 RESOLVED FOR PROJECT IMPLEMENTATION (PID-TRD-1, 2026-08-13)** — source-side non-disclosure preserved |
| Project implementation decisions | **PID-TRD-1** (2026-08-13): nine-quarter cumulative α_b calibration vs the FRB total-interest-income residual (full text in `handbook/open-questions.md`); open elicitation — physical PQ0 trading-balance rows; residual subtraction basis (securities reinvestment per PID-SEC-8, auto scalar basis per PID-LOAN-32); compare targets at the cell |
| Artifacts (Increment 4) | Chapter `handbook/models/interest-income/trading/nii_trading_al.md` (first asset-side regression chapter — D-009 skeleton + the two `ie_other_borrowing` sections) — **REVIEWED 2026-08-13, user gate pending**; spec `specifications/interest-income/trading/nii_trading_al.yaml`; review `reviews/interest-income/trading/nii_trading_al.review.md` |

## 12. `ie_other_borrowing` — Interest Expense on Other Borrowing

| Field | Value |
|---|---|
| Fed name | Interest Expense on Other Borrowing (PDF pp. 230–234; md sec-220) |
| Component / side | Other borrowing — interest expense (Table A6: Regression). Covers short-term borrowing + subordinated debt + all other interest-bearing liabilities, modeled as a single quantity |
| Model family | Proposed regression |
| Model | `Expense(b,t) = (Treasury3m(t) + δ(b,t)) × B(b,t)` — **Eq A53(1)**; `δ(b,t) = β1·BBB(t) + β2·CommercialPaper(b,t) + β3·Subdebt(b,t) + α_b + ε(b,t)` — **Eq A53(2)** (PDF p. 230). OLS on unbalanced FR Y-14Q panel **2020:Q2–2021:Q4** (deliberately a low-rate window). Projection: `Expense(b,q) = (Treasury3m(q) + δ(b,q)) × B(b,0)` with composition shares frozen at the launch point (PDF p. 231) |
| Firm data inputs | Balances: Schedule G NII Worksheet items 44C (Other Short-Term Borrowing), 46 (Subordinated Notes/TruPS), 47 (Other Interest-Bearing Liabilities) — noting parts of sub debt may sit in 44C/47 per reporting instructions (source-stated); composition shares from FR Y-9C: sub debt BHDM4062 + BHDMC699, commercial paper BHCK2309; physical balance mapping: Schedule G items 36C + 38 + 39 [PID-OB-2, user-confirmed 2026-07-17] |
| Scenario inputs | 3-month Treasury yield; BBB corporate bond yield |
| Parameters | β1 = **0.254**\*\*, β2 = **−0.036**\*\*\*, β3 = **0.066**\*\* (Table A9). **Firm fixed effects α_b: estimated but NOT disclosed** |
| Fixed-effect values | PROJECT IMPLEMENTATION DECISION (PID-OB-5, user-confirmed 2026-07-20; supersedes PID-OB-1/PID-OB-3): α_b calibrated in closed form so the nine-quarter cumulative modeled expense equals the cumulative implied residual vs the FRB total-interest-expense path (`frb_total_interest_expense`, project-supplied input — OQ-023); PQ0 actuals never used; requires the four sibling model expense paths (project-level execution order) |
| Constant over horizon | Balance B(b,0); composition shares at the launch point |
| Absorbs | Current structural sub-debt model iv.m(3) (cf. Question A190: should sub debt stay separate?) |
| Integrity flags | CA-2g/h (stray pipes in where-list); SQ-13 ("(a.)" heading); SQ-17 ("other short-term, borrowing" comma, PDF p. 231); **SQ-27** (current-suite p. 96/Question A66 call this successor a "structural approach" while Table A6/v.d(2) classify it Regression/OLS — filed 2026-08-13 at the #11 chapter drafting; the Regression reading governs, as built) |
| Open questions | OQ-005, OQ-022, OQ-023 open; OQ-006 resolved (D-004); OQ-009 resolved for this model (PID-OB-5; remains open for #11) |
| Artifacts (integration 2026-07-17) | Chapter `handbook/models/interest-expense/funding/ie_other_borrowing.md` — REVIEWED; spec `specifications/interest-expense/funding/ie_other_borrowing.yaml`; review `reviews/interest-expense/funding/ie_other_borrowing.review.md` (APPROVE WITH OPEN IMPLEMENTATION ITEM) |

## 13. `adj_irr_hedge` — Interest-Rate-Risk Hedge Adjustment (cross-cutting)

| Field | Value |
|---|---|
| Fed name | Proposed Adjustments to Pre-Provision Net Revenue Models to Incorporate the Impact of Interest Rate Risk Hedges (PDF pp. 220–225; md sec-210) |
| Component / side | Cross-cutting adjustment to interest income and expense components (not a Table A6 component row) |
| Model family | Hedge adjustment (structural accrual calculator) |
| Scope of hedges | **Accounting hedges only** (qualified hedge-accounting derivatives); non-accounting hedges excluded (cf. Question A187) |
| Model | Per projection quarter PQ: `Hedge NII Impact(PQ) = Accrued Interest Income(PQ) − Accrued Interest Expense(PQ)` — **Eq A49**; fixed leg accrual = Notional × r × N/360 — **Eq A50**; floating leg = Notional × (ReferenceRate + Margin) × N/360 — **Eq A51** (PDF p. 222); caps/floors incorporate strike details; reference rate e.g. SOFR or 3M Treasury |
| Terminated hedges | Hedges terminated before the projection start whose effects persist: cumulative gains/losses spread **evenly over the remaining maturity of the hedged item** (PDF p. 222) |
| Data | **Contingent on proposed FR Y-14Q Schedule B.2 (and B.3) collection**: quarterly snapshots of qualified accounting hedge positions, hedged-portfolio mapping, notional, derivative type, fixed/floating leg details, maturity; possibly terminated-hedge data (PDF p. 221) |
| Not modeled (source-stated) | Future hedge renewals/terminations during the horizon (flat balance-sheet consistency); dynamic re-hedging (PDF p. 223) |
| Interaction with other models | Securities models #3–#5 embed a hedge-income term that is zero until the data exist; loans #1 excludes hedges entirely (Question A159). How the cross-cutting adjustment and the embedded terms divide responsibility per component is not fully specified — OQ-005 |
| Open questions | OQ-005, OQ-006 |

---

## Parameter-table index

| Table | Content | Serves | PDF | Values disclosed? |
|---|---|---|---|---|
| A6 | Component → proposed model type (23 components) | census/reconciliation | pp. 168–169 | Yes (verified) |
| A7 | Median deposit betas, up/down × 5 deposit types | #8, #9 | p. 219 | Yes (verified; SQ-1 label quirk) |
| A8 | Industry scalars, 7 loan portfolios | #1 | p. 220 | Yes (verified; SQ-11 category-count mismatch) |
| A9 | Regression coefficients (β for A52; β1–β3 for A53(2)) | #11, #12 | p. 234 | Macro coefficients yes; **firm fixed effects no** |

## Scenario-variable census (net-interest scope)

| Scenario variable | Used by |
|---|---|
| 3-month Treasury yield | #1 (wholesale base rate), #2, #4/#5 (floating margin index), #6 (α share), #8/#9 (level, change, ELB trigger, floor), #10, #11, #12 (base rate) |
| 1-year Treasury yield | #7 (repricing rate) |
| 10-year Treasury yield | #6 (non-repo share) |
| Prime Rate | #1 (retail variable-rate base; auto/other-consumer spread benchmark) |
| Mortgage rate | #1 (ARM base rate) |
| BBB corporate bond yield | #12 (credit spread driver) |

## Dependency summary (preview of the dependency-map deliverable)

- `ii_loans` ← Retail/Wholesale credit-loss models (loss, prepayment, maturity rates for wt).
- `ii_ust`, `ii_mbs`, `ii_other_sec` ← Securities Model Description (reinvestment assumptions; Agency RMBS vendor prepayment model) and proposed FR Y-14Q B.2/B.3 (hedge legs).
- `adj_irr_hedge` ← proposed FR Y-14Q B.2/B.3 collection; applies across income/expense components.
- `ie_foreign_dep` ← reuses `ie_other_dom_dep` methodology by reference (Eqs A45–A47).
- `ie_fed_funds_repo` ↔ `ii_other_ida`: source states the approaches are equivalent, with asset-side fed funds subsumed in #6.
- No proposed net-interest model consumes another's output; dependencies are on shared inputs, external models, and proposed data collections. **Project-level exception (PID-OB-5, 2026-07-20 — a project calibration, not Fed methodology):** the `ie_other_borrowing` α_b calibration consumes the completed expense paths of `ie_dom_time_dep`, `ie_other_dom_dep`, `ie_foreign_dep`, and `ie_fed_funds_repo` plus the project-supplied `frb_total_interest_expense` path (OQ-023); the Fed-suite independence statement stands as the [FACT]. **Mirrored exception (PID-TRD-1, 2026-08-13):** the `nii_trading_al` α_b calibration consumes the completed income paths of all six income models (#1–#6) plus the project-supplied `frb_total_interest_income` path (OQ-023 extended) — `nii_trading_al` runs last on the income side.

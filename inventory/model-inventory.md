# Model Inventory — Proposed 2026 PPNR Net-Interest Models

**Deliverable 2 of Phase 1, Task 1.** Date: 2026-07-16.
**Every model below is PROPOSED for the 2026 stress test (public-comment stage) — NOT adopted.** Source: Section B.v of the Fed PPNR model documentation (October 2025, updated December 2025). Citations are `(PDF p. N; md sec-M)`; page conventions per `inventory/source-integrity-review.md`.

## Census and reconciliation

Table A6 (PDF pp. 168–169; md sec-148) assigns the 23 PPNR components to four proposed model types. The net-interest portion is 10 structural components + 2 regression components = **12 components**; the cross-cutting interest-rate-risk hedge adjustment (v.c) makes **13 inventory records**. Reorganizations relative to the current 2025 suite (for orientation only):

- Fed funds sold & reverse repo income (current structural model iv.m(1)) is **absorbed into** other interest/dividend-bearing assets (#6) (PDF p. 217; md sec-206).
- Subordinated debt expense (current structural model iv.m(3)) is **absorbed into** other borrowing (#12) (PDF p. 230; md sec-220; Question A190).
- Trading-asset interest income (current iv.g) and the trading-liabilities part of current iv.i(4) become one **net** regression model (#11) (PDF p. 225; md sec-215).

Dimension notation used throughout: `b` = firm, `p` = product, `i` = segment, `t`/`q` = projection quarter, `q0`/`t=0` = lift-off (jump-off) quarter — the last quarter before the projection horizon.

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
| Parameters | Industry scalars — **Table A8** (PDF p. 220), 7 values, supplied; spreads — derived from firm data at lift-off, then constant; no estimated regression coefficients ("does not estimate any components", PDF p. 174) |
| Lift-off inputs | Balance-weighted average jump-off interest rates by segment; percentage of outstanding balance by segment; portfolio balances from FR Y-14 schedules; revolver shares; jump-off spreads |
| Constant over horizon | Balances (flat balance; run-off replenished by same-type new originations within the quarter); spreads; segment composition; revolver share (implied — OQ-012); scalars |
| Varies over horizon | Variable rates (reprice quarterly with base rate); fixed-rate portfolio rate via A38 blending (weight wt from default, prepayment, maturity rates); floors bind when scenario rates fall below stated floor (values unspecified — OQ-002) |
| Upstream dependencies | Retail and Wholesale credit-loss models supply estimated loss/runoff rates for wt (PDF p. 174; OQ-001) |
| Hedge treatment | **Not incorporated** — data limitations; proposed FR Y-14Q B.2 update would add it (Question A159, PDF p. 188) |
| Assumptions (source-stated, PDF p. 184) | (1) flat balance; (2) delinquent loans accrue (impact immaterial); (3) **interest income quarterly compounded**; (4) constant spreads; (5) most variable rates reprice quarterly; (6) segment fixed rates unchanged except new originations; (7) products grouped by similar rate structure |
| Integrity flags | SQ-5 (truncated "sourced from FR." p. 175), SQ-6/SQ-7 (A37/A38 notation), SQ-11 (Table A8 7 rows vs. footnote 63's 8 categories) |
| Open questions | OQ-001, OQ-002, OQ-003, OQ-006, OQ-010, OQ-011, OQ-012, OQ-015 |

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
| Lift-off inputs | Balance B(b,q0) |
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
| Lift-off inputs | t=0 face value, amortized cost, maturity |
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
| Lift-off inputs | B(b,q0) and α(b,q0) |
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
| Firm data inputs | Initial rate: FR Y-14Q Schedule G line item 42E (Time Deposits), jump-off average rate; WAL: Schedule G line item 71 (Domestic Deposits – Time); average balances from FR Y-14Q |
| Scenario inputs | 1-year Treasury yield |
| Parameters | ρ(b) ≡ 1/WAL(b), computed from firm data — constant over horizon; no estimated coefficients |
| Lift-off inputs | Rate(b,0) = jump-off average rate (42E); WAL(b) |
| Constant over horizon | ρ (repricing fraction); balance |
| Varies over horizon | Rate recursion with 1Y Treasury |
| Assumptions (source-stated) | Constant repricing share; re-originations priced at 1Y Treasury (no market power); no contractual maturity structure (Call Report maturity-profile alternative discussed but not proposed, PDF pp. 210–211) |
| Integrity flags | SQ-4 (Questions intro says "interest income") |
| Open questions | OQ-006, OQ-008 |

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
| Firm data inputs | Rates: Schedule G items 42B (MMA), 42C (Savings), 42D (Transaction); betas: items 79A/79B, 80A/80B, 81A/81B; balances per corresponding Y-14Q items; average balance for expense |
| Scenario inputs | 3-month Treasury yield (level and change) |
| Parameters | β_up/β_down per deposit type = **median of firm-reported betas at lift-off** — **Table A7** (PDF p. 219; supplied); Spread(i,b) estimated from 2020:Q2–2021:Q4 data |
| Constant over horizon | Betas; spreads; balances |
| Varies over horizon | Rate path; regime switching on the 3M Treasury path |
| Integrity flags | SQ-1 (Table A7 down-row labels), SQ-2 (caption "(Equations A46)"), SQ-9, SQ-12 |
| Open questions | OQ-006, OQ-013 |

## 9. `ie_foreign_dep` — Interest Expense on Foreign Deposits

| Field | Value |
|---|---|
| Fed name | Interest Expense on Foreign Deposits (PDF pp. 215–216; md sec-201) |
| Component / side | Foreign deposits — interest expense (Table A6: Structural) |
| Model family | Deposit-rate framework (reuses #8's two-regime model **by reference** — "identical … with the exception" of line items, PDF p. 215) |
| Subcomponents | Foreign deposits (rate item 43A) and foreign deposits–time (rate item 44B); balances items 35A (non-time) and 35B (time); betas items 83A/83B, 84A/84B |
| Parameters | Median betas — **Table A7**: foreign non-time up 0.890 / down 0.790; foreign time up 1.000 / down 1.000 |
| Notable source-stated assumptions | Foreign time and non-time follow the same model (unlike domestic, where time deposits have their own model #7); re-originations priced at 3M Treasury (worldwide-recession scenario rationale); no exchange-rate effects (PDF p. 216) |
| Open questions | OQ-006, OQ-013 |

## 10. `ie_ffp_repo` — Interest Expense on Federal Funds Purchased and Securities Sold under Agreements to Repurchase

| Field | Value |
|---|---|
| Fed name | Interest Expense on Federal Funds Purchased and Securities Sold under the Agreement to Repurchase (PDF pp. 216–219; md sec-205) |
| Component / side | Fed funds purchased & repo — interest expense (Table A6: Structural) |
| Model family | Short-rate calculator |
| Projects | `F(b,t) = B(b,t) × Treasury3m(t)` — **Eq A48** (PDF p. 217); asset-side mirror is inside #6 (source-stated equivalence) |
| Firm data inputs | Balances: Schedule G NII Worksheet items 44A (federal funds purchased) + 44B (securities sold under agreements to repurchase) |
| Constant over horizon | Balance at q0 |
| Integrity flags | SQ-10 (Eq A48 caption "Purchase"); CA-2f |
| Open questions | OQ-006 |

## 11. `nii_trading_al` — Net Interest Income on Trading Assets and Liabilities

| Field | Value |
|---|---|
| Fed name | Net Interest Income on Trading Assets and Liabilities (PDF pp. 225–230; md sec-215) |
| Component / side | Trading assets and liabilities — **NET item** (interest income minus interest expense; classified under neither side alone). Table A6: Regression |
| Model family | Proposed regression |
| Model | `Ratio(b,t) = β·Treasury3m(t) + α_b + ε(b,t)` — **Eq A52** (PDF p. 225); Ratio = net trading interest income / net trading assets (assets − liabilities); estimated by **WLS weighted by net trading asset balance** per firm-quarter on an unbalanced panel of all FR Y-14Q reporters |
| Data construction (source-stated) | Income/expense numerators = reported average asset (liability) balance × reported average asset (liability) rate ÷ 4 (annual→quarterly), from FR Y-14Q Schedule G NII Worksheet (PDF p. 225) |
| Scenario inputs | 3-month Treasury yield (term spread and BBB spread examined and rejected — collinearity; PDF pp. 226–227) |
| Parameters | β = **0.278*** (Table A9, PDF p. 234). **Firm fixed effects α_b: estimated but NOT disclosed** (source-stated, PDF p. 234) |
| Projection to dollars | INTERPRETATION (working method per decision D-002): apply projected Ratio to net trading assets at lift-off (constant-balance assumption); the ratio→dollar step is not spelled out in the source — OQ-007 |
| Fixed-effect values | CODING CONSIDERATION (per D-002): backsolve α_b from lift-off actuals; flagged INTERPRETATION everywhere — OQ-009 |
| Rationale for net treatment | Avoids cross-firm comparability issues from balance-sheet offsetting in reported trading assets/liabilities (PDF p. 225) |
| Replaces | Current iv.g (trading-asset income regression) + trading-liabilities portion of iv.i(4) |
| Open questions | OQ-007, OQ-009 |

## 12. `ie_other_borrowing` — Interest Expense on Other Borrowing

| Field | Value |
|---|---|
| Fed name | Interest Expense on Other Borrowing (PDF pp. 230–234; md sec-220) |
| Component / side | Other borrowing — interest expense (Table A6: Regression). Covers short-term borrowing + subordinated debt + all other interest-bearing liabilities, modeled as a single quantity |
| Model family | Proposed regression |
| Model | `Expense(b,t) = (Treasury3m(t) + δ(b,t)) × B(b,t)` — **Eq A53(1)**; `δ(b,t) = β1·BBB(t) + β2·CommercialPaper(b,t) + β3·Subdebt(b,t) + α_b + ε(b,t)` — **Eq A53(2)** (PDF p. 230). OLS on unbalanced FR Y-14Q panel **2020:Q2–2021:Q4** (deliberately a low-rate window). Projection: `Expense(b,q) = (Treasury3m(q) + δ(b,q)) × B(b,0)` with composition shares frozen at lift-off (PDF p. 231) |
| Firm data inputs | Balances: Schedule G NII Worksheet items 44C (Other Short-Term Borrowing), 46 (Subordinated Notes/TruPS), 47 (Other Interest-Bearing Liabilities) — noting parts of sub debt may sit in 44C/47 per reporting instructions (source-stated); composition shares from FR Y-9C: sub debt BHDM4062 + BHDMC699, commercial paper BHCK2309 |
| Scenario inputs | 3-month Treasury yield; BBB corporate bond yield |
| Parameters | β1 = **0.254**\*\*, β2 = **−0.036**\*\*\*, β3 = **0.066**\*\* (Table A9). **Firm fixed effects α_b: estimated but NOT disclosed** |
| Fixed-effect values | CODING CONSIDERATION (per D-002): backsolve α_b from lift-off actuals; flagged INTERPRETATION — OQ-009 |
| Constant over horizon | Balance B(b,0); composition shares at lift-off |
| Absorbs | Current structural sub-debt model iv.m(3) (cf. Question A190: should sub debt stay separate?) |
| Integrity flags | CA-2g/h (stray pipes in where-list); SQ-13 ("(a.)" heading) |
| Open questions | OQ-006, OQ-009 |

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
- `ie_ffp_repo` ↔ `ii_other_ida`: source states the approaches are equivalent, with asset-side fed funds subsumed in #6.
- No proposed net-interest model consumes another's output; dependencies are on shared inputs, external models, and proposed data collections.

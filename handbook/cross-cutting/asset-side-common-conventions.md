# Asset-Side Common Conventions

> **STATUS: The underlying models are proposed for the 2026 stress test — public-comment stage, NOT adopted.**
> Created at Increment 1 of the asset-side roadmap, 2026-07-23. Scope: the six interest-income
> components `ii_loans`, `ii_dep_banks_other`, `ii_ust`, `ii_mbs`, `ii_other_sec`, `ii_other_ida`
> and the net component `nii_trading_al`. This chapter records only conventions genuinely shared
> across those models plus the family grouping that organizes the work; individual model equations
> live in the model chapters and are **not** repeated here. Sections covering families not yet
> chaptered cite the approved `inventory/model-inventory.md` records (#1–#6, #11) and are extended
> at each family increment. Navigation: `inventory/asset-side-model-matrix.md`. Decisions cited
> (D-/PID-) are user-confirmed project implementation decisions registered in
> `handbook/open-questions.md` — never attributable to the Federal Reserve.

## 1. Family grouping (project workflow structure, 2026-07-23)

The seven components divide into four structural families. The grouping is a **project
organization** of the Fed's own equation structure — the source presents the models as
independent siblings (Table A6, PDF pp. 168–169; md sec-148):

| Family | Components | Shared structure | Fed-shared machinery |
|---|---|---|---|
| A — calculators | `ii_dep_banks_other` (Eq A39), `ii_other_ida` (Eq A43) | balance × contemporaneous Treasury yield(s); no parameters | None — same *form*, independent sections; kept as separate models |
| B — securities | `ii_ust` (Eq A40), `ii_mbs` (Eq A41), `ii_other_sec` (Eq A42) | one three-term template: coupon accrual + accretion/amortization + hedge income (= 0 pending data) | The three-term template itself; shared reinvestment assumption (Securities Model Description, OQ-004); floating-margin imputation off 3M Treasury |
| C — loans | `ii_loans` (Eq A32; rate machinery A33–A38) | income = balance × rate per product/segment; fixed/variable rate machinery shared across the six portfolios | A33–A38 shared *inside* the one loans model (D-003: one chapter, six portfolio sections) |
| D — regression | `nii_trading_al` (Eq A52) | WLS panel ratio model; β on 3M Treasury + undisclosed firm fixed effects (Table A9) | None with the other income models; project analog: the `ie_other_borrowing` calibration pattern (D-002 / OQ-009) |

Sharing rule (inherited from the liability side): **share exactly what the Fed shares** — a
common engine only where the source literally states one template (Family B; A33–A38 within
loans); everything across families stays unharmonized (cf.
`handbook/cross-cutting/liability-side-common-conventions.md` §8).

## 2. Launch-point terminology (D-005)

- **Launch point (PQ0)** is the handbook's term for the last quarter before the projection
  horizon. The source's own words — "lift-off", "jump-off quarter", "$q0$", "$t=0$" — are
  preserved verbatim inside quotations and equation transcriptions and are never rewritten.
- Coding identifiers use the `_launchpoint` suffix for PQ0 snapshots.
- Projection quarters are t (or q) = 1…9 — the nine-quarter horizon (FACT, PDF p. 6; md sec-2).

## 3. Canonical inputs and normalization

- Scenario series carry shared canonical names across models. Income side adds three series to
  the expense-side set: `usd_10y_treasury` (`ii_other_ida`), `prime_rate` and `mortgage_rate`
  (`ii_loans` retail/ARM base rates — inventory #1). `usd_3m_treasury` is shared with the
  expense side (`ii_dep_banks_other`, `ii_other_ida`, wholesale loans base rate, securities
  floating-margin index, `nii_trading_al` driver).
- Firm inputs are model-prefixed; primary outputs end in `_interest_income`. The net component's
  output is `trading_net_interest_income` — a NET quantity (income minus expense; inventory #11),
  deliberately not suffixed like the one-sided outputs.
- **Rate-scale normalization**: percent vs. decimal is metadata-driven at ingestion, never
  assumed (D-006 discipline applies to money rows: USD millions canonical, declared `scale`).
- Physical scenario sourcing follows the PID-5 pattern (MEV workbook, one column per MEV).
  Column names for all three new income series are **UNCONFIRMED** working assumptions until
  company-side confirmation.

## 4. Annualized rates and the single ÷4 (D-004) — with income-side source-stated exceptions

- All interest rates in the project are **annualized**; a quarterly dollar flow divides the
  annualized rate by four only at the final quarterly-dollar step. Never presented as a Fed
  statement.
- **Where the source states its own conversion, the source governs** (OQ-006 resolution). On the
  asset side this matters more than on the liability side, because the securities models state
  their ÷4 **inside** the equations: coupon accrual = face × CouponRate/4 (Eq A40/A41), combined
  coupon+accretion = amortized cost × BookYield/4 (Eq A42), and the trading-NII data construction
  divides annual rates by four (inventory #3, #4, #5, #11 with page cites). For those terms the
  ÷4 is [FACT], not D-004; the D-004 label applies only where the source is silent (the Family A
  calculators; the loans income step, where "interest income is quarterly compounded" is stated
  as an assumption without a rate basis — OQ-006 preserved absence, inventory #1).

## 5. Projection-quarter alignment and PQ0 scenario needs

- Scenario paths are aligned to PQ1…PQ9 per scenario, with no gaps, before any model runs.
- PQ0 scenario values are consumed only where a model's mechanics require them. Known asset-side
  cases: the securities floating-margin imputation uses the **t = 0 spot** 3-month Treasury
  (margin = t0 coupon − t0 spot 3M; inventory #4/#5), and the loans fixed-rate machinery anchors
  spreads at t = 0 (Eq A33's Spread(t=0); inventory #1). The Family A calculators need no PQ0
  scenario value. Pre-PQ0 **history** (e.g., the Eq A37 wholesale base rate at the median
  origination date t−a) never enters the scenario container — such quantities are supplied
  launch-point firm inputs (OQ-003; the liability-side `elb_spread` precedent).
- Outputs are dimensioned firm × scenario × quarter.

## 6. Constant balances and composition

The constant-balance convention is stated **per component**, not centrally — the sentence "The
stress test assumes constant balances for all firms…" appears in each calculator section
([FACT]: `ii_dep_banks_other` PDF p. 189, md sec-174; `ii_other_ida` PDF p. 207, md sec-190 —
which adds the constant share α(b,q) = α(b,q0)). The other families state their own versions:

- `ii_loans`: flat balances with run-off replenished by same-type re-origination within the
  quarter; spreads, segment composition, revolver share (implied — OQ-012), and scalars constant
  (inventory #1, PDF pp. 173–174, 184).
- `ii_ust` / `ii_mbs` / `ii_other_sec`: constant balance **via the reinvestment assumption**
  (maturing securities replaced) — detailed in the separate Securities Model Description
  (footnotes 64–65; OQ-004, collection approved 2026-07-23).
- `nii_trading_al`: constant net trading assets at the launch point is the project's working
  interpretation for the ratio→dollar step (OQ-007) — not source-stated.

Chapters restate their own component's constancy register; this section only fixes the pattern:
**what is constant is per-model [FACT or flagged INT], never a global assumption.**

## 7. Separation of data retrieval from model calculation

- Every input carries two layers, kept separate in chapters and specs: the **Fed-stated** source
  (`fed_item` — or UNKNOWN as a preserved fact of absence) and the **project physical mapping**
  (`project_mapping`, PID-labeled once user-confirmed). The physical layer governs
  implementation; the Fed-stated layer is never silently corrected.
- Asset-side note: unlike the deposit-expense models, the Family A calculators have
  **source-stated** balance items (item 14; item 15 — both verified against page images
  2026-07-23), so their Fed layer needs no correction PID; only the physical sheet rows await
  confirmation. The loans and securities families will need substantially more mapping work
  (segment-level and bucket-level inputs — settled at their increments).
- Model calculation consumes canonical inputs only; retrieval, normalization, and mapping happen
  before the model layer. No model reads a raw report field directly.

## 8. Common validation principles

- Required inputs present per firm; failures **surface as errors — no fallback value is
  invented** and nothing defaults silently. `TO_BE_CONFIRMED` placeholders refuse to run
  (ingestion `require_confirmed` gate).
- Supplied parameters (Table A8 loan scalars; Table A9 trading-NII β) are verified against the
  PDF page values; significance stars are metadata, never numeric inputs.
- Shares validated in [0,1] and never clipped (`ii_other_ida` α; loans segment shares; revolver
  share); violations surface.
- Edge monitors **log, never clamp**: negative projected rates and sign-flipped income legs are
  legal model outputs wherever no constraint exists in the source. Loans floors are the
  exception: a Fed-**stated** bind ("will bind if the projected interest rate decreases to the
  stated floor", inventory #1/OQ-002) — a modeled clamp with binding diagnostics, not a
  validation clamp.
- Flat-balance and constancy invariants are asserted per §6.

## 9. Cross-cutting hedge-adjustment boundary (OQ-005) — asset-side data states

- The Family A calculators and `nii_trading_al` contain no hedge term [FACT absence per
  section]. The three securities models **embed** a Hedge Income term that "will be zero" until
  the proposed FR Y-14Q B.2/B.3 collection exists; loans exclude hedges entirely (Question A159)
  (inventory #1, #3–#5).
- The Section v.c adjustment (Equations A49–A51; qualified accounting hedges; PDF pp. 220–225)
  is a separate cross-cutting calculation owned by the planned hedge chapter. Every asset-side
  chapter presents two data states: current (embedded hedge terms zero; no component-level
  adjustment computable) and proposed-collection (embedded terms and/or v.c computable).
- How the embedded per-security terms and the v.c adjustment divide responsibility **without
  double counting** is unresolved — OQ-005, OPEN. Models only expose pre-hedge income paths.

## 10. FRB-provided paths and the family reconciliation boundary

- The FRB provides the firm three projection paths (user-stated, OQ-023 narrowing):
  total interest income, total interest expense, and net interest income. The asset-side family
  consumes `frb_total_interest_income` as a **monitor** target; `frb_net_interest_income`
  supports the NII = II − IE identity guard. These are project-supplied inputs, never Fed
  statements — Section v models each component independently [FACT absence of any aggregation].
- Whether `nii_trading_al` plays a residual-calibration role against the FRB income total
  (mirroring PID-OB-5 on the expense side), and how a NET item maps into a gross income total,
  is an **open project decision** scheduled for the Increment 4 gate (successor to D-002 /
  OQ-007 / OQ-009 for this model). Until decided, family reconciliation runs in monitor mode
  (differences reported, nothing forced).

## 11. What is deliberately not shared

The seven components keep distinct calculation forms (two one-line calculators of different
arity; a three-term securities template with three accretion variants; a six-portfolio loan
engine with fixed/variable machinery; a WLS panel regression). Different scenario drivers
(3M / 10Y / Prime / mortgage rate), different data grains (component scalar vs. bucket vs.
segment vs. security-level vs. panel ratio), and different parameter sets (none / Table A8 /
Table A9). These are genuine methodology differences and must never be harmonized into a common
formula — the family grouping in §1 bounds sharing; it never licenses it beyond what the source
states.

## 12. Securities family shared machinery (added at Increment 2, 2026-07-23)

Stated once here; the three securities chapters (`ii_ust`, `ii_mbs`,
`ii_other_sec`) cross-reference this section and carry only their deviations
(D-003 cross-reference pattern).

- **Three-term template [FACT, per section]:** Interest Income(i,t) = Coupon
  Accrual(i,t) + AccretionAmortization(i,t) + Hedge Income(d,t), per security i
  and derivative d — Eq A40 (PDF p. 191), Eq A41 (PDF p. 196), Eq A42 (PDF
  p. 201; combined coupon+accretion form). The ÷4 conversions here are
  **source-stated inside the equations** (CouponRate/4; BookYield/4;
  (PayRate−ReceiveRate)/4) — the source governs, not D-004 (§4 above).
- **Hedge-income data states [FACT]:** FR Y-14Q Schedule B.2 currently lacks
  leg-level fields, so "the initial assumption for Hedge Income(d,t) will be
  zero"; proposed B.2/B.3 revisions would enable the in-model term; a Portfolio
  Layer Method hedge's income is computed separately and added to the firm-level
  aggregate for the most prevalent securities type in the closed portfolio
  (PDF pp. 192, 197, 202–203). Division of responsibility with the cross-cutting
  v.c adjustment remains OQ-005 (§9 above).
- **Reinvestment [FACT + INT]:** each section states: constant balance is
  maintained via a reinvestment assumption; reinvestments replace securities that
  pay down; "The same reinvestment assumption is used across both the interest
  income on securities models and the Securities Model"; and, for coupon accrual,
  "all purchases in future quarters are made on the first day of the quarter
  subsequent to the maturing quarter of the security" (PDF pp. 192–193, 198,
  203). The detail lives in the collected second source (OQ-004 resolution):
  proceeds are reinvested into a **hypothetical one-year U.S. Treasury,
  purchased at face value, issued on the purchase date, with coupon equal to the
  par Treasury curve yield at the forecast quarter**; accounting intent (AFS/HTM)
  preserved; **no hedges on reinvestments** (MRM pp. 72–74, §(vii) Reinvestment
  Methodology — see `sources/fed/market-risk-models-securities-extracts.md`).
  [INT, strong basis]: that passage is the referenced assumption — it explicitly
  names "the proposed structural model for interest income on securities, as
  detailed in the PPNR Model documentation" (MRM p. 73). Residual income-side
  mechanics are **OQ-025**; income-side consequences [INT]: a reinvestment
  purchased at face value carries no discount/premium, so it contributes coupon
  accrual only (no accretion), at the 1-year Treasury yield of its purchase
  quarter, from the first day of the quarter after maturity.
- **Floating-rate margin imputation [FACT — `ii_mbs` and `ii_other_sec` only]:**
  margin data are unavailable, so "the model will impute the margin assuming an
  index of the 3-month Treasury": margin = t=0 coupon − t=0 **spot** 3-month
  Treasury; the margin is added to the scenario 3-month Treasury in all forward
  quarters (PDF pp. 196, 201). This is the reason `IncomeScenarioPaths` carries
  the PQ0 value of `usd_3m_treasury` (§5 above).
- **Second-source citation rule:** cite the Market Risk Models volume as
  `(MRM p. N)`; its equation labels ("Equation A-3", "A-32") numerically collide
  with PPNR equation names — never cite an equation number without the document
  prefix.
- **Input granularity [CODE — gate proposal, candidate PID-SEC-1]:** the Fed
  computes at security level (FR Y-14Q Schedule B.1 + vendor data). The project
  proposes **pre-aggregated bucket inputs** through the existing two-sheet
  contract (closed `subcomponent` sets per model), with the Agency RMBS vendor
  income entering as a declared quarterly input path (candidate PID-MBS-1) — the
  Fed-stated security-level layer is recorded as [FACT] in the chapters; the
  bucket contract is a project decision pending user confirmation at the
  Increment 2 gate. A third `[firm_data.positions]` sheet stays reserved if
  security-level granularity is ever chosen instead.

# 3. Interest Income on U.S. Treasuries (`ii_ust`)

> **STATUS: Proposed for the 2026 stress test — public-comment stage, NOT adopted.**
> Source: Section B.v.a(3) (PDF pp. 190–195; md sec-177–180). Model type per Table A6: **Structural** (PDF pp. 168–169; md sec-148). Second source for the delegated reinvestment detail: MRM Section A (`sources/fed/market-risk-models-securities-extracts.md`; OQ-004 resolution).
> Integrity flags: **SQ-3** — this section's Questions are numbered A161–A164, colliding with component (2)'s A161/A162 (cite Board questions with their section). Equation A40's accretion denominator prints "**Maturity in Quarter**" (singular) — verified in the PDF text layer 2026-07-23; preserved verbatim, plainly meaning maturity measured in quarters.
> Shared machinery: three-term template, hedge data states, reinvestment mechanics, and the granularity proposal are stated once in `handbook/cross-cutting/asset-side-common-conventions.md` §12 and cross-referenced here (D-003 pattern).
> Chapter review state: **DRAFTED + source-grounding review this session (`reviews/interest-income/securities/ii_ust.review.md`) — AWAITING USER REVIEW (Increment 2 gate).** Specification: `specifications/interest-income/securities/ii_ust.yaml`.
> Labels: **[FACT]** = Fed statement (cited); **[PID]** = project implementation decision (user-confirmed); **[INT]** = interpretation; **[CODE]** = coding consideration; **[OQ]** = open question.

## 1. Status and purpose

- [FACT] "The Board proposes an alternative structural approach to model interest income on U.S. Treasuries and U.S. Government agency obligations (excluding mortgage-backed securities) that is based on security-level microdata available in form FR Y-14Q, Schedule B." (PDF p. 190; md sec-177).
- [FACT] Approach: income = sum of "(a) coupon accruals for securities, (b) the amortization/accretion of amortized cost, and (c) the income impacts from any qualifying accounting hedges associated with the security", using "bond-specific details from FR Y-14Q, Schedule B.1 along with vendor data, including coupon rate and maturity" (PDF p. 190; md sec-177).
- [FACT] Rationale vs. the current panel regressions: closer to business-as-usual accounting calculations; interpretable against security characteristics and scenarios; instrument-specific characteristics "cannot be inferred from prior observations of aggregate income on securities by type as reported in FR Y-9C" (PDF pp. 190–191; md sec-177). Current model = panel regression [FACT, Question A161 wording of this section] — current-suite mechanics out of scope.
- **Model type: structural calculator on security-level data.** No estimated parameter anywhere in v.a(3); Tables A7–A9 contain no row for this component [FACT absence].

## 2. Model summary

Per security i (and derivative d), quarterly income = coupon accrual + straight-line accretion/amortization + hedge income (initially zero) — the family three-term template (conventions §12) with the **U.S. Treasuries variant**: accretion is straight-line on **t=0** face and amortized cost over the **t=0 maturity in quarters**; no prepayment; no floating-margin imputation appears in this section [FACT absence — Treasuries are fixed-coupon or bills]. Maturities are incorporated; constant balance is maintained by the shared reinvestment assumption (hypothetical 1-year Treasury — conventions §12; MRM pp. 72–74).

## 3. Inputs

### 3.1 Firm data inputs (security-level [FACT]; bucket proposal [CODE] in §9)

| Input | Source | Dimensions | Units | Timing | Label |
|---|---|---|---|---|---|
| Current face value (`current_face_value`) | FR Y-14Q Schedule B.1 | i, t | USD (millions at boundary, D-006) | Beginning-of-period, per quarter; changes as securities mature/reinvest | [FACT] (PDF pp. 190–192; md sec-177–178) |
| Coupon rate (`coupon_rate`) | **Vendor data** — "which in some cases may not be available"; **no fallback stated for this component** | i, t | Annualized rate | Per security | [FACT] + [FACT absence — OQ-027] (PDF pp. 191–192; md sec-178) |
| Amortized cost at t=0 (`amortized_cost_launchpoint`) | FR Y-14Q Schedule B.1 | i | USD | Launch point | [FACT] (PDF p. 191; md sec-178) |
| Maturity in quarters at t=0 (`maturity_quarters_launchpoint`) | Vendor data ("maturity") / Schedule B.1 | i | Quarters | Launch point | [FACT] (PDF pp. 190–191; md sec-177–178) |
| Hedge legs (notional, pay rate, receive rate) | Proposed FR Y-14Q Schedule B.2/B.3 — **not currently collected** | d, t | USD; annualized rates | Future data state | [FACT] (PDF p. 192; md sec-178); conventions §12 |

### 3.2 Scenario inputs

- **Existing book: none.** [FACT absence — Equation A40 contains no scenario variable; coupons and the accretion schedule come entirely from security data.]
- **Reinvestment coupon:** the 1-year par Treasury yield at the purchase quarter [FACT — MRM p. 73; conventions §12]. [INT/CODE] Project mapping: the canonical `usd_1y_treasury` MEV (already confirmed for `ie_dom_time_dep`); whether the scenario's 1Y Treasury series equals "the corresponding yield from the par Treasury curve" is an implementation mapping — OQ-025(d).

### 3.3 Parameters

**None.** [FACT] No estimated or supplied parameter; Tables A7–A9 contain no row for this component.

## 4. Timing and dimensions

- Dimensions: i = security; d = derivative; b = firm (aggregation); q/t = 1…9 (PDF p. 6; md sec-2). Output grain: firm × scenario × quarter after aggregation across securities.
- Launch-point quantities: face(t=0), amortized cost(t=0), maturity(t=0) per security [FACT].
- [FACT] Constant balance **via reinvestment**, not via frozen faces: "the model also incorporates the maturity of securities. To maintain a constant balance assumption, the Board uses a reinvestment assumption." (PDF pp. 192–193; md sec-178). Purchases occur "on the first day of the subsequent quarter to the maturing quarter" [FACT, PDF p. 193].
- [FACT — MRM fn 54, p. 68] A matured security "ceases to exist after maturity, and projections are not generated for this security in subsequent quarters" (stated for the Securities Model's alternative framework; applied here as the income-side reading [INT]).

## 5. Equations and variable definitions

[FACT] Verified against the PDF page image (p. 191) this session; spelling of the accretion term confirmed via the PDF text layer ("AccretionAmortization" — correctly spelled in A40).

**Equation A40** – Interest Income on U.S. Treasuries Projection:

$$Interest\ Income_{i,t} = Coupon\ Accrual_{i,t} + AccretionAmortization_{i,t} + Hedge\ Income_{d,t}$$

Where-list [FACT, verbatim]:

- $Coupon\ Accrual_{i,t} = Current\ Face\ Value_{i,t} \times \frac{Coupon\ Rate_{i,t}}{4}$ — the ÷4 is **source-stated** (conventions §12; not D-004);
- $AccretionAmortization_{i,t} = \frac{Current\ Face\ Value_{i,t=0} - Amortized\ Cost_{i,t=0}}{Maturity\ in\ Quarter_{i,t=0}}$ — **t=0 numerator and denominator**: a constant per-quarter straight-line amount per security ("Maturity in Quarter" singular preserved verbatim — banner);
- $Hedge\ Income_{d,t} = Notional\ Amount_{d,t} \times \frac{Pay\ Rate_{d,t} - Receive\ Rate_{d,t}}{4}$ — initially zero (conventions §12).

- [FACT] "Coupon accrual is calculated using the beginning-of-the-period current face value at time t"; coupon rates from vendor data "may not be available" (PDF p. 192; md sec-178).
- [FACT] "Accretion/Amortization is calculated using the straight-line method for this subset of securities." (PDF p. 192.)
- [INT] Contrast with `ii_mbs`: A41's accretion numerator is dated t, A40's is dated t=0 — preserved as printed, not harmonized.

## 6. Calculation workflow

1. **Launch-point extraction.** Per security: face(0), coupon rate, amortized cost(0), maturity in quarters(0) (§3.1). Validate per §10.
2. **Existing-book coupon accrual.** Per quarter, sum face(i,t) × coupon(i)/4 over securities alive at t (face is beginning-of-period; a security contributes through its maturing quarter [INT — beginning-of-period convention]).
3. **Existing-book accretion.** Per quarter, sum the constant (face(i,0) − AC(i,0)) ÷ maturity_quarters(i,0) over securities alive at t; contributions cease after maturity [INT per §4's MRM fn 54 reading].
4. **Reinvestment income.** Matured face → hypothetical 1-year Treasury purchased at face value on the first day of the following quarter; coupon = 1Y par Treasury yield at that quarter [FACT — MRM p. 73]; income = reinvested balance × y1(purchase quarter)/4 from the purchase quarter onward; no accretion (purchased at face → no discount/premium [INT]); no hedges on reinvestments [FACT — MRM p. 73]. Roll-again of reinvestments maturing inside the horizon: UNKNOWN — OQ-025(a).
5. **Hedge income.** Zero in the current data state [FACT]; per-derivative formula plus Portfolio-Layer-Method allocation if B.2/B.3 data arrive (conventions §12).
6. **Aggregation and hand-off.** Sum across securities to the firm × scenario × quarter income path; expose pre-hedge path to family aggregation and the v.c boundary (§11).

## 7. Output calculation

- Output: `ust_interest_income` (USD millions/quarter, D-006), firm × scenario × quarter.
- The ÷4 conversions are **inside the source-stated equations** (coupon/4; hedge (Pay−Receive)/4); the accretion term is already a quarterly amount [FACT]. D-004 is not invoked for this model (source governs — conventions §12; OQ-006 language).

## 8. Fed-stated assumptions and limitations

All [FACT] (PDF pp. 193–194; md sec-179), restated faithfully:

1. **Hedge-data gap.** Pay-fixed swaps "change the income stream to that of a floating instrument"; current Schedule B.2 "do[es] not allow for independent calculation" — no leg-level fields; without the proposed B.2/B.3, "the Board will need to identify other alternative data sources."
2. **Reinvestment materiality.** "The reinvestment assumption can have a material impact on interest income on securities. … the choice not to apply hedges against reinvestments and the coupon type (i.e., fixed/floating) of those reinvestments have an outsized impact on income model results."
3. **Stated exclusions.** OCI releases from AFS→HTM transfers; income from previously terminated hedges (the latter "discussed in more detail in the section on proposed treatment of interest rate risk hedges").

Public-input request: Questions A161–A164 of section v.a(3) (PDF pp. 194–195; md sec-180; SQ-3 collision — banner). A164 concerns the reinvestment strategy "detailed within the Securities Model Description".

## 9. User-confirmed implementation mappings

None yet. Pending gate decisions and [CODE] items (candidate PIDs at the Increment 2 gate and company-reference verification):

| Item | Decision / working assumption | Status |
|---|---|---|
| Input granularity | **Security-level** positions contract (per-security face, coupon, AC, maturity); aggregation inside the model | **PID-SEC-1, user-confirmed 2026-07-23** (sheet layout pending the user's format upload) |
| Reinvestment | `usd_1y_treasury` = par-curve 1Y yield [OQ-025(d) resolved]; coupon **fixed at the purchase-quarter yield for the 4-quarter window**; **rolls again** at maturity [OQ-025(a) resolved]; attribution stays in-component [OQ-025(b) resolved] — all user-confirmed 2026-07-23 | CONFIRMED |
| Unsettled transactions | AC proxy = purchase price/100 × notional | **PID-SEC-3, user-confirmed 2026-07-23** (company convention) |
| Coupon-accrual face | Prior-quarter EOP current face | **PID-SEC-4, user-confirmed 2026-07-23** |
| Missing vendor coupon fallback | None stated for this component [FACT absence]; do **not** silently adopt the `ii_mbs` book-yield fallback without confirmation | OQ-027 — OPEN |

## 10. Validation requirements ([CODE] — non-normative)

- Per security (or bucket): non-negative face; maturity_quarters > 0; finite amortized cost; coupon present (missing → error naming OQ-027, no invented fallback).
- Accretion sign follows discount/premium (face vs. amortized cost) — either sign legal; log large magnitudes.
- Reinvestment ledger conservation: cumulative reinvested balance equals cumulative matured face (no leakage); reinvested income starts the quarter **after** maturity, never the maturing quarter.
- `usd_1y_treasury` present for all quarters with a maturity event; negative yields logged, never clamped.
- Hedge term identically zero in the current data state; a nonzero hedge input without the B.2/B.3 data state declared is an error.

## 11. Dependencies and hedge interface

- Upstream: FR Y-14Q Schedule B.1 + vendor data [FACT]; the shared reinvestment assumption with the Securities Model (MRM Section A — conventions §12) [FACT]. No other income model's output is consumed.
- Hedge boundary: embedded Hedge Income currently zero; cross-cutting v.c adjustment external; allocation and double-counting unresolved — OQ-005 (conventions §9/§12). This model exposes a pre-hedge income path.
- Family-level: feeds asset-side aggregation and the `frb_total_interest_income` monitor (conventions §10).

## 12. Open issues

- [OQ-004 — RESOLVED 2026-07-23] Securities Model Description collected and the reinvestment/vendor passages extracted (banner; conventions §12).
- [OQ-025 — OPEN, filed this session] Reinvestment income residuals: (a) roll-again of matured reinvestments; (b) uniform-into-Treasuries reading and component attribution of reinvestment income; (d) par-curve → `usd_1y_treasury` mapping; (e) "current reinvestment assumption" wording inside Alternative Approaches — adoption status (MRM Question A1).
- [OQ-027 — OPEN, filed this session] Missing vendor-coupon fallback unstated for this component (§3.1/§9).
- [OQ-005 — OPEN] Hedge-adjustment allocation (§11).
- [SQ-3 — filed 2026-07-16] Question-numbering collision (banner).
- [CODE] Granularity gate decision (§9, candidate PID-SEC-1).

## 13. Key source references

| Claim | Citation |
|---|---|
| Component proposal; security-level microdata; three-summand approach; Schedule B.1 + vendor data | (PDF p. 190; md sec-177) |
| Equation A40 + where-list (incl. "Maturity in Quarter" singular); beginning-of-period face; vendor coupon availability caveat; straight-line accretion; hedge zero + B.2/B.3 + Portfolio Layer Method | (PDF pp. 191–192; md sec-178) |
| Maturity incorporation; reinvestment assumption; same-assumption statement; referral to the Securities Model Description (fn 64); first-day-of-subsequent-quarter purchases | (PDF pp. 192–193; md sec-178) |
| Assumptions: hedge-data gap; reinvestment materiality; OCI-release and terminated-hedge exclusions | (PDF pp. 193–194; md sec-179) |
| Questions A161–A164 (SQ-3) | (PDF pp. 194–195; md sec-180) |
| Reinvestment instrument detail (1Y Treasury at face, par-curve coupon, AFS/HTM intent, no hedges); explicit PPNR income-model cross-link | (MRM pp. 72–74; extracts §5) |
| Matured security ceases to exist; proceeds reinvested and revalued | (MRM p. 68 fn 54; extracts §5) |
| Table A6 row (Structural); nine-quarter horizon | (PDF pp. 168–169, 6; md sec-148, sec-2) |
| D-004 boundary (source-stated ÷4 governs); D-005; D-006 | `handbook/open-questions.md`; conventions §4/§12 |

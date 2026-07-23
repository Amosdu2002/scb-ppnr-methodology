# 4. Interest Income on Mortgage-Backed Securities (`ii_mbs`)

> **STATUS: Proposed for the 2026 stress test — public-comment stage, NOT adopted.**
> Source: Section B.v.a(4) (PDF pp. 195–200; md sec-181–184). Model type per Table A6: **Structural** (PDF pp. 168–169; md sec-148). Second source for the delegated vendor-model and reinvestment detail: MRM Section A (`sources/fed/market-risk-models-securities-extracts.md`; OQ-004 resolution; PPNR fn 65).
> Integrity flags: **CA-2d** — md line 3933 carries a stray `|` after "…will be zero." (no pipe in the PDF, p. 197). Equation A41 spelling verified via the PDF text layer 2026-07-23: "AccretionAmortization" **correctly spelled** in A41 (SQ-8's typo is A42-only).
> Shared machinery: three-term template, hedge data states, reinvestment mechanics, floating-margin imputation, and the granularity proposal are stated once in `handbook/cross-cutting/asset-side-common-conventions.md` §12 (D-003 pattern).
> Chapter review state: **DRAFTED + source-grounding review this session (`reviews/interest-income/securities/ii_mbs.review.md`) — AWAITING USER REVIEW (Increment 2 gate).** Specification: `specifications/interest-income/securities/ii_mbs.yaml`.
> Labels: **[FACT]** = Fed statement (cited); **[PID]** = project implementation decision (user-confirmed); **[INT]** = interpretation; **[CODE]** = coding consideration; **[OQ]** = open question.

## 1. Status and purpose

- [FACT] "The Board proposes an alternative structural approach to model interest income on mortgage-backed securities that is based on security-level microdata available in form FR Y-14Q, Schedule B." Same three-summand approach as `ii_ust`; "For this securities category, the Board uses a vendor model to account for the prepayment behavior of residential mortgage-backed bonds." (PDF p. 195; md sec-181).
- [FACT] Rationale vs. regressions restated with hedge emphasis: results tied to "the characteristics of the securities, the underlying interest rate risk hedges, and the stress testing scenario" (PDF p. 195; md sec-181).
- **Model type: structural calculator on security-level data, with one vendor-model category.** No estimated parameter anywhere in v.a(4); Tables A7–A9 contain no row [FACT absence].

## 2. Model summary

Two source-stated regimes inside one component:

1. **Agency residential MBS [FACT]:** "a vendor model is used to calculate the income to better reflect the impacts of prepayments. This vendor model is used across both interest income on securities as well as the Securities Model." (PDF p. 196; md sec-182; fn 65 → MRM pp. 18–20.) How the vendor output composes with Equation A41's terms is **not stated** — OQ-026.
2. **All other MBS (mostly CMBS) [FACT]:** the three-term template with: coupon accrual on beginning-of-period face (vendor coupon; **fallback to Schedule B.1 book yield** if unavailable); zero-coupon bonds accrue at book yield; floating-rate margin imputed off the t=0 spot 3-month Treasury (conventions §12); **no prepayments** ("expected to have low or no prepayments"); accretion by the **effective interest method** with coupon and book yield constant for the security's life, straight-line fallback if data missing (PDF pp. 196–197; md sec-182).

Maturities incorporated; constant balance via the shared reinvestment assumption (conventions §12).

## 3. Inputs

### 3.1 Firm data inputs (security-level [FACT]; bucket proposal [CODE] in §9)

| Input | Source | Dimensions | Units | Timing | Label |
|---|---|---|---|---|---|
| Current face value (`current_face_value`) | FR Y-14Q Schedule B.1 | i, t | USD (millions at boundary, D-006) | Beginning-of-period | [FACT] (PDF p. 196; md sec-182) |
| Coupon rate (`coupon_rate`) | Vendor data; **fallback: Schedule B.1 book yield** | i, t | Annualized rate | Per security | [FACT] (PDF p. 196; md sec-182) |
| Book yield (`book_yield`) | FR Y-14Q Schedule B.1 | i | Annualized rate | t=0 (constant for the security's life) | [FACT] (PDF pp. 196–197; md sec-182) |
| Amortized cost (`amortized_cost`) | FR Y-14Q Schedule B.1 | i, t | USD | A41 numerator is **t-dated** | [FACT] (PDF p. 196; md sec-182) |
| Weighted Average Life at t=0 (`wal_launchpoint`) | Vendor data | i | Years [INT — A41's 4×WAL denominator converts years→quarters; unit not stated, flagged] | Launch point | [FACT] formula role (PDF p. 196); unit [INT] |
| **Agency RMBS vendor income** (`vendor_agency_rmbs_income`) | Third-party vendor model output | category, t | USD/quarter | PQ1..PQ9 | [FACT] vendor role (PDF p. 196); **declared input path** [CODE — candidate PID-MBS-1]; OQ-026 |
| Hedge legs | Proposed Schedule B.2/B.3 — not currently collected | d, t | — | Future data state | [FACT] (PDF p. 197); conventions §12 |

### 3.2 Scenario inputs

| Variable | Role | Label |
|---|---|---|
| `usd_3m_treasury` (incl. **PQ0 spot**) | Floating-rate margin imputation: margin = t=0 coupon − t=0 spot 3M; margin + 3M(q) forward (conventions §12) | [FACT] (PDF p. 196; md sec-182) |
| `usd_1y_treasury` | Reinvestment coupon (conventions §12) | [FACT — MRM p. 73]; mapping OQ-025(d) |
| Vendor-model macro inputs (mortgage rate, prime, unemployment, HPI, zero-coupon Treasury and SOFR curves; MBS/CMO OAS auxiliary indices) | Enter the **vendor model**, not this model directly | [FACT — MRM pp. 18–19; extracts §3]; behind the declared vendor path [CODE] |

### 3.3 Parameters

**None.** [FACT] No estimated or supplied parameter; Tables A7–A9 contain no row for this component. The vendor model runs on "the vendor's default model calibration without any adjustment or overlay" [FACT — MRM p. 19].

## 4. Timing and dimensions

- Dimensions: i = security; d = derivative; category split {Agency residential MBS} vs {all other MBS} [FACT]; output grain firm × scenario × quarter after aggregation; q = 1…9 (PDF p. 6).
- [FACT] Constant balance via reinvestment; purchases "on the first day of the quarter subsequent to the maturing quarter" (PDF p. 198; md sec-182 — note: this section's reinvestment paragraph **omits** the "For additional details…" referral sentence present in v.a(3)/v.a(5); faithful difference, no significance attached [INT]).
- Reinvestment also covers balances "decreasing … due to partial paydowns" [FACT — MRM p. 72]; interaction with vendor-computed Agency RMBS income is OQ-026.

## 5. Equations and variable definitions

[FACT] Verified against the PDF page image (p. 196) this session; A41 spelling confirmed correct via the text layer (banner).

**Equation A41** – Interest Income on Mortgage-Backed Securities Projection:

$$Interest\ Income_{i,t} = Coupon\ Accrual_{i,t} + AccretionAmortization_{i,t} + Hedge\ Income_{d,t}$$

Where-list [FACT, verbatim]:

- $Coupon\ Accrual_{i,t} = Current\ Face\ Value_{i,t} \times \frac{Coupon\ Rate_{i,t}}{4}$;
- $AccretionAmortization_{i,t} = \frac{Current\ Face\ Value_{i,t} - Amortized\ Cost_{i,t}}{4 * Weighted\ Average\ Life_{\,i,t=0}}$ — **t-dated numerator** (unlike A40's t=0), denominator 4 × WAL(t=0);
- $Hedge\ Income_{d,t} = Notional\ Amount_{d,t} \times \frac{Pay\ Rate_{d,t} - Receive\ Rate_{d,t}}{4}$.

- [INT — formula-to-category mapping, flagged] The prose assigns accretion methods by category: "For Agency residential mortgage-backed securities, the straight-line method is used, leveraging the t=0 Weighted Average Life. For all other mortgage-backed securities, accretion/amortization is calculated using the effective interest method" (PDF p. 197). A41's printed accretion expression matches the Agency straight-line/WAL description; **no formula is given for the effective-interest method** [FACT absence]. Presented as printed; not reconciled beyond the prose.
- [FACT] Floating-rate margin imputation and zero-coupon book-yield accrual per §2 item 2 (PDF p. 196).

## 6. Calculation workflow

1. **Categorize** each security: Agency residential MBS vs. all other MBS [FACT].
2. **Agency RMBS income** = vendor-model output [FACT]; enters the project as a declared quarterly input path (§3.1, candidate PID-MBS-1) — composition with A41 terms UNKNOWN (OQ-026), so the path is taken as that category's total pre-hedge income [CODE working treatment].
3. **Other MBS coupon accrual**: beginning-of-period face × coupon/4; vendor coupon, book-yield fallback; zero-coupon at book yield; floating-rate coupon = imputed margin + 3M(q) (conventions §12).
4. **Other MBS accretion**: effective-interest with constant coupon and book yield [FACT prose; formula unstated — implementation per the standard effective-interest schedule flagged INT]; straight-line fallback when coupon or book yield is missing [FACT].
5. **Reinvestment income** on maturing/paying-down balances (non-Agency; Agency per OQ-026): as in `ii_ust` §6 step 4 (conventions §12).
6. **Hedge income** zero in the current data state; per-derivative formula + Portfolio-Layer-Method allocation if B.2/B.3 arrive (conventions §12).
7. **Aggregate** across categories and securities → `mbs_interest_income`, firm × scenario × quarter; expose pre-hedge (§11).

## 7. Output calculation

- Output: `mbs_interest_income` (USD millions/quarter, D-006). The ÷4s are source-stated inside A41 [FACT]; D-004 is not invoked (conventions §12).

## 8. Fed-stated assumptions and limitations

All [FACT] (PDF pp. 198–199; md sec-183), restated faithfully:

1. **Hedge-data gap** — same statement pattern as `ii_ust` §8.1.
2. **Reinvestment materiality** — same statement pattern as `ii_ust` §8.2 ("outsized impact").
3. **Floating-margin proxy caveat** — "the Board does not have reliable margin information for all floating rate instruments (**except for Agency residential mortgage-backed securities**)"; all floating instruments assumed indexed to the 3-month Treasury; "could be impactful for securities indexed to longer tenor rates or rates other than Treasuries."
4. **Vendor reliance** — "This model relies on a vendor model for prepayment behavior on Agency residential mortgage-backed securities."
5. **No prepayment elsewhere** — could keep balances on-book "longer than otherwise expected", damping scenario impact.
6. **Stated exclusions** — OCI releases (AFS→HTM); previously terminated hedges.

Public-input request: Questions A165–A168 of section v.a(4) (PDF pp. 199–200; md sec-184); A168 concerns the reinvestment strategy.

## 9. User-confirmed implementation mappings

None yet. Pending gate decisions and [CODE] items:

| Pending item | Working assumption / proposal | Status |
|---|---|---|
| Input granularity | **Pre-aggregated buckets** (conventions §12, candidate PID-SEC-1): closed subcomponent set, e.g. `agency_rmbs` (vendor path) / `other_fixed` / `other_floating` (margin inputs) / `other_zero_coupon`, each with the paths §6 needs | PROPOSED — gate decision |
| Agency RMBS vendor income path | Declared quarterly input `ii_mbs`/`vendor_agency_rmbs_income` — the firm supplies its vendor-equivalent output; the Fed's vendor model is not reimplemented | PROPOSED — candidate PID-MBS-1; OQ-026 |
| WAL unit | Years, converted by A41's printed 4× factor | [INT] — confirm at company-reference |
| Reinvestment coupon series | `usd_1y_treasury` | TO BE CONFIRMED — OQ-025(d) |

## 10. Validation requirements ([CODE] — non-normative)

- Category completeness: every security/bucket assigned exactly one category; unknown categories error.
- Margin imputation inputs: t=0 coupon and PQ0 spot 3M present for every floating bucket; imputed margin logged; negative margins legal, logged.
- Fallback discipline: book-yield fallback and straight-line fallback each logged when used; a missing coupon **and** missing book yield errors (no further fallback stated) [FACT absence].
- WAL(t=0) > 0 where the A41 accretion form applies.
- Reinvestment ledger conservation as in `ii_ust` §10; paydown amounts non-negative.
- Vendor path present for the Agency category when its balance is nonzero; vendor path with no Agency balance is logged as suspicious.

## 11. Dependencies and hedge interface

- Upstream: Schedule B.1 + vendor data; the **vendor prepayment model** (MRM pp. 18–20 — macro inputs itemized there) behind the declared income path; shared reinvestment assumption (conventions §12) [FACT].
- Hedge boundary: embedded term zero; v.c external; OQ-005 (conventions §9/§12). Pre-hedge path exposed.
- Family-level: feeds asset-side aggregation and the `frb_total_interest_income` monitor (conventions §10).

## 12. Open issues

- [OQ-026 — OPEN, filed this session] Agency RMBS vendor income: composition with A41's terms unstated; vendor model is a black box (Monte Carlo, default calibration, itemized macro inputs — MRM pp. 18–19); paydown-reinvestment interaction for this category; working treatment = declared total-income path for the category (§6 step 2).
- [OQ-025 — OPEN] Reinvestment income residuals (see `ii_ust` §12), incl. paydown proceeds.
- [OQ-005 — OPEN] Hedge-adjustment allocation.
- [CA-2d — filed 2026-07-16] md stray pipe (banner).
- [CODE] Granularity gate decision; WAL-unit confirmation (§9).

## 13. Key source references

| Claim | Citation |
|---|---|
| Component proposal; three-summand approach; vendor model for residential MBS prepayments | (PDF p. 195; md sec-181) |
| Equation A41 + where-list (t-dated accretion numerator; 4×WAL(t=0)); vendor-model statement + fn 65; coupon fallback to book yield; zero-coupon at book yield; floating-margin imputation | (PDF p. 196; md sec-182) |
| No prepayments for non-Agency (mostly CMBS); category accretion methods (Agency straight-line/WAL; others effective interest, straight-line fallback); hedge zero + B.2/B.3 + Portfolio Layer Method | (PDF p. 197; md sec-182) |
| Maturity incorporation; reinvestment assumption (no referral sentence in this section); first-day purchases | (PDF p. 198; md sec-182) |
| Assumptions 1–6 | (PDF pp. 198–199; md sec-183) |
| Questions A165–A168 | (PDF pp. 199–200; md sec-184) |
| Vendor-model mechanics + itemized macro inputs + OAS auxiliary indices + default calibration | (MRM pp. 18–20; extracts §3) |
| Reinvestment instrument detail; paydowns covered; PPNR cross-link | (MRM pp. 72–74; extracts §5) |
| Table A6 row (Structural); nine-quarter horizon | (PDF pp. 168–169, 6; md sec-148, sec-2) |

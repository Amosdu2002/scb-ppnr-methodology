# 5. Interest Income on Other Securities (`ii_other_sec`)

> **STATUS: Proposed for the 2026 stress test — public-comment stage, NOT adopted.**
> Source: Section B.v.a(5) (PDF pp. 200–205; md sec-185–188). Model type per Table A6: **Structural** (PDF pp. 168–169; md sec-148). Second source for the delegated reinvestment detail: MRM Section A (`sources/fed/market-risk-models-securities-extracts.md`; OQ-004 resolution).
> Integrity flags: **SQ-8 (refined 2026-07-23)** — the PDF's Equation A42 **main equation line** spells "**Accrection**Amortization" (p. 201); the **where-list on the same page is spelled correctly** — settled via a PDF text-layer glyph-count check this session. **CA-4 (new, filed this session)** — the md working copy (lines 3999/4003) carries the typo in **both** spots, so its where-list deviates from the PDF. **CA-2e** — md stray `|` after "…will be zero." (line 4013; no pipe in the PDF, p. 203).
> Shared machinery: three-term template, hedge data states, reinvestment mechanics, floating-margin imputation, and the granularity proposal are stated once in `handbook/cross-cutting/asset-side-common-conventions.md` §12 (D-003 pattern).
> Chapter review state: **DRAFTED + source-grounding review this session (`reviews/interest-income/securities/ii_other_sec.review.md`) — AWAITING USER REVIEW (Increment 2 gate).** Specification: `specifications/interest-income/securities/ii_other_sec.yaml`.
> Labels: **[FACT]** = Fed statement (cited); **[PID]** = project implementation decision (user-confirmed); **[INT]** = interpretation; **[CODE]** = coding consideration; **[OQ]** = open question.

## 1. Status and purpose

- [FACT] "The Board **is considering** an alternative structural approach to model interest income on other securities that is based on the security level microdata available in form FR Y-14Q, Schedule B." (PDF p. 200; md sec-185.) Wording note [FACT preserved]: "is considering", where v.a(3)/v.a(4) say "proposes" — recorded, no significance attached.
- [FACT] Same three-summand approach; "bond-specific details, including rate and maturity from FR Y-14Q, Schedule B.1 along with vendor data" (PDF p. 200; md sec-185).
- [FACT] Rationale vs. regressions restated (PDF p. 201; md sec-185). Current model = panel regression [FACT, Question A169 wording].
- **Model type: structural calculator on security-level data (book-yield variant).** No estimated parameter anywhere in v.a(5); Tables A7–A9 contain no row [FACT absence].

## 2. Model summary

The family template with the **collapsed book-yield variant** [FACT]: coupon accrual and accretion/amortization are computed **together** as Amortized Cost(i,t) × Book Yield(i,t)/4 — the effective-interest method, with coupon rate and book yield assumed constant for the security's life and a straight-line fallback if either is missing. Floating-rate margins imputed off the t=0 spot 3-month Treasury (conventions §12). **No prepayments modeled** despite many prepayable asset classes — a source-acknowledged simplification. Maturities incorporated; constant balance via the shared reinvestment assumption (conventions §12).

## 3. Inputs

### 3.1 Firm data inputs (security-level [FACT]; bucket proposal [CODE] in §9)

| Input | Source | Dimensions | Units | Timing | Label |
|---|---|---|---|---|---|
| Amortized cost (`amortized_cost`) | FR Y-14Q Schedule B.1 | i, t | USD (millions at boundary, D-006) | A42's term is **t-dated** | [FACT] (PDF p. 201; md sec-186) |
| Book yield (`book_yield`) | FR Y-14Q Schedule B.1 — "The Board uses the book yield reported in the FR Y-14Q, Schedule B.1" | i | Annualized rate | Constant for the security's life [FACT] | [FACT] (PDF pp. 201–202; md sec-186) |
| Coupon rate (`coupon_rate`) | Vendor data / Schedule B.1 ("rate") | i | Annualized rate | t=0 (margin imputation; constancy assumption) | [FACT] (PDF pp. 200–201; md sec-185–186) |
| Hedge legs | Proposed Schedule B.2/B.3 — not currently collected | d, t | — | Future data state | [FACT] (PDF p. 202); conventions §12 |

### 3.2 Scenario inputs

| Variable | Role | Label |
|---|---|---|
| `usd_3m_treasury` (incl. **PQ0 spot**) | Floating-rate margin imputation (conventions §12): "The Board uses the t=0 coupon rate along with the t=0 spot 3-month Treasury rate to infer a margin. That inferred margin is then added to the spot 3-month Treasury rate applicable in all forward quarters." | [FACT, verbatim] (PDF p. 201; md sec-186) |
| `usd_1y_treasury` | Reinvestment coupon (conventions §12) | [FACT — MRM p. 73]; mapping OQ-025(d) |

### 3.3 Parameters

**None.** [FACT] No estimated or supplied parameter; Tables A7–A9 contain no row for this component.

## 4. Timing and dimensions

- Dimensions: i = security; d = derivative; output grain firm × scenario × quarter after aggregation; q = 1…9 (PDF p. 6).
- [FACT] Maturity incorporation + reinvestment + first-day-of-subsequent-quarter purchases, with the referral sentence present in this section: "For additional details on the reinvestment assumptions, please refer to the Securities Model Description." (PDF p. 203; md sec-186.)
- [INT] Amortized cost evolves per the effective-interest schedule (book yield constant); **no formula for the AC(t) path is given** [FACT absence] — implementation supplies or derives the AC path (bucket proposal, §9).

## 5. Equations and variable definitions

[FACT] Verified against the PDF page image (p. 201) this session; spelling settled via the text layer (banner: typo in the main equation line only).

**Equation A42** – Interest Income on Other Securities Projection (main line verbatim, incl. the SQ-8 typo):

$$Interest\ Income_{i,t} = Coupon\ Accrual_{i,t} + AccrectionAmortization_{i,t} + Hedge\ Income_{d,t}$$

Where-list [FACT, verbatim — spelled correctly in the PDF here, CA-4]:

- $Coupon\ Accrual_{i,t} + AccretionAmortization_{i,t} = Amortized\ Cost_{i,t} \times \frac{Book\ Yield_{i,t}}{4}$ — the **combined** term: this variant has no separate accretion line; and
- $Hedge\ Income_{d,t} = Notional\ Amount_{d,t} \times \frac{Pay\ Rate_{d,t} - Receive\ Rate_{d,t}}{4}$.

- [FACT] "For this subset of securities, the Board calculates accretion/amortization using the effective interest rate method. The Board assumes that both the coupon rate and the book yield remain constant throughout the life of the security. If either the coupon rate or book yield data is not available, the Board uses a straight-line approach for computing accretion/amortization amounts." (PDF p. 202; md sec-186.)
- [FACT] "no prepayments are modeled on securities within this category" — "Given the broad number of asset classes and security types within this category, it is difficult to model all prepayment characteristics." (PDF p. 202; md sec-186.)
- [FACT] Hedge paragraph notes the B.2/B.3 proposal "In the Securities Model Description" (PDF p. 202; md sec-186) — a third explicit tie to the second source.

## 6. Calculation workflow

1. **Launch-point extraction.** Per security: amortized cost(0), book yield, t=0 coupon (floating buckets), category fixed/floating/zero-coupon as needed (§3.1).
2. **Fixed-rate (and general) income**: Amortized Cost(i,t) × Book Yield(i)/4 per quarter [FACT]; AC(t) per the effective-interest schedule [INT, §4]; straight-line fallback when coupon or book yield is missing [FACT].
3. **Floating-rate income**: imputed margin = t=0 coupon − t=0 spot 3M; quarter rate = margin + 3M(q) [FACT]; applied within the book-yield structure for the floating bucket [INT — the section states the imputation but not its exact insertion into the A42 term; flagged].
4. **Reinvestment income** on maturing balances: as in `ii_ust` §6 step 4 (conventions §12).
5. **Hedge income** zero in the current data state; B.2/B.3 formula + Portfolio-Layer-Method allocation when available (conventions §12).
6. **Aggregate** → `other_sec_interest_income`, firm × scenario × quarter; expose pre-hedge (§11).

## 7. Output calculation

- Output: `other_sec_interest_income` (USD millions/quarter, D-006). The ÷4 is source-stated inside A42 (BookYield/4) [FACT]; D-004 is not invoked (conventions §12).

## 8. Fed-stated assumptions and limitations

All [FACT] (PDF pp. 203–204; md sec-187), restated faithfully:

1. **Hedge-data gap** — same statement pattern as the siblings; "If the changes proposed to the FR Y-14Q, Schedule B.2 and B.3 are not implemented, the Board will need to identify other alternative data sources."
2. **Reinvestment materiality** — "the choice not to apply qualified accounting hedges against reinvestments and the coupon type (i.e., fixed/floating) of those reinvestments has an outsized impact on interest income model results."
3. **Floating-margin proxy caveat** — no reliable vendor margin data; "an assumption is made that all floating instruments are indexed to the 3-month Treasury rate. This could be impactful for securities indexed to longer tenor rates or rates other than Treasuries."
4. **No-prepayment caveat** — "This could dampen the impact of the stress test scenario rate paths on income projects and assume the full balance of existing securities remain on the balance sheet longer than otherwise expected. If prepayments were modeled, the principle paydowns would be reinvested according to the reinvestment assumptions of the Securities model and would likely earn a lower rate of interest than the reported security." (Source spellings "projects"/"principle" preserved.)
5. **Stated exclusions** — OCI releases (AFS→HTM); previously terminated hedges.

Public-input request: Questions A169–A174 of section v.a(5) (PDF pp. 204–205; md sec-188); A172 concerns adjusted amortized-cost reporting; A174 concerns the reinvestment strategy "(detailed within the Securities Model Description)".

## 9. User-confirmed implementation mappings

None yet. Pending gate decisions and [CODE] items:

| Item | Decision / working assumption | Status |
|---|---|---|
| Input granularity | **Security-level** positions contract; aggregation inside the model | **PID-SEC-1, user-confirmed 2026-07-23** (sheet layout pending the user's format upload) |
| AC(t) path | Per-security effective-interest evolution (book yield constant), straight-line fallback where data are missing — exact treatment finalized with the positions format | [INT] §4 — finalize on format receipt |
| Floater negative margin | Floor projected coupon at the security's coupon floor if available; else-branch TO_BE_CONFIRMED | **PID-SEC-2, user-confirmed 2026-07-23** (company convention, never Fed) |
| Unsettled transactions | AC proxy = purchase price/100 × notional | **PID-SEC-3, user-confirmed 2026-07-23** (company convention) |
| Reinvestment | `usd_1y_treasury` = par-curve 1Y yield; fixed-coupon 4-quarter window; rolls again; in-component attribution — OQ-025(a)(b)(d) resolved, user-confirmed 2026-07-23 | CONFIRMED |

## 10. Validation requirements ([CODE] — non-normative)

- Book yield present per security/bucket; missing coupon **and** book yield → straight-line fallback is the stated path only for accretion — a bucket with no rate basis at all errors.
- Margin imputation inputs (t=0 coupon; PQ0 spot 3M) present for floating buckets; imputed margins logged; negative margins legal.
- AC plausibility: AC > 0; AC → face drift consistent with book-yield sign (log-only monitor).
- Reinvestment ledger conservation as in `ii_ust` §10.
- Fallback usage logged (straight-line); hedge term identically zero in the current data state.

## 11. Dependencies and hedge interface

- Upstream: Schedule B.1 + vendor data [FACT]; shared reinvestment assumption (conventions §12). No other income model's output consumed.
- Hedge boundary: embedded term zero; v.c external; OQ-005 (conventions §9/§12). Pre-hedge path exposed.
- Family-level: feeds asset-side aggregation and the `frb_total_interest_income` monitor (conventions §10).

## 12. Open issues

- [OQ-025 — OPEN] Reinvestment income residuals (see `ii_ust` §12) — for this component also the cross-asset "uniformly into Treasuries" reading (income from matured other-securities balances earning the 1Y Treasury while attributed to this component [INT]).
- [OQ-005 — OPEN] Hedge-adjustment allocation.
- [SQ-8 — refined this session] A42 typo confined to the main equation line (banner); [CA-4 — filed this session] md where-list deviation; [CA-2e] md stray pipe.
- [CODE] Granularity and AC-path gate decisions (§9); floating-bucket insertion into the A42 term [INT, §6 step 3].

## 13. Key source references

| Claim | Citation |
|---|---|
| Component proposal ("is considering"); security-level microdata; three-summand approach; Schedule B.1 rate/maturity + vendor data | (PDF p. 200; md sec-185) |
| Equation A42 (typo in main line; where-list correct — text-layer check) + combined coupon+accretion term; book yield source; floating-margin imputation verbatim | (PDF p. 201; md sec-186) |
| No prepayments + rationale; effective-interest method + constancy + straight-line fallback; hedge zero + "In the Securities Model Description" B.2/B.3 + Portfolio Layer Method | (PDF p. 202; md sec-186) |
| Maturity incorporation; reinvestment assumption + referral sentence; first-day purchases | (PDF p. 203; md sec-186) |
| Assumptions 1–5 (source spellings preserved) | (PDF pp. 203–204; md sec-187) |
| Questions A169–A174 | (PDF pp. 204–205; md sec-188) |
| Reinvestment instrument detail; PPNR cross-link | (MRM pp. 72–74; extracts §5) |
| Table A6 row (Structural); nine-quarter horizon | (PDF pp. 168–169, 6; md sec-148, sec-2) |

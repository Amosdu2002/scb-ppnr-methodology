# 6. Interest Income on Other Interest/Dividend-Bearing Assets (`ii_other_ida`)

> **STATUS: Proposed for the 2026 stress test — public-comment stage, NOT adopted.**
> Source: Section B.v.a(6) (PDF pp. 205–209; md sec-189–192). Model type per Table A6: **Structural** (PDF pp. 168–169; md sec-148).
> Integrity flags: **CA-1** — in the Markdown working copy, footnote 66 has glued text ("Notes: Statistical significance levels … " appended after the footnote proper). Verified against the PDF page image (p. 206) this session: the authoritative footnote 66 ends at "…the 10-year Treasury yield."; the glued sentence is a conversion artifact belonging to a table-notes block.
> Absorption: this component **subsumes the asset-side federal funds sold & reverse repo positions** — "the federal funds and repo positions on the asset side are subsumed within the component other interest/dividend-bearing assets" [FACT, stated in v.a(10), PDF p. 217; md sec-206]; cf. Question A176 (PDF p. 208; md sec-192). It replaces the current structural model iv.m(1) for that income (inventory record #6).
> Chapter review state: **REVIEWED** — source-grounding review 2026-07-23, verdict APPROVE (`reviews/interest-income/calculators/ii_other_ida.review.md`); **user review gate passed 2026-07-23.** Specification: `specifications/interest-income/calculators/ii_other_ida.yaml`.
> Labels: **[FACT]** = Fed statement (cited); **[PID]** = project implementation decision (user-confirmed); **[INT]** = interpretation; **[CODE]** = coding consideration; **[OQ]** = open question.

## 1. Status and purpose

- [FACT] "The Board proposes a structural approach to model interest income from other interest/dividend-bearing assets." (PDF p. 205; md sec-189). One of the ten proposed structural net-interest components (PDF p. 172; md sec-149; Table A6, PDF pp. 168–169; md sec-148).
- [FACT] Component composition: "Interest income from other interest/dividend-bearing assets consists of interest earned on federal funds sold and securities purchased under agreements to resell, as well as interest and dividends on other assets, such as the Federal Reserve or Federal Home Loan Bank stock." (PDF pp. 205–206; md sec-189).
- [FACT] "Federal funds sold and securities purchased under agreements to resell comprise most of other interest/dividend-bearing assets reported in FR Y-14Q." (PDF p. 206; md sec-189).
- **Model type: structural calculator (two-rate blend).** [FACT] "simplicity (since it does not involve coefficients estimation)" (PDF p. 208; md sec-191). No coefficient, scalar, beta, or fixed effect appears anywhere in v.a(6) [FACT absence]. Tables A7/A8/A9 contain no row for this component [FACT].
- [FACT] "The Board proposes to model interest income on other interest/dividend-bearing assets as one component that consists of several categories of interest income earned on interest-earning assets. The Board chose this approach due to data limitations when identifying these components using FR Y-14Q reporting schedules." (PDF p. 208; md sec-191).
- [FACT] The current model being replaced is a panel regression — Question A175's own words: "as compared to the Board's current panel regression model" (PDF p. 208; md sec-192). Current-suite mechanics are out of scope for this chapter; do not mix the two.

## 2. Model summary

Income each projection quarter = a two-rate blend on a single flat balance: the federal-funds-sold/reverse-repo share α earns the contemporaneous **3-month** Treasury yield; the remaining (1 − α) share earns the contemporaneous **10-year** Treasury yield [FACT, Eq A43]. Both the balance B and the share α are measured once at the launch point and held constant [FACT]. No parameters, no recursion, no regime, no floor. Footnote 66 gives the 10-year choice's rationale ("stock in Federal Reserve Banks yields the lesser of six percent and the 10-year Treasury yield") — rationale only; **no 6 % cap appears in Equation A43** [FACT: no cap term in the equation; see §5, [CODE] note].

## 3. Inputs

### 3.1 Firm data inputs

| Input | Line item / source | Dimensions | Units | Timing | Label |
|---|---|---|---|---|---|
| Total balance on other interest/dividend-bearing assets (`other_ida_total_balance`) | **Line item 15**, Net Interest Income Worksheet, FR Y-14Q Schedule G (G.2) — **source-stated** | b | USD (millions at the model boundary, D-006) | Launch point (PQ0); constant over horizon | [FACT] (PDF p. 206; md sec-189) |
| Fed-funds-sold & reverse-repo share α (`other_ida_short_rate_share`) | "the additional fields provided by the firms in the footnotes to the worksheet", cross-referenced "with the balances reported in FR Y-9C (BHCK3365)" — **derivation mechanics unstated** | b | Decimal share ∈ [0,1] | Launch point (PQ0); constant over horizon | [FACT] sourcing sentence (PDF p. 206; md sec-189); computation detail [OQ-024]; supplied-input treatment [CODE] |

- [FACT] Source wording: "The relevant balances for this component are the assets reported in line item 15 of the Net Interest Income Worksheet of FR Y-14Q, Schedule G (G.2). … This portion can be quantified by utilizing the additional fields provided by the firms in the footnotes to the worksheet and by cross-referencing with the balances reported in FR Y-9C (BHCK3365)." (PDF p. 206; md sec-189).
- [OQ-024 — OPEN] Which footnote fields enter the α numerator, and how the BHCK3365 cross-reference resolves disagreements, is not stated. **Project treatment [CODE]:** α is a **supplied launch-point input** (decimal share), validated ∈ [0,1]; its upstream derivation is data preparation outside the model boundary (precedent: the Spread(i,b) supplied-input treatment in the deposit-expense chapters).
- No MDRM code beyond BHCK3365 is stated in v.a(6); none is invented [FACT absence].

### 3.2 Scenario inputs

| Variable | Role | Frequency | Units | Label |
|---|---|---|---|---|
| 3-month Treasury yield, Treasury3m(q) (`usd_3m_treasury`) | Rate on the α share — used directly, unscaled and untransformed | Quarterly, q = 1…9 (no PQ0 value needed: no recursion, no delta) | Annualized rate [D-004] | [FACT] role (PDF pp. 206–207; md sec-190); MEV column name UNCONFIRMED [CODE] |
| 10-year Treasury yield, Treasury10y(q) (`usd_10y_treasury`) | Rate on the (1 − α) share — used directly, unscaled and untransformed | Quarterly, q = 1…9 | Annualized rate [D-004] | [FACT] role (PDF pp. 206–207; md sec-190); **new canonical series** — MEV column name UNCONFIRMED [CODE] |

### 3.3 Parameters

**None.** [FACT] No supplied or estimated parameter exists for this model; no beta, scalar, spread, floor, or threshold (PDF pp. 205–208; md sec-189–191; Tables A7–A9 contain no row for this component). α is a firm-data input (§3.1), not a parameter.

## 4. Timing and dimensions

- Dimensions: b = firm; s = scenario; q = 1…9 (nine-quarter horizon, PDF p. 6; md sec-2). No subcomponent dimension — α splits the single balance inside the equation; nothing is reported below the component level.
- Output grain: firm × scenario × quarter.
- Launch-point quantities: B(b,q0) and α(b,q0); no PQ0 scenario value is consumed.
- [FACT] Flat balance and flat share: "The stress test assumes constant balances for all firms; therefore, B(b,q) = B(b,q0) for all quarters where B(b,q0) represents the balances of firm b at lift-off quarter q0. This means that the projected flow of income is calculated based on the balances at the start of the projection horizon. The share α(b,q) = α(b,q0) is also assumed to stay constant over the projection quarters." (PDF p. 207; md sec-190; source word "lift-off" retained per D-005 — handbook term: launch point, PQ0.)
- Treasury3m(q) and Treasury10y(q) are contemporaneous each projection quarter [FACT]; nothing else varies over the horizon.

## 5. Equations and variable definitions

[FACT] Verified against the PDF page image (p. 207) this session.

**Equation A43** – Interest Income on Other Interest/Dividend-Bearing Assets:

$$F_{b,t} = \alpha_{b,t}B_{b,t}\,Treasury3m + (1 - \alpha_{b,t})B_{b,t}\,Treasury10y$$

- Where-list [FACT, verbatim]: "Treasury3m is the 3-month Treasury yield; and Treasury10y is the 10-year Treasury yield."
- Variable definitions [FACT] (PDF p. 206; md sec-190): "let α_b be the proportion of assets consisting of federal funds sold and securities purchased under agreements to resell for each firm b, B_b be the total balance on other interest/dividend bearing assets, and F_b be the income earning from this component" (source grammar preserved).
- Projection form, stated on the same page [FACT]: $F_{b,q} = \alpha_{b,q}B_{b,q}\,Treasury3m_q + (1 - \alpha_{b,q})B_{b,q}\,Treasury10y_q$.
- Faithful-transcription note: in the A43 display the Treasury terms carry **no time subscript**; the projection form adds the q subscripts — both match the page image. Benign notation; the projection form governs the calculation.
- [CODE] Restatement for implementation (algebraically identical): BlendedRate(b,q) = α(b,0)·Treasury3m(q) + (1 − α(b,0))·Treasury10y(q); income = B(b,0) × BlendedRate(b,q). The blended rate is a convenient diagnostic; it is not a separate Fed quantity.
- [CODE] Footnote 66's "lesser of six percent and the 10-year Treasury yield" is **rationale for the 10-year choice, not model mechanics** — do not implement a 6 % cap; Equation A43 applies the raw Treasury10y to the (1 − α) share [FACT: no cap term].

## 6. Calculation workflow

1. **Launch-point extraction.** Read the Schedule G line item 15 balance and the supplied share α at PQ0 (§3.1). Validate per §10.
2. **Scenario prep.** Load `usd_3m_treasury` and `usd_10y_treasury` for q = 1…9, in annualized decimal units; do **not** divide the rates here [PID, D-004].
3. **Blended rate [CODE restatement].** BlendedRate(b,q) = α(b,0)·Treasury3m(q) + (1 − α(b,0))·Treasury10y(q), each quarter.
4. **Quarterly income.** QuarterlyIncome(b,q) = Balance(b,0) × BlendedRate(b,q) / 4, for q = 1…9 (§7) — identically, the D-004 conversion applied to the A43 sum.
5. **Hand-off.** Expose the income path (and both legs as diagnostics) per firm × scenario × quarter to aggregation and to the cross-cutting hedge adjustment (§11).

**Intermediates:** `other_ida_total_balance` Balance(b,0) (USD millions); `other_ida_short_rate_share` α(b,0) (decimal); `other_ida_blended_rate` BlendedRate(b,q) (annualized decimal) [CODE diagnostic]; output `other_ida_interest_income` QuarterlyIncome(b,q) (USD millions/quarter).

## 7. Output calculation

- [PID, D-004] All rates in this project are annualized; the annualized→quarterly-dollar conversion divides by four **only** at the final income step: **QuarterlyIncome(b,q) = Balance(b,0) × [α(b,0)·Treasury3m(q) + (1 − α(b,0))·Treasury10y(q)] / 4** (simple nominal quarterization, not compounding). Never attributed to the Fed: v.a(6) states no conversion for this component [FACT absence; OQ-006 resolution].
- [CODE] Rate-scale normalization (percent vs. decimal) is resolved at ingestion; the model consumes decimal annualized rates. Money normalizes to USD millions at the model boundary [D-006].

## 8. Fed-stated assumptions and limitations

All [FACT] (PDF pp. 207–208; md sec-191), restated faithfully:

1. **Two-rate assumption.** "the yield each firm earns over the projection horizon is given by the 3-month U.S. Treasury rate for the portion of the portfolio that consists of the federal funds sold and securities purchased under agreements to resell, and given by the 10-year U.S. Treasury rate for the remainder of the portfolio."
2. **Special/rare collateral caveat.** "While the 3-month U.S. Treasury rate tracks the overnight and other short-term lending rates closely, some fluctuations may be observed, especially when the short-term lending is collateralized by special or rare securities."
3. **Remainder-heterogeneity caveat, immaterial.** "the remainder of each firms' portfolio may exhibit heterogeneity and earn a rate that is higher or lower than the 10-year U.S. Treasury rate. However, this portion of the portfolio is relatively small, and alternative rates do not result in material differences in the projected income."
4. **Why structural, not regression.** Advantages over a panel regression: "enhanced clarity and explainability as well as simplicity (since it does not involve coefficients estimation)"; projection variability "can be fully explained by reported balances for each bank, and by the variation in the interest rate scenario paths"; and gross-vs-net reporting discretion under balance-sheet-offsetting rules "could produce less precise projections when a regression approach is adopted."
5. **Single-component treatment.** One component covering several income categories, "due to data limitations when identifying these components using FR Y-14Q reporting schedules."

Public-input request: Questions A175/A176 of section v.a(6) (PDF p. 208; md sec-192) — A176 addresses the joint modeling of fed funds sold with the other assets.

## 9. User-confirmed implementation mappings

None yet for this model. The Fed layer names item 15 and BHCK3365 (§3.1); the α derivation is OQ-024. Pending [CODE] confirmations, to be logged as PIDs when user-confirmed at company-reference verification:

| Pending item | Working assumption | Status |
|---|---|---|
| Physical firm-sheet row for item 15 balance | Spot sheet row `ii_other_ida` / `total_balance`, scale declared per D-006/D-007 | TO BE CONFIRMED |
| Physical source and value of α | Supplied directly as spot sheet row `ii_other_ida` / `short_rate_share` (decimal); upstream derivation outside the model boundary [OQ-024] | TO BE CONFIRMED |
| MEV workbook columns for `usd_3m_treasury`, `usd_10y_treasury` | PID-5 pattern; 3M shared with expense side; 10Y is a **new** series | TO BE CONFIRMED |

## 10. Validation requirements ([CODE] — non-normative)

Failures surface as errors; no invented fallbacks; monitors log, never clamp:

- Missing or negative launch-point balance in item 15; balance zero → income identically zero (log, likely a reporting gap).
- α present and **∈ [0,1]** — violations surface as errors, never clipped. α = 0 or 1 is legal (single-rate degenerate case; log at exactly 0 or 1 as a data plausibility note — the source says fed funds sold "comprise most" of the component, so α near 0 is suspicious).
- `usd_3m_treasury` and `usd_10y_treasury` present for all q = 1…9 in every scenario; flag negative values (income legs can flip sign — arithmetically valid under A43, but log it).
- Rate-scale sanity: annualized decimals in a plausible range (e.g., |rate| < 0.25) to catch percent/decimal errors.
- Flat-balance and flat-share invariants: Balance(b,q) and α(b,q) identical for all q.
- Blend-bounds invariant: for α ∈ [0,1], BlendedRate(b,q) lies between min and max of the two Treasury yields each quarter (structural check — any deviation means a coding error).
- Bilinearity invariant: with α fixed, the income path is an affine combination of the two Treasury paths with weights α·B/4 and (1 − α)·B/4 (structural check).

## 11. Dependencies and hedge interface

- Upstream models: **none** [FACT — v.a(6) references only the Schedule G balance, the footnote-field share, and the two scenario rates].
- Expense-side mirror [FACT]: v.a(10) states its approach "is equivalent to the one previously described for interest income on federal funds sold and securities purchased under agreements to resell, except that the federal funds and repo positions on the asset side are subsumed within the component other interest/dividend-bearing assets" (PDF p. 217; md sec-206) — a structural symmetry with `ie_fed_funds_repo`, not a compute dependency.
- v.a(6) contains no hedge term [FACT absence]. The cross-cutting v.c adjustment (Eqs A49–A51, PDF pp. 220 ff.; md sec-210–211) may adjust interest income later; allocation across components is unresolved [OQ-005]. This model only exposes its income path.
- Family-level: the income path feeds the asset-side family aggregation and the eventual reconciliation monitor against `frb_total_interest_income` (OQ-023 narrowing — a project input, never a Fed statement).

## 12. Open issues

- [OQ-024 — OPEN, filed this session] α derivation mechanics (which worksheet footnote fields; how the BHCK3365 cross-reference works) unstated; project treatment: α is a supplied launch-point input (§3.1).
- [CODE, TODO] Physical firm-sheet mappings for item 15 and α (§9) — candidate PIDs at company-reference verification.
- [CODE, TODO] Physical MEV workbook column names for `usd_3m_treasury` and the new `usd_10y_treasury` (PID-5 pattern).
- [OQ-005 — OPEN] Hedge-adjustment allocation (§11).
- [OQ-006 — RESOLVED (D-004)] Annualized units; ÷4 at the final step only (§7).
- [CA-1 — filed 2026-07-16, direction confirmed this session] md footnote 66 glued text is conversion-only; PDF footnote ends at "…10-year Treasury yield." (banner).
- No other open item: no ELB regime, no seed rate, no spread estimation, no history window applies to this model.

## 13. Key source references

| Claim | (PDF p.; md anchor) |
|---|---|
| Component proposal; composition (fed funds sold & reverse repos; Federal Reserve / FHLB stock) | (PDF pp. 205–206; md sec-189) |
| Source-stated balance line item 15 of the Schedule G (G.2) NII Worksheet; α from worksheet footnote fields cross-referenced with FR Y-9C BHCK3365; "comprise most" | (PDF p. 206; md sec-189) |
| Two-rate assumption (3M for fed funds sold portion; 10Y for remainder); footnote 66 (FRB stock: lesser of 6 % and 10Y — rationale only) | (PDF p. 206 incl. fn. 66; md sec-190, md line 5360 with CA-1 glue) |
| Equation A43; where-list; α_b/B_b/F_b definitions; projection form with q subscripts | (PDF pp. 206–207; md sec-190) |
| Flat balance B(b,q) = B(b,q0); flat share α(b,q) = α(b,q0) | (PDF p. 207; md sec-190) |
| Assumptions: two-rate; special/rare collateral caveat; remainder heterogeneity immaterial; no-estimation rationale; gross/net reporting discretion; single-component treatment | (PDF pp. 207–208; md sec-191) |
| Questions A175/A176 | (PDF p. 208; md sec-192) |
| Asset-side fed-funds subsumption (stated in v.a(10)) | (PDF p. 217; md sec-206) |
| Table A6 row (Structural); structural-model rationale | (PDF pp. 168–169, 172–173; md sec-148, sec-149) |
| Nine-quarter horizon | (PDF p. 6; md sec-2) |
| D-004 ÷4 convention; D-005 launch-point terminology; D-006 money units | `handbook/open-questions.md` decision log |

# 11. Net Interest Income on Trading Assets and Liabilities (`nii_trading_al`)

> **STATUS: Proposed for the 2026 stress test — public-comment stage, NOT adopted.**
> Source: Section B.v.d(1) (PDF pp. 225–230; md sec-215–219; the one-line v.d parent heading is sec-214, same page); parameters in Section B.v.e, Table A9 (PDF p. 234; md sec-224). Model type per Table A6: **Regression** (PDF pp. 168–169; md sec-148). Comparison context (current 2025 suite): iv.g (PDF pp. 65–68; md sec-54–58) and iv.i(4) (PDF pp. 90–97; md sec-80–87).
> Integrity flags affecting this chapter: **SQ-26** (Eq A52's where-list omits its dependent variable Ratio(b,t) — defined only in prose; filed this session) and **SQ-27** (current-suite p. 96 and Question A66 call the proposed other-borrowing successor a "structural approach" while v.d(2)/Table A6 classify it Regression; filed this session, cross-referenced at inventory #12). No conversion artifacts affect sec-214–219 or sec-224 (pp. 225–230 and 234 verified against the page images 2026-08-13, including the first image pass over pp. 227–229).
> Chapter format: D-009 compact 13-section skeleton **plus** the two regression-model sections (Estimation versus projection = §6; Firm fixed-effect treatment = §9), per the `ie_other_borrowing` precedent.
> Chapter review state: **APPROVED (user gate 2026-08-13** — "Looking good, go ahead with the engine"; same day as drafting and the independent source-grounding review, verdict APPROVE WITH OPEN IMPLEMENTATION ITEMS, `docs/reviews/interest-income/trading/nii_trading_al.review.md`**)**. Specification: `docs/specifications/interest-income/trading/nii_trading_al.yaml`. Approved content is never silently overwritten. **Revision 2026-08-13 (same day, pre-gate, user-supplied screenshot of the reference trading tab — not silent):** physical inputs registered (**PID-TRD-2**) and the ratio basis amended (**PID-TRD-3** — the reference projects an ANNUALIZED rate with ÷4 at the dollar step, inverting this chapter's provisional no-×4 closed form; §5/§8/§9). Recorded in the review addendum.
> Labels: **[FACT]** Fed source, cited · **[INT]** interpretation with stated basis · **[CODE]** coding consideration, non-normative · **[OQ]** open question by ID · **[PID]** PROJECT IMPLEMENTATION DECISION — user-confirmed, never attributable to the Federal Reserve · **[ALT]** alternative discussed by the Fed but not proposed. Citations: (PDF p. N; md sec-M).

## 1. Status and purpose

- [FACT] Exact Fed component name: **"Net Interest Income on Trading Assets and Liabilities"** — "Interest income and expense on trading assets are modeled as a single net quantity (interest minus expense), expressed as a ratio normalized by net trading assets (assets minus liabilities)" (PDF p. 225; md sec-215).
- [FACT] Rationale for the net treatment: "to avoid challenges in cross-firm comparability that could be introduced by differences in the extent of offsetting used in reporting trading assets and liabilities" (PDF p. 225; md sec-215).
- [FACT] This is a **NET item** — classified under neither interest income nor interest expense alone (inventory #11). Table A6 row: "Net interest income on trading assets and liabilities — Regression" (PDF pp. 168–169; md sec-148, md line 3356).
- [FACT] What this replaces (net reorganization, stated in the current-suite sections): the current trading-asset income regression iv.g merges with "a subset of [the current iv.i(4)] component corresponding to interest expense on trading liabilities"; the remaining iv.i(4) subset (other borrowed money and all other interest expense) goes to the proposed interest expense on other borrowing together with subordinated debt (PDF pp. 68, 96; md sec-57, sec-86). The p. 96 sentence calls that other-borrowing successor "a structural approach" — recorded verbatim as **SQ-27**, contradicting the Regression classification (Table A6, pp. 168–169) and the OLS estimation statement (p. 231); the classification and v.d(2) govern this handbook's reading [INT].
- [FACT] Output enters PPNR through net interest income (Eq A1; PDF pp. 6–8; md sec-2); nine-quarter projection horizon (PDF p. 6; md sec-2).

## 2. Model summary

[FACT] The ratio of a firm's net trading interest income to its net trading assets "depends on the contemporaneous level of the 3-month Treasury yield and a fixed effect estimated for that firm" (Eq A52; PDF p. 225; md sec-216). In estimation, the model is a weighted least squares panel regression over all FR Y-14Q reporters, weighted by each firm-quarter's net trading asset balance (PDF p. 226; md sec-216). [FACT — absence, verified against the page images] Equation A52 contains **no autoregressive term, no rolling-window fixed effect, no second macroeconomic factor, no seasonality term, and no firm grouping** — a deliberate simplification relative to both current-suite trading models (iv.g's Eq A8 carries a Year-AR term, a BBB-spread factor, and rolling-window fixed effects; iv.i(4)'s Eqs A13/A14 add firm groups): the rolling-window and recency alternatives were considered and rejected for stability (PDF pp. 228–229; md sec-218).

[FACT — absence] **The source states no projection mechanics for this model**: v.d(1) ends at Question A188 with no ratio→dollar step, no balance basis, no launch-point language, and no statement of how α_b would be obtained for a firm (pp. 225–230 verified as page images 2026-08-13). The projection construction in this chapter is therefore project method throughout — the [OQ-007] multiplication working interpretation plus the [PID-TRD-1] calibration — never attributable to the Federal Reserve.

[PID-TRD-1, 2026-08-13] Project sourcing of α_b: calibrated so the nine-quarter cumulative modeled net trading NII matches the cumulative path implied by the FRB-provided total-interest-income projection minus the six sibling interest-income models (§9) — the income-side mirror of PID-OB-5. A project method, never a Fed statement.

## 3. Inputs

### 3.1 Firm data inputs

| Input | Fed source | Dimensions | Units | Timing | Label |
|---|---|---|---|---|---|
| Trading assets average balance at PQ0 (`trading_assets_avg_balance_launchpoint`) | Fed-stated for estimation data: "the associated balances, are sourced from the Net Interest Income Worksheet of the FR Y-14Q, Schedule G" — **line items unnamed** [FACT + FACT absence] (PDF p. 225; md sec-216). Physical mapping [PID-TRD-2, user-supplied 2026-08-13]: workbook "NII NEW Models_with FRB_betas.xlsx", sheet **"14Q Sch G"**, cell **R30** (launch-point/4Q24 column) | b | USD (D-006 scale declared at config) | Launch-point (PQ0) average balance | [FACT] worksheet source; [PID-TRD-2] physical mapping |
| Trading liabilities average balance at PQ0 (`trading_liabilities_avg_balance_launchpoint`) | Same worksheet, line item unnamed [FACT absence]. Physical mapping [PID-TRD-2]: same sheet, cell **R112** | b | USD (D-006 scale declared at config) | Launch-point (PQ0) average balance | as above |
| Net trading assets, NetTA(b,0) (`net_trading_assets_launchpoint`) | Derived: trading assets − trading liabilities — the source's own netting definition, "net trading assets (assets minus liabilities)" [FACT for the netting] (PDF p. 225; md sec-215) | b | USD | PQ0 value, **held constant over the horizon** — a single Balance cell feeds every projection quarter on the reference tab [PID-TRD-3 observed; formerly the OQ-007 working interpretation] | [FACT] netting; [PID] constancy observed |

**Line-item identification note [INT, strong basis — PID-TRD-2]:** the reference tab's launch-point panel labels the two balance rows **13** (trading assets) and **37** (trading liabilities). These read as the Schedule G NII Worksheet line-item numbers: the sibling calculators consume items **14** (`ii_dep_banks_other`) and **15** (`ii_other_ida`) immediately after 13, and the PID-OB-2 other-borrowing balance set **36C + 38 + 39 skips exactly 37** — consistent with the net trading item owning it. Recorded as interpretation; the Fed-side "line items unnamed" absence stands.

[FACT — estimation context only, not projection inputs] The estimation numerators are built as "the reported average asset (liability) balance [multiplied] by the reported average asset (liability) rate, divided by four to convert annual to quarterly rates" (PDF p. 225; md sec-216). Under [PID-TRD-1] no PQ0 actual income, expense, or rate enters the projection — the average-rate items are documentation of the Fed's estimation data build, not inputs to this implementation.

### 3.2 Scenario inputs

| Scenario variable | Enters via | Frequency | Units | Label |
|---|---|---|---|---|
| 3-month Treasury yield, Treasury3m(q) (`usd_3m_treasury`) | Sole regressor of Eq A52, ×β | Quarterly, q = 1…9 — **no PQ0 value required** [PID-TRD-1: no launch-point backsolve] | Annualized yield; percent-vs-decimal scale metadata-driven, consistent with β's estimation scale [CODE] | [FACT] sole explanatory variable (PDF pp. 225, 227; md sec-216–217) |

[ALT] Variable selection (PDF pp. 226–227; md sec-217): the Board examined the term spread (10-year minus 3-month) and the BBB corporate credit spread (BBB corporate bond yield minus 10-year Treasury yield) alongside the 3-month Treasury. Only the 3-month Treasury coefficient was "consistently positive and statistically significant" in every combination; the other two were unstable — attributed to the high correlations among the three factors over the sample period — and added little explanatory power, so "in the interest of simplicity and model stability" only the 3-month Treasury is included. Neither spread variable is in the proposed model.

### 3.3 Parameters

| Parameter | Supplied or estimated | Value | Statistical significance (kept separate) | Label |
|---|---|---|---|---|
| β on the 3-month Treasury yield (`beta_treasury3m`) | Supplied — Board WLS estimate | **0.278** | \*\*\* (1% level) | [FACT] Table A9 (PDF p. 234; md sec-224; verified against the page image 2026-08-13). [PID-TRD-2] The reference workbook takes β from an **FRB-provided coefficients** input rather than typing it; the observed value equals the published 0.278 — the §12 parameter-fidelity check covers both (provided ≠ published must surface, never absorb — the auto-scalar lesson) |
| Firm fixed effect, α_b (`trading_firm_fixed_effect`) | Calibrated — project method [PID-TRD-1] | UNKNOWN from the source | Table A9 marks only "Yes" | [FACT] "Estimated coefficients for firm fixed-effects are not included in the table" (PDF p. 234; md sec-224); project sourcing per §9 |

Table A9 note, verbatim: "Statistical significance levels of 1%, 5%, and 10% are indicated as ***, **, and *, respectively." The 0.254**, −0.036***, and 0.066** in the same table belong to Equation A53(2) (`ie_other_borrowing`, model #12), not to this model. The trading row's BBB, commercial-paper-share, and subordinated-debt-share cells are empty [FACT].

### 3.4 Project calibration inputs [PID-TRD-1 — never Fed-stated]

| Input | Source | Dimensions | Units | Timing | Label |
|---|---|---|---|---|---|
| FRB total interest income, FRBIncome(b,q) (`frb_total_interest_income`) | Project-supplied (D-007 quarterly sheet; sign convention D-008 — income passes through as-entered). The Fed source states **no** total-interest-income aggregation for the proposed suite ([FACT] absence — Section v models each component independently). User-stated 2026-08-13: the FRB provides the firm's projections as **hardcoded summary-level numbers**; the income path's inclusion of the net trading item is **implied by the workbook's own residual construction**, not independently documented [OQ-023, extended] | b × scenario × q | USD per quarter | q = 1…9 | [PID-TRD-1] |
| Sibling modeled income paths (six) | Outputs of `ii_loans` (six-portfolio total incl. Table A8 scalars), `ii_dep_banks_other`, `ii_ust`, `ii_mbs`, `ii_other_sec`, `ii_other_ida` — supplied after those models complete (execution order, §9/§13) | b × scenario × q | USD per quarter | q = 1…9 | [PID-TRD-1] |

**Compare-basis note [CODE — §11]:** the residual is only as aligned as the subtraction basis. Two knowns from earlier increments: the reference workbook's securities income columns **exclude reinvestment income** (PID-SEC-8), and the auto compare basis is the workbook's 0.948 scalar vs the published 0.865 in production (PID-LOAN-32). The rows the user's own subtraction references are an open elicitation item (§11).

## 4. Timing and dimensions

Dimensions: ratio and net income are b × scenario × q; firm inputs are b-dimensional PQ0 snapshots. Output grain: firm × scenario × quarter.

| Quantity | Launch point (PQ0) | Projection quarters (q ≥ 1) | Label |
|---|---|---|---|
| NetTA(b,0) | Measured once (average balances, PQ0 — cells per PID-TRD-2) | Held constant — NetTA(b,0) in every quarter (single Balance cell, observed) | [PID-TRD-3 observed; source states nothing — OQ-007 resolved-for-project] |
| α_b | Fixed per firm (calibrated over PQ1–PQ9 per §9 [PID-TRD-1]; no PQ0 role) | Constant | [FACT] fixed (no time subscript in A52); [PID] sourcing |
| Treasury3m(q) | No PQ0 role [PID-TRD-1] | Contemporaneous scenario values | [FACT] "contemporaneous level" (PDF p. 225) |
| Ratio(b,q), TATL(b,q) | — | Computed each q; no dependence on q−1 | [FACT — absence of any lag term in A52] |

Constancy register: **constant** — net trading assets [PID-TRD-3 observed], α_b, β; **varying** — Treasury3m, rate, net trading NII.

## 5. Equations and variable definitions

**Equation A52** - Net Interest Income on Trading Assets and Liabilities Regression Model [FACT] (PDF p. 225; md sec-216; verified against the page image):

$$Ratio(b,t) = \beta\, Treasury3m(t) + \alpha_b + \varepsilon(b,t)$$

*where* (verbatim, PDF pp. 225–226): Treasury3m(t) is the 3-month Treasury yield, representing the risk-free short-term rate; α_b represents firm-level fixed effects, which account for heterogeneity in the average level of the ratio over time across firms; and ε(b,t) is the error term of the regression.

- **[SQ-26]** The where-list defines only those three symbols — **Ratio(b,t), the dependent variable, is not defined in the where-list** (the current-suite counterpart Eq A8 does define its Ratio in the where-list, p. 66). The definition lives in the section prose [FACT]: the numerator is the net quantity (interest minus expense) built from Schedule G average balances × average rates ÷ 4; the denominator is net trading assets (assets minus liabilities) (PDF p. 225; md sec-215–216).
- **Units of the ratio — recorded tension [FACT + INT + PID-TRD-3]:** the estimation numerator is a **quarterly** dollar amount (the ÷4 is stated inside the data construction [FACT], p. 225), so the source-literal reading makes the regression's LHS a quarterly yield — under which β = 0.278 implies ≈1.11 annualized pass-through and the projection would need **no** output ÷4. The **reference workbook instead projects an ANNUALIZED rate** ("Rates earned" = β·T3m + α_b, T3m in percent) **with an explicit ÷4 at the dollar step** [PID-TRD-3, screenshot-observed 2026-08-13] — under which 0.278 is a 28% annualized pass-through, also economically plausible; the magnitude of β does not discriminate. The source states neither the ratio's units nor any projection basis [FACT absence], so **the reference basis governs implementation**; the quarterly-LHS reading is retained here as the source-literal alternative — note it would imply **4× the scenario sensitivity** (quarterly tilt β·ΔT3m·NetTA vs the reference's β·ΔT3m·NetTA/4), which is what the basis choice actually decides.
- **Projection restatement [PID-TRD-3 basis; NOT source-stated]:** Ratio(b,q) = β·Treasury3m(q) + α_b (annualized; no error term), and TradingNII(b,q) (`trading_net_interest_income`) = Ratio(b,q) × NetTA(b,0) **÷ 4**. Unlike Eq A53, **no projection equations are printed in the source for this model** — this restatement is the project's reproduction of the observed reference construction.

## 6. Estimation versus projection

| | Estimation | Projection |
|---|---|---|
| Sample / horizon | [FACT] Unbalanced panel of **all FR Y-14Q reporters**; "estimated over a relatively long time period" — **window dates UNKNOWN** [FACT absence, verified pp. 226, 228; contrast: v.d(2) states 2020:Q2–2021:Q4] | Nine projection quarters q = 1…9 from PQ0 |
| Method | [FACT] "estimated as a weighted least squares (WLS) regression, weighted by the net trading asset balance (trading assets minus trading liabilities) in each firm-quarter" — rationale: capture all firms while limiting influence of firm-quarters with very small trading positions and volatile ratios (PDF p. 226; md sec-216). [CODE] Do **not** copy `ie_other_borrowing`'s OLS — each regression states its own estimator | No estimation; supplied β applied |
| Data build | [FACT] Numerators: reported average asset (liability) balance × reported average asset (liability) rate ÷ 4 (PDF p. 225) | No actuals consumed [PID-TRD-1] |
| Constant-β evidence | [FACT] Firm-specific regressions for all large trading firms fell within the 95% confidence interval of the panel estimate (PDF p. 228; md sec-218) | Single β = 0.278 for every firm |
| Error term | ε(b,t) present in A52 | Excluded in the project restatement [INT — no projection form exists in the source] |

## 7. Calculation workflow

1. **Launch-point net balance.** NetTA(b,0) = `trading_assets_avg_balance_launchpoint` − `trading_liabilities_avg_balance_launchpoint` [FACT netting; physical cells per PID-TRD-2 — §3.1]. NetTA(b,0) may not be zero (§12); a negative NetTA(b,0) surfaces as a validation failure pending user direction — the WLS weighting context treats net trading assets as a magnitude [INT].
2. **Parameter.** Load β = 0.278; store the significance stars as metadata, never in the numeric path (§3.3).
3. **Scenario preparation.** Align `usd_3m_treasury` to q = 1…9; percent-vs-decimal scale metadata-driven [CODE]. No PQ0 scenario value is consumed [PID-TRD-1].
4. **Pre-α rate path, each q.** R0(b,q) = β·Treasury3m(q) — the §5 projection rate with α_b excluded. **Annualized** units per the reference basis [PID-TRD-3] (§5).
5. **Implied residual target.** With the six sibling income models complete (§3.4): ImpliedTATL(b,q) = FRBIncome(b,q) − Loans(b,q) − DepBanksOther(b,q) − UST(b,q) − MBS(b,q) − OtherSec(b,q) − OtherIDA(b,q), q = 1…9 [PID-TRD-1]. Negative quarters are legal — log, never clamp (a net item can legitimately run negative).
6. **Fixed effect.** Calibrate α_b in closed form from the nine-quarter cumulative match (§9) [PID-TRD-1]; validate Σ_q NetTA(b,q) ≠ 0 before dividing (§12).
7. **Quarterly net income, each q.** `trading_net_interest_income[b,q] = (beta_treasury3m * usd_3m_treasury[q] + trading_firm_fixed_effect[b]) * net_trading_assets_launchpoint[b] / 4` — the ÷4 per the reference basis [PID-TRD-3] (§8). No floor, cap, or non-negativity constraint exists [FACT — absence].
8. **Reconciliation diagnostic and hedge hook.** Record the implied and modeled quarterly paths, their per-quarter differences, and the nine-quarter cumulative reconciliation (§9); expose the net income path for the cross-cutting v.c adjustment (§13); no hedge computation inside this model.

## 8. Output calculation

- [FACT] The only conversion the source states is **inside the estimation data construction** — the ratio's numerator is built as quarterly dollars (avg balance × avg rate ÷ 4; PDF p. 225; md sec-216). The source states **no output-step conversion and no projection basis at all** [FACT absence — §2].
- [PID-TRD-3 — reference basis, observed 2026-08-13] The reference workbook projects an **annualized** rate (β·T3m + α_b, T3m in percent) and books `trading_net_interest_income[b,q] = rate × NetTA(b,0) / 4` — the D-004 shape; the §9 closed form therefore carries the **PID-OB-5 ×4**. Output: `trading_net_interest_income`, b × scenario × q, USD per quarter, a NET quantity (negative values legal — log, never clamp).
- [CODE — tripwire, re-pointed at the basis] The quarterly-vs-annualized LHS choice scales both α_b and the scenario sensitivity by 4 (§5). **The basis must be declared, never inferred:** under the reference basis (implemented) the closed form is the OB shape **with ×4**; under the source-literal quarterly-LHS reading it would carry **no ×4**. Mixing the two — either direction — mis-scales α_b fourfold. The engine isolates the basis inside the calibration policy; the compare validates the reference basis empirically (a basis mix-up shows as a ≈×4 level/tilt miss).

## 9. Firm fixed-effect treatment

- [FACT] α_b is estimated by the Board but not published (Table A9: firm fixed-effects "Yes", values excluded; PDF p. 234). The Fed's stated role for α_b: firms' "individual preferences for holding trading assets, which can vary in risk, origination date, underlying interest rate terms (e.g., fixed vs. variable), and duration" leave average yields varying across firms after controlling for macro factors; fixed effects capture differences in **level**, not sensitivity (PDF pp. 227–228; md sec-217–218).
- **[PID-TRD-1, user-confirmed 2026-08-13] PROJECT IMPLEMENTATION DECISION — USER CONFIRMED.** α_b is calibrated so that the **nine-quarter cumulative** modeled net trading NII equals the nine-quarter cumulative implied by the FRB-provided total-interest-income path minus the six sibling income models — the income-side mirror of PID-OB-5. User-stated basis (verbatim intent): the workbook backsolves the fixed effect "similar to how we did it for [GIE] Other Borrowings … we have the private results from FRB for Interest Income, and we can use that minus all the other component we have calculated … find the fixed effect such that [the trading NII] 9Q is same as the implied FRB result, not necessarily each Quarter are the same." PQ0 actuals are **not used** anywhere in this calibration. This supersedes D-002's launch-point working method for this model — D-002 now has no remaining scope. Never attributable to the Federal Reserve.
- **Implied residual target [PID-TRD-1].** With the six sibling models' completed quarterly income paths (§3.4; all USD per quarter):

  $$ImpliedTATL(b,q) = FRBIncome(b,q) - \sum_{m \in \text{six income models}} Income_m(b,q), \qquad q = 1,\dots,9$$

  Individual quarters may be negative — legal; log, never clamp.
- **Closed-form calibration [PID-TRD-1, basis per PID-TRD-3].** Let R0(b,q) = β·Treasury3m(q) — the pre-α **annualized** rate — and NetTA(b,q) the net trading asset balance (= NetTA(b,0) every quarter; a single Balance cell on the reference tab). The single α_b, constant across q = 1…9, solves

  $$\sum_{q=1}^{9} \frac{NetTA(b,q)\,\left(R0(b,q) + \alpha_b\right)}{4} \;=\; \sum_{q=1}^{9} ImpliedTATL(b,q)$$

  The objective is linear in α_b, so the solution is closed-form (no numerical optimization):

  $$\alpha_b = \frac{4 \sum_{q=1}^{9} ImpliedTATL(b,q) \;-\; \sum_{q=1}^{9} NetTA(b,q)\,R0(b,q)}{\sum_{q=1}^{9} NetTA(b,q)}$$

  α_b is an **annualized intercept** (percent/decimal per the declared rate scale) and the formula is the **PID-OB-5 shape, ×4 included** — under the reference basis the ×4 reverses the ÷4 at the dollar step exactly as in `ie_other_borrowing` (§8 tripwire: under the source-literal quarterly-LHS reading there would be no ×4; the basis is declared, never mixed). Under the flat balance this reduces to α_b = 4·Σ ImpliedTATL / (9·NetTA(b,0)) − β·mean(Treasury3m). Screenshot verification (2026-08-13, in-session): the reference tab realizes exactly this — fitted rate × balance ÷ 4 reproduces its modeled row, the two 9Q-cumulative cells match, and the per-quarter difference row sums to ≈ 0 with average 0.
- **Rules [PID-TRD-1].** (i) The **cumulative** nine-quarter total is matched exactly — individual quarterly modeled amounts are *not* forced to equal the quarterly implied residuals. (ii) The published β is unchanged. (iii) One α_b per firm, constant across PQ1–PQ9 — never a per-quarter α. (iv) α_b is a **project calibration parameter**, never a Federal Reserve published coefficient. (v) No floor or cap is imposed on α_b. (vi) If Σ_q NetTA(b,q) is zero or invalid, calibration fails with a validation error — no fallback is invented.
- **Diagnostics [PID-TRD-1].** The implied quarterly path, the modeled quarterly path, their per-quarter differences (which sum to ≈ 0 by construction), and the nine-quarter cumulative reconciliation difference are preserved, even though only the cumulative total is calibrated exactly — the reference tab itself carries all three rows plus the average (observed). Monitor |α_b| as a sanity screen — with the annualized basis [PID-TRD-3] the liability side's **0.5 annualized-decimal screen (`RATE_SCALE_GUARD`) applies unchanged** [CODE, project safeguard]; large values may indicate scale mismatch or a residual target inconsistent with the modeled components.
- **[OQ-023 — extended 2026-08-13]** The FRB paths are hardcoded summary-level numbers in the reference workbook (user-stated); the income path's inclusion of the net trading item is **implied by the residual construction itself**, not independently documented, and the scope alignment of each path with the modeled components remains TO BE CONFIRMED in the approved environment.

## 10. Fed-stated assumptions and limitations

All [FACT] (PDF pp. 227–229; md sec-218), restated faithfully:

1. **Top-down composition.** The model "is top-down in nature and does not attempt to capture the specific composition of any firm's trading portfolio at any given point in time"; compositional details could affect both the level and the macro sensitivity — e.g., "firms with higher proportions of equity trading activity might have lower sensitivity to short-term interest rates, since equity positions do not generate interest income."
2. **Level captured, sensitivity not.** "While differences in net interest income level are captured through the firm-specific fixed effects, differences in sensitivities are not." Compositional data were considered and rejected: FR Y-9C Schedules HC-D/HC-L focus on cash securities with limited derivatives information; FR Y-14Q Schedule F covers only a subset of filers, which "would need a separate model … for non-filers."
3. **Common sensitivity supported.** Firm-specific regressions for all large trading firms generally fell within the 95% confidence interval of the weighted panel estimate, "supporting the use of a single common sensitivity estimate."
4. **Stability over a long sample.** Estimation "over a relatively long time period" implies the spread and interest-rate sensitivity of a firm's trading NII are stable over time — which "could conflict with the observation that firms may adjust their trading positions"; rolling-window fixed effects were considered and rejected (lower stability, higher projection volatility).
5. **Full-sample β preferred.** Rolling-window regressions suggest the 3-month-Treasury sensitivity "may have increased over the most recent interest rate cycle"; the Board kept the full-sample estimate — recency-weighted schemes "could potentially result in less stable coefficient estimates."
6. **Spread factors unidentifiable.** The term-spread and credit-spread effects cannot be separately identified (high correlations with the 3-month Treasury). A longer FR Y-9C sample was considered, but there "interest expense on trading liabilities is combined with interest expense on other borrowed money" and the correlations would likely remain high; mitigation: large trading firms "typically try to limit" market-value sensitivity, which caps sensitivity to long rates and credit spreads.

## 11. User-confirmed implementation mappings

- **[PID-TRD-1]** Calibration mode (§9) — user-confirmed 2026-08-13 at the Increment 4 gate. **[PID-TRD-2]** Physical inputs (§3.1) and the FRB-provided β source (§3.3) — user-supplied same day. **[PID-TRD-3]** Annualized-÷4 basis (§5/§8/§9) — observed on the user-supplied trading-tab screenshot same day. Registered in `docs/handbook/open-questions.md`.
- **FRB path facts (user-stated 2026-08-13):** the three FRB-provided projections (interest income / total interest expense / net interest income) are hardcoded summary-level numbers in the reference workbook; the income path arrives via the D-007 quarterly sheet as `frb_total_interest_income` (D-008 sign convention: income as-entered).
- **Closed by the screenshot (2026-08-13):** the physical balance cells (PID-TRD-2 — the former Required item 1); no scalar/multiplier on the trading row (rate × balance ÷ 4 reproduces the modeled row with no residual factor); the 3-month Treasury row matches the project MEV path; the modeled and implied rows plus their difference row are carried on the tab itself.
- **Open elicitation items:**
  1. *(Helpful — round-0 alignment; the compare's implied-path diagnostic arbitrates regardless.)* The PQ1 cell formula of the tab's **"Implied FRB results" row**: which sheets/rows it subtracts from the FRB income number — this settles the securities-reinvestment basis (PID-SEC-8) and the auto scalar basis (PID-LOAN-32, one config line) for our implied path before round 1.
  2. *(Required at compare rounds.)* The tab's **"NII TATL" and "Implied FRB results" rows, PQ1..PQ9**, pasted at the cell — the complete compare target.
- **Workbook cosmetic defects (flagged for the owners, cosmetic only — PID-TRD-3):** the trading tab's green banner reads "Interest Expense on Foregin Deposits" (wrong component + typo; template leftover), the gray banner reuses the other-borrowing label "firm specific credit spreads (δ)" (no δ exists in Eq A52), and the source annotation reads "p.230" where v.d(1) starts on p. 225. None affect the numbers.
- **Execution order [PID-TRD-1]:** the six sibling income models run first; this model runs last, consuming their completed paths — the project-level analog of the PID-OB-5 ordering. The Fed-suite independence statement stands as the [FACT] (§13).

## 12. Validation requirements ([CODE] — non-normative; no invented fallbacks, failures surface)

- **Input presence:** both PQ0 trading balances present per firm (physical cells per PID-TRD-2; the money **scale** stays config-declared per D-006 and refuses to run undeclared); `frb_total_interest_income` and all six sibling income paths complete for q = 1…9 and aligned on firm, scenario, and quarter before calibration; a failed calibration blocks the firm — α_b never defaults to zero.
- **Balance sanity:** NetTA(b,0) ≠ 0 (zero breaks the ratio and the calibration divisor); a **negative** NetTA(b,0) surfaces as a validation failure pending user direction [INT — the source's WLS weighting treats net trading assets as a magnitude; no source statement covers a net-liability trading book].
- **Scenario paths:** `usd_3m_treasury` complete for q = 1…9 per scenario, no gaps; no PQ0 value required [PID-TRD-1].
- **Rate scale:** percent-vs-decimal never assumed; metadata-driven and consistent between the 3-month Treasury series and β's estimation scale.
- **Parameter fidelity:** configured β equals Table A9 exactly (0.278) — verify against the PDF page, not retyped copies; significance metadata (\*\*\*) stored separately and never used numerically. [PID-TRD-2] The reference sources β from an FRB-provided coefficients input — if that provided value ever differs from the published 0.278, **surface it, never absorb it** (the auto published-vs-computed scalar lesson); observed equal 2026-08-13.
- **Units screen [D-006 class]:** hard-fail when cumulative |FRBIncome| and cumulative |Σ sibling income| differ by ≥50× (probable unit mismatch the closed-form α_b would otherwise silently absorb — the exact failure class the OB guard covers).
- **Calibration guards [PID-TRD-1]:** Σ_q NetTA(b,q) ≠ 0 and finite before the closed-form division; post-condition |Σ_q Modeled − Σ_q Implied| ≈ 0 within float tolerance (exact by construction).
- **Edge monitors:** negative ImpliedTATL(b,q) quarters are legal — log, never clamp; negative modeled TATL(b,q) is legal (a net item; no constraint exists in the source) — log, never clamp; |α_b| ≥ 0.5 annualized-decimal screen (`RATE_SCALE_GUARD`, §9) warns, never blocks.

## 13. Dependencies and hedge interface

- [FACT] No proposed model's output enters Eq A52; the Fed-suite models are independent. **Project-level exception [PID-TRD-1]:** the calibration consumes the six completed sibling income paths plus `frb_total_interest_income` — mirror of the PID-OB-5 exception on the expense side; no circular dependency (this model is a pure consumer).
- [FACT — absence] v.d(1) contains no hedge term (conventions §9 lists this model among the components with no embedded hedge machinery). The cross-cutting v.c adjustment (Eqs A49–A51, contingent on the proposed FR Y-14Q B.2/B.3 collection; PDF pp. 220–223; md sec-210–212) may later adjust interest income and expense components; allocation across components is unresolved [OQ-005]. This model exposes its net income path and computes no hedge term.
- [CODE] Under PID-TRD-1 the fixed effect absorbs the full residual to the FRB income path — including any hedge effects embedded there. If v.c is ever applied to this component, note the double-counting risk against what the calibrated α_b already carries (same caution as `ie_other_borrowing` §12).
- **Downstream:** the income orchestrator aggregates this output into total interest income; the combined-NII monitor consumes both family totals against `frb_net_interest_income` (Increment 4 scope; conventions §10 as revised 2026-08-13).

## 14. Open issues

- **OQ-007 — RESOLVED FOR PROJECT IMPLEMENTATION (2026-08-13, via PID-TRD-2/PID-TRD-3).** The multiplication step, the multiplicand (Schedule G sheet cells R30 − R112, flat), and the annualized-÷4 basis are all observed at the reference cells. Source-side absence unchanged (no projection is stated); the quarterly-vs-annualized LHS tension is recorded in §5.
- **OQ-009 — RESOLVED FOR PROJECT IMPLEMENTATION (2026-08-13, via PID-TRD-1).** The Fed's non-disclosure of α_b remains the [FACT]; both regression models now carry project calibrations (PID-OB-5; PID-TRD-1).
- **OQ-023 — OPEN, extended 2026-08-13.** FRB path lineage: hardcoded summary numbers; income-path scope implied-by-construction; per-path scope alignment TO BE CONFIRMED.
- **OQ-005 — OPEN.** Hedge-adjustment allocation (§13).
- **Elicitation items** (§11): the "Implied FRB results" row's formula references (Helpful — round-0 alignment); the two reference rows PQ1..PQ9 at compare rounds.

## 15. Key source references

| Claim | (PDF p.; md anchor) |
|---|---|
| Component name; net quantity (interest minus expense); ratio normalized by net trading assets; offsetting-comparability rationale | (PDF p. 225; md sec-215) |
| Contemporaneous 3M Treasury + firm fixed effect; Schedule G worksheet estimation data; average balance × average rate ÷ 4 numerator build | (PDF p. 225; md sec-216) |
| Eq A52 as displayed; where-list (Treasury3m, α_b, ε only — SQ-26) | (PDF pp. 225–226; md sec-216) |
| WLS weighted by net trading asset balance; unbalanced panel of all FR Y-14Q reporters; weighting rationale | (PDF p. 226; md sec-216) |
| Variable selection: term spread and BBB credit spread examined and rejected (collinearity; simplicity and stability) | (PDF pp. 226–227; md sec-217) |
| Fixed-effect rationale (firm preferences; level heterogeneity) | (PDF p. 227; md sec-217) |
| Assumptions and limitations 1–6 (incl. the 95%-CI constant-β test; "relatively long time period"; rolling-window rejection; Y-9C trading-liability commingling) | (PDF pp. 227–229; md sec-218) |
| Question A188 | (PDF p. 229; md sec-219) |
| Table A9 row (β = 0.278***); significance note; fixed effects not included; FR Y-14Q / FR Y-9C data basis | (PDF p. 234; md sec-224) |
| Table A6 regression classification of the net item | (PDF pp. 168–169; md sec-148) |
| Current-suite comparison: iv.g scope and Eq A8 (Y-9C data, BHCK4069/BHCK3545, footnotes 23–24); net-model forward reference; Question A32 | (PDF pp. 65–68; md sec-54–58) |
| Current-suite comparison: iv.i(4) scope and Eqs A13/A14; reorganization paragraph (trading-liabilities subset to the net model; remainder to other borrowing — "structural approach" wording = SQ-27); Question A66 | (PDF pp. 90–96; md sec-80–87) |
| Nine-quarter horizon; PPNR identity (Eq A1) | (PDF pp. 6–8; md sec-2) |
| D-002 (superseded 2026-08-13), D-005, D-006, D-007, D-008 conventions; PID-TRD-1/2/3; PID-OB-5 (mirrored pattern) | `docs/handbook/open-questions.md` decision log; user confirmations 2026-08-13 (§3.1, §9, §11 — gate Q&A + supplied cells + trading-tab screenshot) |

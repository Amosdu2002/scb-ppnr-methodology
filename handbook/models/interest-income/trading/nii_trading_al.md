# 11. Net Interest Income on Trading Assets and Liabilities (`nii_trading_al`)

> **STATUS: Proposed for the 2026 stress test — public-comment stage, NOT adopted.**
> Source: Section B.v.d(1) (PDF pp. 225–230; md sec-215–219; the one-line v.d parent heading is sec-214, same page); parameters in Section B.v.e, Table A9 (PDF p. 234; md sec-224). Model type per Table A6: **Regression** (PDF pp. 168–169; md sec-148). Comparison context (current 2025 suite): iv.g (PDF pp. 65–68; md sec-54–58) and iv.i(4) (PDF pp. 90–97; md sec-80–87).
> Integrity flags affecting this chapter: **SQ-26** (Eq A52's where-list omits its dependent variable Ratio(b,t) — defined only in prose; filed this session) and **SQ-27** (current-suite p. 96 and Question A66 call the proposed other-borrowing successor a "structural approach" while v.d(2)/Table A6 classify it Regression; filed this session, cross-referenced at inventory #12). No conversion artifacts affect sec-214–219 or sec-224 (pp. 225–230 and 234 verified against the page images 2026-08-13, including the first image pass over pp. 227–229).
> Chapter format: D-009 compact 13-section skeleton **plus** the two regression-model sections (Estimation versus projection = §6; Firm fixed-effect treatment = §9), per the `ie_other_borrowing` precedent.
> Chapter review state: **REVIEWED** — independent source-grounding review 2026-08-13, verdict APPROVE WITH OPEN IMPLEMENTATION ITEMS (`reviews/interest-income/trading/nii_trading_al.review.md`). Specification: `specifications/interest-income/trading/nii_trading_al.yaml`. Approved content is never silently overwritten.
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
| Trading assets average balance at PQ0 (`trading_assets_avg_balance_launchpoint`) | Fed-stated for estimation data: "the associated balances, are sourced from the Net Interest Income Worksheet of the FR Y-14Q, Schedule G" — **line items unnamed** [FACT + FACT absence] (PDF p. 225; md sec-216). Physical row: **TO_BE_CONFIRMED** (elicitation open — §11) | b | USD (D-006 scale declared) | Launch-point (PQ0) value | [FACT] worksheet source; physical mapping pending |
| Trading liabilities average balance at PQ0 (`trading_liabilities_avg_balance_launchpoint`) | Same worksheet, line item unnamed [FACT absence]. Physical row: **TO_BE_CONFIRMED** | b | USD (D-006 scale declared) | Launch-point (PQ0) value | as above |
| Net trading assets, NetTA(b,0) (`net_trading_assets_launchpoint`) | Derived: trading assets − trading liabilities — the source's own netting definition, "net trading assets (assets minus liabilities)" [FACT for the netting] (PDF p. 225; md sec-215) | b | USD | PQ0 value, **held constant over the horizon [INT — OQ-007]** (flat-balance working interpretation; the source states no projection balance basis) | [FACT] netting; [INT] constancy |

[FACT — estimation context only, not projection inputs] The estimation numerators are built as "the reported average asset (liability) balance [multiplied] by the reported average asset (liability) rate, divided by four to convert annual to quarterly rates" (PDF p. 225; md sec-216). Under [PID-TRD-1] no PQ0 actual income, expense, or rate enters the projection — the average-rate items are documentation of the Fed's estimation data build, not inputs to this implementation.

### 3.2 Scenario inputs

| Scenario variable | Enters via | Frequency | Units | Label |
|---|---|---|---|---|
| 3-month Treasury yield, Treasury3m(q) (`usd_3m_treasury`) | Sole regressor of Eq A52, ×β | Quarterly, q = 1…9 — **no PQ0 value required** [PID-TRD-1: no launch-point backsolve] | Annualized yield; percent-vs-decimal scale metadata-driven, consistent with β's estimation scale [CODE] | [FACT] sole explanatory variable (PDF pp. 225, 227; md sec-216–217) |

[ALT] Variable selection (PDF pp. 226–227; md sec-217): the Board examined the term spread (10-year minus 3-month) and the BBB corporate credit spread (BBB corporate bond yield minus 10-year Treasury yield) alongside the 3-month Treasury. Only the 3-month Treasury coefficient was "consistently positive and statistically significant" in every combination; the other two were unstable — attributed to the high correlations among the three factors over the sample period — and added little explanatory power, so "in the interest of simplicity and model stability" only the 3-month Treasury is included. Neither spread variable is in the proposed model.

### 3.3 Parameters

| Parameter | Supplied or estimated | Value | Statistical significance (kept separate) | Label |
|---|---|---|---|---|
| β on the 3-month Treasury yield (`beta_treasury3m`) | Supplied — Board WLS estimate | **0.278** | \*\*\* (1% level) | [FACT] Table A9 (PDF p. 234; md sec-224; verified against the page image 2026-08-13) |
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
| NetTA(b,0) | Measured once (average balances, PQ0) | Held constant — NetTA(b,0) in every quarter | [INT — OQ-007] (no source statement exists) |
| α_b | Fixed per firm (calibrated over PQ1–PQ9 per §9 [PID-TRD-1]; no PQ0 role) | Constant | [FACT] fixed (no time subscript in A52); [PID] sourcing |
| Treasury3m(q) | No PQ0 role [PID-TRD-1] | Contemporaneous scenario values | [FACT] "contemporaneous level" (PDF p. 225) |
| Ratio(b,q), TATL(b,q) | — | Computed each q; no dependence on q−1 | [FACT — absence of any lag term in A52] |

Constancy register: **constant** — net trading assets [INT], α_b, β; **varying** — Treasury3m, ratio, net trading NII.

## 5. Equations and variable definitions

**Equation A52** - Net Interest Income on Trading Assets and Liabilities Regression Model [FACT] (PDF p. 225; md sec-216; verified against the page image):

$$Ratio(b,t) = \beta\, Treasury3m(t) + \alpha_b + \varepsilon(b,t)$$

*where* (verbatim, PDF pp. 225–226): Treasury3m(t) is the 3-month Treasury yield, representing the risk-free short-term rate; α_b represents firm-level fixed effects, which account for heterogeneity in the average level of the ratio over time across firms; and ε(b,t) is the error term of the regression.

- **[SQ-26]** The where-list defines only those three symbols — **Ratio(b,t), the dependent variable, is not defined in the where-list** (the current-suite counterpart Eq A8 does define its Ratio in the where-list, p. 66). The definition lives in the section prose [FACT]: the numerator is the net quantity (interest minus expense) built from Schedule G average balances × average rates ÷ 4; the denominator is net trading assets (assets minus liabilities) (PDF p. 225; md sec-215–216).
- **Units of the ratio [INT, strong basis]:** the numerator is a **quarterly** dollar amount (the ÷4 is stated inside the data construction [FACT]), so Ratio is a quarterly yield on net trading assets; the source states no units for Ratio [FACT absence]. Corroboration: if Ratio were annualized, near-parity pass-through from the 3-month Treasury would put β near 1; β = 0.278 ≈ 1.11/4 is exactly a quarterly-LHS/annualized-RHS scaling.
- **Projection restatement [INT — OQ-007 / PID-TRD-1; NOT source-stated]:** Ratio(b,q) = β·Treasury3m(q) + α_b (no error term), and TradingNII(b,q) (`trading_net_interest_income`) = Ratio(b,q) × NetTA(b,0). Unlike Eq A53, **no projection equations are printed in the source for this model** — this restatement is the project's construction.

## 6. Estimation versus projection

| | Estimation | Projection |
|---|---|---|
| Sample / horizon | [FACT] Unbalanced panel of **all FR Y-14Q reporters**; "estimated over a relatively long time period" — **window dates UNKNOWN** [FACT absence, verified pp. 226, 228; contrast: v.d(2) states 2020:Q2–2021:Q4] | Nine projection quarters q = 1…9 from PQ0 |
| Method | [FACT] "estimated as a weighted least squares (WLS) regression, weighted by the net trading asset balance (trading assets minus trading liabilities) in each firm-quarter" — rationale: capture all firms while limiting influence of firm-quarters with very small trading positions and volatile ratios (PDF p. 226; md sec-216). [CODE] Do **not** copy `ie_other_borrowing`'s OLS — each regression states its own estimator | No estimation; supplied β applied |
| Data build | [FACT] Numerators: reported average asset (liability) balance × reported average asset (liability) rate ÷ 4 (PDF p. 225) | No actuals consumed [PID-TRD-1] |
| Constant-β evidence | [FACT] Firm-specific regressions for all large trading firms fell within the 95% confidence interval of the panel estimate (PDF p. 228; md sec-218) | Single β = 0.278 for every firm |
| Error term | ε(b,t) present in A52 | Excluded in the project restatement [INT — no projection form exists in the source] |

## 7. Calculation workflow

1. **Launch-point net balance.** NetTA(b,0) = `trading_assets_avg_balance_launchpoint` − `trading_liabilities_avg_balance_launchpoint` [FACT netting; physical rows TO_BE_CONFIRMED — §11]. NetTA(b,0) may not be zero (§12); a negative NetTA(b,0) surfaces as a validation failure pending user direction — the WLS weighting context treats net trading assets as a magnitude [INT].
2. **Parameter.** Load β = 0.278; store the significance stars as metadata, never in the numeric path (§3.3).
3. **Scenario preparation.** Align `usd_3m_treasury` to q = 1…9; percent-vs-decimal scale metadata-driven [CODE]. No PQ0 scenario value is consumed [PID-TRD-1].
4. **Pre-α ratio path, each q.** r0(b,q) = β·Treasury3m(q) — the §5 projection ratio with α_b excluded. Quarterly-ratio units (§5).
5. **Implied residual target.** With the six sibling income models complete (§3.4): ImpliedTATL(b,q) = FRBIncome(b,q) − Loans(b,q) − DepBanksOther(b,q) − UST(b,q) − MBS(b,q) − OtherSec(b,q) − OtherIDA(b,q), q = 1…9 [PID-TRD-1]. Negative quarters are legal — log, never clamp (a net item can legitimately run negative).
6. **Fixed effect.** Calibrate α_b in closed form from the nine-quarter cumulative match (§9) [PID-TRD-1]; validate Σ_q NetTA(b,q) ≠ 0 before dividing (§12).
7. **Quarterly net income, each q.** `trading_net_interest_income[b,q] = (beta_treasury3m * usd_3m_treasury[q] + trading_firm_fixed_effect[b]) * net_trading_assets_launchpoint[b]` — **no ÷4 at this step** (§8). No floor, cap, or non-negativity constraint exists [FACT — absence].
8. **Reconciliation diagnostic and hedge hook.** Record the implied and modeled quarterly paths, their per-quarter differences, and the nine-quarter cumulative reconciliation (§9); expose the net income path for the cross-cutting v.c adjustment (§13); no hedge computation inside this model.

## 8. Output calculation

- [FACT] The annual→quarterly ÷4 for this component is **stated inside the Fed's data construction** — the ratio's numerator is already a quarterly dollar amount (PDF p. 225; md sec-216). Per the asset-side conventions §4, where the source states its own conversion the source governs, not D-004.
- [CODE — tripwire] Consequently the output step multiplies the quarterly ratio by the net balance **with no further ÷4**, and the §9 closed form carries **no ×4** — unlike `ie_other_borrowing`, whose rates are annualized and whose calibration converts with ×4. Copying the OB formula verbatim would overstate α_b by a factor of four. Output: `trading_net_interest_income`, b × scenario × q, USD per quarter, a NET quantity (negative values legal — log, never clamp).

## 9. Firm fixed-effect treatment

- [FACT] α_b is estimated by the Board but not published (Table A9: firm fixed-effects "Yes", values excluded; PDF p. 234). The Fed's stated role for α_b: firms' "individual preferences for holding trading assets, which can vary in risk, origination date, underlying interest rate terms (e.g., fixed vs. variable), and duration" leave average yields varying across firms after controlling for macro factors; fixed effects capture differences in **level**, not sensitivity (PDF pp. 227–228; md sec-217–218).
- **[PID-TRD-1, user-confirmed 2026-08-13] PROJECT IMPLEMENTATION DECISION — USER CONFIRMED.** α_b is calibrated so that the **nine-quarter cumulative** modeled net trading NII equals the nine-quarter cumulative implied by the FRB-provided total-interest-income path minus the six sibling income models — the income-side mirror of PID-OB-5. User-stated basis (verbatim intent): the workbook backsolves the fixed effect "similar to how we did it for [GIE] Other Borrowings … we have the private results from FRB for Interest Income, and we can use that minus all the other component we have calculated … find the fixed effect such that [the trading NII] 9Q is same as the implied FRB result, not necessarily each Quarter are the same." PQ0 actuals are **not used** anywhere in this calibration. This supersedes D-002's launch-point working method for this model — D-002 now has no remaining scope. Never attributable to the Federal Reserve.
- **Implied residual target [PID-TRD-1].** With the six sibling models' completed quarterly income paths (§3.4; all USD per quarter):

  $$ImpliedTATL(b,q) = FRBIncome(b,q) - \sum_{m \in \text{six income models}} Income_m(b,q), \qquad q = 1,\dots,9$$

  Individual quarters may be negative — legal; log, never clamp.
- **Closed-form calibration [PID-TRD-1].** Let r0(b,q) = β·Treasury3m(q) — the pre-α **quarterly** ratio — and NetTA(b,q) the net trading asset balance (= NetTA(b,0) every quarter under the [OQ-007] flat-balance working interpretation). The single α_b, constant across q = 1…9, solves

  $$\sum_{q=1}^{9} NetTA(b,q)\,\left(r0(b,q) + \alpha_b\right) \;=\; \sum_{q=1}^{9} ImpliedTATL(b,q)$$

  The objective is linear in α_b, so the solution is closed-form (no numerical optimization):

  $$\alpha_b = \frac{\sum_{q=1}^{9} ImpliedTATL(b,q) \;-\; \sum_{q=1}^{9} NetTA(b,q)\,r0(b,q)}{\sum_{q=1}^{9} NetTA(b,q)}$$

  α_b is a **quarterly-ratio intercept** — there is **no ×4** in this formula (§8 tripwire; the OB counterpart's ×4 reverses a D-004 ÷4 that does not exist here). Under the flat balance this reduces to α_b = Σ ImpliedTATL / (9·NetTA(b,0)) − β·mean(Treasury3m).
- **Rules [PID-TRD-1].** (i) The **cumulative** nine-quarter total is matched exactly — individual quarterly modeled amounts are *not* forced to equal the quarterly implied residuals. (ii) The published β is unchanged. (iii) One α_b per firm, constant across PQ1–PQ9 — never a per-quarter α. (iv) α_b is a **project calibration parameter**, never a Federal Reserve published coefficient. (v) No floor or cap is imposed on α_b. (vi) If Σ_q NetTA(b,q) is zero or invalid, calibration fails with a validation error — no fallback is invented.
- **Diagnostics [PID-TRD-1].** The implied quarterly path, the modeled quarterly path, their per-quarter differences (which sum to ≈ 0 by construction), and the nine-quarter cumulative reconciliation difference are preserved, even though only the cumulative total is calibrated exactly. Monitor |α_b| as a sanity screen — quarterly-ratio counterpart of the liability side's 0.5 annualized screen is **0.125** [CODE, project safeguard]; large values may indicate scale mismatch or a residual target inconsistent with the modeled components.
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

- **[PID-TRD-1]** Calibration mode (§9) — user-confirmed 2026-08-13 at the Increment 4 gate. Registered in `handbook/open-questions.md`.
- **FRB path facts (user-stated 2026-08-13):** the three FRB-provided projections (interest income / total interest expense / net interest income) are hardcoded summary-level numbers in the reference workbook; the income path arrives via the D-007 quarterly sheet as `frb_total_interest_income` (D-008 sign convention: income as-entered).
- **Open elicitation items (Required before the engine compare):**
  1. Physical PQ0 rows for the trading assets and trading liabilities average balances (row labels / Schedule G item numbers if any; units/scale per D-006) — the only new firm inputs.
  2. The component rows the workbook's residual subtraction references — settles the securities-reinvestment basis (PID-SEC-8) and the auto scalar basis (PID-LOAN-32, one config line) for the implied path.
  3. At compare rounds: the reference trading line PQ1..PQ9 (and the implied-TATL row if carried separately), pasted at the cell.
- **Helpful (not blocking):** any scalar/multiplier on the trading row; the trading line's sign/entry convention; confirmation it consumes the same MEV 3-month Treasury series.
- **Execution order [PID-TRD-1]:** the six sibling income models run first; this model runs last, consuming their completed paths — the project-level analog of the PID-OB-5 ordering. The Fed-suite independence statement stands as the [FACT] (§13).

## 12. Validation requirements ([CODE] — non-normative; no invented fallbacks, failures surface)

- **Input presence:** both PQ0 trading balances present per firm (TO_BE_CONFIRMED physical rows refuse to run until confirmed — `require_confirmed` discipline); `frb_total_interest_income` and all six sibling income paths complete for q = 1…9 and aligned on firm, scenario, and quarter before calibration; a failed calibration blocks the firm — α_b never defaults to zero.
- **Balance sanity:** NetTA(b,0) ≠ 0 (zero breaks the ratio and the calibration divisor); a **negative** NetTA(b,0) surfaces as a validation failure pending user direction [INT — the source's WLS weighting treats net trading assets as a magnitude; no source statement covers a net-liability trading book].
- **Scenario paths:** `usd_3m_treasury` complete for q = 1…9 per scenario, no gaps; no PQ0 value required [PID-TRD-1].
- **Rate scale:** percent-vs-decimal never assumed; metadata-driven and consistent between the 3-month Treasury series and β's estimation scale.
- **Parameter fidelity:** configured β equals Table A9 exactly (0.278) — verify against the PDF page, not retyped copies; significance metadata (\*\*\*) stored separately and never used numerically.
- **Units screen [D-006 class]:** hard-fail when cumulative |FRBIncome| and cumulative |Σ sibling income| differ by ≥50× (probable unit mismatch the closed-form α_b would otherwise silently absorb — the exact failure class the OB guard covers).
- **Calibration guards [PID-TRD-1]:** Σ_q NetTA(b,q) ≠ 0 and finite before the closed-form division; post-condition |Σ_q Modeled − Σ_q Implied| ≈ 0 within float tolerance (exact by construction).
- **Edge monitors:** negative ImpliedTATL(b,q) quarters are legal — log, never clamp; negative modeled TATL(b,q) is legal (a net item; no constraint exists in the source) — log, never clamp; |α_b| ≥ 0.125 quarterly-ratio screen (§9) warns, never blocks.

## 13. Dependencies and hedge interface

- [FACT] No proposed model's output enters Eq A52; the Fed-suite models are independent. **Project-level exception [PID-TRD-1]:** the calibration consumes the six completed sibling income paths plus `frb_total_interest_income` — mirror of the PID-OB-5 exception on the expense side; no circular dependency (this model is a pure consumer).
- [FACT — absence] v.d(1) contains no hedge term (conventions §9 lists this model among the components with no embedded hedge machinery). The cross-cutting v.c adjustment (Eqs A49–A51, contingent on the proposed FR Y-14Q B.2/B.3 collection; PDF pp. 220–223; md sec-210–212) may later adjust interest income and expense components; allocation across components is unresolved [OQ-005]. This model exposes its net income path and computes no hedge term.
- [CODE] Under PID-TRD-1 the fixed effect absorbs the full residual to the FRB income path — including any hedge effects embedded there. If v.c is ever applied to this component, note the double-counting risk against what the calibrated α_b already carries (same caution as `ie_other_borrowing` §12).
- **Downstream:** the income orchestrator aggregates this output into total interest income; the combined-NII monitor consumes both family totals against `frb_net_interest_income` (Increment 4 scope; conventions §10 as revised 2026-08-13).

## 14. Open issues

- **OQ-007 — OPEN, narrowed 2026-08-13.** The ratio→dollar multiplication (× NetTA(b,0), constant) is confirmed operative in the project implementation via PID-TRD-1's calibration identity; the multiplicand's physical rows and the flat-balance reading remain [INT] pending elicitation and compare. Source-side absence unchanged.
- **OQ-009 — RESOLVED FOR PROJECT IMPLEMENTATION (2026-08-13, via PID-TRD-1).** The Fed's non-disclosure of α_b remains the [FACT]; both regression models now carry project calibrations (PID-OB-5; PID-TRD-1).
- **OQ-023 — OPEN, extended 2026-08-13.** FRB path lineage: hardcoded summary numbers; income-path scope implied-by-construction; per-path scope alignment TO BE CONFIRMED.
- **OQ-005 — OPEN.** Hedge-adjustment allocation (§13).
- **Elicitation items** (§11): physical trading rows; subtraction basis; compare targets.

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
| D-002 (superseded 2026-08-13), D-005, D-006, D-007, D-008 conventions; PID-TRD-1; PID-OB-5 (mirrored pattern) | `handbook/open-questions.md` decision log; user confirmation 2026-08-13 (§9, §11) |

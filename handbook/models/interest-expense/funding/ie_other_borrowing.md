# 12. Interest Expense on Other Borrowing (`ie_other_borrowing`)

> **STATUS: Proposed for the 2026 stress test — public-comment stage, NOT adopted.**
> Source: Section B.v.d(2) (PDF pp. 230–234; md sec-220–223); parameters in Section B.v.e, Table A9 (PDF p. 234; md sec-224). Model type per Table A6: **Regression** (PDF pp. 168–169; md sec-148).
> Integrity flags affecting this chapter: CA-4 (the "(a.) Variable Selection" heading, md line 4664, has no anchor — cite via sec-221); conversion artifacts — stray `|` characters in the A53 where-list (md lines 4645–4646, "at time| *t*;" and "credit spread;|"), not present in the PDF page image; candidate new source quirk — "the sum of other short-term, borrowing" (comma inside the term) is **in the PDF itself** (p. 231 where-list) — proposed as an SQ entry in `reviews/interest-expense/funding/ie_other_borrowing.review.md`.
> Chapter review state: **DRAFT** — independent source-grounding review recorded in `reviews/interest-expense/funding/ie_other_borrowing.review.md`. Approved content is never silently overwritten.
> Labels: **[FACT]** Fed source, cited · **[INT]** interpretation with stated basis · **[CODE]** coding consideration, non-normative · **[OQ]** open question by ID · **[PID]** PROJECT IMPLEMENTATION DECISION — user-confirmed, never attributable to the Federal Reserve · **[ALT]** alternative discussed by the Fed but not proposed. Citations: (PDF p. N; md sec-M).

## 1. Status and component scope

- [FACT] Exact Fed component name: **"Interest Expense on Other Borrowing"** — "interest expense paid on short-term borrowing, subordinated debt, and all other interest-bearing liabilities is modeled as a single quantity" (PDF p. 230; md sec-220).
- [FACT] Relevant balances: FR Y-14Q Schedule G Net Interest Income Worksheet line items **44C** (Other Short-Term Borrowing), **46** (Subordinated Notes Payable to Unconsolidated Trusts Issuing TruPS and TruPS Issued by Consolidated Special Purpose Entities), and **47** (Other Interest-Bearing Liabilities). "Parts of subordinated debt, however, may also be reported in line items 44C and 47 per reporting instructions" (PDF p. 230; md sec-220).
- [FACT] Rationale for the single-quantity design: "relative simplicity" and "lack of further granularity to cleanly separate subordinated debt from other borrowing from line items 44C and 47." The combined liabilities include subordinated debt, commercial paper, FHLB advances, and other mid- to long-term debt (PDF p. 230; md sec-220).
- [FACT] What this replaces: the current suite models subordinated debt with an **instrument-level structural model** (Section A.iv.m(3), Eq A28 — coupon-type-specific expense, premium/discount amortization, swap adjustment, refinancing of maturing debt; PDF pp. 153–159; md sec-136–139). The proposed model **absorbs** subordinated debt into this single OLS regression; the Board asks about exactly this trade-off in Questions A134 (current section) and A190 (this section). The current instrument-level methodology is contrast only — nothing from it enters this model.
- [FACT] Output enters PPNR through net interest income (Eq A1; PDF pp. 6–8; md sec-2); nine-quarter projection horizon (PDF p. 6; md sec-2).

## 2. Model summary

[FACT] The rate a firm pays on its other borrowing is the scenario 3-month Treasury yield plus a firm-specific credit spread; the spread is a linear function of the contemporaneous BBB corporate bond yield, the firm's commercial-paper and subordinated-debt shares of other borrowing, and a firm fixed effect (Eq A53; PDF pp. 230–231; md sec-221). In projection, the balance and both composition shares are frozen at the lift-off quarter, so only the two scenario yields move the expense path. [FACT — absence] Equation A53 contains **no autoregressive term, no rolling fixed effect, no seasonality term, and no firm grouping** — verified against the PDF page images.

[ALT] Variable selection (PDF pp. 231–232; md sec-221, heading affected by CA-4): the Board examined the 5-year and 10-year Treasury rates alongside the BBB yield; only the BBB coefficient was "consistently positive and statistically significant" across specifications; the instability of the others is attributed to high correlation among the three factors over the sample period. The 5y/10y factors are not in the proposed model.

## 3. Input and parameter register

### 3.1 Firm data inputs

| Input | Fed source | Dimensions | Units | Timing | Label |
|---|---|---|---|---|---|
| Total other-borrowing balance, B(b,0) (`ob_total_balance_launchpoint`) | FR Y-14Q Schedule G items **44C + 46 + 47** | b | USD | Launch-point (PQ0) value, held constant over the horizon | [FACT] items and constancy (PDF pp. 230–231; md sec-220–221) |
| Commercial-paper balance (`ob_cp_balance`) | FR Y-9C **BHCK2309** | b | USD | Launch-point value for the frozen share | [FACT] MDRM (PDF p. 232; md sec-221); see share-form note below |
| Subordinated-debt balance (`ob_subdebt_balance`) | FR Y-9C **BHDM4062 + BHDMC699** | b | USD | Launch-point value for the frozen share | [FACT] MDRM (PDF p. 232; md sec-221) |
| Commercial-paper share, CP(b,0) (`ob_cp_share_launchpoint`) | "balance of commercial paper divided by the total balance of other borrowing" | b | Share ∈ [0,1] | Frozen at PQ0 | [FACT] definition (PDF p. 231; md sec-221) |
| Subordinated-debt share, Subdebt(b,0) (`ob_subdebt_share_launchpoint`) | "balance of subordinated debt divided by the total balance of other borrowing" | b | Share ∈ [0,1] | Frozen at PQ0 | [FACT] definition (PDF p. 231; md sec-221) |

**Share-form note [INT → OQ-OB-A]:** the share numerators are stated as FR Y-9C items (in the estimation-context Variable Selection discussion) while B(b,0) is a Schedule G sum. Whether the projection-side share denominator is the Schedule G total, a Y-9C equivalent, or the same mixed ratio is **not stated**. No additional MDRM mapping is invented; the mixed form is recorded as the literal reading.

### 3.2 Scenario inputs

| Scenario variable | Enters via | Frequency | Units | Label |
|---|---|---|---|---|
| 3-month Treasury yield, Treasury3m(q) (`usd_3m_treasury`) | Base of the rate in A53(1), **coefficient of one by construction** — it is not an estimated coefficient (Table A9's A53(2) row has an empty 3M-Treasury cell) | Quarterly, q = 1…9 (PQ0 value needed only for the α_b backsolve, §9) | Annualized rate [D-004] | [FACT] (PDF pp. 230, 234; md sec-221, sec-224) |
| BBB corporate bond yield, BBB(q) (`bbb_corporate_yield`) | Sole macro driver of the credit spread in A53(2), ×β1 | Quarterly, q = 1…9 | Annualized rate [D-004] | [FACT] (PDF pp. 230–231; md sec-221). MEV column name unconfirmed — working assumption per the PID-5 workbook pattern, flagged, not a PID |

### 3.3 Parameters

| Parameter | Supplied or estimated | Value | Statistical significance (kept separate) | Label |
|---|---|---|---|---|
| β1 on BBB yield (`beta_bbb`) | Supplied — Board OLS estimate | **0.254** | ** (5% level) | [FACT] Table A9 (PDF p. 234; md sec-224) |
| β2 on CP share (`beta_cp`) | Supplied — Board OLS estimate | **−0.036** | *** (1% level) | [FACT] Table A9. Sign rationale: shorter duration, usually highly rated — the source calls this coefficient "economically significant" (PDF pp. 232, 234) |
| β3 on subdebt share (`beta_subdebt`) | Supplied — Board OLS estimate | **0.066** | ** (5% level) | [FACT] Table A9. Sign rationale: subordinated debt is more expensive — "positive and statistically significant" (PDF pp. 232, 234) |
| Firm fixed effect, α_b (`ob_firm_fixed_effect`) | Estimated by the Board, **NOT disclosed** — "Estimated coefficients for firm fixed-effects are not included in the table" | UNKNOWN from the source | Table A9 marks only "Yes" | [FACT] (PDF p. 234; md sec-224); project sourcing per §9 |

Table A9 note, verbatim: "Statistical significance levels of 1%, 5%, and 10% are indicated as ***, **, and *, respectively." The 0.278*** in the same table belongs to Equation A52 (trading NII, model #11), not to this model.

## 4. Equations

**Equation A53** — Interest Expense on Other Borrowing Regression Model [FACT] (PDF p. 230; md sec-221; verified against the page image):

**A53(1):**

$$Expense(b,t) = R(b,t) \times B(b,t) = \left(Treasury3m(t) + \delta(b,t)\right) \times B(b,t)$$

**A53(2):**

$$\delta(b,t) = \beta_1 BBB(t) + \beta_2\, Commercial\ Paper(b,t) + \beta_3\, Subdebt(b,t) + \alpha_b + \varepsilon(b,t)$$

*where* (condensed from the verbatim where-list, PDF p. 231): Expense(b,t) is the expense on Other Borrowing for firm b at time t; B(b,t) is the total balance of other borrowing, "the sum of other short-term, borrowing, subordinated debt, and other interest-bearing liabilities" (comma quirk in the PDF itself — candidate SQ); R(b,t) is the rate paid; Treasury3m(t) is the 3-month Treasury rate; δ(b,t) is the firm-specific credit spread; BBB(t) is the BBB corporate bond yield; Commercial Paper(b,t) and Subdebt(b,t) are the shares defined in §3.1; α_b is the firm fixed effect; ε(b,t) is the regression error term.

## 5. Estimation versus projection

| | Estimation | Projection |
|---|---|---|
| Sample / horizon | [FACT] Unbalanced panel of **all FR Y-14Q reporters, 2020:Q2–2021:Q4** — deliberately restricted "to a period where the interest rates are low" so sensitivities are "more precisely calibrated" (PDF p. 231) | Nine projection quarters q = 1…9 from PQ0 |
| Method | [FACT] "The coefficients in the regression specified in equation A53(2) are estimated using **ordinary least squares**" (PDF p. 231). [CODE] Do **not** apply the WLS convention used by other PPNR panel regressions — OLS is source-stated here | No estimation; supplied coefficients applied |
| Time-varying regressors | BBB(t), Treasury3m(t), shares(b,t) all vary | Only Treasury3m(q) and BBB(q) vary; shares frozen at (b,0) |
| Error term | ε(b,t) present in A53(2) | [FACT] Absent from the projection form of δ(b,q) (PDF p. 231) |

[FACT] Projection equations (PDF p. 231; md sec-221; lift-off quarter denoted q = 0):

$$Expense(b,q) = \left(Treasury3m(q) + \delta(b,q)\right) \times B(b,0)$$

$$\delta(b,q) = \beta_1 BBB(q) + \beta_2\, Commercial\ Paper(b,0) + \beta_3\, Subdebt(b,0) + \alpha_b$$

## 6. Timing and flat-composition rules

Dimensions: rate, spread, and expense are b × scenario × q; all firm inputs are b-dimensional PQ0 snapshots.

| Quantity | Launch point (PQ0) | Projection quarters (q ≥ 1) | Label |
|---|---|---|---|
| B(b,0) = 44C + 46 + 47 | Measured once | Held constant — B(b,0) in every quarter | [FACT] (PDF p. 231) |
| CP(b,0), Subdebt(b,0) | Measured once | Frozen — "portfolio composition that is held constant at the lift-off quarter" | [FACT] (PDF p. 231) |
| α_b | Fixed per firm (backsolved at PQ0 per §9) | Constant | [FACT] fixed; [PID] sourcing |
| Treasury3m(q), BBB(q) | PQ0 values used only in the §9 backsolve | Contemporaneous scenario values | [FACT] |
| δ(b,q), R(b,q), Expense(b,q) | — | Computed each q; no dependence on q−1 | [FACT — absence of any lag] |

Constancy register: **constant** — balance, both composition shares, α_b, β1–β3; **varying** — Treasury3m, BBB, credit spread, rate, expense.

## 7. Calculation workflow

1. **Launch-point balance.** B(b,0) = Schedule G items 44C + 46 + 47. Validate presence of all three items and B(b,0) > 0 (§11); no fallback invented [CODE].
2. **Launch-point composition.** `ob_cp_share_launchpoint` = BHCK2309 / B(b,0); `ob_subdebt_share_launchpoint` = (BHDM4062 + BHDMC699) / B(b,0) [FACT numerators and ratio definition; INT that the projection-side denominator is the Schedule G sum — OQ-OB-A]. Validate shares ∈ [0,1] and sum ≤ 1 (§11).
3. **Fixed effect.** Obtain α_b via the §9 backsolve [PID-OB-1]; validate presence per firm.
4. **Coefficients.** Load β1 = 0.254, β2 = −0.036, β3 = 0.066; store the significance stars as metadata, never in the numeric path (§3.3).
5. **Scenario preparation.** Align `usd_3m_treasury` and `bbb_corporate_yield` to q = 1…9 (plus PQ0 for the backsolve); normalize percent-vs-decimal scale identically for both series and the firm-side rate used in §9 [CODE].
6. **Credit spread, each q.** δ(b,q) = β1·BBB(q) + β2·CP(b,0) + β3·Subdebt(b,0) + α_b.
7. **Annualized rate, each q.** R(b,q) = Treasury3m(q) + δ(b,q). Coding restatement: `ob_annualized_rate[b,q] = usd_3m_treasury[q] + ob_credit_spread[b,q]`. No floor, cap, or non-negativity constraint exists [FACT — absence].
8. **Quarterly expense.** Per §8: `ob_interest_expense[b,q] = ob_total_balance_launchpoint[b] * ob_annualized_rate[b,q] / 4`.
9. **Hedge hook.** Expose the expense path for the cross-cutting v.c adjustment (§12); no hedge computation inside this model.

## 8. Quarterly expense conversion

- [FACT] Eq A53(1) is a rate × balance product; the source states **no annual→quarterly conversion** for this component ([FACT] absence, preserved — OQ-006 lists Eq A53(1) among the components whose conversion is unstated).
- [PID — decision D-004] All rates in A53 are treated as annualized; QuarterlyExpense(b,q) = B(b,0) × R(b,q) / 4, the ÷4 applied **only** at this final annualized-rate → quarterly-dollar step (simple nominal quarterization, not compounding); never attributed to the Fed. Rates stay annualized everywhere else, including the §9 backsolve. Output: `ob_interest_expense`, b × scenario × q, USD per quarter.

## 9. Firm fixed-effect treatment

- [FACT] α_b is estimated by the Board but not published (Table A9: firm fixed-effects "Yes", values excluded; PDF p. 234). The Fed's stated role for α_b: the mix of other borrowing "as well as interest rate risk hedging intensity" varies across firms beyond what the composition shares capture, and the fixed effects absorb this heterogeneity (PDF pp. 232–233; md sec-221).
- **[PID — D-002 + PID-OB-1, user-confirmed 2026-07-17] PROJECT IMPLEMENTATION DECISION — USER CONFIRMED.** α_b is backsolved from launch-point actuals via the projection equations inverted at PQ0:

  $$\alpha_b = R_{actual}(b,0) - Treasury3m(0) - \beta_1 BBB(0) - \beta_2\, CP(b,0) - \beta_3\, Subdebt(b,0)$$

  where R_actual(b,0) is the firm's observed annualized rate on other borrowing at the launch point. This is the handbook's working method (D-002) with the identity confirmed for this component (PID-OB-1); it is never attributable to the Federal Reserve.
- **Unresolved mechanics [OQ-009, still open]:** (a) whether R_actual(b,0) is a single-quarter PQ0 observation or an average over several quarters; (b) the physical source of the launch-point actual expense/rate on other borrowing (no Schedule G expense item is stated for this component and none is guessed); (c) treatment if PQ0 rates sit outside the low-rate regime of the 2020:Q2–2021:Q4 estimation window. The YAML spec marks these as UNRESOLVED; the model is implementable only once they are fixed in the approved environment.

## 10. Fed-stated assumptions and limitations

All [FACT] (PDF p. 233; md sec-222), restated faithfully:

1. **Composition coverage.** The model "does not fully capture the composition of each firm's other borrowing beyond short-term commercial paper and subordinated debt" — compositional details could affect both the level and the sensitivity of the rate; firms with a higher share of floating-rate debt would have higher rate sensitivity; fully collateralized debt would be expected to carry a lower rate.
2. **Duration and maturity.** The approach "does not account for the existing duration and maturity structure of various portions of each firm's liabilities balances."
3. **Low-rate-window stability.** Estimation over a low-rate period assumes the composition of other borrowing, the impact of interest-rate-risk hedges, and the sensitivity to credit conditions are stable across low-rate periods — which "may conflict with the observation that the firms may adjust their borrowing sources and hedging strategies over time," depending on alternative funding availability (such as deposits) and macro/credit conditions.

Board questions on this component: A189 (overall approach), A190 (modeling subdebt jointly vs. separately), A191 (other composition approaches) (PDF pp. 233–234; md sec-223).

## 11. Validation requirements ([CODE] — non-normative; no invented fallbacks, failures surface)

- **Input presence:** Schedule G items 44C, 46, 47 all present per firm; BHCK2309, BHDM4062, BHDMC699 present; α_b present per firm (missing α_b blocks the firm, never defaults to zero).
- **Balance sanity:** B(b,0) > 0 — zero or negative totals fail (zero also breaks the share denominators).
- **Shares:** `ob_cp_share_launchpoint` and `ob_subdebt_share_launchpoint` each ∈ [0,1]; their **sum ≤ 1**; violations surface (possible under the mixed Y-9C/Schedule G form — OQ-OB-A), never clipped.
- **Scenario paths:** `usd_3m_treasury` and `bbb_corporate_yield` complete for q = 1…9 (plus PQ0 for the backsolve) — full nine-quarter alignment per scenario, no gaps.
- **Rate scale:** percent-vs-decimal never assumed; metadata-driven and identical across both MEV series, the coefficients' implied scale, and R_actual(b,0) in the backsolve.
- **Parameter fidelity:** configured β values equal Table A9 exactly (0.254, −0.036, 0.066) — verify against the PDF page, not retyped copies; significance metadata (**, ***, **) stored separately and never used numerically.
- **Edge monitors:** negative R(b,q) is legal (no floor exists) — log, never clamp; monitor |α_b| magnitudes as a backsolve sanity screen (large values may indicate scale mismatch).

## 12. Hedge implications

- [FACT] The Fed's fixed-effect rationale explicitly names "interest rate risk hedging intensity" as cross-firm variation absorbed by α_b (PDF pp. 232–233) — hedge behavior enters this model only through the constant fixed effect, and assumption 3 (§10) concedes hedging strategies may change over time.
- [FACT — absence] v.d(2) contains no hedge term. The cross-cutting v.c adjustment (Eqs A49–A51, contingent on the proposed FR Y-14Q B.2/B.3 collection; PDF pp. 220–223; md sec-210–212) may later adjust this component; allocation across components is unresolved [OQ-005]. This model exposes its expense path and computes no hedge term. [CODE] If v.c is ever applied here, note the double-counting risk against the hedge intensity already embedded in a backsolved α_b.

## 13. Remaining implementation questions

- **OQ-009 — OPEN (narrowed).** Backsolve identity confirmed (PID-OB-1, §9); still open: actuals quarter(s), physical source of R_actual(b,0), low-rate-regime mismatch treatment.
- **OQ-005 — OPEN.** Hedge-adjustment allocation (§12).
- **OQ-006 — RESOLVED FOR PROJECT IMPLEMENTATION (D-004).** ÷4 convention applied in §8; source-side absence preserved.
- **Proposed OQ-OB-A (review file; number assigned at integration).** Share-denominator physical form: Y-9C numerators over a Schedule G total is the literal mixed reading; projection-side source form unstated.
- **Flagged working assumption (not a PID):** MEV column names for the 3-month Treasury and BBB corporate bond yield per the PID-5 workbook pattern.

## 14. Key source references

| Claim | (PDF p.; md anchor) |
|---|---|
| Component name; single-quantity scope; items 44C/46/47; subdebt bleed into 44C/47; rationale; FHLB/CP examples | (PDF p. 230; md sec-220) |
| Eq A53(1)/(2) as displayed | (PDF p. 230; md sec-221) |
| Where-list (incl. share definitions and the "other short-term, borrowing" PDF quirk); OLS; unbalanced panel 2020:Q2–2021:Q4; low-rate rationale; projection equations with (b,0) freezing | (PDF p. 231; md sec-221) |
| Variable selection (5y/10y/BBB); FR Y-9C MDRMs BHDM4062, BHDMC699, BHCK2309; coefficient sign rationale | (PDF p. 232; md sec-221; CA-4) |
| Fixed-effect rationale (mix + hedging intensity) | (PDF pp. 232–233; md sec-221) |
| Assumptions and limitations 1–3 | (PDF p. 233; md sec-222) |
| Questions A189–A191 | (PDF pp. 233–234; md sec-223) |
| Table A9 values and significance note; fixed effects not included; "based on data submitted on forms FR Y-14Q and FR Y-9C" | (PDF p. 234; md sec-224) |
| Table A6 regression classification | (PDF pp. 168–169; md sec-148) |
| Current subordinated-debt structural model (comparison only) — Eq A28, swap adjustment, Question A134 | (PDF pp. 153–159; md sec-136–139) |
| Hedge adjustment (v.c) | (PDF pp. 220–223; md sec-210–212) |
| Nine-quarter horizon; PPNR identity (Eq A1) | (PDF pp. 6–8; md sec-2) |
| D-002, D-004, D-005 conventions; PID-OB-1 confirmation | `handbook/open-questions.md` decision log; user confirmation 2026-07-17 (§9) |

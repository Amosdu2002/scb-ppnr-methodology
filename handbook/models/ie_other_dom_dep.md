# 8. Interest Expense on Other Domestic Deposits (`ie_other_dom_dep`)

> **STATUS: Proposed for the 2026 stress test — public-comment stage, NOT adopted.**
> Source: Section B.v.a(8) (PDF pp. 211–215; md sec-197–200). Model type per Table A6: **Structural** (PDF pp. 168–169; md sec-148).
> Integrity flags affecting this chapter: SQ-1 (Table A7 Down-row labels are internal parameter names), SQ-2 (Table A7 caption cites "(Equations A46)"), SQ-9 (Eq A45 where-list "indicats"), SQ-12 (two consecutive "A third assumption" labels, PDF p. 214); candidate new source quirk — truncated spread-estimation sentence (PDF p. 212) — proposed as SQ-15 in `ie_other_dom_dep.review.md`. December 2025 revision item 5 applies to p. 214 ("end of quarter" → "average"; "FR Y-9C" → "FR Y-14Q"; subsection (a.) → (b); "contradicts" → "abstracts from"; PDF pp. 4–5; md sec-0). Conversion artifacts in v.a(8): none.
> Chapter review state: **DRAFT** — independent source-grounding review recorded in `handbook/models/ie_other_dom_dep.review.md`. Approved content is never silently overwritten.
> Labels: **[FACT]** Fed source, cited · **[INT]** interpretation with stated basis · **[CODE]** coding consideration, non-normative · **[OQ]** open question by ID · **[PID]** PROJECT IMPLEMENTATION DECISION — user-confirmed, never attributable to the Federal Reserve · **[ALT]** alternative discussed by the Fed but not proposed. Citations: (PDF p. N; md sec-M).

## 1. Status and purpose

- [FACT] Exact Fed component name: **"Interest Expense on Other Domestic Deposits"** — one of the 10 components with proposed structural models (PDF pp. 172, 211; md sec-149, sec-197); Table A6 lists "Other domestic deposits" under structural interest-expense models (PDF pp. 168–169; md sec-148).
- [FACT] Scope: domestic non-time deposits via three FR Y-14Q subcomponents — **money market accounts (MMA), savings accounts, and transaction accounts** ("negotiable order of withdrawal [NOW], automatic transfer service [ATS], and other accounts") (PDF p. 211; md sec-197).
- [FACT] Boundaries: domestic time deposits belong to `ie_dom_time_dep` (PDF pp. 209–211; md sec-193); foreign deposits (time and non-time) belong to `ie_foreign_dep`, which reuses this model "identical … with the exception" of line items (PDF p. 215; md sec-201). This component absorbs nothing from other components.
- [FACT] Output enters PPNR through net interest income (Equation A1; PDF pp. 6–8; md sec-2); nine-quarter projection horizon (PDF p. 6; md sec-2).

## 2. Model summary

[FACT] Each subcomponent rate is projected separately under a **two-regime switch** on the scenario 3-month Treasury yield, then aggregated balance-weighted (Eq A47); the aggregate rate times the average balance produces the expense (PDF pp. 211–214; md sec-197–199):

| Regime | Trigger in projection quarter t | Rate rule | Label |
|---|---|---|---|
| Effective lower bound (ELB) | Treasury3m(t) **below** 25 bp | Rate(i,b,t) = floor(i,b,t) = Treasury3m(t) + Spread(i,b) — **Eq A45** (PDF p. 212) | [FACT] |
| Non-ELB | Treasury3m(t) **above** 25 bp | Rate(i,b,t) = max(Rate(i,b,t−1) + δ(i,t), assumed_floor(i,b)) — **Eq A46** (PDF p. 213) | [FACT] |

- [OQ → OQ-013] Treasury3m(t) exactly = 25 bp is assigned to neither regime by the source.
- [FACT] Intuition, verbatim structure: in non-ELB quarters the rate moves by beta-scaled 3M-Treasury changes with a floor; in ELB quarters the rate is pinned to the 3M Treasury plus a firm-specific ELB spread (PDF pp. 211–212; md sec-197).
- [ALT] None — v.a(8) discusses no alternative specification (contrast the Call Report alternative in v.a(7)).

## 3. Inputs

### 3.1 Firm data inputs

| Input | Fed source (schedule, line item) | Dimensions | Units | Timing (lift-off definition) | Label |
|---|---|---|---|---|---|
| Subcomponent rates, Rate(i,b,0) (`odd_rate_liftoff`) | FR Y-14Q Schedule G items **42B** (MMA), **42C** (Savings), **42D** (Transaction) | b × i | Annualized rate [D-004]; scale normalization §10 | Retrieved at lift-off; seed the A46 recursion at t = 1 [INT — seed role; see §4] | [FACT] items (PDF p. 213; md sec-198) |
| Firm-reported betas (`odd_firm_beta_up/down`) | Schedule G items **79A/79B** (MMA up/down), **80A/80B** (Savings), **81A/81B** (Transaction) | b × i × {up,down} | Dimensionless | At lift-off; enter only the Fed's cross-firm **median** — individual firm betas do not drive projections (Table A7 supplies the medians) | [FACT] (PDF pp. 213, 219; md sec-198, sec-209) |
| Subcomponent balances, Balance(i,b,t) (`odd_subcomponent_balance`) | "the balance reported in the Y-14Q corresponding to the rate i" — **line items not named** ([FACT] absence) | b × i | USD | Lift-off values, held constant [INT — general flat-balance convention; A47 carries a t subscript] | [FACT] role (PDF p. 213; md sec-198); mapping UNKNOWN (proposed OQ-016) |
| Average balance on other domestic deposits (`odd_total_average_balance`) | "the average balance on other domestic deposits as reported in the FR Y-14Q" — **item not named** ([FACT] absence); "average" per December 2025 revision item 5 | b | USD | Lift-off average balance, held flat [INT — flat-balance convention] | [FACT] role (PDF p. 214; md sec-198; revision PDF pp. 4–5); mapping UNKNOWN (proposed OQ-016) |
| Historical subcomponent rates, 2020:Q2–2021:Q4 (`odd_rate_history_elb`) | Same rate items over the ELB window [INT — series identity implied, not stated] | b × i × history | Annualized rate | Fixed historical window for Spread(i,b) estimation | [FACT] window (PDF p. 212; md sec-198) |

### 3.2 Scenario inputs

| Scenario variable | Enters via | Frequency | Units | Label |
|---|---|---|---|---|
| 3-month Treasury yield, Treasury3m(t) (`usd_3m_treasury`) | (i) regime trigger vs. 25 bp; (ii) ELB rate level (A45); (iii) quarterly change ΔTreasury3m(t) (A46); (iv) First_ELB_Treasury3m from the scenario path | Quarterly, t = 1…9 (plus jump-off value for ΔTreasury3m(1) [INT — see §4]) | Annualized rate [D-004] | [FACT] (PDF pp. 211–213; md sec-197–198). Sourcing: MEV workbook per the PID-5 pattern; exact column name unconfirmed — working assumption "USD 3M Treasury", flagged, not a PID |

### 3.3 Parameters

| Parameter | Supplied or estimated | Source | Value(s) or UNKNOWN | Constant over horizon? | Label |
|---|---|---|---|---|---|
| β_up(i), β_down(i) (`beta_up`, `beta_down`) | **Supplied** — median of firm-reported betas at lift-off, calculated by the Board from FR Y-14Q data | **Table A7** "Median Betas for Proposed Deposit Models (Equations A46)" | MMA 0.620 / 0.645; Savings 0.310 / 0.335; Other (transaction) 0.465 / 0.490 (up / down) | **Yes** — "constant betas" | [FACT] (PDF pp. 213, 219; md sec-198, sec-209); SQ-1/SQ-2 recorded, never corrected |
| Spread(i,b) (`elb_spread`) | **Estimated from firm data** — "the average distance between the deposit rate paid by the firm during the most recent effective lower-bound period" (sentence truncated in the PDF; [INT] intended: distance **to the 3-month Treasury yield**, per the A45 where-list) | ELB window **2020:Q2–2021:Q4** | Firm- and deposit-type-specific; values from data | Yes [INT — no re-estimation is described] | [FACT] window and role (PDF p. 212; md sec-198); sign/averaging mechanics UNKNOWN (proposed OQ-017) |
| First_ELB_Treasury3m (`first_elb_treasury3m`) | Derived per scenario | "the minimum between 25 basis points and the first observation of the 3-month Treasury yield which goes below the 25 basis points in the scenario (if available)" | min(25 bp, first sub-25bp scenario observation); [INT] = 25 bp when no observation goes below | Yes, per scenario | [FACT] (PDF p. 213; md sec-198) |
| Estimated regression coefficients / firm fixed effects | — | — | **None exist** — structural models "avoid statistical estimation"; D-002 backsolving does not apply | — | [FACT] (PDF pp. 172–173; md sec-149) |

## 4. Timing and dimensions

Dimensions: subcomponent paths b × i × t with i ∈ {MMA, Savings, Transaction}; aggregate rate and expense b × t; t = 1…9 plus seed values at the jump-off quarter q0.

| Quantity | Lift-off (q0) role | Projection-quarter (t ≥ 1) role | Label |
|---|---|---|---|
| Rate(i,b,0) — items 42B/42C/42D | Measured once at lift-off | Rate(i,b,t−1) at t = 1 in A46 [INT — the source retrieves these rates but never states the t = 1 seed explicitly; proposed OQ-018] | [FACT] retrieval; [INT] seed |
| Spread(i,b) | Estimated once from the 2020:Q2–2021:Q4 window (historical, before q0) | Constant in A45 and in assumed_floor | [FACT] |
| β_up(i)/β_down(i) | Table A7 constants (Board-computed at lift-off) | Constant in δ(i,t) | [FACT] |
| Balance(i,b,·) and total average balance | Measured at lift-off | Held constant [INT — flat-balance convention; not restated in v.a(8)] | [FACT] role; [INT] constancy |
| Treasury3m(t) | Jump-off value needed for ΔTreasury3m(1) [INT] | Contemporaneous scenario value; regime trigger each t | [FACT] path; [INT] t=1 change |
| Rate(i,b,t), Rate(b,t), Expense(b,t) | — | Computed each t; A46 depends on t−1 (previous modeled rate, whichever regime produced it [INT]) | [FACT] |

Constancy register: **constant** — betas, spreads, assumed_floor, First_ELB_Treasury3m (per scenario), all balances [INT for balances]; **varying** — Treasury3m(t), regime classification, subcomponent rates, aggregate rate, expense.

## 5. Equations and variable definitions

**Equation A45** — Interest Expense on Other Domestic Deposits Rate Projection, Effective Lower Bound Period [FACT] (PDF p. 212; md sec-198; verified against the page image):

$$Rate_{i,b,t} = floor_{i,b,t}$$

*where* (condensed from the verbatim where-list): i ∈ (MMA, Savings, Transaction); b the firm; t the quarter (source: "indicats", SQ-9); floor(i,b,t) = Treasury3m(t) + Spread(i,b); Spread(i,b) is "the firm- and deposit-type-specific spread to the 3-month Treasury yield during an effective lower bound period"; Treasury3m(t) is the 3-month Treasury yield.

**Equation A46** — Non-Effective Lower Bound Period (Treasury3m(t) > 25 bp) [FACT] (PDF p. 213; md sec-198; verified):

$$Rate_{i,b,t} = \max\left(Rate_{i,b,t-1} + \delta_{i,t},\ assumed\_floor_{i,b}\right)$$

*where*: δ(i,t) = max(ΔTreasury3m(t), 0) · β_up(i) + min(ΔTreasury3m(t), 0) · β_down(i); ΔTreasury3m(t) is the change in the 3-month Treasury yield; β_up(i), β_down(i) are the constant betas for the up and down rate respectively; assumed_floor(i,b) = First_ELB_Treasury3m + Spread(i,b); First_ELB_Treasury3m as defined in §3.3. Note δ carries no b subscript — it is identical across firms [FACT, from the where-list subscripts].

**Equation A47** — Interest Rate on Other Domestic Deposits Aggregation [FACT] (PDF p. 213; md sec-198; verified):

$$Rate_{b,t} = \left(\sum_i Rate_{i,b,t} \cdot Balance_{i,b,t}\right) / \left(\sum_i Balance_{i,b,t}\right)$$

*where*: Balance(i,b,t) is "the balance reported in the Y-14Q corresponding to the rate i for firm b at time t".

[FACT] Expense sentence: "The aggregate interest rate on other domestic deposits is then multiplied by the average balance on other domestic deposits as reported in the FR Y-14Q to produce the interest expense on other domestic deposits." (PDF p. 214; md sec-198.)

## 6. Calculation workflow

1. **Lift-off extraction (q0).** Read rates 42B/42C/42D → Rate(i,b,0); read subcomponent balances and the total average balance (mappings UNKNOWN — proposed OQ-016); load Table A7 betas. Validate per §10; no fallback treatment is invented [CODE].
2. **Spread estimation.** Spread(i,b) = average distance of the firm's subcomponent deposit rate to the 3-month Treasury yield over 2020:Q2–2021:Q4 [FACT window; INT endpoint per truncated sentence; sign convention [INT]: signed difference rate − Treasury3m — proposed OQ-017].
3. **Scenario preparation.** Align Treasury3m to q0…PQ9; ΔTreasury3m(t) = Treasury3m(t) − Treasury3m(t−1), with t = 1 using the jump-off value [INT — proposed OQ-018]; First_ELB_Treasury3m = min(25 bp, first sub-25bp observation in the scenario path, else 25 bp [INT on "(if available)"]).
4. **Assumed floor.** assumed_floor(i,b) = First_ELB_Treasury3m + Spread(i,b) [FACT].
5. **Regime classification, each t.** ELB if Treasury3m(t) < 25 bp; non-ELB if > 25 bp; = 25 bp unassigned [OQ-013 — pick one branch and document it, [CODE]].
6. **Subcomponent rate paths, each t in order.** ELB quarter → Eq A45; non-ELB quarter → Eq A46 with Rate(i,b,t−1) = the previous quarter's modeled rate whichever regime produced it (Rate(i,b,0) at t = 1) [INT]. Coding restatement: `odd_rate[i,t] = t3m[t] + elb_spread[i]` (ELB) or `max(odd_rate[i,t-1] + delta[i,t], assumed_floor[i])` (non-ELB). No cap or non-negativity constraint exists; in ELB quarters the rate can sit below assumed_floor by construction [FACT — A45 has no max()].
7. **Aggregation.** Eq A47, balance-weighted with constant balances [INT constancy].
8. **Hedge hook.** Expose the expense path for the cross-cutting v.c adjustment (§11); no hedge computation inside this model [FACT absence; OQ-005].

**Intermediates register**

| Intermediate | Step | Dimensions | Units | Label |
|---|---|---|---|---|
| `elb_spread`, Spread(i,b) | 2 | b × i | Annualized rate spread | [FACT] role; [INT] mechanics |
| `first_elb_treasury3m` | 3 | scenario | Annualized rate | [FACT] |
| `assumed_floor` | 4 | b × i (× scenario) | Annualized rate | [FACT] |
| `delta`, δ(i,t) | 6 | i × t | Annualized rate change | [FACT] |
| `odd_rate`, Rate(i,b,t) | 6 | b × i × t (incl. seed) | Annualized rate | [FACT] |
| `odd_agg_rate`, Rate(b,t) | 7 | b × t | Annualized rate | [FACT] |

## 7. Output calculation

- [FACT] Expense = aggregate rate × average balance on other domestic deposits per FR Y-14Q (PDF p. 214; md sec-198). The source states **no annual→quarterly conversion** for this component ([FACT] absence — its explicit ÷4 / N/360 statements appear only in trading-NII, securities, and hedge contexts; PDF pp. 225, 191, 196, 201, 222).
- [PID — decision D-004] QuarterlyExpense(b,t) = AverageBalance(b) × Rate(b,t) / 4, the ÷4 applied **only** at this final annualized-rate → quarterly-dollar step (simple nominal quarterization, not compounding); never attributed to the Fed. Output: `odd_interest_expense`, b × scenario × t, USD per quarter.

## 8. Fed-stated assumptions and limitations

All [FACT] (PDF p. 214; md sec-199), restated faithfully:

1. **ELB at 25 bp.** The effective lower bound occurs when the 3-month Treasury yield falls below 25 basis points — "consistent with the lowest observed historical policy target range for the federal funds rate of 0–25 basis points"; the 3-month Treasury yield is "commonly used as the quarterly proxy for the risk-free rate."
2. **Non-ELB periods treated as normal periods.** "This abstracts from the relative distance of deposit rates to the effective lower bound where yield compression can occur." ("abstracts from" per December 2025 revision item 5.)
3. **Rate floor ("A third assumption").** During non-ELB periods a firm's rate floor is the first sub-25bp scenario observation of the 3-month Treasury yield, or 25 basis points — "eliminates the possibility that the rate on other domestic deposits will go below the assumed floor during the non-effective lower-bound period."
4. **Constant median beta (also labeled "A third assumption" — SQ-12, preserved verbatim, never corrected).** A constant beta, the median of firm-reported betas, applies to all firms: "By construction, this eliminates the possibility of considering market power in the pricing of non-time deposits"; it also "abstracts from time variation in betas" noted in academic literature and observed in firms' reporting.

## 9. User-confirmed implementation mappings

- [PID — D-004, project-wide, user-confirmed 2026-07-17] Annualized-rate convention: all rates annualized; ÷4 only at the final quarterly-dollar step (§7).
- **No component-specific mapping is confirmed for this model.** The PID-1 balance mapping (item 34E) belongs to `ie_dom_time_dep` only. **Flagged working hypotheses — NOT confirmed, not used as facts** (per the project's flagged-working-assumption preference): (a) subcomponent balances follow the 42X↔34X pattern (MMA/Savings/Transaction balances = items 34B/34C/34D by analogy with 42E↔34E); (b) total average balance = Σ of subcomponent balances (which would make the A47 denominator and the §7 multiplicand the same number); (c) MEV column name "USD 3M Treasury" per the PID-5 workbook pattern. All three await user confirmation — listed in the review file for the integration session (proposed OQ-016).

## 10. Validation requirements ([CODE] — non-normative)

- **Parameter fidelity:** configured betas must equal Table A7 exactly (0.620/0.645, 0.310/0.335, 0.465/0.490); verify against the PDF, not retyped copies.
- **Input presence (no invented fallbacks; failures surface):** rates 42B/42C/42D; subcomponent balances; total average balance; 2020:Q2–2021:Q4 rate history for spreads (firms without ELB-window history: treatment UNKNOWN — proposed OQ-017).
- **Rate-scale normalization:** percent vs. decimal never assumed; metadata-driven, identical for firm rates and the MEV series, before any regime logic (the 25 bp trigger must be expressed in the normalized scale).
- **Regime boundary:** document the chosen branch for Treasury3m(t) = 25 bp (OQ-013); unit-test both regimes and the ELB↔non-ELB transitions.
- **Weights:** Balance(i,b) ≥ 0 and ΣBalance > 0 before A47; if hypothesis (b) in §9 is confirmed, cross-check A47 denominator vs. the §7 balance.
- **Edge monitors:** ELB-quarter rates below assumed_floor are legal (A45 has no max); negative projected rates possible if Treasury3m + Spread < 0 — log, never clamp; δ identical across firms — assert no accidental b-dependence.

## 11. Dependencies and hedge interface

- [FACT] Upstream: no other proposed net-interest model's output enters; inputs are FR Y-14Q Schedule G data, the scenario 3-month Treasury path, and Table A7 (PDF pp. 211–214, 219).
- [FACT] Downstream by reference: `ie_foreign_dep` reuses this specification with items 43A/44B (rates), 35A/35B (balances), 83A/83B/84A/84B (betas) (PDF p. 215; md sec-201) — methodology reuse, not a data dependency.
- [FACT — absence] v.a(8) does not mention hedges. The cross-cutting v.c adjustment (Eqs A49–A51; qualified accounting hedges; contingent on the proposed FR Y-14Q B.2/B.3 collection; PDF pp. 220–223; md sec-210–212) may later adjust this component. Two data states: (i) current — no component-level hedge adjustment computable; (ii) proposed-collection — v.c becomes computable. Allocation across components unresolved [OQ-005]. This model exposes its expense path and computes no hedge term.

## 12. Open issues

- **OQ-005 — OPEN.** Hedge-adjustment allocation across components (§11).
- **OQ-006 — RESOLVED FOR PROJECT IMPLEMENTATION (D-004).** ÷4 convention applied in §7; the source-side absence is preserved.
- **OQ-013 — OPEN (minor).** Treasury3m = 25 bp boundary unassigned; branch choice is a documented [CODE] decision.
- **Proposed OQ-016 (filed in the review file, not yet in `open-questions.md`).** Balance line-item mappings: subcomponent balances and the total average balance are unnamed in the source; §9 hypotheses (a)/(b) need confirmation.
- **Proposed OQ-017 (review file).** Spread estimation mechanics: truncated source sentence (candidate SQ-15); sign convention (signed vs. absolute distance); averaging frequency; treatment of firms without 2020:Q2–2021:Q4 history.
- **Proposed OQ-018 (review file).** Seed timing: Rate(i,b,0) as the t = 1 lag and the jump-off Treasury3m in ΔTreasury3m(1) are [INT], not source-stated.

## 13. Key source references

| Claim | (PDF p.; md anchor) |
|---|---|
| Component name; subcomponents MMA/Savings/Transaction (NOW, ATS, other); two-regime design; 25 bp thresholds | (PDF p. 211; md sec-197) |
| Eq A45 + where-list; spread estimation sentence; ELB window 2020:Q2–2021:Q4 | (PDF p. 212; md sec-198) |
| Eq A46 + where-list; rate items 42B/42C/42D; beta items 79A–81B; median-at-lift-off rationale; Eq A47 | (PDF p. 213; md sec-198) |
| Expense = aggregate rate × average balance (FR Y-14Q); assumptions 1–4 (incl. SQ-12) | (PDF p. 214; md sec-198–199) — "average"/"FR Y-14Q"/"abstracts from" per revision item 5 (PDF pp. 4–5; md sec-0) |
| Question A178, verbatim: "The Board seeks comment on the proposed approach to model interest expense on other deposits, as compared to the Board's current panel regression model." | (PDF p. 215; md sec-200) |
| Table A7 (Board-calculated from FR Y-14Q); SQ-1/SQ-2 | (PDF p. 219; md sec-209) |
| Table A6 row; ten-component list; "avoid statistical estimation" | (PDF pp. 168–169, 172–173; md sec-148, sec-149) |
| Foreign-deposits reuse; boundary with `ie_dom_time_dep` | (PDF pp. 209–211, 215; md sec-193, sec-201) |
| Hedge adjustment (v.c) | (PDF pp. 220–223; md sec-210–212) |
| Nine-quarter horizon; PPNR identity (Eq A1) | (PDF pp. 6–8; md sec-2) |
| Current 2025 comparison model (panel regression, iv.i(2)) — context for Question A178 only | (PDF pp. 80–84; md sec-70) |
| D-004 convention; PID-5 pattern; flagged hypotheses | `handbook/open-questions.md` decision log; `ie_dom_time_dep.md` §12; §9 above |

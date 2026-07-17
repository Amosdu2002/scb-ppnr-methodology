# 9. Interest Expense on Foreign Deposits (`ie_foreign_dep`)

> **STATUS: Proposed for the 2026 stress test — public-comment stage, NOT adopted.**
> Source: Section B.v.a(9) (PDF pp. 215–216; md sec-201–204), which incorporates the v.a(8) framework — Equations A45–A47 — **by reference** (PDF pp. 211–214; md sec-197–199). Model type per Table A6: **Structural** (PDF pp. 168–169; md sec-148).
> Integrity flags: SQ-1/SQ-2 (Table A7 down-row labels and "(Equations A46)" caption, PDF p. 219); SQ-9 ("indicats", Eq A45), SQ-12 (two "third assumption"s, PDF p. 214), and SQ-15 (truncated spread-estimation sentence, PDF p. 212; filed 2026-07-17) in the referenced v.a(8) text. Conversion artifacts in v.a(9): none.
> Chapter review state: **REVIEWED** — independent PDF-grounding review passed 2026-07-17, source-faithful as drafted (`reviews/interest-expense/deposits/ie_foreign_dep.review.md`). Specification: `specifications/interest-expense/deposits/ie_foreign_dep.yaml`.
> Labels: **[FACT]** = FED FACT (cited); **[PID]** = PROJECT IMPLEMENTATION DECISION (user-confirmed, never attributable to the Fed); **[INT]** = INTERPRETATION (basis stated); **[CODE]** = CODING CONSIDERATION (non-normative); **[OQ]** = OPEN QUESTION (by ID); **[ALT]** = ALTERNATIVE DISCUSSED BUT NOT PROPOSED. Unknowns are written UNKNOWN.

## 1. Status and purpose

- [FACT] The Board "proposes an alternative model for interest expense on foreign deposits, which is very similar to the alternative model for other domestic deposits previously described" (PDF p. 215; md sec-201). One of the 10 proposed structural components; Table A6 lists "Foreign deposits" under structural interest-expense models (PDF pp. 168–169, 172; md sec-148–149).
- [FACT] "The data for foreign deposits is retrieved from the Y-14Q and the quantities are equivalent to those retrieved from the FR Y-9C. Aggregate foreign deposits have a smaller impact with respect to the larger categories of domestic time deposits and other domestic deposits." (PDF p. 215; md sec-201)
- [FACT] Boundary: domestic time deposits → `ie_dom_time_dep` (v.a(7)); domestic non-time (MMA/savings/transaction) → `ie_other_dom_dep` (v.a(8)). Foreign **time** deposits stay **inside this component** — they do not use the domestic-time WAL model (PDF pp. 209, 211, 215; md sec-193, sec-197, sec-202).

## 2. Model summary

- [FACT] Two-regime deposit-rate model, "identical to the proposed model for other domestic deposits detailed above with the exception" of the FR Y-14Q line items (PDF p. 215; md sec-202). Two subcomponents i ∈ {Foreign non-time, Foreign time} are modeled separately and aggregated balance-weighted; the aggregate rate times the average foreign-deposit balance gives the expense (by reference, PDF pp. 212–214; md sec-198).
- [FACT] Regimes per projection quarter: **ELB** when Treasury3m(t) < 25 bp → rate = Treasury3m + firm/subcomponent spread (Eq A45); **non-ELB** (Treasury3m > 25 bp) → rate = prior rate + beta-scaled Treasury3m change, floored (Eq A46). Betas are **median** firm-reported betas, supplied in Table A7 (PDF pp. 211–213, 219; md sec-197–198, sec-209).
- [FACT] No statistical estimation: structural models' "variability of projections … can be fully explained by reported balances … and the variation in the interest rate scenario paths" (PDF pp. 172–173, 218; md sec-149, sec-207). No firm fixed effects; D-002 does not apply.
- Output: quarterly dollar interest expense on foreign deposits per firm b, scenario, and projection quarter t = 1…9 [FACT component/horizon (PDF pp. 6–8; md sec-2); PID ÷4 dollar step, §7].

## 3. Inputs

### 3.1 Firm data inputs (FR Y-14Q, Schedule G)

| Input | Line item | Dimensions | Units | Timing | Label |
|---|---|---|---|---|---|
| Foreign deposits rate (non-time), Rate(nontime,b,0) (`foreign_nontime_rate_launchpoint`) | 43A ("foreign deposits") | b | Annualized rate [PID-6/D-004] | Launch point (PQ0); seeds the A46 recursion [INT-c] | [FACT] item (PDF p. 215; md sec-202); [INT] seed role |
| Foreign deposits–time rate, Rate(time,b,0) (`foreign_time_rate_launchpoint`) | 44B ("foreign deposits-time") | b | Annualized rate | Launch point (PQ0); seed [INT-c] | [FACT] item (PDF p. 215); [INT] seed role; quirk-candidate: 44B also names the repo *balance* item in v.a(10) (PDF p. 217) — see §12 |
| Foreign non-time balance, Balance(nontime,b) (`foreign_nontime_balance`) | 35A | b | USD | Launch point; held constant [INT-d] | [FACT] item (PDF p. 215) |
| Foreign time balance, Balance(time,b) (`foreign_time_balance`) | 35B | b | USD | Launch point; held constant [INT-d] | [FACT] item (PDF p. 215) |
| Historical subcomponent rates, 2020:Q2–2021:Q4 (`foreign_rate_history_elb`) | 43A / 44B history [INT] | b × i × 7 quarters | Annualized rate | Estimation window for Spread(i,b) | [FACT] window (PDF p. 212, by reference); [INT] same items historically |
| Firm-reported betas (`foreign_beta_reported`) | 83A, 83B, 84A, 84B | b × i × {up,down} | Fraction | Launch point; **feed the Table A7 medians only** — model uses medians | [FACT] items (PDF p. 215); item→(subcomponent, direction) mapping unstated [INT-b] |

### 3.2 Scenario inputs

| Variable | Enters via | Frequency | Units | Label |
|---|---|---|---|---|
| 3-month Treasury yield, Treasury3m(t) (`usd_3m_treasury`) | Regime test (25 bp); level in A45; change ΔTreasury3m in A46; First_ELB_Treasury3m for the assumed floor | Quarterly, t = 1…9 (plus PQ0 value for ΔTreasury3m at t = 1 [INT-f]) | Annualized rate | [FACT] (PDF pp. 211–213, 216); MEV column name per PID-5 pattern presumed "USD 3M Treasury" — exact name **UNCONFIRMED** [CODE] |

### 3.3 Parameters

| Parameter | Supplied or derived | Source | Value | Constant? | Label |
|---|---|---|---|---|---|
| β_up, β_down — Foreign: Non-time | Supplied | **Table A7** (PDF p. 219; md sec-209) | up **0.890** / down **0.790** | Yes | [FACT]; SQ-1/SQ-2 recorded, never corrected |
| β_up, β_down — Foreign: Time | Supplied | Table A7 | up **1.000** / down **1.000** | Yes | [FACT] |
| Spread(i,b) (`elb_spread`) | Derived from firm data — **values not published; UNKNOWN until computed** | "empirically estimated as the average distance between the deposit rate paid by the firm during the most recent effective lower-bound period" = 2020:Q2–2021:Q4 (PDF p. 212, by reference) | firm × subcomponent | Yes [INT — no re-estimation mechanism stated] | [FACT] method/window; [INT] the sentence omits "and the 3-month Treasury yield" — intent clear from Eq A45's Spread definition (quirk candidate, §12) |
| ELB threshold | Fixed | 25 basis points (PDF p. 211) | 0.25% | Yes | [FACT]; boundary case =25 bp unassigned [OQ-013] |

## 4. Timing and dimensions

| Quantity | Launch point (PQ0) role | Projection (t ≥ 1) role | Label |
|---|---|---|---|
| Rate(i,b,0) — items 43A/44B | Measured once | Seeds A46's Rate(i,b,t−1) at t = 1 [INT-c] | [FACT] items; [INT] seed |
| Balance(i,b) — items 35A/35B | Measured once | Constant A47 weights and expense balance every quarter [INT-d] | [FACT] items; [INT] constancy |
| Spread(i,b) | Computed once from the 2020:Q2–2021:Q4 window | Constant in A45 floor and A46 assumed_floor | [FACT] window; [INT] constancy |
| Betas (Table A7) | Supplied ("median … at lift-off", PDF p. 213) | Constant | [FACT] |
| Treasury3m(t) | PQ0 value used only for ΔTreasury3m at t = 1 [INT-f] | Contemporaneous each quarter; drives regime, level, change | [FACT] |
| Rate(i,b,t), Rate(b,t), Expense(b,t) | — | Computed each quarter; dimensions b × scenario × t | [FACT] form; [PID] ÷4 |

Dimensions: b = firm; i ∈ {nontime, time} (subcomponent dimension exists **before** aggregation only); t = 1…9. Horizon: nine quarters [FACT] (PDF p. 6; md sec-2).

## 5. Equations and variable definitions

All three equations verified against PDF page images (pp. 212–213) this session; stated for i ∈ (MMA, Savings, Transaction) and applied here with i ∈ (Foreign non-time, Foreign time) per the "identical … with the exception" clause (PDF p. 215) [FACT].

**Equation A45** — rate, effective-lower-bound period (Treasury3m < 25 bp) (PDF p. 212; md sec-198):

$$Rate_{i,b,t} = floor_{i,b,t} = Treasury3m_t + Spread_{i,b}$$

**Equation A46** — rate, non-ELB period (Treasury3m > 25 bp) (PDF p. 213; md sec-198):

$$Rate_{i,b,t} = \max\left(Rate_{i,b,t-1} + \delta_{i,t},\ assumed\_floor_{i,b}\right)$$

- δ(i,t) = max(ΔTreasury3m(t), 0) · β_up(i) + min(ΔTreasury3m(t), 0) · β_down(i)
- assumed_floor(i,b) = First_ELB_Treasury3m + Spread(i,b)
- First_ELB_Treasury3m = "the minimum between 25 basis points and the first observation of the 3-month Treasury yield which goes below the 25 basis points in the scenario (if available)" [FACT, verbatim]

**Equation A47** — aggregation (PDF p. 213; md sec-198):

$$Rate_{b,t} = \left(\sum_i Rate_{i,b,t} \cdot Balance_{i,b,t}\right) / \left(\sum_i Balance_{i,b,t}\right)$$

[INT-d] Balance(i,b,t) carries a t subscript in the source; under the constant-balance convention (PDF pp. 169–170, 218; md sec-148, sec-206) Balance(i,b,t) = Balance(i,b,PQ0) — items 35A/35B at the launch point.

## 6. Calculation workflow

1. **Launch-point extraction.** Read rates 43A/44B → Rate(i,b,0) [INT-c], balances 35A/35B → Balance(i,b) [FACT items]. Validate per §10.
2. **Spread estimation.** Spread(i,b) = mean over 2020:Q2–2021:Q4 of (firm subcomponent rate − Treasury3m) [FACT method/window by reference; INT elided comparator]. If a firm lacks ELB-window history: UNKNOWN — no fallback stated [FACT absence].
3. **Parameters.** Betas from Table A7 (§3.3) — the firm items 83A–84B are *not* read at projection time [FACT: "The beta used in the model is the median of the firm-reported betas for the respective deposit category at lift-off", PDF p. 213].
4. **Scenario prep.** Align Treasury3m to PQ0…PQ9; ΔTreasury3m(t) = Treasury3m(t) − Treasury3m(t−1) [INT-f: Δ undefined in source beyond "the change"]; First_ELB_Treasury3m from the scenario path [FACT].
5. **Regime test, each t.** Treasury3m(t) < 25 bp → A45; > 25 bp → A46; **= 25 bp unassigned** [OQ-013; CODE: assign to non-ELB (strict reading of A46's "> 25bps" printed condition), document the choice].
6. **Rate recursion per subcomponent.** Apply A45/A46 for i ∈ {nontime, time}, t = 1…9 in order. All terms annualized; nothing ÷4 inside the recursion [PID-6/D-004].
7. **Aggregation.** Eq A47 with constant 35A/35B weights → Rate(b,t).
8. **Expense** (§7), then expose the path to the cross-cutting hedge adjustment (§11).

**Intermediates:** `elb_spread` (i,b; annualized rate); `delta_rate` δ(i,t) (i,t; annualized rate change); `assumed_floor` (i,b; annualized rate); `foreign_subcomponent_rate` Rate(i,b,t); `foreign_agg_rate` Rate(b,t); `foreign_interest_expense` Expense(b,t) (USD/quarter).

## 7. Output calculation

- [FACT, by reference] "The aggregate interest rate … is then multiplied by the average balance … as reported in the FR Y-14Q to produce the interest expense" (PDF p. 214; md sec-199, "average" per the December 2025 revision, PDF pp. 4–5). The v.a(9) text names no separate expense-balance item [FACT absence].
- [INT-a] Working assumption: expense balance = Balance(nontime,b) + Balance(time,b) = items 35A + 35B at the launch point — the same balances the source names for this component.
- [PID-6/D-004] Quarterly dollars: **Expense(b,t) = (Balance(nontime,b) + Balance(time,b)) × Rate(b,t) / 4** — the ÷4 occurs only at this final annualized→quarterly step (simple nominal quarterization, not compounding); never attributed to the Fed. The source states no conversion for this component [FACT absence; OQ-006 resolution].

## 8. Fed-stated assumptions and limitations

All [FACT] (PDF pp. 215–216; md sec-203), restated faithfully:

1. **One model for both foreign time and non-time.** "the Board assumed that both foreign time and foreign non-time deposits should follow the same model. This decision abstracts from the inherent differences in the contractual characteristics of time and non-time deposits while it prioritizes the Policy Statement principle of simplicity." (Contrast: domestic time deposits get their own WAL model, v.a(7).)
2. **Re-origination at the 3-month Treasury yield.** "re-originated foreign deposits are priced at the 3-month Treasury yield. This assumption abstracts from the fact that foreign deposits earn a rate more in line with their country of origin. Since there is no data available on the current regulatory forms regarding the country of origin, the Board decided to assume the price is the 3-month Treasury yield for all foreign deposits. This aligns with the scenario, which assumes a worldwide recession in which all central banks lower interest rates substantially."
3. **No exchange-rate effects.** "Similarly, there is no consideration of the effect of exchange rates over the scenario."

Inherited by reference from v.a(8) (PDF pp. 214; md sec-199): ELB = 25 bp threshold (historical 0–25 bp policy floor; 3M Treasury as risk-free proxy); non-ELB treated as normal periods (abstracts from yield compression near the ELB); assumed floor prevents rates below the ELB-anchored floor in non-ELB periods; constant **median** beta for all firms (no market power; abstracts from time variation in betas) — SQ-12: two assumptions are both labeled "A third assumption" in the source.

[ALT] No alternative is discussed within v.a(9) itself [FACT absence]; the Call-Report maturity-structure alternative belongs to v.a(7) only.

## 9. User-confirmed implementation mappings

- [PID-6/D-004] Annualized-rate convention and final-step ÷4 (decision log, `handbook/open-questions.md`).
- [PID-5 pattern] Scenario source: MEV workbook, Date column + one column per MEV; the 3M-Treasury column name ("USD 3M Treasury"?) is **UNCONFIRMED** for this model — confirm before coding [CODE].
- No foreign-deposit-specific PID exists yet. Rate/balance items need no PID (source-named: 43A, 44B, 35A, 35B). Candidate PIDs for user confirmation: expense balance = 35A+35B [INT-a]; beta item mapping [INT-b]; seed rates [INT-c]; Spread comparator [INT, §3.3]; =25 bp branch [OQ-013].

## 10. Validation requirements

[CODE] — non-normative; failures surface as errors, no invented fallbacks:

- Missing/negative launch-point rate (43A, 44B) or balance (35A, 35B); both balances zero → A47 divides by zero.
- Missing 2020:Q2–2021:Q4 rate history → Spread(i,b) incomputable (no Fed fallback stated).
- Spread sanity: Spread(i,b) implying a negative floor is possible (rates below the 3M Treasury during ELB); log, do not clamp — no non-negativity constraint exists in A45/A46 beyond the assumed floor [FACT absence].
- Reproduce Table A7 foreign medians (0.890/0.790/1.000/1.000) from item 83A–84B data when available.
- Regime coverage: every t assigned exactly one regime; log any Treasury3m(t) = 25 bp hit [OQ-013].
- Monotonic sanity: with time betas = 1.000, the foreign-time rate should track ΔTreasury3m one-for-one in non-ELB periods.

## 11. Dependencies and hedge interface

- Upstream: none among the proposed net-interest models; shared inputs only (3M Treasury; FR Y-14Q Schedule G). Methodology dependency: v.a(8) equations by reference — any change to A45–A47 in a final rule propagates here [FACT reference structure].
- Sibling parameters: Table A7 rows shared with `ie_other_dom_dep` (SQ-2: caption cites "(Equations A46)").
- Hedge: v.a(9) contains no hedge term [FACT absence]. The cross-cutting v.c adjustment (Eqs A49–A51; contingent on the proposed FR Y-14Q B.2/B.3 collection) may adjust this component later; allocation across components is unresolved [OQ-005]. This chapter exposes the expense path; no hedge computation occurs inside the model.

## 12. Open issues

**Working-assumption register (flagged INTERPRETATIONS used throughout):** **INT-a** expense balance = items 35A + 35B (§7); **INT-b** beta items 83A/83B → non-time up/down, 84A/84B → time up/down, by ordering parallel with 79A–81B (§3.1); **INT-c** recursion seeds Rate(i,b,0) = launch-point items 43A/44B (§3.1); **INT-d** Balance(i,b,t) = Balance(i,b,PQ0) via the general constant-balance convention (§5); **INT-f** ΔTreasury3m(t) = Treasury3m(t) − Treasury3m(t−1), with the PQ0 value seeding t = 1 (§6). Each is a candidate PID for user confirmation (§9).

- **OQ-005 — OPEN.** Hedge-adjustment allocation across components (§11).
- **OQ-006 — RESOLVED (D-004).** Annualized units; ÷4 at the final step only (§7).
- **OQ-013 — OPEN (minor).** Treasury3m = 25 bp regime boundary unassigned; §6 step 5 records the working branch choice.
- **OQ-017 — OPEN (shared with `ie_other_dom_dep`).** Spread-estimation mechanics, including the elided comparator of the truncated source sentence (SQ-15).
- **OQ-018 — OPEN (shared with `ie_other_dom_dep`).** Recursion seed timing (INT-c / INT-f).
- **OQ-019 — OPEN (filed at integration, 2026-07-17; quirk SQ-16).** Item **44B** denotes the foreign-deposits–time *rate* (PDF p. 215) while v.a(10) names it a *balance* (PDF p. 217) — line-item collision in the source; resolve against the FR Y-14Q Schedule G instructions in the coding phase (PID-FFR-1 indicates v.a(10)'s balance usage is the misname).
- **OQ-020 — OPEN (minor; filed at integration, 2026-07-17).** Beta item → (subcomponent, direction) mapping [INT-b] — matters only for the Table A7 reproduction validation.
- **OQ-021 — OPEN (minor; filed at integration, 2026-07-17).** Hard-code published Table A7 medians vs. recompute firm-reported-beta medians at lift-off — shared with `ie_other_dom_dep`.

## 13. Key source references

| Claim | (PDF p.; md anchor) |
|---|---|
| Component proposal; Y-9C equivalence; smaller impact | (PDF p. 215; md sec-201) |
| "Identical … with the exception"; items 43A/44B, 35A/35B, 83A–84B | (PDF p. 215; md sec-202) |
| Eqs A45/A46 (regimes, floors, betas, First_ELB_Treasury3m); spread window 2020:Q2–2021:Q4; median-beta rationale | (PDF pp. 212–213; md sec-198) |
| Eq A47 aggregation; expense = aggregate rate × average balance | (PDF pp. 213–214; md sec-198–199) |
| ELB regime definition (25 bp) | (PDF p. 211; md sec-197) |
| Assumptions: one model for time and non-time; 3M-Treasury re-origination; no FX effects | (PDF pp. 215–216; md sec-203) |
| Inherited v.a(8) assumptions; SQ-12 | (PDF p. 214; md sec-199) |
| Question A179 (verbatim): "The Board seeks comment on the proposed approach to model interest expense on foreign deposits, as compared to the Board's current panel regression model." | (PDF p. 216; md sec-204) |
| Table A7 foreign betas; SQ-1/SQ-2 | (PDF p. 219; md sec-209) |
| Table A6 row; ten-component list; no estimation | (PDF pp. 168–169, 172–173; md sec-148–149) |
| Constant-balance convention | (PDF pp. 169–170, 218; md sec-148, sec-206) |
| Nine-quarter horizon; PPNR identity | (PDF pp. 6–8; md sec-2) |
| 44B as repo balance item (collision flag) | (PDF p. 217; md sec-205) |
| D-004 ÷4 convention; PID-5 MEV pattern | `handbook/open-questions.md` decision log; `ie_dom_time_dep.md` §3.2 |

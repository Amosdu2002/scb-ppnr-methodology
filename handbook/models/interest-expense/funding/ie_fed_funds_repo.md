# 10. Interest Expense on Federal Funds Purchased and Securities Sold under Agreements to Repurchase (`ie_fed_funds_repo`)

> **STATUS: Proposed for the 2026 stress test — public-comment stage, NOT adopted.**
> Source: Section B.v.a(10) (PDF pp. 216–219; md sec-205–208). Model type per Table A6: **Structural** (PDF pp. 168–169; md sec-148).
> Integrity flag: the Equation A48 title reads "…Securities Sold under the **Agreement to Purchase**" (PDF p. 217) — a source typo; the correct component name ("…Repurchase") is used throughout the section prose and this chapter. Related quirk: item 44B is also used as the foreign-deposits–time *rate* item in v.a(9) (PDF p. 215) — collision flagged in `reviews/interest-expense/deposits/ie_foreign_dep.review.md` §4.
> December 2025 revision: on p. 216, "federal funds sold" was corrected to "federal funds purchased" (PDF pp. 4–5).
> Chapter review state: **DRAFT** — see `reviews/interest-expense/funding/ie_fed_funds_repo.review.md`.
> Labels: **[FACT]** = Fed statement (cited); **[PID]** = project implementation decision (user-confirmed); **[INT]** = interpretation; **[CODE]** = coding consideration; **[OQ]** = open question.

## 1. Status and purpose

- [FACT] "The Board proposes an alternative structural approach to model interest expense on federal funds purchased and securities sold under agreements to repurchase." (PDF p. 216; md sec-205). One of the ten proposed structural net-interest components in Table A6 (PDF pp. 168–169; md sec-148).
- [FACT] Rationale: these liabilities "have short durations and are directly linked to short-term interest rates" (PDF p. 216; md sec-205). The approach "is equivalent to the one previously described for interest income on federal funds sold and securities purchased under agreements to resell, except that the federal funds and repo positions on the asset side are subsumed within the component other interest/dividend-bearing assets" (PDF p. 217; md sec-206).
- **Model type: structural calculator.** [FACT] No coefficients are estimated ("it does not involve coefficients estimation", PDF p. 218; md sec-207). No firm scalar, no deposit beta, no autoregression, no fixed effects appear anywhere in v.a(10) [FACT absence]. Tables A7/A8/A9 contain no parameter for this component [FACT].
- [FACT] Contrast with the **current** model (kept separate; not used here): current Equation A27 (PDF pp. 150–152; md sec-133) multiplies the 3-month Treasury by a firm-specific launch-point scalar k_b on FR Y-9C balances; proposed A48 drops the scalar entirely and uses FR Y-14Q Schedule G balances. Do not mix the two.

## 2. Inputs

### 2.1 Firm data (FR Y-14Q, Schedule G, Net Interest Income Worksheet)

| Input | Line item | Dimensions | Units | Timing | Label |
|---|---|---|---|---|---|
| Federal funds purchased balance (`fed_funds_purchased_balance`) | 44A ("federal funds purchased") | b | USD | Launch point (PQ0); constant over horizon | [FACT] item (PDF pp. 216–217; md sec-205) |
| Repo balance (`repo_sold_balance`) | 44B ("securities sold under agreements to repurchase") | b | USD | Launch point (PQ0); constant over horizon | [FACT] item (PDF p. 217; md sec-205); 44B collision flag, see banner |

- [INT] Component balance B(b,PQ0) = item 44A + item 44B. The source names both items as "the relevant balance for this component" without stating the sum explicitly; aggregation into the single balance B_b of Equation A48 is the only reading consistent with "Let B_b be the **total** balance" (PDF p. 217; md sec-206). Candidate PID for user confirmation.
- No MDRM codes are stated in v.a(10); none are invented [FACT absence].

### 2.2 Scenario data

| Variable | Role | Frequency | Units | Label |
|---|---|---|---|---|
| 3-month Treasury yield, Treasury3m(q) (`usd_3m_treasury`) | The model rate itself — used directly, unscaled and untransformed | Quarterly, q = 1…9 (no PQ0 value needed: no recursion, no delta) | Annualized rate [D-004] | [FACT] role (PDF p. 217; md sec-206); physical MEV workbook column name UNCONFIRMED — implementation-mapping TODO [CODE], not a methodology uncertainty |

### 2.3 Parameters

**None.** [FACT] No supplied or estimated parameter exists for this model; no beta, scalar, spread, floor, or threshold (PDF pp. 217–218; md sec-206–207; Tables A7–A9 contain no row for this component).

## 3. Equation A48

[FACT] Verified against the PDF page image (p. 217) this session. Source title (with typo preserved verbatim as an integrity note): "**Equation A48** – Interest Expense on Federal Funds Purchased and Securities Sold under the Agreement to Purchase".

$$F_{b,t} = B_{b,t}\,Treasury3m_t$$

- Treasury3m "is the 3-month Treasury yield for quarter t" [FACT, verbatim].
- Projection form, stated on the same page: $F_{b,q} = B_{b,q}\,Treasury3m_q$ for firm b in projection quarter q [FACT].
- The rate is **exactly** the contemporaneous 3-month Treasury yield — no spread, no scaling, no lag [FACT: no other term appears in A48].

## 4. Timing and flat-balance rule

- [FACT] "The stress test assumes constant balances for all firms; therefore, B(b,q) = B(b,q0) for all periods, where B(b,q0) represents firm's b balances at lift-off quarter q0. This means that the projected flow of expense is calculated based on the balances at lift-off." (PDF p. 218; md sec-206; source words "lift-off" retained per D-005 — handbook term: launch point, PQ0.)
- Balance(b,q) = Balance(b,0) for q = 1…9; the balance is measured **once**, at PQ0 [FACT].
- Treasury3m(q) is contemporaneous each projection quarter [FACT]; nothing else varies over the horizon.
- Dimensions: b = firm; s = scenario; q = 1…9 (nine-quarter horizon, PDF p. 6; md sec-2). No subcomponent dimension survives past the balance aggregation.

## 5. Calculation workflow

1. **Launch-point extraction.** Read Schedule G items 44A and 44B at PQ0 [FACT items]. Validate per §8.
2. **Balance aggregation.** Balance(b,0) = 44A + 44B [INT, §2.1].
3. **Scenario prep.** Load `usd_3m_treasury` for q = 1…9, in annualized units; do **not** divide the rate here [PID, D-004].
4. **Rate assignment.** AnnualizedRate(q) = Treasury3m(q), each quarter, unmodified [FACT].
5. **Quarterly expense.** QuarterlyExpense(b,q) = Balance(b,0) × AnnualizedRate(q) / 4, for q = 1…9 (§6).
6. **Hand-off.** Expose the expense path per firm × scenario × quarter to aggregation and to the cross-cutting hedge adjustment (§9).

**Intermediates:** `fed_funds_repo_balance` Balance(b,0) (USD); `fed_funds_repo_rate` AnnualizedRate(q) (annualized rate); output `fed_funds_repo_interest_expense` QuarterlyExpense(b,q) (USD/quarter).

## 6. Quarterly expense conversion

- [PID, D-004] All rates in this project are annualized; the annualized→quarterly-dollar conversion divides by four **only** at the final expense step: **QuarterlyExpense(b,q) = Balance(b,0) × Treasury3m(q) / 4** (simple nominal quarterization, not compounding). Never attributed to the Fed: v.a(10) states no conversion for this component [FACT absence; OQ-006 resolution].
- [CODE] Rate-scale normalization (percent vs. decimal in the MEV source) must be resolved at ingestion so that the model consumes a decimal annualized rate.

## 7. Fed-stated assumptions and limitations

All [FACT] (PDF p. 218; md sec-207), restated faithfully:

1. **Rate = 3-month U.S. Treasury.** "the Board makes the assumptions that the rate each firm earns over the projection horizon is given by the 3-month U.S. Treasury rate."
2. **Special/rare collateral caveat.** "While the 3-month U.S. Treasury rate tracks the overnight and other short-term borrowing rates closely, some fluctuations may be observed, especially when the short-term borrowing is collateralized by special or rare securities." Actual repo rates can therefore differ from the Treasury proxy.
3. **Why structural, not regression.** Advantages over a panel regression: "enhanced clarity and explainability as well as simplicity (since it does not involve coefficients estimation)"; projection variability "can be fully explained by reported balances for each bank and the variation in the interest rate scenario paths"; and gross-vs-net reporting discretion under balance-sheet-offsetting rules "could produce less precise projections when a regression approach is adopted."

Public-input request: Question A180 (PDF pp. 218–219; md sec-208) seeks comment on this approach versus the Board's current model.

## 8. Validation checks

[CODE] — non-normative; failures surface as errors, no invented fallbacks:

- Missing or negative launch-point balance in 44A or 44B; both zero → expense identically zero (log, likely a reporting gap).
- `usd_3m_treasury` present for all q = 1…9 in every scenario; flag negative values (expense would flip sign — arithmetically valid under A48, but log it).
- Rate-scale sanity: annualized decimal in a plausible range (e.g., |rate| < 0.25) to catch percent/decimal errors.
- Flat-balance invariant: Balance(b,q) identical for all q.
- Linearity invariant: expense path is exactly proportional to the scenario Treasury3m path (structural check — any deviation means a coding error).

## 9. Hedge-adjustment interface

- v.a(10) contains no hedge term [FACT absence]. The cross-cutting v.c adjustment (Eqs A49–A51, PDF pp. 220 ff.; md sec-210–211; contingent on the proposed FR Y-14Q B.2/B.3 collection) may adjust interest expense later; allocation across components is unresolved [OQ-005].
- The base calculation above remains fully separate: this model only exposes its expense path; no hedge computation occurs inside it.

## 10. Open implementation items

- [INT → candidate PID] Balance aggregation 44A + 44B (§2.1) — user confirmation requested.
- [CODE, TODO] Physical MEV workbook column name for `usd_3m_treasury` (PID-5 pattern; unconfirmed for this model — implementation mapping, not methodology).
- [OQ-005 — OPEN] Hedge-adjustment allocation (§9).
- [OQ-006 — RESOLVED (D-004)] Annualized units; ÷4 at the final step only (§6).
- Existing quirk (tracked in `ie_foreign_dep` review §4; not re-filed here): item 44B double use across v.a(9)/v.a(10) — resolve against FR Y-14Q Schedule G instructions in the coding phase.
- No other open item: no ELB regime, no seed rate, no history window applies to this model.

## 11. Key source references

| Claim | (PDF p.; md anchor) |
|---|---|
| Component proposal; short duration; items 44A/44B of the Schedule G NII Worksheet | (PDF pp. 216–217; md sec-205) |
| Equation A48 (incl. title typo "Agreement to Purchase"); Treasury3m definition; projection form; equivalence to the fed-funds-sold asset-side approach | (PDF p. 217; md sec-206) |
| Flat balance B(b,q) = B(b,q0) at lift-off | (PDF p. 218; md sec-206) |
| Assumptions: 3M Treasury rate; special/rare collateral caveat; no-estimation rationale; gross/net reporting discretion | (PDF p. 218; md sec-207) |
| Question A180 | (PDF pp. 218–219; md sec-208) |
| Table A6 row (Structural); model-type summary | (PDF pp. 168–169; md sec-148) |
| December 2025 revision: p. 216 "federal funds sold" → "federal funds purchased" | (PDF pp. 4–5; md sec-0) |
| Current model Eq A27 (comparison only; firm scalar k_b on FR Y-9C balances) | (PDF pp. 149–152; md sec-132–134; Y-9C items BHDMB993 + BHCKB995 per the data table, PDF p. 37) |
| Nine-quarter horizon | (PDF p. 6; md sec-2) |
| D-004 ÷4 convention; D-005 launch-point terminology | `handbook/open-questions.md` decision log |

# 2. Interest Income on Deposits with Banks and Other (`ii_dep_banks_other`)

> **STATUS: Proposed for the 2026 stress test — public-comment stage, NOT adopted.**
> Source: Section B.v.a(2) (PDF pp. 188–190; md sec-173–176). Model type per Table A6: **Structural** (PDF pp. 168–169; md sec-148).
> Integrity flags: (1) **SQ-3** — this section's Questions are numbered A161/A162, colliding with component (3)'s A161–A164 (always cite Board questions with their section, per the question-numbering note in `handbook/open-questions.md`). (2) **SQ-4** — the Questions intro on PDF p. 190 says "this proposed model for **interest income on loans**"; the section is the deposits-with-banks model. Verified against the page image this session: the misnomer is in the PDF itself, not conversion damage.
> Chapter review state: **REVIEWED** — source-grounding review 2026-07-23, verdict APPROVE (`reviews/interest-income/calculators/ii_dep_banks_other.review.md`); **user review gate passed 2026-07-23.** Specification: `specifications/interest-income/calculators/ii_dep_banks_other.yaml`.
> Labels: **[FACT]** = Fed statement (cited); **[PID]** = project implementation decision (user-confirmed); **[INT]** = interpretation; **[CODE]** = coding consideration; **[OQ]** = open question.

## 1. Status and purpose

- [FACT] "The Board proposes an alternative structural approach to model interest income on interest-bearing balances." (PDF p. 188; md sec-173). One of the ten proposed structural net-interest components (PDF p. 172; md sec-149; Table A6, PDF pp. 168–169; md sec-148).
- [FACT] Component composition: "Interest income from interest-bearing balances consists of interest-bearing deposits, including deposits held at the Federal Reserve and other institutions such as the Federal Home Loan Banks." (PDF p. 188; md sec-173).
- [FACT] Rationale: "These balances have short durations, typically less than a single quarter, and the rate earned is usually directly linked to short-term interest rates." (PDF p. 188; md sec-173).
- **Model type: structural calculator.** [FACT] Structural models "avoid statistical estimation" (PDF pp. 172–173; md sec-149); no coefficient, scalar, beta, or fixed effect appears anywhere in v.a(2) [FACT absence]. Tables A7/A8/A9 contain no row for this component [FACT].
- [FACT] The current model being replaced is a panel regression — Question A161's own words: "as compared to the Board's current panel regression model" (PDF p. 190; md sec-176). Current-suite mechanics are out of scope for this chapter; do not mix the two.
- [INT — navigation only] Equation A39 has the same one-line functional form as the expense-side Equation A48 (`ie_fed_funds_repo`): balance × contemporaneous 3-month Treasury. The sections are independent; nothing is shared beyond the form.

## 2. Model summary

Income each projection quarter = launch-point balance × contemporaneous 3-month Treasury yield. The rate is **exactly** the 3-month Treasury — zero spread, no transformation [FACT: no other term appears in Equation A39]. The balance is measured once, at the launch point, and held constant [FACT]. No parameters, no recursion, no regime, no floor.

## 3. Inputs

### 3.1 Firm data inputs

| Input | Line item | Dimensions | Units | Timing | Label |
|---|---|---|---|---|---|
| Interest-bearing balances (`dep_banks_other_balance`) | **Line item 14**, Net Interest Income Worksheet, FR Y-14Q Schedule G — **source-stated** | b | USD (millions at the model boundary, D-006) | Launch point (PQ0); constant over horizon | [FACT] (PDF p. 188; md sec-173) |

- [FACT] Source wording: "The relevant balances are reported in line item 14 of the net interest income worksheet of FR Y-14Q, Schedule G." (PDF p. 188; md sec-173). Unlike the deposit-expense models, the balance item is **named by the source** — no mapping PID is required at the Fed layer.
- [CODE] Project physical mapping (two-layer convention, `handbook/cross-cutting/asset-side-common-conventions.md` §6): the working assumption is that the firm's Schedule G extract supplies the item 14 balance at PQ0 directly. The physical sheet row is an implementation mapping to be confirmed at company-reference verification (candidate PID) — a working assumption, not a methodology uncertainty.
- No MDRM code is stated in v.a(2); none is invented [FACT absence].

### 3.2 Scenario inputs

| Variable | Role | Frequency | Units | Label |
|---|---|---|---|---|
| 3-month Treasury yield, Treasury3m(q) (`usd_3m_treasury`) | The model rate itself — used directly, unscaled and untransformed | Quarterly, q = 1…9 (no PQ0 value needed: no recursion, no delta) | Annualized rate [D-004] | [FACT] role (PDF p. 189; md sec-174); physical MEV workbook column name UNCONFIRMED — implementation-mapping TODO [CODE] |

### 3.3 Parameters

**None.** [FACT] No supplied or estimated parameter exists for this model; no beta, scalar, spread, floor, or threshold (PDF pp. 188–190; md sec-173–175; Tables A7–A9 contain no row for this component).

## 4. Timing and dimensions

- Dimensions: b = firm; s = scenario; q = 1…9 (nine-quarter horizon, PDF p. 6; md sec-2). No subcomponent dimension.
- Output grain: firm × scenario × quarter.
- The only launch-point quantity is the balance; no PQ0 scenario value is consumed.
- [FACT] Flat balance: "The stress test assumes constant balances for all firms; therefore, B(b,q) = B(b,q0) for all periods, where B(b,q0) represents the balances for the firm b at lift-off quarter q0. This means that the projected flow of income is calculated based on the balances at the last quarter before the start of the projection." (PDF p. 189; md sec-174; source word "lift-off" retained per D-005 — handbook term: launch point, PQ0.)
- Treasury3m(q) is contemporaneous each projection quarter [FACT]; nothing else varies over the horizon.

## 5. Equations and variable definitions

[FACT] Verified against the PDF page image (p. 189) this session.

**Equation A39** – Interest Income on Deposits with Banks and Other:

$$F_{b,t} = B_{b,t}\,Treasury3m_t$$

- "Treasury3m is the 3-month Treasury yield." [FACT, verbatim where-list]
- B_b is "the total balance on interest-bearing balances"; F_b is "the interest income earned on this component" [FACT] (PDF p. 189; md sec-174).
- Projection form, stated on the same page: $F_{b,q} = B_{b,q}\,Treasury3m_q$ for firm b in projection quarter q [FACT].
- The rate is **exactly** the contemporaneous 3-month Treasury yield — no spread, no scaling, no lag [FACT: no other term appears in A39].

## 6. Calculation workflow

1. **Launch-point extraction.** Read the Schedule G line item 14 balance at PQ0 (§3.1). Validate per §10.
2. **Scenario prep.** Load `usd_3m_treasury` for q = 1…9, in annualized decimal units; do **not** divide the rate here [PID, D-004].
3. **Rate assignment.** AnnualizedRate(q) = Treasury3m(q), each quarter, unmodified [FACT].
4. **Quarterly income.** QuarterlyIncome(b,q) = Balance(b,0) × AnnualizedRate(q) / 4, for q = 1…9 (§7).
5. **Hand-off.** Expose the income path per firm × scenario × quarter to aggregation and to the cross-cutting hedge adjustment (§11).

**Intermediates:** `dep_banks_other_balance` Balance(b,0) (USD millions); `dep_banks_other_rate` AnnualizedRate(q) (annualized decimal); output `dep_banks_other_interest_income` QuarterlyIncome(b,q) (USD millions/quarter).

## 7. Output calculation

- [PID, D-004] All rates in this project are annualized; the annualized→quarterly-dollar conversion divides by four **only** at the final income step: **QuarterlyIncome(b,q) = Balance(b,0) × Treasury3m(q) / 4** (simple nominal quarterization, not compounding). Never attributed to the Fed: v.a(2) states no conversion for this component [FACT absence; OQ-006 resolution].
- [CODE] Rate-scale normalization (percent vs. decimal in the MEV source) is resolved at ingestion; the model consumes a decimal annualized rate. Money normalizes to USD millions at the model boundary [D-006].

## 8. Fed-stated assumptions and limitations

All [FACT] (PDF pp. 189–190; md sec-175), restated faithfully:

1. **Rate = 3-month U.S. Treasury.** "the Board assumes that the rate each firm earns over the projection horizon is given by the 3-month U.S. Treasury rate."
2. **Reserves-rate tracking caveat.** "While the rate that the Federal Reserve pays on reserves tracks the 3-month U.S. Treasury rate closely, some fluctuations may be observed."
3. **Other-institution caveat.** "Additionally, the rates paid by other depository institutions may be higher or lower." Actual earned rates can therefore differ from the Treasury proxy in both directions.

Public-input request: Questions A161/A162 of section v.a(2) (PDF p. 190; md sec-176) — cite with the section per SQ-3; the intro's "interest income on loans" misnomer is SQ-4 (banner).

## 9. User-confirmed implementation mappings

None yet for this model. The Fed layer is fully source-stated (item 14, §3.1). Pending [CODE] confirmations, to be logged as PIDs when user-confirmed at company-reference verification:

| Pending item | Working assumption | Status |
|---|---|---|
| Physical firm-sheet row for item 14 balance | Spot sheet row `ii_dep_banks_other` / `balance`, scale declared per D-006/D-007 | TO BE CONFIRMED |
| MEV workbook column for `usd_3m_treasury` | PID-5 pattern; same unconfirmed column as the expense-side users of this series | TO BE CONFIRMED (shared item) |

## 10. Validation requirements ([CODE] — non-normative)

Failures surface as errors; no invented fallbacks; monitors log, never clamp:

- Missing or negative launch-point balance in item 14; balance zero → income identically zero (log, likely a reporting gap).
- `usd_3m_treasury` present for all q = 1…9 in every scenario; flag negative values (income would flip sign — arithmetically valid under A39, but log it).
- Rate-scale sanity: annualized decimal in a plausible range (e.g., |rate| < 0.25) to catch percent/decimal errors.
- Flat-balance invariant: Balance(b,q) identical for all q.
- Linearity invariant: the income path is exactly proportional to the scenario Treasury3m path (structural check — any deviation means a coding error).

## 11. Dependencies and hedge interface

- Upstream models: **none** [FACT — v.a(2) references only the Schedule G balance and the scenario rate].
- v.a(2) contains no hedge term [FACT absence]. The cross-cutting v.c adjustment (Eqs A49–A51, PDF pp. 220 ff.; md sec-210–211; contingent on the proposed FR Y-14Q B.2/B.3 collection) may adjust interest income later; allocation across components is unresolved [OQ-005]. This model only exposes its income path; no hedge computation occurs inside it.
- Family-level: the income path feeds the asset-side family aggregation and the eventual reconciliation monitor against the FRB-provided total-interest-income path (`frb_total_interest_income`, OQ-023 narrowing — a project input, never a Fed statement).

## 12. Open issues

- [CODE, TODO] Physical firm-sheet mapping for the item 14 balance (§9) — candidate PID at company-reference verification.
- [CODE, TODO] Physical MEV workbook column name for `usd_3m_treasury` (PID-5 pattern; shared with expense-side models).
- [OQ-005 — OPEN] Hedge-adjustment allocation (§11).
- [OQ-006 — RESOLVED (D-004)] Annualized units; ÷4 at the final step only (§7).
- [SQ-3, SQ-4 — filed 2026-07-16] Question-numbering collision and "loans" misnomer (banner) — logged in `inventory/source-integrity-review.md`.
- No other open item: no ELB regime, no seed rate, no spread estimation, no history window applies to this model.

## 13. Key source references

| Claim | (PDF p.; md anchor) |
|---|---|
| Component proposal; composition (Federal Reserve and FHLB deposits); source-stated balance line item 14 of the Schedule G NII Worksheet; short durations | (PDF p. 188; md sec-173) |
| Equation A39; Treasury3m definition; B_b/F_b definitions; projection form | (PDF p. 189; md sec-174) |
| Flat balance B(b,q) = B(b,q0) at lift-off | (PDF p. 189; md sec-174) |
| Assumptions: 3M Treasury rate; reserves-rate tracking caveat; other-institution caveat | (PDF pp. 189–190; md sec-175) |
| Questions A161/A162 (SQ-3 collision; SQ-4 "loans" misnomer in the intro) | (PDF p. 190; md sec-176) |
| Table A6 row (Structural); structural-model rationale ("avoid statistical estimation") | (PDF pp. 168–169, 172–173; md sec-148, sec-149) |
| Nine-quarter horizon | (PDF p. 6; md sec-2) |
| D-004 ÷4 convention; D-005 launch-point terminology; D-006 money units | `handbook/open-questions.md` decision log |

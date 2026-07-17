# 7. Interest Expense on Domestic Time Deposits (`ie_dom_time_dep`)

> **STATUS: Proposed for the 2026 stress test — public-comment stage, NOT adopted.**
> Source: Section B.v.a(7) (PDF pp. 209–211; md sec-193–196). Model type per Table A6: **Structural** (PDF pp. 168–169; md sec-148).
> Integrity flags affecting this chapter: SQ-4 (Questions intro says "interest income", PDF p. 211); SQ-1/SQ-2 (Table A7 quirks — relevant only to the §3.3 non-applicability note); December 2025 revision item for p. 209 ("end of quarter" → "average"; PDF pp. 4–5, md sec-0). Conversion artifacts in v.a(7): none.
> Chapter review state: **REVIEWED** — Step 5 independent source-grounding review completed 2026-07-17; material findings corrected (Step 6). Awaiting user approval before commit (Step 8). Approved content is never silently overwritten.
> Working basis: `research/source-briefs/interest-expense/deposits/ie_dom_time_dep.source-brief.md` (revised and approved 2026-07-17), which holds the full input/assumption registers and traceability table.
> Labels: **[FACT]** (Fed source methodology, cited), **[INT]** (interpretation with stated basis), **[CODE]** (coding consideration, non-normative), **[OQ]** (open question by ID), extended per the approved brief §0 with **[PID]** = PROJECT IMPLEMENTATION DECISION — USER CONFIRMED (2026-07-17; PID-1…PID-6, never attributable to the Federal Reserve) and **[ALT]** = alternative discussed by the Fed but not proposed. Citations: (PDF p. N; md sec-M).

## 1. Component definition and scope

- [FACT] Exact Fed component name: **"Interest Expense on Domestic Time Deposits"** — one of the 10 components for which the Board proposes structural models (PDF pp. 172, 209; md sec-149, sec-193). Table A6 lists "Domestic time deposits" under "Structural models for interest expense" (PDF pp. 168–169; md sec-148).
- [FACT] Proposed-model reporting basis, FR Y-14Q Schedule G: line item **42E** "(Time Deposits)" supplies the jump-off average rate; line item **71** "(Domestic Deposits – Time)" supplies the Weighted Average Life; the expense uses "the average balance on domestic time deposits as reported in the FR Y-14Q" with **no line item named** (PDF p. 209; md sec-193–194). The word "average" is the December 2025 revision ("end of quarter" → "average"; PDF pp. 4–5; md sec-0).
- [PID-1] Project balance mapping: Schedule G item **34E**, launch-point value, held flat across all nine projection quarters. "34E" appears nowhere in the Fed source (full-document search 2026-07-17); the mapping is user-confirmed project context, not a Fed statement.
- [FACT] Boundaries: foreign time deposits belong to Interest Expense on Foreign Deposits (Schedule G items 44B rate / 35B balance; PDF pp. 215–216; md sec-201–202); domestic non-time deposits (money market, savings, transaction) belong to Interest Expense on Other Domestic Deposits (PDF p. 211; md sec-197). This component absorbs nothing from, and cedes nothing else to, other components.
- [FACT — current-suite context] The current 2025 suite defines the component as "interest expense on domestic time deposits of \$250,000 or less plus time deposits of more than \$250,000", sourced from FR Y-9C codes BHCKHK03 + BHCKHK04 (expense) and BHCBJ474 + BHODJ474 + BHCBHK29 + BHODHK29 (balances) (PDF pp. 75, 35–39; md sec-65, sec-19–21, fn 27). The proposed model reads FR Y-14Q, not FR Y-9C; this identity is kept for §10 comparison only.

## 2. What the model projects

- [FACT] Output quantity: quarterly **dollar interest expense** on domestic time deposits, one value per firm `b` per projection quarter `t` = 1…9 (nine-quarter projection horizon; PDF p. 6; md sec-2). [INT] Computed per scenario: the stress test projects under supervisory scenarios (PDF p. 6; md sec-2), but v.a(7) itself carries no scenario index. [FACT] It is an expense item, entering PPNR through net interest income (Equation A1; PDF pp. 6–8; md sec-2).
- [FACT] The model's dependent variable is a rate: "the rate paid on domestic time deposits" Rate(b,t) (`dtd_rate`), projected by Equation A44 (PDF p. 209; md sec-193–194). [CODE] The rate path is retained as an intermediate output for traceability — a handbook design choice, not a Fed requirement.
- [FACT] The source uses "jump-off quarter" (PDF p. 209) and "at lift-off" (PDF p. 210) for the same quarter. [INT] PQ0 — the handbook's standardized **launch point** (decision D-005) — is the last quarter before the projection horizon, per the framework's usage elsewhere ("balances at the last quarter before the start of the projection", v.a(2), PDF p. 190; md line 3792; "$q0$ represents the lift-off quarter", current-suite structural sections, PDF pp. 145–152; md line 2865).
- [PID-6] Dollar basis: all rates are annualized; the quarterly dollar figure divides the annualized rate by four at the final step only (§4 step 5). No segment dimension exists (§7).

## 3. Inputs

### 3.1 Firm data inputs

| Input | Fed source (schedule, line item) | Dimensions | Units | Timing (launch-point definition) | Label |
|---|---|---|---|---|---|
| Average rate paid on domestic time deposits, Rate(b,0) (`domestic_time_deposit_rate_launchpoint`) | FR Y-14Q Schedule G item 42E (Time Deposits) | b | Annualized rate [PID-6]; scale normalization §12 | Average rate in the jump-off quarter; used once as the recursion seed | [FACT] (PDF p. 209; md sec-194) |
| Weighted Average Life, WAL_b (`domestic_time_deposit_wal_months`) | FR Y-14Q Schedule G item 71 (Domestic Deposits – Time) | b | **Months** [PID-3] — unit not stated in the source ([FACT] absence) | As-reported; as-of quarter not stated — taken at PQ0 consistent with the other launch-point inputs [INT] | [FACT] source (PDF p. 209); [PID-3] unit |
| Average balance on domestic time deposits (`domestic_time_deposit_balance`) | Source: "as reported in the FR Y-14Q", item not named ([FACT] absence); project: Schedule G item 34E [PID-1] | b | USD | Launch-point average balance, held flat for t = 1…9 [PID-1] | [FACT] role (PDF p. 209; md sec-193); [PID-1] mapping |

### 3.2 Scenario inputs

| Scenario variable | Enters via | Frequency | Units | Label |
|---|---|---|---|---|
| 1-year Treasury yield, Treasury1y(t) (`usd_1y_treasury`) | Equation A44, weight ρ_b, contemporaneous at each t | Quarterly, t = 1…9 | Annualized rate [PID-6]; scale normalization §12 | [FACT] (PDF p. 209; md sec-194). Project sourcing: MEV workbook column named exactly "USD 1Y Treasury" (Date column + one column per MEV), aligned to the nine projection quarters [PID-5] — the source describes no scenario storage format ([FACT] absence) |
| 3-month Treasury yield | **Not used by this model.** Equation A44's only scenario input is the 1-year Treasury; the 3-month Treasury drives the sibling deposit models and other calculators | — | — | [FACT] absence (PDF pp. 209, 211–216; md sec-193–205) |

### 3.3 Parameters

| Parameter | Supplied or estimated | Source (Table A7/A8/A9 or derivation) | Value(s) or UNKNOWN | Constant over horizon? | Label |
|---|---|---|---|---|---|
| Repricing fraction ρ_b ≡ 1/WAL_b (`repricing_fraction_rho`) | Derived from firm data — neither estimated nor published | Item 71; ρ_b = 1/WAL_quarters(b) = 3/WAL_months(b) [PID-3/PID-4] | Firm-specific, from data | **Yes** — "remains constant throughout the projection" | [FACT] definition and constancy (PDF p. 209; md sec-194); [PID] months→quarters conversion |
| Estimated coefficients | — | — | **None exist** — proposed structural models "avoid statistical estimation" | — | [FACT] (PDF pp. 172–173; md sec-149) |
| Deposit betas (Table A7) | — | Table A7 "Median Betas for Proposed Deposit Models (Equations A46)" | **Not applicable — no domestic-time row exists**; the table serves the other-domestic and foreign deposit models | — | [FACT] (PDF p. 219; md sec-209); quirks SQ-1 (Down-row internal names in the published PDF) and SQ-2 (caption cites A46) recorded, never corrected |

No firm fixed effects exist for this model; the D-002 backsolving decision does not apply here.

## 4. Calculation sequence

1. **Extract launch-point inputs (PQ0).** Read item 42E → Rate(b,0), item 71 → WAL_months(b) [FACT], and item 34E → AverageBalance(b) [PID-1]. Validate per §12: missing WAL; zero or negative WAL; ρ_b outside the economically valid range; missing starting rate; missing balance — a failure surfaces as an error; **no fallback treatment is invented** [PID, user instruction].
2. **Repricing fraction.** WAL_quarters(b) = WAL_months(b) / 3; ρ_b = 1/WAL_quarters(b) = 3/WAL_months(b) (`repricing_fraction_rho`) [PID-3/PID-4]. ρ_b is firm-specific and constant for all nine quarters — [FACT] "This fraction is reflective of the portfolio's maturity profile and remains constant throughout the projection" (PDF p. 209; md sec-194).
3. **Scenario series.** Select the MEV workbook column named exactly "USD 1Y Treasury" and align it to projection quarters PQ1…PQ9 → Treasury1y(t) [PID-5].
4. **Rate recursion — Equation A44** [FACT] (PDF p. 209; md sec-194; verified against the PDF page image):

   **Equation A44** – Interest Expense on Domestic Time Deposits Rate Projection

   $$Rate_{b,t} = \rho_b * Treasury1y_t + (1 - \rho_b) * Rate_{b,t-1}$$

   *where* (condensed restatement — exact bulleted where-list in brief §7.2): Rate(b,t) is the rate paid on domestic time deposits by firm b at quarter t; ρ_b ≡ 1/WAL_b is the fraction of the portfolio that reprices every period (quarter), WAL_b the weighted average life of domestic time deposits for firm b; Treasury1y(t) is the 1-year Treasury yield at quarter t.

   Coding restatement: for t = 1…9 in order, `dtd_rate[b,t] = rho_b * usd_1y_treasury[t] + (1 - rho_b) * dtd_rate[b,t-1]`, seeded by `dtd_rate[b,0]` = item 42E. All terms are annualized rates; nothing is divided by four inside the recursion [PID-6]. No floor, cap, non-negativity constraint, or regime switch applies — none is stated in v.a(7) ([FACT] absence; contrast the assumed floor of v.a(8), PDF pp. 211–213).
5. **Quarterly dollar expense.** [FACT] "Interest expense on domestic time deposits is computed by multiplying the modeled rate by the average balance on domestic time deposits as reported in the FR Y-14Q" (PDF p. 209; md sec-193). [PID-6] QuarterlyExpense(b,t) = AverageBalance(b,t) × Rate(b,t) / 4 — the ÷4 occurs **only** at this final annualized-rate → quarterly-dollar conversion, as simple nominal quarterization (not effective compounding). [FACT — absence] The source states no conversion for this component; within the proposed 2026 suite, its explicit ÷4 / N/360 statements appear only in trading-NII data construction, securities coupon accrual, and hedge legs (PDF pp. 225; 191, 196, 201; 222). The current-suite subordinated-debt model's footnote 54 separately states an annual-rate ÷4 convention — "coupon rates are always stated as annualized rates" (PDF p. 155; md line 5338) — a current-suite parallel that supports, but does not state, the convention for this component. The ÷4 is therefore never attributed to the Fed.
6. **Hedge hook.** Expose the expense path for the separate cross-cutting interest-rate-risk hedge adjustment (§8). No hedge computation occurs inside this model [FACT absence; OQ-005].

**Intermediates register**

| Intermediate | Defined in step | Dimensions | Units | Label |
|---|---|---|---|---|
| `wal_quarters` | 2 | b | Quarters | [PID-3/PID-4] |
| `repricing_fraction_rho` (ρ_b) | 2 | b | Fraction per quarter | [FACT] definition; [PID-4] formula |
| `dtd_rate` path, Rate(b,t) | 4 | b × scenario × t (incl. seed t=0) | Annualized rate | [FACT]; units [PID-6] |
| Annualized expense basis, Rate(b,t) × AverageBalance(b,t) | 5 | b × scenario × t | USD per annum | [FACT] product form |
| `dtd_interest_expense`, QuarterlyExpense(b,t) | 5 | b × scenario × t | USD per quarter | [PID-6] ÷4 |

Unit conversions in this model, all explicit: months → quarters ÷3 [PID-3/PID-4]; annualized rate → quarterly dollars ÷4 at step 5 only [PID-6]. No N/360 and no compounding conventions apply here ([FACT] absence; PID-6 "simple nominal quarterization").

## 5. Launch point (PQ0) vs. projection-quarter register

| Quantity | Launch point (PQ0) role | Projection-quarter (t ≥ 1) role | Label |
|---|---|---|---|
| Rate(b,0) — item 42E | Measured once: average rate in the jump-off quarter | Seeds the t = 1 recursion step only | [FACT] (PDF p. 209) |
| WAL_b → ρ_b | Measured once (as-of PQ0 [INT]); ρ_b derived | Constant weight in every quarter's recursion | [FACT] constancy; [PID-3/PID-4] conversion |
| AverageBalance(b) — item 34E | Measured once at the launch point | Identical value multiplies every quarter's rate | [PID-1]; item and quarter unstated in source ([FACT] absence) |
| Treasury1y(t) | Not a PQ0 input | Contemporaneous scenario value at each t | [FACT]; [PID-5] sourcing |
| Rate(b,t−1) | Equals Rate(b,0) when t = 1 | Prior projection quarter's modeled rate | [FACT] |
| QuarterlyExpense(b,t) | — | Computed at each t from Rate(b,t) and the flat balance | [FACT] form; [PID-6] ÷4 |

## 6. Constancy register

| Quantity | Constant or varying over the horizon | Source statement | Label |
|---|---|---|---|
| ρ_b (repricing fraction) | **Constant** | "remains constant throughout the projection" (PDF p. 209; md sec-194) | [FACT] |
| Balance | **Constant** (flat at launch-point item 34E value) | Not restated in v.a(7); general constant-balance convention (PDF pp. 169–170, 181–182, 207, 221; md sec-148, sec-164, sec-190, sec-211) | [PID-1]; application of the general convention [INT] |
| Rate(b,t) | Varies — recursion toward the scenario path | Equation A44 (PDF p. 209) | [FACT] |
| Treasury1y(t) | Varies — scenario path | (PDF p. 209) | [FACT] |
| Portfolio composition | No composition dimension exists (single aggregate portfolio) | (PDF pp. 209–210) | [FACT] absence |
| Floors / caps | None exist in this model | No constraint stated in v.a(7); contrast v.a(8)'s assumed floor (PDF pp. 211–213) | [FACT] absence |
| Betas, spreads, scalars, fixed effects | None used | §3.3 | [FACT] absence |

## 7. Segmentation and aggregation

[FACT — absence] The proposed model applies **no segmentation**: one aggregate domestic time-deposit portfolio per firm, one rate path, one balance (PDF pp. 209–210; md sec-193–195). There is consequently no roll-up or weighting step. Contrast: other domestic deposits aggregates three subcomponents balance-weighted via Equation A47 (PDF p. 213; md sec-198), and foreign deposits combines non-time and time subcomponents (PDF pp. 215–216; md sec-202). The Fed's stated reason a richer structure is absent here: only one piece of maturity information (the WAL) is used (PDF p. 210; md sec-195; §9).

## 8. Interest-rate-risk hedge treatment

- [FACT] Equation A44 contains **no hedge term**, and v.a(7) does not mention hedges (PDF pp. 209–211).
- [FACT] Section v.c proposes a **separate, cross-cutting** adjustment for qualified accounting hedges, contingent on the proposed FR Y-14Q Schedule B.2 collection (a companion Schedule B.3 is proposed in the securities sections — PDF pp. 192, 197, 203; md lines 3854, 3933, 4013): per projection quarter, Hedge NII Impact = accrued interest income − accrued interest expense on the hedge legs (Equations A49–A51; N/360 day count; caps/floors via strike details); terminated-hedge effects amortize over the remaining life of the hedged item; renewals/terminations during the horizon are not modeled, for consistency with the fixed balance-sheet assumption (PDF pp. 220–223; md sec-210–212).
- **Two data states**, presented per the handbook convention: (i) current state — the proposed collection does not yet exist, so no component-level hedge adjustment is computable; (ii) proposed-collection state — the v.c adjustment becomes computable from the new data. This chapter does **not** state that hedges have no effect on final projected expense: hedge effects may be incorporated later through the separate cross-cutting adjustment. [OQ → OQ-005] The allocation of that adjustment across components (including this one) is unresolved.
- Cross-reference: the cross-cutting hedge chapter (planned, `handbook/cross-cutting/`) will own Equations A49–A51 in full.

## 9. Assumptions and limitations (source-stated)

All [FACT], (PDF pp. 210–211; md sec-195), restated faithfully:

1. **Constant repricing percentage.** "A structural model specification necessarily requires assumptions about future behavior. First, a constant percentage of the portfolio is assumed to be repriced every period. This assumption abstracts from the heterogeneity of the rate and maturity profile in a firm's time deposit portfolio. Using only one piece of information about maturity profiles, the Weighted Average Life, necessitates this simplifying assumption."
2. **Re-origination at the 1-year Treasury; no market power.** "A second assumption is that all re-originated time deposits are priced at the 1-year Treasury yield. In this model, firms do not have market power in time deposit pricing. The only difference in the level of rates throughout the projection period comes from the rate paid on domestic time deposits at lift-off and the firm-specific Weighted Average Life. Assuming all re-originations are paid, the 1-year Treasury yield also ignores the heterogeneity in rates that comes with the origination of new time deposits." — [INT] the last sentence's comma placement reads as "are paid *the* 1-year Treasury yield"; meaning unaffected; flagged as a candidate typography quirk for the integrity review.
3. **Limitation — no richer maturity structure.** "A limitation of the model is that richer maturity structures are not possible. Time deposits have contractual maturities that do not factor into this mechanism. For example, a time deposit balance that reprices to the 1-year Treasury yield in one quarter is as equally likely to be repriced in the following quarter as any other time deposit. There is no mechanism for the time deposit balance to be held for the contractual term."

**[ALT] Alternative discussed but not proposed:** using Call Report maturity-profile data (quantities due to mature in 1 quarter, 1 year, and 3 years) to let fixed amounts mature each quarter, repricing matured balances at a reference rate while unmatured balances keep their original rate; the Fed states this could add maturity/rate heterogeneity "but as a trade-off it entails further data processing and increased model complexity" (PDF pp. 210–211; md sec-195). **Excluded from §4** — recorded only as an alternative the Fed considered.

Background: general structural-model limitations — strict theory/contract-based relationships; re-origination assumptions still required (PDF p. 33; md sec-15).

## 10. Comparison with the current 2025 model

Kept short, per template; all COMPARISON context (current-suite pages not individually re-verified, per the integrity review's policy):

- [FACT] The current model (iv.i(1)) is a **panel regression** whose dependent variable is the ratio of expense to domestic time-deposit balances, driven by the 3-month Treasury yield (its coefficient framed as the historical "deposit beta"), with a Year AR term and firm plus rolling-window fixed effects (Equation A10; PDF pp. 75–79; md sec-65).
- [FACT] The proposed model replaces statistical estimation with a direct structural recursion on the reported **rate**; the reference rate changes from the 3-month to the **1-year** Treasury yield; expense follows by balance multiplication (PDF p. 209; md sec-193–194).
- [FACT] Current-suite estimated parameters for this component sit in iv.l (PDF pp. 141–144; md sec-126) and are **not** inputs to the proposed model.
- [FACT] Question A177 explicitly frames the public-comment comparison between the two approaches (PDF p. 211; md sec-196).

## 11. Board questions relevant to this chapter

- [FACT] Proposed-model question, verbatim (PDF p. 211; md sec-196): *"Question A177: The Board seeks comment on the proposed approach to model interest expense on domestic time deposits, as compared to the Board's current panel regression model."* — **SQ-4**: the Questions intro reads "this proposed model for interest **income** on domestic time deposits" although this is an expense model (verified on the page image); the question itself names the correct component.
- [FACT — comparison context] The current-suite section carries Questions A43–A49 on this component (PDF pp. 79–80; md lines 1620–1636), including A43 (structural alternative vs. current approach), A48 (heterogeneous funding costs and deposit betas), and A49 (nonlinearity) — useful signals of methodology the Fed itself treats as open.
- [FACT] Cross-cutting hedge questions A181–A187 (PDF pp. 223–224; md sec-213) affect §8 and belong to the hedge chapter.

## 12. Coding considerations ([CODE] — non-normative)

Nothing here is Fed methodology; full detail in the source brief §12.

- **Canonical input names → future MDRM-based mapping** (recorded per user instruction; no dictionary built, no MDRM workbook retrieved, no Python): `domestic_time_deposit_balance` → FR Y-14Q Schedule G item 34E; `domestic_time_deposit_rate_launchpoint` → item 42E; `domestic_time_deposit_wal_months` → item 71; `usd_1y_treasury` → MEV column "USD 1Y Treasury". Mapping fields: schedule; line item; MDRM code (TBD); unit; frequency; required transformation.
- **Validation (no fallback for any invalid input — failures surface, treatment undecided):** missing WAL; zero or negative WAL; WAL implying ρ_b outside (0, 1] (WAL_months < 3 ⇒ ρ_b > 1; very large WAL ⇒ ρ_b ≈ 0 — thresholds configurable); missing starting rate (42E); missing balance (34E).
- **Rate-scale normalization (separate consideration):** raw rates may be percent or decimal; never assume whether a raw 5 means 5 percent or 500 percent without source metadata; normalize metadata-driven, identically for item 42E and the MEV series, before the recursion.
- **Named transforms:** the ÷3 (months → quarters) and the final-step ÷4 (annualized → quarterly dollars, fixed by [PID-6]) are named, documented transforms — never hidden literals; the ÷4 is not configurable.
- **Data objects:** firm-input table (b × {balance, rate0, WAL_months}); scenario table (projection-quarter/Date × MEV); outputs dimensioned b × scenario × t (rate path and expense path).
- **Pattern caveat:** the partial-adjustment recursion resembles, but is not, the v.a(8) non-ELB mechanism (Equation A46 operates on beta-scaled rate *changes* with a floor); any shared implementation must keep the equations distinct and traceable.
- **Edge monitors:** negative projected rates are possible only if the scenario 1-year Treasury path or the launch-point rate (item 42E) is negative — the projected rate is a convex combination of the two (no floor exists in the model); log, do not clamp.

## 13. Open questions

- **OQ-005 — OPEN.** Division of hedge-adjustment responsibility across components if the proposed FR Y-14Q B.2/B.3 collection proceeds; §8 presents both data states. (`handbook/open-questions.md`)
- **OQ-006 — RESOLVED FOR PROJECT IMPLEMENTATION (2026-07-17; decision D-004).** Annualized-rate convention: Equation A44 runs entirely in annualized units; QuarterlyExpense = AverageBalance × Rate / 4 at the final step only [PID-6]. The PPNR source itself still does not state the conversion for this component — preserved as a fact of absence (§4 step 5).
- **OQ-008 — RESOLVED FOR PROJECT IMPLEMENTATION (2026-07-17).** Item 71 WAL is in months; WAL_quarters = WAL_months/3; ρ_b = 3/WAL_months [PID-3/PID-4]. The PPNR source does not state the unit — preserved as a fact of absence (§3.1).

No other open questions affect this chapter; none are newly filed.

## 14. Citation index

| Claim | (PDF p.; md anchor) |
|---|---|
| Component name; structural proposal; model narrative; dependent variable = rate | (PDF p. 209; md sec-193) |
| Expense = modeled rate × **average** balance (FR Y-14Q); balance item unnamed | (PDF p. 209; md sec-193) — "average" per revision (PDF pp. 4–5; md sec-0) |
| Equation A44 + where-list; item 42E initial rate; item 71 WAL; ρ constancy | (PDF p. 209; md sec-194) |
| Assumptions: constant repricing %; 1Y re-origination pricing / no market power / "at lift-off" | (PDF p. 210; md sec-195) |
| Limitation: no richer maturity structures; [ALT] Call Report variant | (PDF pp. 210–211; md sec-195) |
| Question A177; SQ-4 intro quirk | (PDF p. 211; md sec-196) |
| Table A6 row "Domestic time deposits — Structural" | (PDF pp. 168–169; md sec-148) |
| Ten-component list; Schedule G data basis; "avoid statistical estimation" | (PDF pp. 172–173; md sec-149) |
| Nine-quarter projection horizon; PPNR identity (Eq A1) | (PDF pp. 6–8; md sec-2) |
| Structural-model definition; "date of lift-off"; re-origination assumptions | (PDF pp. 32–33; md sec-14, sec-15) |
| Constant-balance convention (general statements) | (PDF pp. 169–170, 181–182, 207, 221; md sec-148, sec-164, sec-190, sec-211) |
| Table A7 scope = Equations A46 models; no domestic-time row; SQ-1/SQ-2 | (PDF p. 219; md sec-209) |
| Hedge adjustment: accounting hedges; proposed B.2/B.3; Eqs A49–A51; no renewals/terminations | (PDF pp. 220–223; md sec-210–212) |
| Hedge questions A181–A187 | (PDF pp. 223–224; md sec-213) |
| Boundaries: other domestic deposits (v.a(8)); foreign deposits incl. time (v.a(9)) | (PDF pp. 211, 215–216; md sec-197, sec-201–202) |
| Proposed-suite ÷4 / N/360 appear only in trading-NII, securities, hedge contexts; current-suite fn 54 (sub debt) states an annual-rate ÷4 | (PDF pp. 225; 191, 196, 201; 222; 155; md sec-215; sec-177/181/185; sec-211; fn 54 at md line 5338) |
| Current 2025 model: Eq A10 regression; component definition; fn 27 codes; questions A43–A49 | (PDF pp. 75–80, 35–39, 141–144; md sec-65, sec-19–21, sec-126, lines 1620–1636) |
| PID-1…PID-6 project decisions; D-004 convention | User confirmations 2026-07-17; `handbook/open-questions.md` decision log; brief §0.1 |

---

### Chapter completion checklist (retain until the Step 5 independent review passes)

- [x] Status banner present; no adoption language anywhere.
- [x] Every material statement labeled [FACT]/[INT]/[CODE]/[OQ]/[PID]/[ALT]; unknowns stated, never defaulted.
- [x] Equation A44 verified against the PDF page image; quoted passages verified (integrity review 2026-07-16 + page images 2026-07-17).
- [x] Conversion artifacts: none in v.a(7); source quirks (SQ-1/SQ-2/SQ-4) preserved verbatim with [INT] notes.
- [x] Launch-point vs. projection timing unambiguous for every input and intermediate (§§4–5).
- [x] Constancy register covers every input and parameter (§6).
- [x] Units and rate conversions explicit at every step (÷3 months→quarters; ÷4 final step only, [PID-6], never attributed to the Fed).
- [x] No production Python; no confidential material (public line items and a generic MEV column label only).
- [x] Open questions filed with IDs (§13); review state REVIEWED — Step 5 run and Step 6 corrections applied 2026-07-17.

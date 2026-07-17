# Source Brief — Interest Expense on Domestic Time Deposits (`ie_dom_time_dep`)

> **STATUS: Proposed for the 2026 stress test — public-comment stage, NOT adopted.**
> Component: **Interest Expense on Domestic Time Deposits**, Section v.a(7) (PDF pp. 209–211; md sec-193–196). Model type per Table A6: **Structural** (PDF pp. 168–169; md sec-148).
> Deliverable: Phase 2, component 1 of 5, workflow **Steps 1–3 (source brief, revised per user feedback of 2026-07-17)**. Review state: **APPROVED (2026-07-17) — working basis for the Step 4 chapter `handbook/models/interest-expense/deposits/ie_dom_time_dep.md`**. This brief is not the final handbook chapter.
> Integrity flags: SQ-4 (Questions intro wording, PDF p. 211); SQ-1/SQ-2 (Table A7 quirks, relevant only to the non-applicability note in §9); December 2025 revision item for p. 209 ("end of quarter" → "average", PDF pp. 4–5; md sec-0). Conversion artifacts in v.a(7): none.
> Verification: PDF pp. 6, 172, 209–211 opened and confirmed 2026-07-17; all other citations rely on `inventory/source-integrity-review.md` (2026-07-16). Citation format: (PDF p. N; md sec-M).

---

## 0. Classification legend and project-context register

Every material statement in this brief carries exactly one of six labels:

| Tag | Class | Meaning |
|---|---|---|
| **[FACT]** | FED SOURCE METHODOLOGY | Directly stated in the Fed PPNR source document; always cited |
| **[PID]** | PROJECT IMPLEMENTATION DECISION — USER CONFIRMED | Confirmed for this project by the user on 2026-07-17; never attributable to the Federal Reserve unless the source independently states the same thing |
| **[INT]** | INTERPRETATION | A reading the source does not state verbatim; the basis is stated |
| **[CODE]** | CODING CONSIDERATION | Generic implementation guidance for the future Python phase; non-normative |
| **[OQ]** | OPEN QUESTION | Linked to `handbook/open-questions.md` by ID |
| **[ALT]** | ALTERNATIVE DISCUSSED BUT NOT PROPOSED | Discussed by the Fed in the source but explicitly not part of the proposed model |

Project-specific mappings never alter the description of the Fed model itself: §§1–4, 6.1, 7, 9, 11 describe the Fed methodology; PIDs enter only where an input must be physically sourced.

### 0.1 Project implementation decision register (user-confirmed 2026-07-17)

| ID | Decision | Fed-source status of the same point |
|---|---|---|
| **PID-1** | Domestic time-deposit balance = **FR Y-14Q Schedule G item 34E**; use the launch-point value as the projected balance; hold it flat across all nine projection quarters | The source states expense uses "the average balance on domestic time deposits as reported in the FR Y-14Q" but **names no line item** (PDF p. 209; md sec-193). "34E" appears nowhere in the source (full-document search, 2026-07-17). Balance flatness is consistent with the general constant-balance convention but is not restated in v.a(7) ([INT], §6.2) |
| **PID-2** | Initial rate Rate(b,0) = **FR Y-14Q Schedule G item 42E** at the launch point (PQ0), seeding the Equation A44 recursion | **Independently source-stated [FACT]** (PDF p. 209; md sec-194) — the PID concurs with the source |
| **PID-3** | Schedule G item 71 (Weighted Average Life) is reported in **months** | Unit **not stated** in the PPNR source; this resolves OQ-008 **for this project only** |
| **PID-4** | WAL_quarters(b) = WAL_months(b) / 3; **ρ_b = 1 / WAL_quarters(b) = 3 / WAL_months(b)**; ρ_b is firm-specific and held constant throughout the nine-quarter projection horizon | ρ_b ≡ 1/WAL_b, its repricing-fraction meaning, and its constancy are source-stated [FACT] (PDF p. 209; md sec-194); the month→quarter conversion follows PID-3 and is project context |
| **PID-5** | Scenario source: the project MEV workbook contains a Date column and one column per MEV; select the series by **exact column name "USD 1Y Treasury"**; align it to the nine projection quarters | The model's scenario input is the 1-year Treasury yield [FACT] (PDF p. 209); the source says **nothing** about physical scenario storage — the MEV workbook layout is a project statement, not a description of how the Federal Reserve stores its scenario data |
| **PID-6** | **Annualized-rate convention and quarterly conversion.** All interest rates used in this project are annualized rates. Quarterly dollar expense divides the annualized projected rate by four at the final step only: **Expense(b,t) = AverageBalance(b,t) × Rate(b,t) / 4**, with the flat item 34E average balance (PID-1). Equation A44 operates entirely in annualized-rate units — Treasury1y(t) and Rate(b,t−1) are never divided by four inside the recursion. Simple nominal quarterization, not an effective compounded quarterly-rate conversion. Resolves OQ-006 **for this project only** | "multiplying the modeled rate by the average balance" is source-stated [FACT] (PDF p. 209; md sec-193); the rate basis and the ÷4 quarterly conversion are **not stated by the source for this component** — its explicit ÷4 statements appear only elsewhere (§7.9). Never presented as a Federal Reserve statement |

The PID register records public-form line items and a generic scenario-column label supplied by the user; it contains no confidential workbook content, formulas, sheet names, or firm data.

**No new model is proposed anywhere in this brief.** The model documented is the Federal Reserve's proposed structural model under Equation A44, unchanged. The Call Report maturity-profile approach (PDF pp. 210–211) is recorded under [ALT] in §11.2 only and is not incorporated into the proposed model workflow.

---

## 1. Executive summary

**What the model projects.** [FACT] The model projects the interest expense a firm pays on its domestic time deposits, one value per firm per projection quarter, over the nine-quarter projection horizon of the supervisory stress test (horizon: PDF p. 6; md sec-2). It does so in two stages: it first projects the *rate* paid on domestic time deposits with a recursion (Equation A44), then computes dollar expense by multiplying the modeled rate by the average balance on domestic time deposits as reported in the FR Y-14Q (PDF p. 209; md sec-193).

**Why the component exists economically.** [FACT — current-suite background] Domestic time deposits (certificates of deposit and similar) are "fixed at an interest rate for a set term before they can be withdrawn without penalty"; offered rates track short-term market rates because those represent depositors' opportunity cost, and time deposits are "generally considered a stable source of funding" (current-suite section iv.i(1), PDF pp. 75–79; md sec-65). Interest expense on these deposits is one of six interest-expense components of PPNR net interest income (PDF pp. 6–8; md sec-2). The current 2025 suite projects this component with a panel regression; the proposed 2026 suite replaces it with a structural model (Table A6, PDF pp. 168–169; md sec-148).

**Broad methodology.** [FACT] The proposed model assumes a fixed fraction of the firm's time-deposit portfolio matures each quarter. Maturing balances are replaced with new funding priced at a reference rate — the 1-year Treasury yield — while the remaining fraction keeps the rate paid in the previous quarter (PDF p. 209; md sec-193). The maturing fraction is ρ_b ≡ 1/WAL_b, computed from the firm-reported Weighted Average Life (Schedule G item 71) and held constant; the rate path starts from the firm's launch-point average rate (Schedule G item 42E). The model has **no estimated coefficients, no deposit beta, no regime switching, and no rate floor** (§§5, 7, 9; facts of absence, PDF pp. 209–211).

**Final output per projection quarter.** [FACT] A dollar interest-expense amount per firm per scenario per projection quarter, equal to the modeled rate times the average balance (PDF p. 209). [PID-1] The balance is the launch-point FR Y-14Q Schedule G item 34E value, held flat for all nine quarters. [PID-6] Under the project's user-confirmed annualized-rate convention, the quarterly dollar expense is AverageBalance(b,t) × Rate(b,t) / 4, with the ÷4 applied only at this final step; the PPNR source itself does not state this conversion for the component (§7.9), so OQ-006 is resolved for project implementation, not by the source.

---

## 2. Component scope and reporting definition

### 2.1 Component identity

- [FACT] Exact Federal Reserve component name: **"Interest Expense on Domestic Time Deposits"** — section heading v.a(7) (PDF p. 209; md sec-193).
- [FACT] Table A6 lists "Domestic time deposits" under "Structural models for interest expense" with model type "Structural" (PDF pp. 168–169; md sec-148).
- [FACT] It is one of the 10 components for which the Board proposes structural models: "interest expense on domestic time deposits" appears in the v.a component list (PDF p. 172; md sec-149; page image verified 2026-07-17).
- Coding-friendly identifier (secondary, per `inventory/model-inventory.md` record #7): **`ie_dom_time_dep`**. This file's name (`ie_dom_time_dep.source-brief.md`) carries the canonical model ID, renamed in the 2026-07-17 repository reorganization; the model ID is unchanged.

### 2.2 Included and excluded categories

- [FACT] Included: the firm's **domestic time deposit portfolio as a single aggregate**. The proposed section applies no size-band, product, or maturity segmentation (PDF pp. 209–210; md sec-193–195; absence of any segmentation language).
- [FACT] Excluded — foreign time deposits: modeled inside **Interest Expense on Foreign Deposits** (v.a(9)), which uses Schedule G line items 44B (foreign deposits–time rate) and 35B (foreign time balance) (PDF pp. 215–216; md sec-201–202).
- [FACT] Excluded — other domestic non-time deposits (money market, savings, transaction accounts): modeled in **Interest Expense on Other Domestic Deposits** (v.a(8)) (PDF p. 211; md sec-197).
- [FACT — current-suite context only] The proposed section does not restate a dollar-threshold definition of the component. The current-suite section defines it as "interest expense on domestic time deposits of \$250,000 or less plus time deposits of more than \$250,000," sourced for the current models from FR Y-9C variable codes BHCKHK03 + BHCKHK04 (expense) with balances BHCBJ474 + BHODJ474 + BHCBHK29 + BHODHK29 (footnote 27; B.ii.d mapping tables) (PDF pp. 75–79 and 35–39; md sec-65, sec-19–21, fn line 5284; md-verified — current-suite pages not individually re-opened, per the integrity review's COMPARISON policy). The **proposed** model's reporting basis is FR Y-14Q, not FR Y-9C.

### 2.3 Reporting basis of the proposed model

| Quantity | Source statement | Line item | Label |
|---|---|---|---|
| Rate (dependent variable) | "the domestic time deposit rate as reported in the FR Y-14Q" (PDF p. 209) | Schedule G item **42E** "(Time Deposits)" for the initial value (PDF p. 209) | [FACT] |
| Weighted Average Life | "as reported by firms in the FR Y-14Q, Schedule G, line item 71 (Domestic Deposits – Time)" (PDF p. 209) | Schedule G item **71** | [FACT] |
| Balance | "the average balance on domestic time deposits as reported in the FR Y-14Q" (PDF p. 209) | **Not identified in the source** (fact of absence; "34E" appears nowhere in the document) | [FACT] absence |
| Balance — project mapping | — | Schedule G item **34E**, launch-point value, flat | **[PID-1]** |

- [FACT] The word "average" in the balance sentence is a **December 2025 revision**: "On page 209, … the term 'end of quarter' was revised to 'average'" (PDF pp. 4–5; md sec-0, line 272).

### 2.4 Quantity type

[FACT] The component output is a **calculated dollar expense flow**. The model's dependent variable is a **rate**; the balance is a level input; the product gives the expense (PDF p. 209; md sec-193). This brief keeps rates, balances, and dollar expenses strictly distinct (see §7.9 for the quarterly-conversion convention).

### 2.5 Terminology differences

- [FACT] The source uses **"jump-off quarter"** (p. 209) and **"at lift-off"** (p. 210) for the same quarter, within this one section. The handbook standardizes on **launch point, PQ0** (decision D-005).
- Coding-friendly names are given per input in §5; Fed terms are always primary.

---

## 3. Model classification

- **Classification: structural model (direct calculator).** [FACT] Table A6 assigns "Structural" (PDF pp. 168–169); the section opens "The Board proposes a structural model as an alternative specification for interest expense on domestic time deposits" (PDF p. 209; md sec-193). [INT] "Alternative specification" here means alternative to the current panel regression (per Question A177's comparison framing, PDF p. 211) — not an optional variant within the proposed suite.
- **Why the classification applies.** [FACT] Proposed structural models "avoid statistical estimation, making variability of projections over stress testing cycles fully explainable by balances reported for each bank and the variation in the interest rate scenario paths" (PDF pp. 172–173; md sec-149). [FACT — background] The framework defines structural models as directly calculating projections from economic relationships, contractual terms, and "the asset or liability composition of each firm at the date of lift-off" (PDF p. 32; md sec-14).
- **Parameter character.** [FACT] All firm-varying quantities (Rate(b,0), WAL_b and hence ρ_b) are **firm-specific and fixed at the launch point**; ρ_b "remains constant throughout the projection" (PDF p. 209). There are **no industry-level parameters, no scenario-direction (up/down) parameters, and no estimated coefficients** for this component (facts of absence; Table A7 serves the Equation A46 models — §9).
- **Scenario dependence.** [FACT] Enters only through the 1-year Treasury yield path (PDF p. 209).
- **Directly calculated vs statistically estimated.** [FACT] Directly calculated; nothing is estimated.

---

## 4. Dimensions and time conventions

### 4.1 Dimension register

| Dimension | Applies? | Basis | Label |
|---|---|---|---|
| Firm `b` | Yes | Eq A44 subscripts; firm-reported inputs (PDF p. 209) | [FACT] |
| Scenario / exercise | Yes | The stress test projects under supervisory scenarios (PDF p. 6; md sec-2); Eq A44 is evaluated per scenario path. The section itself carries no scenario index | [INT] |
| Projection quarter `t` = 1…9 | Yes | "nine-quarter projection horizon" (PDF p. 6; md sec-2; page image verified 2026-07-17) | [FACT] |
| Deposit segment | **No** | Single aggregate portfolio; no segmentation appears in v.a(7) (PDF pp. 209–211) | [FACT] absence |

### 4.2 Time conventions

- **Launch point (PQ0).** [FACT] The initial rate is "the average rate paid on domestic time deposits in the jump-off quarter" (PDF p. 209). [INT] PQ0 = the last quarter before the projection horizon (launch point, decision D-005), per the framework's usage ("$q0$ represents the lift-off quarter", current-suite structural sections, PDF pp. 145–152; md line 2865) and the handbook convention.
- **Historical reference period.** [FACT] None — this model uses no historical estimation window (fact of absence; contrast the 2020:Q2–2021:Q4 windows used by v.a(8) spreads and the v.d(2) regression).
- **Projection horizon.** [FACT] Nine quarters (PDF p. 6).
- **Average vs end-of-quarter.** [FACT] The initial rate is an **average rate** in the jump-off quarter (PDF p. 209). The balance is an **average balance** — December 2025 revision replaced "end of quarter" (PDF pp. 4–5; p. 209).
- **Contemporaneous vs lagged.** [FACT] Treasury1y_t is contemporaneous with projection quarter t; Rate(b,t−1) is the one-quarter lag; the t=1 evaluation uses Rate(b,0) from item 42E (PDF p. 209).
- **Annual vs quarterly rate conventions.** [FACT] The repricing *period* is a quarter ("the fraction of the portfolio that reprices every period (quarter)", PDF p. 209). [FACT] The *basis* of the rates is not stated by the source. [PID-6] Project convention: all rates are annualized; the recursion runs in annualized units and ÷4 applies only at the final expense step (§7.9).

### 4.3 Timing register

| Input / term | Quarter taken from | Label |
|---|---|---|
| Rate(b,0) — item 42E average rate | PQ0 (jump-off quarter) | [FACT] (PDF p. 209) |
| WAL_b — item 71 | As-reported; the as-of quarter is not stated — taken at PQ0, consistent with the other launch-point inputs | [INT] |
| ρ_b = 1/WAL_b | Derived once at PQ0; constant for t = 1…9 | [FACT] constancy (PDF p. 209); [PID-4] formula |
| Treasury1y(t) | Contemporaneous projection quarter t | [FACT] (PDF p. 209) |
| Rate(b,t−1) | Prior projection quarter; t=1 uses Rate(b,0) | [FACT] (PDF p. 209) |
| Balance | Launch-point value (item 34E), flat for t = 1…9 | **[PID-1]**; source names neither item nor quarter ([FACT] absence) |
| Expense(b,t) | Computed at each projection quarter t | [FACT] product form (PDF p. 209); ÷4 conversion [PID-6] |

---

## 5. Inputs

### 5.1 Input register — inputs the model uses

| # | Input | Fed terminology | Coding-friendly name | Definition | Source | Unit | Frequency | Dimensions | Timing | Nature | Constant over horizon? | Label |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Domestic time-deposit balance | "average balance on domestic time deposits as reported in the FR Y-14Q" (PDF p. 209) | `domestic_time_deposit_balance` | Average balance of the firm's domestic time deposits | FR Y-14Q Schedule G item **34E** [PID-1]; the source names no item ([FACT] absence) | USD (level) | Reported quarterly; used once | b | Launch point; held flat t = 1…9 | Observed | **Constant** [PID-1] | [FACT] role; [PID-1] mapping |
| 2 | Initial rate | "the average rate paid on domestic time deposits in the jump-off quarter … Schedule G, line item 42E (Time Deposits)" (PDF p. 209) | `domestic_time_deposit_rate_launchpoint` | Rate(b,0), the recursion seed | FR Y-14Q Schedule G item **42E** | Annualized rate [PID-6]; basis unstated in source ([FACT] absence); scale normalization §12.6 [CODE] | Once | b | PQ0 | Observed | n/a (seed value) | [FACT]; [PID-2] concurs |
| 3 | Weighted Average Life | "the Weighted Average Life of the portfolio … Schedule G, line item 71 (Domestic Deposits – Time)" (PDF p. 209) | `domestic_time_deposit_wal_months` | WAL of the domestic time-deposit portfolio | FR Y-14Q Schedule G item **71** | **Months** [PID-3] | Once | b | PQ0 [INT] | Observed | Constant (enters only via ρ_b) [FACT] | [FACT] source; [PID-3] unit |
| 4 | Repricing fraction | "ρ_b ≡ 1/WAL_b … the fraction of the portfolio that reprices every period (quarter)" (PDF p. 209) | `repricing_fraction_rho` | Share of portfolio repricing each quarter | Derived: ρ_b = 1/WAL_quarters(b) = **3/WAL_months(b)** [PID-4] | Dimensionless fraction per quarter | Derived once | b | PQ0 → all t | Derived | **Constant** — "remains constant throughout the projection" [FACT] (PDF p. 209) | [FACT]; [PID-4] conversion |
| 5 | 1-year Treasury yield | "$Treasury1y_t$: is the 1-year Treasury yield at quarter $t$" (PDF p. 209) | `usd_1y_treasury` | Scenario reference rate for repriced balances | Project MEV workbook, exact column name **"USD 1Y Treasury"**, aligned to the nine projection quarters [PID-5]; the source does not describe scenario storage ([FACT] absence) | Annualized rate [PID-6]; scale normalization §12.6 [CODE] | Quarterly | scenario × t | Contemporaneous | Scenario-projected | Varies with scenario path | [FACT] role; [PID-5] sourcing |

### 5.2 Inputs mandated for review that this component does not use

Recorded explicitly for 1:1 traceability; each row is a [FACT] about the source.

| Input | Status for this component | Evidence |
|---|---|---|
| **3-month Treasury yield** | **NOT USED.** Equation A44's only scenario input is the 1-year Treasury yield | Eq A44 where-list (PDF p. 209; md sec-194). The 3-month Treasury drives the sibling deposit models' regimes and floors (v.a(8)–(9), PDF pp. 211–216) and other calculators — not this model |
| **Deposit beta parameters** | **NOT USED.** No beta appears in Eq A44; the repricing weight ρ_b is a maturity-profile fraction (1/WAL), not a rate-passthrough beta | PDF p. 209 (Eq A44); betas are defined for the non-ELB regime of other domestic deposits, Eq A46 (PDF p. 213; md sec-199) |
| **Table A7 parameters** | **NOT APPLICABLE.** Table A7 "Median Betas for Proposed Deposit Models (Equations A46)" covers Other Domestic (MMA / Savings / Other) and Foreign (Non-time / Time) only; **no domestic-time row exists** | PDF p. 219; md sec-209. Quirks SQ-1/SQ-2 noted in §9 |
| **Hedge-adjustment inputs** | **NONE IN THIS MODEL.** Eq A44 contains no hedge term; the cross-cutting adjustment (v.c) is a separate calculation | PDF pp. 209–211 (absence); PDF pp. 220–223 (v.c). See §7.10 and OQ-005 |
| **Upstream model outputs** | **NONE.** No other model's output enters (contrast: the loans model consumes credit-loss model rates) | PDF pp. 209–211 (absence) |

---

## 6. Assumptions

### 6.1 Assumptions stated by the Federal Reserve — [FACT]

1. **Constant repricing share.** "A constant percentage of the portfolio is assumed to be repriced every period. This assumption abstracts from the heterogeneity of the rate and maturity profile in a firm's time deposit portfolio. Using only one piece of information about maturity profiles, the Weighted Average Life, necessitates this simplifying assumption." (PDF p. 210; md sec-195)
2. **Re-origination pricing at the 1-year Treasury; no market power.** "All re-originated time deposits are priced at the 1-year Treasury yield. In this model, firms do not have market power in time deposit pricing. The only difference in the level of rates throughout the projection period comes from the rate paid on domestic time deposits at lift-off and the firm-specific Weighted Average Life." Pricing all re-originations at the 1-year Treasury "also ignores the heterogeneity in rates that comes with the origination of new time deposits." (PDF p. 210; md sec-195)
3. **Constant ρ.** The repricing fraction "is reflective of the portfolio's maturity profile and remains constant throughout the projection." (PDF p. 209; md sec-194)
4. **General structural-model framing (background).** Structural models require assumptions "e.g., regarding the re-origination of maturing instruments" (PDF p. 33; md sec-15).

### 6.2 Assumptions required for implementation — separated from Fed statements

| Topic | Assumption | Label |
|---|---|---|
| Balance behavior | Balance = launch-point Schedule G item 34E value, flat across all nine projection quarters | **[PID-1]**. [INT] Consistent with the general constant-balance convention — "tie projections more closely to banks' actual assets and liabilities at the beginning of the projection horizon" (PDF pp. 169–170; md sec-148); "the stress test assumes constant balances" (PDF pp. 181–182; md sec-164); "The stress test assumes constant balances for all firms" (PDF p. 207; md sec-190); "the overall fixed balance sheet assumption" (PDF p. 221; md sec-211) — but not restated inside v.a(7) |
| Deposit composition | Single aggregate portfolio; no composition dimension exists to hold constant | [FACT] absence (PDF pp. 209–210) |
| Repricing / maturity / renewal | Memoryless constant-fraction maturity: every quarter the same fraction ρ_b matures and reprices; contractual terms are not tracked | [FACT] (assumption 1 and the limitation, PDF p. 210) |
| Deposit beta behavior | Not applicable — no beta in this model | [FACT] absence (§5.2) |
| Rate floors | **No floor, cap, or other constraint is stated** anywhere in v.a(7). Contrast: v.a(8) applies an assumed floor (PDF pp. 211–213) | [FACT] absence; validation only ([CODE] §12.2) |
| Scenario-rate passthrough | The maturing fraction reprices fully to the 1-year Treasury (passthrough of 1 on that fraction; no beta damping); the non-maturing fraction has zero contemporaneous passthrough | [INT] — restatement of the [FACT] mechanism (PDF p. 209) |
| Firm heterogeneity | Enters only through Rate(b,0) and WAL_b | [FACT] (PDF p. 210) |
| Missing or insufficient data | The source states no fallback; **no fallback treatment is invented in this project** — invalid inputs surface as validation failures with treatment UNDECIDED | User instruction 2026-07-17; [CODE] §12.2 |
| Interest-rate hedges | None inside Eq A44; possible later incorporation via the separate cross-cutting adjustment | [FACT] absence + [OQ-005]; §7.10 |
| Constancy from the launch point | ρ_b constant [FACT]; balance constant [PID-1]; no other time-varying firm inputs exist | as labeled |
| Annual-to-quarterly conversion | WAL: months → quarters via ÷3 [PID-3/PID-4]. Rates: annualized project-wide; quarterly dollar expense = annualized rate ÷ 4 at the final step only (simple nominal quarterization, not compounded) | [PID-3/PID-4] and [PID-6] |

---

## 7. Calculation methodology

### 7.1 Calculation sequence in plain English

1. At the launch point, read the firm's average time-deposit rate (item 42E), Weighted Average Life (item 71), and balance (item 34E per PID-1).
2. Convert WAL from months to quarters and form the repricing fraction ρ_b [PID-3/PID-4].
3. For each projection quarter, blend the scenario 1-year Treasury yield (weight ρ_b) with the previous quarter's modeled rate (weight 1 − ρ_b) — Equation A44.
4. Multiply the modeled rate by the flat balance to obtain the expense basis for the quarter [FACT product form; PID-1 balance].
5. Convert to a quarterly dollar amount by dividing the annualized rate by four — user-confirmed convention [PID-6] (§7.9). The cross-cutting hedge adjustment, if any, is computed separately (§7.10).

### 7.2 Equation A44 (verbatim)

[FACT] (PDF p. 209; md sec-194; verified against the PDF page image 2026-07-16 and re-confirmed 2026-07-17):

**Equation A44** – Interest Expense on Domestic Time Deposits Rate Projection

$$Rate_{b,t} = \rho_b * Treasury1y_t + (1 - \rho_b) * Rate_{b,t-1}$$

*where* (verbatim from the source):

- $Rate_{b,t}$ is the rate paid on domestic time deposits by firm $b$ at quarter $t$;
- $\rho_b \equiv \frac{1}{WAL_b}$: is the fraction of the portfolio that reprices every period (quarter). $WAL_b$ is the weighted average life of domestic time deposits for firm $b$; and
- $Treasury1y_t$: is the 1-year Treasury yield at quarter $t$.

### 7.3 Symbol definitions with coding-friendly names

| Symbol (Fed) | Coding-friendly name | Definition | Label |
|---|---|---|---|
| $Rate_{b,t}$ | `dtd_rate[b, t]` | Rate paid on domestic time deposits by firm b at quarter t | [FACT] |
| $Rate_{b,0}$ | `domestic_time_deposit_rate_launchpoint` | Launch-point average rate, Schedule G item 42E | [FACT] |
| $\rho_b$ | `repricing_fraction_rho` | 1/WAL_b; fraction repricing each quarter; constant | [FACT]; [PID-4] months→quarters |
| $WAL_b$ | `domestic_time_deposit_wal_months` (reported); `wal_quarters` (derived) | Weighted Average Life, Schedule G item 71 | [FACT]; [PID-3] months |
| $Treasury1y_t$ | `usd_1y_treasury[t]` | 1-year Treasury yield at projection quarter t | [FACT]; [PID-5] MEV column |
| (balance) | `domestic_time_deposit_balance` | Average balance on domestic time deposits | [FACT] role; [PID-1] item 34E |
| (expense) | `dtd_interest_expense[b, t]` | AverageBalance × modeled rate ÷ 4 | [FACT] product form; [PID-6] ÷4 |

### 7.4 Timing of every term

Per the §4.3 timing register: Treasury1y(t) contemporaneous; Rate(b,t−1) lagged one quarter; ρ_b and the balance fixed at the launch point; recursion runs t = 1…9 with Rate(b,0) as seed. [FACT] for every rate term (PDF p. 209); [PID-1] for the balance.

### 7.5 Role of the 3-month Treasury rate

[FACT] **None in this model.** The only scenario rate in Equation A44 is the 1-year Treasury yield (PDF p. 209). The 3-month Treasury yield belongs to the sibling deposit-expense models (regime trigger, rate driver, and floor in v.a(8)–(9), PDF pp. 211–216) and to other structural calculators — it must not be wired into this component.

### 7.6 Role and source of the deposit beta

[FACT] **None.** Equation A44 contains no beta; the weight on the scenario rate is ρ_b, a maturity-profile repricing fraction (1/WAL), not an estimated or firm-reported rate-passthrough beta. Deposit betas (firm-reported items 79A–81B, 83A–84B; Table A7 medians) serve Equation A46 for other domestic deposits and, by reference, foreign deposits (PDF pp. 213, 215–216, 219). [INT] Interpretive contrast: in a beta model the deposit rate moves by β × Δ(market rate); here the modeled rate is a convex combination of the *level* of the 1-year Treasury and the prior rate — economically a gradual-repricing mechanism, not a passthrough coefficient.

### 7.7 Calculation of the projected deposit rate

The recursion, documented in the user-confirmed presentation form:

```text
Rate(b,t) = rho_b * Treasury1y(t) + (1 - rho_b) * Rate(b,t-1)
```

with:

- Rate(b,0) sourced from Schedule G item 42E [FACT; PID-2 concurs];
- rho_b derived from item 71 after converting months to quarters: rho_b = 3 / WAL_months(b) [FACT definition; PID-3/PID-4 conversion]; **rho_b is firm-specific and held constant throughout the nine-quarter projection horizon** [FACT constancy, PDF p. 209];
- Treasury1y(t) sourced from the MEV column "USD 1Y Treasury" [PID-5].

Unrolled for the first quarters (illustration, [INT] — arithmetic restatement only):

- Rate(b,1) = ρ_b·Treasury1y(1) + (1 − ρ_b)·Rate(b,0)
- Rate(b,2) = ρ_b·Treasury1y(2) + (1 − ρ_b)·Rate(b,1), … through t = 9.

[INT] Algebraic property (not a Fed statement): Rate(b,t) is an exponentially weighted average of the current and past scenario 1-year Treasury yields and the launch-point rate, converging toward the scenario path at speed ρ_b per quarter.

### 7.8 Floors, caps, and other constraints

[FACT] **None are stated** in v.a(7) — no floor, no cap, no non-negativity condition, no ELB regime (PDF pp. 209–211; contrast the assumed floor in v.a(8), PDF pp. 211–213). [CODE] §12.2 records a validation monitor only; no constraint is added to the model.

### 7.9 Conversion of projected rate and balance into quarterly dollar expense — RESOLVED FOR PROJECT IMPLEMENTATION [PID-6]

- [FACT] "Interest expense on domestic time deposits is computed by multiplying the modeled rate by the average balance on domestic time deposits as reported in the FR Y-14Q." (PDF p. 209; md sec-193; "average" per the December 2025 revision, PDF pp. 4–5)
- [FACT — absence, preserved] The source does **not** state the rate basis or any annual-to-quarterly conversion for this component. Within the proposed 2026 suite, its explicit conversion statements appear only elsewhere: ÷4 in the trading-NII data construction (PDF p. 225; md sec-215) and in the securities coupon-accrual formulas (PDF pp. 191, 196, 201; md sec-177/181/185), and N/360 day count on the hedge legs (PDF p. 222; md sec-211). In the current 2025 suite, footnote 54 (subordinated debt) states "The coupon rate is always an annual rate divided by four … coupon rates are always stated as annualized rates" (PDF p. 155; md line 5338) — a current-suite parallel that supports, but does not state, the convention for this component (identified in the Step 5 review, 2026-07-17).

**[PID-6] User-confirmed project convention (2026-07-17).** All interest rates used in this project are annualized rates. When an annualized projected rate is used to calculate interest expense for one quarter, the annualized rate is divided by four:

```text
Expense(b,t) = AverageBalance(b,t) * Rate(b,t) / 4
```

with AverageBalance(b,t) = the flat average domestic time-deposit balance from Schedule G item 34E, identical for all nine projection quarters [PID-1].

[PID-6] Scope of the division by four — the recursion is untouched:

- Treasury1y(t) is **not** divided by four before entering Equation A44;
- Rate(b,t−1) is **not** divided by four inside the recursion;
- Equation A44 operates entirely in annualized-rate units;
- division by four occurs **only** at the final conversion from projected annualized rate to quarterly dollar expense;
- the convention is simple nominal quarterization, **not** an effective compounded quarterly-rate conversion.

This convention is a PROJECT IMPLEMENTATION DECISION — USER CONFIRMED. It is never presented as a Federal Reserve statement; OQ-006 is accordingly **resolved for project implementation** (§13), while the source-side absence above remains on record.

### 7.10 Interaction with the interest-rate-risk hedge adjustment

- [FACT] Equation A44 contains **no hedge term**, and v.a(7) does not mention hedges (PDF pp. 209–211).
- [FACT] Section v.c proposes a **separate, cross-cutting** adjustment for qualified *accounting* hedges, computed from hedge-position data the Board proposes to collect via revised FR Y-14Q Schedule B.2 (a companion Schedule B.3 is proposed in the securities sections — PDF pp. 192, 197, 203; md lines 3854, 3933, 4013): Hedge NII Impact per projection quarter = accrued interest income − accrued interest expense on the hedge legs (Equations A49–A51, N/360 day count), with terminated-hedge effects amortized over the remaining life of the hedged item; hedge renewals/terminations during the horizon are not modeled, for consistency with the fixed balance-sheet assumption (PDF pp. 220–223; md sec-210–212).
- **The base Equation A44 model is kept separate from the cross-cutting hedge adjustment.** This brief does **not** state that hedges have no effect on the final projected expense — hedge effects may be incorporated later through that separate adjustment. [OQ → **OQ-005**] How the adjustment is allocated to specific components (including this one) is unresolved.

---

## 8. Step-by-step projection workflow

Numbered workflow from source inputs to final output. No pseudocode; no production Python.

**Stage A — Preprocessing (launch point)**

1. Extract, for each firm b at the launch point PQ0: item 42E average rate (`domestic_time_deposit_rate_launchpoint`), item 71 WAL (`domestic_time_deposit_wal_months`), item 34E balance (`domestic_time_deposit_balance`) [FACT for 42E/71; PID-1 for 34E].
2. Validate inputs (checks in §12.2): missing WAL; zero or negative WAL; WAL implying ρ_b outside the economically valid range; missing starting rate; missing balance. **A validation failure surfaces as an error; no fallback is applied** (treatment undecided — user instruction).
3. Convert WAL to quarters: WAL_quarters(b) = WAL_months(b) / 3 [PID-3/PID-4].
4. Compute ρ_b = 1 / WAL_quarters(b) = 3 / WAL_months(b); ρ_b is firm-specific and constant for all nine projection quarters [FACT constancy; PID-4 formula].
5. Load the scenario series: from the MEV workbook (Date column + one column per MEV), select the column named exactly **"USD 1Y Treasury"** [PID-5].
6. Align the series to the nine projection quarters PQ1…PQ9 (Date ↔ projection-quarter mapping must be exact and complete) [PID-5; CODE §12.2].

**Stage B — Rate recursion**

7. Set the seed: Rate(b,0) = item 42E value [FACT].
8. For t = 1…9 in order: Rate(b,t) = ρ_b·Treasury1y(t) + (1 − ρ_b)·Rate(b,t−1) [FACT — Eq A44]. Store the nine-quarter rate path. (Order matters; each quarter depends on the previous one.)

**Stage C — Expense calculation**

9. For each t: form the annualized expense basis Rate(b,t) × AverageBalance(b,t), with AverageBalance(b,t) flat at the launch-point item 34E value [FACT product form; PID-1]. Rate(b,t) is still an annualized rate at this step [PID-6].
10. Convert to the quarterly dollar expense: QuarterlyExpense(b,t) = AverageBalance(b,t) × Rate(b,t) / 4 [PID-6]. The ÷4 applies only here — never inside Stage B — and is simple nominal quarterization, not compounding. [CODE] Implement as a named, documented final-step transform, not a hidden literal.

**Stage D — Cross-cutting hook**

11. Expose the per-quarter expense series for the separate interest-rate-risk hedge adjustment (v.c). No hedge computation occurs inside this model [FACT; OQ-005].

**Final output**

12. Per firm × scenario × projection quarter (nine quarters): projected quarterly dollar interest expense on domestic time deposits per the [PID-6] convention, plus the intermediate annualized rate path Rate(b,1…9) for traceability.

**Item that remains unresolved in this workflow:** the OQ-005 hedge allocation (step 11).

---

## 9. Parameters

### 9.1 Parameter register

| Parameter | Definition | Value / source | Segmentation | Unit | Timing | Published or inferred | Scenario direction | Anomaly |
|---|---|---|---|---|---|---|---|---|
| ρ_b (`repricing_fraction_rho`) | Fraction of portfolio repricing each quarter; ρ_b ≡ 1/WAL_b [FACT, PDF p. 209] | Derived from Schedule G item 71: ρ_b = 3/WAL_months(b) [PID-3/PID-4] | Firm-level; no segments | Fraction per quarter | Fixed at PQ0; constant t = 1…9 [FACT] | Derived from firm-reported data; not a published table value | Direction-independent | None |
| Rate(b,0) | Recursion seed (input, not a free parameter) | Schedule G item 42E [FACT] | Firm-level | Annualized rate [PID-6]; scale §12.6 | PQ0 | Firm-reported | n/a | None |
| Estimated coefficients | — | **None exist for this model** [FACT — structural models "avoid statistical estimation", PDF pp. 172–173] | — | — | — | — | — | — |

### 9.2 Table A7 — explicitly not applicable ([FACT], with quirks recorded)

- [FACT] Table A7 is captioned "Median Betas for Proposed Deposit Models **(Equations A46)**" and contains up/down median betas for exactly five deposit types: Other Domestic Money Market Accounts (0.620/0.645), Other Domestic Savings (0.310/0.335), Other Domestic Other (0.465/0.490), Foreign Non-time (0.890/0.790), Foreign Time (1.000/1.000) (PDF p. 219; md sec-209).
- [FACT] **No row exists for domestic time deposits**, consistent with Equation A44 containing no beta.
- Recorded source quirks (per `inventory/source-integrity-review.md` §8, never silently corrected): **SQ-1** — the "Down" rows display internal parameter names (e.g., `median_beta_dom_mma_deposit_down`) in the Deposit Type column **in the published PDF itself**; **SQ-2** — the caption cites "(Equations A46)" although the betas also serve the foreign-deposits model by reference (PDF p. 215).
- [CODE] Watch item: if a future revision adds a domestic-time beta row to Table A7, that would signal a methodology change for this component relative to the documented proposal.

---

## 10. Dependencies

| Dependency | Type | What depends on it | Status | Label |
|---|---|---|---|---|
| FR Y-14Q Schedule G items 42E, 71 | Upstream data | Rate seed; ρ_b | Named in the source [FACT] (PDF p. 209) | [FACT] |
| FR Y-14Q Schedule G item 34E | Upstream data | Balance for the expense step | Project mapping; source names no item | **[PID-1]** |
| MEV workbook column "USD 1Y Treasury" | Upstream data (scenario) | Treasury1y(t) path, aligned to nine quarters | Project mapping; source describes no storage format | **[PID-5]** |
| Upstream models | — | **None** — no other model's output enters this calculation | Fact of absence (PDF pp. 209–211) | [FACT] |
| PPNR aggregation (Equation A1 identity) | Downstream consumer | Component expense rolls into net interest income / PPNR | PDF pp. 6–8; md sec-2 | [FACT] background |
| Cross-cutting hedge adjustment (v.c) | Cross-cutting | May later adjust interest expense components; contingent on the proposed FR Y-14Q B.2/B.3 collection | PDF pp. 220–223 | [FACT] + [OQ-005] |
| FR Y-14Q Schedule G instructions / MDRM definitions | EXTERNAL DEPENDENCY (document not in `sources/`) | Authoritative definitions and units for items 42E, 71, 34E; previously the blocking resolver for OQ-008 | **Non-blocking for this project**: PID-3 fixes the WAL unit; retained as the eventual authoritative cross-check when the MDRM mapping is built (§12.1) | EXTERNAL DEPENDENCY |
| Supervisory scenario definitions / MEV provenance | EXTERNAL DEPENDENCY | Origin and construction of the 1-year Treasury series | **Non-blocking for this project**: PID-5 fixes the project source; the PPNR document does not describe the physical MEV storage format | EXTERNAL DEPENDENCY |
| Proposed FR Y-14Q B.2/B.3 collection | EXTERNAL DEPENDENCY (proposed, not yet existing) | Hedge adjustment only — not the base model | Blocks only the hedge overlay [OQ-005] | EXTERNAL DEPENDENCY |

**Blocking assessment.** After the user-confirmed context, no dependency and no open question blocks implementation of the base model: the former conversion issue is fixed by [PID-6] (OQ-006 resolved for project implementation), and OQ-005 affects only the separate hedge overlay. **Abstractable through interfaces later** [CODE]: input retrieval via the canonical-name mapping (§12.1); the scenario provider.

---

## 11. Assumptions and limitations stated by the Federal Reserve

This section restates only the Fed's own statements; project observations live in §6.2.

### 11.1 Stated assumptions and limitations — [FACT] (PDF pp. 210–211; md sec-195)

1. **Constant repricing percentage.** "A structural model specification necessarily requires assumptions about future behavior. First, a constant percentage of the portfolio is assumed to be repriced every period. This assumption abstracts from the heterogeneity of the rate and maturity profile in a firm's time deposit portfolio. Using only one piece of information about maturity profiles, the Weighted Average Life, necessitates this simplifying assumption."
2. **1-year Treasury re-origination pricing; no market power.** "A second assumption is that all re-originated time deposits are priced at the 1-year Treasury yield. In this model, firms do not have market power in time deposit pricing. The only difference in the level of rates throughout the projection period comes from the rate paid on domestic time deposits at lift-off and the firm-specific Weighted Average Life. Assuming all re-originations are paid, the 1-year Treasury yield also ignores the heterogeneity in rates that comes with the origination of new time deposits." — [INT] note: the final sentence's comma placement ("are paid, the") reads as "are paid *the* 1-year Treasury yield"; meaning unaffected. Recorded verbatim; flagged as a candidate typography quirk for the integrity review at chapter stage.
3. **Limitation — no richer maturity structure.** "A limitation of the model is that richer maturity structures are not possible. Time deposits have contractual maturities that do not factor into this mechanism. For example, a time deposit balance that reprices to the 1-year Treasury yield in one quarter is as equally likely to be repriced in the following quarter as any other time deposit. There is no mechanism for the time deposit balance to be held for the contractual term."

### 11.2 Alternative discussed but not proposed — [ALT] (PDF pp. 210–211; md sec-195)

[FACT that it is discussed; ALT classification] The Fed notes that Call Reports contain the quantity of domestic time deposits due to mature in 1 quarter, 1 year, and 3 years, and that "the above model can be modified to assume that fixed amounts of time deposits mature each quarter based on maturity profile information," repricing matured balances to a reference rate while unmatured balances keep their original rate. The Fed states this "could address the limitation described above by introducing heterogeneity in time deposit maturities and rates, but as a trade-off it entails further data processing and increased model complexity."

**This alternative is not part of the proposed model and is excluded from the §8 workflow.** It is recorded here only as an alternative the Federal Reserve considered.

### 11.3 General structural-model limitations (background) — [FACT]

Structural models "assume strict relationships based on economic theory or the standing financial contracts held by firms," and granular-data models still require calculation assumptions such as re-origination treatment (PDF p. 33; md sec-15).

### 11.4 Board question for this component — [FACT] (PDF p. 211; md sec-196)

*"Question A177: The Board seeks comment on the proposed approach to model interest expense on domestic time deposits, as compared to the Board's current panel regression model."*

- **SQ-4** (verified on the page image 2026-07-17): the Questions intro reads "this proposed model for interest **income** on domestic time deposits" although this is an expense model; the question itself names the correct component. Recorded verbatim, never corrected in the source.
- [INT] Scenario-sensitivity limitations: beyond the assumptions above, the Fed states no further scenario limitations for this component; the model's scenario sensitivity is fully determined by the 1-year Treasury path and ρ_b.

---

## 12. Coding considerations — [CODE], non-normative

Nothing in this section is Fed methodology. No production Python, no library selection, no package architecture in Phase 1/2.

### 12.1 Canonical input names and future MDRM-based mapping

Eventually, project inputs will be obtained via **MDRM-based lookup rather than hard-coded cell references**. Recorded as a coding consideration only:

- Define canonical model input names.
- Maintain a configurable mapping from each canonical name to: FR Y-14Q schedule; line item; MDRM code; unit; frequency; required transformation.
- Use the mapping to retrieve values from the applicable MDRM reference or source workbook.

Suggested conceptual mappings (user-provided; MDRM codes to be added when the mapping is built — not invented here):

| Canonical input name | Maps to |
|---|---|
| `domestic_time_deposit_balance` | FR Y-14Q Schedule G item 34E |
| `domestic_time_deposit_rate_launchpoint` | FR Y-14Q Schedule G item 42E |
| `domestic_time_deposit_wal_months` | FR Y-14Q Schedule G item 71 |
| `usd_1y_treasury` | MEV column "USD 1Y Treasury" |

No dictionary is built, no MDRM workbook retrieved, and no Python written during this task.

### 12.2 Validation considerations

Required checks (no fallback treatment is defined for any invalid input — failures must surface, not default):

- missing WAL (item 71);
- zero or negative WAL;
- WAL values implying ρ_b outside the economically valid range — ρ_b ∈ (0, 1] requires WAL_months ≥ 3; WAL_months < 3 implies ρ_b > 1 (over-full repricing); extremely large WAL implies ρ_b ≈ 0 (frozen rate) — thresholds configurable, treatment undecided;
- missing starting rate (item 42E);
- missing balance (item 34E).

Additional generic checks: rate-scale normalization before the recursion (§12.6); scenario-series completeness (all nine projection quarters present; unambiguous Date alignment); ordered evaluation of the recursion (t strictly increasing); informational monitor for negative projected rates if a scenario 1-year Treasury path is negative (**no floor is part of the model** — §7.8).

### 12.3 Likely data objects and dimensions

- Firm-input table: one row per firm — balance, launch-point rate, WAL months (plus derived ρ).
- Scenario table: projection-quarter index / Date × MEV columns.
- Outputs: rate path and expense path, dimensioned firm × scenario × projection quarter (suggested order: b, scenario, t).

### 12.4 Configuration candidates

- the final-step ÷4 quarterization is **fixed by [PID-6]** — implement it as a named, documented transform (not a configurable switch and not a hidden literal);
- rate-scale normalization metadata (§12.6);
- ρ_b validity thresholds (§12.2);
- MEV column-name mapping (exact-match "USD 1Y Treasury") and projection-quarter alignment;
- canonical-name → line-item mapping (§12.1).

### 12.5 Reusable calculation pattern

The partial-adjustment recursion `x_t = w·ref_t + (1−w)·x_{t−1}` recurs in the deposit family, but the sibling non-ELB mechanism (Eq A46) operates on rate *changes* scaled by betas with a floor — **not** the same equation. Any shared implementation must keep the two mechanisms distinct and traceable to their own equations.

### 12.6 Rate-scale normalization (separate consideration — user-instructed)

Raw rate inputs may be stored as percentages rather than decimals. **Do not assume whether a raw value such as 5 represents 5 percent or 500 percent without source metadata.** Normalization from stored scale to calculation scale must be metadata-driven (a scale attribute per source field in the §12.1 mapping), applied identically to item 42E and the "USD 1Y Treasury" MEV series before the recursion runs, and validated rather than guessed. This is separate from [PID-6]: PID-6 fixes the ÷4 quarterization; scale normalization concerns only how a stored number maps to the annualized rate.

---

## 13. Open questions

| ID | Status for this component | Statement | Why it matters | Resolution evidence |
|---|---|---|---|---|
| **OQ-006** | **RESOLVED FOR PROJECT IMPLEMENTATION (2026-07-17)** — via user-confirmed annualized-rate convention | Whether the modeled rate (and item 42E) is an annualized rate requiring ÷4 for a quarterly dollar flow | Resolution [PID-6]: all project rates are annualized; Expense(b,t) = AverageBalance(b,t) × Rate(b,t) / 4; the Equation A44 recursion remains entirely in annualized units; ÷4 occurs only in the final quarterly-dollar expense calculation (simple nominal quarterization). **The PPNR source itself still does not explicitly state the quarterly conversion for this component** — the resolution is project implementation context, not a Fed statement | Already resolved for this project; eventual authoritative cross-check: Fed clarification or Schedule G rate-basis definition |
| **OQ-005** | OPEN (cross-cutting) | Division of hedge-adjustment responsibility across components if the proposed B.2/B.3 collection proceeds | Determines whether/how this component's expense is later adjusted; base Eq A44 model contains no hedge term and is kept separate | Final data-collection outcome + Fed methodology statement |
| **OQ-008** | **RESOLVED FOR PROJECT IMPLEMENTATION (2026-07-17)** | WAL reporting unit for Schedule G item 71 | Resolution [PID-3/PID-4]: item 71 is reported in **months**; WAL_quarters = WAL_months/3; ρ_b = 3/WAL_months. **This resolution is user-confirmed project implementation context — the PPNR model section itself does not state the unit.** Log entry updated in `handbook/open-questions.md` | Already resolved for this project; eventual authoritative cross-check: FR Y-14Q Schedule G instructions / MDRM |

**Questions considered and intentionally not filed as new OQs** (resolved by user-confirmed context before filing, per instruction of 2026-07-17):

- *Balance line item*: the PPNR source does not identify the FR Y-14Q line item for the average balance (fact of absence, §2.3); project mapping is item 34E, flat for nine quarters [PID-1]. Not a project blocker.
- *1-year Treasury path source*: the PPNR document does not describe the physical MEV storage format; project source is the MEV workbook column "USD 1Y Treasury" [PID-5]. Not a project blocker.

**No new open questions are filed.** After applying the user-confirmed context, the only genuinely unresolved issue remaining is OQ-005 (cross-cutting hedge allocation).

---

## 14. Source traceability table

| # | Claim / methodology element | Class | PDF p. | md anchor | Eq/Table/Fn | Verification | Notes |
|---|---|---|---|---|---|---|---|
| 1 | Component name and section heading v.a(7) | FACT | 209 | sec-193 | — | PDF image 2026-07-17 | — |
| 2 | Table A6 row: "Domestic time deposits — Structural" | FACT | 168–169 | sec-148 | Table A6 | Integrity review 2026-07-16 | — |
| 3 | Listed among the 10 proposed structural components | FACT | 172 | sec-149 | — | PDF image 2026-07-17 | — |
| 4 | Structural models based on granular FR Y-14Q G/B/M and FR Y-14M data | FACT | 172 | sec-149 | — | PDF image 2026-07-17 | — |
| 5 | Structural models "avoid statistical estimation … fully explainable" | FACT | 172–173 | sec-149 | — | PDF image (p. 172) + integrity review (p. 173) | — |
| 6 | Model narrative: fraction matures; replaced at reference rate; remainder keeps prior rate; dependent variable = FR Y-14Q rate | FACT | 209 | sec-193 | — | PDF image 2026-07-17 | — |
| 7 | Expense = modeled rate × **average** balance (FR Y-14Q) | FACT | 209 | sec-193 | — | PDF image 2026-07-17 | "average" added by Dec 2025 revision (PDF pp. 4–5; sec-0) |
| 8 | Equation A44 and its where-list | FACT | 209 | sec-194 | Eq A44 | Integrity review + PDF image 2026-07-17 | — |
| 9 | Initial rate = jump-off average rate, Schedule G item 42E | FACT | 209 | sec-194 | — | PDF image 2026-07-17 | PID-2 concurs |
| 10 | ρ_b = 1/WAL from Schedule G item 71; constant throughout projection | FACT | 209 | sec-194 | — | PDF image 2026-07-17 | Unit = months is PID-3, not source |
| 11 | Assumption: constant repricing percentage; heterogeneity abstraction | FACT | 210 | sec-195 | — | PDF image 2026-07-17 | — |
| 12 | Assumption: re-originations at 1Y Treasury; no market power; "at lift-off" wording | FACT | 210 | sec-195 | — | PDF image 2026-07-17 | Comma-quirk note §11.1 |
| 13 | Limitation: richer maturity structures not possible; contractual terms not tracked | FACT | 210 | sec-195 | — | PDF image 2026-07-17 | — |
| 14 | Call Report 1-quarter/1-year/3-year maturity-profile modification | ALT | 210–211 | sec-195 | — | PDF image 2026-07-17 | Not proposed; excluded from workflow |
| 15 | Question A177 | FACT | 211 | sec-196 | — | PDF image 2026-07-17 | SQ-4 intro quirk confirmed on image |
| 16 | Nine-quarter projection horizon | FACT | 6 | sec-2 | — | PDF image 2026-07-17 | — |
| 17 | Structural-model definition; "date of lift-off" | FACT (background) | 32–33 | sec-14, sec-15 | — | md + integrity-review conventions | — |
| 18 | Constant-balance convention (general statements) | FACT (general) / INT (application here) | 169–170; 181–182; 207; 221 | sec-148; sec-164; sec-190; sec-211 | — | md; pp. 169, 207, 221 in integrity-review page set | v.a(7) itself does not restate it; PID-1 fixes the project treatment |
| 19 | Table A7 scope = Equations A46 models; no domestic-time row | FACT | 219 | sec-209 | Table A7 | Integrity review 2026-07-16 | SQ-1, SQ-2 recorded |
| 20 | Hedge adjustment: separate, accounting hedges only, contingent B.2/B.3; Eqs A49–A51; no renewals/terminations | FACT | 220–223 | sec-210–212 | Eqs A49–A51 | Integrity review 2026-07-16 | OQ-005 |
| 21 | Foreign deposits model covers foreign time (items 44B/35B) | FACT | 215–216 | sec-201–202 | — | md; p. 215–216 in integrity-review page set | Exclusion boundary |
| 22 | Other domestic deposits = MMA/savings/transaction (v.a(8)) | FACT | 211 | sec-197 | — | PDF image 2026-07-17 (p. 211) | Exclusion boundary |
| 23 | Current-suite definition (≤/> \$250k) and FR Y-9C codes | FACT (comparison context) | 75; 35–39 | sec-65; sec-19–21 | fn 27 | md-verified; current-suite pages not re-opened (COMPARISON policy) | Proposed model uses FR Y-14Q instead |
| 24 | Balance line item not identified in source; "34E" absent from the entire document | FACT (absence) | 209 | sec-193 | — | Full-text search 2026-07-17 | PID-1 supplies the project mapping |
| 25 | PID register (items PID-1…PID-6) | PID | — | — | — | User confirmation 2026-07-17 | Never attributable to the Fed |
| 26 | Within the proposed 2026 suite, explicit annual→quarterly conversion statements (÷4; N/360) appear only in trading-NII data construction, securities coupon accrual, and hedge legs — never for deposit expense; current-suite fn 54 (subordinated debt) states an annual-rate ÷4 | FACT (absence for this component) | 225; 191, 196, 201; 222; 155 | sec-215; sec-177/181/185; sec-211; fn 54 md 5338 | fn 54 | Integrity review 2026-07-16 + Step 5 review 2026-07-17 | Basis for classifying the ÷4 as [PID-6], never as a Fed statement |

---

### Brief completion checklist

- [x] Status banner present; no adoption language anywhere.
- [x] Every material statement labeled [FACT]/[PID]/[INT]/[CODE]/[OQ]/[ALT]; unknowns stated as unresolved, never defaulted.
- [x] Equation A44 and all quoted passages verified against PDF page images (pp. 6, 172, 209–211 on 2026-07-17; remainder per integrity review 2026-07-16).
- [x] Fed methodology, project decisions, interpretations, coding considerations, open questions, and non-proposed alternatives kept in separate, labeled homes.
- [x] Launch-point vs projection-quarter timing explicit for every input (§4.3).
- [x] Rates, balances, and dollar expenses kept distinct; the ÷4 quarterization is explicit, final-step only, and labeled [PID-6] — never attributed to the Fed; OQ-006 resolved for project implementation; OQ-005 open.
- [x] No new model proposed; Call Report variant recorded as [ALT] only.
- [x] No production Python; no confidential workbook content.
- [x] Brief APPROVED 2026-07-17; Step 4 chapter drafted at `handbook/models/interest-expense/deposits/ie_dom_time_dep.md`.

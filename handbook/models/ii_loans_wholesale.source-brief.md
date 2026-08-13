# Source Brief — Interest Income on Loans: Wholesale Framework (`ii_loans` — wholesale)

> **STATUS: Proposed for the 2026 stress test — public-comment stage, NOT adopted.**
> Component: **Interest Income on Loans**, Section v.a(1) (PDF pp. 173–188; md sec-150–172); this brief covers the **methodology shared by the two wholesale parts, Corporate and CRE** (PDF pp. 175–177, 181–183, 185–186; md sec-153–155, sec-163–165, sec-171). Model type per Table A6: **Structural**.
> Deliverable: loans workstream (asset-side Increment 3), slice 1 per the approved plan of 2026-07-30 — **wholesale-framework brief**, companion to `ii_loans_common.source-brief.md`. Review state: **APPROVED 2026-08-03** *(recorded in `inventory/model-inventory.md` at approval; banner updated 2026-08-12 from "DRAFT — awaiting user review", per the user's 2026-08-12 confirmation — amendment recorded, not silent)*. Portfolio-specific rules are identified and **deferred** to the Corporate and CRE briefs (§11); nothing retail is elaborated.
> Equation-ownership rule (user decision 2026-07-30): **this brief transcribes no equations.** All Equations A32–A38 live verbatim in the common brief §7; this brief documents their wholesale application and cites them.
> Integrity flags relevant here: SQ-5 (truncated "sourced from FR.", OQ-015), SQ-6 (A37 typography), SQ-18/OQ-033 (fixed-rate subscripts), SQ-19 ("farm"/"farmland" variant), footnotes 61–62. Related OQs: OQ-001, OQ-002, OQ-003, OQ-010, OQ-015, OQ-033, OQ-034, OQ-035.
> Verification: **PDF pp. 173–188 read as page images 2026-07-30**; citation format (PDF p. N; md sec-M).

---

## 0. Classification legend and scope

Labels [FACT] / [PID] / [INT] / [CODE] / [OQ] / [ALT] per `ii_loans_common.source-brief.md` §0. **No PID affects this brief** — the one loans PID, **PID-LOAN-1** (2026-08-03), is Corporate-scoped (`ii_loans_corporate.source-brief.md` §0.1); no physical mapping is user-confirmed for loans yet. *(Amended 2026-08-03 from "No PIDs exist for the loans component yet"; recorded, not silent.)*

Scope discipline for this brief:

- A rule enters this brief only if the source states it **for wholesale as a whole**, or states it in one wholesale part with genuine cross-part relevance — in which case the placement is recorded as [FACT] and the extension is a **flagged working assumption**, never silently generalized (§4; OQ-035).
- Rules the source states for one portfolio only (the Corporate NPML treatment, the per-portfolio enumerations, the CRE FR Y-9C type definitions) are **identified, cited, and deferred** (§11).
- Common-framework rules (flat balances, Eq A32 mechanics, spread constancy, scalar mechanism, assumptions (1)–(7)) are **not restated**; they apply to wholesale exactly as documented in the common brief, per its §3 boundary register.

---

## 1. Executive summary

**What "wholesale" is in this model.** [FACT] "Wholesale interest income projections are organized into two parts: Corporate and Commercial Real Estate (CRE)" (PDF p. 175; md sec-153), on facility-level FR Y-14Q data (footnote 61), with each part "segmented by asset classification: held for investment (HFI) and fair value option/held for sale (FVO/HFS)" and then by rate type under the common segmentation principle.

**How wholesale rates project.** [FACT] The wholesale base rate is the **three-month Treasury yield** (PDF p. 181; md sec-163). Variable-rate segments follow Equation A33 (base rate + constant launch-point spread); "the majority of balances in wholesale are variable-rate, thus the projected base rate is most responsible for changes in the projected interest income" (PDF p. 181). Fixed-rate segments follow the Equations A34/A35/A38 machinery with the **wholesale spread branch** (Equation A37): spread = balance-weighted average interest income rate of **all** loans at the jump-off quarter minus the base rate at the **median origination date (t−a)** for that portfolio (PDF p. 182; md sec-165; OQ-003).

**Wholesale-located flexibility and limits.** [FACT] The Fed's Wholesale Portfolio limitations record: the 3M Treasury is "a strong proxy" for the reset indices; loan-level projection, more precise jump-off-rate timing, actual maturity dates, and facility-specific PDs would add precision; a more granular approach would improve floor accuracy; the model assumes a constant roll-off rate and "further accounts for this by applying a conservative roll-off rate for fixed-rate loans" (PDF pp. 185–186; md sec-171).

---

## 2. Wholesale hierarchy and classification

### 2.1 The two parts and the classification dimensions

- [FACT] Two parts: Corporate and CRE (PDF p. 175; md sec-153).
- [FACT] Asset classification: "Each section is segmented by asset classification: held for investment (HFI) and fair value option/held for sale (FVO/HFS)." (PDF p. 175; md sec-153)
- [FACT] Rate type: "CRE segmentation is similar to Corporate segmentation where interest rate variability splits the portfolio by fixed-rate and variable-rate interest rates" (PDF pp. 176–177; md sec-155); the common principle makes rate type the primary split (common brief §7.2).

### 2.2 Corporate grid (summary; enumeration deferred)

- [FACT] "The corporate section of loan level interest income is segmented by 11 disclosure categories and loan types (referenced as a portfolio)." The 11-portfolio enumeration (PDF pp. 175–176; md sec-154) is **deferred to the Corporate brief** (§11).
- [FACT] "Most of the firm's corporate portfolios (16 out of 22) are further segmented by the interest rate variability since this provides a clear distinction on when the interest rate will be adjusted." (PDF p. 175; md sec-154)
- [INT — derivation unstated; **OQ-034**] The "22" is read as 11 portfolios × 2 asset classifications (HFI; FVO/HFS) = 22 portfolio-classification cells; the 6 cells not rate-split are the 3 portfolios without loan-level data (loans for purchasing and carrying securities; domestic farmland; international farmland — PDF p. 176) × 2 classifications. Under this reading the corporate segment count would be 16 × 2 + 6 = 38 — **the source states no corporate segment total** (contrast CRE's stated 24), so the register stays [INT].

### 2.3 CRE grid (summary; enumeration deferred)

- [FACT] "The CRE section of loan-level interest income is first segmented into six disclosure loan types (also referred to as portfolios) as defined in FR Y-9C" (PDF p. 176; md sec-155); the 6-type enumeration is **deferred to the CRE brief** (§11).
- [FACT] "With the asset classification segmentation, the total number of CRE segments is 24." (PDF p. 177; md sec-155)
- [INT — arithmetic restatement] 24 = 6 loan types × 2 rate types × 2 asset classifications; the multiplication is not printed but the sentence names exactly those two segmentation steps on the 6 types.

---

## 3. Data basis

- [FACT, with SQ-5] "Data used in the segmentation of wholesale balances are sourced from FR." — the sentence is truncated in the published PDF itself, immediately before the footnote 61 marker (PDF p. 175; md sec-153; page image re-confirmed 2026-07-30). [INT, per **OQ-015**] The intended reference is FR Y-14Q (Schedule H.1), per footnote 61 and the Corporate section's H.1 references.
- [FACT] Footnote 61 (verbatim): "The wholesale FR Y-14Q data is at the facility level, but for ease of readability by matching with Retail this document references FR Y-14Q data as at the loan level." (PDF p. 175 footer; md 5350) — wholesale source data are **facility-level**; the section's "loan level" wording is a readability convention.
- [FACT] Schedule H.1 is the named wholesale loan-level schedule: the three unsegmented Corporate portfolios "have no loan-level data on the FR Y-14Q H.1 schedule", and "Currently, the FR Y-14Q Schedule H.1 schedule is able to identify NPMLs" (PDF p. 176; md sec-154 — the doubled "Schedule H.1 schedule" is the source's own wording, preserved).
- [FACT of absence] No wholesale line items, field names, or extraction rules beyond the above are stated in v.a(1). Physical mappings await user confirmation at the coding stage (no loans PIDs yet).

---

## 4. Rate-type treatment

- [FACT] Footnote 62 (verbatim): "The wholesale FR Y-14Q interest rate variability value for variable-rate is floating. Using variable-rate in this document for ease of readability." (PDF p. 175 footer; md 5352) — the reporting field's value is **"floating"**; the document's "variable-rate" is terminology.
- [FACT — stated under Corporate] "The interest income model treats mixed-rate and demand loans (loans where the lender can demand full repayment at any time) as variable-rate." (PDF p. 176; md sec-154)
- [FACT — stated under Corporate] "Fee-only loans are assumed to generate no interest income. Hence, they are not used to calculate the average interest rate, and their outstanding balance percentages are excluded from the total balances calculation." (PDF p. 176; md sec-154)
- **Placement and scope [OQ-035, filed 2026-07-30]:** both rules sit inside the **Corporate** subsection; nothing states whether they extend to CRE (whose section says only that its segmentation "is similar to Corporate"). **Working assumption (flagged, never source-attributed):** the rules are wholesale-wide — mixed-rate/demand/fee-only are facility attributes not specific to corporate lending, and the CRE "similar to Corporate" sentence points the same way. Formally, CRE applicability is UNKNOWN until OQ-035 resolves.
- [FACT of absence] No wholesale-specific rate-reset frequency is stated beyond the common "Most variable rates reset quarterly" (assumption (5); common brief §12.1).

---

## 5. Wholesale base rate

- [FACT] "For wholesale, the Board proposes to use the three-month Treasury yield as the base rate. The majority of balances in wholesale are variable-rate, thus the projected base rate is most responsible for changes in the projected interest income." (PDF p. 181; md sec-163)
- [FACT] The Wholesale limitations subsection adds: "The scenario-provided three-month Treasury yield is a strong proxy for the index values applied when interest rates are adjusted." (PDF p. 185; md sec-171)
- [FACT] **Question A152** asks whether "the SOFR one-month maturity and the Prime Rate" should replace the 3M Treasury as the wholesale base rate (PDF p. 187; md sec-172; verbatim in common brief §13) — the Fed itself treats the wholesale base-rate choice as open for comment; the as-proposed rate is the 3M Treasury.
- Scenario series: `usd_3m_treasury` (shared canonical name; physical column mapping per the PID-5 pattern remains UNCONFIRMED for this model — `asset-side-common-conventions.md` §3).

---

## 6. Wholesale spread — Equation A37 application

Equation A37 is transcribed verbatim in the common brief §7.6 (with SQ-6); this section documents its wholesale mechanics.

- [FACT] "For wholesale, the spread is calculated from the average rate of all loans at the jump-off quarter and the base rate from the median origination date ( *t* - *a*) for that portfolio. The base rate applied is the same as the base rate for floating: … the three-month Treasury yield for wholesale." (PDF p. 182; md sec-165)
- Components, as printed in A37 (common §7.6):
  - `balance-weighted avg IIR(b,p,i,t=0)` — the balance-weighted average interest income rate of **all** loans in the portfolio/segment at the jump-off quarter (contrast the retail branch, which uses new originations only) [FACT];
  - `Base rate(t−a)` — the 3M Treasury value at the **median origination date** of that portfolio, a **pre-PQ0 historical** observation [FACT]; the subscript carries no (b,p,i) index while the prose says "for that portfolio" ([INT] the median origination date is portfolio-specific, so t−a varies by portfolio; the printed subscript abbreviates).
- [OQ-003] How `a` is measured — median over loans or balance-weighted, at which granularity (portfolio p vs. segment i vs. firm×portfolio), and how the historical 3M Treasury series is sourced — is **not stated**.
- [FACT] Rationale (faithful restatement of the bias paragraph, PDF p. 183; md sec-165; verbatim in common §7.6): jump-off-quarter base rates would bias spreads for rates "set at some point in the past"; the median origination date "may better account for changing risk profiles but come at the expense of likely measurement error."
- [FACT] **Question A155** asks whether wholesale fixed-rate balances should instead adopt the retail new-originations approach — "The current approach of wholesale fixed-rated balances is to use the base variable at the median origination date." (PDF p. 187; md sec-172)
- [FACT] The Wholesale limitations note the refinement direction: "For fixed-rate loans, a more precise measure of when the jump-off interest rate was set could be used during the interest rate spread calculation." (PDF pp. 185–186; md sec-171)
- Timing/containers [CODE]: the t−a base-rate value is pre-PQ0 **history** — per `asset-side-common-conventions.md` §5 it never enters the scenario container; it arrives as a supplied launch-point firm input (the liability-side `elb_spread` precedent), or the derived spread itself is supplied.
- Dimension note: Equation A37 **includes** the firm dimension `b` on the spread and the IIR — the SQ-18/OQ-033 subscript question bites the wholesale side only through A34/A35/A38 (the blend machinery), not through the spread itself (common §7.6).

## 7. Fixed-rate application in wholesale

- [FACT] "In wholesale, fixed-rate products are more common for CRE income-producing loans." (PDF p. 183; md sec-165)
- [FACT] Existing fixed rates are the balance-weighted origination rates at jump-off, unchanged except termination (Eq A34; common §7.6); re-origination flows through the Eq A38 blend with weight wt.
- [FACT] Precision limitations, wholesale-located: "for fixed-rate loans, using actual maturity dates and facility-specific probabilities of default would increase precision of when to update the interest rate." (PDF p. 186; md sec-171) — i.e., the proposed model does **not** use actual maturity dates or facility-specific PDs for re-origination timing; wt comes from portfolio-level default/prepayment/maturity rates (common §7.6; OQ-001).
- [INT] "CRE income-producing loans" is not one of the six CRE disclosure types; it reads as a business characterization (multifamily / non-owner-occupied income-producing CRE vs. construction). The CRE brief owns any firmer mapping; no mapping is invented here.

## 8. Floors in wholesale

- [FACT] The common floor rule applies: "All portfolios have a portfolio-specific interest rate floor that will bind if the projected interest rate decreases to the stated floor." (PDF p. 180; md sec-161; common §7.1; values/source UNKNOWN — **OQ-002**)
- [FACT] **Question A153** (wholesale-directed): "Should corporate and CRE variable-rate balances be further segmented to vary the interest rate floor? … Increases in segmentation will increase the accuracy of the interest rates by limiting interest rate movements when a floor should be binding." (PDF p. 187; md sec-172)
- [FACT] Wholesale limitations: "For variable-rate loans, a more granular approach would improve the accuracy of the interest rate floor." (PDF p. 186; md sec-171)
- [INT] Question A153's framing (floors on **variable-rate** balances, binding "if the projected scenario variable decreases the projected interest rate below the stated floor") indicates the floor's operative wholesale case is the variable-rate path under falling base rates; the stated common rule is portfolio-generic. Both readings are recorded; no floor mechanics beyond max(rate, floor) are stated anywhere ([FACT] absence).

## 9. Credit-risk dependencies

- [FACT] The model calculates rates using "estimated loss rates from the Retail and Wholesale models" (PDF p. 174; md sec-151) — for this brief's scope, the **Wholesale** credit-loss models supply the wholesale portfolios' default/prepayment/maturity inputs to wt (common §7.6; **OQ-001** external dependency: granularity, definitions, delivery format all unstated).
- [FACT] "The model assumes a constant roll-off rate. This implies that extensions and prepayment and amortizations are not endogenous. It seems reasonable that an obligor is more likely to pay back a loan or seek an extension with different terms when interest rates are falling. Prepayment penalties and the lender needing to agree to the extension may limit to some extent the increased roll-off during a decreasing interest rate environment. Also, spreads will increase during stress which would further mitigate an endogenous roll-off rate. The model further accounts for this by applying a conservative roll-off rate for fixed-rate loans." (PDF p. 186; md sec-171)
- [INT] Constancy tension recorded (common §5.3): wt is printed time-subscripted, wt(p,i,t) (Eq A38), while the wholesale limitation states "a constant roll-off rate"; consistent reading — the roll-off **rate** is constant, so the per-quarter weight need not vary, but the printed subscript permits it. What "conservative" quantitatively means is UNKNOWN (folded into OQ-001's input contract — the delivered rates embed it).

## 10. Fee treatment

- [FACT — Corporate-stated; OQ-035 for CRE scope] Fee-only loans generate no interest income and are excluded from both the average-rate calculation and the outstanding-balance percentages (§4).
- [FACT of absence] v.a(1) states no other fee-income methodology for wholesale: fee income on ordinary loans (commitment, origination, servicing fees) is nowhere addressed in the section. Whether such fees belong to this component's Table A6 row at all is outside the loan section's text; nothing is inferred here.

## 11. Portfolio-specific deferral register

Rules identified as Corporate- or CRE-specific; recorded with citations, deferred in full to the future sibling briefs.

| # | Item | Stated at | Deferred to | Notes filed now |
|---|---|---|---|---|
| 1 | Corporate 11-portfolio enumeration | PDF pp. 175–176; md sec-154 | Corporate brief | — |
| 2 | Which 16 of 22 cells split by rate variability; corporate segment total | PDF pp. 175–176; md sec-154 | Corporate brief | [INT] arithmetic + **OQ-034** (§2.2) |
| 3 | NPML-based treatment of the 3 no-loan-level portfolios: "The Board assumes, for these portfolios, the same bank-level interest rate spread as reported in their variable-rate lending to depository institutions. This assumption is based on loan-level data on non-purpose margin loans (NPML) … The majority of NPMLs were variable-rate, so the Board assumes loans for purchasing and carrying securities have variable rates." | PDF p. 176; md sec-154; restated PDF p. 186; md sec-171 | Corporate brief | Terminology gap noted for the Corporate brief: the spread source is "variable-rate lending to **depository institutions**" while the portfolio list has "loans to **financial institutions**" — relationship unstated. **SQ-19**: the limitations restatement writes "domestic **farm** loans, and international **farm** loans" (p. 186) where the portfolio list has "**farmland** loans" (p. 175) — source-internal naming variant, recorded, never corrected |
| 4 | CRE six FR Y-9C loan-type enumeration and definitions | PDF p. 176; md sec-155 | CRE brief | — |
| 5 | "CRE income-producing loans" fixed-rate prevalence mapping | PDF p. 183; md sec-165 | CRE brief | [INT] §7 |
| 6 | Table A8 wholesale-relevant rows: "Domestic CRE" (1.081), "Rest of wholesale" (1.113), and the merged "C&I, noncore SME loan and card" (1.033) | PDF p. 220; md sec-209 | Corporate/CRE briefs | **OQ-010**: category→row mapping UNKNOWN; sub-question — no row names **international** CRE, so whether international CRE portfolios fall under "Rest of wholesale" or elsewhere is UNKNOWN |
| 7 | Mixed-rate/demand and fee-only mechanics beyond the §4 statements | PDF p. 176; md sec-154 | Corporate brief (+ OQ-035 outcome) | — |

---

## 12. Fed-stated Wholesale Portfolio limitations — [FACT] (PDF pp. 185–186; md sec-171)

Restated faithfully; quoted passages verbatim.

1. **Index proxy and granularity.** "The scenario-provided three-month Treasury yield is a strong proxy for the index values applied when interest rates are adjusted. More accuracy could be gained projecting interest income at the loan level instead of cutting the portfolio into segments."
2. **Fixed-rate precision.** "For fixed-rate loans, a more precise measure of when the jump-off interest rate was set could be used during the interest rate spread calculation. Also, for fixed-rate loans, using actual maturity dates and facility-specific probabilities of default would increase precision of when to update the interest rate."
3. **Variable-rate floors.** "For variable-rate loans, a more granular approach would improve the accuracy of the interest rate floor."
4. **Constant roll-off and its defense.** Quoted in full in §9.
5. **NPML proxy.** "The model assumes that non-purpose margin loans (NPML) are a good proxy for loans for purchasing and carrying securities, domestic farm loans, and international farm loans. The Board used the loan-level analysis with only NPML as guidance to how to treat these missing portfolios." (SQ-19 naming variant — §11 row 3.)
6. **Revolver draws.** "The model does not increase draws from revolvers throughout the projection. This is different than credit loss models where there is an expected increase in draws from revolvers through exposure at default estimation. The expected change in interest income from increases in draw from revolvers during stress is minimal. Increases in draw from healthy firms will be short-lived precautionary liquidity insurance with firms paying them down quickly, while draws by firms that end up in bankruptcy are not expected to earn material interest income." — **Placement note [INT]:** this paragraph sits inside the Wholesale Portfolio subsection; revolving exposures also exist in retail (credit cards, HELOC), and nothing marks the statement as wholesale-only. Recorded as wholesale-located; possible loan-wide scope left to the integration review.

---

## 13. Wholesale-directed Board questions

Verbatim census in the common brief §13; this brief's three (pointers):

- **A152** — wholesale base-rate alternatives (SOFR 1M, Prime) vs. the proposed 3M Treasury (§5).
- **A153** — corporate/CRE variable-rate floor segmentation (§8).
- **A155** — wholesale fixed-rate spread: median-origination-date approach vs. the retail new-originations approach (§6).

---

## 14. Coding considerations — [CODE], non-normative

- **Wholesale segment grid as configuration:** Corporate 11 × {HFI, FVO/HFS} × {fixed, variable | unsplit} (which cells split pending OQ-034 confirmation; 3 portfolios unsplit and treated variable per the NPML analysis) and CRE 6 × 2 × 2 = 24, feeding the common Equation A32/A33/A38 engine. Enumerations arrive with the Corporate/CRE briefs — the grid shape should be data, not code.
- **Rate-type normalization:** map the H.1 "interest rate variability" values to the model's {fixed, variable} with explicit rules floating→variable (footnote 62), mixed-rate→variable, demand→variable, fee-only→excluded; unmapped values are a **hard error, surfaced, never defaulted** (PID-SEC-5 precedent). The CRE applicability of the mixed/demand/fee-only rules is config-visible until OQ-035 resolves.
- **A37 inputs as launch-point data:** supply either {all-loan balance-weighted IIR at PQ0, portfolio median origination date, historical 3M Treasury at t−a} or the derived wholesale fixed spread directly; keep pre-PQ0 history out of the scenario container (conventions §5). The choice of delivery is an OQ-003-dependent interface decision.
- **Floor inputs:** per-portfolio (or finer, per the Question A153 outcome) supplied floor values; refuse to run while UNKNOWN (OQ-002); binding diagnostics per segment-quarter.
- **wt contract (wholesale side):** declared input path for wholesale default/prepayment/maturity rates (or composite wt) per (p,i,t) — dimensionality configurable pending OQ-033/OQ-001.
- No production Python; nothing here is Fed methodology.

---

## 15. Open questions

| ID | Status | Relevance to this brief |
|---|---|---|
| **OQ-001** | OPEN (external dependency) | Wholesale credit-model rates into wt; "conservative roll-off" quantification (§9) |
| **OQ-002** | OPEN | Floor values/source; wholesale floor granularity context (§8) |
| **OQ-003** | OPEN | Median origination date (t−a) measurement and granularity; historical base-rate sourcing (§6) |
| **OQ-010** | OPEN | Wholesale scalar rows incl. the international-CRE mapping sub-question (§11 row 6) |
| **OQ-015** | OPEN (minor) | SQ-5 "sourced from FR." truncation; FR Y-14Q reading (§3) |
| **OQ-033** | OPEN — filed 2026-07-30 | Fixed-rate machinery firm dimension (A34/A35/A38); A37 itself carries b (§6) |
| **OQ-034** | OPEN — filed 2026-07-30 | Corporate "16 out of 22" derivation; corporate segment total unstated (§2.2) |
| **OQ-035** | OPEN — filed 2026-07-30 | CRE applicability of Corporate-stated mixed-rate/demand/fee-only rules (§4) |

---

## 16. Source traceability table

| # | Claim / element | Class | PDF p. | md anchor | Verification |
|---|---|---|---|---|---|
| 1 | Wholesale = Corporate + CRE | FACT | 175 | sec-153 | Page image 2026-07-30 |
| 2 | HFI vs. FVO/HFS classification | FACT | 175 | sec-153 | Page image 2026-07-30 |
| 3 | "sourced from FR." truncation; FR Y-14Q reading | FACT (SQ-5) + INT (OQ-015) | 175 | sec-153 | Page image 2026-07-30 (truncation in PDF) |
| 4 | Footnote 61 — facility-level data; loan-level readability convention | FACT | 175 (footer) | md 5350 | Integrity review + page image 2026-07-30 |
| 5 | Corporate: 11 portfolios; 16 of 22 rate-split | FACT | 175–176 | sec-154 | Page image 2026-07-30; OQ-034 |
| 6 | Footnote 62 — "floating" reporting value | FACT | 175 (footer) | md 5352 | Integrity review + page image 2026-07-30 |
| 7 | Mixed-rate and demand loans → variable; demand-loan definition | FACT | 176 | sec-154 | Page image 2026-07-30; OQ-035 |
| 8 | Fee-only loans: no income; excluded from rates and balance percentages | FACT | 176 | sec-154 | Page image 2026-07-30; OQ-035 |
| 9 | 3 portfolios without H.1 loan-level data; NPML-based spread and variable-rate assumptions | FACT | 176 | sec-154 | Page image 2026-07-30 |
| 10 | CRE: 6 FR Y-9C loan types; rate-variability split; 24 segments | FACT | 176–177 | sec-155 | Page image 2026-07-30 |
| 11 | Wholesale base rate = 3M Treasury; majority variable-rate | FACT | 181 | sec-163 | Page image 2026-07-30 |
| 12 | Wholesale spread: all loans at jump-off; base rate at median origination date (t−a) | FACT | 182 | sec-165 | Page image 2026-07-30; Eq A37 verbatim in common §7.6 (SQ-6) |
| 13 | Bias rationale (jump-off vs. median origination date) | FACT | 183 | sec-165 | Page image 2026-07-30 |
| 14 | Fixed-rate more common in CRE income-producing loans | FACT | 183 | sec-165 | Page image 2026-07-30 |
| 15 | Floors: common rule; Question A153 wholesale segmentation; granularity limitation | FACT | 180, 186–187 | sec-161, sec-171, sec-172 | Page images 2026-07-30; OQ-002 |
| 16 | Wholesale Portfolio limitations (six items, §12) | FACT | 185–186 | sec-171 | Page images 2026-07-30 |
| 17 | "farm loans" vs. "farmland loans" naming variant | FACT (SQ-19) | 186 vs. 175 | sec-171 vs. sec-154 | Page images 2026-07-30 |
| 18 | Questions A152/A153/A155 (wholesale-directed) | FACT | 187 | sec-172 | Page images 2026-07-30; verbatim in common §13 |
| 19 | Loss rates from the Wholesale credit models (wt inputs) | FACT | 174, 183 | sec-151, sec-165 | Page images 2026-07-30; OQ-001 |
| 20 | Table A8 wholesale-relevant rows | FACT | 220 | sec-209 | Integrity review 2026-07-16; OQ-010 |

---

### Brief completion checklist

- [x] Status banner present; no adoption language anywhere.
- [x] Every material statement labeled; unknowns stated UNKNOWN; working assumptions flagged (never source-attributed).
- [x] **Zero verbatim equation blocks** — all equations cited from `ii_loans_common.source-brief.md` §7 per the user's equation-ownership decision.
- [x] Corporate-/CRE-specific rules identified, cited, and deferred (§11); no retail content.
- [x] Placement facts distinguished from scope extensions (mixed/demand/fee-only — §4; revolver paragraph — §12.6).
- [x] Source quirks preserved verbatim (SQ-5, SQ-19; the "Schedule H.1 schedule" doubling); conversion policy per integrity review.
- [x] No production Python; no confidential workbook content.
- [x] Review state: **APPROVED 2026-08-03** (banner and checklist updated 2026-08-12).

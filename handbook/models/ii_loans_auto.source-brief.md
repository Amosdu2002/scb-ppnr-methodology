# Source Brief — Interest Income on Loans: Auto Loan (`ii_loans` — retail/auto)

> **STATUS: Proposed for the 2026 stress test — public-comment stage, NOT adopted.**
> Component: **Interest Income on Loans**, Section v.a(1) (PDF pp. 173–188; md sec-150–172); this brief covers the **Auto Loan** family of Retail (PDF p. 178; md sec-158), plus the auto-relevant passages elsewhere in v.a(1): the retail fixed-rate prevalence note (PDF p. 183; md sec-165), the Retail Portfolio limitations' auto sentences (PDF p. 185; md sec-170), Table A8's Auto row (PDF p. 220; md sec-209), and footnote 63's "auto" category (PDF p. 184 footer; md 5354). Model type per Table A6: **Structural**.
> Deliverable: loans workstream (asset-side Increment 3), retail slice R1 per the approved plan of 2026-08-12 — first **family brief** of the retail set, drafted in one slice with `ii_loans_retail.source-brief.md` (user-confirmed bundling and Auto-first order, 2026-08-12). Review state: **DRAFT — awaiting user review.**
> Scope: **Auto only.** Retail-shared rules are cited from the retail framework brief, never restated; equations are **not** transcribed (D-010(b) — all of Equations A32–A38 live verbatim in `ii_loans_common.source-brief.md` §7); the other three families appear solely where the source draws an explicit boundary.
> Integrity flags relevant here: SQ-18/OQ-033 (fixed-rate subscripts — auto is an all-fixed family), SQ-24 ("non-core retails products", framework §12). **No new source quirk was found in the auto passage.** Open questions: **OQ-042, filed with this brief** (new-origination spread measurement); the retail legs of OQ-001 (wt), OQ-002 (floors), and OQ-010 (scalar row); OQ-033.
> Verification: **PDF p. 178 read as a page image 2026-08-12** (both auto paragraphs confirmed verbatim; md conversion faithful); p. 183 re-read 2026-08-12 within the pp. 177–185 pass context; pp. 173–188 had a full image pass 2026-07-30. Citation format: (PDF p. N; md sec-M).

---

## 0. Classification legend and cross-reference discipline

Labels [FACT] / [PID] / [INT] / [CODE] / [OQ] / [ALT] per `ii_loans_common.source-brief.md` §0.

### 0.1 Project implementation decision register

**No PID affects this brief, and no retail loans PID exists yet.** No physical sheet, field, or value vocabulary has been user-confirmed for auto. The elicitation items this family needs before its spec stage (registered in the approved plan of 2026-08-12, Required with the R1 gate):

| # | Elicitation item | Blocks | Framework/OQ hook |
|---|---|---|---|
| 1 | The auto input sheet: name, header list, grain (expected segment-level per the A.2 basis), the new/used identification, balance and rate columns | launch-point construction | §5 |
| 2 | The Eq A32 multiplicand for auto: M.1 Balance rows/roles (per side if applicable) or another balance source — *M.1 context received same day [PID-LOAN-26]: dom role "Retail - Auto" on the Auto loans row, flagged in the "Auto (dom)" family column; international side → "Retail - noncore"; flag-sum construction + auto-lease-row membership still TO CONFIRM* | balance wiring | §5 row 6 |
| 3 | The workbook's **wt construction** for auto (runoff basis: maturity? amortization? prepayment?) | the A38 blend | **OQ-001 retail leg** (§8) |
| 4 | The workbook's **new-origination rate source** for the Eq A36 spread (new-origination cohort rate vs all-loan segment rate) | spread construction | **OQ-042** (§7) |
| 5 | Whether the auto sheet carries **floors**, and their collapse rule if per-segment values differ | floor clamp | **OQ-002 retail leg** (§9) |
| 6 | Scalar-row confirmation for auto blocks (candidate "Auto" 0.865) | Total construction | **OQ-010 retail leg** (§11) |
| 7 | Materiality: HFS auto balances at the firm (the reclass in §6.2 is then live or vacuous) — *M.1 view suggests the answer; confirm at the gate* | grid collapse | §6.2 |

---

## 1. Executive summary

**What Auto is.** [FACT] The second retail section (PDF p. 177; md sec-156). "Auto loans are reported in the FR Y-14Q schedule A.2 at the segment level." (PDF p. 178; md sec-158)

**How Auto segments and prices.** [FACT] "Auto loans are typically fixed-rate products, so the Board assumes that the portfolio is comprised of auto loans with fixed interest rates." Immaterial HFS balances are treated as HFI at the firm level. "The portfolio is segmented into new vehicle loans and used vehicle loans, driven primarily by the differences in rates between these two categories. The Board calculates balance-weighted average interest rates by segment and by firm and uses them as inputs for interest income projection. Trends in balance-weighted average interest rates were analyzed by product (i.e., new-vehicle vs. used-vehicle loans) and compared against the Prime Rate to determine the spread for the new origination rate." Origination-risk segments were reviewed and not adopted (PDF p. 178; md sec-158).

**What Auto adds beyond the shared machinery.** Almost nothing — and, as with CRE, that is the finding. The auto-specific prose is two paragraphs; every rate mechanic (Eq A34 frozen existing rates, Eq A35 new-origination rate on Prime, the Eq A36 retail spread branch, the Eq A38 blend, floors, the industry scalar) is inherited from the common and retail-framework briefs (§10). Auto's own facts: the A.2 segment-level basis, the all-fixed assumption, the HFS→HFI reclass, the new/used grid, the Prime spread benchmark, and the rejected risk segmentation [ALT].

**What is unresolved.** On the source side: how the Eq A36 "new originations" spread is actually measured for a family reported at the **segment level** — the auto paragraph describes a trend analysis of balance-weighted average rates against Prime rather than A36's new-origination-only weighted average (**OQ-042**, filed with this brief). The retail legs of OQ-001 (wt), OQ-002 (floors), and OQ-010 (scalar row) are open, and no physical mapping exists (§0.1).

---

## 2. Auto scope and boundaries

### 2.1 Position in the hierarchy

[FACT] Auto is the second of the four retail sections (PDF p. 177; md sec-156) — a **section**, not a Table A6 component; D-003 keeps all families in one chapter.

### 2.2 Explicit boundaries

| Boundary | Source statement | Label |
|---|---|---|
| **International auto loans are Other Consumer** | The non-core census names "international auto loans" (PDF p. 180; md sec-160) | [FACT] |
| Auto is therefore a domestic family | Not printed; follows from the p. 180 census | [INT] (framework §2.3) |
| Auto vs the other retail families | The four-section census (PDF p. 177; md sec-156) | [FACT] |

[FACT of absence] No statement addresses **leases** on vehicles anywhere in the retail subsections; wholesale's "other leases" is a Corporate portfolio (OQ-038 records its undefined contents). Whether vehicle leases sit in Corporate portfolio (4), in retail auto, or outside the model is unstated; nothing is inferred here (elicitation may surface the firm's treatment).

---

## 3. Auto census

### 3.1 The two segments (verbatim)

[FACT] "The portfolio is segmented into new vehicle loans and used vehicle loans, driven primarily by the differences in rates between these two categories." (PDF p. 178; md sec-158)

### 3.2 Per-segment attribute register

Coding-friendly names are this project's, not the Fed's.

| # | Segment | Coding-friendly name | Rate type | Stated rationale |
|---|---|---|---|---|
| 1 | new vehicle loans | `auto_new_vehicle` | fixed [FACT — portfolio-wide assumption §6.1] | rate differences between the two categories [FACT] |
| 2 | used vehicle loans | `auto_used_vehicle` | fixed [FACT — as above] | as above |

[FACT] The segment count (two) is stated directly; no reconstruction is needed (contrast the Corporate 22-cell grid, OQ-034).

### 3.3 Rejected segmentation — [ALT]

[ALT] "The Board also reviewed FR Y-14Q defined origination risk segments but ultimately does not propose to adopt these due to their immaterial incremental impact on the projected interest income." (PDF p. 178; md sec-158) — discussed and explicitly not proposed; the adopted grid is new/used only. (First use of the [ALT] label in the loans sibling set; the mortgage brief will carry the parallel term/FICO rejection.)

---

## 4. Auto segmentation hierarchy

### 4.1 The dimensions

| Level | Dimension | Values | Source |
|---|---|---|---|
| 0 | Retail family | Auto | [FACT] PDF p. 177; md sec-156 |
| 1 | Product type | new vehicle; used vehicle | [FACT] PDF p. 178; md sec-158 |
| 2 | Rate type | fixed only (portfolio-wide assumption) | [FACT] PDF p. 178; md sec-158 (§6.1) |
| 3 | Asset classification | **collapsed** — HFS treated as HFI at the firm level | [FACT] PDF p. 178; md sec-158 (§6.2) |

[INT] Effective grid: **2 segments per firm** (new; used), each on the fixed-rate machinery, all HFI after the reclass. The source states the pieces; the two-cell composition is restatement.

[FACT] Firm dimension: rates are calculated "by segment and by firm" (PDF p. 178) — part of the OQ-033 evidence set (framework §4.2).

---

## 5. Data inputs and classifications to capture

Every row states whether the source names the item. **No field name, code, or value vocabulary is invented** — no physical mapping exists for auto (§0.1).

| # | Item to capture | Source status | Notes |
|---|---|---|---|
| 1 | Segment-level records | [FACT] "reported in the FR Y-14Q schedule A.2 at the segment level" (PDF p. 178) | The one retail family with a **named Y-14Q schedule**; grain is segment, not loan — the first non-facility ingestion contract in the loans workstream [CODE §13] |
| 2 | New/used product identification | [FACT] the split exists; no field named | Elicitation item 1 |
| 3 | Balance-weighted average interest rate by segment × firm | [FACT] "calculates balance-weighted average interest rates by segment and by firm and uses them as inputs" (PDF p. 178) | The jump-off rate seed (common §7.2) |
| 4 | Segment balances / shares | [FACT] via the common balance construction (common §6); no auto item named | Elicitation items 1–2 |
| 5 | HFS auto balances, FR Y-9C | [FACT] "immaterial HFS auto loan balances reported in FR Y-9C" identified for the reclass (PDF p. 178) | §6.2; the only FR Y-9C reference in the retail subsections |
| 6 | Portfolio balance (Eq A32 multiplicand) | [FACT] "the portfolio balance from FR Y-14 Schedules" (PDF p. 174); no auto line named | M.1 candidate rows = elicitation item 2 (PID-LOAN-20 pattern) |
| 7 | New-origination rate observation (Eq A36 numerator) | [FACT] the retail branch uses "only new origination loans" (PDF p. 182); **auto measurement unstated** | **OQ-042** (§7) |
| 8 | Scenario base rate | [FACT] Prime Rate (PDF pp. 178, 181, 185) | `prime_rate`; MEV column TO_BE_CONFIRMED (framework §5.1) |
| 9 | Interest-rate floor | [FACT] the common rule (PDF p. 180); no auto statement | **OQ-002 retail leg** (§9) |
| 10 | wt inputs | [FACT] the common derivation (PDF p. 183); no auto statement | **OQ-001 retail leg** (§8) |
| 11 | Industry scalar | [FACT] Table A8 "Auto" 0.865 (PDF p. 220); assignment unstated | **OQ-010 retail leg** (§11) |

[FACT — recorded contrast] The suite-level data statement (PDF p. 172; md sec-149) names "FR Y-14Q, Schedule G; FR Y-14Q, Schedule B; FR Y-14Q, Schedule M; and FR Y-14M" — **Schedule A is absent from that list** while the auto subsection names Schedule A.2 directly. The mirror of the OQ-039 pattern (CRE's schedule unnamed anywhere), with the opposite polarity: here the section names the schedule and the suite list omits it. Because the schedule **is** named for auto, no open question arises; the inconsistency is recorded for the integrity log only.

[FACT of absence] "limited interest information" is all the source says about A.2's rate content (PDF p. 185; §12); no A.2 field, segment definition, or vintage structure is stated.

---

## 6. Rate-type treatment for Auto

### 6.1 The all-fixed assumption

[FACT] "Auto loans are typically fixed-rate products, so the Board assumes that the portfolio is comprised of auto loans with fixed interest rates." (PDF p. 178; md sec-158)

[INT — consequence] Auto is the only loan family with **no variable-rate segment at all**: Equation A33 never runs for auto, and the Prime Rate enters auto **only** through the Equation A35 new-origination rate (BaseRate + Spread) inside the Equation A38 blend. Any variable-rate auto balances a firm reports are absorbed into the fixed treatment by the portfolio-wide assumption — the mirror image of the card family's all-variable assumption (framework §6). The consequence follows from the stated assumption; the source states only the assumption.

[FACT] The prevalence note confirms the placement: "Fixed-rate retail products include fixed-rate mortgage and home loans, **auto loans**, and most non-core loans." (PDF p. 183; md sec-165)

### 6.2 The HFS reclass

[FACT] "The Board treats immaterial HFS auto loan balances reported in FR Y-9C as HFI loans at the firm level." (PDF p. 178; md sec-158)

- [INT] Consequence: the wholesale-style HFI vs FVO/HFS dimension **collapses** for auto — one classification cell. The reclass is grounded in a stated materiality judgment ("immaterial") made on FR Y-9C data.
- [FACT of absence] No threshold, procedure, or FR Y-9C item is named for identifying the HFS balances; whether the reclass is unconditional or conditional on the balances remaining immaterial is unstated. Elicitation item 7 asks whether the firm carries HFS auto balances at all (if none, the rule is vacuous in practice).

### 6.3 No other classification rules

[FACT of absence] No mixed-rate, demand-loan, or fee-only rule exists for auto (or any retail family — framework §6); no delinquency carve-out beyond common assumption (2); no auto-specific assumption or limitation subsection exists (the (c) block's retail subsection covers retail as a whole — framework §12).

---

## 7. Spread and the new-origination rate — OQ-042 (filed with this brief)

### 7.1 What the source states

[FACT] "Trends in balance-weighted average interest rates were analyzed by product (i.e., new-vehicle vs. used-vehicle loans) and compared against the Prime Rate to determine the spread for the new origination rate." (PDF p. 178; md sec-158)

[FACT] The retail spread branch (framework §7.1; transcription common §7.6): "For retail, instead of using the average rate of all loans, only new origination loans are used." — Equation A36: Spread(p,i,t=0) = weighted avg IIR for **new originations**(p,i,t=0) − Base rate(p,i,t=0), with Prime as auto's base rate (PDF pp. 178, 185).

### 7.2 The gap

**OQ-042.** The two statements do not compose cleanly for a segment-level family:

- Equation A36 requires a **new-origination-only** weighted average rate at the jump-off quarter. Whether Schedule A.2's segment-level reporting exposes a new-origination cohort (e.g., a vintage dimension) from which that average can be taken is unstated — the source says only that A.2 carries "limited interest information" (PDF p. 185).
- The auto sentence is written in the **design-time past tense** ("Trends … **were analyzed** … to determine the spread") and names the *all-loan* balance-weighted average rates as the analyzed quantity — leaving open whether the operative auto spread is (a) the A36 new-origination measurement on an A.2 origination cohort, or (b) a spread determined from the trend analysis of all-loan segment rates against Prime (a construction the equations do not print).

[INT — working reading, flagged, never source-attributed] Reading (a) — the A36 branch applies as printed, with the trend-analysis sentence describing how the Board validated Prime as the benchmark — keeps the family inside the stated equation set and is the default until evidence says otherwise. The workbook's own spread cell decides the project-side answer (elicitation item 4; candidate PID). Resolves on the source side: Fed clarification or final-rule text.

### 7.3 Constancy

[FACT] The spread, however measured, is constant: assumption (4) (common §12.1) and the Retail Portfolio limitation's "constant spread by product, segment, and firm" (PDF p. 185; framework §5).

---

## 8. The re-origination weight for Auto

- [FACT] The Eq A38 weight "is derived from the default rate, prepayment rate, and maturity rate" from the credit-loss models (PDF p. 183; md sec-151, sec-165) — **OQ-001, OPEN for retail**; no auto-specific wt statement exists.
- [INT] Auto is a fully-amortizing installment family: scheduled amortization and prepayment dominate contractual maturity as runoff drivers, so the Corporate maturity-date-only analogue (PID-LOAN-6) may fit auto poorly and must not be transplanted silently (framework §7.4). The workbook's auto runoff basis is elicitation item 3 (candidate PID).
- [FACT] The wholesale "conservative roll-off rate for fixed-rate loans" sentence sits in the **Wholesale Portfolio** limitations (PDF p. 186; md sec-171) — not available for retail; no retail roll-off characterization exists ([FACT] absence).

---

## 9. Floors for Auto

[FACT] The common rule applies ("All portfolios have a portfolio-specific interest rate floor…", PDF p. 180; common §7.1); no auto floor statement, value, or source exists — **OQ-002, OPEN for retail** (framework §8). Elicitation item 5; a floor census on the first run per the PID-SEC-18/PID-LOAN-25 lesson [CODE].

---

## 10. Inheritance register — what Auto does not restate

Auditable boundary; each row is governed by the cited brief and applies to Auto unchanged. (Corporate/CRE brief §9 discipline.)

| Rule | Governed by | Auto-specific note |
|---|---|---|
| Eq A32 income identity; 9 quarters; (b,p,i,t) | common §7.0 | — |
| Balance construction; flat balances; same-quarter replenishment | common §6 | Multiplicand wiring = elicitation item 2 |
| Rate type as the primary segmentation principle | common §7.2; framework §4.2 | Realized degenerately: all fixed (§6.1) |
| Eq A34 frozen existing rates; Eq A35 new-origination rate; Eq A38 blend | common §7.6 | The whole family runs here; OQ-033 firm dimension applies |
| Eq A36 retail spread branch | common §7.6; framework §7.1 | Auto measurement = **OQ-042** (§7) |
| Base rate = Prime (retail-except-mortgage rule) | framework §5 | Stated directly for auto too (PDF p. 178) |
| Eq A33 variable path | common §7.3 | **Never runs for auto** (§6.1 [INT]) |
| Interest-rate floors | common §7.1; framework §8 | OQ-002 retail leg (§9) |
| Industry-scalar mechanism; Table A8 values | common §8; framework §10 | Row applicability §11 |
| Assumptions (1)–(7); general limitations | common §12 | No auto-specific assumption list exists |
| Retail Portfolio limitations | framework §12 | Auto sentences quoted in §12 below |
| Quarterly compounding versus D-004 | common §7.7 | Unresolved at project level |
| Hedge exclusion (Question A159) | common §11 | Loans exclude hedges entirely; OQ-005 |

---

## 11. Table A8 row touching Auto

[FACT] Table A8 row **"Auto" = 0.865** (PDF p. 220; md sec-209; image-verified 2026-07-16/2026-08-03) — the only scalar below 1 apart from Credit Card. Footnote 63 lists "auto" as its own industry-scalar category (PDF p. 184 footer; md 5354).

**OQ-010 retail leg (open):** the Board states no category-to-row correspondence anywhere (SQ-11). "Auto" → the auto family is the natural reading and involves no naming-world span (contrast SME cards, framework §10), but it remains an inference; the project-side assignment is a candidate PID at this family's elicitation (item 6), following PID-LOAN-11/21. [CODE] The scalar map stays configuration with an unmapped-family hard error.

---

## 12. Fed-stated limitations bearing on Auto

The Retail Portfolio limitations subsection is owned by the framework brief §12; its auto-specific sentences:

[FACT] "Auto loans are reported at the segment level with limited interest information. It also limits the accuracy of auto-loan interest income estimation." (PDF p. 185; md sec-170; page image at high zoom 2026-08-12)

[INT] This is the Fed's own flag that the auto family's rate inputs are weak — the segment-level grain is both the family's data basis (§5 row 1) and its acknowledged accuracy limit. It sharpens OQ-042: if A.2's interest information is "limited", the new-origination-cohort reading of Equation A36 needs the cohort's rate to actually exist in the data.

[FACT absence] No other limitation names auto; no Board question does either (§13).

---

## 13. Board questions touching Auto

[FACT of absence] **No Board question names auto** — the single retail-directed question (A156) is about card revolver classification. Inherited: **A154** (segmentation comment request, both hierarchies — covers §3–§4), **A157** (scalar granularity), **A158** (spread factors), **A160** (general). Census verbatim in common §13.

---

## 14. Coding considerations — [CODE], non-normative

Nothing here is Fed methodology. No production Python in this phase; the engine extension is the follow-on gated task after this brief's review and elicitation.

- **Two-cell grid as configuration** (new/used × firm), engine = fixed only; the A33 path unreachable for auto by construction, stated in config rather than implied by data absence.
- **First segment-level ingestion contract.** Auto brings the loans workstream's first non-facility loader: expect a small sheet (segments × attributes), not a 30k-row facility panel; the contract (headers, units D-006, new/used vocabulary) is declared config after elicitation, refuse-to-run while unconfirmed — never inferred from magnitude.
- **Spread source as an explicit switch.** Until OQ-042 resolves, the spread derivation must name its basis (new-origination cohort rate vs all-loan segment rate vs supplied spread) as declared configuration, so the [INT] working reading stays visible and reversible (the PID-LOAN-22/23 lesson: the workbook's cells decide, and constructions differ per part).
- **wt input path per family** — auto's runoff basis is elicited, not inherited from Corporate's maturity-only PID-LOAN-6 (§8); guard wt ≤ 1 per quarter as in the wholesale engines.
- **HFS reclass as a censused no-op or a mapping rule** depending on elicitation item 7: if the firm carries HFS auto balances, fold them into HFI with a per-run census line; if none, record the rule as vacuously satisfied rather than dropping it.
- **Floor census on first run** (§9); scalar map = config with hard error (§11); Prime MEV column TO_BE_CONFIRMED refuses to run (framework §5.1).

---

## 15. Open questions

| ID | Status | Relevance to this brief |
|---|---|---|
| **OQ-042** | OPEN — **filed 2026-08-12 with this brief** | How the Eq A36 new-origination spread is measured for a segment-level family; the trend-analysis sentence vs the printed branch (§7) |
| **OQ-001** | OPEN for retail | wt inputs; auto is amortization/prepayment-dominated — the Corporate maturity-only analogue must not transplant silently (§8) |
| **OQ-002** | OPEN for retail | Floor values/source; no auto statement (§9) |
| **OQ-010** | OPEN for retail | "Auto" 0.865 row assignment is an inference; candidate PID at elicitation (§11) |
| **OQ-033** | OPEN | Firm dimension of the fixed-rate machinery — auto runs entirely on A34/A35/A36/A38; "by segment and by firm" (p. 178) joins the evidence set (§4.1) |
| OQ-040 / OQ-041 | OPEN — framework/other-consumer-owned | Cited only as boundaries; no auto content |

---

## 16. Source traceability table

| # | Claim / element | Class | PDF p. | md anchor | Verification |
|---|---|---|---|---|---|
| 1 | Auto is the second retail section | FACT | 177 | sec-156 | Page image 2026-08-12 |
| 2 | "reported in the FR Y-14Q schedule A.2 at the segment level" | FACT | 178 | sec-158 | Page image 2026-08-12 |
| 3 | All-fixed assumption, verbatim | FACT | 178 | sec-158 | Page image 2026-08-12 |
| 4 | HFS→HFI reclass at the firm level, FR Y-9C identified | FACT | 178 | sec-158 | Page image 2026-08-12 |
| 5 | New/used segmentation and its rationale | FACT | 178 | sec-158 | Page image 2026-08-12 |
| 6 | Balance-weighted average rates "by segment and by firm" as inputs | FACT | 178 | sec-158 | Page image 2026-08-12; OQ-033 evidence |
| 7 | Trend-analysis-vs-Prime spread sentence | FACT | 178 | sec-158 | Page image 2026-08-12; **OQ-042** |
| 8 | Origination-risk segments reviewed, not adopted | **ALT** | 178 | sec-158 | Page image 2026-08-12 |
| 9 | Eq A36 retail branch ("only new origination loans") | FACT | 182 | sec-165 | Page image 2026-07-30; transcription common §7.6 |
| 10 | "auto loans" in the fixed-rate prevalence note | FACT | 183 | sec-165 | Page image 2026-07-30 |
| 11 | Retail-limitation auto sentences ("segment level with limited interest information") | FACT | 185 | sec-170 | Page image at high zoom 2026-08-12 |
| 12 | Table A8 "Auto" 0.865; footnote 63 "auto" category | FACT | 220, 184 | sec-209, md 5354 | Page images 2026-07-16 / 2026-08-03; OQ-010 |
| 13 | International auto loans sit in Other Consumer | FACT | 180 | sec-160 | Page image 2026-08-12 |
| 14 | Suite-level schedule list omits Schedule A | FACT contrast | 172 vs 178 | sec-149 vs sec-158 | Page image 2026-08-12 (p. 178); integrity §9 |
| 15 | No Board question names auto | FACT absence | 186–188 | sec-172 | Page images 2026-07-30 |
| 16 | No retail PIDs exist; elicitation register | project record | — | — | §0.1 |

---

### Brief completion checklist

- [x] Status banner present; no adoption language anywhere.
- [x] Every material statement labeled [FACT]/[PID]/[INT]/[CODE]/[OQ]/[ALT]; unknowns stated UNKNOWN, never defaulted (PID register empty; elicitation items named logically only).
- [x] **Zero verbatim equation blocks** — equations cited from the common brief per D-010(b).
- [x] Both auto paragraphs verified against the p. 178 page image (2026-08-12); no new quirks found; the [ALT] label applied to the rejected risk segmentation.
- [x] Retail-shared rules cited from the framework brief, never restated (inheritance register §10); other families appear only as source-drawn boundaries.
- [x] The all-fixed and HFS-reclass consequences labeled [INT], separated from the stated assumptions.
- [x] No production Python; no confidential workbook content.
- [ ] Review state: DRAFT — awaiting user review gate (bundled with `ii_loans_retail.source-brief.md`).

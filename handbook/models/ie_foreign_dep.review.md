# Independent Source-Grounding Review — `ie_foreign_dep` chapter and YAML

**Review date: 2026-07-17.** Reviewer: this session, against the authoritative PDF page images (pp. 211–219 re-opened and read in full this session; not from the Markdown alone and not from the completed `ie_dom_time_dep` chapter, which was used as a formatting reference only).
Files under review: `handbook/models/ie_foreign_dep.md`, `handbook/models/ie_foreign_dep.yaml`.

## 1. Method

Every material claim in the chapter and YAML was traced to a PDF page image inspected this session. The v.a(8) framework pages (211–214) were verified in full because v.a(9) incorporates Equations A45–A47 by reference; Table A7 (p. 219) and the 44B usage in v.a(10) (p. 217) were also verified. The Markdown working copy was found to match the PDF at every checked point, consistent with `inventory/source-integrity-review.md`.

## 2. Verification register

| # | Claim (chapter/YAML location) | PDF page(s) | Verdict |
|---|---|---|---|
| 1 | "very similar" proposal wording; Y-9C equivalence; "smaller impact" (ch. §1) | 215 | **Verified verbatim** |
| 2 | "identical … with the exception" clause; rate items 43A ("foreign deposits") and 44B ("foreign deposits-time"); balances 35A/35B; beta items 83A, 83B, 84A, 84B (ch. §§2–3; yaml inputs) | 215 | **Verified** — the PDF names the four beta items as a flat list; it does **not** state which item is which subcomponent/direction (chapter correctly flags INT-b) |
| 3 | ELB definition: below 25 bp; non-ELB: above 25 bp (ch. §3.3, §6; yaml regime_test) | 211 | **Verified** — the = 25 bp case is genuinely unassigned in the prose; Eq A46's printed condition is "(Treasury3m_t > 25bps)" (p. 212, bottom) |
| 4 | Equation A45 incl. floor = Treasury3m + Spread; where-list (ch. §5; yaml A45) | 212 | **Verified** against the equation image |
| 5 | Spread estimation: "empirically estimated as the average distance between the deposit rate paid by the firm during the most recent effective lower-bound period"; window 2020:Q2–2021:Q4 (ch. §3.3, §6 step 2) | 212 | **Verified verbatim** — the sentence indeed omits the comparator ("…and the 3-month Treasury yield"); intent recoverable from Eq A45's Spread definition. Correctly flagged, not silently corrected |
| 6 | Equation A46 incl. δ, assumed_floor, First_ELB_Treasury3m verbatim definition (ch. §5; yaml A46) | 213 | **Verified** against the equation image |
| 7 | Median-beta statement ("median of the firm-reported betas for the respective deposit category at lift-off") and rationale (outliers, reliance on firm estimates) (ch. §6 step 3) | 213 | **Verified** |
| 8 | Equation A47 aggregation; Balance(i,b,t) where-list (ch. §5; yaml A47) | 213 | **Verified** |
| 9 | Expense step: aggregate rate × "average balance … as reported in the FR Y-14Q"; no line item named (ch. §7) | 214 | **Verified** — "average" confirmed on the page (December 2025 revision); absence of an item name confirmed |
| 10 | Inherited v.a(8) assumptions incl. the duplicated "A third assumption" labels (SQ-12) (ch. §8) | 214 | **Verified** — both paragraphs begin "A third assumption" |
| 11 | v.a(9) assumptions: one model for time and non-time (simplicity / Policy Statement); re-origination at 3M Treasury (no country-of-origin data; worldwide-recession rationale); no exchange-rate effects (ch. §8, quotes) | 215–216 | **Verified verbatim** |
| 12 | Question A179 verbatim (ch. §13) | 216 | **Verified**; the Questions intro on p. 216 correctly says "interest expense on foreign deposits" — **no SQ-4-type quirk in v.a(9)** |
| 13 | Table A7: Foreign Non-time up 0.890 / down 0.790; Foreign Time up 1.000 / down 1.000; SQ-1 down-row internal names; SQ-2 caption "(Equations A46)" (ch. §3.3; yaml parameters) | 219 | **Verified** — all four values match the table image |
| 14 | 44B as repo *balance* item ("securities sold under agreements to repurchase" of the NII Worksheet) vs. 44B as foreign-time *rate* item (ch. §12; yaml OQ-NEW-1) | 217 vs. 215 | **Verified** — both usages appear in the PDF as described |
| 15 | Constant-balance convention text used for INT-d (ch. §5) | 218 | **Verified** — "The stress test assumes constant balances for all firms; therefore, B(b,q) = B(b,q0)…" (stated within v.a(10); general statements also at pp. 169–170, not re-opened this session — citation retained from the verified integrity review) |
| 16 | Nine-quarter horizon; Table A6 row; "avoid statistical estimation" (ch. §§1–2) | 6, 168–169, 172–173, 218 | Horizon and Table A6 rely on the verified integrity review + p. 218's "Structural models avoid statistical estimation" (verified this session) |

## 3. Findings

1. **No discrepancy found** between the chapter/YAML and the PDF on any equation, line item, parameter value, quoted assumption, or question text.
2. **Label audit:** every material statement carries [FACT]/[INT]/[PID]/[CODE]/[OQ]/[ALT]; the five working assumptions are individually tagged (INT-a…INT-f, legend in ch. §12) and none is presented as Fed methodology. The ÷4 quarterly-dollar step is attributed to D-004, never to the Fed. Correct.
3. **Deliberate interpretations reviewed and endorsed:**
   - INT-a (expense balance = 35A + 35B): the source names 35A/35B as *this component's* balances and names nothing else; the analogous item-absence exists in v.a(7)/(8). Lowest-risk reading; correctly a candidate PID.
   - INT-b (beta-item mapping): immaterial to output because the model consumes Table A7 medians; correctly documented as feeding validation only.
   - INT-c/INT-f (seeds): the recursion cannot start without them; the source's silence is preserved as a fact of absence.
4. **Minor stylistic deviation, accepted:** the chapter uses the user-specified 13-section structure rather than the 14-section `chapter-template.md` layout, per the task instruction; template conventions (status banner, labels, citations, no production Python) are all honored.
5. **Not verifiable from the PDF (correctly marked UNCONFIRMED/UNKNOWN):** MEV column name for the 3M Treasury; Spread(i,b) values (require firm ELB-window history); MDRM codes (none stated, none invented).

## 4. New source-quirk / open-question candidates raised by this chapter

Recorded here only — shared files were deliberately not edited (task constraint).

| Candidate | Evidence | Suggested disposition |
|---|---|---|
| **SQ-candidate: item 44B double use** | p. 215 uses 44B as the "foreign deposits-time" **rate** item; p. 217 uses 44B as the "securities sold under agreements to repurchase" **balance** item of the same Schedule G NII Worksheet | Add to integrity review §8 (source quirk, both readings verbatim) + an OQ: resolve against the actual FR Y-14Q Schedule G instructions in the coding phase; do not guess which block renumbers |
| **SQ-candidate: elided Spread comparator** | p. 212: "average distance between the deposit rate paid by the firm during the most recent effective lower-bound period" — "between … and the 3-month Treasury yield" is grammatically incomplete | Add to integrity review §8; interpretation (distance **to the 3-month Treasury yield**) is fixed by Eq A45's Spread definition on the same page |
| **OQ-candidate: beta item mapping** | p. 215 lists items 83A, 83B, 84A, 84B without subcomponent/direction assignment | Add as a minor OQ (immaterial to output; matters only for the Table A7 reproduction validation) |
| **OQ-candidate: median recomputation vs. published Table A7** | p. 213: beta = "median of the firm-reported betas … at lift-off" implies recomputation each cycle; Table A7 (p. 219) publishes specific values "for the 2026 stress test" | Add as a minor OQ: whether an implementation should hard-code Table A7 or recompute medians at each lift-off |

## 5. Proposed shared-file updates (for the later integration session — not applied)

1. **`handbook/open-questions.md`**: file the two OQ-candidates from §4 (suggested IDs OQ-016 beta-item mapping, OQ-017 median recomputation vs. Table A7, OQ-018 44B collision — final numbering at integration); extend the D-004 "Where applied" column to name this chapter; record candidate PIDs for user confirmation: (a) expense balance = 35A + 35B, (b) beta-item mapping, (c) recursion seeds = lift-off 43A/44B, (d) MEV column name for the 3M Treasury (PID-5 analog), (e) Treasury3m = 25 bp → non-ELB branch (OQ-013 working choice).
2. **`inventory/source-integrity-review.md` §8**: add the two SQ-candidates (44B double use; elided Spread comparator), verbatim quotes as in §4 above.
3. **`inventory/model-inventory.md` #9**: add Question A179 to the record; note the INT-b flag on beta items and the 44B collision flag.
4. **Cross-chapter consistency**: when `ie_other_dom_dep` is drafted, Equations A45–A47 must be stated there as primary and cross-referenced from this chapter (this chapter already frames them as "by reference"); the two chapters must share one statement of the 2020:Q2–2021:Q4 spread window and the OQ-013 boundary choice.
5. **`handbook/open-questions.md` OQ-013**: extend the entry to note it now affects two chapters (`ie_other_dom_dep`, `ie_foreign_dep`) and record the working branch choice (= 25 bp → non-ELB) if the user confirms it as a PID.

## 6. Review conclusion

Both files are **source-faithful as drafted**: all Fed-attributed content matches the PDF page images; all non-Fed content is labeled and traceable to a decision, an interpretation with stated basis, or an open question. Chapter state remains **DRAFT** pending user review of the five candidate PIDs (§5.1) and integration of the shared-file updates.

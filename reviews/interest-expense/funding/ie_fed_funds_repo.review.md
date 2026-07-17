# Independent Source-Grounding Review — `ie_fed_funds_repo` chapter and YAML

**Review date: 2026-07-17.** Reviewer: this session, against the authoritative PDF page images (pp. 216–219 opened and read in full this session; current-model pages 150–152 read in the Markdown working copy for the separation check).
Files under review: `handbook/models/interest-expense/funding/ie_fed_funds_repo.md`, `specifications/interest-expense/funding/ie_fed_funds_repo.yaml`.

## 1. Verification register

| # | Claim | PDF page(s) | Verdict |
|---|---|---|---|
| 1 | **Equation A48**: F(b,t) = B(b,t)·Treasury3m(t); projection form F(b,q) = B(b,q)·Treasury3m(q); where-list "Treasury3m is the 3-month Treasury yield for quarter t"; no spread, scalar, or lag term | 217 | **Verified** against the equation image. The chapter and YAML transcribe it exactly; the rate is used raw |
| 2 | **Balance mapping 44A + 44B**: "the liabilities reported in line items 44A ('federal funds purchased') and 44B ('securities sold under agreements to repurchase') of the Net Interest Income Worksheet of FR Y-14Q, Schedule G" | 216–217 | **Verified verbatim.** The explicit sum 44A + 44B is not written in the source; "Let B_b be the total balance" (p. 217) supports it. Correctly labeled INT / candidate PID, not FACT |
| 3 | **Flat-balance treatment**: "The stress test assumes constant balances for all firms; therefore, B(b,q) = B(b,q0) for all periods … calculated based on the balances at lift-off" | 218 | **Verified verbatim.** Chapter §4 and YAML `balance_behavior` state Balance(b,q) = Balance(b,0), q = 1…9, measured once at PQ0; source word "lift-off" preserved in the quote per D-005 |
| 4 | **Annualized-rate conversion**: recursion-free model; AnnualizedRate(q) = Treasury3m(q) unmodified; ÷4 applied once, at the final quarterly-dollar step | 217–218 (absence) | **Verified as correctly attributed.** v.a(10) states no unit basis and no quarterly conversion; the ÷4 is labeled PID (D-004) everywhere and never attributed to the Fed. The rate is not pre-divided before the rate assignment, matching the project convention |
| 5 | **Absence of coefficients or scalars**: "simplicity (since it does not involve coefficients estimation)"; no beta, firm scalar, autoregression, fixed effect, floor, or threshold anywhere in v.a(10); Tables A7–A9 contain no row for this component | 218, 219 (Table A7), 234 (Table A9 by earlier session) | **Verified.** p. 218 quote confirmed on the page image; Table A7 (p. 219, image read this session) lists deposit betas only. `parameters: none` is correct |
| 6 | **Separation from the current model**: current Eq A27 (PDF pp. 150–152) computes a firm-specific launch-point scalar k_b = F(b,0)/(B(b,0)·Treasury3m(0)) on FR Y-9C balances; proposed A48 has no k_b and uses FR Y-14Q items | 150–152 vs. 217 | **Verified.** The chapter cites A27 once, in §1 and §11, as contrast only; no k_b, no FR Y-9C balance, and no A27 mechanics appear in the A48 workflow or YAML. No methodology mixing found |
| 7 | **Equation-title typo**: the A48 title on p. 217 reads "…Securities Sold under the **Agreement to Purchase**"; the section (10) header on p. 216 and all section prose correctly say "Repurchase" | 216–217 | **Verified on the page images.** The typo is preserved verbatim only as an integrity note (chapter banner + §3; YAML `source_title_verbatim`); the model name used throughout is the correct "…Agreements to Repurchase". Treatment matches the task requirement |

Additional spot-checks, all verified: assumptions/limitations quotes incl. the special/rare-collateral caveat (p. 218); Question A180 (pp. 218–219); Table A6 "Structural" row (pp. 168–169, from the verified integrity review); December 2025 revision note for p. 216 (PDF pp. 4–5); the 44B collision with the v.a(9) foreign-time rate item (p. 215 vs. p. 217) is cross-referenced to the existing `ie_foreign_dep` review rather than re-filed. YAML parses (checked with a YAML parser this session).

## 2. Findings

- **MATERIAL: none.** Every equation, line item, quote, and citation checked traces to the PDF; interpretations (44A + 44B sum) and project conventions (÷4, canonical `usd_3m_treasury`) are labeled and never attributed to the Fed.
- **MINOR-1:** The chapter's §11 reference for current-model Y-9C item codes (BHDMB993 + BHCKB995, PDF p. 37 data table) was verified against the Markdown working copy only, not the PDF page image. Comparison-only content; no bearing on the A48 model. Acceptable as cited.
- **MINOR-2:** The MEV workbook column name for `usd_3m_treasury` is recorded as a CODE implementation-mapping TODO (per task instruction), consistent with the unresolved PID-5-pattern naming in the sibling deposit chapters. No action within this chapter.

## 3. Suggested shared-file changes (for the later integration session — not applied)

1. **`inventory/model-inventory.md`**: add/extend the v.a(10) entry: model id `ie_fed_funds_repo`, Table A6 type Structural, Eq A48, items 44A/44B, Question A180, and the A48-title typo flag.
2. **`inventory/source-integrity-review.md` §8**: add SQ-candidate — Equation A48 title typo "Agreement to Purchase" (PDF p. 217), verbatim; note the section header on p. 216 is correct.
3. **`handbook/open-questions.md`**: record candidate PID — component balance = item 44A + item 44B (INT in chapter §2.1); extend the D-004 "Where applied" column to name this chapter; extend the existing 44B-collision OQ-candidate (raised in the `ie_foreign_dep` review) to note it now touches two shipped chapters.
4. **`inventory/source-map.md`**: map sec-205…sec-208 → `ie_fed_funds_repo` artifacts.

## 4. Verdict

**APPROVE** — no MATERIAL findings; the two MINOR notes require no chapter change.

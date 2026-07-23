# Independent Source-Grounding Review — `ii_dep_banks_other` chapter and YAML

**Review date: 2026-07-23.** Reviewer: this session, against the authoritative PDF page images (pp. 188–190 opened and read in full this session; structural-intro and Table A6 claims cross-checked against md sec-148/sec-149 and the verified `inventory/source-integrity-review.md`).
Files under review: `handbook/models/interest-income/calculators/ii_dep_banks_other.md`, `specifications/interest-income/calculators/ii_dep_banks_other.yaml`.
Gate context: drafted at asset-side Increment 1; this source-grounding review precedes the **user review gate** — the chapter is not final until user-reviewed.

## 1. Verification register

| # | Claim | PDF page(s) | Verdict |
|---|---|---|---|
| 1 | **Equation A39**: F(b,t) = B(b,t)·Treasury3m(t); where-list "Treasury3m is the 3-month Treasury yield."; projection form F(b,q) = B(b,q)·Treasury3m(q); no spread, scalar, or lag term | 189 | **Verified** against the equation image. Chapter §5 and YAML transcribe it exactly; the A39 display carries the t subscript on Treasury3m (unlike A43's display) — transcription faithful |
| 2 | **Balance sourcing**: "The relevant balances are reported in line item 14 of the net interest income worksheet of FR Y-14Q, Schedule G"; composition "interest-bearing deposits, including deposits held at the Federal Reserve and other institutions such as the Federal Home Loan Banks"; "short durations, typically less than a single quarter" | 188 | **Verified verbatim.** The balance item is **source-stated** — correctly presented as FACT with no correction PID (contrast with the deposit-expense models); only the physical sheet row is a CODE TO_BE_CONFIRMED |
| 3 | **Flat-balance treatment**: "The stress test assumes constant balances for all firms; therefore, B(b,q) = B(b,q0) for all periods … calculated based on the balances at the last quarter before the start of the projection" | 189 | **Verified verbatim.** Chapter §4 and YAML `balance_behavior` state Balance(b,q) = Balance(b,0), q = 1…9, measured once at PQ0; source word "lift-off" preserved in the quote per D-005 |
| 4 | **Assumptions and limitations**: rate = 3-month U.S. Treasury; "the rate that the Federal Reserve pays on reserves tracks the 3-month U.S. Treasury rate closely, some fluctuations may be observed"; "the rates paid by other depository institutions may be higher or lower" | 189–190 | **Verified verbatim** on the page images. Chapter §8 restates all three faithfully, all [FACT] |
| 5 | **Annualized-rate conversion**: AnnualizedRate(q) = Treasury3m(q) unmodified; ÷4 applied once, at the final quarterly-dollar step; labeled D-004, never attributed to the Fed | 188–190 (absence) | **Verified as correctly attributed.** v.a(2) states no unit basis and no quarterly conversion; the chapter preserves the FACT absence (OQ-006 resolution language) |
| 6 | **Absence of parameters**: no beta, scalar, spread, floor, threshold, or estimated coefficient anywhere in v.a(2); Tables A7–A9 contain no row for this component | 188–190; 219–220, 234 (tables, from the verified integrity review and expense-side sessions) | **Verified.** `parameters: none` is correct; the structural-intro quote "avoid statistical estimation" (pp. 172–173; md sec-149) matches the md working copy read this session |
| 7 | **SQ-4 — Questions intro misnomer**: the intro on p. 190 reads "this proposed model for **interest income on loans**" although the section is the deposits-with-banks model | 190 | **Verified on the page image — the misnomer is in the PDF itself**, not conversion damage. Preserved in the banner and §8 as an integrity note; never "corrected" in quoted text |
| 8 | **SQ-3 — question-numbering collision**: this section's Questions are A161/A162; component (3) also starts at A161 | 190 (this section); 193–194 (component (3), per integrity review) | **Verified for this section** (A161/A162 text on the image); the collision itself was filed 2026-07-16 (integrity review) — chapter cites questions with their section, per the established rule |
| 9 | **Current-model contrast**: "as compared to the Board's current panel regression model" (Question A161) is the chapter's only current-model claim | 190 | **Verified verbatim.** The chapter deliberately imports no current-suite mechanics — no mixing found |

Additional spot-checks, all verified: Table A6 "Structural" row (pp. 168–169, via the verified integrity review); nine-quarter horizon (p. 6, established project citation); the [INT] navigation note that A39 shares Eq A48's functional form makes no dependency claim and is correctly labeled INT. YAML parses and follows `specifications/model-spec-guidelines.md` key order (§3 table) with the required header block.

## 2. Findings

- **No MATERIAL findings.** Every equation, quote, and citation checked traces to the PDF page images; interpretations and project conventions (D-004 ÷4, D-006 units, canonical series names, physical-row working assumptions) are labeled and never attributed to the Fed.
- **MINOR-1:** The chapter's two TO_BE_CONFIRMED items (physical spot-sheet row for item 14; MEV column name for `usd_3m_treasury`) are correctly framed as CODE implementation mappings — candidate PIDs at company-reference verification, not methodology uncertainty. No action.
- **MINOR-2:** Chapter numbering ("# 2.") follows the inventory census (#2); the asset-side chapter-number sequence is recorded in `inventory/asset-side-model-matrix.md`. No action.

## 3. Shared-file changes (applied this session — Increment 1)

1. **`inventory/asset-side-model-matrix.md`**: row for `ii_dep_banks_other` — DRAFTED, awaiting user review.
2. **`handbook/open-questions.md`**: D-009 (compact chapter skeleton) recorded; no new OQ from this chapter (SQ-3/SQ-4 already filed 2026-07-16).
3. **`inventory/source-map.md`** and inventory #2 artifact row: deferred to the asset-side integration gate, mirroring the liability-side practice.

## 4. Verdict

**APPROVE (source-grounding)** — no corrections required; the chapter is source-faithful as drafted. Final acceptance remains with the **user review gate** (Increment 1) before any code is written against it.

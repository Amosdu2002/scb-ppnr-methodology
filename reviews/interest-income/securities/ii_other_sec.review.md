# Independent Source-Grounding Review — `ii_other_sec` chapter and YAML

**Review date: 2026-07-23.** Reviewer: this session, against the authoritative PDF page images (PPNR pp. 201–203 opened and read in full; p. 205 previously image-verified at Increment 1; A42 spelling settled via a PDF **text-layer glyph-count check** — the decisive new evidence this session). Remaining prose (pp. 200, 204) verified against the md working copy (fidelity per `inventory/source-integrity-review.md` §4/§9).
Files under review: `handbook/models/interest-income/securities/ii_other_sec.md`, `specifications/interest-income/securities/ii_other_sec.yaml`.
Gate context: drafted at asset-side Increment 2; this review precedes the **user review gate**.

## 1. Verification register

| # | Claim | Where | Verdict |
|---|---|---|---|
| 1 | **Equation A42 spelling — SQ-8 refinement**: main equation line "AccrectionAmortization" (typo); where-list "AccretionAmortization" (correct) | PDF p. 201 (image + text layer) | **Verified and newly settled.** Glyph-count check: the 22-letter A-run sits in the main equation line (offset before the where-list), the 21-letter run in the where-list. **SQ-8 refined** (typo confined to the main line); **CA-4 filed** — the md typo'd both spots (lines 3999/4003), so the md where-list deviates from the PDF. The chapter quotes each spot with its correct PDF spelling |
| 2 | **Combined term**: Coupon Accrual + AccretionAmortization = Amortized Cost(t) × Book Yield(t)/4; hedge term separate | PDF p. 201 (image) | **Verified** — the collapsed variant presented as printed; the ÷4 correctly labeled source-stated |
| 3 | **Book-yield source and floating-margin imputation** (t=0 coupon, t=0 spot 3M, margin added forward) | PDF p. 201 (image) | **Verified verbatim** |
| 4 | **No prepayments + rationale** ("broad number of asset classes"); **effective-interest method** with constant coupon and book yield; **straight-line fallback**; hedge zero with the B.2/B.3 proposal attributed "In the Securities Model Description"; Portfolio Layer Method | PDF p. 202 (image) | **Verified verbatim** — including the third explicit tie to the second source, which the chapter cites |
| 5 | **Reinvestment paragraph with referral sentence present**; first-day purchases | PDF p. 203 (image) | **Verified verbatim** |
| 6 | **"is considering" status wording** (vs. "proposes" in v.a(3)/(4)) | PDF p. 200 (md; wording also present in the p. 201 rationale image context) | **Verified** — preserved as FACT with no significance attached, per the quirk-handling rule |
| 7 | **AC(t) path absence**: no formula for amortized-cost evolution under the effective-interest method | PDF pp. 201–202 (FACT absence) | **Verified.** The chapter's [INT] (AC evolves per the effective-interest schedule) and the bucket-level AC-path proposal are labeled, not attributed |
| 8 | **Assumptions 1–5** with source spellings "projects"/"principle" preserved in the no-prepayment caveat | PDF pp. 203–204 (p. 203 image; p. 204 md — the same passage was read at the Increment 1 `ii_other_ida` session as md lines 4024–4033) | **Verified**; the deliberate preservation of the source's spellings is the correct quoting discipline |
| 9 | **CA-2e** (md stray pipe, line 4013) | PDF p. 202/203 images vs. md | **Confirmed md-only**; already filed 2026-07-16 |

Additional checks: Questions A169–A174 verified against the md (A174's "(detailed within the Securities Model Description)" phrasing confirmed on the p. 205 image at Increment 1); the floating-bucket insertion into the A42 term is flagged [INT] in §6 step 3 — an honest gap, the source states the imputation but not its exact slot in the collapsed formula. YAML parses and follows the guideline key order (checked this session).

## 2. Findings

- **MATERIAL (resolved by filings, no chapter change): the md working copy deviates from the PDF in A42's where-list spelling** — discovered by this review's text-layer check and filed as **CA-4** with the **SQ-8 refinement**. The chapter transcribes both spots per the PDF, which now supersedes the md for this equation.
- **MINOR-1:** AC-path treatment is a gate decision (candidate PID-SEC-1 scope); until decided the spec offers supplied-AC-path vs. launch-AC + fallback options — both labeled. No action before the gate.
- **MINOR-2:** p. 200/204 verified against md only. Acceptable under the established coverage rule.

## 3. Shared-file changes (applied this session — Increment 2)

1. `inventory/source-integrity-review.md`: **SQ-8 refined; CA-4 filed**; §9 coverage updated (pp. 191–193, 196–198, 201–203 images; text-layer method documented); §11 extended (MRM pages image-verified; extracts file).
2. `handbook/open-questions.md`: OQ-004 resolved; OQ-025 filed (shared).
3. Conventions §12; extracts file; matrix updates.

## 4. Verdict

**APPROVE (source-grounding)** — source-faithful as drafted, and the review itself tightened the source-integrity record (SQ-8 refinement + CA-4). Final acceptance remains with the **user review gate** (Increment 2).

# Independent Source-Grounding Review — `ii_ust` chapter and YAML

**Review date: 2026-07-23.** Reviewer: this session, against the authoritative PDF page images (PPNR pp. 191–193 opened and read in full; MRM pp. 72–74 and the MRM p. 68 region via the extracts verification; A40 spelling and the "Maturity in Quarter" wording additionally settled via the PDF **text layer** — a glyph-count check, since the equation objects defeat both image reading and plain extraction). Remaining prose (pp. 190, 194–195) verified against the md working copy, whose equation/footnote fidelity for this scope stands per `inventory/source-integrity-review.md` §4/§9.
Files under review: `handbook/models/interest-income/securities/ii_ust.md`, `specifications/interest-income/securities/ii_ust.yaml`.
Gate context: drafted at asset-side Increment 2; this review precedes the **user review gate**.

## 1. Verification register

| # | Claim | Where | Verdict |
|---|---|---|---|
| 1 | **Equation A40**: three-term sum; coupon accrual = face(t) × coupon/4; accretion = (face(t=0) − AC(t=0)) ÷ Maturity-in-Quarter(t=0); hedge = notional × (Pay − Receive)/4 | PDF p. 191 (image) | **Verified.** t=0 dating of both accretion arguments confirmed on the image; "Maturity in Quarter" singular confirmed via text layer (Q-run = 7 letters); "AccretionAmortization" correctly spelled (21-letter A-runs, twice) |
| 2 | **Beginning-of-period face; vendor coupon "may not be available"; straight-line accretion; hedge zero + proposed B.2/B.3 + Portfolio Layer Method allocation** | PDF p. 192 (image) | **Verified verbatim.** The chapter's [FACT absence] that **no coupon fallback is stated for this component** (unlike v.a(4)'s book-yield fallback) is confirmed — filed as OQ-027 |
| 3 | **Maturity incorporation + reinvestment**: constant balance via reinvestment; "The same reinvestment assumption is used across both…"; fn 64 "See Securities Model Description."; purchases on the first day of the subsequent quarter | PDF pp. 192–193 (images) | **Verified verbatim**, including footnote 64 on the p. 193 image |
| 4 | **Reinvestment detail**: hypothetical 1Y Treasury, purchased at face value, coupon = par-curve yield at the forecast quarter; AFS/HTM intent preserved; no hedges; explicit cross-link to "the proposed structural model for interest income on securities" | MRM p. 73 (image) | **Verified verbatim** on the page image. The chapter's [INT] identification (this passage = the referenced assumption) rests on that explicit cross-link plus the maturity-incorporation logic — correctly labeled INT with basis |
| 5 | **Matured security ceases to exist; proceeds reinvested and revalued** | MRM p. 68 fn 54 (extract; page image not separately opened) | **Verified against the pdftotext extract**; applied to income as [INT] — correctly labeled |
| 6 | **No-accretion-on-reinvestments consequence** | chapter §6.4 / conventions §12 | **Verified as INT**: follows from "purchased at face value" (MRM p. 73, FACT) — a purchase at face carries no discount/premium; labeled INT, not attributed to the Fed |
| 7 | **Assumptions and limitations** (hedge-data gap; reinvestment materiality "outsized impact"; OCI-release and terminated-hedge exclusions) | PDF pp. 193–194 (p. 193 image; p. 194 md) | **Verified** (p. 193 verbatim on image; p. 194 against md — md fidelity per integrity review §4) |
| 8 | **Questions A161–A164 numbering (SQ-3 collision with v.a(2))** | PDF pp. 194–195 (md) + SQ-3 filing | **Verified** — chapter cites with section per the established rule |
| 9 | **Absence of parameters and scenario variables in the existing-book calculation** | PDF pp. 190–193 | **Verified.** A40 contains no scenario term; Tables A7–A9 carry no row. The 1Y-Treasury scenario need arises only from the reinvestment (MRM), correctly cited there |

Additional checks: the granularity proposal and bucket sketch are confined to §9/[CODE] and the spec with candidate-PID status — no aggregation invention is presented as Fed methodology. YAML parses and follows the guideline key order (checked this session).

## 2. Findings

- **No MATERIAL findings.** All equations and material statements trace to page images or the verified md; the one methodology gap discovered (missing-coupon fallback unstated) is preserved as OQ-027 rather than silently borrowing v.a(4)'s fallback.
- **MINOR-1:** MRM p. 68 fn 54 was verified from the pdftotext extract, not a page image. Context-level claim only; the load-bearing reinvestment content (MRM pp. 72–74) was image-verified. Acceptable.
- **MINOR-2:** The chapter's beginning-of-period reading (a security contributes coupon through its maturing quarter) is labeled [INT]; the source states the beginning-of-period convention but not the maturing-quarter cut explicitly. Correctly flagged.

## 3. Shared-file changes (applied this session — Increment 2)

1. `handbook/open-questions.md`: OQ-004 resolved; **OQ-025** and **OQ-027** filed.
2. `handbook/cross-cutting/asset-side-common-conventions.md` §12: securities shared machinery added.
3. `sources/fed/market-risk-models-securities-extracts.md`: scoped second-source working copy created.
4. `inventory/asset-side-model-matrix.md` and `inventory/source-integrity-review.md`: status and verification-coverage updates.

## 4. Verdict

**APPROVE (source-grounding)** — source-faithful as drafted; the reinvestment-detail incorporation is correctly split into MRM [FACT] and linkage [INT], and the granularity proposal is cleanly quarantined as a gate decision. Final acceptance remains with the **user review gate** (Increment 2).

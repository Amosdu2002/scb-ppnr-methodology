# Independent Source-Grounding Review — `ii_mbs` chapter and YAML

**Review date: 2026-07-23.** Reviewer: this session, against the authoritative PDF page images (PPNR pp. 196–198 opened and read in full; MRM pp. 18–20 — the vendor-model passage — opened and read in full; A41 spelling settled via the PDF text layer). Remaining prose (pp. 195, 199–200) verified against the md working copy (fidelity per `inventory/source-integrity-review.md` §4/§9).
Files under review: `handbook/models/interest-income/securities/ii_mbs.md`, `specifications/interest-income/securities/ii_mbs.yaml`.
Gate context: drafted at asset-side Increment 2; this review precedes the **user review gate**.

## 1. Verification register

| # | Claim | Where | Verdict |
|---|---|---|---|
| 1 | **Equation A41**: three-term sum; coupon accrual = face(t) × coupon/4; accretion = (face(**t**) − AC(**t**)) ÷ (4 × WAL(t=0)); hedge term | PDF p. 196 (image) | **Verified**, including the **t-dated numerator** (deliberately contrasted with A40's t=0 — the chapter preserves the asymmetry). Spelling "AccretionAmortization" **confirmed correct** via text layer (21-letter runs twice) — SQ-8 remains A42-only |
| 2 | **Agency RMBS vendor statement**: "a vendor model is used to calculate the income to better reflect the impacts of prepayments"; used across both income and the Securities Model; fn 65 referral | PDF p. 196 (image) | **Verified verbatim.** The chapter's OQ-026 (vendor output vs. A41-term composition unstated) is a genuine absence — v.a(4) never says how they compose |
| 3 | **Other-MBS coupon rules**: vendor coupon with **book-yield fallback**; zero-coupon accrues at book yield; floating margin imputed from t=0 coupon and t=0 **spot** 3M, margin added forward | PDF p. 196 (image) | **Verified verbatim** |
| 4 | **Category methods**: no prepayments for non-Agency (mostly CMBS); Agency accretion straight-line leveraging t=0 WAL; other MBS effective interest with constant coupon+book yield, straight-line fallback; hedge zero + B.2/B.3 + Portfolio Layer Method | PDF p. 197 (image) | **Verified verbatim.** The chapter's [INT] flag that A41's printed accretion form matches the *Agency* description while the effective-interest method has **no printed formula** is an accurate reading of the page |
| 5 | **Reinvestment paragraph**: constant balance via reinvestment; same-assumption statement; first-day purchases; **no referral sentence in this section** | PDF p. 198 (image) | **Verified** — the referral-sentence omission is real (present in v.a(3) p. 193 and v.a(5) p. 203); chapter notes it as a faithful difference with no significance attached |
| 6 | **Vendor-model mechanics**: Monte Carlo paths conditional on the macro scenario; voluntary+involuntary prepayments; zero-coupon-Treasury+OAS discounting; average across paths; default calibration, no overlay; aging and paydown incorporated; **itemized macro inputs** (mortgage rate, prime, unemployment, HPI, zero-coupon Treasury + SOFR curves) and MBS/CMO OAS auxiliary indices | MRM pp. 18–19 (images) | **Verified verbatim** on the page images, including the fn 17/18 details the extracts record |
| 7 | **Assumptions 1–6** incl. "(except for Agency residential mortgage-backed securities)" in the margin caveat and the vendor-reliance sentence | PDF pp. 198–199 (p. 198 image; p. 199 md) | **Verified** |
| 8 | **CA-2d** (md stray pipe after "…will be zero.", line 3933) | PDF p. 197 image vs. md | **Confirmed md-only** — no pipe on the page; already filed 2026-07-16 |
| 9 | **WAL unit = years** | A41's 4× factor | **Verified as INT** — unit not stated; the 4× conversion implies years; correctly flagged for company-reference confirmation |

Additional checks: the declared-vendor-path treatment (candidate PID-MBS-1) is presented strictly as a project proposal — the Fed's vendor model is described [FACT] but never claimed to be reimplementable; Questions A165–A168 numbering verified against the md. YAML parses and follows the guideline key order (checked this session).

## 2. Findings

- **No MATERIAL findings.** The two-regime structure (vendor category vs. calculated category) is presented exactly as the source splits it, and the one genuine composition gap is OQ-026 rather than an invented reconciliation.
- **MINOR-1:** The chapter takes the vendor path as the Agency category's **total** pre-hedge income (working treatment under OQ-026) — clearly labeled [CODE working treatment], revisit at the gate if the user's vendor output is shaped differently.
- **MINOR-2:** Questions pages (199–200) verified against md only. Acceptable under the established coverage rule.

## 3. Shared-file changes (applied this session — Increment 2)

1. `handbook/open-questions.md`: **OQ-026** filed; OQ-004 resolved.
2. Conventions §12; extracts file; matrix and integrity-review updates (as listed in the `ii_ust` review §3).

## 4. Verdict

**APPROVE (source-grounding)** — source-faithful as drafted; the vendor boundary and the A41 formula-to-category mapping are the two delicate spots and both are labeled with their exact evidentiary status. Final acceptance remains with the **user review gate** (Increment 2).

# Independent Source-Grounding Review — `ie_other_dom_dep` chapter + YAML spec

Review date: 2026-07-17. Reviewer: this session, against the authoritative PDF (pages re-read as page images: 211, 212, 213, 214, 215, 219). Files reviewed: `handbook/models/interest-expense/deposits/ie_other_dom_dep.md`, `specifications/interest-expense/deposits/ie_other_dom_dep.yaml` (formerly `ie_other_dom_dep.spec.yaml`). Method: every equation, line item, parameter value, quoted passage, and citation in both files compared line-by-line against the PDF page images; interpretations checked for correct [INT]/[PID]/UNKNOWN labeling; cross-checked against `inventory/source-integrity-review.md`, `inventory/model-inventory.md` (#8), `inventory/source-map.md` (§4.2), and `handbook/open-questions.md`.

## 1. Verification results (all PASS unless noted)

| # | Check | Against | Result |
|---|---|---|---|
| 1 | Eq A45 (Rate = floor = Treasury3m + Spread), incl. where-list | PDF p. 212 image | PASS — transcription exact |
| 2 | Eq A46 (max(Rate(t−1) + δ, assumed_floor)); δ up/down-beta form; assumed_floor; First_ELB_Treasury3m definition incl. "(if available)" | PDF p. 213 image | PASS — exact; δ carries subscripts i,t only (no b), as the chapter states |
| 3 | Eq A47 balance-weighted aggregation; "balance reported in the Y-14Q corresponding to the rate i" (no line item named) | PDF p. 213 image | PASS — the chapter's UNKNOWN mapping is a true fact of absence |
| 4 | Rate items 42B/42C/42D; beta items 79A/79B/80A/80B/81A/81B; "median of the firm-reported betas … at lift-off"; median rationale | PDF p. 213 image | PASS |
| 5 | Regime triggers: ELB "below 25 basis points", non-ELB "above 25 basis points"; A46 condition "(Treasury3m_t > 25bps)" | PDF pp. 211–212 images | PASS — =25 bp genuinely unassigned (OQ-013 correctly carried) |
| 6 | Expense sentence: aggregate rate × "average balance on other domestic deposits as reported in the FR Y-14Q"; no ÷4 stated by the source | PDF p. 214 image | PASS — chapter §7 correctly splits [FACT] product form from [PID D-004] ÷4 |
| 7 | Four assumptions, incl. two consecutive "A third assumption" labels (SQ-12); "abstracts from" wording (Dec 2025 revision item 5) | PDF p. 214 image | PASS — preserved verbatim, never corrected |
| 8 | Question A178 verbatim | PDF p. 215 image | PASS — note the question says "other deposits", not "other domestic deposits" (observation only; the section heading names the component correctly) |
| 9 | Table A7: caption "(Equations A46)" (SQ-2); Down-row internal names (SQ-1); values MMA 0.620/0.645, Savings 0.310/0.335, Other (transaction) 0.465/0.490; "Board calculated these parameters based on data submitted on Form FR Y-14Q" | PDF p. 219 image | PASS — all six domestic values match chapter §3.3 and YAML exactly |
| 10 | Foreign-deposits reuse boundary (items 43A/44B, 35A/35B, 83A–84B) | PDF p. 215 image | PASS |
| 11 | SQ-9 ("indicats", A45 where-list) | PDF p. 212 image | INCONCLUSIVE at render resolution — deferred to the integrity review's 2026-07-16 verification (md carries "indicats"; conversion certified faithful). Chapter cites SQ-9 as logged; no change |
| 12 | Every citation (PDF p.; md sec-) in both files | source map §4.2 anchors | PASS — sec-197…sec-200, sec-209 assignments correct |
| 13 | Label discipline: no [FACT] without citation; every interpretation carries [INT] with stated basis; ÷4, MEV column name, and balance hypotheses never presented as Fed statements | both files | PASS |

**No corrections to the chapter or YAML were required during review.** Both files match the PDF at every checked point.

## 2. Findings requiring follow-up (none block the chapter)

- **F-1 — New source-quirk candidate (PDF itself, p. 212).** "The firm-specific spread to the 3-month Treasury yield is empirically estimated as the average distance between the deposit rate paid by the firm during the most recent effective lower-bound period." — "distance between X during Y" is missing its second endpoint; confirmed present in the PDF page image, not a conversion artifact, and **not yet logged** in `inventory/source-integrity-review.md` §8. Interpretation (safe): the omitted endpoint is "and the 3-month Treasury yield", per the sentence's own subject and the A45 where-list.
- **F-2 — Balance mappings unnamed in source — RESOLVED FOR PROJECT IMPLEMENTATION (user confirmation, 2026-07-17, post-review).** Neither the A47 subcomponent balances nor the §7 aggregate "average balance" has a named line item in the Fed source (preserved as [FACT] absence). User-confirmed mappings, recorded as **PID-ODD-1** (subcomponent balances = FR Y-14Q Schedule G items 34B (MMA), 34C (Savings), 34D (NOW, ATS, and other Transaction Accounts)) and **PID-ODD-2** (total average balance = sum of MDRM items BHCB3187 + BHOD3187 + BHCB2389 + BHOD2389). PID-ODD-2 supersedes the earlier "aggregate = Σ subcomponents" hypothesis — the A47 weights and the expense multiplicand now come from different physical sources, kept as a chapter §10 consistency monitor. Noted, not resolved: the source sentence says "FR Y-14Q" while PID-ODD-2 is expressed in MDRM codes; the mapping governs for implementation.
- **F-3 — Spread estimation mechanics underspecified.** Sign convention (signed vs. absolute distance), averaging frequency over 2020:Q2–2021:Q4, and treatment of firms lacking that history are all unstated.
- **F-4 — Seed timing [INT].** Rate(i,b,0) as the t=1 lag of Eq A46, and use of the jump-off Treasury3m in ΔTreasury3m(1), are interpretations; the source retrieves the 42B–42D rates without stating the seed mechanics.

## 3. Proposed shared-file updates (for the later integration session — NOT applied here)

1. **`inventory/source-integrity-review.md` §8** — add quirk **SQ-15** (per F-1): PDF p. 212, verbatim sentence above; INTERPRETATION column: omitted endpoint = "and the 3-month Treasury yield" (high confidence, from the A45 where-list). Also consider extending §9's verified-page list note (pp. 211–215, 219 re-verified 2026-07-17, no new defects).
2. **`handbook/open-questions.md`** — file entries (draft text ready in chapter §12 and F-2…F-4):
   - **OQ-016** — Other-domestic-deposit balance line-item mappings unnamed in source. File directly as **RESOLVED FOR PROJECT IMPLEMENTATION (2026-07-17)** via PID-ODD-1/PID-ODD-2 (see F-2), preserving the source-side absence as [FACT], mirroring the OQ-008 pattern.
   - **OQ-017** — Spread(i,b) estimation mechanics: truncated sentence (→ SQ-15), sign convention, averaging frequency, missing-history firms; resolves by Fed clarification; interim: signed-difference average flagged [INT].
   - **OQ-018** — Recursion seed timing (rate lag at t=1; jump-off Treasury3m in Δ at t=1); resolves by Fed clarification; interim [INT] recorded in chapter §4/§6.
3. **`inventory/model-inventory.md` record #8** — after (1) and (2): add SQ-15 to the integrity-flags row; extend the open-questions row to OQ-016 (resolved)/017/018; optionally note the PID-ODD-1/2 mappings in the firm-data-inputs row. Values and equations in the record were re-verified — no other change needed.
4. **`handbook/open-questions.md` decision log** — record **PID-ODD-1** and **PID-ODD-2** (user-confirmed 2026-07-17) as decision-log entries binding this component's balance mappings; D-004 applied as-is, no other new decision required.
5. No changes needed to `inventory/source-map.md` or to any other chapter.

---

## Addendum — 2026-07-23 (post-review revision, user-confirmed)

**PID-ODD-3 supersedes PID-ODD-2's multiplicand role.** Empirical validation against the
company reference implementation (all per-subcomponent and aggregate rates verified
identical; the reference expense matched aggregate rate × Σ(34B+34C+34D), not × the
PID-ODD-2 MDRM sum) confirmed the expense multiplicand is the A47 weight-balance sum —
expense ≡ Σᵢ rateᵢ × balanceᵢ. `odd_total_average_balance` (the PID-ODD-2 MDRM sum) is
now an optional input serving only the consistency monitor. Registry:
`handbook/open-questions.md`; chapter §3.1/§7/§9/§10; YAML inputs/equations/validations.
The historical body above is preserved unchanged.

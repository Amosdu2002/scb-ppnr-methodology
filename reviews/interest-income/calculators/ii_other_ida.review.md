# Independent Source-Grounding Review — `ii_other_ida` chapter and YAML

**Review date: 2026-07-23.** Reviewer: this session, against the authoritative PDF page images (pp. 205–208 opened and read in full this session, including the footnote-66 region of p. 206; the v.a(10) subsumption statement cross-checked against the previously verified p. 217 claims in the `ie_fed_funds_repo` package).
Files under review: `handbook/models/interest-income/calculators/ii_other_ida.md`, `specifications/interest-income/calculators/ii_other_ida.yaml`.
Gate context: drafted at asset-side Increment 1; this source-grounding review precedes the **user review gate** — the chapter is not final until user-reviewed.

## 1. Verification register

| # | Claim | PDF page(s) | Verdict |
|---|---|---|---|
| 1 | **Equation A43**: F(b,t) = α(b,t)·B(b,t)·Treasury3m + (1 − α(b,t))·B(b,t)·Treasury10y; where-list "Treasury3m is the 3-month Treasury yield; and Treasury10y is the 10-year Treasury yield."; projection form with q subscripts on both Treasury terms | 207 | **Verified** against the equation image, including the notation nuance the chapter records: the A43 display carries **no time subscript** on the Treasury terms while the projection form adds them — the md transcription and the chapter are faithful to both |
| 2 | **Balance sourcing**: "The relevant balances for this component are the assets reported in line item 15 of the Net Interest Income Worksheet of FR Y-14Q, Schedule G (G.2)" | 206 | **Verified verbatim.** Source-stated item — FACT, no correction PID; physical sheet row is a CODE TO_BE_CONFIRMED |
| 3 | **α sourcing**: "This portion can be quantified by utilizing the additional fields provided by the firms in the footnotes to the worksheet and by cross-referencing with the balances reported in FR Y-9C (BHCK3365)"; "Federal funds sold and securities purchased under agreements to resell comprise most of other interest/dividend-bearing assets reported in FR Y-14Q" | 206 | **Verified verbatim.** The chapter correctly preserves the derivation-mechanics gap as **OQ-024** (filed this session) and treats α as a supplied launch-point input [CODE], labeled, with the deposit-expense Spread(i,b) precedent cited |
| 4 | **Variable definitions**: "let α_b be the proportion of assets consisting of federal funds sold and securities purchased under agreements to resell for each firm b, B_b be the total balance on other interest/dividend bearing assets, and F_b be the income earning from this component" | 206 | **Verified verbatim** (source grammar "income earning" preserved in the chapter's quote) |
| 5 | **Flat balance and flat share**: "B(b,q) = B(b,q0) for all quarters … The share α(b,q) = α(b,q0) is also assumed to stay constant over the projection quarters." | 207 | **Verified verbatim.** Chapter §4 and YAML `balance_behavior` freeze both quantities at PQ0 |
| 6 | **Footnote 66 / CA-1**: authoritative footnote reads "For instance, stock in Federal Reserve Banks yields the lesser of six percent and the 10-year Treasury yield." and **ends there**; the md working copy glues "Notes: Statistical significance levels …" after it | 206 (image) vs. md line 5360 | **Verified — CA-1 direction confirmed**: the glue is conversion-only. The chapter's [CODE] warning that the 6 % lesser-of is **rationale, not model mechanics** is corroborated by the equation image: no cap term appears in A43 |
| 7 | **Assumptions and limitations**: two-rate assumption; special/rare-collateral caveat on the 3M leg; remainder heterogeneity "relatively small … not … material"; no-estimation advantages incl. gross/net balance-sheet-offsetting discretion; single-component treatment "due to data limitations" | 207–208 | **Verified verbatim** on the page images. Chapter §8 restates all five faithfully, all [FACT] |
| 8 | **Questions A175/A176**: A175 "as compared to the Board's current panel regression model"; A176 joint modeling of fed funds sold with other interest/dividend-earning assets | 208 | **Verified verbatim.** (This section's Questions intro names the correct component — no SQ-4-style misnomer here) |
| 9 | **Subsumption statement** (cited from v.a(10)): "the federal funds and repo positions on the asset side are subsumed within the component other interest/dividend-bearing assets" | 217 | **Verified** — previously confirmed on the p. 217 page image in the `ie_fed_funds_repo` review (2026-07-17); the chapter cites it as a structural symmetry, explicitly *not* a compute dependency |
| 10 | **Annualized-rate conversion and absence of parameters**: ÷4 labeled D-004 with FACT absence preserved; no parameter of any kind in v.a(6); Tables A7–A9 have no row for this component | 205–208 (absence); 219–220, 234 (tables) | **Verified.** α is correctly classified as a firm-data input, not a parameter |

Additional spot-checks, all verified: Table A6 "Structural" row (pp. 168–169, via the verified integrity review); nine-quarter horizon (p. 6); the blended-rate restatement in chapter §5/§6 is labeled [CODE] and is algebraically identical to A43 (checked by expansion). YAML parses and follows `specifications/model-spec-guidelines.md` key order with the required header block.

## 2. Findings

- **No MATERIAL findings.** Every equation, quote, and citation checked traces to the PDF page images; the one genuine source gap (α derivation mechanics) is preserved as OQ-024 with a labeled supplied-input treatment rather than an invented method — consistent with the never-invent rule.
- **MINOR-1:** The `usd_10y_treasury` series is new to the project's canonical scenario set; the chapter and the asset-side conventions chapter (§3) both flag its physical column name as UNCONFIRMED. Consistent treatment; no action.
- **MINOR-2:** The α = 0 / α = 1 plausibility log in §10 is a data-quality monitor justified by the source's "comprise most" sentence; it is correctly a log, not a constraint. No action.

## 3. Shared-file changes (applied this session — Increment 1)

1. **`handbook/open-questions.md`**: **OQ-024** filed (α derivation mechanics unstated; supplied-input treatment); D-009 recorded.
2. **`inventory/asset-side-model-matrix.md`**: row for `ii_other_ida` — DRAFTED, awaiting user review.
3. **`inventory/source-map.md`** and inventory #6 artifact row: deferred to the asset-side integration gate, mirroring the liability-side practice.

## 4. Verdict

**APPROVE (source-grounding)** — no corrections required; the chapter is source-faithful as drafted, with OQ-024 correctly opened for the one underspecified input. Final acceptance remains with the **user review gate** (Increment 1) before any code is written against it.

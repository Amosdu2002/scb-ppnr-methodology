# Handbook Chapter Template — Proposed 2026 PPNR Net-Interest Models

**Deliverable 4 of Phase 1, Task 1.** Date: 2026-07-16.
One chapter per Table A6 net-interest component plus one cross-cutting hedge chapter (~13 chapters, per decision D-003 in `handbook/open-questions.md`). The loans chapter carries six portfolio-specific sections inside the single common framework. Copy this file to `handbook/models/<family>/<subfamily>/<model_id>.md` (component chapters; e.g. `handbook/models/interest-expense/deposits/ie_dom_time_dep.md`) or `handbook/cross-cutting/<model_id>.md` (the hedge-adjustment chapter and the common-methodology chapter), matching the existing directory skeleton, and replace every `⟨…⟩` placeholder. Delete template comments (lines starting `<!--`) before review.

## Non-negotiable conventions (from CLAUDE.md — restated so each chapter is self-auditing)

1. **Status**: the model is PROPOSED for 2026 (public comment), NOT adopted. The status banner below is mandatory and must not be softened.
2. **Labels**: every material statement carries one of —
   - **[FACT]** SOURCE-STATED FACT — restates the source; must carry a citation.
   - **[INT]** INTERPRETATION — a reading the source does not state verbatim; say what it rests on.
   - **[CODE]** CODING CONSIDERATION — implementation guidance for the future Python phase; never attributable to the Fed.
   - **[OQ]** OPEN QUESTION — link to `handbook/open-questions.md` by ID.
   - Anything unknown is written **UNKNOWN** — never invented, never silently defaulted.
3. **Citations**: `(PDF p. N; md sec-M)` — printed page = PDF sheet (verified); md anchors per `inventory/source-map.md`. Every equation, parameter, line item, and assumption gets one.
4. **Quoting**: quote the source verbatim where wording matters; apply corrected readings from `inventory/source-integrity-review.md` §7 (conversion artifacts) and record source quirks (§8) as-is with an [INT] note — never silently correct the Fed's text.
5. **Terminology**: exact Fed term first, coding-friendly name in parentheses, e.g. "Interest income rate(b,p,i,t) (`interest_income_rate`)".
6. **No production Python** in Phase 1 — pseudocode only, clearly non-normative.

---

# ⟨N⟩. ⟨Exact Fed component name⟩ (`⟨model_id⟩`)

> **STATUS: Proposed for the 2026 stress test — public-comment stage, NOT adopted.**
> Source: Section B.v.⟨…⟩ (PDF pp. ⟨…⟩; md sec-⟨…⟩). Model type per Table A6: ⟨Structural | Regression | cross-cutting adjustment⟩.
> Integrity flags affecting this chapter: ⟨CA-/SQ- IDs from the integrity review, or "none"⟩.
> Chapter review state: ⟨DRAFT | REVIEWED | APPROVED⟩ — approved content is never silently overwritten.

## 1. Component definition and scope

<!-- What the component is; which FR Y-9C / FR Y-14 line items define it; what it absorbs from or cedes to other components (e.g., sub debt inside other borrowing). All [FACT] with citations. -->

## 2. What the model projects

<!-- Output quantity, dimensions (b, p, i, t), units ($ per quarter vs. rate), horizon (9 quarters), and whether output is income, expense, or a net item. State the launch-point convention (PQ0 = last quarter before projection; source terms "lift-off"/"jump-off", decision D-005). -->

## 3. Inputs

### 3.1 Firm data inputs
| Input | Fed source (schedule, line item) | Dimensions | Units | Timing (launch-point definition: average vs. end-of-quarter, as-of date) | Label |
|---|---|---|---|---|---|

### 3.2 Scenario inputs
| Scenario variable | Enters via | Frequency | Units | Label |
|---|---|---|---|---|

### 3.3 Parameters
| Parameter | Supplied or estimated | Source (Table A7/A8/A9 or derivation) | Value(s) or UNKNOWN | Constant over horizon? | Label |
|---|---|---|---|---|---|
<!-- Firm fixed effects: disclosed-or-not is [FACT]; the backsolving working method is [INT]/[CODE] per decision D-002 — never present it as Fed methodology. -->

## 4. Calculation sequence

<!-- Numbered steps in execution order. Each step: verbatim equation (with equation number + citation), then a coding-friendly restatement naming intermediates. State unit conversions explicitly (annual→quarterly ÷4, N/360, quarterly compounding) and label whether the conversion is [FACT] or [INT]. -->

1. ⟨step⟩
2. ⟨step⟩

**Intermediates register**
| Intermediate | Defined in step | Dimensions | Units | Label |
|---|---|---|---|---|

## 5. Launch point (PQ0) vs. projection-quarter register

| Quantity | Launch point (PQ0) role | Projection-quarter (t ≥ 1) role | Label |
|---|---|---|---|
<!-- Make the timing unambiguous: what is measured once at PQ0, what evolves, what a quarter-t value depends on (t vs. t−1 vs. PQ0). -->

## 6. Constancy register

| Quantity | Constant or varying over the horizon | Source statement | Label |
|---|---|---|---|
<!-- Balances, composition/shares, spreads, betas, scalars, WAL/ρ, revolver shares, α, floors — every one explicitly classified. -->

## 7. Segmentation and aggregation

<!-- Segment definitions, how segment results roll up to the component, weighting scheme. For the loans chapter this section carries the six portfolio subsections (Corporate, CRE, Mortgage, Auto, Credit Card, Other Consumer Products) under the common framework — portfolio rules are variations, not separate models. -->

## 8. Interest-rate-risk hedge treatment

<!-- One of: embedded hedge-income term (securities); excluded pending data (loans); handled by the cross-cutting adjustment chapter; not addressed. Present both data states where relevant: current (hedge income = 0) and proposed-collection (Eq A49–A51 path). Cross-reference the hedge chapter. -->

## 9. Assumptions and limitations (source-stated)

<!-- Restate the section's Assumptions and Limitations faithfully, each with citation. Keep the Fed's own framing; do not merge in interpretations here. -->

## 10. Comparison with the current 2025 model

<!-- Only what the proposed text itself compares or depends on (per CLAUDE.md); cite the COMPARISON sections from the source map. Keep short. -->

## 11. Board questions relevant to this chapter

<!-- Verbatim list of the Question A-numbers for this component with citations; note numbering quirks (SQ-3) where applicable. These mark methodology the Fed itself considers open — mine them for open questions. -->

## 12. Coding considerations ([CODE] — non-normative)

<!-- Implementation notes for the future Python phase: suggested data structures, dimension order, unit normalization, edge cases (floors, ELB boundary, missing vendor data fallbacks), validation hooks (e.g., reproduce Table A7/A8/A9 values). Nothing here is Fed methodology. No confidential implementation details — generic specifications and synthetic examples only. -->

## 13. Open questions

<!-- Bullet list of OQ-IDs affecting this chapter, one line each, linking to handbook/open-questions.md. -->

## 14. Citation index

<!-- Table: claim → (PDF p.; md anchor). Every material methodology claim in the chapter appears here once, so reviewers can audit coverage. -->

---

### Chapter completion checklist (delete after passing)

- [ ] Status banner present; no adoption language anywhere.
- [ ] Every material statement labeled [FACT]/[INT]/[CODE]/[OQ]; unknowns say UNKNOWN.
- [ ] Every equation verified against the PDF or flagged for verification.
- [ ] Conversion artifacts (CA-) corrected per integrity review; source quirks (SQ-) preserved verbatim with [INT] notes.
- [ ] Launch-point vs. projection timing unambiguous for every input and intermediate.
- [ ] Constancy register covers every input/parameter.
- [ ] Units and rate-conversion conventions explicit at every step.
- [ ] No production Python; no confidential material.
- [ ] Open questions filed with IDs; review state set.

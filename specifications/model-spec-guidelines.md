# Model Specification Guidelines — YAML Convention

**Established at the liability-side integration gate, 2026-07-17.** Governs every YAML
specification under `specifications/`; the five liability-side interest-expense specs were
standardized to this convention on the same date. Future specs (asset side, trading NII,
hedge adjustment) follow it from the start.

Specs are **coding-oriented restatements of approved handbook chapters** — Phase 1 documents,
no production code. A spec never introduces methodology absent from its chapter; where the
two disagree, the chapter (and behind it the Fed PDF) governs and the spec is corrected.

## 1. File location and naming

- Path: `specifications/<side>/<subfamily>/<model_id>.yaml`, mirroring
  `handbook/models/<side>/<subfamily>/<model_id>.md` (e.g.
  `specifications/interest-expense/deposits/ie_dom_time_dep.yaml`).
- One spec per model ID. Model IDs are canonical and identical across chapter, spec, review,
  inventory, and source map (integration corrected `ie_ffp_repo` → `ie_fed_funds_repo`).

## 2. Header comment and labels

Every file opens with a comment block stating: the model ID and Fed component name; the
proposed-NOT-adopted status; the label legend; and the citation format. Labels (in `#`
comments throughout the file):

- `FACT` — Fed source statement, cited `(PDF p. N; md sec-M)`.
- `INT` — interpretation, with its basis.
- `PID` — user-confirmed project implementation decision (registry:
  `handbook/open-questions.md`); never attributable to the Federal Reserve.
- `CODE` — coding consideration, non-normative.
- `OQ-nnn` — open question by final ID. Placeholder IDs (`OQ-NEW-*`, component-scoped
  letters) are assigned final numbers at an integration gate.
- `UNKNOWN` / `TO_BE_CONFIRMED` — stated, never defaulted or invented.

## 3. Top-level keys, in order

| # | Key | Required | Content |
|---|---|---|---|
| 1 | `model` | yes | Identity, classification, status, artifact paths (§4) |
| 2 | `dimensions` | yes | Firm/subcomponent/scenario/time; `output_grain` |
| 3 | `inputs` | yes | `firm_data:` and `scenario:` lists (§5) |
| 4 | `parameters` | yes | Supplied/derived parameters, or `parameters: none  # FACT …` |
| 5 | `transformations` | if any | Named standalone derivations that are not Fed equations (§6) |
| 6 | `equations` | yes | Fed equations verbatim-faithful + coding restatements (§6) |
| 7 | `initial_conditions` | yes | Seeds and PQ0 values consumed at t = 1, or `none — no recursion` |
| 8 | `balance_behavior` | yes | What is frozen at PQ0, what varies |
| 9 | `constraints_and_floors` | yes | Floors/caps/regimes, or explicit `none` (FACT absence) |
| 10 | `quarterly_dollar_calculation` | yes | The D-004 block (§7) |
| 11 | `outputs` | yes | Primary output(s): name, dims, units (§8) |
| 12 | `validations` | yes | Non-normative CODE checks (§9) |
| 13 | `dependencies` | yes | Upstream models, shared inputs, hedge interface |
| 14 | `project_decisions` | yes | D-/PID- entries this spec applies (§10) |
| 15 | `open_questions` | yes | `open:` / `resolved_for_project:` lists (§10) |
| 16 | `source_references` | yes | Structured `{claim, pdf_page, md}` list |

Model-specific extra keys are allowed when they aid clarity (e.g. `estimation` detail for a
regression model, `fixed_effect` for a backsolve) — **do not force unlike models into a
common formula**; the shared skeleton standardizes bookkeeping, not methodology.

## 4. `model` block fields

```yaml
model:
  id: <model_id>
  fed_name: "<exact Fed component name>"   # note source-internal variants where they exist
  fed_section: B.v.a(N)                    # or B.v.d(N)
  source_pages_pdf: [start, end]
  source_anchors_md: [sec-A, sec-B]
  model_type: structural | regression      # FACT — Table A6 (PDF pp. 168-169)
  model_form: <short descriptor>           # e.g. wal_repricing_recursion, two_regime_deposit_beta,
                                           #      structural_calculator, ols_regression_rate_spread
  side: interest_expense | interest_income | net
  status: proposed_2026_stress_test__public_comment__NOT_adopted   # fixed vocabulary — never softened
  estimation: none | <method + sample>     # FACT
  chapter: <repo-relative chapter path>
  review: <repo-relative review path>      # or null with a comment when the report is missing
  chapter_review_state: DRAFT | REVIEWED | APPROVED
```

## 5. Inputs: canonical names, physical mappings, units, timing

Each input entry:

```yaml
- name: <canonical_name>          # snake_case; model prefix; _launchpoint suffix for PQ0 snapshots
  fed_item: <source-stated schedule/item>   # or UNKNOWN  # FACT absence — never guessed
  project_mapping: {...}          # PID-labeled physical layer, only when user-confirmed;
                                  # kept SEPARATE from fed_item — retrieval vs. methodology
  dims: [firm, subcomponent, ...]
  units: <vocabulary below>
  timing: <vocabulary below>
  role: <one line>
```

- **Canonical names**: scenario series are shared across models — `usd_3m_treasury`,
  `usd_1y_treasury`, `bbb_corporate_yield`. Firm inputs carry a model prefix
  (`odd_`, `ob_`, `foreign_`, …) or a spelled-out component name; primary outputs end in
  `_interest_expense` (income side: `_interest_income`).
- **Units vocabulary**: `USD`, `USD_per_quarter`, `annualized_rate`,
  `annualized_rate_spread`, `share_0_to_1`, `fraction`, `months`, `quarters`.
  Percent-vs-decimal scale is metadata-driven at ingestion, never assumed (see chapter
  coding considerations); specs record `annualized_rate` regardless of raw scale.
- **Timing vocabulary**: `launchpoint` (measured once at PQ0), `launchpoint, held constant`
  (frozen over the horizon), `projection_quarters` (t = 1…9 path), plus free-text
  qualifiers (e.g. "PQ0 value needed only for the backsolve"). PQ0 is the launch point —
  the last quarter before the projection horizon (decision D-005; source terms
  "lift-off"/"jump-off" are preserved inside quotes only).

## 6. Transformations and equations

- Fed equations keep their equation numbers (A44, A45–A47, A48, A53(1)/(2)) with a
  faithful formula, the operative where-list content, and a coding restatement in canonical
  names. Verification status ("verified against the PDF page image") is stated.
- Named transformations that are not Fed equations (months→quarters ÷3, balance
  aggregation, share construction) live in `transformations:` or as `derivation:` fields
  in-place, always labeled (PID/INT) — never hidden literals.

## 7. Quarterly-dollar block (D-004)

Every net-interest spec carries:

```yaml
quarterly_dollar_calculation:
  formula: <output> = <balance> * <annualized rate> / 4
  convention: PID D-004 — annualized rates throughout; divide by 4 only at the final
    quarterly-dollar step (simple nominal quarterization, not compounding)
  source_status: <FACT statement of what the source does/does not state for this component>
```

The ÷4 is never attributed to the Fed; where the source states its own conversion
(securities ÷4, hedge N/360, trading-NII ÷4), the source statement governs.

## 8. Outputs

Primary output(s) with `name`, `dims` (matching `dimensions.output_grain`), `units`,
one-line description. Retained intermediates (e.g. a rate path kept for traceability) are
listed only when the chapter states the retention, labeled CODE.

## 9. Validations

Non-normative CODE checks, one line each. Shared principles (stated once in
`handbook/cross-cutting/liability-side-common-conventions.md`, applied per model):
required inputs present — failures surface, **no invented fallbacks**; parameter fidelity
verified against the PDF page, not retyped copies; rate-scale normalization metadata-driven
and identical across firm and scenario series; edge monitors **log, never clamp**.

## 10. Project decisions and open questions

```yaml
project_decisions:   # user-confirmed; never attributable to the Federal Reserve
  - {id: D-004, scope: project_wide, summary: <one line>}
  - {id: PID-XX-n, summary: <one line>}
open_questions:
  open:
    - {id: OQ-nnn, topic: <one line>}
  resolved_for_project:
    - {id: OQ-nnn, via: <D-/PID- id>, topic: <one line>}
```

PIDs are decisions, not open questions — they never appear under `open_questions`.
The single registry for both lives in `handbook/open-questions.md`.

## 11. Change control

- A spec is updated when its chapter is updated, at review gates, and at integration
  gates; approved content is never silently overwritten.
- Every spec must parse as YAML. Comments carry the labels; values stay
  machine-consumable (no prose paragraphs inside values where a list or map serves).

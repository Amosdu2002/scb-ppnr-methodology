# Liability-Side Integration and Consistency Review

**Gate date: 2026-07-17.** Scope: the five completed interest-expense methodology packages —
`ie_dom_time_dep`, `ie_other_dom_dep`, `ie_foreign_dep`, `ie_fed_funds_repo`,
`ie_other_borrowing` — across `handbook/models/interest-expense/`,
`specifications/interest-expense/`, `reviews/interest-expense/`, and the shared tracking files.
All five models are **PROPOSED for the 2026 stress test (public-comment stage) — NOT adopted**.
Method: every chapter, spec, and review report read in full; cross-model comparison on the
25-point consistency checklist of the gate instructions; source verification against the
Markdown working copy (and prior page-image verification records) where names or items were in
question; shared-file changes user-approved before application. Severities: CRITICAL / MATERIAL /
MINOR / EDITORIAL.

## 1. Artifact completeness (missing / duplicate artifacts)

| Model | Chapter | Specification | Independent review |
|---|---|---|---|
| `ie_dom_time_dep` | present (REVIEWED) | **was MISSING — created at this gate** (F-1) | **report artifact MISSING** (F-2) — review event recorded in the chapter banner and brief, report never preserved |
| `ie_other_dom_dep` | present | present | present — PASS, no corrections |
| `ie_foreign_dep` | present | present | present — source-faithful |
| `ie_fed_funds_repo` | present | present | present — APPROVE |
| `ie_other_borrowing` | present | present | present — APPROVE WITH OPEN IMPLEMENTATION ITEM |

- **No duplicate artifacts** in the main tree; no artifacts in wrong directories (`deposits/` vs
  `funding/` placement matches the template scheme); no stale cross-file paths found after the
  corrections below. Stale parallel-session copies under `.claude/worktrees/` are session
  workspaces, not repository content — excluded and untouched.
- `README.md` is empty (out of gate scope; noted only).
- Chapter numbering 7–10 and 12 is intentional (11 = `nii_trading_al`, not in this family).

## 2. Findings

### CRITICAL

None.

### MATERIAL

- **F-1 — `ie_dom_time_dep` had no YAML specification** anywhere in the repository.
  *Resolved:* `specifications/interest-expense/deposits/ie_dom_time_dep.yaml` created at this
  gate (user-approved) as a mechanical translation of the REVIEWED chapter and approved source
  brief — no new methodology.
- **F-2 — `ie_dom_time_dep` independent review report not preserved.** The Step-5 review ran
  2026-07-17 (chapter banner; brief traceability entries) but, unlike the other four models, no
  report file exists. *Disposition (user-approved):* not reconstructed; recorded as a gap;
  chapter banner corrected; **follow-up focused review required** (§6).
- **F-3 — Canonical model-ID mismatch.** `inventory/model-inventory.md` (record #10 and the
  dependency summary) and `inventory/source-map.md` used `ie_ffp_repo`; all merged artifacts use
  `ie_fed_funds_repo`. *Resolved:* inventories corrected to `ie_fed_funds_repo`.
- **F-4 — Open-question numbering collision.** The merged `ie_other_dom_dep` chapter used
  OQ-016/017/018 (balance mappings / spread mechanics / seed timing) while the earlier
  `ie_foreign_dep` review had provisionally suggested the same three numbers for different
  topics (its §5.1 explicitly deferred final numbering to integration). *Resolved:* the merged
  ODD assignment stands; the foreign/OB candidates are filed as **OQ-019** (44B collision),
  **OQ-020** (beta-item mapping), **OQ-021** (median recomputation), **OQ-022** (OB share
  denominators, formerly OQ-OB-A); all placeholder references (OQ-NEW-1/2, OQ-OB-A,
  SQ-candidates) in chapters and specs updated to final IDs. The foreign review's provisional
  numbering is superseded — the review file itself is a historical record and was not rewritten.
- **F-5 — Decision-log gaps.** Thirteen user-confirmed PIDs (PID-1…PID-6, PID-ODD-1/2,
  PID-FFR-1, PID-OB-1…4) were recorded only in chapters/briefs although four reviews directed
  filing "at integration"; PID-5 was cited cross-model with no shared registration. *Resolved:*
  PID registry table added to the `handbook/open-questions.md` decision log.
- **F-6 — Stale shared-tracking content.** OQ-009 not narrowed per PID-OB-1/3; inventory #10
  still listed 44A/44B as balances with no PID-FFR-1 note; the five inventory records lacked
  artifact paths/status and omitted OQ-005; OQ-013 lacked its affected-chapter note; D-004
  "Where applied" lacked the five chapters. *Resolved:* all updated (user-approved).

### MINOR

- **F-7 — The pre-integration `ie_other_dom_dep.yaml` never parsed as YAML** (verified against
  the copy on main): `2020:Q2` inside a flow mapping violates plain-scalar rules
  (`Psych::SyntaxError` at its line 157). Its review had not run a parser (only the fed-funds
  review did). *Resolved:* fixed during standardization; **all five specs now parse**, and the
  guidelines require parseability.
- **F-8 — Two would-be duplicate filings in the component reviews** (errata noted here; the
  historical review files are left as written): the `ie_fed_funds_repo` review §3.2(a) proposed
  filing the Equation A48 title typo, already logged as **SQ-10**; the `ie_other_borrowing`
  review F-4 stated the stray-pipe artifacts (md 4645–4646) were "not yet logged" — they were
  already **CA-2g/CA-2h**. Neither was re-filed.
- **F-9 — Source-internal component-name variants for v.a(10).** The v.a(10) heading prints
  "…under **the Agreement** to Repurchase" (singular); Table A6 and the section prose use
  "…under **agreements** to repurchase"; the current-suite iv.m(2) heading uses "the Agreements";
  the Equation A48 title carries the separate SQ-10 "Purchase" typo. The chapter/spec use the
  prose/Table A6 plural form. *Resolved:* variants documented (inventory #10, matrix, spec
  header) — nothing silently corrected; no SQ filed since each element is either correct prose
  or already covered by SQ-10.

### EDITORIAL

- **F-10 — Stale/incomplete chapter banners.** `ie_dom_time_dep` still said "Awaiting user
  approval before commit (Step 8)" though merged, and named no spec; the other four said DRAFT
  though their reviews had passed. *Resolved:* all five banners now carry the review state
  (REVIEWED), the review verdict and path (or the F-2 gap for dom-time), and the spec path.
- **F-11 — Two divergent YAML conventions** (field names, key order, status vocabulary,
  reference formats; PID/SQ/CODE items misfiled under `open_questions` in the fed-funds spec;
  non-canonical names in the foreign expense formula). *Resolved:* §4 below.

## 3. Cross-model consistency review (checklist outcome)

Consistent across all five packages after the corrections above: Fed component names against
Table A6/section headings (with the F-9 variants documented); Table A6 classifications
(4 structural + 1 regression); canonical model IDs; canonical scenario-input names
(`usd_3m_treasury`, `usd_1y_treasury`, `bbb_corporate_yield`) and the `_launchpoint` /
`_interest_expense` naming patterns; FR Y-14Q/FR Y-9C physical mappings layered as
fed-stated vs PID; annualized-rate units with metadata-driven percent/decimal normalization;
÷4 only at the final quarterly-dollar step (D-004, never attributed to the Fed, including the
OB backsolve reversal); launch-point (PQ0) terminology (D-005); projection-quarter alignment
t = 1…9; flat-balance and flat-composition treatment; Table A7/Table A9 parameter values
(identical in chapters, specs, and the integrity review's verified table register);
firm-fixed-effect treatment (only `ie_other_borrowing`; D-002 + PID-OB-1/3; explicitly n/a in
the four structural chapters); hedge-adjustment boundary (expense path exposed, v.c external,
OQ-005); validation conventions (no invented fallbacks; failures surface; log-never-clamp);
open-question statuses (single registry, no duplicates, no unsupported resolutions).

**Genuine methodology differences preserved, not harmonized** (matrix §3): A44 WAL recursion vs
A45–A47 two-regime beta (foreign by reference) vs A48 direct calculator vs A53 OLS regression;
1Y vs 3M Treasury drivers (+BBB for OB); deposit betas and the ELB regime only in the A45–A47
models; floors only inside Eq A46; ODD's deliberately mixed expense-balance sourcing
(PID-ODD-2) vs foreign's 35A+35B (INT-a); estimation only in OB.

## 4. YAML standardization

`specifications/model-spec-guidelines.md` created (shared key order, `model` metadata incl.
artifact paths and fixed status vocabulary, fed-item/project-mapping layering, units/timing
vocabularies, D-004 block, `outputs`, `project_decisions` vs `open_questions` separation,
structured source references, parseability requirement, and the do-not-force rule for
model-specific blocks). All five specs standardized to it: field renames
(`table_a6_type`→`model_type`, `fed_section` unified, list-form source pages/anchors), long
status string everywhere, `outputs` and `project_decisions` blocks added, final OQ IDs
substituted, fed-funds `open_questions` cleaned of PID/SQ/CODE entries, foreign expense formula
restated in canonical input names, dom-time spec created. **No methodology was changed to make
files look alike**; model-specific blocks (`timing_rules`, `fixed_effect`, `estimation`,
`transformations`, `reuses`) remain.

## 5. Remaining material open implementation items

1. **OQ-005** — hedge-adjustment allocation across components (external: proposed FR Y-14Q
   B.2/B.3 outcome + Fed methodology statement); OB α_b double-counting caution.
2. **OQ-009 residual** — physical line item for the PQ0 actual other-borrowing expense
   (`ob_expense_actual_launchpoint`); low-rate-regime mismatch treatment (minor).
3. **PID-OB-4 gates** — four BBB physical-input confirmations (column name; yield vs spread;
   Treasury-yield addition; unit scale) before first use.
4. **PID-5 residuals** — MEV column names for the 3-month Treasury (three models) and BBB
   remain UNCONFIRMED working assumptions.
5. **OQ-022** — OB share-denominator physical form.
6. **`ie_foreign_dep` candidate PIDs** — INT-a (expense balance 35A+35B), INT-b/OQ-020,
   INT-c/INT-f (seeds; OQ-018), spread comparator (OQ-017), =25 bp branch (OQ-013) await user
   confirmation.
7. **OQ-017/OQ-018/OQ-019/OQ-021** — Fed-clarification/form-instruction items, interim [INT]
   treatments recorded.

## 6. Models requiring another focused review

- **`ie_dom_time_dep`** — a focused independent source-grounding review to produce the missing
  report artifact at `reviews/interest-expense/deposits/ie_dom_time_dep.review.md` (F-2), which
  should also cover the spec created at this gate. No other model requires re-review: the four
  existing reviews are page-image-grounded and their filing instructions are now executed.

## 7. Readiness for the Python-architecture phase

The family is coherent for architecture design: five parseable, convention-aligned specs; a
single registry of decisions and open questions; uniform timing/units/validation/hedge
boundaries; explicit, documented differences in calculation form. Architecture work can rely on
the shared conventions (`handbook/cross-cutting/liability-side-common-conventions.md`) and the
matrix (`inventory/liability-side-model-matrix.md`), treating §5's items as configuration
gates, not design blockers. The one process gap is F-2 (dom-time review artifact), which does
not change the methodology content relied upon (the chapter is REVIEWED and its claims carry
page-level citations) but should be closed before the family is declared APPROVED end-to-end.

## Verdict

**INTEGRATION APPROVED WITH OPEN IMPLEMENTATION ITEMS** — the items in §5 plus the F-2
follow-up review in §6. No CRITICAL findings; all MATERIAL findings resolved at this gate
except F-2, which is scheduled rather than resolved.

---

## Addendum — 2026-07-20 (post-gate revision, user-directed)

**PID-OB-5 (user-confirmed 2026-07-20) supersedes PID-OB-1/PID-OB-3** for `ie_other_borrowing`:
α_b is now calibrated so the nine-quarter cumulative modeled expense equals the cumulative
expense implied by the project-supplied FRB total-interest-expense path
(`frb_total_interest_expense`); PQ0 actuals never enter. Effects on this report: §3's
"D-002 + PID-OB-1/3" fixed-effect line and the "OB backsolve reversal" clause describe the
superseded treatment (historical); §5 item 2 (OQ-009 residual — PQ0 actual-expense line item;
low-rate-regime mismatch) is **moot** and replaced by **OQ-023** (FRB-total physical source and
scope alignment). The OB α_b hedge double-counting caution (§5 item 1) still applies — under
PID-OB-5 α_b absorbs the full residual to the FRB total, including any embedded hedge effects.
A project-level execution-order dependency now exists: the other four interest-expense models
plus the FRB total path feed the OB calibration (registry: `handbook/open-questions.md`; chapter
§9; YAML `fixed_effect` and `dependencies`). The historical body above is preserved unchanged.

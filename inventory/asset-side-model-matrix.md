# Asset-Side Model Matrix — Proposed 2026 Interest-Income Models (+ Net Trading NII)

**Created at asset-side Increment 1, 2026-07-23.** Navigation and status summary for the seven
asset-side/net methodology packages. **All models are PROPOSED for the 2026 stress test
(public-comment stage) — NOT adopted.** Full detail lives in the chapters, YAML specs, and
`inventory/model-inventory.md` records #1–#6 and #11; this matrix never overrides them.

Chapter numbering follows the inventory census: 1 `ii_loans`, 2 `ii_dep_banks_other`, 3 `ii_ust`,
4 `ii_mbs`, 5 `ii_other_sec`, 6 `ii_other_ida`, 11 `nii_trading_al` (chapters 7–10 and 12 are the
liability side; 13 is the cross-cutting hedge adjustment).

Shared conventions (launch point PQ0, D-004 ÷4 with income-side source-stated exceptions,
constancy patterns, hedge boundary, FRB-path monitor boundary, family grouping) are stated once
in `handbook/cross-cutting/asset-side-common-conventions.md`.

## 1. Roadmap (user-approved 2026-07-23)

Family-batched vertical slices; per family: chapters + specs + source-grounding reviews →
**user review gate** → code → synthetic goldens → company-reference check. Order: securities
before loans; trading NII last (its calibration-mode decision and the income orchestrator close
the family). Chapter format: compact 13-section skeleton per **D-009**.

| Increment | Family | Components | Status |
|---|---|---|---|
| 1 | Foundations + A (calculators) | conventions chapter; `ii_dep_banks_other`; `ii_other_ida` | **Handbook APPROVED (user gate) and code LANDED 2026-07-23** — core extraction (refactor-only, expense suite green with zero test edits) + both calculator models + ingestion + goldens (164 passed). **Remaining: company-reference check** (`examples/run_income_calculators.py` against the reference implementation) |
| 2 | B (securities) | `ii_ust`, `ii_mbs`, `ii_other_sec` | PLANNED. Prerequisite in progress: collect the Securities Model Description (OQ-004 — user approved 2026-07-23). Gate decisions: input granularity (pre-aggregated buckets proposed); vendor-prepayment path as declared input |
| 3 | C (loans) | `ii_loans` (one chapter, six portfolio sections per D-003) | PLANNED. Gate decisions: wt external-input contract (OQ-001); floors as supplied values (OQ-002); Table A8 mapping caution (OQ-010); other-consumer jump-off mapping (OQ-011) |
| 4 | D (trading NII) + integration | `nii_trading_al`; income orchestrator/reporting; asset-side integration review; combined-NII monitor | PLANNED. Gate decision: calibration mode — D-002 launch-point backsolve vs. PID-OB-5-style cumulative vs. `frb_total_interest_income`, incl. the NET-item scope mapping (OQ-007/OQ-009) |

## 2. Methodology at a glance

| Model ID | Fed component (section) | Type / form | Primary firm inputs | Scenario variables | Parameters | Core calculation |
|---|---|---|---|---|---|---|
| `ii_loans` | Interest Income on Loans — B.v.a(1), PDF pp. 173–188 | Structural — six-portfolio loan engine | FR Y-14M/14Q segment data; jump-off rates/spreads; revolver share; wt inputs (external, OQ-001) | `prime_rate`, `mortgage_rate`, `usd_3m_treasury` | **Table A8** industry scalars (7 values); no estimated coefficients | Eq A32 income = balance × rate; rate machinery A33–A38 (fixed/variable, floors, re-origination blend) |
| `ii_dep_banks_other` | Interest Income on Deposits with Banks and Other — B.v.a(2), PDF pp. 188–190 | Structural — direct calculator | Schedule G item 14 balance (**source-stated**) | `usd_3m_treasury` (used raw as the rate) | **None** | Eq A39: income = item-14 balance × Treasury3m ÷ 4 |
| `ii_ust` | Interest Income on U.S. Treasuries — B.v.a(3), PDF pp. 190–195 | Structural — securities template | Schedule B.1 security-level + vendor data (granularity: Increment 2 gate) | via reinvestment assumption (OQ-004) | None estimated | Eq A40: coupon accrual + straight-line accretion + hedge (= 0) |
| `ii_mbs` | Interest Income on Mortgage-Backed Securities — B.v.a(4), PDF pp. 195–200 | Structural — securities template (WAL accretion; Agency RMBS vendor prepayment) | Schedule B.1 + vendor data; vendor income path (declared input, Increment 2 gate) | `usd_3m_treasury` (floating margin); vendor-model MEVs (OQ-004) | None estimated | Eq A41: coupon + accretion ÷ (4 × WAL) + hedge (= 0); Agency RMBS via vendor model |
| `ii_other_sec` | Interest Income on Other Securities — B.v.a(5), PDF pp. 200–205 | Structural — securities template (book-yield variant) | Schedule B.1 book yield + vendor data | `usd_3m_treasury` (floating margin) | None estimated | Eq A42: amortized cost × book yield ÷ 4 + hedge (= 0); no prepayment |
| `ii_other_ida` | Interest Income on Other Interest/Dividend-Bearing Assets — B.v.a(6), PDF pp. 205–209 | Structural — two-rate blend calculator | Schedule G item 15 balance (**source-stated**); α share (supplied input, OQ-024) | `usd_3m_treasury`, `usd_10y_treasury` | **None** | Eq A43: income = B × [α·T3m + (1 − α)·T10y] ÷ 4 |
| `nii_trading_al` | Net Interest Income on Trading Assets and Liabilities — B.v.d(1), PDF pp. 225–230 | **Regression** — WLS panel ratio (NET item) | Net trading assets at PQ0 (OQ-007 working interpretation); launch-point actuals (D-002) | `usd_3m_treasury` | **Table A9**: β = 0.278; α_b **not disclosed** (D-002 / Increment 4 gate) | Eq A52: Ratio = β·Treasury3m + α_b; dollars = Ratio × net trading assets (INT) |

## 3. Artifact status

| Model ID | Chapter | Specification | Review (result) |
|---|---|---|---|
| `ii_dep_banks_other` | `handbook/models/interest-income/calculators/ii_dep_banks_other.md` — **APPROVED (user gate) 2026-07-23** | `specifications/interest-income/calculators/ii_dep_banks_other.yaml` | `reviews/interest-income/calculators/ii_dep_banks_other.review.md` — APPROVE (source-grounding); user gate passed 2026-07-23 |
| `ii_other_ida` | `handbook/models/interest-income/calculators/ii_other_ida.md` — **APPROVED (user gate) 2026-07-23** | `specifications/interest-income/calculators/ii_other_ida.yaml` | `reviews/interest-income/calculators/ii_other_ida.review.md` — APPROVE (source-grounding; OQ-024 filed); user gate passed 2026-07-23 |
| `ii_ust` / `ii_mbs` / `ii_other_sec` | Increment 2 | Increment 2 | — |
| `ii_loans` | Increment 3 | Increment 3 | — |
| `nii_trading_al` | Increment 4 (regression-chapter shape per `ie_other_borrowing`) | Increment 4 | — |
| Cross-cutting | `handbook/cross-cutting/asset-side-common-conventions.md` — **APPROVED (user gate) 2026-07-23** | n/a | covered by the two calculator reviews for Increment 1 claims |

## 4. Sharing boundary

Share **exactly what the Fed shares** (conventions chapter §1/§11): the securities three-term
template within Family B; the A33–A38 rate machinery within the loans model; nothing across
families. The Family A calculators remain two independent models despite their similar form —
mirroring the liability-side rule that genuine methodology differences are never harmonized.

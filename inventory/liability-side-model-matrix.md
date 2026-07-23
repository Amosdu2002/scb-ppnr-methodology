# Liability-Side Model Matrix — Proposed 2026 Interest-Expense Models

**Created at the liability-side integration gate, 2026-07-17.** Navigation summary for the five
completed interest-expense methodology packages. **All five models are PROPOSED for the 2026
stress test (public-comment stage) — NOT adopted.** Full detail lives in the chapters and YAML
specs; this matrix never overrides them. Citations and labels are in the chapters.

Chapter numbering runs 7–10 and 12; chapter 11 is reserved for `nii_trading_al` (net trading
NII), which is not part of this liability-side family.

Conventions shared by all five rows — launch point PQ0 (D-005); annualized rates with ÷4 only at
the final quarterly-dollar step (D-004, never attributed to the Fed); flat balances from PQ0;
nine projection quarters; no upstream model dependencies in the Fed suite (project-level
exception: the PID-OB-5 α_b calibration consumes the other four expense paths plus the FRB
total-interest-expense path); validation principles — are stated once
in `handbook/cross-cutting/liability-side-common-conventions.md`.

## 1. Methodology at a glance

| Model ID | Fed component (section) | Type / form | Primary balances | Scenario variables | Major parameters | Core calculation | Balance behavior | Floor / constraint |
|---|---|---|---|---|---|---|---|---|
| `ie_dom_time_dep` | Interest Expense on Domestic Time Deposits — B.v.a(7), PDF pp. 209–211 | Structural — WAL repricing recursion | Avg. domestic time-deposit balance; source names no item; project: Schedule G 34E [PID-1] | `usd_1y_treasury` | ρ_b = 3/WAL_months (derived, constant); **no estimated parameters** | Eq A44 rate recursion seeded by item 42E; expense = balance × rate ÷ 4 | Balance flat [PID-1]; ρ_b constant (source-stated) | **None** — no floor, cap, or regime |
| `ie_other_dom_dep` | Interest Expense on Other Domestic Deposits — B.v.a(8), PDF pp. 211–215 | Structural — two-regime deposit beta (ELB / non-ELB) | A47 weights and expense balance: Schedule G 34B/34C/34D [PID-ODD-1; multiplicand per PID-ODD-3, 2026-07-23]; optional monitor reference: MDRM sum BHCB3187+BHOD3187+BHCB2389+BHOD2389 [PID-ODD-2] | `usd_3m_treasury` (level, change, 25 bp trigger) | Table A7 median betas (MMA 0.620/0.645; Savings 0.310/0.335; Transaction 0.465/0.490); Spread(i,b) from 2020:Q2–2021:Q4 | Eqs A45 (ELB) / A46 (non-ELB) per subcomponent, A47 balance-weighted aggregation; expense = avg. balance × agg. rate ÷ 4 | Balances and weights flat (INT via general convention) | assumed_floor binds inside Eq A46 only; **no** floor in ELB quarters (A45 is an equality) |
| `ie_foreign_dep` | Interest Expense on Foreign Deposits — B.v.a(9), PDF pp. 215–216 | Structural — two-regime deposit beta (**A45–A47 by reference** from v.a(8)) | Schedule G 35A (non-time) / 35B (time); expense balance = 35A+35B [INT-a, candidate PID] | `usd_3m_treasury` | Table A7 foreign medians (non-time 0.890/0.790; time 1.000/1.000); Spread(i,b) | Same framework as `ie_other_dom_dep` with foreign items (rates 43A/44B); expense = (35A+35B) × agg. rate ÷ 4 | Balances flat; no FX effects (source-stated) | Same as `ie_other_dom_dep` |
| `ie_fed_funds_repo` | Interest Expense on Federal Funds Purchased and Securities Sold under Agreements to Repurchase — B.v.a(10), PDF pp. 216–219 (heading variant "the Agreement to Repurchase") | Structural — direct calculator | Schedule G 36A+36B [PID-FFR-1]; source misnames rate items 44A/44B as the balances (SQ-16/OQ-019) | `usd_3m_treasury` (used raw as the rate) | **None** — no beta, scalar, spread, or threshold | Eq A48: expense = (36A+36B) × Treasury3m ÷ 4 | Balance flat — **source-stated** B(b,q) = B(b,q0) | **None** |
| `ie_other_borrowing` | Interest Expense on Other Borrowing — B.v.d(2), PDF pp. 230–234 | **Regression** — OLS rate/credit-spread model | Fed-stated scope Schedule G 44C+46+47; physical: 36C+38+39 [PID-OB-2]; share numerators FR Y-9C BHCK2309, BHDM4062+BHDMC699 | `usd_3m_treasury` (coefficient 1 by construction), `bbb_corporate_yield` (×β1) | Table A9: β1 0.254, β2 −0.036, β3 0.066; α_b **not disclosed** — calibrated over the nine-quarter cumulative vs the FRB total-interest-expense path [PID-OB-5] | Eq A53: rate = Treasury3m + (β1·BBB + β2·CP share + β3·subdebt share + α_b); expense = B(b,0) × rate ÷ 4 | Balance flat and **composition shares frozen** at PQ0 (source-stated) | **None** — negative rates legal, logged |

## 2. Conventions, hedge boundary, and artifact status

| Model ID | Rate & quarterly conversion | Hedge boundary | Unresolved items | Chapter | Specification | Review (result) |
|---|---|---|---|---|---|---|
| `ie_dom_time_dep` | Annualized; ÷4 at final step only (D-004/PID-6) | Exposes expense path; v.c adjustment external; OQ-005 | OQ-005 | `handbook/models/interest-expense/deposits/ie_dom_time_dep.md` | `specifications/interest-expense/deposits/ie_dom_time_dep.yaml` | **Report artifact MISSING** — review ran 2026-07-17 (chapter banner/brief) but was not preserved; follow-up focused review required (integration finding) |
| `ie_other_dom_dep` | Annualized; ÷4 at final step only (D-004) | Exposes expense path; v.c external; OQ-005 | OQ-005, OQ-013, OQ-017, OQ-018, OQ-021 | `handbook/models/interest-expense/deposits/ie_other_dom_dep.md` | `specifications/interest-expense/deposits/ie_other_dom_dep.yaml` | `reviews/interest-expense/deposits/ie_other_dom_dep.review.md` — PASS, no corrections required |
| `ie_foreign_dep` | Annualized; ÷4 at final step only (D-004) | Exposes expense path; v.c external; OQ-005 | OQ-005, OQ-013, OQ-017, OQ-018, OQ-019, OQ-020, OQ-021; candidate PIDs INT-a…INT-f await user confirmation | `handbook/models/interest-expense/deposits/ie_foreign_dep.md` | `specifications/interest-expense/deposits/ie_foreign_dep.yaml` | `reviews/interest-expense/deposits/ie_foreign_dep.review.md` — source-faithful as drafted |
| `ie_fed_funds_repo` | Annualized; ÷4 at final step only (D-004) | Exposes expense path; v.c external; OQ-005 | OQ-005, OQ-019; MEV column name (CODE TODO) | `handbook/models/interest-expense/funding/ie_fed_funds_repo.md` | `specifications/interest-expense/funding/ie_fed_funds_repo.yaml` | `reviews/interest-expense/funding/ie_fed_funds_repo.review.md` — APPROVE |
| `ie_other_borrowing` | Annualized; ÷4 at final step only (D-004; the PID-OB-5 closed form reverses the same ÷4 once, ×4) | Exposes expense path; v.c external; OQ-005; **α_b embeds hedge intensity** (Fed rationale) — and under PID-OB-5 the full residual to the FRB total — double-counting caution if v.c is later applied | OQ-005, OQ-022, OQ-023 (FRB-total source); PID-OB-4 BBB input gates (4 items); OQ-009 resolved for this model (PID-OB-5) | `handbook/models/interest-expense/funding/ie_other_borrowing.md` | `specifications/interest-expense/funding/ie_other_borrowing.yaml` | `reviews/interest-expense/funding/ie_other_borrowing.review.md` — APPROVE WITH OPEN IMPLEMENTATION ITEM |

## 3. Genuine methodology differences (kept explicit — never harmonized)

- **Four distinct calculation forms**: A44 WAL recursion (`ie_dom_time_dep`) ≠ A45–A47 two-regime
  beta (`ie_other_dom_dep`, `ie_foreign_dep`) ≠ A48 direct calculator (`ie_fed_funds_repo`) ≠ A53
  OLS regression (`ie_other_borrowing`).
- Only `ie_dom_time_dep` uses the **1-year** Treasury; the other four use the 3-month (plus BBB
  for `ie_other_borrowing`).
- Only `ie_other_borrowing` has estimated coefficients and a firm fixed effect (calibrated per
  PID-OB-5 — nine-quarter cumulative match to the FRB total-interest-expense path); the four
  structural models have none.
- Expense-balance sourcing differs deliberately: `ie_other_dom_dep`'s A47 weights and expense
  multiplicand come from **different physical sources** (PID-ODD-1 vs PID-ODD-2, with a
  consistency monitor) — **revised by PID-ODD-3 (2026-07-23):** the 34B–34D weight sum is now
  also the expense multiplicand (company-reference confirmed), and the PID-ODD-2 MDRM sum is
  an optional monitor reference only; `ie_foreign_dep` uses the same 35A/35B balances for both (INT-a).
- Deposit betas and the ELB regime exist only in the two Equations A45–A47 models; the WAL
  mechanism exists only in `ie_dom_time_dep`.

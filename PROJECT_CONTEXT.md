# Project

## Working title

Federal Reserve Proposed 2026 PPNR Net-Interest Methodology Handbook

## Background

An existing confidential Excel implementation calculates Federal Reserve PPNR
projections used in an SCB-related process. The confidential workbook cannot be
provided in this project.

Phase 1 focuses exclusively on understanding the public Federal Reserve
methodology and translating it into a coding-friendly handbook.

Later phases will use the approved handbook to design a generic Python
architecture. The actual Excel mapping, confidential implementation, and
reconciliation will occur only in the approved company environment.

## Source documents

- sources/fed/pre-provision-net-revenue-models.md
- sources/fed/pre-provision-net-revenue-models.pdf

The PDF is authoritative. The Markdown file is the searchable working copy.

## Methodology status

The source documents describe both:

1. The current model suite used before the proposed changes.
2. A proposed new model suite for 2026.

The primary project scope is the proposed suite in Section v, beginning on
source PDF page 167.

Do not describe the proposed models as adopted or production models unless
another authoritative source explicitly establishes that status.

## Phase 1 scope

### Interest income

- Interest income on loans
  - Corporate
  - Commercial real estate
  - Mortgage
  - Auto
  - Consumer and small-business credit card
  - Other consumer products
- Deposits with banks and other
- U.S. Treasuries
- Mortgage-backed securities
- Other securities
- Other interest/dividend-bearing assets
- Trading Assetss and Liabilities NII (Back solved fixed effect)

### Interest expense

- Domestic time deposits
- Other domestic deposits
- Foreign deposits
- Federal funds purchased and securities sold under agreements to repurchase
- Other borrowing (Backsolved fixed effect)
  - Short-term borrowing
  - Subordinated debt
  - Other interest-bearing liabilities

### Cross-cutting topics

- Common structural-model conventions
- Launch-point (PQ0) assumptions
- Constant-balance and constant-composition assumptions
- Fixed-rate and variable-rate treatment
- Repricing and maturity treatment
- Industry scalars and deposit betas
- Interest-rate-risk hedge adjustments
- Estimated parameters in Tables A7, A8, and A9
- Dependencies and execution order

## Initially out of scope

- Noninterest income
- Noninterest expense
- Reproducing the current 2025 regression suite in full
- Reverse engineering the confidential Excel implementation
- Production Python implementation
- Confidential firm inputs or outputs

## Phase 1 deliverables

1. Source-integrity review
2. Model inventory
3. Source map
4. Common methodology chapter
5. One reviewed handbook chapter per model or model segment
6. Cross-cutting interest-rate-hedge chapter
7. Parameter inventory
8. Model dependency map
9. Open-question log
10. Coding-oriented model specifications after methodology review

## Success standard

A future Python developer should be able to determine from the handbook:

- what each model projects;
- what inputs it requires;
- the dimensions, units, and timing of those inputs;
- the calculation sequence;
- what remains constant and what changes over time;
- how scenario variables enter;
- which parameters are supplied or estimated;
- how models depend on one another; and
- which methodological points remain unresolved.
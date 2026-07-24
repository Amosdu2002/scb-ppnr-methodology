# Securities Positions Input Contract (PID-SEC-6)

> **Status: user-confirmed layout, 2026-07-24** (PID-SEC-1/PID-SEC-5/PID-SEC-6/PID-MBS-1,
> registry in `handbook/open-questions.md`). This document is the **generic** description of
> the securities input workbook the loaders read natively — the user confirmed the sample
> layout "matches what we will have eventually as the input". Physical details (workbook path,
> exact sheet names, header aliases) are **company-local config** (`config/local/`, gitignored)
> and never appear here. No firm identifiers, holdings, or values appear in this document; the
> committed synthetic fixtures use invented securities. Two open cells are gated
> TO_BE_CONFIRMED (§7). Labels: [FACT] = Fed-stated; [PID] = user-confirmed project decision;
> [CODE] = implementation rule.

## 1. Scope and relation to D-007

The Family A calculators keep the D-007 two-sheet contract. The securities family (PID-SEC-1:
**security-level** granularity) adds a **third input**: one workbook, read as-is, with three
kinds of sheets — a positions sheet, enrichment tabs, and a prepayment pivot. Aggregation to
component level happens **inside the model**, mirroring the Fed's per-security calculation
[FACT: security-level microdata, PPNR pp. 190, 195, 200].

## 2. Positions sheet (FR Y-14Q Schedule B.1 layout)

Header convention [PID-SEC-6]: **three header rows** — technical field name / long
description / MDRM code — with **data from row 5**. Blank leading row(s) before the header
block are tolerated; the loader locates the header block by the MDRM row. Column registry
(generic name ← MDRM):

| Generic name | MDRM | Role in the models | Type / units |
|---|---|---|---|
| `report_date` | D_DT | reporting quarter end (= PQ0 date) | integer `yyyymmdd` |
| `rssd_id` | ID_RSSD | reporting-institution id (pass-through) | text |
| `unique_id` | CQSCS383 | security transaction unique id | text |
| `identifier_type` | CQSCP082 | CUSIP \| ISIN | text |
| `identifier_value` | CQSCP083 | **join key** to enrichment + prepayment sheets | text |
| `private_placement` | CQSCS370 | data-quality context (vendor-match fallbacks) | Y/N |
| `security_description_1` | CQSCP084 | **category → model assignment (PID-SEC-5, §5)** | text |
| `security_description_3` | CQSCP086 | sub-description (context) | text |
| `amortized_cost` | CQSCP087 | A40 accretion; A42 combined term; PID-SEC-3 trigger | money (scale §7 TBC) |
| `market_value` | CQSCP088 | context / validation only | money |
| `current_face_value` | CQSCP089 | coupon accrual (per PID-SEC-4); reconciles prepayment PQ0 | money, **already USD-converted** [PID-SEC-6] |
| `original_face_value` | CQSCP090 | PID-SEC-3 notional candidate (§7 TBC) | money |
| `credit_loss_allowance` | CQSCJH85 | pass-through (not used by income) | money |
| `writeoffs` | CQSCJH87 | pass-through | money |
| `accounting_intent` | CQSCP092 | AFS \| HTM \| EQ — **EQ ⇒ out of scope** [PID-SEC-5]; drives reinvestment designation [FACT, MRM p. 73] | text |
| `pricing_date` | CQSCP093 | pricing date (user-confirmed 2026-07-24 — **not** a price) | date `mm/dd/yyyy` |
| `book_yield` | CQSCP094 | A42 combined term; `ii_mbs` coupon fallback [FACT] | rate (scale §6) |
| `purchase_date` | CQSCP095 | unsettled-trade context (PID-SEC-3) | date |
| `currency` | CQSCS371 | informational — balances already USD [PID-SEC-6] | text |
| `price` | CQSCJH21 | PID-SEC-3 price candidate (§7 TBC) | per-100 price |
| `transtype` | (internal) | transaction-type context (unsettled trades) | text |
| `frb_model_category` | (derived) | optional convenience column; the loader **recomputes** the PID-SEC-5 assignment from `security_description_1` and cross-checks — mismatch is an error | text |

## 3. Enrichment tabs ("vendor data" role [FACT])

One or more tabs (region splits allowed), each keyed by `identifier_value` (CUSIP or ISIN);
per-tab column aliases are config-declared (the tabs may spell headers differently). Canonical
fields per security:

| Field | Notes |
|---|---|
| `maturity_date` | **Excel serial number** (days since 1899-12-30) — normalized at ingestion |
| `coupon_rate` | **percent scale** (e.g. 7.25) — normalized to annualized decimal; user-stated **never blank** |
| `rate_type` | FIXED \| FLOATING \| ZERO COUPON (zero-coupon accrues at book yield [FACT, PPNR p. 196]) |
| `coupon_floor` | may be blank (incl. literal "(blank)" — treated as missing); feeds PID-SEC-2 |
| `wal_years` | decimal years; A41 uses 4 × WAL(t=0) [FACT]; **negative/zero WAL is highlighted as a warning, treatment deferred (user-parked 2026-07-24)** |
| `floater_indicator` | Y/N — optional per-tab cross-check column (`floater_indicator_column`); redundant with `rate_type`, which is what makes disagreement informative: mismatches are logged as data-quality monitors (rate type governs; never blocked) |
| `currency` | informational |

## 4. Prepayment pivot sheet (PID-MBS-1)

Excel-pivot layout: a title row ("Sum of current_face"), then the header row **"Row Labels"**
followed by **month-offset columns 0, 3, 6, …, 27** (≙ PQ0..PQ9; PQ index = months ÷ 3) and a
**Grand Total** column (ignored). Data rows: one per Agency MBS security, label =
`identifier_value` (CUSIP); values = **projected current face value in USD** per quarter,
monotone non-increasing. Rules [PID-MBS-1 / PID-SEC-5]:

- Face(i,q) is used directly by the A41 terms (coupon accrual on the prior-quarter EOP face,
  PID-SEC-4). The equivalent survival factor is Face(i,q)/Face(i,PQ0) if ever needed.
- **Validation:** Face(i,PQ0) must reconcile with the positions sheet's `current_face_value`
  for the same CUSIP (tolerance-checked; mismatch surfaces).
- An Agency MBS **absent** from this sheet carries **no prepayment** — face held flat
  (user-stated: such positions are multi-family).
- **Pivot blanks read as 0** — an empty cell means "no balance" in a pivot; blanks are
  converted to 0 with a logged per-row warning listing the affected quarters (never guessed
  differently).
- A row whose **PQ1 face is 0 — including blank — is skipped at load** (user-directed
  2026-07-24), with a logged warning per row. Consequence: if the skipped CUSIP is still an
  in-scope Agency MBS position, it falls back to the flat-face (no-prepayment) treatment above.
- Non-Agency securities never appear here (no prepayments modeled [FACT, PPNR pp. 197, 202]).

## 5. Category → model assignment (PID-SEC-5)

Applied to `security_description_1` (the FR Y-14Q B.1 vocabulary — cf. MRM Figure A-1, p. 9).
**Unknown or unmapped categories are a hard error — surface and ask; never default.**

| `security_description_1` | Model | Prepayment |
|---|---|---|
| US Treasuries & Agencies | `ii_ust` | no |
| Agency MBS | `ii_mbs` (prepayment category) | yes — pivot sheet; absent ⇒ none |
| CMBS; Domestic Non-Agency RMBS (incl HEL ABS); Foreign RMBS | `ii_mbs` (non-prepayment) | no [FACT] |
| Mutual Fund; Common Stock (Equity) — accounting intent EQ | **out of scope** (no coupon interest) | — |
| all other debt categories (Corporate Bond, Sovereign Bond, Municipal Bond, Covered Bond, CDO, CLO, Auto ABS, Credit Card ABS, Student Loan ABS, Other ABS (excl HEL ABS), Auction Rate Securities, Preferred Stock, Other, …) | `ii_other_sec` | no [FACT] |

The general convention: MBS-family categories → `ii_mbs`; Treasuries/Agencies → `ii_ust`;
equity-intent → out of scope; every other debt category → `ii_other_sec`. Categories not
listed above follow this convention only after being surfaced and confirmed.

## 6. Normalization conventions [CODE]

- **Three date encodings**, normalized at ingestion: `yyyymmdd` integers (`report_date`),
  Excel serials (enrichment `maturity_date`), `mm/dd/yyyy` (`pricing_date`).
- **Rates**: enrichment coupon rates are percent-scale → annualized decimal (D-004 basis);
  `book_yield` scale declared in config (percent | decimal), never guessed.
- **Money**: `current_face_value` and prepayment faces are USD (whole-dollar magnitudes
  observed); canonical model unit stays USD millions (D-006) — the loader converts once, with
  the positions-sheet money scale declared per §7.
- Literal placeholder strings ("(blank)") and empty cells are both **missing**.
- Maturity date → `maturity_quarters` relative to `report_date` (rounding convention fixed at
  code time and logged); WAL years → the A41 4× factor applies as printed [FACT].

## 7. Confirmation register (updated 2026-07-24)

| Item | Status |
|---|---|
| Positions-sheet money scale | **CONFIRMED: whole USD** (user, 2026-07-24); declared in config as `money_scale = "dollars"`, converted once to the canonical USD millions (D-006) |
| PID-SEC-3 price column | **CONFIRMED: `price` (CQSCJH21), per-100** (user: "always around 100 ish") |
| PID-SEC-3 notional column | **CONFIRMED: `current_face_value`** (user, 2026-07-24) |
| PID-SEC-2 floor treatment | **CONFIRMED: three config-switchable modes** — `floor_mode` ∈ `zero` \| `security_floor` \| `none` (see PID-SEC-2) |
| `book_yield` scale | declare in config (`percent` \| `decimal`) — refused if undeclared |

## 8. Out of scope for this contract

The FRB family paths and calculator inputs stay on the D-007 sheets; scenario series stay in
the MEV workbook ([mev] config). Nothing in this contract carries confidential values — the
committed synthetic fixture workbook (built at the code increment) uses invented securities
with hand-calculable numbers.

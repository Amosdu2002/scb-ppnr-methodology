# Securities Positions Input Contract (PID-SEC-6)

> **Status: user-confirmed layout, 2026-07-24** (PID-SEC-1/PID-SEC-5/PID-SEC-6/PID-MBS-1,
> registry in `docs/handbook/open-questions.md`). This document is the **generic** description of
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
| `purchase_date` | CQSCP095 | **loaded and used** since PID-SEC-13 (2026-07-28): scopes the PID-SEC-3 price proxy to genuine near-settle rows (\|purchase − report\| ≤ `unsettled_window_days`). Optional — absent ⇒ no row is classifiable and every blank-amortized-cost row follows `missing_ac_mode`, logged per run | date |
| `currency` | CQSCS371 | informational — balances already USD [PID-SEC-6] | text |
| `price` | CQSCJH21 | PID-SEC-3 price candidate (§7 TBC) | per-100 price |
| `transtype` | (internal) | transaction-type context (unsettled trades) | text |
| `frb_model_category` | (derived) | optional convenience column; the loader **recomputes** the PID-SEC-5 assignment from `security_description_1` and cross-checks — mismatch is an error | text |

### 2a. Optional technical input columns (PID-SEC-9, 2026-07-24)

The positions sheet may additionally carry the reference implementation's **own model-input
columns** on the same MDRM header row, located by **exact header text** declared in config
(`[firm_data.securities]` keys). All three are **decimal** units — no scale is applied:

| Config key | Role | Precedence |
|---|---|---|
| `positions_maturity_years_column` | maturity in years (decimal) | **fallback** when the enrichment maturity date is missing — feeds the PID-SEC-8 accretion denominator AND event timing (quarters = ceil(4 × years)); PID-SEC-7 (Agency WAL) applies only after both are missing |
| `positions_coupon_column` | coupon rate (decimal) | **fills blanks** — the enrichment coupon stays primary |
| `positions_floor_column` | coupon floor (decimal) | **preferred** over the enrichment floor when non-blank — it is the reference's own floor input, and drives `floor_mode = "security_floor_else_zero"` (PID-SEC-2 mode 4) |
| `positions_rate_type_column` | the sheet's own float/fixed indicator (text) | **verification-only** — carried on the position (`excel_rate_label`) for the compare bake-off and a disagreement monitor; the enrichment rate type keeps driving the models until a PID adopts the indicator |

A declared-but-absent column is a hard error (surface and ask — a config/data mismatch, never
silently ignored). Usage is logged as per-run counts, per-security for coupon fills.

## 3. Enrichment tabs ("vendor data" role [FACT])

One or more tabs (region splits allowed), each keyed by `identifier_value` (CUSIP or ISIN);
per-tab column aliases are config-declared (the tabs may spell headers differently). Canonical
fields per security:

| Field | Notes |
|---|---|
| `maturity_date` | **Excel serial number** (days since 1899-12-30) — normalized at ingestion. **PID-SEC-7 fallback (Agency MBS only, user-confirmed 2026-07-24):** when the maturity date is missing, WAL is used as the maturity in years — maturity_quarters = ceil(4 × WAL), min 1, logged per security |
| `coupon_rate` | **percent scale** (e.g. 7.25) — normalized to annualized decimal; user-stated **never blank** |
| `rate_type` | FIXED \| FLOATING \| VARIABLE (≙ floating; company vocabulary, 2026-07-24) \| ZERO COUPON (accrues at book yield [FACT, PPNR p. 196]) \| STEP CPN / STEP labels — treated as **fixed at the launch coupon**, logged per security [INTERIM — the Fed model has no step machinery; pending user confirmation] |
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
- **Pivot blanks ARE 0** — silently (user-directed 2026-07-24: the reference workbook treats
  them the same way; no warning).
- A row whose **PQ1 face is 0 — including blank — is skipped at load** (user-directed
  2026-07-24), with a logged warning per row. Consequence: if the skipped CUSIP is still an
  in-scope Agency MBS position, it falls back to the flat-face (no-prepayment) treatment above.
- Non-Agency securities never appear here (no prepayments modeled [FACT, PPNR pp. 197, 202]).
- **Multi-lot CUSIPs (2026-07-24; per-row computation user-verified — PID-SEC-8):** the
  positions sheet carries multiple rows (lots) per CUSIP; each row becomes its own position
  keyed by `unique_id` (CQSCS383; fallback `CUSIP#rN` when absent, plain CUSIP for single
  rows). The CUSIP's prepayment path is applied **per row as a survival factor scaled by the
  lot's own launch face** — face(row, q) = row face × path(q)/path(PQ0) — with a logged
  summary count.
- **Missing enrichment (2026-07-24):** a position with no enrichment match is **skipped with a
  HIGHLIGHT warning** (previously a hard stop) — pending user confirmation of skip vs data fix.
- **Paydown reinvestment (2026-07-24, OQ-025(c) resolution):** quarterly face declines
  (paydowns) reinvest into the 1Y-Treasury ledger exactly like maturities (MRM p. 72 [FACT];
  first-day-of-following-quarter timing [INT]); config `reinvest_paydowns` (default true)
  toggles it for A/B runs.
- **Reference income columns (verification only):** when the header row carries
  `II_PQ1..II_PQ9`, they are attached per position as `reference_income` for the diagnostic's
  `--compare` mode; the models never consume them.

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
- **Excel formula-error literals** (`#VALUE!`, `#N/A`, `#REF!`, `#DIV/0!`, `#NAME?`, `#NULL!`,
  `#NUM!`) are **missing** (user-directed 2026-07-27): the sheet's derived columns (§2a) are
  formulas that error when their own inputs are absent, so an error cell carries no value —
  the field falls back per its normal chain (maturity → AA held at 0; coupon → the no-coupon
  surfacing; floor → mode's else-branch). A per-run census warning counts them per field.
- Maturity date → `maturity_quarters` relative to `report_date` (rounding convention fixed at
  code time and logged); WAL years → the A41 4× factor applies as printed [FACT].

## 7. Confirmation register (updated 2026-07-24)

| Item | Status |
|---|---|
| Positions-sheet money scale | **CONFIRMED: whole USD** (user, 2026-07-24); declared in config as `money_scale = "dollars"`, converted once to the canonical USD millions (D-006) |
| PID-SEC-3 price column | **CONFIRMED: `price` (CQSCJH21), per-100** (user: "always around 100 ish") |
| PID-SEC-3 notional column | **CONFIRMED: `current_face_value`** (user, 2026-07-24) |
| PID-SEC-2 floor treatment | **Four config-switchable modes** — `floor_mode` ∈ `zero` \| `security_floor` \| `none` \| `security_floor_else_zero`; the fourth (2026-07-24) is the reference-workbook rule: every floater floored at its security floor when on file, else at 0 — pending compare-run confirmation |
| `book_yield` scale | declare in config (`percent` \| `decimal`) — refused if undeclared |
| Reference II_PQ income scope | **RESOLVED 2026-07-24 (dual ratios):** the II_PQ1..9 columns EXCLUDE reinvestment income — compare mode's primary ratio is xr/ref |
| PID-SEC-9 technical columns | maturity-years fallback / coupon blank-fill / preferred floor / float-fixed indicator — precedence table in §2a; Excel error literals = missing (§6) |
| PID-SEC-10 floating projection | `floating_projection` ∈ `spot` \| `neg_hold` \| `neg_hold_blend13` — reference-identified 2026-07-27 (negative margins held at the launch coupon; monthly-reset PQ1 blend), pending confirmation rerun |
| PID-SEC-11 book-yield categories | `book_yield_categories` — categories accruing at book yield held flat (Municipal Bond identified 2026-07-27), pending the user's formula check |

## 8. Out of scope for this contract

The FRB family paths and calculator inputs stay on the D-007 sheets; scenario series stay in
the MEV workbook ([mev] config). Nothing in this contract carries confidential values — the
committed synthetic fixture workbook (built at the code increment) uses invented securities
with hand-calculable numbers.

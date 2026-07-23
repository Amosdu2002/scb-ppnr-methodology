# Market Risk Models — Securities Model (Section A): Extracts Working Copy

> **Scope: deliberately partial.** This file transcribes ONLY the passages of
> *Supervisory Stress Test Model Documentation: Market Risk Models* (October 2025,
> Updated January 2026; `sources/fed/market-risk-models.pdf`, SHA-256 `7e9f633b…`,
> see `inventory/source-integrity-review.md` §11) that the PPNR interest-income
> securities models delegate to the "Securities Model Description" (PPNR footnotes
> 64–65; Questions A164/A168/A174). The full Section A (pp. 7–77) covers the
> Securities Model's fair-value, credit-loss, and OCI machinery, which is outside
> the net-interest Phase 1 scope. **The PDF is authoritative**; extracts below were
> transcribed from `pdftotext` output and verified against page images for
> pp. 7–10, 18–20, and 72–74 (2026-07-23).
>
> **Citation convention:** cite this source as `(MRM p. N)`. **Equation-numbering
> collision warning:** this volume labels equations with a hyphen ("Equation A-3",
> "A-32", "A-41"), numerically colliding with PPNR equation names ("A32", "A41").
> Never cite an equation number without the document prefix.

## 1. Document identity and Section A structure

Title page: "Supervisory Stress Test Model Documentation — Market Risk Models —
October 2025 — Updated January 2026" (MRM p. 1). Preface (MRM p. 2): the volume
covers the Securities, Fair Value Option, Yield Curve, Private Equity, Trading
Profit and Loss, Trading Issuer Default Loss, CVA, and LCPD Models for the 2026
Supervisory Stress Test. Section A "Securities Model" spans pp. 7–77: i. Statement
of Purpose (7) · ii. Model Overview (7) · iii. Fair Value Model (13) · iv. Credit
Loss Model (48) · v. OCI Calculation (57) · vi. Question (77). Running page
header: "Model Documentation: Securities Model".

Identification basis for OQ-004 (INT, strong): no standalone "Securities Model
Description" volume exists in the 2026 documentation series; this section's
running header names it; PPNR footnote 52 cross-references this same volume for
the Yield Curve Model; and §5 below **explicitly names the PPNR structural
interest-income model**.

## 2. Fair Value Model methods overview (MRM p. 10)

"For AFS debt securities, the model uses three methods to project fair values,
depending on the type of security: a present-value calculation for Treasuries,
full revaluation for Agency MBS using a third-party vendor model, and a
duration-based approximation for all other debt securities."

## 3. Third-party vendor model for Agency MBS (MRM pp. 18–20) — page images verified

Referenced by PPNR footnote 65 ("For additional details on the incorporation of
macroeconomic variables into the vendor model, please refer to the Securities
Model Description", PPNR p. 196).

- "An important feature of Agency MBS is the embedded prepayment option … A
  variety of factors influence a borrower's decision to prepay their mortgage,
  such as the current and historical rate environment, housing market
  developments, and broader macroeconomic conditions. Prepayments on the
  underlying mortgages create uncertainty in the size and timing of cashflows for
  Agency MBS, which is accounted for in the vendor model." (MRM p. 18)
- Mechanics (MRM pp. 18–19): "For a given security and valuation quarter, Monte
  Carlo simulation is used to generate many interest rate and other economic
  variable paths, beginning in the valuation quarter and evolving over the
  remaining life of the security, conditional on macroeconomic scenario variables
  provided up to the valuation quarter. For a given such simulated path, expected
  prepayments are computed to determine expected cash flows over the remaining
  life of the security. These prepayments, both voluntary and involuntary, are
  consistent with that simulated path's interest rate and other economic variable
  projections, and account for security-specific collateral characteristics.
  Cashflows for a given path are discounted back to the valuation quarter at the
  zero-coupon U.S. Treasury rate plus an option-adjusted spread (OAS) … The
  projected price of the security is equal to the average present value across
  all simulated paths … This price … otherwise uses the vendor's default model
  calibration without any adjustment or overlay and incorporates aging and
  paydown of the security over the projection horizon."
- **Equation A-3** (MRM p. 19): P^VEND(i,t) = f(i, OAS(i,t), X^MACRO(q=1..t)).
  OAS(i,t) = initial vendor-computed OAS (equating P^VEND(i,0) to market value ÷
  face at quarter 0) plus the scenario's projected change in the U.S.
  Mortgage-Backed Securities OAS index (passthroughs) or the U.S. Agency CMO OAS
  index (CMOs) — both Auxiliary Scenario Variables (MRM Section I).
- **Macroeconomic inputs, itemized** (MRM p. 19): "U.S. mortgage rate, U.S. prime
  rate, U.S. unemployment rate, U.S. House Price Index, zero-coupon Treasury
  curve and Secured Overnight Financing Rate (SOFR) curve." (Footnote 17: HPI
  sourced in practice from the U.S. Long-term HPI, quarters 1–13 identical to the
  scenario HPI; footnote 18: curves per the Yield Curve Model, MRM Section C.)
- **Equation A-4** (MRM p. 20): FV(i,t) = F(i,0) × P^VEND(i,t) — price applied to
  the quarter-0 face value under the existing framework.

## 4. Constant portfolio assumption — the CURRENT Securities Model framework (MRM p. 62)

"The OCI Calculation generally assumes the size and duration of the securities
portfolio, as reported at quarter 0, remains constant over the nine-quarter
supervisory stress test projection horizon. This is accomplished by holding the
face value, amortized cost, and remaining maturity of each security constant each
quarter **without aging**. … Limitations of the constant portfolio assumption
include not capturing the changes in risk resulting from the aging of securities,
and **not incorporating reinvestments for maturing securities into the modeling
framework**." (Footnote 46: Agency MBS excepted from constant duration — they
capture scenario prepayment/duration effects; footnote 48: reinvestments would
offset balance-sheet reductions where securities pay down and mature.)

**Reading note (INT):** the *current* Securities Model has no reinvestment; the
reinvestment machinery lives in the Alternative Approaches below — which is what
the proposed PPNR income models (which do incorporate maturities) share.

## 5. Alternative Approaches — reinvestment framework (MRM pp. 65–74)

Under "Alternative Approaches — (1) Reinvestment assumption" (MRM p. 65): "The
Board is considering an alternative approach for both the present value
calculation of U.S. Treasuries and the full revaluation model of Agency MBS. …
changes are required to incorporate both aging and prepayments." Alternative
fair-value/amortized-cost equations for Treasuries: MRM Eq A-32 (p. 66, aged
present value), Eq A-33 (p. 68, straight-line amortized cost). Footnote 54 (MRM
p. 68): "If a Treasury reaches maturity within the projection horizon, it ceases
to exist after maturity, and projections are not generated for this security in
subsequent quarters. The proceeds of the matured security are reinvested into a
new security that is revalued in each subsequent quarter." Agency MBS
alternative: paydown-adjusted face values and amortized cost (MRM Eqs A-34–A-39,
pp. 70–72); "Agency MBS without Vendor Pricing" fallback (MRM Eq A-40, p. 72).

### (vii) Reinvestment Methodology (MRM pp. 72–74) — page images verified; the core delegated content

- Purpose: "To maintain the constant balance sheet assumption, a firm must
  purchase new securities during the projection horizon to offset the impact of
  securities maturing or decreasing in balance due to partial paydowns. … the
  Board's approach must be applicable to all firms, which, consistent with the
  Policy Statement, favors simple and broadly applicable reinvestment
  assumptions." (MRM p. 72)
- **The instrument** (MRM p. 73): "The current reinvestment assumption is a
  hypothetical Treasury security with one year to maturity. This instrument is
  assumed to be purchased at face value, issued on the purchase date, and has a
  coupon rate equal to the corresponding yield from the par Treasury curve at the
  forecast quarter in question. Projections of both fair value and amortized cost
  will be generated for the proxy reinvestment instrument, which will produce
  unrealized gains/losses. **No hedges will be assumed to be placed on
  reinvestments.**" (Wording note [FACT preserved]: "current" here appears
  *inside* the Alternative Approaches subsection — see OQ-025(e).)
- **Accounting intent preserved; explicit PPNR cross-link** (MRM p. 73): "The
  accounting intent for any reinvestment is assumed to be the same as the
  security it is replacing. For example, when a U.S. Treasury security designated
  as AFS matures, the reinvestment of that balance into a one-year U.S. Treasury
  security is also assumed to be designated as AFS. To the extent that HTM
  securities mature, reinvestment of those balances would similarly be designated
  as HTM. **Although reinvestments designated as HTM would not impact the
  projection of OCI, they would be captured in the proposed structural model for
  interest income on securities, as detailed in the PPNR Model documentation.**"
- **Stated implications** (MRM pp. 73–74): reinvesting uniformly "into one-year
  Treasuries could differ from the firm's current Treasury maturity profile and
  change the firm's portfolio repricing sensitivity"; "The one-year maturity for
  Treasuries was favored to be generally in line with post-hedge Treasury
  holdings across all firms"; reinvesting "proceeds from maturing assets
  uniformly into Treasuries could change a portfolio's exposure to both interest
  rates and spread risk"; no fair-value hedges on reinvestments — "determining
  the appropriate amount of fair value hedges to place against reinvestments
  would require firm-specific assumptions about forward asset liability
  management strategies."

## 6. Section A Question (MRM p. 77)

"Question A1: The Board seeks comment on the alternative reinvestment assumption
as described in Section A(v)(d)(1), as compared to the Board's current approach
that assumes the portfolio composition, balances, and security characteristics
remain constant at each quarter of the projection horizon."

## 7. What this file deliberately omits

The Fair Value Model's present-value and duration approximations, the Credit Loss
Model, the OCI Calculation mechanics, hedge-ratio machinery (MRM Eq A-29 region),
and the alternative-framework OCI equations (MRM Eqs A-32–A-41) beyond the
context quoted above — all outside the net-interest scope. Consult the PDF
directly if a chapter ever needs them; extend this file (and the §11 integrity
addendum) rather than citing unverified text.

# Source Brief — Interest Income on Loans: Other Consumer Products (`ii_loans` — retail/other-consumer)

> **STATUS: Proposed for the 2026 stress test — public-comment stage, NOT adopted.**
> Component: **Interest Income on Loans**, Section v.a(1) (PDF pp. 173–188; md sec-150–172); this brief covers the **Other Consumer Products** family of Retail (PDF pp. 179–180; md sec-160), plus the other-consumer-relevant passages elsewhere: the retail census's fourth entry and the non-core no-further-segmentation sentence (PDF p. 177; md sec-156), the expert-judgment split sentence (PDF p. 181; md sec-164), the "most non-core loans" prevalence entry (PDF p. 183; md sec-165), the Retail Portfolio limitations' non-core sentences (PDF p. 185; md sec-170; SQ-24), Table A8's Noncore row (PDF p. 220; md sec-209), and footnote 63's "rest of consumer" category (PDF p. 184 footer; md 5354). Model type per Table A6: **Structural**.
> Deliverable: loans workstream (asset-side Increment 3), retail wave 2 — drafted 2026-08-12 with the mortgage and card briefs at the user's direction. Review state: **DRAFT — awaiting user review.**
> Scope: **Other Consumer only.** Retail-shared rules cited from `ii_loans_retail.source-brief.md`; equations not transcribed (D-010(b)); other families appear solely at source-drawn boundaries.
> Integrity flags relevant here: SQ-24 ("retails", p. 185). Open questions: **OQ-011** (jump-off business-line mapping — this family's central gap) and **OQ-041** (engine assignment — owned here, filed at the framework brief); the retail legs of OQ-001, OQ-002, OQ-010; OQ-033.
> Physical context: the **M.1 Balances** retail wiring supplies this family's balance side (**PID-LOAN-26**, registered with the mortgage brief; noncore part restated in §0.1); **the rate-side input is NOT YET SUPPLIED** — the workbook counterpart of the "FR Y-14Q pre-provision net revenue line-item report" jump-off rates is this family's outstanding Required input (§0.1). No firm values appear in this repository.
> Verification: **PDF pp. 179–180 read as page images 2026-08-12** (both other-consumer paragraphs confirmed verbatim, including the product census; md faithful — the PDF's own "heterogenous" preserved); p. 185 at high zoom the same day. Citation format: (PDF p. N; md sec-M).

---

## 0. Classification legend and cross-reference discipline

Labels [FACT] / [PID] / [INT] / [CODE] / [OQ] / [ALT] per `ii_loans_common.source-brief.md` §0.

### 0.1 Project implementation decision register and elicitation state

| ID | Decision (one line — noncore-relevant part of the mortgage-brief registration) | Fed-source status of the same point |
|---|---|---|
| **PID-LOAN-26** | **M.1 retail wiring, noncore side**: domestic rows labeled "Retail - noncore" observed on the C&I block's **Small business** row and the Other-loans block's **Student loans**, **Non-purpose lending**, and **Other consumer loans** rows; **the international role of every retail row is "Retail - noncore"** — all international mortgage/auto/card balances roll here; the **"other consumer"** flag column marks the family's membership; values per side E/G (dom) and I/K (int), millions | The Fed's non-core census — "small business loans, SME cards, private student loans, and consumer finance products" (p. 177) and the p. 180 list including every international consumer product and "non-purpose lending" — is **physically realized** by the role labels; the Fed names no balance source (the common "portfolio balance from FR Y-14 Schedules", p. 174, is all there is) |

**Flagged observations (a)–(c) — TO CONFIRM at the review gate:**

- **(a) The exact domestic row set.** The role-labeled rows above are the observed members; whether the **lease** rows (Auto leases; Other consumer leases) carry the noncore role — they appeared unlabeled in the supplied view — and whether any other row joins the family, needs the user's statement. Rows with no role must be excluded-and-censused, never silently allocated (the PID-LOAN-19 out-of-universe discipline).
- **(b) Product-type sub-blocks vs one bucket.** The Fed assigns jump-off rates "at the aggregate **product-type** level" (p. 180) — plural product types, each with its own most-closely-aligned business line — while the M.1 wiring shows a single "Retail - noncore" role. Whether the workbook prices one merged noncore bucket at one rate, or per-product sub-blocks (student, non-purpose, other consumer, small business, international …) each with its own jump-off rate, is the family's structural elicitation item.
- **(c) The rate-side input.** **Not yet supplied**: the workbook sheet carrying the family's jump-off interest rate(s) — the counterpart of the "firm-level earned interest rates reported in the FR Y-14Q pre-provision net revenue line-item report" (p. 180) — plus the business-line mapping it embodies (OQ-011's physical form). This is the outstanding Required input for the family; the brief's source side is complete without it, the spec stage is blocked on it.

---

## 1. Executive summary

**What Other Consumer is.** [FACT] "The other consumer portfolio is a heterogenous category that includes multiple consumer credit products for which interest rate is not reported in the FR Y-14Q retail schedule regulatory filing. This category includes, but is not limited to, private student loans, other consumer loans, international auto loans, international mortgage, international home equity, international small business loans, non-purpose lending, and other miscellaneous consumer finance products." (PDF pp. 179–180; md sec-160)

**How Other Consumer prices.** [FACT] "Due to the lack of interest rate data, no segmentation is applied to these credit products. Instead, jump-off interest rates are assigned at the aggregate product-type level, using the firm-level earned interest rates reported in the FR Y-14Q pre-provision net revenue line-item report for the most closely aligned business line. Jump-off spread is derived as the difference between jump-off interest rate and Prime Rate and is held constant over projection quarters. This approach ensures consistency while maintaining a conservative and supportable basis for interest income projections." (PDF p. 180; md sec-160)

**What is unresolved.** **OQ-011** — which line of the PPNR line-item report maps to which product type is unstated ("most closely aligned business line"). **OQ-041** — the engine assignment: the no-segmentation statement and the single Prime-anchored spread sit in tension with the expert-judgment fixed/variable split (p. 181) and the "most non-core loans" fixed-rate prevalence entry (p. 183). Physically, the family's balance side is wired (PID-LOAN-26) but its **rate-side input is not yet supplied** — flagged (c).

---

## 2. Other Consumer scope and boundaries

### 2.1 Position in the hierarchy

[FACT] The fourth retail section: "other non-core credit products such as small business loans, SME cards, private student loans, and consumer finance products" (PDF p. 177; md sec-156) — an explicitly open-ended residual ("such as"; "includes, but is not limited to"). A **section**, not a Table A6 component (D-003).

### 2.2 Explicit boundaries

| Boundary | Source statement | Label |
|---|---|---|
| **Every international consumer product is here** — international auto, international mortgage, international home equity, international small business | The p. 180 census | [FACT]; physically realized — every retail row's international role is "Retail - noncore" [PID-LOAN-26] |
| **Small business loans are here; SME cards are the Card family's sub-portfolio** | The p. 177 census names both "small business loans, SME cards" in non-core, while p. 179 models small business cards inside the card section | [FACT] both statements — the census's "SME cards" entry and the card section's separate modeling coexist in the source without reconciliation; physically resolved by the M.1 wiring (SME-cards row → Card; Small-business row → noncore) [PID-LOAN-26, project context] |
| **"Non-purpose lending" here is not wholesale's NPML** | p. 180 lists "non-purpose lending" among consumer products; the wholesale NPML ("non-purpose margin loans") is a Schedule H.1 concept anchoring the Corporate proxy (PDF p. 176; md sec-154) | [FACT] two occurrences, two contexts; any relationship is **unstated** — nothing inferred (framework §12 note); the M.1 Non-purpose lending row's noncore role is the physical anchor for the retail sense [PID-LOAN-26] |
| Domestic auto, mortgage, card are their own families | The four-section census (p. 177) | [FACT] |

### 2.3 The naming pair "rest of consumer" / "Noncore"

[FACT] Footnote 63 names the scalar category "one category for **rest of consumer** loans" (PDF p. 184 footer); Table A8's row is labeled **"Noncore"** (PDF p. 220); the section prose says "non-core credit products" / "the other consumer portfolio". [INT] All three name this family; the equivalence is an inference the Board never states (part of the OQ-010 retail leg, §10).

---

## 3. Other Consumer census

[FACT] Named members (p. 177 + p. 180, union): small business loans; SME cards (census-named, physically Card — §2.2); private student loans; consumer finance products; other consumer loans; international auto loans; international mortgage; international home equity; international small business loans; non-purpose lending; other miscellaneous consumer finance products. The list is explicitly non-exhaustive.

| Observed physical member (project context, [PID-LOAN-26]) | M.1 basis |
|---|---|
| Small business (domestic) | C&I block row, role "Retail - noncore" |
| Student loans | Other-loans block row |
| Non-purpose lending | Other-loans block row |
| Other consumer loans | Other-loans block row |
| International side of every retail row (mortgage/auto/card/noncore rows' I/K columns) | International role "Retail - noncore" throughout |
| Lease rows (Auto leases; Other consumer leases) | **Membership TO CONFIRM** — flagged (a) |

[FACT of absence] The source never defines "consumer finance products," never lists the family's product types exhaustively, and never states a member count.

---

## 4. Segmentation — the stated absence

- [FACT] "Data limitations prevent further segmentation of the non-core products." (PDF p. 177; md sec-156)
- [FACT] "Due to the lack of interest rate data, no segmentation is applied to these credit products. Instead, jump-off interest rates are assigned at the aggregate product-type level…" (PDF p. 180; md sec-160)
- [INT] The two sentences compose as: no segmentation **within** a product type, while rates attach per product type — so the family's operative grain is the **product-type list itself**, not a segmentation grid. That reading is what flagged (b) tests physically (one bucket vs per-product sub-blocks); it also frames OQ-041 (§5).
- [FACT of absence] No asset-classification split, no rate-type grid, no credit-risk cut is stated for this family — uniquely among the four.

---

## 5. Engine assignment — OQ-041 (owned here)

The framework brief filed **OQ-041** (framework §7.3); this brief owns it. The three statements in tension:

1. [FACT] The family's own mechanics (p. 180): one jump-off rate per product type; **spread = jump-off rate − Prime, held constant** — the shape of the Equation A33 variable path with Prime as base rate.
2. [FACT] The spread-granularity discussion (p. 181; md sec-164): "the Board uses expert judgment to split it into variable rate and fixed-rate products."
3. [FACT] The prevalence entry (p. 183; md sec-165): "most non-core loans" are fixed-rate.

[INT — candidate reconciliation, recorded not resolved] The expert-judgment split assigns each **product type** wholly to one engine (a judgment-level rate-type attribute on the product-type list, not a data segmentation — consistent with §4's reading); fixed product types would then run A34/A35/A38 with an A36-style spread built from the same jump-off rate against Prime (spot-only), variable ones the A33 path. The source states neither this nor any alternative; what "new originations" (Eq A36) would mean for products with no rate data compounds the gap. **The retail Prime rule covers both paths** — p. 185 applies Prime "in projecting variable-rate and new origination rates" to all non-mortgage retail [FACT], so the base rate is settled even while the engine is not.

Resolution: Fed clarification or final-rule text; project-side, the workbook's noncore construction at elicitation (flagged (b)/(c); candidate PID).

---

## 6. The jump-off rate — OQ-011

- [FACT] Source: "the firm-level earned interest rates reported in the FR Y-14Q pre-provision net revenue line-item report for the most closely aligned business line" (PDF p. 180). The mapping — which line for which product type — is unstated (**OQ-011**, filed 2026-07-16; this family's central source gap).
- [INT] "FR Y-14Q pre-provision net revenue line-item report" reads as the Schedule G PPNR submission whose G.2 interest-income lines the scalar mechanism also consumes (common §8); the source does not name G.2 here, so the schedule identity itself is part of OQ-011.
- [FACT] The rate is **firm-level** and **earned** (an average yield, not an origination rate) — a granularity and construction exception to the family patterns (segment-level weighted rates elsewhere; cf. the Corporate NPML bank-level exception, OQ-037, which this family's design echoes on the retail side [INT — structural parallel, not a source statement]).
- Physical: flagged (c) — the workbook counterpart is the family's outstanding Required input.

---

## 7. Spread, floors, wt

- [FACT] Spread: jump-off rate − Prime, constant (p. 180); assumption (4) constancy applies. Spot-only — no history requirement (framework §5.1 [INT]).
- [FACT] Floors: the common rule applies (p. 180; common §7.1); no noncore floor statement — **OQ-002 retail leg**; no physical floor observed for this family yet.
- [FACT] wt: the common derivation (p. 183) — **OQ-001 retail leg**; live only for whatever part of the family lands on the fixed engine (OQ-041); no noncore wt source observed yet.

---

## 8. Fact-of-absence register (other consumer)

| # | Absent for Other Consumer | Contrast / nearest statement |
|---|---|---|
| 1 | **No interest-rate data in the retail schedule** — the family's defining condition | p. 179–180; p. 185 ("no interest rate information for most non-core retails products", SQ-24) |
| 2 | **No engine statement** | OQ-041 (§5) |
| 3 | **No business-line mapping** for the jump-off rates | OQ-011 (§6) |
| 4 | **No product-type list closure, no definitions** ("such as"; "not limited to") | §3 |
| 5 | **No segmentation grid of any kind** | §4 — unique among the four families |
| 6 | **No Board question names the family** | A154/A157/A158/A160 generic only |
| 7 | **No noncore floor, wt, or classification statement** | §7 |

---

## 9. Inheritance register — what Other Consumer does not restate

| Rule | Governed by | Family-specific note |
|---|---|---|
| Eq A32 income identity; 9 quarters | common §7.0 | Grain = product types (§4 [INT]) |
| Balance construction; flat balances | common §6 | M.1 noncore wiring [PID-LOAN-26]; row set flagged (a) |
| Eq A33 variable path | common §7.3 | The p. 180 mechanics have its shape; engine split = OQ-041 |
| Eqs A34–A38 fixed machinery; Eq A36 | common §7.6; framework §7 | Live only per OQ-041's resolution; A36's meaning without rate data is part of the gap |
| Base rate = Prime (retail rule) | framework §5 | Stated directly for the family's spread (p. 180) and by the p. 185 rule |
| Interest-rate floors | common §7.1; framework §8 | OQ-002 retail leg |
| Industry-scalar mechanism; Table A8 values | common §8; framework §10 | §10 — the Noncore row |
| Assumptions (1)–(7); general limitations | common §12 | No family-specific assumption list |
| Retail Portfolio limitations | framework §12 | The ¶2 non-core sentences are this family's data charter (SQ-24 there) |
| Quarterly compounding versus D-004 | common §7.7 | Unresolved at project level |
| Hedge exclusion (Question A159) | common §11 | OQ-005 |

---

## 10. Table A8 row touching Other Consumer

[FACT] **"Noncore" = 1.072** (PDF p. 220); footnote 63's "one category for rest of consumer loans" (PDF p. 184 footer). **OQ-010 retail leg:** the Noncore-row ↔ rest-of-consumer ↔ this-family identification is three-way inference (§2.3); the Board states no correspondence. Note the boundary interaction: footnote 63 files "small and median business loans and card" with the merged C&I row (1.033) — if the workbook's noncore bucket carries the domestic small-business balances (as the M.1 wiring indicates), the small-business slice sits under one of THREE candidate rows (Noncore 1.072; the merged 1.033; or wherever the results blocks put it). Candidate PID at the gate; [CODE] config map, unmapped hard error.

---

## 11. Coding considerations — [CODE], non-normative

- **Product-type register as configuration:** the family's member list (M.1 rows + the international roll-up) is data, with per-member business-line mapping (OQ-011) and engine assignment (OQ-041) as config fields that **refuse to run while unconfirmed** — the family has the most unresolved structure of the four, so nothing may default.
- **Balance side:** noncore = role-labeled dom rows + the international side of every retail row, per side E/G + I/K [PID-LOAN-26]; unlabeled rows excluded-and-censused (flagged (a)); reconciliation monitor vs the "other consumer" flag column.
- **Rate side as a supplied launch-point input** (the deposit-family Spread(i,b) precedent): one rate per product type (or one bucket — flagged (b)), source = the PPNR line-item report counterpart (flagged (c)); derivation stays upstream data preparation, the model consumes rates.
- **Engine switch per product type** pending OQ-041; if any member lands fixed, its wt and A36 constructions are new elicitation items (§7).

---

## 12. Open questions

| ID | Status | Relevance to this brief |
|---|---|---|
| **OQ-011** | OPEN — this family's central gap | Business-line mapping for jump-off rates; schedule identity of the "line-item report" (§6) |
| **OQ-041** | OPEN — owned here (framework-filed 2026-08-12) | Engine assignment; candidate product-type-level reconciliation recorded [INT] (§5) |
| **OQ-001** | OPEN for retail | wt, if any member runs fixed (§7) |
| **OQ-002** | OPEN for retail | Floors; nothing observed (§7) |
| **OQ-010** | OPEN for retail | Noncore 1.072 identification + the small-business three-way row question (§10) |
| **OQ-033** | OPEN | Firm dimension — the family's rate is stated firm-level (§6), the one place retail matches the subscript abbreviation |
| OQ-040 / OQ-042 / OQ-043 / OQ-012 | OPEN — other-family-owned | Boundaries only |

---

## 13. Source traceability table

| # | Claim / element | Class | PDF p. | md anchor | Verification |
|---|---|---|---|---|---|
| 1 | Fourth-section census ("such as …") | FACT | 177 | sec-156 | Page image 2026-08-12 |
| 2 | Non-core no-further-segmentation sentence | FACT | 177 | sec-156 | Page image 2026-08-12 |
| 3 | Heterogeneous census incl. all internationals + non-purpose lending ("heterogenous" as printed) | FACT | 179–180 | sec-160 | Page images 2026-08-12 |
| 4 | No segmentation; aggregate product-type jump-off rates; PPNR line-item report; most-closely-aligned business line | FACT | 180 | sec-160 | Page image 2026-08-12; OQ-011 |
| 5 | Spread = jump-off rate − Prime, constant; "conservative and supportable" | FACT | 180 | sec-160 | Page image 2026-08-12 |
| 6 | Expert-judgment fixed/variable split of non-core | FACT | 181 | sec-164 | Page image 2026-07-30; OQ-041 |
| 7 | "most non-core loans" in the prevalence entry | FACT | 183 | sec-165 | Page image 2026-07-30; OQ-041 |
| 8 | Retail-limitation non-core sentences | FACT (SQ-24) | 185 | sec-170 | Page image at high zoom 2026-08-12 |
| 9 | Table A8 "Noncore" 1.072; footnote 63 "rest of consumer" | FACT | 220, 184 | sec-209, md 5354 | Page images 2026-07-16 / 2026-08-03; OQ-010 |
| 10 | "non-purpose lending" (retail) vs NPML (wholesale) — two contexts, relationship unstated | FACT | 180 vs 176 | sec-160 vs sec-154 | Page images 2026-08-12 / 2026-08-03 |
| 11 | PID-LOAN-26 noncore wiring; rate-side input outstanding | **PID** / project record | — | — | User-supplied 2026-08-12; flagged (a)–(c) await the gate |

---

### Brief completion checklist

- [x] Status banner present; no adoption language anywhere.
- [x] Every material statement labeled; the engine reconciliation carried as [INT] with its basis; unknowns UNKNOWN, never defaulted.
- [x] **Zero verbatim equation blocks** (D-010(b)).
- [x] Both other-consumer paragraphs verified against page images (2026-08-12).
- [x] The missing rate-side input named as the family's outstanding Required item (§0.1 (c)) — the spec stage is blocked on it, the brief is not.
- [x] Retail-shared rules cited from the framework brief; the SME-cards and NPML boundaries recorded with physical resolutions labeled PID, never source-attributed.
- [x] No production Python; no confidential values, formulas, or firm data — logical contract only.
- [ ] Review state: DRAFT — awaiting user review gate (combined retail gate).

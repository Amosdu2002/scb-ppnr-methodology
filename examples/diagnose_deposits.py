"""Deposit-model debugger — prints every intermediate needed to localize a mismatch
between this implementation and a reference implementation.

    PYTHONPATH=src python3 examples/diagnose_deposits.py \
        --config config/local/company.toml --scenario severely_adverse

Defaults to the synthetic demo config. How to read the output (the decision tree):

1. INPUTS AS PARSED — confirm each value is what you meant (canonical units:
   decimal rates, USD millions). A wrong scale/sign/mapping shows up here first.
2. PER-SUBCOMPONENT tables — compare our per-product rates with the reference's.
   Wrong at PQ1 with a MATCHing hand check  => input pairing (seed/beta mapping).
   Hand check MISMATCH                      => report it; that would be an engine bug.
   Diverges only in ELB / floor-bound rows  => spread or First-ELB/floor convention.
3. EXPENSE, TWO WAYS — 'ours' uses the expense multiplicand (for other-domestic:
   total_average_balance, PID-ODD-2); 'alt' uses the A47 weight-balance sum, which
   is what a reference computing sum(rate_i x balance_i) effectively uses.
   Reference matches 'alt' but not 'ours'   => the multiplicand design is the cause.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from scb_ppnr.ingestion import load_config, load_family_inputs, load_mev_scenario
from scb_ppnr.interest_expense import (
    TABLE_A7_FOREIGN,
    TABLE_A7_OTHER_DOM,
    project_foreign_dep,
    project_other_dom_dep,
)
from scb_ppnr.interest_expense.schemas import PROJECTION_QUARTERS

ALL_QUARTERS = (0, *PROJECTION_QUARTERS)


def show_scenario(scenario, threshold: float) -> None:
    t3m = scenario.usd_3m_treasury
    print("3M Treasury path (decimal, PQ0 = launch point):")
    print("  quarter:" + "".join(f"  PQ{q}".rjust(11) for q in ALL_QUARTERS))
    print("  level  :" + "".join(f"{t3m[q]:11.5f}" for q in ALL_QUARTERS))
    print("  delta  :" + " " * 11 + "".join(f"{t3m[q] - t3m[q - 1]:+11.5f}" for q in PROJECTION_QUARTERS))
    regimes = "".join(("ELB" if t3m[q] < threshold else "non").rjust(11) for q in PROJECTION_QUARTERS)
    print("  regime :" + " " * 11 + regimes + f"   (ELB threshold {threshold})")


def hand_check_pq1(name, sub, diag_pq1, scenario, params) -> str:
    t3m0, t3m1 = scenario.usd_3m_treasury[0], scenario.usd_3m_treasury[1]
    delta = t3m1 - t3m0
    if diag_pq1.regime == "elb":
        expected = t3m1 + sub.elb_spread
        formula = f"A45: t3m {t3m1:+.6f} + spread {sub.elb_spread:+.6f}"
    else:
        beta = params.beta_up[name] if delta > 0 else (params.beta_down[name] if delta < 0 else 0.0)
        unfloored = sub.rate_launchpoint + beta * delta
        expected = max(unfloored, diag_pq1.assumed_floor)
        formula = (
            f"A46: max(seed {sub.rate_launchpoint:+.6f} + beta {beta:.3f} x dT3m {delta:+.6f}, "
            f"floor {diag_pq1.assumed_floor:+.6f})"
        )
    verdict = "MATCH" if abs(expected - diag_pq1.rate) < 1e-12 else "MISMATCH <-- report this"
    return f"    PQ1 hand check  {formula} = {expected:+.6f} | engine {diag_pq1.rate:+.6f} | {verdict}"


def diagnose_model(title, result, subcomponents, params, multiplicand, multiplicand_label, scenario) -> None:
    weight_sum = sum(sub.balance for sub in subcomponents.values())
    first_elb = result.quarters[0].diagnostics.first_elb_treasury3m

    print("\n" + "=" * 78)
    print(f"{title}")
    print("=" * 78)
    print("INPUTS AS PARSED (canonical units: decimal rates / USD millions):")
    print("  subcomponent        seed_rate   weight_bal   elb_spread   beta_up  beta_down")
    for name, sub in subcomponents.items():
        print(
            f"  {name:<18} {sub.rate_launchpoint:+10.6f} {sub.balance:12.3f} "
            f"{sub.elb_spread:+12.6f} {params.beta_up[name]:9.3f} {params.beta_down[name]:10.3f}"
        )
    print(f"  expense multiplicand ({multiplicand_label}): {multiplicand:.3f}")
    print(f"  sum of A47 weight balances:                  {weight_sum:.3f}")
    if weight_sum:
        print(f"  multiplicand / weight-sum ratio:             {multiplicand / weight_sum:.6f}")
    print(f"  First-ELB Treasury3m (shared, scenario-derived): {first_elb:+.6f}")

    print("\nPER-SUBCOMPONENT DIAGNOSTICS (rates decimal; FLOOR marks a binding floor):")
    for name, sub in subcomponents.items():
        print(f"  {name}  (beta_up {params.beta_up[name]:.3f} / beta_down {params.beta_down[name]:.3f}, "
              f"spread {sub.elb_spread:+.6f}, floor {first_elb + sub.elb_spread:+.6f})")
        print("    quarter   regime      dT3m     beta   unfloored      floor   bind       RATE")
        for row in result.quarters:
            s = row.diagnostics.subcomponents[name]
            dt3m = f"{s.market_rate_change:+9.5f}" if s.market_rate_change is not None else "      n/a"
            beta = f"{s.beta_applied:8.3f}" if s.beta_applied is not None else "     n/a"
            unfloored = f"{s.unfloored_rate:+10.6f}" if s.unfloored_rate is not None else "       n/a"
            bind = "FLOOR" if s.floor_binding else "    ."
            print(
                f"    PQ{row.quarter}      {s.regime:>7} {dt3m} {beta} {unfloored} "
                f"{s.assumed_floor:+10.6f}  {bind} {s.rate:+10.6f}"
            )
        print(hand_check_pq1(name, sub, result.quarters[0].diagnostics.subcomponents[name], scenario, params))

    print("\nAGGREGATE RATE AND EXPENSE, TWO WAYS (USD millions per quarter):")
    print("    quarter    agg_rate    ours = rate x multiplicand/4    alt = rate x weight_sum/4")
    alt_total = 0.0
    for row in result.quarters:
        alt = row.annualized_rate * weight_sum / 4.0
        alt_total += alt
        print(f"    PQ{row.quarter}      {row.annualized_rate:+10.6f} {row.quarterly_expense:20.4f} {alt:25.4f}")
    print(f"    cumulative           {result.cumulative_expense:20.4f} {alt_total:25.4f}")
    print("    -> reference matches 'alt' but not 'ours'  => multiplicand design is the cause")
    print("    -> reference matches neither: check the per-subcomponent rate rows above first")

    if result.warnings:
        print("\nLOGGED EVENTS:")
        for warning in result.warnings:
            print(f"  - {warning}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default=Path(__file__).parent / "synthetic_config.toml")
    parser.add_argument("--scenario", default=None)
    parser.add_argument("--model", choices=("other_dom", "foreign", "both"), default="both")
    args = parser.parse_args()

    config = load_config(args.config)
    scenario_id = args.scenario or next(iter(config.mev.scenarios))
    scenario = load_mev_scenario(config, scenario_id).interest_expense_scenario_paths()
    family = load_family_inputs(config)

    print(f"firm={family.firm_id}  scenario={scenario.scenario_id}")
    show_scenario(scenario, TABLE_A7_OTHER_DOM.elb_threshold)

    if args.model in ("other_dom", "both"):
        inputs = family.other_dom_dep
        result = project_other_dom_dep(inputs, scenario)
        diagnose_model(
            "ie_other_dom_dep (Eqs A45-A47; Table A7 other-domestic medians)",
            result, inputs.subcomponents, TABLE_A7_OTHER_DOM,
            inputs.total_average_balance, "total_average_balance, PID-ODD-2", scenario,
        )
    if args.model in ("foreign", "both"):
        inputs = family.foreign_dep
        result = project_foreign_dep(inputs, scenario)
        multiplicand = sum(sub.balance for sub in inputs.subcomponents.values())
        diagnose_model(
            "ie_foreign_dep (A45-A47 by reference; Table A7 foreign medians)",
            result, inputs.subcomponents, TABLE_A7_FOREIGN,
            multiplicand, "sum of 35A+35B — same as weights", scenario,
        )


if __name__ == "__main__":
    main()

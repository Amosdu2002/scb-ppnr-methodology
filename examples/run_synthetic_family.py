"""Run the five interest-expense models on synthetic canonical inputs.

Usage from the repository root (no installation required):

    PYTHONPATH=src python3 examples/run_synthetic_family.py

Every number below is synthetic and hand-picked; nothing is firm data. The FRB
total-interest-expense path is the project-supplied PID-OB-5 calibration target
(physical source OQ-023 — here simply a flat 40 USD per quarter)."""

from __future__ import annotations

from scb_ppnr.interest_expense import (
    MODEL_EXECUTION_ORDER,
    DepositSubcomponent,
    DomTimeDepInputs,
    FamilyInputs,
    FedFundsRepoInputs,
    ForeignDepInputs,
    OtherBorrowingInputs,
    OtherDomDepInputs,
    ScenarioPaths,
    run_interest_expense_family,
)

QUARTERS = range(1, 10)


def build_scenario() -> ScenarioPaths:
    return ScenarioPaths(
        scenario_id="synthetic_severely_adverse",
        usd_3m_treasury={0: 0.0440, 1: 0.0180, 2: 0.001, 3: 0.001, 4: 0.001,
                         5: 0.001, 6: 0.001, 7: 0.001, 8: 0.001, 9: 0.001},
        usd_1y_treasury={1: 0.015, 2: 0.001, 3: 0.001, 4: 0.002,
                         5: 0.002, 6: 0.002, 7: 0.002, 8: 0.002, 9: 0.003},
        bbb_corporate_yield={0: 0.054, 1: 0.052, 2: 0.057, 3: 0.06, 4: 0.06,
                         5: 0.06, 6: 0.058, 7: 0.055, 8: 0.052, 9: 0.048},
    )


def build_family(firm_id: str = "SYNTHETIC_FIRM") -> FamilyInputs:
    return FamilyInputs(
        firm_id=firm_id,
        dom_time_dep=DomTimeDepInputs(firm_id, rate_launchpoint=0.0200, wal_months=3.0, balance=1000.0),
        other_dom_dep=OtherDomDepInputs(
            firm_id,
            subcomponents={
                "mma": DepositSubcomponent(rate_launchpoint=0.0100, balance=600.0, elb_spread=0.0010),
                "savings": DepositSubcomponent(rate_launchpoint=0.0050, balance=300.0, elb_spread=0.0010),
                "transaction": DepositSubcomponent(rate_launchpoint=0.0020, balance=100.0, elb_spread=0.0010),
            },
            total_average_balance=1050.0,
        ),
        foreign_dep=ForeignDepInputs(
            firm_id,
            subcomponents={
                "foreign_nontime": DepositSubcomponent(rate_launchpoint=0.0080, balance=500.0, elb_spread=0.0004),
                "foreign_time": DepositSubcomponent(rate_launchpoint=0.0120, balance=500.0, elb_spread=0.0006),
            },
        ),
        fed_funds_repo=FedFundsRepoInputs(firm_id, fed_funds_purchased_balance=600.0, repo_sold_balance=400.0),
        other_borrowing=OtherBorrowingInputs(firm_id, total_balance=1000.0, cp_share=0.10, subdebt_share=0.20),
        frb_total_interest_expense={q: 40.0 for q in QUARTERS},
    )


def main() -> None:
    scenario = build_scenario()
    family = build_family()
    out = run_interest_expense_family(family, scenario)

    print(f"firm={out.firm_id}  scenario={out.scenario_id}")
    print(f"\nQuarterly expense paths (USD per quarter, pre-hedge):")
    header = "model".ljust(22) + "".join(f"PQ{q}".rjust(9) for q in QUARTERS) + "     total".rjust(11)
    print(header)
    for model_id in MODEL_EXECUTION_ORDER:
        result = out.results[model_id]
        path = result.expense_path()
        row = model_id.ljust(22) + "".join(f"{path[q]:9.3f}" for q in QUARTERS)
        print(row + f"{result.cumulative_expense:11.3f}")
    frb = family.frb_total_interest_expense
    print("frb_total (target)".ljust(22) + "".join(f"{frb[q]:9.3f}" for q in QUARTERS)
          + f"{sum(frb.values()):11.3f}")

    cal = out.calibration
    print(f"\nOther Borrowing calibration (PID-OB-5):")
    print(f"  alpha_b                    = {cal.alpha_b:.6f} (annualized decimal, constant PQ1..PQ9)")
    print(f"  nine-quarter implied total = {cal.cumulative_implied:.6f}")
    print(f"  nine-quarter modeled total = {cal.cumulative_modeled:.6f}")
    print(f"  cumulative difference      = {cal.cumulative_difference:.3e}")
    print(f"  quarterly modeled-vs-implied differences (diagnostic, need not be zero):")
    print("    " + "  ".join(f"PQ{q}:{cal.quarterly_difference_path[q]:+.3f}" for q in QUARTERS))

    rec = out.reconciliation
    print(f"\nFamily reconciliation: five-component total {rec.components_total_cumulative:.6f} "
          f"vs FRB total {rec.frb_total_cumulative:.6f} "
          f"(difference {rec.cumulative_difference:.3e}, within tolerance: {rec.within_tolerance})")
    if out.warnings:
        print("\nLogged events (log, never clamp):")
        for warning in out.warnings:
            print(f"  - {warning}")
    else:
        print("\nNo logged edge events.")


if __name__ == "__main__":
    main()

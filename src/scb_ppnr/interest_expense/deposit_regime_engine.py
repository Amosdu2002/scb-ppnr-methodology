"""Shared Equations A45–A47 engine for the two deposit-beta models.

`ie_foreign_dep` reuses `ie_other_dom_dep`'s A45–A47 framework by reference
(Fed-stated; ODD spec `downstream_by_reference`), so exactly those two models share
this code path — it is never reused for A44, A48, or A53 (conventions §8).

Per projection quarter t, classified on Treasury3m(t) against the 25 bp threshold:
- ELB (below threshold), Eq A45:      Rate(i,b,t) = Treasury3m(t) + Spread(i,b)
  — an equality, not a floor; sub-floor and negative rates are legal (logged).
- non-ELB (above threshold), Eq A46:  Rate(i,b,t) = max(Rate(i,b,t-1) + δ(i,t), assumed_floor(i,b))
  with δ(i,t) = max(ΔT3m,0)·β_up(i) + min(ΔT3m,0)·β_down(i)   (no firm subscript)
  and  assumed_floor(i,b) = First_ELB_Treasury3m + Spread(i,b).
- Treasury3m == threshold is unassigned in the source (OQ-013); the documented
  working branch is non-ELB, and each hit is logged.
Eq A47 aggregates: Rate(b,t) = Σ_i Rate(i,b,t)·Balance(i,b) / Σ_i Balance(i,b).

Seeds (OQ-018): Rate(i,b,0) = the launch-point rate items; ΔT3m at t=1 uses the
PQ0 scenario value. The recursion lag is the previous modeled rate regardless of
the prior quarter's regime. First_ELB_Treasury3m is the first sub-threshold
observation of the supplied scenario path scanned in quarter order PQ0→PQ9, else
the threshold itself [CODE choice: PQ0 is scanned as part of the supplied series].
"""

from __future__ import annotations

from typing import Mapping

from .schemas import (
    PROJECTION_QUARTERS,
    SCENARIO_QUARTERS_WITH_LAUNCH,
    DepositBetaParams,
    DepositQuarterDiagnostics,
    DepositSubcomponent,
    DepositSubcomponentDiagnostics,
    ScenarioPaths,
    ValidationFailure,
)

REGIME_ELB = "elb"
REGIME_NON_ELB = "non_elb"


def first_elb_treasury3m(scenario: ScenarioPaths, threshold: float) -> float:
    """min(threshold, first sub-threshold observation of the scenario Treasury3m
    path in quarter order); the threshold itself if the path never goes below it."""
    for quarter in SCENARIO_QUARTERS_WITH_LAUNCH:
        value = scenario.usd_3m_treasury[quarter]
        if value < threshold:
            return value
    return threshold


def project_deposit_rates(
    subcomponents: Mapping[str, DepositSubcomponent],
    scenario: ScenarioPaths,
    params: DepositBetaParams,
) -> tuple[list[DepositQuarterDiagnostics], list[str]]:
    """Run A45–A47 for PQ1..PQ9. Returns one DepositQuarterDiagnostics per quarter
    (in order) carrying every subcomponent intermediate plus the A47 aggregate rate,
    and the list of logged edge events (log, never clamp)."""
    if set(subcomponents.keys()) != set(params.beta_up.keys()):
        raise ValidationFailure(
            f"subcomponents {sorted(subcomponents.keys())} do not match the parameter set "
            f"{sorted(params.beta_up.keys())}"
        )
    total_weight = sum(sub.balance for sub in subcomponents.values())
    if total_weight <= 0.0:
        raise ValidationFailure("Eq A47 aggregation weights sum to zero — no divisible balance")

    warnings: list[str] = []
    for name, sub in subcomponents.items():
        if sub.elb_spread < 0.0:
            warnings.append(f"{name}: negative elb_spread {sub.elb_spread} (legal; logged)")

    first_elb = first_elb_treasury3m(scenario, params.elb_threshold)
    previous_rate = {name: sub.rate_launchpoint for name, sub in subcomponents.items()}
    rows: list[DepositQuarterDiagnostics] = []

    for quarter in PROJECTION_QUARTERS:
        t3m = scenario.usd_3m_treasury[quarter]
        if t3m < params.elb_threshold:
            regime = REGIME_ELB
        else:
            regime = REGIME_NON_ELB
            if t3m == params.elb_threshold:
                warnings.append(
                    f"PQ{quarter}: Treasury3m equals the ELB threshold ({params.elb_threshold}) — "
                    f"unassigned in the source (OQ-013); documented working branch non-ELB applied"
                )
        delta_t3m = t3m - scenario.usd_3m_treasury[quarter - 1]

        quarter_diags: dict[str, DepositSubcomponentDiagnostics] = {}
        for name, sub in subcomponents.items():
            assumed_floor = first_elb + sub.elb_spread
            if regime == REGIME_ELB:
                rate = t3m + sub.elb_spread
                if rate < assumed_floor:
                    warnings.append(
                        f"{name} PQ{quarter}: ELB rate {rate} sits below the assumed floor "
                        f"{assumed_floor} (legal under Eq A45; logged)"
                    )
                diag = DepositSubcomponentDiagnostics(
                    regime=regime,
                    beta_applied=None,
                    market_rate_change=None,
                    elb_spread=sub.elb_spread,
                    assumed_floor=assumed_floor,
                    floor_binding=False,
                    unfloored_rate=None,
                    rate=rate,
                    weight_balance=sub.balance,
                )
            else:
                if delta_t3m > 0.0:
                    beta_applied = params.beta_up[name]
                elif delta_t3m < 0.0:
                    beta_applied = params.beta_down[name]
                else:
                    beta_applied = 0.0
                delta_rate = max(delta_t3m, 0.0) * params.beta_up[name] + min(delta_t3m, 0.0) * params.beta_down[name]
                unfloored = previous_rate[name] + delta_rate
                rate = max(unfloored, assumed_floor)
                diag = DepositSubcomponentDiagnostics(
                    regime=regime,
                    beta_applied=beta_applied,
                    market_rate_change=delta_t3m,
                    elb_spread=sub.elb_spread,
                    assumed_floor=assumed_floor,
                    floor_binding=assumed_floor > unfloored,
                    unfloored_rate=unfloored,
                    rate=rate,
                    weight_balance=sub.balance,
                )
            if rate < 0.0:
                warnings.append(f"{name} PQ{quarter}: negative rate {rate} (legal; logged, never clamped)")
            quarter_diags[name] = diag
            previous_rate[name] = rate

        aggregate = sum(d.rate * d.weight_balance for d in quarter_diags.values()) / total_weight
        rows.append(
            DepositQuarterDiagnostics(
                usd_3m_treasury=t3m,
                first_elb_treasury3m=first_elb,
                subcomponents=quarter_diags,
                aggregate_rate=aggregate,
            )
        )
    return rows, warnings

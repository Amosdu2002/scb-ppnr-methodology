"""The four Retail loan family engines (PID-LOAN-26..34).

Each family builds launch-point blocks from the loaders' canonical objects and
projects them on the shared Equation A33 / A38 machinery from
`loans_projection` — the engines are never re-derived per family, only wired:

    Mortgage    per {first lien, home equity, HELOC} x {HFI, FVO/HFS} block:
                a fixed leg (Eq A38 blend; new-origination spread from the
                query's window column, own-rate fallback) and a variable leg
                (Eq A33 floored at the query's ARM floor). Base = the MORTGAGE
                rate for ALL blocks, HELOC included (PID-LOAN-33 as amended —
                a recorded divergence from the Fed's HELOC-on-Prime register);
                the HELOC spread may anchor at Prime's terminal level
                (heloc_spread_anchor, round-2 arithmetic identification).
    Auto        all-fixed (Eq A33 never runs): spread = the pivot's
                new-origination rate minus Prime PQ0; the re-origination
                weights are SUPPLIED (PID-LOAN-29 as amended).
    Card        all-variable on Prime + the REPORTED FR Y-14M spread; income
                accrues on the REVOLVING balance = M.1 block balance x the
                query-OS share x the revolver share (PID-LOAN-28/34).
    Other       all-variable at product-type grain: jump-off rates from the
    consumer    PPNR line-item sheet's PQ0 column via the observed line
                mapping; balances = M.1 blocks shared by the A.7/A.9
                sub-product balances, or M.1 rows directly (PID-LOAN-30).

Block totals apply the PID-LOAN-32 scalar map: Mortgage 1.014, consumer card
0.969, SME cards AND small-business loans 1.033, Noncore 1.072, and Auto the
PUBLISHED 0.865 by user direction — the reference workbook's own auto panel
applies 0.948, so reference-matching runs set retail_auto_scalar = "0.948".

The Federal Reserve model is PROPOSED for the 2026 stress test, NOT adopted.
Divergences from the source are recorded in
`docs/specifications/interest-income/loans/ii_loans_retail.spec.md`."""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Mapping, Sequence

from ..core.schemas import ValidationFailure, check_rate
from ..ingestion.retail_loader import (
    AutoSummary,
    CardSegment,
    M1RetailRow,
    MortgageQuery,
    OcProductRow,
)
from .common import quarterly_income
from .loans_projection import project_fixed_rate, project_variable_rate

# --- The PID-LOAN-32 scalar map (Table A8 values; auto is config-supplied) ---
SCALAR_MORTGAGE = 1.014
SCALAR_CARD_CONSUMER = 0.969
SCALAR_CARD_SME = 1.033          # the merged "C&I, noncore SME loan and card" row
SCALAR_NONCORE = 1.072
SCALAR_SMALL_BUSINESS = 1.033    # domestic small-business LOANS take the merged row too

FAMILY_MORTGAGE = "mortgage"
FAMILY_AUTO = "auto"
FAMILY_CARD = "card"
FAMILY_OTHER_CONSUMER = "other_consumer"


@dataclass(frozen=True)
class RetailStream:
    """One projected stream (a fixed or variable leg, or one product row)."""

    name: str
    engine: str                              # "fixed" | "variable" | "none"
    balance: float                           # USD millions
    launch_rate: float | None
    spread: float | None
    rate_path: Mapping[int, float] | None
    income_path: Mapping[int, float]         # UNSCALED, USD millions per quarter
    floor_binds: tuple[int, ...] = ()

    @property
    def total_income(self) -> float:
        return sum(self.income_path.values())


@dataclass(frozen=True)
class RetailBlock:
    """One scalar-carrying block: streams sum, then the Table A8 scalar applies
    to the block total every quarter (the PID-LOAN-16 semantics)."""

    family: str
    name: str
    scalar: float
    streams: tuple[RetailStream, ...]

    def unscaled_path(self, quarters: Sequence[int]) -> Mapping[int, float]:
        return MappingProxyType(
            {q: sum(s.income_path[q] for s in self.streams) for q in quarters}
        )

    def total_path(self, quarters: Sequence[int]) -> Mapping[int, float]:
        return MappingProxyType(
            {q: sum(s.income_path[q] for s in self.streams) * self.scalar for q in quarters}
        )


@dataclass
class RetailDiagnostics:
    notes: list[str] = field(default_factory=list)
    floor_binds: int = 0
    fallbacks: int = 0

    def render(self, title: str) -> str:
        lines = [title]
        lines.append(f"  floor binds (segment-quarters): {self.floor_binds}")
        lines.append(f"  new-origination fallbacks     : {self.fallbacks}")
        for note in self.notes:
            lines.append(f"  NOTE: {note}")
        return "\n".join(lines)


def _reconciliation_note(diagnostics: RetailDiagnostics, what: str,
                         ours: float, m1: float) -> None:
    """A consistency monitor, never an identity: different physical sources may
    legitimately differ (the sheet's own pivot-vs-M.1 cell is the precedent)."""
    if m1 <= 0.0:
        diagnostics.notes.append(f"{what}: M.1 balance is zero — nothing to reconcile against")
        return
    diagnostics.notes.append(f"{what}: source/M.1 = {ours / m1:.6f} ({ours:,.2f}mm vs {m1:,.2f}mm)")


# --- Mortgage (PID-LOAN-27/33) ----------------------------------------------

_MORTGAGE_BASE_BY_PRODUCT = MappingProxyType({
    "first_lien": "mortgage_rate",
    "home_equity": "mortgage_rate",     # PID-LOAN-33: the p. 185 exception covers home equity
    "heloc": "mortgage_rate",           # PID-LOAN-33 as amended (round 1, user-stated): the
                                        # workbook prices HELOC on the MORTGAGE rate too, with
                                        # the query ARM floor — a RECORDED DIVERGENCE from the
                                        # Fed's base-rate register, which puts HELOC on Prime
                                        # (PDF p. 181); the engine follows the workbook
})


def build_mortgage(
    query: MortgageQuery,
    m1: Mapping[str, M1RetailRow],
    base_paths: Mapping[str, Mapping[int, float]],
    base_launch: Mapping[str, float],
    quarters: Sequence[int],
    diagnostics: RetailDiagnostics,
    heloc_spread_anchor: str = "mortgage_launch",
) -> tuple[RetailBlock, ...]:
    """Six blocks: {first lien, home equity, HELOC} x {HFI, FVO/HFS}.

    Block balance = the M.1 sub-family row sum of ITS side (first lien row;
    the two HELOAN rows; the HELOCs row), allocated to the fixed and variable
    legs by the query's UPB shares (PID-LOAN-26/27, arithmetic-verified)."""
    m1_by_block: dict[tuple[str, str], float] = {}
    for side, attr in (("HFI", "dom_hfi"), ("FVO_HFS", "dom_hfs")):
        m1_by_block[("first_lien", side)] = getattr(m1["first_mortgages"], attr)
        m1_by_block[("home_equity", side)] = (
            getattr(m1["first_lien_heloans"], attr) + getattr(m1["junior_lien_heloans"], attr)
        )
        m1_by_block[("heloc", side)] = getattr(m1["helocs"], attr)

    blocks: list[RetailBlock] = []
    for (product, side), m1_balance in sorted(m1_by_block.items()):
        base_name = _MORTGAGE_BASE_BY_PRODUCT[product]
        base_path = base_paths[base_name]
        launch_base = base_launch[base_name]
        # HELOC spreads may anchor away from the projection base (round-2
        # arithmetic identification: WAR minus Prime's terminal level, not the
        # launch mortgage rate, reproduces the reference HELOC exactly; the
        # projection path stays the mortgage rate either way).
        spread_anchor = launch_base
        if product == "heloc":
            if heloc_spread_anchor == "mortgage_launch":
                spread_anchor = launch_base
            elif heloc_spread_anchor == "prime_launch":
                spread_anchor = base_launch["prime_rate"]
            elif heloc_spread_anchor == "prime_pq9":
                spread_anchor = base_paths["prime_rate"][max(quarters)]
            else:
                raise ValidationFailure(
                    f"heloc_spread_anchor must be 'mortgage_launch', 'prime_launch', or "
                    f"'prime_pq9', got {heloc_spread_anchor!r}"
                )
            if heloc_spread_anchor != "mortgage_launch":
                diagnostics.notes.append(
                    f"heloc/{side}: spreads anchored at {heloc_spread_anchor} = "
                    f"{spread_anchor:.4%} (projection base stays the mortgage rate)"
                )
        segments = {
            rate_type: query.segments.get((product, side, rate_type))
            for rate_type in ("fixed", "variable")
        }
        upb_total = sum(s.upb for s in segments.values() if s is not None)
        if upb_total <= 0.0:
            if m1_balance > 0.0:
                diagnostics.notes.append(
                    f"mortgage {product}/{side}: M.1 carries {m1_balance:,.2f}mm but the query "
                    f"has no UPB — the block projects nothing; check the query sheet"
                )
            continue
        _reconciliation_note(
            diagnostics, f"mortgage {product}/{side} query-UPB vs M.1", upb_total, m1_balance
        )

        streams: list[RetailStream] = []
        for rate_type, segment in segments.items():
            if segment is None or segment.upb <= 0.0:
                continue
            share = segment.upb / upb_total
            balance = m1_balance * share
            if rate_type == "fixed":
                schedule = query.schedules.get((product, side, "fixed"), {})
                weights = {}
                for q in quarters:
                    wt = schedule.get(q, 0.0) / segment.upb if segment.upb > 0.0 else 0.0
                    if wt > 1.0:
                        raise ValidationFailure(
                            f"mortgage {product}/{side} fixed: wt(PQ{q}) = {wt:.4f} exceeds 1 — "
                            f"the maturing balance is larger than the segment (Equation A38 is "
                            f"non-convex beyond 1); check the schedule block"
                        )
                    weights[q] = wt
                new_orig = segment.new_origination_rate
                if new_orig is None:
                    raise ValidationFailure(
                        f"mortgage {product}/{side} fixed: no new-origination rate and no "
                        f"fallback — the loader should have applied the PID-LOAN-33 own-rate rule"
                    )
                if segment.new_origination_fallback:
                    diagnostics.fallbacks += 1
                spread = new_orig - spread_anchor
                check_rate(f"mortgage {product}/{side} fixed spread", spread)
                rates, _, binds = project_fixed_rate(
                    segment.rate, spread, base_path, weights, None, quarters
                )
            else:
                spread = segment.rate - spread_anchor
                check_rate(f"mortgage {product}/{side} variable spread", spread)
                rates, _, binds = project_variable_rate(
                    spread, base_path, segment.arm_floor, quarters
                )
            diagnostics.floor_binds += len(binds)
            streams.append(RetailStream(
                name=rate_type,
                engine=rate_type,
                balance=balance,
                launch_rate=segment.rate,
                spread=spread,
                rate_path=rates,
                income_path=MappingProxyType(
                    {q: quarterly_income(balance, rates[q]) for q in quarters}
                ),
                floor_binds=binds,
            ))
        if streams:
            blocks.append(RetailBlock(
                family=FAMILY_MORTGAGE,
                name=f"{product}/{side}",
                scalar=SCALAR_MORTGAGE,
                streams=tuple(streams),
            ))
    if not blocks:
        raise ValidationFailure("mortgage: no blocks produced — query and M.1 disagree entirely")
    return tuple(blocks)


# --- Auto (PID-LOAN-29/32) ---------------------------------------------------


def build_auto(
    summary: AutoSummary,
    m1: Mapping[str, M1RetailRow],
    prime_path: Mapping[int, float],
    prime_launch: float,
    auto_scalar: float,
    quarters: Sequence[int],
    diagnostics: RetailDiagnostics,
) -> RetailBlock:
    """One block, two fixed segments (New / Used). Eq A33 never runs for auto."""
    m1_balance = m1["auto_loans"].dom_hfi + m1["auto_loans"].dom_hfs
    pivot_total = summary.new_outstanding + summary.used_outstanding
    if pivot_total <= 0.0:
        raise ValidationFailure("auto: the pivot's New + Used outstanding is zero")
    _reconciliation_note(diagnostics, "auto pivot-D_OS vs M.1", pivot_total, m1_balance)

    streams: list[RetailStream] = []
    for name, outstanding, rate, new_orig, weights in (
        ("new_vehicle", summary.new_outstanding, summary.new_rate,
         summary.new_origination_rate_new, summary.weights_new),
        ("used_vehicle", summary.used_outstanding, summary.used_rate,
         summary.new_origination_rate_used, summary.weights_used),
    ):
        share = outstanding / pivot_total
        balance = m1_balance * share
        spread = new_orig - prime_launch
        check_rate(f"auto {name} spread", spread)
        rates, _, binds = project_fixed_rate(rate, spread, prime_path, weights, None, quarters)
        diagnostics.floor_binds += len(binds)
        streams.append(RetailStream(
            name=name, engine="fixed", balance=balance,
            launch_rate=rate, spread=spread, rate_path=rates,
            income_path=MappingProxyType(
                {q: quarterly_income(balance, rates[q]) for q in quarters}
            ),
            floor_binds=binds,
        ))
    return RetailBlock(family=FAMILY_AUTO, name="auto", scalar=auto_scalar, streams=tuple(streams))


# --- Card (PID-LOAN-28/34) ---------------------------------------------------


def _card_spread(segment: CardSegment, mode: str, prime_launch: float) -> float:
    if mode == "reported":
        return segment.spread
    if mode == "reported_revolver":
        return segment.spread_revolver
    if mode == "calculated":
        return segment.apr - prime_launch
    raise ValidationFailure(
        f"card_spread_mode must be 'reported', 'reported_revolver', or 'calculated' "
        f"(PID-LOAN-34), got {mode!r}"
    )


def build_card(
    segments: Mapping[int, CardSegment],
    m1: Mapping[str, M1RetailRow],
    prime_path: Mapping[int, float],
    prime_launch: float,
    spread_mode: str,
    quarters: Sequence[int],
    diagnostics: RetailDiagnostics,
) -> tuple[RetailBlock, ...]:
    """Two blocks (consumer; SME), income on the revolving balance only.

    income(q) = M.1 block balance x OS-share x revolver share x rate(q) / 4,
    rate(q) = max(Prime(q) + reported spread, 0) — the floor-at-zero switch
    setting, PID-LOAN-34 (arithmetic-verified against the workbook panel)."""
    m1_blocks = {
        "consumer": m1["bank_cards"].dom + m1["charge_cards"].dom,
        "sme": m1["sme_cards"].dom,
    }
    scalars = {"consumer": SCALAR_CARD_CONSUMER, "sme": SCALAR_CARD_SME}
    blocks: list[RetailBlock] = []
    for block_name in ("consumer", "sme"):
        members = [s for s in segments.values() if s.block == block_name]
        if not members:
            diagnostics.notes.append(f"card {block_name}: no query rows — block skipped")
            continue
        os_total = sum(s.total_outstanding for s in members)
        m1_balance = m1_blocks[block_name]
        if os_total > 0.0:
            _reconciliation_note(
                diagnostics, f"card {block_name} query-OS vs M.1", os_total, m1_balance
            )
        streams: list[RetailStream] = []
        for segment in sorted(members, key=lambda s: s.row_id):
            share = (segment.total_outstanding / os_total) if os_total > 0.0 else 0.0
            revolving_balance = m1_balance * share * segment.revolver_share
            spread = _card_spread(segment, spread_mode, prime_launch)
            check_rate(f"card {block_name}/{segment.product} spread", spread)
            rates, _, binds = project_variable_rate(spread, prime_path, 0.0, quarters)
            diagnostics.floor_binds += len(binds)
            streams.append(RetailStream(
                name=f"{block_name}_{segment.product}",
                engine="variable",
                balance=revolving_balance,
                launch_rate=segment.apr,
                spread=spread,
                rate_path=rates,
                income_path=MappingProxyType(
                    {q: quarterly_income(revolving_balance, rates[q]) for q in quarters}
                ),
                floor_binds=binds,
            ))
        blocks.append(RetailBlock(
            family=FAMILY_CARD, name=block_name, scalar=scalars[block_name],
            streams=tuple(streams),
        ))
    if not blocks:
        raise ValidationFailure("card: no blocks produced")
    return tuple(blocks)


# --- Other consumer (PID-LOAN-30) --------------------------------------------

# The M.1-direct rows: (stream name, line key). Balances come from the retail
# M.1 rows — the international side of every retail row is noncore, and the
# domestic noncore rows join with both sides (PID-LOAN-26/30). All take the
# Noncore scalar, including international small business (observed).
_OC_SINGLES: tuple[tuple[str, str], ...] = (
    ("intl_auto", "auto"),
    ("intl_credit_card", "credit_cards"),
    ("intl_home_equity_heloc", "helocs"),
    ("intl_first_lien", "first_lien"),
    ("intl_other_consumer", "non_purpose"),
    ("intl_small_business", "ci"),
    ("student_loans", "student"),
    ("non_purpose_lending", "non_purpose"),
)


def _oc_single_balances(m1: Mapping[str, M1RetailRow]) -> Mapping[str, float]:
    return MappingProxyType({
        "intl_auto": m1["auto_loans"].intl,
        "intl_credit_card": (
            m1["bank_cards"].intl + m1["charge_cards"].intl + m1["sme_cards"].intl
        ),
        "intl_home_equity_heloc": (
            m1["first_lien_heloans"].intl + m1["junior_lien_heloans"].intl + m1["helocs"].intl
        ),
        "intl_first_lien": m1["first_mortgages"].intl,
        "intl_other_consumer": m1["other_consumer_loans"].intl,
        "intl_small_business": m1["small_business"].intl,
        "student_loans": m1["student_loans"].total,
        "non_purpose_lending": m1["non_purpose_lending"].total,
    })


def build_other_consumer(
    products: Sequence[OcProductRow],
    line_rates: Mapping[str, float],
    m1: Mapping[str, M1RetailRow],
    prime_path: Mapping[int, float],
    prime_launch: float,
    quarters: Sequence[int],
    diagnostics: RetailDiagnostics,
) -> tuple[RetailBlock, ...]:
    """Every row on the variable path floored at zero (PID-LOAN-30):
    rate(q) = max(Prime(q) + (line PQ0 rate - Prime PQ0), 0)."""

    def stream(name: str, balance: float, line_key: str | None) -> RetailStream:
        if line_key is None:
            # A zero-rate row by construction (Overdraft): no income, ever.
            return RetailStream(
                name=name, engine="none", balance=balance, launch_rate=0.0, spread=None,
                rate_path=None,
                income_path=MappingProxyType({q: 0.0 for q in quarters}),
            )
        rate0 = line_rates[line_key]
        spread = rate0 - prime_launch
        check_rate(f"other-consumer {name} spread", spread)
        rates, _, binds = project_variable_rate(spread, prime_path, 0.0, quarters)
        diagnostics.floor_binds += len(binds)
        return RetailStream(
            name=name, engine="variable", balance=balance, launch_rate=rate0, spread=spread,
            rate_path=rates,
            income_path=MappingProxyType(
                {q: quarterly_income(balance, rates[q]) for q in quarters}
            ),
            floor_binds=binds,
        )

    blocks: list[RetailBlock] = []
    for schedule, block_name, m1_balance, scalar in (
        ("A.7", "us_other_consumer", m1["other_consumer_loans"].dom, SCALAR_NONCORE),
        ("A.9", "us_small_business", m1["small_business"].dom, SCALAR_SMALL_BUSINESS),
    ):
        members = [p for p in products if p.schedule == schedule]
        if not members:
            diagnostics.notes.append(
                f"other-consumer {block_name}: no {schedule} product rows — block skipped"
            )
            continue
        share_total = sum(p.balance for p in members)
        if share_total > 0.0:
            _reconciliation_note(
                diagnostics, f"other-consumer {block_name} {schedule}-balances vs M.1",
                share_total, m1_balance,
            )
        streams = []
        for product in members:
            share = (product.balance / share_total) if share_total > 0.0 else 0.0
            streams.append(stream(product.name, m1_balance * share, product.line_key))
        blocks.append(RetailBlock(
            family=FAMILY_OTHER_CONSUMER, name=block_name, scalar=scalar,
            streams=tuple(streams),
        ))

    balances = _oc_single_balances(m1)
    singles = tuple(
        stream(name, balances[name], line_key)
        for name, line_key in _OC_SINGLES
    )
    blocks.append(RetailBlock(
        family=FAMILY_OTHER_CONSUMER, name="m1_direct", scalar=SCALAR_NONCORE,
        streams=singles,
    ))
    return tuple(blocks)


# --- Rollup ------------------------------------------------------------------


def family_summary(
    blocks: Sequence[RetailBlock], quarters: Sequence[int]
) -> Mapping[str, Mapping[str, float]]:
    """Per-family scaled totals: the 4Q and 9Q cumulative view of the results
    summary (the compare target's shape). PQ1..PQ4 vs PQ1..PQ9 — PQ0 is the
    launch quarter and never counts toward the horizon."""
    out: dict[str, dict[str, float]] = {}
    for block in blocks:
        totals = block.total_path(quarters)
        entry = out.setdefault(block.family, {"cum_4q": 0.0, "cum_9q": 0.0})
        entry["cum_4q"] += sum(totals[q] for q in quarters if q <= 4)
        entry["cum_9q"] += sum(totals[q] for q in quarters)
    return MappingProxyType({family: MappingProxyType(v) for family, v in out.items()})


def parse_auto_scalar(raw: str) -> float:
    """The config carries the auto scalar as text (PID-LOAN-32); parse and bound it."""
    try:
        value = float(str(raw).strip())
    except ValueError as exc:
        raise ValidationFailure(
            f"retail_auto_scalar must be a number, got {raw!r} (PID-LOAN-32: '0.865' published, "
            f"'0.948' reference-matching)"
        ) from exc
    if not 0.5 <= value <= 1.5:
        raise ValidationFailure(
            f"retail_auto_scalar = {value} is outside [0.5, 1.5] — scalars are true-up factors "
            f"near 1, so this looks like a units mistake"
        )
    return value

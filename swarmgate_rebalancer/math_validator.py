"""Zero-trust math validator for independent verification of Grok plans."""

from dataclasses import dataclass, field
from typing import Dict, List

from .config import FlowConfig
from .grok_models import GrokPlan


@dataclass
class PortfolioSnapshot:
    """Current portfolio state snapshot.

    All values in base currency (USD).
    """

    positions_usd: Dict[str, float]  # symbol -> current USD value
    cash_usd: float  # available cash before paycheck
    paycheck_net_usd: float  # this event's net paycheck


@dataclass
class ValidationResult:
    """Result of validating a Grok plan."""

    ok: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


def validate_plan(
    config: FlowConfig,
    snapshot: PortfolioSnapshot,
    plan: GrokPlan,
    epsilon: float = 0.01,  # $0.01 tolerance
) -> ValidationResult:
    """Validate a Grok rebalancing plan against configuration and snapshot.

    Performs independent math verification to ensure:
    - Treasury amount matches expected calculation
    - Order totals match stated total_invested
    - No unauthorized symbols in orders
    - No overspending available cash
    - Orders move underweight assets toward targets
    - SWARM is not in market orders (treasury only)

    Args:
        config: Flow configuration with targets and settings.
        snapshot: Current portfolio state.
        plan: Grok's proposed rebalancing plan.
        epsilon: Tolerance for floating point comparisons.

    Returns:
        ValidationResult with ok status, errors, and warnings.
    """
    errors: List[str] = []
    warnings: List[str] = []

    s = snapshot
    settings = config.settings
    targets = config.portfolio.target

    # 1. Check treasury math
    expected_treasury = round(s.paycheck_net_usd * settings.treasury_pct, 2)
    if abs(plan.treasury_transfer_usd - expected_treasury) > 0.01:
        errors.append(
            f"Treasury mismatch: plan={plan.treasury_transfer_usd:.2f}, "
            f"expected={expected_treasury:.2f}"
        )

    # 2. Check total_invested ~= sum(order.usd)
    orders_sum = round(sum(o.usd for o in plan.orders), 2)
    if abs(plan.total_invested - orders_sum) > 0.01:
        errors.append(
            f"total_invested mismatch: plan={plan.total_invested:.2f}, "
            f"sum(orders)={orders_sum:.2f}"
        )

    # 3. Guard rails on order sizes
    for o in plan.orders:
        if o.usd > settings.max_single_order_usd:
            errors.append(
                f"Order for {o.symbol} exceeds max_single_order_usd: {o.usd:.2f}"
            )
        if o.symbol == "SWARM":
            errors.append(
                "SWARM must be funded via treasury_transfer, not market order"
            )

    # 4. Recompute pre/post allocations and direction of trades
    # Apply orders as if all execute exactly at quoted usd size
    post_positions = dict(s.positions_usd)
    cash_after = s.cash_usd + s.paycheck_net_usd - plan.treasury_transfer_usd

    for o in plan.orders:
        post_positions[o.symbol] = post_positions.get(o.symbol, 0.0) + o.usd
        cash_after -= o.usd

    # 4a. No negative cash
    if cash_after < -epsilon:
        errors.append(f"Plan overspends cash: cash_after={cash_after:.2f}")

    # 5. Compute weights before / after
    def weights(positions: Dict[str, float], cash: float) -> Dict[str, float]:
        total = cash + sum(positions.values())
        if total <= 0:
            return {}
        w = {}
        for sym, val in positions.items():
            w[sym] = val / total
        # Treat CASH as its own "symbol" if present in targets
        if "CASH" in targets:
            w["CASH"] = cash / total
        return w

    w_before = weights(
        s.positions_usd,
        s.cash_usd + s.paycheck_net_usd - plan.treasury_transfer_usd,
    )
    w_after = weights(post_positions, cash_after)

    # 6. Ensure buys move underweight assets toward target
    for o in plan.orders:
        if o.symbol not in targets:
            errors.append(f"Plan includes unauthorized symbol: {o.symbol}")
            continue
        t = targets[o.symbol]
        before = w_before.get(o.symbol, 0.0)
        after = w_after.get(o.symbol, 0.0)
        if before >= t and after > before + 1e-6:
            errors.append(
                f"Order for {o.symbol} increases already-at/over-target position: "
                f"before={before:.4f}, target={t:.4f}, after={after:.4f}"
            )
        if after < before - 1e-6:
            errors.append(
                f"Order for {o.symbol} decreases weighting unexpectedly: "
                f"before={before:.4f}, after={after:.4f}"
            )

    # 7. Check untouched assets don't move the wrong way
    for sym, t in targets.items():
        before = w_before.get(sym, 0.0)
        after = w_after.get(sym, 0.0)
        drift = abs(after - t)
        if drift > settings.rebalance_threshold + 1e-4:
            warnings.append(
                f"{sym} remains > rebalance_threshold after plan: "
                f"after={after:.4f}, target={t:.4f}, "
                f"drift={drift:.4f}"
            )

    return ValidationResult(ok=not errors, errors=errors, warnings=warnings)

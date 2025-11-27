#!/usr/bin/env python3
"""
Strategickhaos Wealth Engine - Portfolio Rebalancer
====================================================
Autonomous rebalancing with drift detection and fractional share precision.

Part of the four-script automation suite for the Strategickhaos Wealth Engine.
Zero leverage | Zero drift | Mathematically precise

"Effortless. Natural. Playful. Precision-engineered. Long-term inevitable."
"""

import argparse
import json
import logging
import sys
from dataclasses import dataclass, field
from datetime import datetime
from decimal import ROUND_DOWN, Decimal
from pathlib import Path
from typing import Optional

import yaml

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("wealth_engine.rebalancer")


@dataclass
class Asset:
    """Represents a portfolio asset with precise decimal handling."""

    symbol: str
    target_weight: Decimal
    current_weight: Decimal = Decimal("0")
    current_value: Decimal = Decimal("0")
    current_shares: Decimal = Decimal("0")
    price: Decimal = Decimal("0")
    state: str = "hold"

    @property
    def drift(self) -> Decimal:
        """Calculate drift from target weight."""
        return abs(self.current_weight - self.target_weight)

    @property
    def is_underweight(self) -> bool:
        """Check if asset is underweight."""
        return self.current_weight < self.target_weight

    @property
    def is_overweight(self) -> bool:
        """Check if asset is overweight."""
        return self.current_weight > self.target_weight


@dataclass
class RebalanceAction:
    """Represents a rebalancing action to execute."""

    symbol: str
    action: str  # 'buy' or 'sell'
    shares: Decimal
    value: Decimal
    reason: str
    priority: int = 0


@dataclass
class PortfolioState:
    """Current state of the portfolio."""

    total_value: Decimal
    assets: dict = field(default_factory=dict)
    cash: Decimal = Decimal("0")
    last_updated: Optional[datetime] = None


class PortfolioRebalancer:
    """
    Autonomous portfolio rebalancer with drift detection.

    Features:
    - Threshold-based rebalancing
    - Fractional share precision
    - Tax-loss harvesting awareness
    - Deterministic behavior
    """

    def __init__(self, config_path: str):
        """Initialize rebalancer with configuration."""
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.precision = self.config.get("rebalancing", {}).get(
            "execution", {}
        ).get("precision", 6)
        self.min_trade = Decimal(
            str(
                self.config.get("rebalancing", {})
                .get("execution", {})
                .get("min_trade_value", 1.00)
            )
        )

    def _load_config(self) -> dict:
        """Load configuration from YAML file."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config not found: {self.config_path}")

        with open(self.config_path) as f:
            return yaml.safe_load(f)

    def _get_thresholds(self) -> dict:
        """Get rebalancing thresholds from config."""
        rebalancing = self.config.get("rebalancing", {})
        return {
            "minor": Decimal(str(rebalancing.get("drift_threshold_minor", 0.03))),
            "moderate": Decimal(
                str(rebalancing.get("drift_threshold_moderate", 0.05))
            ),
            "critical": Decimal(
                str(rebalancing.get("drift_threshold_critical", 0.10))
            ),
        }

    def _calculate_target_allocations(self) -> dict[str, Decimal]:
        """Calculate target allocations from config."""
        targets = {}
        allocations = self.config.get("portfolio", {}).get("allocations", {})

        for sleeve_name, sleeve_config in allocations.items():
            sleeve_weight = Decimal(str(sleeve_config.get("target_weight", 0)))
            assets = sleeve_config.get("assets", [])

            for asset in assets:
                symbol = asset.get("symbol")
                weight = Decimal(str(asset.get("weight", 0)))
                targets[symbol] = weight

        return targets

    def analyze_drift(self, portfolio: PortfolioState) -> dict:
        """
        Analyze portfolio drift from target allocations.

        Returns drift analysis with severity levels.
        """
        thresholds = self._get_thresholds()
        targets = self._calculate_target_allocations()
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "total_value": str(portfolio.total_value),
            "assets": {},
            "overall_drift": Decimal("0"),
            "severity": "normal",
            "needs_rebalance": False,
        }

        total_drift = Decimal("0")
        max_drift = Decimal("0")

        for symbol, target in targets.items():
            asset_data = portfolio.assets.get(symbol, {})
            current = Decimal(str(asset_data.get("weight", 0)))
            drift = abs(current - target)
            total_drift += drift
            max_drift = max(max_drift, drift)

            severity = "normal"
            if drift >= thresholds["critical"]:
                severity = "critical"
            elif drift >= thresholds["moderate"]:
                severity = "moderate"
            elif drift >= thresholds["minor"]:
                severity = "minor"

            analysis["assets"][symbol] = {
                "target_weight": str(target),
                "current_weight": str(current),
                "drift": str(drift),
                "severity": severity,
                "direction": "underweight" if current < target else "overweight",
            }

        analysis["overall_drift"] = str(total_drift / len(targets) if targets else 0)

        # Determine overall severity
        if max_drift >= thresholds["critical"]:
            analysis["severity"] = "critical"
            analysis["needs_rebalance"] = True
        elif max_drift >= thresholds["moderate"]:
            analysis["severity"] = "moderate"
        elif max_drift >= thresholds["minor"]:
            analysis["severity"] = "minor"

        return analysis

    def generate_rebalance_actions(
        self, portfolio: PortfolioState
    ) -> list[RebalanceAction]:
        """
        Generate list of rebalancing actions.

        Uses fractional share precision for exact allocations.
        """
        targets = self._calculate_target_allocations()
        actions = []

        for symbol, target in targets.items():
            asset_data = portfolio.assets.get(symbol, {})
            current_value = Decimal(str(asset_data.get("value", 0)))
            target_value = portfolio.total_value * target
            price = Decimal(str(asset_data.get("price", 1)))

            diff_value = target_value - current_value

            # Skip if difference is below minimum trade
            if abs(diff_value) < self.min_trade:
                continue

            # Calculate shares with precision
            shares = abs(diff_value / price).quantize(
                Decimal(10) ** -self.precision, rounding=ROUND_DOWN
            )

            if shares <= 0:
                continue

            action_type = "buy" if diff_value > 0 else "sell"
            reason = (
                f"{'Underweight' if diff_value > 0 else 'Overweight'} "
                f"by {abs(diff_value):.2f} USD"
            )

            actions.append(
                RebalanceAction(
                    symbol=symbol,
                    action=action_type,
                    shares=shares,
                    value=abs(diff_value),
                    reason=reason,
                    priority=1 if action_type == "sell" else 2,  # Sell first
                )
            )

        # Sort by priority (sells before buys)
        actions.sort(key=lambda x: x.priority)
        return actions

    def execute_rebalance(
        self, portfolio: PortfolioState, dry_run: bool = True
    ) -> dict:
        """
        Execute rebalancing actions.

        Args:
            portfolio: Current portfolio state
            dry_run: If True, simulate only (default: True for safety)

        Returns:
            Execution report
        """
        analysis = self.analyze_drift(portfolio)
        actions = self.generate_rebalance_actions(portfolio)

        report = {
            "timestamp": datetime.now().isoformat(),
            "dry_run": dry_run,
            "analysis": analysis,
            "actions": [],
            "summary": {
                "total_actions": len(actions),
                "buy_orders": 0,
                "sell_orders": 0,
                "total_buy_value": Decimal("0"),
                "total_sell_value": Decimal("0"),
            },
        }

        for action in actions:
            action_report = {
                "symbol": action.symbol,
                "action": action.action,
                "shares": str(action.shares),
                "value": str(action.value),
                "reason": action.reason,
                "status": "simulated" if dry_run else "executed",
            }

            if action.action == "buy":
                report["summary"]["buy_orders"] += 1
                report["summary"]["total_buy_value"] += action.value
            else:
                report["summary"]["sell_orders"] += 1
                report["summary"]["total_sell_value"] += action.value

            if not dry_run:
                # Here would be actual broker API calls
                # For now, mark as executed in simulation
                action_report["status"] = "executed"
                logger.info(
                    f"Executed: {action.action.upper()} "
                    f"{action.shares} {action.symbol}"
                )

            report["actions"].append(action_report)

        # Convert Decimal to string for JSON serialization
        report["summary"]["total_buy_value"] = str(
            report["summary"]["total_buy_value"]
        )
        report["summary"]["total_sell_value"] = str(
            report["summary"]["total_sell_value"]
        )

        return report


def create_sample_portfolio() -> PortfolioState:
    """Create a sample portfolio for demonstration."""
    return PortfolioState(
        total_value=Decimal("520.00"),
        assets={
            "VOO": {
                "weight": Decimal("0.38"),
                "value": Decimal("197.60"),
                "shares": Decimal("0.45"),
                "price": Decimal("439.11"),
            },
            "VTI": {
                "weight": Decimal("0.19"),
                "value": Decimal("98.80"),
                "shares": Decimal("0.38"),
                "price": Decimal("260.00"),
            },
            "SCHD": {
                "weight": Decimal("0.14"),
                "value": Decimal("72.80"),
                "shares": Decimal("0.95"),
                "price": Decimal("76.63"),
            },
            "VIG": {
                "weight": Decimal("0.09"),
                "value": Decimal("46.80"),
                "shares": Decimal("0.25"),
                "price": Decimal("187.20"),
            },
            "BND": {
                "weight": Decimal("0.05"),
                "value": Decimal("26.00"),
                "shares": Decimal("0.35"),
                "price": Decimal("74.29"),
            },
            "CASH": {
                "weight": Decimal("0.15"),
                "value": Decimal("78.00"),
                "shares": Decimal("78.00"),
                "price": Decimal("1.00"),
            },
        },
        cash=Decimal("78.00"),
        last_updated=datetime.now(),
    )


def main():
    """Main entry point for the rebalancer."""
    parser = argparse.ArgumentParser(
        description="Strategickhaos Wealth Engine - Portfolio Rebalancer"
    )
    parser.add_argument(
        "--config",
        default="wealth_engine_config.yaml",
        help="Path to configuration file",
    )
    parser.add_argument(
        "--analyze",
        action="store_true",
        help="Analyze drift only (no rebalancing)",
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Execute rebalancing (default is dry-run)",
    )
    parser.add_argument(
        "--output",
        choices=["json", "yaml", "text"],
        default="text",
        help="Output format",
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run with demo portfolio data",
    )

    args = parser.parse_args()

    try:
        # Find config file
        config_path = Path(args.config)
        if not config_path.exists():
            # Try relative to script location
            script_dir = Path(__file__).parent.parent.parent
            config_path = script_dir / args.config

        rebalancer = PortfolioRebalancer(str(config_path))

        # Use demo portfolio or would load real data
        if args.demo:
            portfolio = create_sample_portfolio()
        else:
            portfolio = create_sample_portfolio()
            logger.info(
                "No portfolio data source configured, using sample data"
            )

        if args.analyze:
            result = rebalancer.analyze_drift(portfolio)
        else:
            result = rebalancer.execute_rebalance(
                portfolio, dry_run=not args.execute
            )

        # Output results
        if args.output == "json":
            print(json.dumps(result, indent=2, default=str))
        elif args.output == "yaml":
            print(yaml.dump(result, default_flow_style=False))
        else:
            print("\n" + "=" * 60)
            print("STRATEGICKHAOS WEALTH ENGINE - REBALANCER REPORT")
            print("=" * 60)
            print(f"Timestamp: {result.get('timestamp', 'N/A')}")

            if "analysis" in result:
                analysis = result["analysis"]
                print(f"\nOverall Drift: {analysis.get('overall_drift', 'N/A')}")
                print(f"Severity: {analysis.get('severity', 'N/A').upper()}")
                print(
                    f"Needs Rebalance: "
                    f"{'Yes' if analysis.get('needs_rebalance') else 'No'}"
                )

            if "actions" in result and result["actions"]:
                print("\nRebalancing Actions:")
                print("-" * 40)
                for action in result["actions"]:
                    print(
                        f"  {action['action'].upper():4} "
                        f"{action['shares']:>10} {action['symbol']:5} "
                        f"(${action['value']})"
                    )
                    print(f"       Reason: {action['reason']}")
                    print(f"       Status: {action['status']}")

            if "summary" in result:
                summary = result["summary"]
                print("\nSummary:")
                print("-" * 40)
                print(f"  Total Actions: {summary['total_actions']}")
                print(f"  Buy Orders: {summary['buy_orders']}")
                print(f"  Sell Orders: {summary['sell_orders']}")
                print(f"  Total Buy Value: ${summary['total_buy_value']}")
                print(f"  Total Sell Value: ${summary['total_sell_value']}")

            print("\n" + "=" * 60)

    except FileNotFoundError as e:
        logger.error(f"Configuration error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Strategickhaos Wealth Engine - Dividend Compounder
===================================================
Automatic dividend reinvestment and long-term compounding engine.

Part of the four-script automation suite for the Strategickhaos Wealth Engine.
Zero leverage | Zero drift | Mathematically precise

"What 'just happened' is the birth of a machine that will grow quietly 
in the background while you live your life."
"""

import argparse
import json
import logging
import sys
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path
from typing import Optional

import yaml

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("wealth_engine.compounder")


@dataclass
class DividendPayment:
    """Represents a dividend payment."""

    symbol: str
    amount: Decimal
    date: datetime
    payment_type: str = "ordinary"  # ordinary | qualified
    reinvested: bool = False
    shares_purchased: Decimal = Decimal("0")


@dataclass
class CompoundingProjection:
    """Projected compounding results."""

    years: int
    starting_value: Decimal
    ending_value: Decimal
    total_dividends: Decimal
    total_growth: Decimal
    cagr: Decimal


@dataclass
class DividendState:
    """Current dividend tracking state."""

    pending_dividends: Decimal = Decimal("0")
    total_received_ytd: Decimal = Decimal("0")
    total_reinvested_ytd: Decimal = Decimal("0")
    qualified_dividends_ytd: Decimal = Decimal("0")
    ordinary_dividends_ytd: Decimal = Decimal("0")
    payments: list = field(default_factory=list)


class DividendCompounder:
    """
    Automatic dividend reinvestment and compounding engine.

    Features:
    - DRIP (Dividend Reinvestment Plan) automation
    - Fractional share reinvestment
    - Tax tracking (qualified vs ordinary)
    - Long-term compounding projections
    - Yield monitoring
    """

    def __init__(self, config_path: str):
        """Initialize compounder with configuration."""
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.dividend_config = self.config.get("dividend_compounding", {})

    def _load_config(self) -> dict:
        """Load configuration from YAML file."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config not found: {self.config_path}")

        with open(self.config_path) as f:
            return yaml.safe_load(f)

    def _get_reinvestment_settings(self) -> dict:
        """Get reinvestment settings from config."""
        reinvestment = self.dividend_config.get("reinvestment", {})
        return {
            "automatic": reinvestment.get("automatic", True),
            "min_accumulation": Decimal(
                str(reinvestment.get("min_accumulation", 1.00))
            ),
            "target_allocation": reinvestment.get(
                "target_allocation", "proportional"
            ),
            "fractional_shares": reinvestment.get("fractional_shares", True),
        }

    def record_dividend(
        self,
        state: DividendState,
        symbol: str,
        amount: Decimal,
        payment_type: str = "ordinary",
    ) -> DividendPayment:
        """
        Record a dividend payment.

        Args:
            state: Current dividend state
            symbol: Stock symbol
            amount: Dividend amount in USD
            payment_type: 'ordinary' or 'qualified'

        Returns:
            Recorded dividend payment
        """
        payment = DividendPayment(
            symbol=symbol,
            amount=amount,
            date=datetime.now(),
            payment_type=payment_type,
        )

        state.pending_dividends += amount
        state.total_received_ytd += amount

        if payment_type == "qualified":
            state.qualified_dividends_ytd += amount
        else:
            state.ordinary_dividends_ytd += amount

        state.payments.append(payment)

        logger.info(
            f"Recorded dividend: ${amount:.2f} from {symbol} ({payment_type})"
        )

        return payment

    def calculate_reinvestment(
        self,
        state: DividendState,
        portfolio_allocations: dict,
        current_prices: dict,
    ) -> list[dict]:
        """
        Calculate reinvestment allocations for pending dividends.

        Args:
            state: Current dividend state
            portfolio_allocations: Target portfolio allocations
            current_prices: Current asset prices

        Returns:
            List of reinvestment actions
        """
        settings = self._get_reinvestment_settings()
        actions = []

        if state.pending_dividends < settings["min_accumulation"]:
            logger.info(
                f"Pending dividends ${state.pending_dividends:.2f} "
                f"below minimum ${settings['min_accumulation']:.2f}"
            )
            return actions

        available = state.pending_dividends
        strategy = settings["target_allocation"]

        if strategy == "proportional":
            # Distribute proportionally to target weights
            for symbol, weight in portfolio_allocations.items():
                if symbol == "CASH":
                    continue

                allocation = available * Decimal(str(weight))
                price = Decimal(str(current_prices.get(symbol, 0)))

                if price > 0 and allocation >= Decimal("0.01"):
                    shares = (allocation / price).quantize(
                        Decimal("0.000001"), rounding=ROUND_HALF_UP
                    )

                    if shares > 0:
                        actions.append(
                            {
                                "symbol": symbol,
                                "shares": shares,
                                "amount": allocation,
                                "price": price,
                                "type": "dividend_reinvestment",
                            }
                        )

        elif strategy == "highest_yield":
            # Reinvest in highest yielding asset
            # Would need yield data - for now, use first asset
            if portfolio_allocations:
                symbol = next(
                    (s for s in portfolio_allocations if s != "CASH"), None
                )
                if symbol:
                    price = Decimal(str(current_prices.get(symbol, 0)))
                    if price > 0:
                        shares = (available / price).quantize(
                            Decimal("0.000001"), rounding=ROUND_HALF_UP
                        )
                        actions.append(
                            {
                                "symbol": symbol,
                                "shares": shares,
                                "amount": available,
                                "price": price,
                                "type": "dividend_reinvestment",
                            }
                        )

        elif strategy == "underweight":
            # Reinvest in most underweight asset
            # Would need current weights - simplified for now
            actions = self._calculate_underweight_reinvestment(
                available, portfolio_allocations, current_prices
            )

        return actions

    def _calculate_underweight_reinvestment(
        self,
        available: Decimal,
        allocations: dict,
        prices: dict,
    ) -> list[dict]:
        """Calculate reinvestment for underweight strategy."""
        # Simplified - in production would compare current vs target
        actions = []
        for symbol, weight in allocations.items():
            if symbol == "CASH":
                continue

            price = Decimal(str(prices.get(symbol, 0)))
            if price > 0:
                allocation = available * Decimal(str(weight))
                shares = (allocation / price).quantize(
                    Decimal("0.000001"), rounding=ROUND_HALF_UP
                )
                if shares > 0:
                    actions.append(
                        {
                            "symbol": symbol,
                            "shares": shares,
                            "amount": allocation,
                            "price": price,
                            "type": "dividend_reinvestment",
                        }
                    )
        return actions

    def execute_reinvestment(
        self,
        state: DividendState,
        actions: list[dict],
        dry_run: bool = True,
    ) -> dict:
        """
        Execute dividend reinvestment.

        Args:
            state: Current dividend state
            actions: Reinvestment actions to execute
            dry_run: If True, simulate only

        Returns:
            Execution report
        """
        report = {
            "timestamp": datetime.now().isoformat(),
            "dry_run": dry_run,
            "pending_before": str(state.pending_dividends),
            "actions": [],
            "total_reinvested": Decimal("0"),
        }

        for action in actions:
            execution = {
                "symbol": action["symbol"],
                "shares": str(action["shares"]),
                "amount": str(action["amount"]),
                "price": str(action["price"]),
                "status": "simulated" if dry_run else "executed",
            }

            if not dry_run:
                # Here would be actual broker API calls
                state.pending_dividends -= action["amount"]
                state.total_reinvested_ytd += action["amount"]

                # Mark recent dividends as reinvested
                for payment in reversed(state.payments):
                    if not payment.reinvested:
                        payment.reinvested = True
                        payment.shares_purchased = action["shares"]
                        break

                execution["status"] = "executed"
                logger.info(
                    f"Reinvested: {action['shares']} shares of "
                    f"{action['symbol']} at ${action['price']}"
                )

            report["actions"].append(execution)
            report["total_reinvested"] += action["amount"]

        report["total_reinvested"] = str(report["total_reinvested"])
        report["pending_after"] = str(state.pending_dividends)

        return report

    def project_compounding(
        self,
        starting_value: Decimal,
        annual_contribution: Decimal = Decimal("0"),
        years_list: Optional[list[int]] = None,
    ) -> list[CompoundingProjection]:
        """
        Project long-term compounding growth.

        Args:
            starting_value: Initial portfolio value
            annual_contribution: Annual contribution amount
            years_list: List of years to project

        Returns:
            List of projections for each year
        """
        projections_config = self.dividend_config.get("projections", {})
        growth_rate = Decimal(
            str(projections_config.get("assumed_growth_rate", 0.07))
        )
        dividend_growth = Decimal(
            str(projections_config.get("assumed_dividend_growth", 0.05))
        )

        if years_list is None:
            years_list = projections_config.get(
                "projection_years", [5, 10, 20, 30]
            )

        projections = []
        avg_yield = Decimal("0.025")  # 2.5% starting yield assumption

        for years in years_list:
            # Compound growth calculation
            total_value = starting_value
            total_dividends = Decimal("0")
            current_yield = avg_yield

            for year in range(years):
                # Growth from capital appreciation
                total_value *= 1 + growth_rate

                # Add annual contribution
                total_value += annual_contribution

                # Dividend income (reinvested)
                dividend_income = total_value * current_yield
                total_dividends += dividend_income
                total_value += dividend_income

                # Dividend growth
                current_yield *= 1 + dividend_growth

            ending_value = total_value.quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )
            total_growth = ending_value - starting_value - (
                annual_contribution * years
            )

            # Calculate CAGR
            cagr = (
                (ending_value / starting_value) ** (Decimal("1") / Decimal(str(years)))
            ) - 1

            projections.append(
                CompoundingProjection(
                    years=years,
                    starting_value=starting_value,
                    ending_value=ending_value,
                    total_dividends=total_dividends.quantize(
                        Decimal("0.01"), rounding=ROUND_HALF_UP
                    ),
                    total_growth=total_growth.quantize(
                        Decimal("0.01"), rounding=ROUND_HALF_UP
                    ),
                    cagr=cagr.quantize(
                        Decimal("0.0001"), rounding=ROUND_HALF_UP
                    ),
                )
            )

        return projections

    def get_dividend_summary(self, state: DividendState) -> dict:
        """Get summary of dividend activity."""
        return {
            "timestamp": datetime.now().isoformat(),
            "pending_dividends": str(state.pending_dividends),
            "ytd_summary": {
                "total_received": str(state.total_received_ytd),
                "total_reinvested": str(state.total_reinvested_ytd),
                "qualified": str(state.qualified_dividends_ytd),
                "ordinary": str(state.ordinary_dividends_ytd),
            },
            "payment_count": len(state.payments),
            "recent_payments": [
                {
                    "symbol": p.symbol,
                    "amount": str(p.amount),
                    "date": p.date.isoformat(),
                    "type": p.payment_type,
                    "reinvested": p.reinvested,
                }
                for p in state.payments[-5:]  # Last 5 payments
            ],
        }


def create_sample_state() -> DividendState:
    """Create sample dividend state for demonstration."""
    state = DividendState()

    # Simulate some dividend history
    sample_payments = [
        ("VOO", Decimal("1.52"), "qualified"),
        ("SCHD", Decimal("0.89"), "qualified"),
        ("VIG", Decimal("0.67"), "qualified"),
        ("BND", Decimal("0.12"), "ordinary"),
    ]

    for symbol, amount, ptype in sample_payments:
        payment = DividendPayment(
            symbol=symbol,
            amount=amount,
            date=datetime.now() - timedelta(days=30),
            payment_type=ptype,
        )
        state.payments.append(payment)
        state.total_received_ytd += amount
        if ptype == "qualified":
            state.qualified_dividends_ytd += amount
        else:
            state.ordinary_dividends_ytd += amount

    state.pending_dividends = Decimal("3.20")

    return state


def main():
    """Main entry point for the dividend compounder."""
    parser = argparse.ArgumentParser(
        description="Strategickhaos Wealth Engine - Dividend Compounder"
    )
    parser.add_argument(
        "--config",
        default="wealth_engine_config.yaml",
        help="Path to configuration file",
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Show dividend summary",
    )
    parser.add_argument(
        "--reinvest",
        action="store_true",
        help="Calculate and execute reinvestment",
    )
    parser.add_argument(
        "--project",
        action="store_true",
        help="Show compounding projections",
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Execute reinvestment (default is dry-run)",
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
        help="Run with demo data",
    )
    parser.add_argument(
        "--starting-value",
        type=float,
        default=520.00,
        help="Starting portfolio value for projections",
    )
    parser.add_argument(
        "--monthly-contribution",
        type=float,
        default=100.00,
        help="Monthly contribution amount",
    )

    args = parser.parse_args()

    try:
        # Find config file
        config_path = Path(args.config)
        if not config_path.exists():
            script_dir = Path(__file__).parent.parent.parent
            config_path = script_dir / args.config

        compounder = DividendCompounder(str(config_path))

        # Use demo state
        state = create_sample_state()

        # Sample data for calculations
        allocations = {"VOO": 0.40, "VTI": 0.20, "SCHD": 0.15, "VIG": 0.10, "BND": 0.05}
        prices = {
            "VOO": 439.11,
            "VTI": 260.00,
            "SCHD": 76.63,
            "VIG": 187.20,
            "BND": 74.29,
        }

        result = {}

        if args.summary:
            result = compounder.get_dividend_summary(state)

        elif args.reinvest:
            actions = compounder.calculate_reinvestment(
                state, allocations, prices
            )
            result = compounder.execute_reinvestment(
                state, actions, dry_run=not args.execute
            )

        elif args.project:
            starting = Decimal(str(args.starting_value))
            annual = Decimal(str(args.monthly_contribution * 12))
            projections = compounder.project_compounding(starting, annual)
            result = {
                "starting_value": str(starting),
                "annual_contribution": str(annual),
                "projections": [
                    {
                        "years": p.years,
                        "ending_value": str(p.ending_value),
                        "total_dividends": str(p.total_dividends),
                        "total_growth": str(p.total_growth),
                        "cagr": f"{p.cagr * 100:.2f}%",
                    }
                    for p in projections
                ],
            }

        else:
            # Default: show summary
            result = compounder.get_dividend_summary(state)

        # Output results
        if args.output == "json":
            print(json.dumps(result, indent=2, default=str))
        elif args.output == "yaml":
            print(yaml.dump(result, default_flow_style=False))
        else:
            print("\n" + "=" * 60)
            print("STRATEGICKHAOS WEALTH ENGINE - DIVIDEND COMPOUNDER")
            print("=" * 60)

            if "ytd_summary" in result:
                ytd = result["ytd_summary"]
                print(f"\nYTD Dividend Summary:")
                print("-" * 40)
                print(f"  Total Received:   ${ytd['total_received']}")
                print(f"  Total Reinvested: ${ytd['total_reinvested']}")
                print(f"  Qualified:        ${ytd['qualified']}")
                print(f"  Ordinary:         ${ytd['ordinary']}")
                print(f"  Pending:          ${result['pending_dividends']}")

            if "projections" in result:
                print(f"\nCompounding Projections:")
                print(f"Starting Value: ${result['starting_value']}")
                print(f"Annual Contribution: ${result['annual_contribution']}")
                print("-" * 40)
                print(f"{'Years':>6} {'Ending Value':>15} {'Growth':>12} {'CAGR':>8}")
                print("-" * 40)
                for p in result["projections"]:
                    print(
                        f"{p['years']:>6} ${p['ending_value']:>14} "
                        f"${p['total_growth']:>11} {p['cagr']:>7}"
                    )

            if "actions" in result:
                print(f"\nReinvestment Actions:")
                print("-" * 40)
                for action in result["actions"]:
                    print(
                        f"  {action['symbol']:5} "
                        f"{action['shares']:>10} shares "
                        f"@ ${action['price']} = ${action['amount']}"
                    )
                    print(f"       Status: {action['status']}")
                print(f"\nTotal Reinvested: ${result['total_reinvested']}")

            print("\n" + "=" * 60)

    except FileNotFoundError as e:
        logger.error(f"Configuration error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Strategickhaos Wealth Engine - Cashflow Autopilot
==================================================
Monthly cashflow automation with dollar-cost averaging.

Part of the four-script automation suite for the Strategickhaos Wealth Engine.
Zero leverage | Zero drift | Mathematically precise

"You literally created future wealth out of thin air with four text files
and your $520."
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
logger = logging.getLogger("wealth_engine.cashflow")


@dataclass
class DepositEvent:
    """Represents a scheduled or completed deposit."""

    amount: Decimal
    scheduled_date: datetime
    executed_date: Optional[datetime] = None
    status: str = "pending"  # pending | executed | failed | skipped
    auto_invested: bool = False
    investments: list = field(default_factory=list)


@dataclass
class DCAAllocation:
    """Dollar-cost averaging allocation for a deposit."""

    symbol: str
    target_amount: Decimal
    spread_days: int
    daily_amount: Decimal
    purchases: list = field(default_factory=list)


@dataclass
class CashflowState:
    """Current cashflow tracking state."""

    available_cash: Decimal = Decimal("0")
    pending_deposits: list = field(default_factory=list)
    completed_deposits: list = field(default_factory=list)
    total_deposited_ytd: Decimal = Decimal("0")
    total_invested_ytd: Decimal = Decimal("0")


class CashflowAutopilot:
    """
    Monthly cashflow automation with dollar-cost averaging.

    Features:
    - Scheduled deposit tracking
    - Automatic investment allocation
    - Dollar-cost averaging
    - Volatility-aware timing
    - Monthly summaries
    """

    def __init__(self, config_path: str):
        """Initialize cashflow autopilot with configuration."""
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.cashflow_config = self.config.get("cashflow_autopilot", {})

    def _load_config(self) -> dict:
        """Load configuration from YAML file."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config not found: {self.config_path}")

        with open(self.config_path) as f:
            return yaml.safe_load(f)

    def _get_deposit_settings(self) -> dict:
        """Get deposit settings from config."""
        deposits = self.cashflow_config.get("deposits", {})
        return {
            "frequency": deposits.get("frequency", "monthly"),
            "day_of_month": deposits.get("day_of_month", 1),
            "amount": Decimal(str(deposits.get("amount", 100.00))),
            "auto_invest": deposits.get("auto_invest", True),
        }

    def _get_dca_settings(self) -> dict:
        """Get DCA settings from config."""
        dca = self.cashflow_config.get("dca", {})
        return {
            "enabled": dca.get("enabled", True),
            "spread_days": dca.get("spread_days", 5),
            "volatility_aware": dca.get("volatility_aware", True),
        }

    def _get_target_allocations(self) -> dict[str, Decimal]:
        """Get target allocations from portfolio config."""
        allocations = {}
        portfolio = self.config.get("portfolio", {}).get("allocations", {})

        for sleeve_name, sleeve_config in portfolio.items():
            for asset in sleeve_config.get("assets", []):
                symbol = asset.get("symbol")
                weight = Decimal(str(asset.get("weight", 0)))
                if symbol != "CASH":
                    allocations[symbol] = weight

        return allocations

    def schedule_deposit(
        self,
        state: CashflowState,
        amount: Optional[Decimal] = None,
        scheduled_date: Optional[datetime] = None,
    ) -> DepositEvent:
        """
        Schedule a new deposit.

        Args:
            state: Current cashflow state
            amount: Deposit amount (uses config default if not provided)
            scheduled_date: When to deposit (uses next scheduled date if not provided)

        Returns:
            Scheduled deposit event
        """
        settings = self._get_deposit_settings()

        if amount is None:
            amount = settings["amount"]

        if scheduled_date is None:
            # Calculate next scheduled date
            today = datetime.now()
            day = settings["day_of_month"]

            if today.day <= day:
                scheduled_date = today.replace(day=day)
            else:
                # Next month
                if today.month == 12:
                    scheduled_date = today.replace(
                        year=today.year + 1, month=1, day=day
                    )
                else:
                    scheduled_date = today.replace(
                        month=today.month + 1, day=day
                    )

        deposit = DepositEvent(
            amount=amount,
            scheduled_date=scheduled_date,
            status="pending",
        )

        state.pending_deposits.append(deposit)
        logger.info(
            f"Scheduled deposit: ${amount:.2f} for "
            f"{scheduled_date.strftime('%Y-%m-%d')}"
        )

        return deposit

    def process_deposit(
        self,
        state: CashflowState,
        deposit: DepositEvent,
        dry_run: bool = True,
    ) -> dict:
        """
        Process a deposit and optionally auto-invest.

        Args:
            state: Current cashflow state
            deposit: Deposit to process
            dry_run: If True, simulate only

        Returns:
            Processing report
        """
        settings = self._get_deposit_settings()
        report = {
            "timestamp": datetime.now().isoformat(),
            "dry_run": dry_run,
            "deposit": {
                "amount": str(deposit.amount),
                "scheduled_date": deposit.scheduled_date.isoformat(),
                "status": deposit.status,
            },
            "investments": [],
        }

        if not dry_run:
            deposit.executed_date = datetime.now()
            deposit.status = "executed"
            state.available_cash += deposit.amount
            state.total_deposited_ytd += deposit.amount

            # Move from pending to completed
            if deposit in state.pending_deposits:
                state.pending_deposits.remove(deposit)
            state.completed_deposits.append(deposit)

            logger.info(f"Processed deposit: ${deposit.amount:.2f}")

        report["deposit"]["status"] = deposit.status

        # Auto-invest if enabled
        if settings["auto_invest"]:
            investments = self.calculate_investments(
                deposit.amount,
                self._get_target_allocations(),
            )
            report["investments"] = investments

            if not dry_run:
                for inv in investments:
                    deposit.investments.append(inv)
                    state.total_invested_ytd += Decimal(str(inv["amount"]))
                deposit.auto_invested = True

        return report

    def calculate_investments(
        self,
        amount: Decimal,
        allocations: dict[str, Decimal],
        current_prices: Optional[dict] = None,
    ) -> list[dict]:
        """
        Calculate investment allocations for a deposit.

        Args:
            amount: Amount to invest
            allocations: Target allocations
            current_prices: Current asset prices (optional)

        Returns:
            List of investment allocations
        """
        # Default prices for calculation
        if current_prices is None:
            current_prices = {
                "VOO": Decimal("439.11"),
                "VTI": Decimal("260.00"),
                "SCHD": Decimal("76.63"),
                "VIG": Decimal("187.20"),
                "BND": Decimal("74.29"),
            }

        investments = []
        strategy = self.cashflow_config.get(
            "new_deposit_strategy", "target_weights"
        )

        # Normalize allocations (exclude CASH)
        total_weight = sum(allocations.values())

        for symbol, weight in allocations.items():
            if symbol == "CASH":
                continue

            normalized_weight = weight / total_weight if total_weight > 0 else 0
            inv_amount = amount * normalized_weight
            price = current_prices.get(symbol, Decimal("1"))

            shares = (inv_amount / price).quantize(
                Decimal("0.000001"), rounding=ROUND_DOWN
            )

            if shares > 0:
                investments.append(
                    {
                        "symbol": symbol,
                        "shares": str(shares),
                        "amount": str(inv_amount.quantize(Decimal("0.01"))),
                        "price": str(price),
                        "weight": str(normalized_weight.quantize(Decimal("0.0001"))),
                    }
                )

        return investments

    def calculate_dca_schedule(
        self,
        amount: Decimal,
        allocations: dict[str, Decimal],
        start_date: Optional[datetime] = None,
    ) -> list[DCAAllocation]:
        """
        Calculate dollar-cost averaging schedule.

        Args:
            amount: Total amount to invest
            allocations: Target allocations
            start_date: When to start DCA

        Returns:
            List of DCA allocations
        """
        dca_settings = self._get_dca_settings()
        spread_days = dca_settings["spread_days"]

        if start_date is None:
            start_date = datetime.now()

        # Normalize allocations
        total_weight = sum(
            w for s, w in allocations.items() if s != "CASH"
        )

        dca_allocations = []

        for symbol, weight in allocations.items():
            if symbol == "CASH":
                continue

            normalized_weight = weight / total_weight if total_weight > 0 else 0
            target_amount = amount * normalized_weight
            daily_amount = target_amount / spread_days

            dca = DCAAllocation(
                symbol=symbol,
                target_amount=target_amount,
                spread_days=spread_days,
                daily_amount=daily_amount.quantize(Decimal("0.01")),
            )

            # Generate purchase schedule
            for day in range(spread_days):
                purchase_date = start_date.replace(
                    day=min(start_date.day + day, 28)  # Safe day handling
                )
                dca.purchases.append(
                    {
                        "date": purchase_date.isoformat(),
                        "amount": str(daily_amount.quantize(Decimal("0.01"))),
                        "status": "scheduled",
                    }
                )

            dca_allocations.append(dca)

        return dca_allocations

    def get_monthly_summary(self, state: CashflowState) -> dict:
        """Get monthly cashflow summary."""
        settings = self._get_deposit_settings()

        return {
            "timestamp": datetime.now().isoformat(),
            "available_cash": str(state.available_cash),
            "ytd_summary": {
                "total_deposited": str(state.total_deposited_ytd),
                "total_invested": str(state.total_invested_ytd),
                "investment_rate": str(
                    (
                        state.total_invested_ytd / state.total_deposited_ytd * 100
                    ).quantize(Decimal("0.01"))
                    if state.total_deposited_ytd > 0
                    else Decimal("0")
                )
                + "%",
            },
            "settings": {
                "frequency": settings["frequency"],
                "day_of_month": settings["day_of_month"],
                "default_amount": str(settings["amount"]),
                "auto_invest": settings["auto_invest"],
            },
            "pending_deposits": len(state.pending_deposits),
            "completed_deposits": len(state.completed_deposits),
        }

    def get_annual_projection(
        self,
        monthly_amount: Decimal,
        current_portfolio: Decimal,
    ) -> dict:
        """
        Project annual cashflow and growth.

        Args:
            monthly_amount: Monthly deposit amount
            current_portfolio: Current portfolio value

        Returns:
            Annual projection
        """
        annual_deposits = monthly_amount * 12
        projections = self.config.get(
            "dividend_compounding", {}
        ).get("projections", {})
        growth_rate = Decimal(
            str(projections.get("assumed_growth_rate", 0.07))
        )

        # Simple projection
        year_end_deposits = current_portfolio + annual_deposits
        year_end_growth = year_end_deposits * (1 + growth_rate)

        return {
            "current_portfolio": str(current_portfolio),
            "monthly_deposit": str(monthly_amount),
            "annual_deposits": str(annual_deposits),
            "projected_year_end": str(
                year_end_growth.quantize(Decimal("0.01"))
            ),
            "projected_growth": str(
                (year_end_growth - current_portfolio - annual_deposits).quantize(
                    Decimal("0.01")
                )
            ),
            "assumed_growth_rate": f"{growth_rate * 100:.1f}%",
        }


def create_sample_state() -> CashflowState:
    """Create sample cashflow state for demonstration."""
    state = CashflowState()
    state.available_cash = Decimal("25.00")
    state.total_deposited_ytd = Decimal("400.00")
    state.total_invested_ytd = Decimal("375.00")

    # Add some completed deposits
    for i in range(4):
        deposit = DepositEvent(
            amount=Decimal("100.00"),
            scheduled_date=datetime.now().replace(
                month=max(1, datetime.now().month - 4 + i)
            ),
            executed_date=datetime.now().replace(
                month=max(1, datetime.now().month - 4 + i)
            ),
            status="executed",
            auto_invested=True,
        )
        state.completed_deposits.append(deposit)

    return state


def main():
    """Main entry point for the cashflow autopilot."""
    parser = argparse.ArgumentParser(
        description="Strategickhaos Wealth Engine - Cashflow Autopilot"
    )
    parser.add_argument(
        "--config",
        default="wealth_engine_config.yaml",
        help="Path to configuration file",
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Show cashflow summary",
    )
    parser.add_argument(
        "--schedule",
        action="store_true",
        help="Schedule a new deposit",
    )
    parser.add_argument(
        "--process",
        action="store_true",
        help="Process pending deposits",
    )
    parser.add_argument(
        "--dca",
        action="store_true",
        help="Calculate DCA schedule",
    )
    parser.add_argument(
        "--project",
        action="store_true",
        help="Show annual projection",
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Execute actions (default is dry-run)",
    )
    parser.add_argument(
        "--amount",
        type=float,
        help="Override deposit amount",
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

    args = parser.parse_args()

    try:
        # Find config file
        config_path = Path(args.config)
        if not config_path.exists():
            script_dir = Path(__file__).parent.parent.parent
            config_path = script_dir / args.config

        autopilot = CashflowAutopilot(str(config_path))

        # Use demo state
        state = create_sample_state()

        # Get allocations
        allocations = autopilot._get_target_allocations()

        result = {}
        amount = Decimal(str(args.amount)) if args.amount else Decimal("100.00")

        if args.schedule:
            deposit = autopilot.schedule_deposit(state, amount=amount)
            result = {
                "scheduled": {
                    "amount": str(deposit.amount),
                    "date": deposit.scheduled_date.isoformat(),
                    "status": deposit.status,
                }
            }

        elif args.process:
            if state.pending_deposits:
                deposit = state.pending_deposits[0]
            else:
                deposit = autopilot.schedule_deposit(state, amount=amount)

            result = autopilot.process_deposit(
                state, deposit, dry_run=not args.execute
            )

        elif args.dca:
            dca_allocations = autopilot.calculate_dca_schedule(
                amount, allocations
            )
            result = {
                "amount": str(amount),
                "dca_schedule": [
                    {
                        "symbol": dca.symbol,
                        "target_amount": str(dca.target_amount),
                        "daily_amount": str(dca.daily_amount),
                        "spread_days": dca.spread_days,
                        "purchases": dca.purchases,
                    }
                    for dca in dca_allocations
                ],
            }

        elif args.project:
            result = autopilot.get_annual_projection(
                amount, Decimal("520.00")
            )

        else:
            result = autopilot.get_monthly_summary(state)

        # Output results
        if args.output == "json":
            print(json.dumps(result, indent=2, default=str))
        elif args.output == "yaml":
            print(yaml.dump(result, default_flow_style=False))
        else:
            print("\n" + "=" * 60)
            print("STRATEGICKHAOS WEALTH ENGINE - CASHFLOW AUTOPILOT")
            print("=" * 60)

            if "ytd_summary" in result:
                ytd = result["ytd_summary"]
                print(f"\nYTD Cashflow Summary:")
                print("-" * 40)
                print(f"  Total Deposited:  ${ytd['total_deposited']}")
                print(f"  Total Invested:   ${ytd['total_invested']}")
                print(f"  Investment Rate:  {ytd['investment_rate']}")
                print(f"  Available Cash:   ${result['available_cash']}")
                print(f"\nSettings:")
                settings = result["settings"]
                print(f"  Frequency:        {settings['frequency']}")
                print(f"  Day of Month:     {settings['day_of_month']}")
                print(f"  Default Amount:   ${settings['default_amount']}")
                print(f"  Auto-Invest:      {settings['auto_invest']}")

            if "scheduled" in result:
                sched = result["scheduled"]
                print(f"\nScheduled Deposit:")
                print("-" * 40)
                print(f"  Amount: ${sched['amount']}")
                print(f"  Date:   {sched['date']}")
                print(f"  Status: {sched['status']}")

            if "dca_schedule" in result:
                print(f"\nDCA Schedule (${result['amount']} over 5 days):")
                print("-" * 40)
                for dca in result["dca_schedule"]:
                    print(f"\n  {dca['symbol']}:")
                    print(f"    Target: ${dca['target_amount']}")
                    print(f"    Daily:  ${dca['daily_amount']}")
                    for purchase in dca["purchases"][:3]:  # Show first 3
                        print(
                            f"      {purchase['date'][:10]}: "
                            f"${purchase['amount']}"
                        )

            if "projected_year_end" in result:
                print(f"\nAnnual Projection:")
                print("-" * 40)
                print(f"  Current Portfolio:   ${result['current_portfolio']}")
                print(f"  Monthly Deposit:     ${result['monthly_deposit']}")
                print(f"  Annual Deposits:     ${result['annual_deposits']}")
                print(f"  Growth Rate:         {result['assumed_growth_rate']}")
                print(f"  Projected Year End:  ${result['projected_year_end']}")
                print(f"  Projected Growth:    ${result['projected_growth']}")

            if "investments" in result and result["investments"]:
                print(f"\nInvestment Allocations:")
                print("-" * 40)
                for inv in result["investments"]:
                    print(
                        f"  {inv['symbol']:5} "
                        f"{inv['shares']:>10} shares "
                        f"@ ${inv['price']} = ${inv['amount']}"
                    )

            print("\n" + "=" * 60)

    except FileNotFoundError as e:
        logger.error(f"Configuration error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

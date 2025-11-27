#!/usr/bin/env python3
"""
Strategickhaos Wealth Engine - Tactical Manager
================================================
Tactical sleeve management with opportunity-based positioning.

Part of the four-script automation suite for the Strategickhaos Wealth Engine.
Zero leverage | Zero drift | Mathematically precise

"This is what it feels like when the two of us build something unstoppable."
"""

import argparse
import json
import logging
import sys
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from decimal import ROUND_HALF_UP, Decimal
from enum import Enum
from pathlib import Path
from typing import Optional

import yaml

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("wealth_engine.tactical")


class TacticalTrigger(Enum):
    """Types of tactical deployment triggers."""

    VOLATILITY_SPIKE = "volatility_spike"
    DRAWDOWN = "drawdown"
    OPPORTUNITY = "opportunity"
    MANUAL = "manual"
    SCHEDULED = "scheduled"


class PositionState(Enum):
    """States for tactical positions."""

    STANDBY = "standby"
    ACTIVE = "active"
    CLOSING = "closing"
    CLOSED = "closed"


@dataclass
class TacticalPosition:
    """Represents a tactical position."""

    position_id: str
    symbol: str
    entry_date: datetime
    entry_price: Decimal
    shares: Decimal
    value: Decimal
    trigger: TacticalTrigger
    state: PositionState = PositionState.ACTIVE
    stop_loss_price: Optional[Decimal] = None
    target_price: Optional[Decimal] = None
    exit_date: Optional[datetime] = None
    exit_price: Optional[Decimal] = None
    pnl: Optional[Decimal] = None
    notes: str = ""


@dataclass
class TacticalState:
    """Current tactical sleeve state."""

    mode: str = "standby"  # standby | active | deployed
    available_capital: Decimal = Decimal("0")
    deployed_capital: Decimal = Decimal("0")
    positions: list = field(default_factory=list)
    closed_positions: list = field(default_factory=list)
    total_pnl_ytd: Decimal = Decimal("0")


@dataclass
class MarketConditions:
    """Current market conditions for tactical decisions."""

    vix: Decimal = Decimal("15.0")
    sp500_drawdown: Decimal = Decimal("0.0")
    trend: str = "neutral"  # bullish | bearish | neutral
    volatility_regime: str = "low"  # low | normal | high | extreme


class TacticalManager:
    """
    Tactical sleeve manager for opportunistic positioning.

    Features:
    - Volatility-based deployment triggers
    - Drawdown opportunity detection
    - Position sizing and risk controls
    - Stop-loss management
    - Time-based position limits
    """

    def __init__(self, config_path: str):
        """Initialize tactical manager with configuration."""
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.tactical_config = self.config.get("tactical_sleeve", {})

    def _load_config(self) -> dict:
        """Load configuration from YAML file."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config not found: {self.config_path}")

        with open(self.config_path) as f:
            return yaml.safe_load(f)

    def _get_deployment_triggers(self) -> list[dict]:
        """Get deployment triggers from config."""
        deployment = self.tactical_config.get("deployment", {})
        return deployment.get("triggers", [])

    def _get_risk_controls(self) -> dict:
        """Get risk controls from config."""
        risk = self.tactical_config.get("risk_controls", {})
        return {
            "max_single_position": Decimal(
                str(risk.get("max_single_position", 0.05))
            ),
            "stop_loss": Decimal(str(risk.get("stop_loss", 0.15))),
            "time_limit_days": risk.get("time_limit_days", 90),
        }

    def _get_allocation_limits(self) -> dict:
        """Get allocation limits from config."""
        return {
            "max": Decimal(
                str(self.tactical_config.get("max_allocation", 0.15))
            ),
            "min": Decimal(
                str(self.tactical_config.get("min_allocation", 0.00))
            ),
        }

    def evaluate_triggers(
        self, conditions: MarketConditions
    ) -> list[dict]:
        """
        Evaluate deployment triggers against current conditions.

        Args:
            conditions: Current market conditions

        Returns:
            List of triggered conditions
        """
        triggers = self._get_deployment_triggers()
        triggered = []

        for trigger in triggers:
            trigger_type = trigger.get("type")

            if trigger_type == "volatility_spike":
                threshold = Decimal(str(trigger.get("threshold", 25)))
                if conditions.vix >= threshold:
                    triggered.append(
                        {
                            "type": trigger_type,
                            "threshold": str(threshold),
                            "current_value": str(conditions.vix),
                            "triggered": True,
                            "recommendation": "Consider deploying tactical capital",
                        }
                    )

            elif trigger_type == "drawdown":
                threshold = Decimal(str(trigger.get("threshold", 0.10)))
                if abs(conditions.sp500_drawdown) >= threshold:
                    triggered.append(
                        {
                            "type": trigger_type,
                            "threshold": str(threshold),
                            "current_value": str(conditions.sp500_drawdown),
                            "triggered": True,
                            "recommendation": (
                                "Drawdown opportunity detected"
                            ),
                        }
                    )

            elif trigger_type == "opportunity":
                # Manual override - always available
                if trigger.get("manual_override", True):
                    triggered.append(
                        {
                            "type": trigger_type,
                            "manual_override": True,
                            "triggered": False,  # Requires manual action
                            "recommendation": (
                                "Manual opportunity deployment available"
                            ),
                        }
                    )

        return triggered

    def calculate_position_size(
        self,
        portfolio_value: Decimal,
        available_tactical: Decimal,
        risk_level: str = "moderate",
    ) -> dict:
        """
        Calculate appropriate position size.

        Args:
            portfolio_value: Total portfolio value
            available_tactical: Available tactical capital
            risk_level: Risk level (conservative | moderate | aggressive)

        Returns:
            Position sizing recommendation
        """
        limits = self._get_allocation_limits()
        risk_controls = self._get_risk_controls()

        # Base position size
        max_position = portfolio_value * risk_controls["max_single_position"]

        # Adjust based on risk level
        multipliers = {
            "conservative": Decimal("0.5"),
            "moderate": Decimal("1.0"),
            "aggressive": Decimal("1.5"),
        }
        multiplier = multipliers.get(risk_level, Decimal("1.0"))

        recommended_size = min(
            max_position * multiplier,
            available_tactical,
            portfolio_value * limits["max"],
        )

        return {
            "portfolio_value": str(portfolio_value),
            "available_tactical": str(available_tactical),
            "risk_level": risk_level,
            "max_position_pct": str(risk_controls["max_single_position"] * 100),
            "recommended_size": str(
                recommended_size.quantize(Decimal("0.01"))
            ),
            "max_allowed": str(
                (portfolio_value * limits["max"]).quantize(Decimal("0.01"))
            ),
        }

    def open_position(
        self,
        state: TacticalState,
        symbol: str,
        shares: Decimal,
        price: Decimal,
        trigger: TacticalTrigger,
        notes: str = "",
        dry_run: bool = True,
    ) -> dict:
        """
        Open a new tactical position.

        Args:
            state: Current tactical state
            symbol: Asset symbol
            shares: Number of shares
            price: Entry price
            trigger: What triggered the position
            notes: Optional notes
            dry_run: If True, simulate only

        Returns:
            Position opening report
        """
        risk_controls = self._get_risk_controls()
        value = shares * price

        # Calculate stop loss
        stop_loss_price = price * (1 - risk_controls["stop_loss"])

        position = TacticalPosition(
            position_id=f"TAC-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            symbol=symbol,
            entry_date=datetime.now(),
            entry_price=price,
            shares=shares,
            value=value,
            trigger=trigger,
            stop_loss_price=stop_loss_price,
            notes=notes,
        )

        report = {
            "timestamp": datetime.now().isoformat(),
            "dry_run": dry_run,
            "position": {
                "id": position.position_id,
                "symbol": symbol,
                "shares": str(shares),
                "entry_price": str(price),
                "value": str(value),
                "stop_loss": str(stop_loss_price.quantize(Decimal("0.01"))),
                "trigger": trigger.value,
                "state": position.state.value,
            },
            "status": "simulated" if dry_run else "opened",
        }

        if not dry_run:
            state.positions.append(position)
            state.deployed_capital += value
            state.available_capital -= value
            state.mode = "active"
            logger.info(
                f"Opened tactical position: {shares} {symbol} @ ${price}"
            )

        return report

    def close_position(
        self,
        state: TacticalState,
        position_id: str,
        exit_price: Decimal,
        reason: str = "manual",
        dry_run: bool = True,
    ) -> dict:
        """
        Close a tactical position.

        Args:
            state: Current tactical state
            position_id: Position ID to close
            exit_price: Exit price
            reason: Reason for closing
            dry_run: If True, simulate only

        Returns:
            Position closing report
        """
        position = next(
            (p for p in state.positions if p.position_id == position_id),
            None,
        )

        if position is None:
            return {
                "error": f"Position {position_id} not found",
                "status": "failed",
            }

        exit_value = position.shares * exit_price
        pnl = exit_value - position.value
        pnl_pct = (pnl / position.value * 100).quantize(Decimal("0.01"))

        report = {
            "timestamp": datetime.now().isoformat(),
            "dry_run": dry_run,
            "position": {
                "id": position_id,
                "symbol": position.symbol,
                "entry_price": str(position.entry_price),
                "exit_price": str(exit_price),
                "shares": str(position.shares),
                "entry_value": str(position.value),
                "exit_value": str(exit_value.quantize(Decimal("0.01"))),
                "pnl": str(pnl.quantize(Decimal("0.01"))),
                "pnl_pct": f"{pnl_pct}%",
                "hold_days": (datetime.now() - position.entry_date).days,
            },
            "reason": reason,
            "status": "simulated" if dry_run else "closed",
        }

        if not dry_run:
            position.exit_date = datetime.now()
            position.exit_price = exit_price
            position.pnl = pnl
            position.state = PositionState.CLOSED

            state.positions.remove(position)
            state.closed_positions.append(position)
            state.deployed_capital -= position.value
            state.available_capital += exit_value
            state.total_pnl_ytd += pnl

            if not state.positions:
                state.mode = "standby"

            logger.info(
                f"Closed tactical position: {position.symbol} "
                f"PnL: ${pnl:.2f} ({pnl_pct}%)"
            )

        return report

    def check_stop_losses(
        self,
        state: TacticalState,
        current_prices: dict,
        dry_run: bool = True,
    ) -> list[dict]:
        """
        Check all positions for stop-loss triggers.

        Args:
            state: Current tactical state
            current_prices: Current asset prices
            dry_run: If True, simulate only

        Returns:
            List of stop-loss reports
        """
        reports = []

        for position in state.positions:
            current_price = Decimal(
                str(current_prices.get(position.symbol, position.entry_price))
            )

            if (
                position.stop_loss_price
                and current_price <= position.stop_loss_price
            ):
                report = self.close_position(
                    state,
                    position.position_id,
                    current_price,
                    reason="stop_loss",
                    dry_run=dry_run,
                )
                reports.append(report)
                logger.warning(
                    f"Stop-loss triggered for {position.symbol} "
                    f"at ${current_price}"
                )

        return reports

    def check_time_limits(
        self,
        state: TacticalState,
        current_prices: dict,
        dry_run: bool = True,
    ) -> list[dict]:
        """
        Check positions for time limit expiration.

        Args:
            state: Current tactical state
            current_prices: Current asset prices
            dry_run: If True, simulate only

        Returns:
            List of time limit reports
        """
        risk_controls = self._get_risk_controls()
        time_limit = risk_controls["time_limit_days"]
        reports = []

        for position in state.positions:
            days_held = (datetime.now() - position.entry_date).days

            if days_held >= time_limit:
                current_price = Decimal(
                    str(current_prices.get(position.symbol, position.entry_price))
                )
                report = self.close_position(
                    state,
                    position.position_id,
                    current_price,
                    reason="time_limit",
                    dry_run=dry_run,
                )
                reports.append(report)
                logger.info(
                    f"Time limit reached for {position.symbol} "
                    f"({days_held} days)"
                )

        return reports

    def get_tactical_summary(self, state: TacticalState) -> dict:
        """Get tactical sleeve summary."""
        total_value = state.available_capital + state.deployed_capital

        return {
            "timestamp": datetime.now().isoformat(),
            "mode": state.mode,
            "capital": {
                "total": str(total_value),
                "available": str(state.available_capital),
                "deployed": str(state.deployed_capital),
                "utilization": str(
                    (
                        state.deployed_capital / total_value * 100
                    ).quantize(Decimal("0.01"))
                    if total_value > 0
                    else Decimal("0")
                )
                + "%",
            },
            "positions": {
                "active": len(state.positions),
                "closed_ytd": len(state.closed_positions),
            },
            "performance": {
                "total_pnl_ytd": str(state.total_pnl_ytd),
            },
            "active_positions": [
                {
                    "id": p.position_id,
                    "symbol": p.symbol,
                    "shares": str(p.shares),
                    "entry_price": str(p.entry_price),
                    "value": str(p.value),
                    "days_held": (datetime.now() - p.entry_date).days,
                    "stop_loss": str(p.stop_loss_price) if p.stop_loss_price else None,
                }
                for p in state.positions
            ],
        }


def create_sample_state() -> TacticalState:
    """Create sample tactical state for demonstration."""
    state = TacticalState()
    state.mode = "standby"
    state.available_capital = Decimal("52.00")  # 10% of $520
    state.deployed_capital = Decimal("0")
    state.total_pnl_ytd = Decimal("0")

    return state


def create_sample_conditions() -> MarketConditions:
    """Create sample market conditions for demonstration."""
    return MarketConditions(
        vix=Decimal("18.5"),
        sp500_drawdown=Decimal("-0.03"),
        trend="neutral",
        volatility_regime="normal",
    )


def main():
    """Main entry point for the tactical manager."""
    parser = argparse.ArgumentParser(
        description="Strategickhaos Wealth Engine - Tactical Manager"
    )
    parser.add_argument(
        "--config",
        default="wealth_engine_config.yaml",
        help="Path to configuration file",
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Show tactical summary",
    )
    parser.add_argument(
        "--evaluate",
        action="store_true",
        help="Evaluate deployment triggers",
    )
    parser.add_argument(
        "--size",
        action="store_true",
        help="Calculate position sizing",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check stop-losses and time limits",
    )
    parser.add_argument(
        "--portfolio-value",
        type=float,
        default=520.00,
        help="Total portfolio value",
    )
    parser.add_argument(
        "--risk-level",
        choices=["conservative", "moderate", "aggressive"],
        default="moderate",
        help="Risk level for position sizing",
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Execute actions (default is dry-run)",
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

        manager = TacticalManager(str(config_path))

        # Use demo state and conditions
        state = create_sample_state()
        conditions = create_sample_conditions()

        result = {}
        portfolio_value = Decimal(str(args.portfolio_value))

        if args.evaluate:
            triggered = manager.evaluate_triggers(conditions)
            result = {
                "timestamp": datetime.now().isoformat(),
                "market_conditions": {
                    "vix": str(conditions.vix),
                    "sp500_drawdown": str(conditions.sp500_drawdown),
                    "trend": conditions.trend,
                    "volatility_regime": conditions.volatility_regime,
                },
                "triggers_evaluated": len(
                    manager._get_deployment_triggers()
                ),
                "triggered": triggered,
            }

        elif args.size:
            result = manager.calculate_position_size(
                portfolio_value,
                state.available_capital,
                args.risk_level,
            )

        elif args.check:
            prices = {"VOO": 439.11, "VTI": 260.00, "SCHD": 76.63}
            stop_loss_reports = manager.check_stop_losses(
                state, prices, dry_run=not args.execute
            )
            time_limit_reports = manager.check_time_limits(
                state, prices, dry_run=not args.execute
            )
            result = {
                "stop_loss_checks": stop_loss_reports,
                "time_limit_checks": time_limit_reports,
            }

        else:
            result = manager.get_tactical_summary(state)

        # Output results
        if args.output == "json":
            print(json.dumps(result, indent=2, default=str))
        elif args.output == "yaml":
            print(yaml.dump(result, default_flow_style=False))
        else:
            print("\n" + "=" * 60)
            print("STRATEGICKHAOS WEALTH ENGINE - TACTICAL MANAGER")
            print("=" * 60)

            if "mode" in result:
                capital = result.get("capital", {})
                print(f"\nTactical Sleeve Status:")
                print("-" * 40)
                print(f"  Mode:         {result['mode'].upper()}")
                print(f"  Total:        ${capital.get('total', 'N/A')}")
                print(f"  Available:    ${capital.get('available', 'N/A')}")
                print(f"  Deployed:     ${capital.get('deployed', 'N/A')}")
                print(f"  Utilization:  {capital.get('utilization', 'N/A')}")

                positions = result.get("positions", {})
                print(f"\nPositions:")
                print(f"  Active:       {positions.get('active', 0)}")
                print(f"  Closed YTD:   {positions.get('closed_ytd', 0)}")

                perf = result.get("performance", {})
                print(f"\nPerformance:")
                print(f"  Total PnL YTD: ${perf.get('total_pnl_ytd', '0')}")

            if "market_conditions" in result:
                cond = result["market_conditions"]
                print(f"\nMarket Conditions:")
                print("-" * 40)
                print(f"  VIX:              {cond['vix']}")
                print(f"  S&P 500 Drawdown: {cond['sp500_drawdown']}")
                print(f"  Trend:            {cond['trend']}")
                print(f"  Volatility:       {cond['volatility_regime']}")

                print(f"\nTrigger Evaluation:")
                for trigger in result.get("triggered", []):
                    status = "TRIGGERED" if trigger.get("triggered") else "standby"
                    print(f"  [{status}] {trigger['type']}")
                    if "recommendation" in trigger:
                        print(f"           {trigger['recommendation']}")

            if "recommended_size" in result:
                print(f"\nPosition Sizing:")
                print("-" * 40)
                print(f"  Portfolio Value:  ${result['portfolio_value']}")
                print(f"  Available:        ${result['available_tactical']}")
                print(f"  Risk Level:       {result['risk_level']}")
                print(f"  Max Position %:   {result['max_position_pct']}%")
                print(f"  Recommended Size: ${result['recommended_size']}")
                print(f"  Max Allowed:      ${result['max_allowed']}")

            print("\n" + "=" * 60)

    except FileNotFoundError as e:
        logger.error(f"Configuration error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

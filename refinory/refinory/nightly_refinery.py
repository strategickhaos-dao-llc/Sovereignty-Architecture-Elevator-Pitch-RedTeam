#!/usr/bin/env python3
"""
Nightly Refinery - Portfolio Monitoring & Automation Script
Strategickhaos Hybrid Refinery Financial Architecture

This script watches the 14-position dividend core portfolio and tracks:
- Real-time position values and changes
- Dividend payments and DRIP reinvestments
- SwarmGate monthly inflow automation
- Portfolio drift and rebalancing alerts

Usage:
    python nightly_refinery.py [--watch] [--report] [--rescale NEW_CAPITAL]
"""

import argparse
import asyncio
import json
from datetime import datetime, date, timedelta
from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
import structlog

# Local imports
from .portfolio_config import (
    DIVIDEND_CORE,
    TOTAL_CAPITAL,
    SWARMGATE,
    WEBULL_ACCOUNT_ID,
    DRIP_ENABLED,
    EXPECTED_YIELD_MIN,
    EXPECTED_YIELD_MAX,
    get_portfolio_summary,
    get_position_details,
    rescale_portfolio,
)
from .swarmgate import SwarmGateRouter, create_default_swarmgate

logger = structlog.get_logger()


@dataclass
class PortfolioSnapshot:
    """Point-in-time portfolio snapshot"""
    timestamp: datetime
    total_value: Decimal
    positions: List[Dict]
    daily_change_pct: Optional[Decimal] = None
    dividends_collected: Decimal = Decimal("0")
    swarmgate_routed: Decimal = Decimal("0")


@dataclass
class DividendPayment:
    """Record of a dividend payment"""
    ticker: str
    payment_date: date
    amount: Decimal
    reinvested: bool
    shares_purchased: Optional[Decimal] = None


@dataclass 
class PortfolioAlert:
    """Portfolio monitoring alert"""
    alert_type: str  # drift, dividend, swarmgate, rebalance
    severity: str  # info, warning, critical
    message: str
    timestamp: datetime
    data: Optional[Dict] = None


class NightlyRefinery:
    """
    Nightly Refinery - Portfolio Monitoring Engine
    
    Watches the 14-ticker dividend core portfolio and provides:
    - Real-time monitoring and alerts
    - Dividend tracking and DRIP management
    - SwarmGate automation integration
    - Portfolio health metrics
    - Rebalancing recommendations
    
    The Refinery runs nightly to:
    1. Capture portfolio snapshot
    2. Check for dividend payments
    3. Process SwarmGate routing (on 1st of month)
    4. Generate health reports
    5. Send alerts for significant events
    """
    
    def __init__(
        self,
        initial_capital: Decimal = TOTAL_CAPITAL,
        drift_threshold_pct: Decimal = Decimal("5.0"),
        enable_notifications: bool = True
    ):
        """
        Initialize Nightly Refinery
        
        Args:
            initial_capital: Starting capital (default $520)
            drift_threshold_pct: Alert threshold for position drift
            enable_notifications: Enable Discord/webhook notifications
        """
        self.initial_capital = initial_capital
        self.current_capital = initial_capital
        self.drift_threshold_pct = drift_threshold_pct
        self.enable_notifications = enable_notifications
        
        # Portfolio tracking
        self.snapshots: List[PortfolioSnapshot] = []
        self.dividends: List[DividendPayment] = []
        self.alerts: List[PortfolioAlert] = []
        
        # SwarmGate integration
        self.swarmgate = create_default_swarmgate()
        
        # Tracking metrics
        self.total_dividends_collected = Decimal("0")
        self.total_swarmgate_routed = Decimal("0")
        self.inception_date = datetime.now()
        
        logger.info(
            "nightly_refinery_initialized",
            initial_capital=float(initial_capital),
            positions=len(DIVIDEND_CORE),
            webull_account=WEBULL_ACCOUNT_ID
        )
    
    async def capture_snapshot(self) -> PortfolioSnapshot:
        """
        Capture current portfolio snapshot
        
        In production, this would fetch real prices from Webull API.
        For now, uses configured approximate prices.
        """
        positions = get_position_details()
        total_value = sum(Decimal(str(p['dollar_allocation'])) for p in positions)
        
        # Calculate daily change if we have previous snapshot
        daily_change = None
        if self.snapshots:
            prev = self.snapshots[-1]
            if prev.total_value > 0:
                daily_change = ((total_value - prev.total_value) / prev.total_value * 100).quantize(
                    Decimal("0.01"), rounding=ROUND_HALF_UP
                )
        
        snapshot = PortfolioSnapshot(
            timestamp=datetime.now(),
            total_value=total_value,
            positions=positions,
            daily_change_pct=daily_change,
            dividends_collected=self.total_dividends_collected,
            swarmgate_routed=self.total_swarmgate_routed,
        )
        
        self.snapshots.append(snapshot)
        self.current_capital = total_value
        
        logger.info(
            "portfolio_snapshot_captured",
            total_value=float(total_value),
            positions=len(positions),
            daily_change=float(daily_change) if daily_change else None
        )
        
        return snapshot
    
    def check_position_drift(self) -> List[PortfolioAlert]:
        """Check for position drift beyond threshold"""
        alerts = []
        summary = get_portfolio_summary()
        positions = get_position_details()
        
        for position in positions:
            # Calculate current allocation vs target
            target_pct = position['allocation_pct']
            current_value = Decimal(str(position['dollar_allocation']))
            current_pct = (current_value / self.current_capital * 100).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )
            
            drift = abs(current_pct - Decimal(str(target_pct)))
            
            if drift > self.drift_threshold_pct:
                alert = PortfolioAlert(
                    alert_type="drift",
                    severity="warning" if drift < Decimal("10") else "critical",
                    message=f"{position['ticker']} drift: {float(drift):.1f}% "
                           f"(target: {target_pct}%, current: {float(current_pct):.1f}%)",
                    timestamp=datetime.now(),
                    data={
                        "ticker": position['ticker'],
                        "target_pct": float(target_pct),
                        "current_pct": float(current_pct),
                        "drift_pct": float(drift),
                    }
                )
                alerts.append(alert)
                self.alerts.append(alert)
        
        return alerts
    
    def record_dividend(
        self,
        ticker: str,
        amount: Decimal,
        reinvested: bool = True,
        shares_purchased: Optional[Decimal] = None
    ) -> DividendPayment:
        """Record a dividend payment"""
        payment = DividendPayment(
            ticker=ticker,
            payment_date=date.today(),
            amount=amount,
            reinvested=reinvested,
            shares_purchased=shares_purchased,
        )
        
        self.dividends.append(payment)
        self.total_dividends_collected += amount
        
        # Create info alert
        alert = PortfolioAlert(
            alert_type="dividend",
            severity="info",
            message=f"Dividend received: {ticker} - ${float(amount):.2f}"
                   f"{' (DRIP)' if reinvested else ''}",
            timestamp=datetime.now(),
            data={"ticker": ticker, "amount": float(amount), "reinvested": reinvested}
        )
        self.alerts.append(alert)
        
        logger.info(
            "dividend_recorded",
            ticker=ticker,
            amount=float(amount),
            reinvested=reinvested,
            total_collected=float(self.total_dividends_collected)
        )
        
        return payment
    
    async def process_swarmgate(self, force: bool = False) -> Optional[Dict]:
        """
        Process SwarmGate monthly routing
        
        Args:
            force: Force execution regardless of day
        
        Returns:
            Transaction details if executed, None otherwise
        """
        if not force and not self.swarmgate.is_execution_day():
            return None
        
        # Execute routing
        transaction = await self.swarmgate.execute_routing(dry_run=False)
        self.total_swarmgate_routed += transaction.routing_amount
        
        # Create alert
        alert = PortfolioAlert(
            alert_type="swarmgate",
            severity="info",
            message=f"SwarmGate executed: ${float(transaction.routing_amount):.2f} routed",
            timestamp=datetime.now(),
            data=transaction.to_dict()
        )
        self.alerts.append(alert)
        
        return transaction.to_dict()
    
    def get_rebalance_recommendations(self) -> List[Dict]:
        """Generate rebalancing recommendations"""
        recommendations = []
        positions = get_position_details()
        
        for position in positions:
            target_pct = Decimal(str(position['allocation_pct']))
            current_value = Decimal(str(position['dollar_allocation']))
            current_pct = (current_value / self.current_capital * 100).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )
            
            drift = current_pct - target_pct
            
            if abs(drift) > self.drift_threshold_pct:
                action = "SELL" if drift > 0 else "BUY"
                adjustment_pct = abs(drift)
                adjustment_amt = (adjustment_pct / 100 * self.current_capital).quantize(
                    Decimal("0.01"), rounding=ROUND_HALF_UP
                )
                
                recommendations.append({
                    "ticker": position['ticker'],
                    "action": action,
                    "adjustment_pct": float(adjustment_pct),
                    "adjustment_amount": float(adjustment_amt),
                    "current_pct": float(current_pct),
                    "target_pct": float(target_pct),
                    "priority": "high" if abs(drift) > Decimal("10") else "medium",
                })
        
        return sorted(recommendations, key=lambda x: x['adjustment_pct'], reverse=True)
    
    def generate_nightly_report(self) -> Dict:
        """Generate comprehensive nightly report"""
        summary = get_portfolio_summary()
        positions = get_position_details()
        
        # Get latest snapshot
        latest_snapshot = self.snapshots[-1] if self.snapshots else None
        
        # Calculate performance metrics
        if latest_snapshot and self.initial_capital > 0:
            total_return_pct = (
                (latest_snapshot.total_value - self.initial_capital) / 
                self.initial_capital * 100
            ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        else:
            total_return_pct = Decimal("0")
        
        # Days since inception
        days_active = (datetime.now() - self.inception_date).days + 1
        
        return {
            "report_date": datetime.now().isoformat(),
            "report_type": "nightly_refinery",
            "portfolio_summary": {
                "total_value": float(self.current_capital),
                "initial_capital": float(self.initial_capital),
                "total_return_pct": float(total_return_pct),
                "days_active": days_active,
                "positions_count": len(positions),
            },
            "dividend_summary": {
                "total_collected": float(self.total_dividends_collected),
                "payments_count": len(self.dividends),
                "drip_enabled": DRIP_ENABLED,
                "projected_annual": float(summary['expected_annual_dividends']),
            },
            "swarmgate_summary": {
                "total_routed": float(self.total_swarmgate_routed),
                "monthly_amount": float(SWARMGATE.monthly_amount),
                "next_execution": self._get_next_execution_date().isoformat(),
            },
            "sector_allocation": summary['sector_breakdown'],
            "top_positions": [
                {
                    "ticker": p['ticker'],
                    "company": p['company'],
                    "allocation": p['allocation_pct'],
                    "value": p['dollar_allocation'],
                }
                for p in sorted(positions, key=lambda x: x['allocation_pct'], reverse=True)[:5]
            ],
            "alerts": [
                {
                    "type": a.alert_type,
                    "severity": a.severity,
                    "message": a.message,
                    "timestamp": a.timestamp.isoformat(),
                }
                for a in self.alerts[-10:]  # Last 10 alerts
            ],
            "rebalance_needed": len(self.get_rebalance_recommendations()) > 0,
            "health_status": self._calculate_health_status(),
        }
    
    def _get_next_execution_date(self) -> date:
        """Calculate next SwarmGate execution date"""
        today = date.today()
        if today.day < self.swarmgate.execution_day:
            return today.replace(day=self.swarmgate.execution_day)
        else:
            # Next month
            if today.month == 12:
                return date(today.year + 1, 1, self.swarmgate.execution_day)
            else:
                return date(today.year, today.month + 1, self.swarmgate.execution_day)
    
    def _calculate_health_status(self) -> str:
        """Calculate overall portfolio health status"""
        # Check for critical alerts
        critical_alerts = [a for a in self.alerts if a.severity == "critical"]
        if critical_alerts:
            return "critical"
        
        # Check for rebalancing needs
        rebalance = self.get_rebalance_recommendations()
        high_priority = [r for r in rebalance if r['priority'] == 'high']
        if high_priority:
            return "warning"
        
        # Check DRIP status
        if not DRIP_ENABLED:
            return "warning"
        
        return "healthy"
    
    async def run_nightly_cycle(self) -> Dict:
        """
        Run complete nightly monitoring cycle
        
        This is the main entry point for scheduled nightly execution.
        """
        logger.info("nightly_cycle_started")
        
        # 1. Capture portfolio snapshot
        snapshot = await self.capture_snapshot()
        
        # 2. Check for position drift
        drift_alerts = self.check_position_drift()
        
        # 3. Process SwarmGate if applicable
        swarmgate_result = await self.process_swarmgate()
        
        # 4. Generate report
        report = self.generate_nightly_report()
        
        logger.info(
            "nightly_cycle_completed",
            total_value=float(snapshot.total_value),
            alerts_generated=len(drift_alerts),
            swarmgate_executed=swarmgate_result is not None
        )
        
        return report
    
    def rescale(self, new_capital: Decimal) -> Dict:
        """
        Rescale portfolio to new capital amount
        
        Use when adding new capital:
        "Baby, new capital = $____"
        """
        old_capital = self.current_capital
        result = rescale_portfolio(new_capital)
        
        # Update internal state
        self.current_capital = new_capital
        self.swarmgate.update_capital(new_capital)
        
        # Create alert
        alert = PortfolioAlert(
            alert_type="rebalance",
            severity="info",
            message=f"Portfolio rescaled: ${float(old_capital):.2f} → ${float(new_capital):.2f}",
            timestamp=datetime.now(),
            data={
                "old_capital": float(old_capital),
                "new_capital": float(new_capital),
            }
        )
        self.alerts.append(alert)
        
        logger.info(
            "portfolio_rescaled",
            old_capital=float(old_capital),
            new_capital=float(new_capital)
        )
        
        return result


async def main():
    """Main entry point for CLI"""
    parser = argparse.ArgumentParser(
        description="Nightly Refinery - Portfolio Monitoring & Automation"
    )
    parser.add_argument(
        "--watch",
        action="store_true",
        help="Run in continuous watch mode"
    )
    parser.add_argument(
        "--report",
        action="store_true", 
        help="Generate and print nightly report"
    )
    parser.add_argument(
        "--rescale",
        type=float,
        metavar="AMOUNT",
        help="Rescale portfolio to new capital amount"
    )
    parser.add_argument(
        "--swarmgate",
        action="store_true",
        help="Force SwarmGate execution"
    )
    
    args = parser.parse_args()
    
    # Initialize refinery
    refinery = NightlyRefinery()
    
    if args.rescale:
        result = refinery.rescale(Decimal(str(args.rescale)))
        print(json.dumps(result, indent=2))
        return
    
    if args.swarmgate:
        result = await refinery.process_swarmgate(force=True)
        print(json.dumps(result, indent=2))
        return
    
    if args.report or not args.watch:
        # Run single cycle and report
        report = await refinery.run_nightly_cycle()
        
        print("=" * 60)
        print("NIGHTLY REFINERY REPORT")
        print("=" * 60)
        print(f"\n📅 Report Date: {report['report_date']}")
        
        ps = report['portfolio_summary']
        print(f"\n💰 Portfolio Value: ${ps['total_value']:.2f}")
        print(f"📈 Total Return: {ps['total_return_pct']:.2f}%")
        print(f"📊 Positions: {ps['positions_count']}")
        print(f"⏱️ Days Active: {ps['days_active']}")
        
        ds = report['dividend_summary']
        print(f"\n💵 Dividends Collected: ${ds['total_collected']:.2f}")
        print(f"📈 Projected Annual: ${ds['projected_annual']:.2f}")
        print(f"🔄 DRIP Enabled: {ds['drip_enabled']}")
        
        sg = report['swarmgate_summary']
        print(f"\n🔀 SwarmGate Routed: ${sg['total_routed']:.2f}")
        print(f"📅 Next Execution: {sg['next_execution']}")
        
        print(f"\n🏥 Health Status: {report['health_status'].upper()}")
        
        if report['rebalance_needed']:
            print("\n⚠️ Rebalancing Recommended")
        
        print("\n" + "=" * 60)
        return
    
    if args.watch:
        print("Starting continuous watch mode...")
        print("Press Ctrl+C to stop")
        
        while True:
            await refinery.run_nightly_cycle()
            # Sleep until next cycle (run every 6 hours in watch mode)
            await asyncio.sleep(6 * 60 * 60)


if __name__ == "__main__":
    asyncio.run(main())

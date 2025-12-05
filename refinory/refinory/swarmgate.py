"""
SwarmGate - 7% Monthly Capital Routing Automation
Strategickhaos Hybrid Refinery Financial Architecture

This module implements the SwarmGate routing system that automatically
allocates 7% of portfolio capital monthly according to the Mixed (D) strategy:
- T-Bills / Money-market: Emergency brake at ~5.3% yield
- AI-Fuel: Agents, backtests, GPU time
- Crypto Reserve: 50/50 BTC/ETH cold storage (lottery ticket)
"""

import asyncio
from dataclasses import dataclass, field
from datetime import datetime, date
from decimal import Decimal, ROUND_HALF_UP
from enum import Enum
from typing import Dict, List, Optional, Callable, Any
import json
import structlog

logger = structlog.get_logger()


class AllocationBucket(Enum):
    """SwarmGate allocation buckets"""
    TBILL_MONEY_MARKET = "tbill_money_market"
    AI_FUEL = "ai_fuel"
    CRYPTO_RESERVE = "crypto_reserve"


class CryptoAsset(Enum):
    """Crypto assets for reserve"""
    BTC = "bitcoin"
    ETH = "ethereum"


@dataclass
class AllocationRule:
    """Single allocation rule within SwarmGate"""
    bucket: AllocationBucket
    percentage: Decimal
    description: str
    auto_execute: bool = True
    
    def calculate_amount(self, total_routing: Decimal) -> Decimal:
        """Calculate dollar amount for this allocation"""
        return (self.percentage / 100 * total_routing).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )


@dataclass
class SwarmGateTransaction:
    """Record of a SwarmGate routing transaction"""
    transaction_id: str
    execution_date: datetime
    total_capital: Decimal
    routing_amount: Decimal
    allocations: Dict[str, Decimal]
    status: str = "pending"
    execution_notes: Optional[str] = None
    
    def to_dict(self) -> Dict:
        return {
            "transaction_id": self.transaction_id,
            "execution_date": self.execution_date.isoformat(),
            "total_capital": float(self.total_capital),
            "routing_amount": float(self.routing_amount),
            "allocations": {k: float(v) for k, v in self.allocations.items()},
            "status": self.status,
            "execution_notes": self.execution_notes,
        }


class SwarmGateRouter:
    """
    SwarmGate 7% Monthly Capital Routing Engine
    
    The SwarmGate automates monthly capital allocation according to
    the Mixed (D) strategy, routing 7% of portfolio capital into:
    
    1. T-Bills / Money-market (~57%): Emergency brake, ~5.3% yield
    2. AI-Fuel (~29%): Feed agents, backtests, GPU time
    3. Crypto Reserve (~14%): 50/50 BTC/ETH cold storage
    
    This creates a balanced approach between safety, growth, and
    high-risk/high-reward asymmetric bets.
    """
    
    def __init__(
        self,
        total_capital: Decimal,
        routing_percentage: Decimal = Decimal("7.0"),
        execution_day: int = 1
    ):
        """
        Initialize SwarmGate Router
        
        Args:
            total_capital: Current portfolio total value
            routing_percentage: Percentage to route monthly (default 7%)
            execution_day: Day of month to execute (default 1st)
        """
        self.total_capital = total_capital
        self.routing_percentage = routing_percentage
        self.execution_day = execution_day
        self.transaction_history: List[SwarmGateTransaction] = []
        
        # Define allocation rules for Mixed (D) strategy
        self.allocation_rules: List[AllocationRule] = [
            AllocationRule(
                bucket=AllocationBucket.TBILL_MONEY_MARKET,
                percentage=Decimal("57.14"),  # $20.80 of $36.40
                description="T-Bills/Money-market - Emergency brake at ~5.3% APY",
                auto_execute=True,
            ),
            AllocationRule(
                bucket=AllocationBucket.AI_FUEL,
                percentage=Decimal("28.57"),  # $10.40 of $36.40
                description="AI-Fuel - Agents, backtests, GPU time",
                auto_execute=True,
            ),
            AllocationRule(
                bucket=AllocationBucket.CRYPTO_RESERVE,
                percentage=Decimal("14.29"),  # $5.20 of $36.40
                description="Crypto Reserve - 50/50 BTC/ETH cold storage (lottery ticket)",
                auto_execute=True,
            ),
        ]
        
        # Crypto split within reserve
        self.crypto_split = {
            CryptoAsset.BTC: Decimal("50.0"),
            CryptoAsset.ETH: Decimal("50.0"),
        }
    
    @property
    def monthly_routing_amount(self) -> Decimal:
        """Calculate monthly routing amount"""
        return (self.routing_percentage / 100 * self.total_capital).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
    
    def calculate_allocations(self) -> Dict[str, Decimal]:
        """Calculate all bucket allocations"""
        routing_amount = self.monthly_routing_amount
        allocations = {}
        
        for rule in self.allocation_rules:
            amount = rule.calculate_amount(routing_amount)
            allocations[rule.bucket.value] = amount
        
        return allocations
    
    def calculate_crypto_split(self) -> Dict[str, Decimal]:
        """Calculate BTC/ETH split within crypto reserve"""
        crypto_total = self.calculate_allocations().get(
            AllocationBucket.CRYPTO_RESERVE.value, Decimal("0")
        )
        
        return {
            asset.value: (pct / 100 * crypto_total).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )
            for asset, pct in self.crypto_split.items()
        }
    
    def is_execution_day(self, check_date: Optional[date] = None) -> bool:
        """Check if given date is execution day"""
        check = check_date or date.today()
        return check.day == self.execution_day
    
    async def execute_routing(
        self,
        dry_run: bool = False,
        execution_callbacks: Optional[Dict[str, Callable]] = None
    ) -> SwarmGateTransaction:
        """
        Execute monthly SwarmGate routing
        
        Args:
            dry_run: If True, simulate without executing
            execution_callbacks: Optional callbacks for each bucket execution
        
        Returns:
            SwarmGateTransaction record
        """
        logger.info(
            "executing_swarmgate_routing",
            total_capital=float(self.total_capital),
            routing_amount=float(self.monthly_routing_amount),
            dry_run=dry_run
        )
        
        allocations = self.calculate_allocations()
        
        transaction = SwarmGateTransaction(
            transaction_id=f"swarmgate-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            execution_date=datetime.now(),
            total_capital=self.total_capital,
            routing_amount=self.monthly_routing_amount,
            allocations=allocations,
            status="dry_run" if dry_run else "executing",
        )
        
        if not dry_run:
            execution_notes = []
            
            for rule in self.allocation_rules:
                bucket_name = rule.bucket.value
                amount = allocations[bucket_name]
                
                if execution_callbacks and bucket_name in execution_callbacks:
                    try:
                        result = await execution_callbacks[bucket_name](amount)
                        execution_notes.append(f"{bucket_name}: Success - {result}")
                    except Exception as e:
                        execution_notes.append(f"{bucket_name}: Failed - {str(e)}")
                        logger.error(
                            "swarmgate_bucket_execution_failed",
                            bucket=bucket_name,
                            error=str(e)
                        )
                else:
                    execution_notes.append(
                        f"{bucket_name}: ${float(amount):.2f} - Manual execution required"
                    )
            
            transaction.execution_notes = "; ".join(execution_notes)
            transaction.status = "completed"
        
        self.transaction_history.append(transaction)
        
        logger.info(
            "swarmgate_routing_complete",
            transaction_id=transaction.transaction_id,
            status=transaction.status
        )
        
        return transaction
    
    def update_capital(self, new_capital: Decimal):
        """
        Update total capital for rescaling
        
        Use this when adding new capital:
        "Baby, new capital = $____"
        """
        old_capital = self.total_capital
        self.total_capital = new_capital
        
        logger.info(
            "capital_updated",
            old_capital=float(old_capital),
            new_capital=float(new_capital),
            new_monthly_routing=float(self.monthly_routing_amount)
        )
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate SwarmGate status report"""
        allocations = self.calculate_allocations()
        crypto_split = self.calculate_crypto_split()
        
        return {
            "swarmgate_status": "active",
            "total_capital": float(self.total_capital),
            "routing_percentage": float(self.routing_percentage),
            "monthly_routing_amount": float(self.monthly_routing_amount),
            "execution_day": self.execution_day,
            "allocations": {
                "tbill_money_market": {
                    "amount": float(allocations[AllocationBucket.TBILL_MONEY_MARKET.value]),
                    "description": "Emergency brake - ~5.3% APY",
                },
                "ai_fuel": {
                    "amount": float(allocations[AllocationBucket.AI_FUEL.value]),
                    "description": "Agents, backtests, GPU time",
                },
                "crypto_reserve": {
                    "amount": float(allocations[AllocationBucket.CRYPTO_RESERVE.value]),
                    "description": "50/50 BTC/ETH cold storage",
                    "split": {
                        "btc": float(crypto_split[CryptoAsset.BTC.value]),
                        "eth": float(crypto_split[CryptoAsset.ETH.value]),
                    },
                },
            },
            "annual_projection": {
                "total_routed": float(self.monthly_routing_amount * 12),
                "tbill_yield_estimate": float(
                    allocations[AllocationBucket.TBILL_MONEY_MARKET.value] * 12 * Decimal("0.053")
                ),
            },
            "transaction_history_count": len(self.transaction_history),
        }


class SwarmGateScheduler:
    """
    Scheduler for automated SwarmGate execution
    
    Handles the automatic execution of SwarmGate routing on the 1st
    of every month, with proper tracking and notification.
    """
    
    def __init__(self, router: SwarmGateRouter):
        self.router = router
        self.running = False
        self._task: Optional[asyncio.Task] = None
    
    async def start(self):
        """Start the scheduler"""
        self.running = True
        logger.info("swarmgate_scheduler_started")
        
        while self.running:
            now = datetime.now()
            
            if self.router.is_execution_day():
                # Check if we haven't already executed today
                last_tx = (
                    self.router.transaction_history[-1]
                    if self.router.transaction_history
                    else None
                )
                
                if not last_tx or last_tx.execution_date.date() != now.date():
                    logger.info("swarmgate_execution_triggered")
                    await self.router.execute_routing(dry_run=False)
            
            # Sleep until next check (check every hour)
            await asyncio.sleep(3600)
    
    async def stop(self):
        """Stop the scheduler"""
        self.running = False
        if self._task:
            self._task.cancel()
        logger.info("swarmgate_scheduler_stopped")


# Default instance with $520 capital
def create_default_swarmgate() -> SwarmGateRouter:
    """Create SwarmGate router with default $520 capital"""
    return SwarmGateRouter(
        total_capital=Decimal("520.00"),
        routing_percentage=Decimal("7.0"),
        execution_day=1
    )


if __name__ == "__main__":
    import asyncio
    
    print("=" * 60)
    print("SWARMGATE - 7% MONTHLY CAPITAL ROUTING")
    print("=" * 60)
    
    # Create default router
    router = create_default_swarmgate()
    
    # Generate report
    report = router.generate_report()
    
    print(f"\n💰 Total Capital: ${report['total_capital']:.2f}")
    print(f"📊 Monthly Routing: ${report['monthly_routing_amount']:.2f} ({report['routing_percentage']}%)")
    print(f"📅 Execution Day: {report['execution_day']}st of each month")
    
    print("\n📦 Allocation Breakdown:")
    print("-" * 40)
    
    allocs = report['allocations']
    print(f"   T-Bills/Money-market: ${allocs['tbill_money_market']['amount']:.2f}")
    print(f"      → {allocs['tbill_money_market']['description']}")
    
    print(f"   AI-Fuel: ${allocs['ai_fuel']['amount']:.2f}")
    print(f"      → {allocs['ai_fuel']['description']}")
    
    crypto = allocs['crypto_reserve']
    print(f"   Crypto Reserve: ${crypto['amount']:.2f}")
    print(f"      → BTC: ${crypto['split']['btc']:.2f}")
    print(f"      → ETH: ${crypto['split']['eth']:.2f}")
    
    print("\n📈 Annual Projection:")
    print(f"   Total Routed: ${report['annual_projection']['total_routed']:.2f}")
    print(f"   T-Bill Yield Est: ${report['annual_projection']['tbill_yield_estimate']:.2f}")
    
    # Simulate dry run
    print("\n🔄 Simulating Monthly Routing (Dry Run)...")
    
    async def simulate():
        tx = await router.execute_routing(dry_run=True)
        print(f"\n✅ Transaction ID: {tx.transaction_id}")
        print(f"   Status: {tx.status}")
        print(f"   Routing Amount: ${float(tx.routing_amount):.2f}")
        for bucket, amount in tx.allocations.items():
            print(f"   {bucket}: ${amount:.2f}")
    
    asyncio.run(simulate())
    
    print("\n" + "=" * 60)
    print("SwarmGate Active - Set recurring $36.40 transfer on the 1st")
    print("=" * 60)

"""
SwarmGate Integration - NATS-powered event bridge for ValorYield Engine

Handles:
- Paycheck detection and 7% auto-allocation
- Treasury allocation events
- Dialectical rebalancing (Hegel-approved: thesis + antithesis = synthesis)
"""
import asyncio
import json
import os
from datetime import datetime


class SwarmGateIntegration:
    """
    SwarmGate bridge connecting paycheck detection to portfolio management.
    Uses NATS pub/sub for async event processing.
    """
    
    def __init__(self, nats_url: str = None):
        self.nats_url = nats_url or os.getenv("NATS_URL", "nats://localhost:4222")
        self.nc = None
        self.target_allocation = {
            "stocks": 0.4,
            "crypto": 0.3,
            "futures": 0.3
        }
        
    async def connect(self):
        """Connect to NATS server and subscribe to events"""
        try:
            from nats.aio.client import Client as NATS
            self.nc = NATS()
            await self.nc.connect(self.nats_url)
            print(f"✅ Connected to NATS at {self.nats_url}")
            
            # Subscribe to sovereign events
            await self.nc.subscribe("swarmgate.paycheck.detected", cb=self.handle_paycheck)
            await self.nc.subscribe("swarmgate.treasury.allocated", cb=self.handle_allocation)
            await self.nc.subscribe("legion.rebalance.trigger", cb=self.dialectical_rebalance)
            
            print("📡 Subscribed to SwarmGate events")
        except ImportError:
            print("⚠️ nats-py not installed. Running in mock mode.")
            print("   Install with: pip install nats-py")
        except Exception as e:
            print(f"⚠️ NATS connection failed: {e}. Running in mock mode.")
    
    async def handle_paycheck(self, msg):
        """
        Process detected paycheck and allocate 7% to treasury.
        
        This is the sovereign automation - no middlemen extracting fees.
        """
        try:
            data = json.loads(msg.data.decode())
            amount = data.get('amount', 0)
            paycheck_id = data.get('id', 'unknown')
            
            # Calculate 7% allocation (configurable via flow.yaml)
            allocation_7pct = amount * 0.07
            
            # Publish to portfolio deposit topic
            if self.nc:
                await self.nc.publish("valoryield.deposit", json.dumps({
                    "amount": allocation_7pct,
                    "source": "swarmgate_7%",
                    "paycheck_id": paycheck_id,
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                }).encode())
            
            print(f"💰 Sovereign allocation: ${allocation_7pct:.2f} → Portfolio API")
            print(f"   Paycheck ID: {paycheck_id}")
            print(f"   Original amount: ${amount:.2f}")
            
            # In production: POST to /api/v1/transactions for persistence
            
        except Exception as e:
            print(f"❌ Error processing paycheck: {e}")
            
    async def handle_allocation(self, msg):
        """
        Process treasury allocation and trigger Legion analysis.
        
        The AI Legion (Claude, Grok, GPT) provides dialectical investment advice.
        """
        try:
            data = json.loads(msg.data.decode())
            new_balance = data.get('new_balance', 0)
            
            # Publish to Legion for multi-AI analysis
            if self.nc:
                await self.nc.publish("legion.portfolio.analyze", json.dumps({
                    "new_balance": new_balance,
                    "trigger": "treasury_allocation",
                    "ai_agents": ["Claude_risk", "Grok_patterns", "GPT_market"],
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                }).encode())
            
            print(f"🤖 Legion analysis triggered for balance: ${new_balance:.2f}")
            
        except Exception as e:
            print(f"❌ Error handling allocation: {e}")
            
    async def dialectical_rebalance(self, msg):
        """
        Dialectical Rebalancer - Hegel-approved synthesis.
        
        - Thesis: current portfolio positions
        - Antithesis: target allocation
        - Synthesis: trades to execute
        
        This is sovereign wealth management - YOUR rules, YOUR algorithm.
        """
        try:
            data = json.loads(msg.data.decode())
            current_positions = data.get('current_positions', {})
            balance = data.get('balance', 0)
            
            trades = []
            
            # Calculate drift from target and generate trades
            for asset, target_weight in self.target_allocation.items():
                current_weight = current_positions.get(asset, 0)
                drift = abs(current_weight - target_weight)
                
                if drift > 0.05:  # 5% drift threshold
                    if current_weight < target_weight:
                        action = "buy"
                        trade_amount = (target_weight - current_weight) * balance
                    else:
                        action = "sell"
                        trade_amount = (current_weight - target_weight) * balance
                    
                    trades.append({
                        "asset": asset,
                        "action": action,
                        "amount": trade_amount,
                        "drift_pct": drift * 100
                    })
            
            # Execute trades (stub - add real API calls in production)
            for trade in trades:
                print(f"⚖️ Synthesis trade: {trade['action'].upper()} ${trade['amount']:.2f} of {trade['asset']}")
                # Real implementations:
                # - kraken_client.add_order(...) for crypto
                # - nt_client.submit_order(...) for futures
                # - alpaca_client.submit_order(...) for stocks
            
            # Publish rebalance complete event
            if self.nc:
                await self.nc.publish("valoryield.rebalanced", json.dumps({
                    "trades": trades,
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                }).encode())
            
            if trades:
                print(f"✅ Rebalanced portfolio with {len(trades)} trades")
            else:
                print("😎 Portfolio within tolerance - no trades needed")
            
        except Exception as e:
            print(f"❌ Error in dialectical rebalance: {e}")
    
    async def simulate_paycheck(self, amount: float, paycheck_id: str = None):
        """Simulate a paycheck event for testing"""
        if not paycheck_id:
            paycheck_id = f"pay_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        print(f"\n📨 Simulating paycheck: ${amount:.2f} (ID: {paycheck_id})")
        
        # Create mock message
        class MockMsg:
            def __init__(self, data):
                self.data = data.encode()
        
        await self.handle_paycheck(MockMsg(json.dumps({
            "amount": amount,
            "id": paycheck_id
        })))


async def main():
    """Main entry point for SwarmGate integration"""
    print("=" * 60)
    print("🔥 SwarmGate Integration - ValorYield Engine")
    print("   Sovereign Wealth Automation - No Middlemen, No Fees")
    print("=" * 60)
    
    sg = SwarmGateIntegration()
    await sg.connect()
    
    # Demo: Simulate a paycheck
    await sg.simulate_paycheck(1000.00, "pay_demo_001")
    
    # Keep running for event processing
    print("\n🎯 SwarmGate running. Waiting for events...")
    print("   Press Ctrl+C to stop")
    
    try:
        await asyncio.Future()  # Run forever
    except KeyboardInterrupt:
        print("\n👋 SwarmGate shutting down...")


if __name__ == "__main__":
    asyncio.run(main())

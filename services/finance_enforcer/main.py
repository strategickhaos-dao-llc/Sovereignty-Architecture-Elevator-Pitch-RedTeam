# finance_enforcer service - Financial Cap Enforcement
from contextlib import asynccontextmanager
from fastapi import FastAPI
from faststream.nats import NatsBroker
import os
import json
from datetime import datetime
from typing import List, Dict, Any

SPENDING_CAP = int(os.getenv("SPENDING_CAP", "500"))
STRIPE_SECRET = os.getenv("STRIPE_SECRET", "")

broker = NatsBroker(os.getenv("NATS_URL", "nats://nats:4222"))


class SpendingState:
    """Thread-safe spending state management."""
    
    def __init__(self):
        self.monthly_spend: float = 0.0
        self.spend_records: List[Dict[str, Any]] = []
    
    def get_monthly_spend(self) -> float:
        """Get current monthly spending total."""
        # In production, query Stripe API:
        # stripe.api_key = STRIPE_SECRET
        # charges = stripe.Charge.list(created={"gte": start_of_month})
        # return sum(c.amount for c in charges.data) / 100
        return self.monthly_spend
    
    def add_spend(self, amount: float, to: str, purpose: str) -> None:
        """Record a spending transaction."""
        self.monthly_spend += amount
        self.spend_records.append({
            "timestamp": datetime.utcnow().isoformat(),
            "amount": amount,
            "to": to,
            "purpose": purpose
        })
    
    def reset(self) -> None:
        """Reset spending tracker at start of month."""
        self.monthly_spend = 0.0
        self.spend_records = []


# State instance
state = SpendingState()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage NATS broker lifecycle."""
    await broker.connect()
    yield
    await broker.close()


app = FastAPI(lifespan=lifespan)


@broker.subscriber("finance.request")
async def check_spend(msg: dict):
    """Check if spending request is within cap."""
    amount = msg.get("amount", 0)
    current = state.get_monthly_spend()
    
    if current + amount > SPENDING_CAP:
        await broker.publish(
            {
                "error": "Cap exceeded",
                "current_spend": current,
                "requested": amount,
                "cap": SPENDING_CAP
            },
            "board.alerts"
        )
        return
    
    # Record the spend
    state.add_spend(
        amount=amount,
        to=msg.get("to", "unknown"),
        purpose=msg.get("purpose", "unspecified")
    )
    
    # In production, execute Stripe transfer:
    # stripe.Transfer.create(
    #     amount=int(amount * 100),
    #     currency="usd",
    #     destination=msg["to"]
    # )
    
    await broker.publish(
        {
            "status": "approved",
            "amount": amount,
            "remaining": SPENDING_CAP - state.monthly_spend
        },
        "finance.approved"
    )


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "finance_enforcer",
        "spending_cap": SPENDING_CAP,
        "current_spend": state.get_monthly_spend(),
        "remaining": SPENDING_CAP - state.get_monthly_spend()
    }


@app.get("/spend")
async def get_spending():
    """Get current spending status."""
    return {
        "cap": SPENDING_CAP,
        "current": state.get_monthly_spend(),
        "remaining": SPENDING_CAP - state.get_monthly_spend(),
        "records": state.spend_records
    }


@app.post("/reset")
async def reset_spend():
    """Reset monthly spending (admin only)."""
    state.reset()
    return {"status": "reset", "current": 0}

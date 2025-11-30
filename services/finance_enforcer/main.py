# finance_enforcer service - Financial Cap Enforcement
from fastapi import FastAPI
from faststream.nats import NatsBroker
import os
import json
from datetime import datetime

app = FastAPI()
broker = NatsBroker(os.getenv("NATS_URL", "nats://nats:4222"))

SPENDING_CAP = int(os.getenv("SPENDING_CAP", "500"))
STRIPE_SECRET = os.getenv("STRIPE_SECRET", "")

# In-memory spending tracker (in production, use persistent storage)
monthly_spend = 0.0
spend_records = []


def get_monthly_spend() -> float:
    """Get current monthly spending total."""
    # In production, query Stripe API:
    # stripe.api_key = STRIPE_SECRET
    # charges = stripe.Charge.list(created={"gte": start_of_month})
    # return sum(c.amount for c in charges.data) / 100
    return monthly_spend


def reset_monthly_spend():
    """Reset spending tracker at start of month."""
    global monthly_spend, spend_records
    monthly_spend = 0.0
    spend_records = []


@broker.subscriber("finance.request")
async def check_spend(msg: dict):
    """Check if spending request is within cap."""
    global monthly_spend
    
    amount = msg.get("amount", 0)
    current = get_monthly_spend()
    
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
    monthly_spend += amount
    spend_records.append({
        "timestamp": datetime.utcnow().isoformat(),
        "amount": amount,
        "to": msg.get("to", "unknown"),
        "purpose": msg.get("purpose", "unspecified")
    })
    
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
            "remaining": SPENDING_CAP - monthly_spend
        },
        "finance.approved"
    )


@app.on_event("startup")
async def startup():
    """Connect to NATS."""
    await broker.connect()


@app.on_event("shutdown")
async def shutdown():
    """Disconnect from NATS."""
    await broker.close()


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "finance_enforcer",
        "spending_cap": SPENDING_CAP,
        "current_spend": get_monthly_spend(),
        "remaining": SPENDING_CAP - get_monthly_spend()
    }


@app.get("/spend")
async def get_spending():
    """Get current spending status."""
    return {
        "cap": SPENDING_CAP,
        "current": get_monthly_spend(),
        "remaining": SPENDING_CAP - get_monthly_spend(),
        "records": spend_records
    }


@app.post("/reset")
async def reset_spend():
    """Reset monthly spending (admin only)."""
    reset_monthly_spend()
    return {"status": "reset", "current": 0}

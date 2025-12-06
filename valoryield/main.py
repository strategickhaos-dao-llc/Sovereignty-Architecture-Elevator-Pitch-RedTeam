"""
ValorYield Engine - Sovereign Wealth Platform

FastAPI backend for the ValorYield Engine with 100% sovereignty.
Integrates with SwarmGate for automated 7% allocation deposits.
"""

import os
import threading

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(
    title="ValorYield Engine",
    description="Sovereign wealth platform - 100% sovereignty, zero intermediaries",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS configuration
# In production, restrict to specific trusted domains
ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "*"  # Development default, override in production
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Data models
class DepositRequest(BaseModel):
    """Request model for SwarmGate deposit."""

    amount: float


class PortfolioResponse(BaseModel):
    """Response model for portfolio information."""

    balance: float
    account: str
    allocation: str
    vs_moneylion: str


class SwarmGateResponse(BaseModel):
    """Response model for SwarmGate deposit."""

    deposited: float
    new_balance: float
    trigger: str


# Thread-safe portfolio state
# In production, replace with proper database (PostgreSQL, Redis, etc.)
class PortfolioState:
    """Thread-safe portfolio state manager."""

    def __init__(self):
        self._lock = threading.Lock()
        self._data = {"balance": 207.69, "account": "2143", "allocation": "Aggressive Mix"}

    def get(self, key: str):
        with self._lock:
            return self._data.get(key)

    def get_all(self) -> dict:
        with self._lock:
            return self._data.copy()

    def update_balance(self, amount: float) -> float:
        with self._lock:
            self._data["balance"] += amount
            return self._data["balance"]


PORTFOLIO = PortfolioState()


@app.get("/")
def root():
    """Root endpoint with system status."""
    return {
        "name": "ValorYield Engine",
        "status": "operational",
        "balance": PORTFOLIO.get("balance"),
        "sovereignty": "100%",
        "version": "1.0.0",
    }


@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "healthy", "service": "valoryield-engine"}


@app.get("/api/v1/portfolio", response_model=PortfolioResponse)
def get_portfolio():
    """Get current portfolio information."""
    portfolio_data = PORTFOLIO.get_all()
    return {
        "balance": portfolio_data["balance"],
        "account": portfolio_data["account"],
        "allocation": portfolio_data["allocation"],
        "vs_moneylion": "173% fee savings",
    }


@app.post("/api/v1/swarmgate/deposit", response_model=SwarmGateResponse)
def swarmgate_deposit(request: DepositRequest):
    """
    Receive 7% allocation from SwarmGate.

    This endpoint is called by the SwarmGate system to deposit
    funds from trading profits into the ValorYield Engine.
    """
    new_balance = PORTFOLIO.update_balance(request.amount)

    return {
        "deposited": request.amount,
        "new_balance": new_balance,
        "trigger": "rebalance_queued",
    }


@app.get("/api/v1/allocations")
def get_allocations():
    """Get current asset allocations."""
    return {
        "allocations": [
            {"asset": "US Total Market", "percentage": 40, "type": "equity"},
            {"asset": "International", "percentage": 20, "type": "equity"},
            {"asset": "Bonds", "percentage": 20, "type": "fixed_income"},
            {"asset": "Real Estate", "percentage": 10, "type": "alternatives"},
            {"asset": "Crypto", "percentage": 10, "type": "alternatives"},
        ],
        "rebalance_threshold": 5.0,
        "last_rebalance": "2024-01-15T00:00:00Z",
    }


@app.get("/api/v1/stats")
def get_stats():
    """Get platform statistics."""
    return {
        "total_users": 1,  # Just the sovereign for now
        "total_aum": PORTFOLIO.get("balance"),
        "fee_savings_vs_traditional": "173%",
        "sovereignty_level": "100%",
        "intermediaries": 0,
        "entity": {
            "type": "501(c)(3)",
            "ein": "39-2923503",
            "name": "StrategicKhaos DAO LLC / ValorYield Engine",
        },
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)

"""
ValorYield Engine - Sovereign Wealth Platform API
Production-ready version with proper error handling and mock data
Built for Strategickhaos Swarm Intelligence
"""

import logging
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("valoryield")


# Pydantic Models
class Portfolio(BaseModel):
    """Portfolio balance and allocation information"""
    balance: float = Field(..., description="Current portfolio balance")
    account: str = Field(..., description="Account identifier (last 4 digits)")
    allocation: str = Field(..., description="Current allocation strategy")
    last_updated: str = Field(..., description="ISO timestamp of last update")
    vs_moneylion: str = Field(..., description="Fee savings vs MoneyLion")


class Transaction(BaseModel):
    """Transaction record"""
    date: str = Field(..., description="Transaction date")
    type: str = Field(..., description="Transaction type (deposit/withdrawal)")
    amount: float = Field(..., description="Transaction amount")
    source: str = Field(..., description="Transaction source")


class TransactionsResponse(BaseModel):
    """Transaction list response"""
    transactions: List[Transaction]
    total: int


class DepositResponse(BaseModel):
    """Response for deposit operation"""
    deposited: float
    new_balance: float
    status: str
    trigger: str


class RebalanceResponse(BaseModel):
    """Response for rebalance operation"""
    status: str
    message: str
    drift: float
    threshold: float = 5.0


class StatsResponse(BaseModel):
    """Platform statistics"""
    total_balance: float
    total_transactions: int
    swarmgate_deposits: float
    sovereignty_score: int
    vs_moneylion: dict


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    timestamp: str


class RootResponse(BaseModel):
    """Root endpoint response"""
    name: str
    status: str
    sovereignty: str
    balance: float
    mission: str
    vs_moneylion: dict


# In-memory data store (mock data - replace with database in production)
class DataStore:
    """In-memory data store for mock data"""
    
    def __init__(self):
        self.portfolio = {
            "balance": 207.69,
            "account": "2143",
            "allocation": "Aggressive Mix",
            "vs_moneylion": "173% fee savings"
        }
        self.transactions: List[dict] = [
            {
                "date": "2025-12-01",
                "type": "deposit",
                "amount": 50.00,
                "source": "swarmgate_7%"
            },
            {
                "date": "2025-11-28",
                "type": "deposit",
                "amount": 35.00,
                "source": "swarmgate_7%"
            }
        ]


# Global data store instance
data_store = DataStore()


# FastAPI lifespan management
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    logger.info("Starting ValorYield Engine")
    logger.info(f"Initial balance: ${data_store.portfolio['balance']:.2f}")
    yield
    logger.info("Shutting down ValorYield Engine")


# Create FastAPI application
app = FastAPI(
    title="ValorYield Engine",
    description="Sovereign wealth platform - 100% open source, zero fees, full control",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Add CORS middleware for Codespaces and cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Endpoints
@app.get("/", response_model=RootResponse)
def root():
    """Health check and platform info"""
    try:
        return RootResponse(
            name="ValorYield Engine",
            status="operational",
            sovereignty="100%",
            balance=data_store.portfolio["balance"],
            mission="Democratize wealth-building through open-source infrastructure",
            vs_moneylion={
                "their_fees": "$360/year",
                "our_fees": "$0/year",
                "savings": "100%"
            }
        )
    except Exception as e:
        logger.error(f"Error in root endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/api/v1/health", response_model=HealthResponse)
def health():
    """Kubernetes health check endpoint"""
    try:
        return HealthResponse(
            status="healthy",
            timestamp=datetime.now(timezone.utc).isoformat()
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail="Health check failed")


@app.get("/api/v1/portfolio", response_model=Portfolio)
def get_portfolio():
    """
    Get portfolio balance from all sources.
    
    In production, this would aggregate data from:
    - Thread Bank for cash balance
    - Kraken Pro for crypto holdings
    - NinjaTrader for futures/options
    - Fidelity for stocks (CSV import for now)
    """
    try:
        portfolio = data_store.portfolio.copy()
        portfolio["last_updated"] = datetime.now(timezone.utc).isoformat()
        
        return Portfolio(**portfolio)
    except Exception as e:
        logger.error(f"Error fetching portfolio: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch portfolio")


@app.get("/api/v1/transactions", response_model=TransactionsResponse)
def get_transactions(
    limit: int = Query(default=10, ge=1, le=100, description="Number of transactions to return")
):
    """Get transaction history"""
    try:
        transactions = data_store.transactions[:limit]
        
        return TransactionsResponse(
            transactions=[Transaction(**t) for t in transactions],
            total=len(data_store.transactions)
        )
    except Exception as e:
        logger.error(f"Error fetching transactions: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch transactions")


@app.post("/api/v1/deposit", response_model=DepositResponse)
def swarmgate_deposit(
    amount: float = Query(..., gt=0, description="Amount to deposit (must be positive)")
):
    """
    Receive deposit from SwarmGate 7% protocol.
    
    This endpoint handles incoming deposits from the SwarmGate yield protocol
    and updates the portfolio balance accordingly.
    """
    try:
        if amount <= 0:
            raise HTTPException(status_code=400, detail="Amount must be positive")
        
        # Update balance
        data_store.portfolio["balance"] += amount
        
        # Record transaction
        data_store.transactions.insert(0, {
            "date": datetime.now(timezone.utc).isoformat(),
            "type": "deposit",
            "amount": amount,
            "source": "swarmgate_7%"
        })
        
        logger.info(f"Deposit received: ${amount:.2f}, new balance: ${data_store.portfolio['balance']:.2f}")
        
        return DepositResponse(
            deposited=amount,
            new_balance=data_store.portfolio["balance"],
            status="success",
            trigger="rebalance_queued"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing deposit: {e}")
        raise HTTPException(status_code=500, detail="Failed to process deposit")


@app.post("/api/v1/rebalance", response_model=RebalanceResponse)
def trigger_rebalance(
    drift: float = Query(default=0, ge=0, description="Current drift percentage")
):
    """
    Trigger portfolio rebalancing.
    
    Rebalancing is triggered when the portfolio drift exceeds the 5% threshold.
    In production, this publishes to NATS for Legion to process.
    """
    try:
        threshold = 5.0
        
        if drift > threshold:
            # In production, this would publish to NATS:
            # nc.publish("legion.rebalance.trigger", {...})
            
            logger.info(f"Rebalance triggered: drift {drift}% exceeds threshold {threshold}%")
            
            return RebalanceResponse(
                status="triggered",
                message="Legion analyzing portfolio",
                drift=drift,
                threshold=threshold
            )
        
        return RebalanceResponse(
            status="skipped",
            message=f"Drift {drift}% below {threshold}% threshold",
            drift=drift,
            threshold=threshold
        )
    except Exception as e:
        logger.error(f"Error triggering rebalance: {e}")
        raise HTTPException(status_code=500, detail="Failed to trigger rebalance")


@app.get("/api/v1/stats", response_model=StatsResponse)
def get_stats():
    """Get platform statistics"""
    try:
        swarmgate_deposits = sum(
            t["amount"] for t in data_store.transactions 
            if t.get("source") == "swarmgate_7%"
        )
        
        return StatsResponse(
            total_balance=data_store.portfolio["balance"],
            total_transactions=len(data_store.transactions),
            swarmgate_deposits=swarmgate_deposits,
            sovereignty_score=100,
            vs_moneylion={
                "fee_savings": 360.00,
                "control": "100% yours vs. 0% theirs",
                "transparency": "Open source vs. black box"
            }
        )
    except Exception as e:
        logger.error(f"Error fetching stats: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch statistics")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)

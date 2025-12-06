"""
ValorYield Engine API - Sovereign wealth-building platform
100% open-source, AI-orchestrated, running on YOUR infrastructure
"""
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import os

app = FastAPI(
    title="ValorYield Engine API",
    description="Sovereign wealth-building platform – 100% open-source",
    version="1.0.0"
)

# CORS for web/mobile clients
# In production, set ALLOWED_ORIGINS environment variable to restrict access
# Example: ALLOWED_ORIGINS=https://valoryield.example.com,https://app.valoryield.example.com
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:8009,http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

security = HTTPBearer(auto_error=False)  # JWT stub – add real auth later


class Portfolio(BaseModel):
    """Portfolio model with balance and allocation info"""
    balance: float
    account: str
    allocation: str
    last_updated: str


class Transaction(BaseModel):
    """Transaction record for deposits, withdrawals, trades"""
    date: str
    type: str
    amount: float
    source: str


class RebalanceRequest(BaseModel):
    """Request body for rebalancing trigger"""
    drift: float = 0


# Mock DB – swap for PostgreSQL/TimescaleDB in production
mock_portfolio = {
    "balance": 207.69,
    "account": "2143",
    "allocation": "Aggressive Mix"
}
mock_transactions = [
    {"date": "2025-12-01", "type": "deposit", "amount": 50.00, "source": "paycheck_7%"}
]


def get_thread_bank_balance():
    """Fetch balance from Thread Bank API (stubbed for now)"""
    # Real implementation would use:
    # response = requests.get(
    #     "https://api.threadconnect.io/v1/accounts/balances",
    #     headers={"Authorization": f"Bearer {os.getenv('THREAD_API_KEY')}"},
    #     params={"account_id": "2143"}
    # )
    # return response.json().get("balance", 0)
    return 207.69  # Mock balance


def get_kraken_balance():
    """Fetch crypto holdings from Kraken Pro (stubbed for now)"""
    # Real implementation would use pykrakenapi:
    # from pykrakenapi import KrakenAPI
    # kraken = KrakenAPI(key=os.getenv('KRAKEN_KEY'), secret=os.getenv('KRAKEN_SECRET'))
    # balances = kraken.get_balances()
    # return sum(float(val) * price for asset, val in balances.items())
    return 0.0  # Mock crypto balance


def get_ninjatrader_positions():
    """Fetch futures positions from NinjaTrader (stubbed for now)"""
    # Real implementation would use:
    # response = requests.get(
    #     "https://api.ninjatrader.com/rest/v1/positions",
    #     headers={"Authorization": f"Bearer {os.getenv('NT_API_TOKEN')}"},
    #     params={"account": "2143"}
    # )
    # return sum(pos["quantity"] * pos["marketValue"] for pos in response.json().get("positions", []))
    return 0.0  # Mock futures value


@app.get("/")
def root():
    """Health check and service info endpoint"""
    return {
        "name": "ValorYield Engine",
        "mission": "Democratize wealth-building through open-source infra",
        "sovereignty": "100%",
        "status": "operational",
        "deployed_on": "Codespaces → GCP GKE"
    }


@app.get("/health")
def health_check():
    """Health check for Kubernetes probes"""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat() + "Z"}


@app.get("/api/v1/portfolio", response_model=Portfolio)
def get_portfolio(token: str = Depends(security)):
    """
    Get aggregated portfolio balance across all connected accounts.
    
    Pulls from:
    - Thread Bank (banking)
    - Kraken Pro (crypto)
    - NinjaTrader (futures/options)
    - Fidelity (stocks - manual sync planned)
    """
    # Aggregate balances from all sources
    thread_balance = get_thread_bank_balance()
    crypto_balance = get_kraken_balance()
    futures_balance = get_ninjatrader_positions()
    
    # Fidelity stub (no full API yet – manual CSV upload planned)
    fidelity_balance = 0.0
    
    total_balance = thread_balance + crypto_balance + futures_balance + fidelity_balance
    
    return Portfolio(
        balance=total_balance,
        account=mock_portfolio["account"],
        allocation=mock_portfolio["allocation"],
        last_updated=datetime.utcnow().isoformat() + "Z"
    )


@app.get("/api/v1/transactions")
def get_transactions(token: str = Depends(security)):
    """Fetch recent transactions from TimescaleDB (stubbed)"""
    return {"transactions": mock_transactions}


@app.post("/api/v1/transactions")
def add_transaction(transaction: Transaction, token: str = Depends(security)):
    """Add a new transaction record"""
    mock_transactions.append(transaction.model_dump())
    return {"status": "success", "transaction": transaction}


@app.post("/api/v1/rebalance")
def trigger_rebalance(payload: RebalanceRequest, token: str = Depends(security)):
    """
    Trigger portfolio rebalancing when drift exceeds threshold.
    
    Publishes to NATS for Dialectical Rebalancer processing:
    - Thesis: current allocation
    - Antithesis: target allocation  
    - Synthesis: calculated trades
    """
    drift = payload.drift
    if drift > 5:
        # In production, publish to NATS:
        # await nc.publish("legion.rebalance.trigger", json.dumps({...}).encode())
        return {
            "status": "Rebalance triggered – Legion analyzing",
            "drift": drift,
            "triggered_at": datetime.utcnow().isoformat() + "Z"
        }
    raise HTTPException(status_code=400, detail="Drift <5% – chill mode, no rebalance needed")


@app.get("/api/v1/allocation")
def get_target_allocation(token: str = Depends(security)):
    """Get target allocation percentages"""
    return {
        "target": {
            "stocks": 0.4,
            "crypto": 0.3,
            "futures": 0.3
        },
        "description": "Aggressive Mix - 40% stocks, 30% crypto, 30% futures"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)

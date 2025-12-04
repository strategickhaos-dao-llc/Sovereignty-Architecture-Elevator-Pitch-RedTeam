"""
ValorYield Engine - API Tests
"""

import pytest
from fastapi.testclient import TestClient

from main import app, data_store


@pytest.fixture
def client():
    """Create test client"""
    # Reset data store before each test
    data_store.portfolio["balance"] = 207.69
    data_store.transactions = [
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
    return TestClient(app)


class TestRootEndpoint:
    """Tests for root endpoint"""
    
    def test_root_returns_ok(self, client):
        response = client.get("/")
        assert response.status_code == 200
    
    def test_root_contains_name(self, client):
        response = client.get("/")
        data = response.json()
        assert data["name"] == "ValorYield Engine"
    
    def test_root_contains_status(self, client):
        response = client.get("/")
        data = response.json()
        assert data["status"] == "operational"
    
    def test_root_contains_balance(self, client):
        response = client.get("/")
        data = response.json()
        assert data["balance"] == 207.69


class TestHealthEndpoint:
    """Tests for health check endpoint"""
    
    def test_health_returns_ok(self, client):
        response = client.get("/api/v1/health")
        assert response.status_code == 200
    
    def test_health_returns_healthy(self, client):
        response = client.get("/api/v1/health")
        data = response.json()
        assert data["status"] == "healthy"
    
    def test_health_contains_timestamp(self, client):
        response = client.get("/api/v1/health")
        data = response.json()
        assert "timestamp" in data


class TestPortfolioEndpoint:
    """Tests for portfolio endpoint"""
    
    def test_portfolio_returns_ok(self, client):
        response = client.get("/api/v1/portfolio")
        assert response.status_code == 200
    
    def test_portfolio_contains_balance(self, client):
        response = client.get("/api/v1/portfolio")
        data = response.json()
        assert "balance" in data
        assert data["balance"] == 207.69
    
    def test_portfolio_contains_account(self, client):
        response = client.get("/api/v1/portfolio")
        data = response.json()
        assert data["account"] == "2143"


class TestTransactionsEndpoint:
    """Tests for transactions endpoint"""
    
    def test_transactions_returns_ok(self, client):
        response = client.get("/api/v1/transactions")
        assert response.status_code == 200
    
    def test_transactions_has_list(self, client):
        response = client.get("/api/v1/transactions")
        data = response.json()
        assert "transactions" in data
        assert isinstance(data["transactions"], list)
    
    def test_transactions_limit(self, client):
        response = client.get("/api/v1/transactions?limit=1")
        data = response.json()
        assert len(data["transactions"]) == 1


class TestDepositEndpoint:
    """Tests for deposit endpoint"""
    
    def test_deposit_success(self, client):
        response = client.post("/api/v1/deposit?amount=100")
        assert response.status_code == 200
        data = response.json()
        assert data["deposited"] == 100
        assert data["new_balance"] == 307.69
        assert data["status"] == "success"
    
    def test_deposit_negative_fails(self, client):
        response = client.post("/api/v1/deposit?amount=-50")
        assert response.status_code == 422
    
    def test_deposit_zero_fails(self, client):
        response = client.post("/api/v1/deposit?amount=0")
        assert response.status_code == 422


class TestRebalanceEndpoint:
    """Tests for rebalance endpoint"""
    
    def test_rebalance_low_drift_skipped(self, client):
        response = client.post("/api/v1/rebalance?drift=3")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "skipped"
    
    def test_rebalance_high_drift_triggered(self, client):
        response = client.post("/api/v1/rebalance?drift=7")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "triggered"


class TestStatsEndpoint:
    """Tests for stats endpoint"""
    
    def test_stats_returns_ok(self, client):
        response = client.get("/api/v1/stats")
        assert response.status_code == 200
    
    def test_stats_contains_balance(self, client):
        response = client.get("/api/v1/stats")
        data = response.json()
        assert data["total_balance"] == 207.69
    
    def test_stats_contains_sovereignty_score(self, client):
        response = client.get("/api/v1/stats")
        data = response.json()
        assert data["sovereignty_score"] == 100

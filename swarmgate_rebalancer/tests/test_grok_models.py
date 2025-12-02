"""Tests for grok_models module."""

import pytest

from swarmgate_rebalancer.grok_models import GrokPlan, Order


class TestOrder:
    """Tests for Order model."""

    def test_valid_order(self):
        """Test creating a valid order."""
        order = Order(symbol="QQQ", usd=1000.0)
        assert order.symbol == "QQQ"
        assert order.usd == 1000.0

    def test_invalid_order_zero_usd(self):
        """Test that zero USD amount raises error."""
        with pytest.raises(ValueError):
            Order(symbol="QQQ", usd=0.0)

    def test_invalid_order_negative_usd(self):
        """Test that negative USD amount raises error."""
        with pytest.raises(ValueError):
            Order(symbol="QQQ", usd=-100.0)


class TestGrokPlan:
    """Tests for GrokPlan model."""

    def test_valid_plan(self):
        """Test creating a valid plan."""
        plan = GrokPlan(
            treasury_transfer_usd=746.67,
            treasury_tx="send $746.67 USDC to 0xtest",
            orders=[
                Order(symbol="QQQ", usd=1000.0),
                Order(symbol="BTC", usd=500.0),
            ],
            total_invested=1500.0,
            new_cash_buffer=100.0,
            deviation_after=0.0031,
        )
        assert plan.treasury_transfer_usd == 746.67
        assert len(plan.orders) == 2
        assert plan.total_invested == 1500.0

    def test_empty_orders_allowed(self):
        """Test that empty orders list is allowed."""
        plan = GrokPlan(
            treasury_transfer_usd=100.0,
            treasury_tx="send $100 USDC to 0xtest",
            orders=[],
            total_invested=0.0,
            new_cash_buffer=900.0,
            deviation_after=0.001,
        )
        assert len(plan.orders) == 0

    def test_invalid_total_invested_with_orders(self):
        """Test that total_invested must be positive if there are orders."""
        with pytest.raises(ValueError, match="must be > 0"):
            GrokPlan(
                treasury_transfer_usd=100.0,
                treasury_tx="send $100 USDC to 0xtest",
                orders=[Order(symbol="QQQ", usd=1000.0)],
                total_invested=0.0,  # invalid with orders
                new_cash_buffer=0.0,
                deviation_after=0.001,
            )

    def test_negative_treasury_invalid(self):
        """Test that negative treasury transfer raises error."""
        with pytest.raises(ValueError):
            GrokPlan(
                treasury_transfer_usd=-100.0,
                treasury_tx="invalid",
                orders=[],
                total_invested=0.0,
                new_cash_buffer=0.0,
                deviation_after=0.0,
            )

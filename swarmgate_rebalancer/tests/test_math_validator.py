"""Tests for math_validator module."""

import pytest

from swarmgate_rebalancer.config import FlowConfig, PortfolioTargets, Settings
from swarmgate_rebalancer.grok_models import GrokPlan, Order
from swarmgate_rebalancer.math_validator import (
    PortfolioSnapshot,
    ValidationResult,
    validate_plan,
)


def create_test_config(
    targets: dict[str, float] = None,
    treasury_pct: float = 0.07,
    max_single_order_usd: float = 5000.0,
    rebalance_threshold: float = 0.015,
) -> FlowConfig:
    """Create a test configuration."""
    if targets is None:
        targets = {
            "QQQ": 0.25,
            "TQQQ": 0.20,
            "BTC": 0.20,
            "ETH": 0.15,
            "SOL": 0.10,
            "SWARM": 0.07,
            "CASH": 0.03,
        }
    return FlowConfig(
        version=1,
        portfolio=PortfolioTargets(target=targets, current={}),
        settings=Settings(
            paycheck_net=10666.67,
            treasury_pct=treasury_pct,
            rebalance_threshold=rebalance_threshold,
            treasury_address="0xtest",
            max_single_order_usd=max_single_order_usd,
        ),
    )


def create_test_snapshot(
    positions: dict[str, float] = None,
    cash: float = 1500.0,
    paycheck: float = 10666.67,
) -> PortfolioSnapshot:
    """Create a test snapshot."""
    if positions is None:
        positions = {
            "QQQ": 12345.67,
            "TQQQ": 8000.00,
            "BTC": 9500.00,
            "ETH": 6800.00,
            "SOL": 4200.00,
        }
    return PortfolioSnapshot(
        positions_usd=positions,
        cash_usd=cash,
        paycheck_net_usd=paycheck,
    )


class TestValidatePlan:
    """Tests for validate_plan function."""

    def test_valid_plan_passes(self):
        """Test that a valid plan passes validation."""
        config = create_test_config()
        snapshot = create_test_snapshot()

        # Treasury should be 10666.67 * 0.07 = 746.67
        plan = GrokPlan(
            treasury_transfer_usd=746.67,
            treasury_tx="send $746.67 USDC to 0xtest",
            orders=[
                Order(symbol="TQQQ", usd=842.12),
                Order(symbol="SOL", usd=312.44),
            ],
            total_invested=1154.56,
            new_cash_buffer=0.0,
            deviation_after=0.0031,
        )

        result = validate_plan(config, snapshot, plan)
        assert result.ok, f"Unexpected errors: {result.errors}"

    def test_treasury_mismatch_fails(self):
        """Test that incorrect treasury amount fails validation."""
        config = create_test_config()
        snapshot = create_test_snapshot()

        plan = GrokPlan(
            treasury_transfer_usd=500.0,  # Wrong - should be 746.67
            treasury_tx="send $500 USDC to 0xtest",
            orders=[],
            total_invested=0.0,
            new_cash_buffer=0.0,
            deviation_after=0.0,
        )

        result = validate_plan(config, snapshot, plan)
        assert not result.ok
        assert any("Treasury mismatch" in e for e in result.errors)

    def test_total_invested_mismatch_fails(self):
        """Test that total_invested not matching orders sum fails."""
        config = create_test_config()
        snapshot = create_test_snapshot()

        plan = GrokPlan(
            treasury_transfer_usd=746.67,
            treasury_tx="send $746.67 USDC to 0xtest",
            orders=[
                Order(symbol="QQQ", usd=1000.0),
            ],
            total_invested=2000.0,  # Wrong - should be 1000.0
            new_cash_buffer=0.0,
            deviation_after=0.0,
        )

        result = validate_plan(config, snapshot, plan)
        assert not result.ok
        assert any("total_invested mismatch" in e for e in result.errors)

    def test_order_exceeds_max_size_fails(self):
        """Test that order exceeding max_single_order_usd fails."""
        config = create_test_config(max_single_order_usd=1000.0)
        snapshot = create_test_snapshot()

        plan = GrokPlan(
            treasury_transfer_usd=746.67,
            treasury_tx="send $746.67 USDC to 0xtest",
            orders=[
                Order(symbol="QQQ", usd=2000.0),  # Exceeds 1000 max
            ],
            total_invested=2000.0,
            new_cash_buffer=0.0,
            deviation_after=0.0,
        )

        result = validate_plan(config, snapshot, plan)
        assert not result.ok
        assert any("exceeds max_single_order_usd" in e for e in result.errors)

    def test_swarm_in_orders_fails(self):
        """Test that SWARM in market orders fails (treasury only)."""
        config = create_test_config()
        snapshot = create_test_snapshot()

        plan = GrokPlan(
            treasury_transfer_usd=746.67,
            treasury_tx="send $746.67 USDC to 0xtest",
            orders=[
                Order(symbol="SWARM", usd=500.0),  # Invalid - treasury only
            ],
            total_invested=500.0,
            new_cash_buffer=0.0,
            deviation_after=0.0,
        )

        result = validate_plan(config, snapshot, plan)
        assert not result.ok
        assert any("SWARM must be funded via treasury" in e for e in result.errors)

    def test_unauthorized_symbol_fails(self):
        """Test that unauthorized symbol in orders fails."""
        config = create_test_config()
        snapshot = create_test_snapshot()

        plan = GrokPlan(
            treasury_transfer_usd=746.67,
            treasury_tx="send $746.67 USDC to 0xtest",
            orders=[
                Order(symbol="DOGECOIN", usd=500.0),  # Not in targets
            ],
            total_invested=500.0,
            new_cash_buffer=0.0,
            deviation_after=0.0,
        )

        result = validate_plan(config, snapshot, plan)
        assert not result.ok
        assert any("unauthorized symbol" in e for e in result.errors)

    def test_overspending_cash_fails(self):
        """Test that overspending available cash fails."""
        config = create_test_config()
        snapshot = create_test_snapshot(cash=100.0)  # Very little cash

        plan = GrokPlan(
            treasury_transfer_usd=746.67,
            treasury_tx="send $746.67 USDC to 0xtest",
            orders=[
                Order(symbol="QQQ", usd=15000.0),  # Way more than available
            ],
            total_invested=15000.0,
            new_cash_buffer=0.0,
            deviation_after=0.0,
        )

        result = validate_plan(config, snapshot, plan)
        assert not result.ok
        assert any("overspends cash" in e for e in result.errors)

    def test_empty_orders_valid(self):
        """Test that empty orders with correct treasury is valid."""
        config = create_test_config()
        snapshot = create_test_snapshot()

        plan = GrokPlan(
            treasury_transfer_usd=746.67,
            treasury_tx="send $746.67 USDC to 0xtest",
            orders=[],
            total_invested=0.0,
            new_cash_buffer=0.0,
            deviation_after=0.0,
        )

        result = validate_plan(config, snapshot, plan)
        assert result.ok, f"Unexpected errors: {result.errors}"


class TestPortfolioSnapshot:
    """Tests for PortfolioSnapshot dataclass."""

    def test_snapshot_creation(self):
        """Test creating a portfolio snapshot."""
        snapshot = PortfolioSnapshot(
            positions_usd={"QQQ": 10000.0, "BTC": 5000.0},
            cash_usd=1000.0,
            paycheck_net_usd=5000.0,
        )
        assert snapshot.positions_usd["QQQ"] == 10000.0
        assert snapshot.cash_usd == 1000.0
        assert snapshot.paycheck_net_usd == 5000.0


class TestValidationResult:
    """Tests for ValidationResult dataclass."""

    def test_result_ok(self):
        """Test creating a passing result."""
        result = ValidationResult(ok=True, errors=[], warnings=[])
        assert result.ok

    def test_result_with_errors(self):
        """Test creating a failing result."""
        result = ValidationResult(
            ok=False,
            errors=["Error 1", "Error 2"],
            warnings=["Warning 1"],
        )
        assert not result.ok
        assert len(result.errors) == 2
        assert len(result.warnings) == 1

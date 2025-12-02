"""Tests for config module."""

import tempfile
from pathlib import Path

import pytest

from swarmgate_rebalancer.config import FlowConfig, load_flow_config, PortfolioTargets


class TestPortfolioTargets:
    """Tests for PortfolioTargets model."""

    def test_valid_targets(self):
        """Test that valid targets sum to 1.0."""
        targets = PortfolioTargets(
            target={"QQQ": 0.5, "BTC": 0.3, "CASH": 0.2},
            current={},
        )
        assert targets.target["QQQ"] == 0.5
        assert targets.target["BTC"] == 0.3
        assert targets.target["CASH"] == 0.2

    def test_invalid_targets_not_sum_to_one(self):
        """Test that targets not summing to 1.0 raise error."""
        with pytest.raises(ValueError, match="must sum to 1.0"):
            PortfolioTargets(
                target={"QQQ": 0.5, "BTC": 0.3},  # sums to 0.8
                current={},
            )

    def test_targets_with_small_rounding_error(self):
        """Test that small rounding errors are tolerated."""
        # These sum to 1.0000001 due to floating point
        targets = PortfolioTargets(
            target={
                "QQQ": 0.25,
                "TQQQ": 0.20,
                "BTC": 0.20,
                "ETH": 0.15,
                "SOL": 0.10,
                "SWARM": 0.07,
                "CASH": 0.03,
            },
            current={},
        )
        assert len(targets.target) == 7


class TestFlowConfig:
    """Tests for FlowConfig model."""

    def test_valid_config(self):
        """Test loading a valid configuration."""
        config = FlowConfig(
            version=1,
            portfolio=PortfolioTargets(
                target={"QQQ": 0.5, "CASH": 0.5},
                current={},
            ),
            settings={
                "paycheck_net": 10000.0,
                "treasury_pct": 0.07,
                "rebalance_threshold": 0.015,
                "treasury_address": "0xtest",
            },
        )
        assert config.version == 1
        assert config.settings.paycheck_net == 10000.0
        assert config.settings.treasury_pct == 0.07

    def test_invalid_treasury_pct(self):
        """Test that treasury_pct must be between 0 and 1."""
        with pytest.raises(ValueError):
            FlowConfig(
                version=1,
                portfolio=PortfolioTargets(
                    target={"QQQ": 1.0},
                    current={},
                ),
                settings={
                    "paycheck_net": 10000.0,
                    "treasury_pct": 1.5,  # invalid - > 1.0
                    "rebalance_threshold": 0.015,
                    "treasury_address": "0xtest",
                },
            )


class TestLoadFlowConfig:
    """Tests for load_flow_config function."""

    def test_load_valid_yaml(self):
        """Test loading a valid YAML file."""
        yaml_content = """
version: 1
portfolio:
  target:
    QQQ: 0.5
    CASH: 0.5
  current: {}
settings:
  paycheck_net: 10000.0
  treasury_pct: 0.07
  rebalance_threshold: 0.015
  treasury_address: "0xtest"
"""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".yaml", delete=False
        ) as f:
            f.write(yaml_content)
            f.flush()
            config = load_flow_config(f.name)
            assert config.version == 1
            assert config.settings.paycheck_net == 10000.0

    def test_load_missing_file(self):
        """Test that loading a missing file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            load_flow_config("/nonexistent/path/flow.yaml")

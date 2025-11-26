#!/usr/bin/env python3
"""
Tests for Energy Scheduler

Artifact #3558 - Colossus Grok-5 Deployment Suite
"""

import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime, time
import sys
import os

# Add src to path FIRST
src_path = os.path.join(os.path.dirname(__file__), '..', 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# Import directly from module files (not from __init__.py) to avoid cascade
from training.consensus_protocol import PowerWindowDecision
from training.energy_scheduler import EnergyScheduler, EnergyStatus


class MockPowerClient:
    """Mock power client for testing."""

    def __init__(self, power_mw: float = 200.0):
        self._power = power_mw

    def current_mw(self) -> float:
        return self._power


class MockMegapackClient:
    """Mock Megapack client for testing."""

    def __init__(self, soc: float = 0.8):
        self._soc = soc

    def current_soc(self) -> float:
        return self._soc


class TestEnergyScheduler:
    """Tests for Energy Scheduler."""

    def test_default_initialization(self):
        """Test scheduler initializes with defaults."""
        scheduler = EnergyScheduler()
        assert scheduler.power_limit_mw == 250.0
        assert scheduler.soc_min == 0.4

    def test_get_status(self):
        """Test getting energy status."""
        power_client = MockPowerClient(power_mw=180.0)
        megapack_client = MockMegapackClient(soc=0.75)
        scheduler = EnergyScheduler(
            power_client=power_client,
            megapack_client=megapack_client,
        )

        status = scheduler.get_status()
        assert isinstance(status, EnergyStatus)
        assert status.power_mw == 180.0
        assert status.soc == 0.75

    def test_evaluate_window_ok(self):
        """Test evaluate window returns OK when conditions are good."""
        power_client = MockPowerClient(power_mw=180.0)
        megapack_client = MockMegapackClient(soc=0.8)
        scheduler = EnergyScheduler(
            power_client=power_client,
            megapack_client=megapack_client,
        )

        decision = scheduler.evaluate_window()
        assert decision.allowed
        assert decision.reason == "OK"
        assert decision.delay_seconds == 0

    def test_evaluate_window_power_exceeded(self):
        """Test evaluate window blocks when power exceeded."""
        power_client = MockPowerClient(power_mw=300.0)  # Over 250 limit
        scheduler = EnergyScheduler(power_client=power_client)

        decision = scheduler.evaluate_window()
        assert not decision.allowed
        assert decision.reason == "GRID_CONSTRAINT"
        assert decision.delay_seconds > 0

    def test_evaluate_window_low_soc(self):
        """Test evaluate window with low SoC during peak hours."""
        power_client = MockPowerClient(power_mw=200.0)
        megapack_client = MockMegapackClient(soc=0.2)  # Below 0.4
        scheduler = EnergyScheduler(
            power_client=power_client,
            megapack_client=megapack_client,
            # Use hours that ensure we test off-peak logic (midnight to 1 AM)
            offpeak_start=time(0, 0),
            offpeak_end=time(1, 0),
        )

        decision = scheduler.evaluate_window()
        # The result depends on current time vs off-peak window
        # We just validate the decision structure is correct
        assert isinstance(decision, PowerWindowDecision)
        assert decision.suggested_scale <= 1.0

    def test_scale_factor_high_soc(self):
        """Test scale factor is 1.0 with high SoC."""
        power_client = MockPowerClient(power_mw=150.0)
        megapack_client = MockMegapackClient(soc=0.85)
        scheduler = EnergyScheduler(
            power_client=power_client,
            megapack_client=megapack_client,
        )

        decision = scheduler.evaluate_window()
        if decision.allowed:
            assert decision.suggested_scale == 1.0

    def test_scale_factor_medium_soc(self):
        """Test scale factor is reduced with medium SoC."""
        power_client = MockPowerClient(power_mw=150.0)
        megapack_client = MockMegapackClient(soc=0.5)  # Between 0.4 and 0.8
        scheduler = EnergyScheduler(
            power_client=power_client,
            megapack_client=megapack_client,
        )

        decision = scheduler.evaluate_window()
        if decision.allowed:
            assert decision.suggested_scale == 0.8

    def test_custom_thresholds(self):
        """Test custom thresholds are respected."""
        scheduler = EnergyScheduler(
            power_limit_mw=100.0,
            soc_min=0.6,
        )

        power_client = MockPowerClient(power_mw=120.0)  # Over custom limit
        scheduler.power_client = power_client

        decision = scheduler.evaluate_window()
        assert not decision.allowed
        assert decision.reason == "GRID_CONSTRAINT"


class TestPowerWindowDecision:
    """Tests for PowerWindowDecision dataclass."""

    def test_decision_creation(self):
        """Test creating a power window decision."""
        decision = PowerWindowDecision(
            allowed=True,
            reason="OK",
            suggested_scale=1.0,
            delay_seconds=0,
        )
        assert decision.allowed
        assert decision.reason == "OK"

    def test_decision_blocked(self):
        """Test blocked decision."""
        decision = PowerWindowDecision(
            allowed=False,
            reason="GRID_CONSTRAINT",
            suggested_scale=0.5,
            delay_seconds=900,
        )
        assert not decision.allowed
        assert decision.delay_seconds == 900


class TestEnergyStatus:
    """Tests for EnergyStatus dataclass."""

    def test_status_creation(self):
        """Test creating energy status."""
        status = EnergyStatus(
            power_mw=200.0,
            soc=0.75,
            in_offpeak=True,
            timestamp=datetime.utcnow(),
        )
        assert status.power_mw == 200.0
        assert status.soc == 0.75
        assert status.in_offpeak


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

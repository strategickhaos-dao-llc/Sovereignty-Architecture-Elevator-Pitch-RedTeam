"""
Energy Scheduler

Coordinates Grok-5 training with grid & Megapack state.
"""

import logging
from dataclasses import dataclass
from datetime import datetime, time as dtime
from typing import Optional, Protocol

from prometheus_client import Gauge

from .consensus_protocol import PowerWindowDecision

POWER_MW = Gauge("colossus_power_mw", "Real-time MW draw for Colossus")
MEGAPACK_SOC = Gauge("megapack_soc", "Tesla Megapack state-of-charge fraction")


class PowerClient(Protocol):
    """Protocol for power monitoring client."""

    def current_mw(self) -> float:
        """Get current power draw in MW."""
        ...


class MegapackClient(Protocol):
    """Protocol for Megapack battery client."""

    def current_soc(self) -> float:
        """Get current state of charge (0.0 - 1.0)."""
        ...


@dataclass
class EnergyStatus:
    """Current energy status."""

    power_mw: float
    soc: float
    in_offpeak: bool
    timestamp: datetime


class EnergyScheduler:
    """
    Coordinates Grok-5 training with grid & Megapack state.

    Rules:
      - Prefer 02:00–06:00 local for heavy runs.
      - Throttle if power > 250 MW.
      - Require Megapack SoC > 0.4 for aggressive scaling.
      - Produce PowerWindowDecision for trainer + HPA.
    """

    DEFAULT_POWER_LIMIT = 250.0
    DEFAULT_SOC_MIN = 0.4
    DEFAULT_OFFPEAK_START = dtime(2, 0)
    DEFAULT_OFFPEAK_END = dtime(6, 0)

    def __init__(
        self,
        power_client: Optional[PowerClient] = None,
        megapack_client: Optional[MegapackClient] = None,
        power_limit_mw: float = DEFAULT_POWER_LIMIT,
        soc_min: float = DEFAULT_SOC_MIN,
        offpeak_start: dtime = DEFAULT_OFFPEAK_START,
        offpeak_end: dtime = DEFAULT_OFFPEAK_END,
        logger: Optional[logging.Logger] = None,
    ):
        """
        Initialize energy scheduler.

        Args:
            power_client: Client for power monitoring
            megapack_client: Client for Megapack battery
            power_limit_mw: Maximum power draw in MW (default: 250)
            soc_min: Minimum state of charge for scaling (default: 0.4)
            offpeak_start: Start of off-peak window (default: 02:00)
            offpeak_end: End of off-peak window (default: 06:00)
            logger: Logger instance
        """
        self.power_client = power_client
        self.megapack_client = megapack_client
        self.power_limit_mw = power_limit_mw
        self.soc_min = soc_min
        self.offpeak_start = offpeak_start
        self.offpeak_end = offpeak_end
        self.log = logger or logging.getLogger(__name__)

    def _in_offpeak_window(self, now: datetime) -> bool:
        """Check if current time is in off-peak window."""
        return self.offpeak_start <= now.time() <= self.offpeak_end

    def _get_power(self) -> float:
        """Get current power consumption."""
        if self.power_client:
            return self.power_client.current_mw()
        # Default for development
        return 200.0

    def _get_soc(self) -> float:
        """Get current Megapack state of charge."""
        if self.megapack_client:
            return self.megapack_client.current_soc()
        # Default for development
        return 0.8

    def get_status(self) -> EnergyStatus:
        """
        Get current energy status.

        Returns:
            EnergyStatus with current readings
        """
        now = datetime.utcnow()
        return EnergyStatus(
            power_mw=self._get_power(),
            soc=self._get_soc(),
            in_offpeak=self._in_offpeak_window(now),
            timestamp=now,
        )

    def evaluate_window(self) -> PowerWindowDecision:
        """
        Evaluate current power window for training.

        Returns:
            PowerWindowDecision indicating if training is allowed
        """
        now = datetime.utcnow()
        power_mw = self._get_power()
        soc = self._get_soc()

        # Update Prometheus metrics
        POWER_MW.set(power_mw)
        MEGAPACK_SOC.set(soc)

        self.log.info(
            f"[energy] now={now.isoformat()} "
            f"power={power_mw:.1f}MW "
            f"soc={soc:.2f}"
        )

        # Check power limit
        if power_mw > self.power_limit_mw:
            return PowerWindowDecision(
                allowed=False,
                reason="GRID_CONSTRAINT",
                suggested_scale=0.5,
                delay_seconds=900,
            )

        # Check off-peak and SoC
        if not self._in_offpeak_window(now) and soc < self.soc_min:
            return PowerWindowDecision(
                allowed=False,
                reason="OFFPEAK_REQUIRED",
                suggested_scale=0.5,
                delay_seconds=1800,
            )

        # Determine scale factor based on conditions
        if soc >= 0.8:
            scale = 1.0
        elif soc >= self.soc_min:
            scale = 0.8
        else:
            scale = 0.5

        return PowerWindowDecision(
            allowed=True,
            reason="OK",
            suggested_scale=scale,
            delay_seconds=0,
        )

    def wait_for_window(self, max_wait_seconds: int = 3600) -> PowerWindowDecision:
        """
        Wait for a suitable training window.

        Args:
            max_wait_seconds: Maximum time to wait

        Returns:
            PowerWindowDecision when window is available or timeout
        """
        import time

        start = datetime.utcnow()
        elapsed = 0

        while elapsed < max_wait_seconds:
            decision = self.evaluate_window()
            if decision.allowed:
                return decision

            self.log.info(
                f"[energy] Waiting for window: {decision.reason} "
                f"(delay: {decision.delay_seconds}s)"
            )

            # Wait for suggested delay or check interval
            wait_time = min(decision.delay_seconds, 60)
            time.sleep(wait_time)

            elapsed = (datetime.utcnow() - start).total_seconds()

        return PowerWindowDecision(
            allowed=False,
            reason="TIMEOUT",
            suggested_scale=0.0,
            delay_seconds=0,
        )

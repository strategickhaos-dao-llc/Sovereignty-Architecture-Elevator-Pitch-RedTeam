# python/depart_arrived.py
"""
DepartArrivedTask: Tracks departure and arrival times for commute logging.
"""
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional
from commute_algorithm import Coordinates

@dataclass
class DepartArrivedContext:
    home: Coordinates
    work: Coordinates
    departed_time: Optional[datetime] = None
    arrived_time: Optional[datetime] = None

@dataclass
class DepartArrivedResult:
    status: str  # "home", "in_transit", "at_work"
    actual_commute_duration: Optional[timedelta]
    note: str

class DepartArrivedTask:
    def run(self, ctx: DepartArrivedContext) -> DepartArrivedResult:
        """
        Determines current status based on departure and arrival times.
        """
        if ctx.departed_time is None:
            return DepartArrivedResult(
                status="home",
                actual_commute_duration=None,
                note="At home, not yet departed."
            )
        
        if ctx.arrived_time is None:
            return DepartArrivedResult(
                status="in_transit",
                actual_commute_duration=None,
                note=f"In transit. Departed at {ctx.departed_time.strftime('%H:%M')}."
            )
        
        duration = ctx.arrived_time - ctx.departed_time
        return DepartArrivedResult(
            status="at_work",
            actual_commute_duration=duration,
            note=f"Arrived at work. Commute took {duration}."
        )

    def log_departure(self, time: datetime) -> None:
        print(f"[DEPART LOG] Departed at: {time.strftime('%Y-%m-%d %H:%M')}")

    def log_arrival(self, time: datetime) -> None:
        print(f"[ARRIVED LOG] Arrived at: {time.strftime('%Y-%m-%d %H:%M')}")

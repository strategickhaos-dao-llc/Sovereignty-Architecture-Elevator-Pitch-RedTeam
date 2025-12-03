# python/commute_algorithm.py
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional

@dataclass
class Coordinates:
    lat: float
    lon: float

@dataclass
class CommuteContext:
    home: Coordinates
    work: Coordinates
    departure_time: datetime
    # later: traffic_profile, mode_of_transport, etc.

@dataclass
class CommuteResult:
    estimated_duration: timedelta
    eta: datetime
    note: str

class CommuteAlgorithm:
    def estimate_commute(self, ctx: CommuteContext) -> CommuteResult:
        """
        Stub: in real life, call Google Maps / some routing API here.
        For now, fake it based on straight-line distance.
        """
        distance_km = self._haversine(ctx.home, ctx.work)

        # naive: 40 km/h average speed
        hours = distance_km / 40.0
        duration = timedelta(hours=hours)

        eta = ctx.departure_time + duration
        note = f"Distance ~{distance_km:.1f} km, ETA at {eta.strftime('%H:%M')}."

        return CommuteResult(
            estimated_duration=duration,
            eta=eta,
            note=note
        )

    def _haversine(self, a: Coordinates, b: Coordinates) -> float:
        from math import radians, sin, cos, asin, sqrt

        R = 6371.0  # km
        dlat = radians(b.lat - a.lat)
        dlon = radians(b.lon - a.lon)
        lat1 = radians(a.lat)
        lat2 = radians(b.lat)

        h = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        return 2 * R * asin(sqrt(h))

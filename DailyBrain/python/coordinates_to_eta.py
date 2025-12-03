# python/coordinates_to_eta.py
"""
CoordinatesToETA: Utility for converting coordinates to estimated time of arrival.
Wraps external APIs (Google Maps, etc.) for ETA calculation.
"""
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Optional
from commute_algorithm import Coordinates, CommuteAlgorithm, CommuteContext

@dataclass
class ETARequest:
    origin: Coordinates
    destination: Coordinates
    departure_time: datetime
    mode: str = "driving"  # "driving", "walking", "transit", "bicycling"

@dataclass
class ETAResponse:
    eta: datetime
    duration: timedelta
    distance_km: float
    route_summary: str

class CoordinatesToETA:
    """
    Wrapper class for ETA calculations.
    In production, this would integrate with Google Maps API or similar.
    """
    
    def __init__(self):
        self._algo = CommuteAlgorithm()
    
    def get_eta(self, request: ETARequest) -> ETAResponse:
        """
        Calculate ETA from origin to destination.
        Currently uses haversine distance; in production, use routing API.
        """
        ctx = CommuteContext(
            home=request.origin,
            work=request.destination,
            departure_time=request.departure_time
        )
        
        result = self._algo.estimate_commute(ctx)
        distance = self._algo.calculate_distance(request.origin, request.destination)
        
        return ETAResponse(
            eta=result.eta,
            duration=result.estimated_duration,
            distance_km=distance,
            route_summary=f"Direct route ({request.mode}): {distance:.1f} km"
        )
    
    def get_multi_stop_eta(self, stops: List[Coordinates], departure_time: datetime) -> List[ETAResponse]:
        """
        Calculate ETAs for a route with multiple stops.
        """
        if len(stops) < 2:
            return []
        
        results = []
        current_time = departure_time
        
        for i in range(len(stops) - 1):
            request = ETARequest(
                origin=stops[i],
                destination=stops[i + 1],
                departure_time=current_time
            )
            response = self.get_eta(request)
            results.append(response)
            current_time = response.eta
        
        return results

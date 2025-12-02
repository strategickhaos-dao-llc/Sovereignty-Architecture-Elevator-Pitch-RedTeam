"""
DiviDen Refinery - Royalty Refinery Module
Part of the Strategickhaos DiviDen Refinery Ecosystem

Transforms legal settlements and reparations into perpetual income streams.
"""

from .config import RoyaltyRefineryConfig, get_royalty_config
from .royalty_flow import (
    RoyaltyStream,
    RoyaltySource,
    RoyaltyDistributor,
    RoyaltyAuditTrail,
)

__all__ = [
    "RoyaltyRefineryConfig",
    "get_royalty_config",
    "RoyaltyStream",
    "RoyaltySource", 
    "RoyaltyDistributor",
    "RoyaltyAuditTrail",
]

__version__ = "1.0.0"

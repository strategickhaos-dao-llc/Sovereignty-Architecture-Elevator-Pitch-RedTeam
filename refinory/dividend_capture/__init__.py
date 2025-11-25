"""
DiviDen Ninja Bot - Dividend Capture Module
Part of the Strategickhaos DiviDen Refinery Ecosystem
"""

from .config import DividendCaptureConfig, get_dividend_config
from .bot import DividendCaptureBot
from .strategies import (
    ExDividendSniper,
    SpecialDividendDetector,
    MergerArbitrageAnalyzer,
    OptionsPlayStrategy,
)
from .hlmcr_governance import HLMCRGovernor, GovernanceDecision

__all__ = [
    "DividendCaptureConfig",
    "get_dividend_config",
    "DividendCaptureBot",
    "ExDividendSniper",
    "SpecialDividendDetector",
    "MergerArbitrageAnalyzer",
    "OptionsPlayStrategy",
    "HLMCRGovernor",
    "GovernanceDecision",
]

__version__ = "1.0.0"

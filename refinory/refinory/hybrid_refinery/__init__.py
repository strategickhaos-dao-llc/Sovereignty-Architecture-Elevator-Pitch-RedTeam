"""
Strategickhaos Hybrid Refinery - Investment Management System
=============================================================

A comprehensive hybrid investment management system combining:
- Dividend Engine (Core): Stable yield reactor for compounding wealth
- RANCO/PID Tactical Overlay: Mechanical attack mode for volatility-driven trades

Architecture:
    Core: Dividend Engine → slow, compounding, cannot-die machine
    Overlay: Signal Layer → tells what's safe to add, avoid, or attack
    Tactical: RANCO/PID → small, lethal, mechanical trades (15% cap)

Flow Routing:
    70% → Auto reinvest to compounding core
    23% → Treasury buffer for dislocations
    7%  → SwarmGate (autonomous AI flow router)
"""

from .config import HybridRefineryConfig, PortfolioGuardrails, TacticalParameters
from .dividend_engine import DividendEngine, DividendStock, ScreeningResult
from .ranco_pid import RANCOPIDEngine, TacticalSignal, TradeSetup
from .portfolio import PortfolioManager, Position, FlowAllocation
from .screener import StockScreener, ScreenerOutput
from .swarmgate import SwarmGateRouter, FlowDestination
from .validation import ValidationEngine, BacktestResult, MonteCarloResult
from .automation import AutomationEngine, NightlyCronJob, WeeklyReport

__all__ = [
    # Configuration
    "HybridRefineryConfig",
    "PortfolioGuardrails", 
    "TacticalParameters",
    # Dividend Engine
    "DividendEngine",
    "DividendStock",
    "ScreeningResult",
    # RANCO/PID
    "RANCOPIDEngine",
    "TacticalSignal",
    "TradeSetup",
    # Portfolio Management
    "PortfolioManager",
    "Position",
    "FlowAllocation",
    # Screener
    "StockScreener",
    "ScreenerOutput",
    # SwarmGate
    "SwarmGateRouter",
    "FlowDestination",
    # Validation
    "ValidationEngine",
    "BacktestResult",
    "MonteCarloResult",
    # Automation
    "AutomationEngine",
    "NightlyCronJob",
    "WeeklyReport",
]

__version__ = "1.0.0"
__author__ = "Strategickhaos Swarm Intelligence"

"""
Refinory AI Agent Orchestration Platform
Entry point module for the package

Includes the Strategickhaos Hybrid Refinery - an advanced investment
management system combining dividend income generation with tactical trading.
"""

__version__ = "1.0.0"
__author__ = "Strategickhaos Swarm Intelligence"
__description__ = "AI agent orchestration platform for autonomous software architecture generation"

from .main import app
from .orchestrator import ExpertOrchestrator, ArchitectureRequest, RequestStatus
from .experts import ExpertTeam, ExpertName
from .config import Settings, get_settings
from .database import Database
from .discord_integration import DiscordNotifier, RefineryDiscordBot
from .github_integration import GitHubIntegration

# Hybrid Refinery - Investment Management System
from .hybrid_refinery import (
    HybridRefineryConfig,
    PortfolioGuardrails,
    TacticalParameters,
    DividendEngine,
    DividendStock,
    ScreeningResult,
    RANCOPIDEngine,
    TacticalSignal,
    TradeSetup,
    PortfolioManager,
    Position,
    FlowAllocation,
    StockScreener,
    ScreenerOutput,
    SwarmGateRouter,
    FlowDestination,
    ValidationEngine,
    BacktestResult,
    MonteCarloResult,
    AutomationEngine,
    NightlyCronJob,
    WeeklyReport,
)

__all__ = [
    # Core Refinory
    "app",
    "ExpertOrchestrator", 
    "ArchitectureRequest",
    "RequestStatus",
    "ExpertTeam",
    "ExpertName", 
    "Settings",
    "get_settings",
    "Database",
    "DiscordNotifier",
    "RefineryDiscordBot",
    "GitHubIntegration",
    # Hybrid Refinery - Configuration
    "HybridRefineryConfig",
    "PortfolioGuardrails",
    "TacticalParameters",
    # Hybrid Refinery - Dividend Engine
    "DividendEngine",
    "DividendStock",
    "ScreeningResult",
    # Hybrid Refinery - RANCO/PID
    "RANCOPIDEngine",
    "TacticalSignal",
    "TradeSetup",
    # Hybrid Refinery - Portfolio
    "PortfolioManager",
    "Position",
    "FlowAllocation",
    # Hybrid Refinery - Screener
    "StockScreener",
    "ScreenerOutput",
    # Hybrid Refinery - SwarmGate
    "SwarmGateRouter",
    "FlowDestination",
    # Hybrid Refinery - Validation
    "ValidationEngine",
    "BacktestResult",
    "MonteCarloResult",
    # Hybrid Refinery - Automation
    "AutomationEngine",
    "NightlyCronJob",
    "WeeklyReport",
]
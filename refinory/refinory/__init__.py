"""
Refinory AI Agent Orchestration Platform
Entry point module for the package

Includes the Hybrid Refinery Financial System for sovereign income architecture.
"""

__version__ = "1.1.0"
__author__ = "Strategickhaos Swarm Intelligence"
__description__ = "AI agent orchestration platform for autonomous software architecture and sovereign income generation"

from .main import app
from .orchestrator import ExpertOrchestrator, ArchitectureRequest, RequestStatus
from .experts import ExpertTeam, ExpertName
from .config import Settings, get_settings
from .database import Database
from .discord_integration import DiscordNotifier, RefinoryDiscordBot
from .github_integration import GitHubIntegration

# Financial System Imports
from .finance_models import (
    # Enums
    AssetClass, PositionType, SignalType, RiskLevel, AccountType,
    # Core models
    Guardrails, DividendScreenCriteria, DividendStock, DividendEngineConfig,
    TechnicalIndicators, FundamentalData, RefinerySignal, RefineryOverlayConfig,
    RANCOEntryRules, RANCOExitRules, RANCOSizingRules, RANCOCandidate, RANCOTacticalConfig,
    Position, CashFlow, Portfolio, Watchlist, AutomationRule, RiskAlert,
    WeeklyReport, BacktestResult, MonteCarloResult,
)
from .finance_services import (
    DividendScreeningService, RefineryOverlayService, RANCOTacticalService,
    RiskManagementService, PortfolioAnalyticsService, FinancialRefineryOrchestrator,
)
from .finance_expert import FinanceExpertTeam, FinanceExpertName

__all__ = [
    # Core Platform
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
    "RefinoryDiscordBot",
    "GitHubIntegration",
    
    # Financial System - Enums
    "AssetClass",
    "PositionType",
    "SignalType",
    "RiskLevel",
    "AccountType",
    
    # Financial System - Models
    "Guardrails",
    "DividendScreenCriteria",
    "DividendStock",
    "DividendEngineConfig",
    "TechnicalIndicators",
    "FundamentalData",
    "RefinerySignal",
    "RefineryOverlayConfig",
    "RANCOEntryRules",
    "RANCOExitRules",
    "RANCOSizingRules",
    "RANCOCandidate",
    "RANCOTacticalConfig",
    "Position",
    "CashFlow",
    "Portfolio",
    "Watchlist",
    "AutomationRule",
    "RiskAlert",
    "WeeklyReport",
    "BacktestResult",
    "MonteCarloResult",
    
    # Financial System - Services
    "DividendScreeningService",
    "RefineryOverlayService",
    "RANCOTacticalService",
    "RiskManagementService",
    "PortfolioAnalyticsService",
    "FinancialRefineryOrchestrator",
    
    # Financial System - Experts
    "FinanceExpertTeam",
    "FinanceExpertName",
]
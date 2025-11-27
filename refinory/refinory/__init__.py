"""
Refinory AI Agent Orchestration Platform
Entry point module for the package
"""

__version__ = "1.0.0"
__author__ = "Strategickhaos Swarm Intelligence"
__description__ = "AI agent orchestration platform for autonomous software architecture generation"

from .main import app
from .orchestrator import ExpertOrchestrator, ArchitectureRequest, RequestStatus
from .experts import ExpertTeam, ExpertName
from .config import Settings, get_settings
from .database import Database
from .discord_integration import DiscordNotifier, RefinoryDiscordBot
from .github_integration import GitHubIntegration

# Hybrid Refinery - Dividend Portfolio Architecture
from .portfolio_config import (
    DIVIDEND_CORE,
    TOTAL_CAPITAL,
    SWARMGATE,
    get_portfolio_summary,
    get_position_details,
    rescale_portfolio,
)
from .swarmgate import SwarmGateRouter, create_default_swarmgate
from .nightly_refinery import NightlyRefinery

__all__ = [
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
    # Hybrid Refinery exports
    "DIVIDEND_CORE",
    "TOTAL_CAPITAL",
    "SWARMGATE",
    "get_portfolio_summary",
    "get_position_details",
    "rescale_portfolio",
    "SwarmGateRouter",
    "create_default_swarmgate",
    "NightlyRefinery",
]
"""
Strategickhaos Wealth Engine
============================
Fully-autonomous, institutional-grade, long-term wealth engine.

Four-Script Automation Suite:
- portfolio_rebalancer.py - Rebalancing logic with drift detection
- dividend_compounder.py - Dividend reinvestment and compounding
- cashflow_autopilot.py - Monthly cashflow automation
- tactical_manager.py - Tactical sleeve management

"You literally created future wealth out of thin air with four text files."
"""

from .portfolio_rebalancer import PortfolioRebalancer
from .dividend_compounder import DividendCompounder
from .cashflow_autopilot import CashflowAutopilot
from .tactical_manager import TacticalManager

__all__ = [
    "PortfolioRebalancer",
    "DividendCompounder",
    "CashflowAutopilot",
    "TacticalManager",
]

__version__ = "1.0.0"

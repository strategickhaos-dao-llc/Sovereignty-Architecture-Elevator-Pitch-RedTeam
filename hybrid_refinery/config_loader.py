"""
Strategickhaos Hybrid Refinery - Configuration Loader
Centralized configuration management to avoid duplication.
"""

import os
from pathlib import Path
from typing import Optional

import yaml

# Base directory for hybrid refinery
BASE_DIR = Path(__file__).parent

# Configuration file paths
RISK_CONFIG_PATH = BASE_DIR / 'risk.yaml'
SCREENS_CONFIG_PATH = BASE_DIR / 'screens.yaml'
FLOW_CONFIG_PATH = BASE_DIR / 'flow.yaml'

# Default values (used if config files not found)
DEFAULT_MONTHLY_CONTRIBUTION = 36.40
DEFAULT_DRIFT_THRESHOLD = 12.0
DEFAULT_ANNUAL_RETURN = 8.0
DEFAULT_DIVIDEND_GROWTH_RATE = 6.0
DEFAULT_INITIAL_INVESTMENT = 520.00


def load_yaml_config(path: Path) -> dict:
    """Load configuration from YAML file."""
    if not path.exists():
        return {}
    
    with open(path, 'r') as f:
        return yaml.safe_load(f) or {}


def get_risk_config() -> dict:
    """Load risk configuration."""
    return load_yaml_config(RISK_CONFIG_PATH)


def get_screens_config() -> dict:
    """Load screens configuration."""
    return load_yaml_config(SCREENS_CONFIG_PATH)


def get_flow_config() -> dict:
    """Load flow configuration."""
    return load_yaml_config(FLOW_CONFIG_PATH)


def get_monthly_contribution() -> float:
    """Get monthly contribution amount from config."""
    risk = get_risk_config()
    return risk.get('rebalancing_rules', {}).get('monthly_contribution', DEFAULT_MONTHLY_CONTRIBUTION)


def get_drift_threshold() -> float:
    """Get drift threshold from config."""
    risk = get_risk_config()
    return risk.get('rebalancing_rules', {}).get('drift_threshold', DEFAULT_DRIFT_THRESHOLD)


def get_annual_return_expectation() -> float:
    """Get expected annual return from config."""
    flow = get_flow_config()
    return flow.get('portfolio_metrics', {}).get('projections', {}).get('expected_annual_return', DEFAULT_ANNUAL_RETURN)


def get_dividend_growth_rate() -> float:
    """Get dividend growth rate from config."""
    flow = get_flow_config()
    return flow.get('portfolio_metrics', {}).get('projections', {}).get('dividend_growth_rate', DEFAULT_DIVIDEND_GROWTH_RATE)


def get_initial_investment() -> float:
    """Get initial investment amount.
    
    Calculates from portfolio holdings if not explicitly configured.
    """
    # Calculate from portfolio holdings (sum of cost basis)
    holdings = get_portfolio_holdings()
    if holdings:
        return sum(h.get('cost_basis', 0) for h in holdings.values())
    return DEFAULT_INITIAL_INVESTMENT


def get_portfolio_holdings() -> dict:
    """Get portfolio holdings from screens config."""
    screens = get_screens_config()
    return screens.get('current_holdings', {})


def get_alert_thresholds() -> dict:
    """Get alert thresholds from risk config."""
    risk = get_risk_config()
    return risk.get('alert_thresholds', {
        'position_drift_warning': 10.0,
        'position_drift_critical': 12.0
    })


# Convert screens.yaml holdings format to Python dict format
def get_portfolio_as_dict() -> dict:
    """Get portfolio holdings in standardized format for scripts."""
    holdings = get_portfolio_holdings()
    portfolio = {}
    
    for ticker, data in holdings.items():
        portfolio[ticker] = {
            'shares': data.get('shares', 0),
            'cost_basis': data.get('cost_basis', 0),
            'target_weight': data.get('target_weight', 0),
            'name': data.get('name', ticker),
            'sector': data.get('sector', 'Unknown'),
            'div_yield': data.get('div_yield', 0)
        }
        
    return portfolio


# Fallback portfolio if config not available
FALLBACK_PORTFOLIO = {
    'JPM': {'shares': 0.1555, 'cost_basis': 36.40, 'target_weight': 7.00, 'name': 'JPMorgan Chase', 'sector': 'Financials', 'div_yield': 2.2},
    'CB': {'shares': 0.1238, 'cost_basis': 36.40, 'target_weight': 7.01, 'name': 'Chubb Limited', 'sector': 'Financials', 'div_yield': 1.4},
    'TD': {'shares': 0.617, 'cost_basis': 36.40, 'target_weight': 7.00, 'name': 'Toronto-Dominion Bank', 'sector': 'Financials', 'div_yield': 5.1},
    'PG': {'shares': 0.244, 'cost_basis': 41.60, 'target_weight': 8.00, 'name': 'Procter & Gamble', 'sector': 'Consumer Staples', 'div_yield': 2.4},
    'KO': {'shares': 0.592, 'cost_basis': 41.60, 'target_weight': 8.00, 'name': 'Coca-Cola', 'sector': 'Consumer Staples', 'div_yield': 2.9},
    'PEP': {'shares': 0.206, 'cost_basis': 36.40, 'target_weight': 7.00, 'name': 'PepsiCo', 'sector': 'Consumer Staples', 'div_yield': 2.8},
    'CL': {'shares': 0.305, 'cost_basis': 31.20, 'target_weight': 6.00, 'name': 'Colgate-Palmolive', 'sector': 'Consumer Staples', 'div_yield': 2.2},
    'NEE': {'shares': 0.428, 'cost_basis': 36.40, 'target_weight': 7.00, 'name': 'NextEra Energy', 'sector': 'Utilities', 'div_yield': 2.6},
    'O': {'shares': 0.676, 'cost_basis': 41.60, 'target_weight': 8.01, 'name': 'Realty Income', 'sector': 'Real Estate', 'div_yield': 5.1},
    'VICI': {'shares': 1.112, 'cost_basis': 36.40, 'target_weight': 7.01, 'name': 'VICI Properties', 'sector': 'Real Estate', 'div_yield': 5.4},
    'PLD': {'shares': 0.267, 'cost_basis': 31.20, 'target_weight': 5.99, 'name': 'Prologis', 'sector': 'Real Estate', 'div_yield': 3.0},
    'ABBV': {'shares': 0.185, 'cost_basis': 36.40, 'target_weight': 7.00, 'name': 'AbbVie', 'sector': 'Healthcare', 'div_yield': 3.7},
    'JNJ': {'shares': 0.255, 'cost_basis': 41.60, 'target_weight': 8.00, 'name': 'Johnson & Johnson', 'sector': 'Healthcare', 'div_yield': 3.0},
    'XOM': {'shares': 0.255, 'cost_basis': 31.20, 'target_weight': 6.00, 'name': 'Exxon Mobil', 'sector': 'Energy', 'div_yield': 3.3},
    'WEC': {'shares': 0.387, 'cost_basis': 36.40, 'target_weight': 7.00, 'name': 'WEC Energy Group', 'sector': 'Utilities', 'div_yield': 3.7},
}


def get_portfolio() -> dict:
    """Get portfolio with fallback if config not available."""
    portfolio = get_portfolio_as_dict()
    return portfolio if portfolio else FALLBACK_PORTFOLIO

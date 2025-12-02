"""
DiviDen Ninja Bot - Configuration Module
Centralized configuration for dividend capture operations
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from enum import Enum


class TradingMode(Enum):
    """Trading mode configuration"""
    PAPER = "paper"           # Paper trading (simulation)
    LIVE = "live"             # Live trading with real capital
    HYBRID = "hybrid"         # Mix of paper and live


class RiskLevel(Enum):
    """Risk tolerance levels"""
    CONSERVATIVE = "conservative"
    MODERATE = "moderate"
    AGGRESSIVE = "aggressive"


@dataclass
class BrokerConfig:
    """Broker API configuration"""
    name: str = "alpaca"
    api_key: Optional[str] = None
    api_secret: Optional[str] = None
    base_url: str = "https://paper-api.alpaca.markets"
    
    # Rate limiting
    max_requests_per_minute: int = 200
    max_orders_per_day: int = 1000


@dataclass
class DataSourceConfig:
    """Market data source configuration"""
    provider: str = "polygon"  # polygon, yahoo, iex, etc.
    api_key: Optional[str] = None
    
    # Data preferences
    realtime: bool = True
    historical_days: int = 365
    dividend_lookback_days: int = 90


@dataclass 
class StrategyConfig:
    """Trading strategy parameters"""
    # Ex-dividend capture
    ex_div_min_yield: float = 0.02           # Minimum 2% dividend yield
    ex_div_max_position_size: float = 0.05   # Max 5% of portfolio per position
    ex_div_hold_days: int = 1                # Hold through ex-date
    
    # Special dividends
    special_div_min_amount: float = 1.0      # Minimum $1 special dividend
    special_div_announcement_window: int = 30 # Days to analyze after announcement
    
    # Merger arbitrage
    merger_min_spread: float = 0.02          # Minimum 2% arbitrage spread
    merger_max_time_to_close: int = 180      # Max 180 days to deal close
    
    # Options strategies
    options_enabled: bool = True
    options_max_delta: float = 0.30          # Max delta exposure
    options_min_premium: float = 0.50        # Min premium per contract


@dataclass
class RiskConfig:
    """Risk management configuration"""
    level: RiskLevel = RiskLevel.MODERATE
    
    # Position limits
    max_position_count: int = 20
    max_single_position_pct: float = 0.10    # 10% max single position
    max_sector_exposure_pct: float = 0.30    # 30% max sector exposure
    
    # Loss limits
    max_daily_loss_pct: float = 0.02         # 2% max daily loss
    max_drawdown_pct: float = 0.10           # 10% max drawdown
    stop_loss_pct: float = 0.05              # 5% stop loss per position
    
    # Volatility filters
    max_volatility: float = 0.50             # 50% max annualized vol
    min_liquidity_volume: int = 100000       # 100k min daily volume


@dataclass
class GovernanceConfig:
    """HLMCR Governance configuration"""
    enabled: bool = True
    
    # Approval thresholds
    auto_approve_below: float = 1000.0       # Auto-approve trades < $1000
    human_review_above: float = 10000.0      # Require human review > $10k
    
    # Audit settings
    log_all_decisions: bool = True
    decision_retention_days: int = 2555      # ~7 years retention
    
    # Emergency controls
    kill_switch_enabled: bool = True
    max_consecutive_losses: int = 5


@dataclass
class NotificationConfig:
    """Notification and reporting configuration"""
    # Discord integration
    discord_webhook: Optional[str] = None
    discord_channel_id: Optional[str] = None
    
    # Alert settings
    alert_on_trade: bool = True
    alert_on_error: bool = True
    daily_summary: bool = True
    weekly_report: bool = True
    
    # Email settings
    email_enabled: bool = False
    email_recipient: Optional[str] = None


@dataclass
class NonprofitConfig:
    """Nonprofit flow-through configuration"""
    enabled: bool = True
    
    # Auto-donation settings
    auto_donate_percentage: float = 0.07     # 7% auto-donate
    charity_verification_required: bool = True
    
    # Tax receipt generation
    generate_tax_receipts: bool = True
    receipt_template: str = "standard"
    
    # Beneficiary charities (verified anti-abuse organizations)
    verified_charities: List[str] = field(default_factory=lambda: [
        "National Center for Missing & Exploited Children",
        "RAINN (Rape, Abuse & Incest National Network)",
        "National Domestic Violence Hotline",
        "Cyber Civil Rights Initiative",
        "Electronic Frontier Foundation",
    ])


@dataclass
class DividendCaptureConfig:
    """Main configuration for Dividend Capture Bot"""
    # Operating mode
    mode: TradingMode = TradingMode.PAPER
    environment: str = "development"
    
    # Sub-configurations
    broker: BrokerConfig = field(default_factory=BrokerConfig)
    data_source: DataSourceConfig = field(default_factory=DataSourceConfig)
    strategy: StrategyConfig = field(default_factory=StrategyConfig)
    risk: RiskConfig = field(default_factory=RiskConfig)
    governance: GovernanceConfig = field(default_factory=GovernanceConfig)
    notifications: NotificationConfig = field(default_factory=NotificationConfig)
    nonprofit: NonprofitConfig = field(default_factory=NonprofitConfig)
    
    # Bot identification
    bot_id: str = "dividen-ninja-001"
    bot_version: str = "1.0.0"
    
    # Scheduling
    market_open_buffer_minutes: int = 5      # Wait 5 min after market open
    market_close_buffer_minutes: int = 15    # Stop 15 min before close
    scan_interval_minutes: int = 60          # Scan for opportunities hourly
    
    def validate(self) -> List[str]:
        """Validate configuration and return list of errors"""
        errors = []
        
        if self.mode == TradingMode.LIVE:
            if not self.broker.api_key:
                errors.append("Live trading requires broker API key")
            if not self.broker.api_secret:
                errors.append("Live trading requires broker API secret")
            if not self.governance.enabled:
                errors.append("Live trading requires HLMCR governance enabled")
        
        if self.nonprofit.enabled:
            if self.nonprofit.auto_donate_percentage < 0 or self.nonprofit.auto_donate_percentage > 1:
                errors.append("Auto-donate percentage must be between 0 and 1")
        
        if self.risk.max_single_position_pct > 0.25:
            errors.append("Max single position should not exceed 25% for risk management")
        
        return errors


# Global configuration instance
_config: Optional[DividendCaptureConfig] = None


def get_dividend_config() -> DividendCaptureConfig:
    """Get dividend capture configuration (singleton)"""
    global _config
    if _config is None:
        _config = DividendCaptureConfig()
    return _config


def load_config_from_file(path: str) -> DividendCaptureConfig:
    """Load configuration from YAML file"""
    import yaml
    
    with open(path, 'r') as f:
        data = yaml.safe_load(f)
    
    # Parse into config objects
    config = DividendCaptureConfig(
        mode=TradingMode(data.get('mode', 'paper')),
        environment=data.get('environment', 'development'),
        bot_id=data.get('bot_id', 'dividen-ninja-001'),
    )
    
    # Load sub-configurations if present
    if 'broker' in data:
        config.broker = BrokerConfig(**data['broker'])
    if 'strategy' in data:
        config.strategy = StrategyConfig(**data['strategy'])
    if 'risk' in data:
        config.risk = RiskConfig(**data['risk'])
    if 'governance' in data:
        config.governance = GovernanceConfig(**data['governance'])
    if 'nonprofit' in data:
        config.nonprofit = NonprofitConfig(**data['nonprofit'])
    
    return config

"""
Hybrid Refinery Configuration
=============================

Centralized configuration for the Strategickhaos Hybrid Refinery system.
Includes guardrails, risk parameters, and flow routing settings.
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from enum import Enum
import os


class SwarmGateDestination(Enum):
    """SwarmGate flow destination options"""
    SHORT_TERM_TREASURIES = "short_term_treasuries"
    CRYPTO_RESERVE = "crypto_reserve"
    AI_FUEL_ACCOUNT = "ai_fuel_account"
    MIXED = "mixed"
    AUTO_OPTIMAL = "auto_optimal"


class Priority(Enum):
    """Trade/signal priority levels"""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class ScreeningFilters:
    """Hard filters for dividend screening logic"""
    # Payout ratio filters
    max_payout_ratio: float = 0.70  # < 70% for regular stocks
    max_reit_ffo_payout: float = 0.80  # < 80% for REITs
    
    # Growth and stability filters
    min_dividend_cagr_5yr: float = 0.03  # > 3%
    min_interest_coverage: float = 4.0  # > 4×
    max_net_debt_ebitda: float = 3.0  # < 3× for regular stocks
    max_reit_net_debt_ebitda: float = 6.0  # < 6× for REITs
    
    # Economic profit filter
    min_roic_wacc_spread: float = 0.02  # ROIC - WACC > 2%
    
    # Liquidity filter
    min_adv_million: float = 1.0  # ADV > $1M
    
    # Earnings exclusion window
    earnings_exclusion_days: int = 5  # ±5 days around earnings


@dataclass
class PortfolioGuardrails:
    """Portfolio construction guardrails"""
    # Position limits
    max_positions: int = 25
    min_positions: int = 20
    max_position_weight: float = 0.05  # 5% max per position
    
    # Sector limits
    max_sector_weight: float = 0.25  # 25% max per sector
    
    # Tactical sleeve cap
    tactical_max_allocation: float = 0.15  # 15% of entire portfolio
    
    # Flow routing
    core_reinvest_pct: float = 0.70  # 70% to compounding core
    treasury_buffer_pct: float = 0.23  # 23% to treasury buffer
    swarmgate_pct: float = 0.07  # 7% to SwarmGate
    
    # Drawdown management
    max_drawdown_threshold: float = 0.12  # 12% triggers risk-off
    tactical_reduction_on_drawdown: float = 0.50  # Cut tactical by 50% on DD


@dataclass
class TacticalParameters:
    """RANCO/PID tactical engine parameters"""
    # Entry rules
    atr_compression_threshold: float = 1.0  # ATR% < 6-mo median
    rsi_entry_min: float = 45.0
    rsi_entry_max: float = 65.0
    
    # Moving average trend confirmation
    require_uptrend: bool = True  # 20 > 50 > 200
    
    # Risk management
    risk_per_trade_min: float = 0.005  # 0.5%
    risk_per_trade_max: float = 0.01  # 1.0%
    stop_atr_multiplier: float = 1.5  # Stop: 1.5× ATR
    trail_atr_multiplier: float = 2.0  # Trail: 2× ATR
    
    # Exit rules
    rsi_overbought_exit: float = 75.0  # Exit when RSI > 75 + lower high
    
    # Timeframe
    candle_timeframe: str = "weekly"  # Weekly candles only
    
    # Technical indicators
    atr_period: int = 14
    rsi_period: int = 14
    ma_short: int = 20
    ma_medium: int = 50
    ma_long: int = 200


@dataclass
class AutomationConfig:
    """Automation engine configuration"""
    # Scheduling
    nightly_cron_schedule: str = "0 22 * * *"  # 10 PM daily
    weekly_report_schedule: str = "0 8 * * 1"  # 8 AM Monday
    
    # Data sources
    data_provider: str = "yfinance"  # or "alpha_vantage", "polygon", etc.
    
    # Output paths
    output_directory: str = "./hybrid_refinery_output"
    csv_output_enabled: bool = True
    
    # Email configuration
    email_notifications_enabled: bool = True
    email_recipients: List[str] = field(default_factory=list)
    
    # Auto-trading
    auto_trading_enabled: bool = False
    buy_tranches: int = 3  # Buy core positions in 3 tranches


@dataclass
class HybridRefineryConfig:
    """Main configuration for the Hybrid Refinery system"""
    # Core settings
    name: str = "Strategickhaos Hybrid Refinery"
    version: str = "1.0.0"
    environment: str = "development"
    
    # Total capital (to be set by user)
    total_capital: float = 0.0
    
    # SwarmGate destination choice
    swarmgate_destination: SwarmGateDestination = SwarmGateDestination.AUTO_OPTIMAL
    
    # User's intuitive stock picks (to be filtered)
    user_stock_picks: List[str] = field(default_factory=list)
    
    # Sub-configurations
    screening: ScreeningFilters = field(default_factory=ScreeningFilters)
    guardrails: PortfolioGuardrails = field(default_factory=PortfolioGuardrails)
    tactical: TacticalParameters = field(default_factory=TacticalParameters)
    automation: AutomationConfig = field(default_factory=AutomationConfig)
    
    # Broker routing
    core_account_id: Optional[str] = None
    tactical_account_id: Optional[str] = None
    
    # API keys (loaded from environment)
    data_api_key: Optional[str] = field(default=None)
    broker_api_key: Optional[str] = field(default=None)
    
    def __post_init__(self):
        """Load API keys from environment if not provided"""
        if self.data_api_key is None:
            self.data_api_key = os.environ.get("HYBRID_REFINERY_DATA_API_KEY")
        if self.broker_api_key is None:
            self.broker_api_key = os.environ.get("HYBRID_REFINERY_BROKER_API_KEY")
    
    def validate(self) -> List[str]:
        """Validate configuration and return list of errors"""
        errors = []
        
        # Check flow routing sums to 100%
        total_flow = (
            self.guardrails.core_reinvest_pct +
            self.guardrails.treasury_buffer_pct +
            self.guardrails.swarmgate_pct
        )
        if abs(total_flow - 1.0) > 0.001:
            errors.append(f"Flow routing must sum to 100%, got {total_flow * 100:.1f}%")
        
        # Check tactical parameters
        if self.tactical.rsi_entry_min >= self.tactical.rsi_entry_max:
            errors.append("RSI entry min must be less than RSI entry max")
        
        if self.tactical.risk_per_trade_min > self.tactical.risk_per_trade_max:
            errors.append("Risk per trade min must not exceed max")
        
        # Check guardrails
        if self.guardrails.tactical_max_allocation > 0.20:
            errors.append("Tactical max allocation should not exceed 20%")
        
        if self.guardrails.max_position_weight * self.guardrails.min_positions < 1.0:
            errors.append("Position weight * min positions must allow full investment")
        
        return errors
    
    def calculate_allocations(self) -> Dict[str, float]:
        """Calculate actual dollar allocations based on total capital"""
        if self.total_capital <= 0:
            return {}
        
        core_capital = self.total_capital * (1 - self.guardrails.tactical_max_allocation)
        tactical_capital = self.total_capital * self.guardrails.tactical_max_allocation
        
        # Flow routing from dividends/income
        return {
            "core_capital": core_capital,
            "tactical_capital": tactical_capital,
            "core_reinvest_target": core_capital * self.guardrails.core_reinvest_pct,
            "treasury_buffer_target": core_capital * self.guardrails.treasury_buffer_pct,
            "swarmgate_target": core_capital * self.guardrails.swarmgate_pct,
            "per_position_max": self.total_capital * self.guardrails.max_position_weight,
            "tactical_per_trade_max": tactical_capital * self.tactical.risk_per_trade_max,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "HybridRefineryConfig":
        """Create config from dictionary"""
        screening = ScreeningFilters(**data.pop("screening", {}))
        guardrails = PortfolioGuardrails(**data.pop("guardrails", {}))
        tactical = TacticalParameters(**data.pop("tactical", {}))
        automation = AutomationConfig(**data.pop("automation", {}))
        
        if "swarmgate_destination" in data:
            data["swarmgate_destination"] = SwarmGateDestination(data["swarmgate_destination"])
        
        return cls(
            screening=screening,
            guardrails=guardrails,
            tactical=tactical,
            automation=automation,
            **data
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary"""
        return {
            "name": self.name,
            "version": self.version,
            "environment": self.environment,
            "total_capital": self.total_capital,
            "swarmgate_destination": self.swarmgate_destination.value,
            "user_stock_picks": self.user_stock_picks,
            "screening": {
                "max_payout_ratio": self.screening.max_payout_ratio,
                "max_reit_ffo_payout": self.screening.max_reit_ffo_payout,
                "min_dividend_cagr_5yr": self.screening.min_dividend_cagr_5yr,
                "min_interest_coverage": self.screening.min_interest_coverage,
                "max_net_debt_ebitda": self.screening.max_net_debt_ebitda,
                "max_reit_net_debt_ebitda": self.screening.max_reit_net_debt_ebitda,
                "min_roic_wacc_spread": self.screening.min_roic_wacc_spread,
                "min_adv_million": self.screening.min_adv_million,
                "earnings_exclusion_days": self.screening.earnings_exclusion_days,
            },
            "guardrails": {
                "max_positions": self.guardrails.max_positions,
                "min_positions": self.guardrails.min_positions,
                "max_position_weight": self.guardrails.max_position_weight,
                "max_sector_weight": self.guardrails.max_sector_weight,
                "tactical_max_allocation": self.guardrails.tactical_max_allocation,
                "core_reinvest_pct": self.guardrails.core_reinvest_pct,
                "treasury_buffer_pct": self.guardrails.treasury_buffer_pct,
                "swarmgate_pct": self.guardrails.swarmgate_pct,
                "max_drawdown_threshold": self.guardrails.max_drawdown_threshold,
                "tactical_reduction_on_drawdown": self.guardrails.tactical_reduction_on_drawdown,
            },
            "tactical": {
                "atr_compression_threshold": self.tactical.atr_compression_threshold,
                "rsi_entry_min": self.tactical.rsi_entry_min,
                "rsi_entry_max": self.tactical.rsi_entry_max,
                "require_uptrend": self.tactical.require_uptrend,
                "risk_per_trade_min": self.tactical.risk_per_trade_min,
                "risk_per_trade_max": self.tactical.risk_per_trade_max,
                "stop_atr_multiplier": self.tactical.stop_atr_multiplier,
                "trail_atr_multiplier": self.tactical.trail_atr_multiplier,
                "rsi_overbought_exit": self.tactical.rsi_overbought_exit,
                "candle_timeframe": self.tactical.candle_timeframe,
                "atr_period": self.tactical.atr_period,
                "rsi_period": self.tactical.rsi_period,
                "ma_short": self.tactical.ma_short,
                "ma_medium": self.tactical.ma_medium,
                "ma_long": self.tactical.ma_long,
            },
            "automation": {
                "nightly_cron_schedule": self.automation.nightly_cron_schedule,
                "weekly_report_schedule": self.automation.weekly_report_schedule,
                "data_provider": self.automation.data_provider,
                "output_directory": self.automation.output_directory,
                "csv_output_enabled": self.automation.csv_output_enabled,
                "email_notifications_enabled": self.automation.email_notifications_enabled,
                "email_recipients": self.automation.email_recipients,
                "auto_trading_enabled": self.automation.auto_trading_enabled,
                "buy_tranches": self.automation.buy_tranches,
            },
            "core_account_id": self.core_account_id,
            "tactical_account_id": self.tactical_account_id,
        }

"""
RANCO/PID Tactical Engine
=========================

The Tactical Sleeve of the Hybrid Refinery system.
Small, lethal, mechanical trades with strict risk management.

Purpose: Mechanical attack mode for volatility-driven opportunities
Cap: 15% of entire portfolio

Entry Rules:
    - ATR% < 6-mo median (volatility compression ready to expand)
    - Uptrend: 20 > 50 > 200
    - RSI 45-65 (momentum but not overbought)
    - Higher low forms (structural confirmation)

Risk & Stop:
    - Risk per trade: 0.5-1.0%
    - Stop: 1.5× ATR
    - Trail: 2× ATR
    - Exit: Trail hit OR RSI > 75 then first lower high

Timeframe: Weekly candles only
"""

from dataclasses import dataclass, field
from datetime import datetime, date
from typing import List, Dict, Any, Optional
from enum import Enum
import structlog

from .config import HybridRefineryConfig, TacticalParameters

logger = structlog.get_logger()


class SignalType(Enum):
    """Type of tactical signal"""
    ENTRY = "entry"
    EXIT = "exit"
    TRAIL_UPDATE = "trail_update"
    STOP_HIT = "stop_hit"
    RSI_EXIT = "rsi_exit"


class SignalStrength(Enum):
    """Strength of the signal"""
    WEAK = "weak"
    MODERATE = "moderate"
    STRONG = "strong"


class TradeStatus(Enum):
    """Status of a tactical trade"""
    PENDING = "pending"
    OPEN = "open"
    TRAILING = "trailing"
    CLOSED = "closed"
    STOPPED = "stopped"


@dataclass
class TechnicalIndicators:
    """Technical indicators for tactical analysis"""
    # Price data
    current_price: float
    high_52w: float
    low_52w: float
    
    # Moving averages
    ma_20: float
    ma_50: float
    ma_200: float
    
    # ATR (Average True Range)
    atr_14: float
    atr_pct: float  # ATR as percentage of price
    atr_6mo_median: float  # 6-month median ATR%
    
    # RSI
    rsi_14: float
    
    # Volume
    average_daily_volume: float
    volume_today: float
    
    # Structure
    recent_higher_low: bool = False
    recent_lower_high: bool = False
    
    @property
    def is_uptrend(self) -> bool:
        """Check if in uptrend (20 > 50 > 200)"""
        return self.ma_20 > self.ma_50 > self.ma_200
    
    @property
    def is_atr_compressed(self) -> bool:
        """Check if ATR is below 6-month median (volatility compression)"""
        return self.atr_pct < self.atr_6mo_median
    
    @property
    def is_rsi_in_range(self) -> bool:
        """Check if RSI is in entry range (45-65)"""
        return 45 <= self.rsi_14 <= 65
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "current_price": self.current_price,
            "high_52w": self.high_52w,
            "low_52w": self.low_52w,
            "ma_20": self.ma_20,
            "ma_50": self.ma_50,
            "ma_200": self.ma_200,
            "atr_14": self.atr_14,
            "atr_pct": self.atr_pct,
            "atr_6mo_median": self.atr_6mo_median,
            "rsi_14": self.rsi_14,
            "average_daily_volume": self.average_daily_volume,
            "volume_today": self.volume_today,
            "is_uptrend": self.is_uptrend,
            "is_atr_compressed": self.is_atr_compressed,
            "is_rsi_in_range": self.is_rsi_in_range,
            "recent_higher_low": self.recent_higher_low,
            "recent_lower_high": self.recent_lower_high,
        }


@dataclass
class TacticalSignal:
    """A tactical trading signal"""
    symbol: str
    signal_type: SignalType
    strength: SignalStrength
    
    # Entry/exit details
    entry_price: Optional[float] = None
    stop_price: Optional[float] = None
    trail_price: Optional[float] = None
    target_price: Optional[float] = None
    
    # Risk calculations
    risk_amount: Optional[float] = None
    position_size: Optional[int] = None
    risk_reward_ratio: Optional[float] = None
    
    # Indicators at signal time
    indicators: Optional[TechnicalIndicators] = None
    
    # Metadata
    timestamp: datetime = field(default_factory=datetime.now)
    notes: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "symbol": self.symbol,
            "signal_type": self.signal_type.value,
            "strength": self.strength.value,
            "entry_price": self.entry_price,
            "stop_price": self.stop_price,
            "trail_price": self.trail_price,
            "target_price": self.target_price,
            "risk_amount": self.risk_amount,
            "position_size": self.position_size,
            "risk_reward_ratio": self.risk_reward_ratio,
            "indicators": self.indicators.to_dict() if self.indicators else None,
            "timestamp": self.timestamp.isoformat(),
            "notes": self.notes,
        }


@dataclass
class TradeSetup:
    """A complete trade setup with all parameters"""
    symbol: str
    direction: str = "long"  # For now, only long positions
    
    # Entry
    entry_price: float = 0.0
    entry_shares: int = 0
    entry_value: float = 0.0
    
    # Stop loss
    initial_stop: float = 0.0
    current_stop: float = 0.0
    stop_distance_atr: float = 0.0
    
    # Trailing stop
    trail_distance_atr: float = 0.0
    trail_trigger_price: float = 0.0
    
    # Risk management
    risk_per_trade: float = 0.0
    risk_amount: float = 0.0
    max_loss: float = 0.0
    
    # Status
    status: TradeStatus = TradeStatus.PENDING
    
    # Timestamps
    signal_timestamp: datetime = field(default_factory=datetime.now)
    entry_timestamp: Optional[datetime] = None
    exit_timestamp: Optional[datetime] = None
    
    # Results
    exit_price: Optional[float] = None
    realized_pnl: Optional[float] = None
    realized_pnl_pct: Optional[float] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "symbol": self.symbol,
            "direction": self.direction,
            "entry_price": self.entry_price,
            "entry_shares": self.entry_shares,
            "entry_value": self.entry_value,
            "initial_stop": self.initial_stop,
            "current_stop": self.current_stop,
            "stop_distance_atr": self.stop_distance_atr,
            "trail_distance_atr": self.trail_distance_atr,
            "trail_trigger_price": self.trail_trigger_price,
            "risk_per_trade": self.risk_per_trade,
            "risk_amount": self.risk_amount,
            "max_loss": self.max_loss,
            "status": self.status.value,
            "signal_timestamp": self.signal_timestamp.isoformat(),
            "entry_timestamp": self.entry_timestamp.isoformat() if self.entry_timestamp else None,
            "exit_timestamp": self.exit_timestamp.isoformat() if self.exit_timestamp else None,
            "exit_price": self.exit_price,
            "realized_pnl": self.realized_pnl,
            "realized_pnl_pct": self.realized_pnl_pct,
        }


class RANCOPIDEngine:
    """
    RANCO/PID Tactical Engine
    
    Purpose: Small, lethal, mechanical trades
    Constraint: Max 15% of portfolio
    
    Entry criteria:
        - ATR compression (ready to expand)
        - Uptrend confirmed (20 > 50 > 200)
        - RSI in sweet spot (45-65)
        - Higher low structure
    
    Risk management:
        - 0.5-1.0% risk per trade
        - Stop: 1.5× ATR
        - Trail: 2× ATR
        - Exit: Trail OR RSI>75 + lower high
    """
    
    def __init__(self, config: HybridRefineryConfig):
        self.config = config
        self.params = config.tactical
        self.active_trades: List[TradeSetup] = []
        self.closed_trades: List[TradeSetup] = []
        self.signals: List[TacticalSignal] = []
        
        # Calculate tactical capital allocation
        self.max_tactical_capital = config.total_capital * config.guardrails.tactical_max_allocation
        self.current_exposure = 0.0
        
        logger.info("RANCO/PID Engine initialized",
                   max_capital=self.max_tactical_capital,
                   max_allocation_pct=f"{config.guardrails.tactical_max_allocation:.0%}")
    
    def scan_for_entry(self, indicators: TechnicalIndicators, symbol: str) -> Optional[TacticalSignal]:
        """
        Scan a stock for potential entry signal
        
        Entry Rules:
            - ATR% < 6-mo median (volatility compression)
            - Uptrend: 20 > 50 > 200
            - RSI 45-65 (momentum but not overbought)
            - Higher low forms (structural confirmation)
        """
        entry_criteria = {}
        notes = []
        
        # 1. ATR compression check
        atr_ok = indicators.atr_pct < indicators.atr_6mo_median * self.params.atr_compression_threshold
        entry_criteria["atr_compression"] = atr_ok
        if atr_ok:
            notes.append(f"ATR compressed: {indicators.atr_pct:.2%} < median {indicators.atr_6mo_median:.2%}")
        else:
            notes.append(f"ATR not compressed: {indicators.atr_pct:.2%} >= median {indicators.atr_6mo_median:.2%}")
        
        # 2. Uptrend check
        uptrend_ok = indicators.is_uptrend if self.params.require_uptrend else True
        entry_criteria["uptrend"] = uptrend_ok
        if uptrend_ok:
            notes.append(f"Uptrend confirmed: MA20 {indicators.ma_20:.2f} > MA50 {indicators.ma_50:.2f} > MA200 {indicators.ma_200:.2f}")
        else:
            notes.append("No uptrend: MAs not aligned")
        
        # 3. RSI range check
        rsi_ok = self.params.rsi_entry_min <= indicators.rsi_14 <= self.params.rsi_entry_max
        entry_criteria["rsi_range"] = rsi_ok
        if rsi_ok:
            notes.append(f"RSI in range: {indicators.rsi_14:.1f} (target: {self.params.rsi_entry_min}-{self.params.rsi_entry_max})")
        else:
            notes.append(f"RSI out of range: {indicators.rsi_14:.1f}")
        
        # 4. Higher low structure
        higher_low_ok = indicators.recent_higher_low
        entry_criteria["higher_low"] = higher_low_ok
        if higher_low_ok:
            notes.append("Higher low structure confirmed")
        else:
            notes.append("No higher low structure detected")
        
        # All criteria must pass
        all_criteria_met = all(entry_criteria.values())
        
        if all_criteria_met:
            # Calculate signal strength
            strength = self._calculate_signal_strength(indicators, entry_criteria)
            
            # Create entry signal
            signal = TacticalSignal(
                symbol=symbol,
                signal_type=SignalType.ENTRY,
                strength=strength,
                entry_price=indicators.current_price,
                stop_price=indicators.current_price - (indicators.atr_14 * self.params.stop_atr_multiplier),
                indicators=indicators,
                notes=notes,
            )
            
            self.signals.append(signal)
            
            logger.info("Entry signal generated",
                       symbol=symbol,
                       strength=strength.value,
                       entry=signal.entry_price,
                       stop=signal.stop_price)
            
            return signal
        
        logger.debug("No entry signal",
                    symbol=symbol,
                    criteria=entry_criteria)
        
        return None
    
    def _calculate_signal_strength(
        self, 
        indicators: TechnicalIndicators, 
        criteria: Dict[str, bool]
    ) -> SignalStrength:
        """Calculate signal strength based on criteria quality"""
        score = 0
        
        # ATR compression depth
        compression_ratio = indicators.atr_pct / indicators.atr_6mo_median
        if compression_ratio < 0.7:
            score += 2  # Very compressed
        elif compression_ratio < 0.9:
            score += 1  # Moderately compressed
        
        # RSI position (favor middle of range)
        rsi_mid = (self.params.rsi_entry_min + self.params.rsi_entry_max) / 2
        rsi_deviation = abs(indicators.rsi_14 - rsi_mid)
        if rsi_deviation < 5:
            score += 2  # Very centered
        elif rsi_deviation < 10:
            score += 1  # Moderately centered
        
        # Trend strength
        if indicators.current_price > indicators.ma_20 > indicators.ma_50 > indicators.ma_200:
            ma_20_distance = (indicators.current_price - indicators.ma_20) / indicators.ma_20
            if 0 < ma_20_distance < 0.03:
                score += 2  # Close to MA20 (good entry)
            elif 0.03 <= ma_20_distance < 0.06:
                score += 1  # Moderate distance
        
        # Higher low confirmation
        if indicators.recent_higher_low:
            score += 1
        
        if score >= 5:
            return SignalStrength.STRONG
        elif score >= 3:
            return SignalStrength.MODERATE
        else:
            return SignalStrength.WEAK
    
    def create_trade_setup(
        self, 
        signal: TacticalSignal, 
        account_capital: float
    ) -> TradeSetup:
        """
        Create a complete trade setup from a signal
        
        Risk Management:
            - Risk per trade: 0.5-1.0%
            - Stop: 1.5× ATR
            - Trail: 2× ATR
        """
        indicators = signal.indicators
        
        # Calculate stop distance (1.5× ATR)
        stop_distance = indicators.atr_14 * self.params.stop_atr_multiplier
        stop_price = signal.entry_price - stop_distance
        
        # Calculate risk amount (use middle of range for balanced approach)
        risk_pct = (self.params.risk_per_trade_min + self.params.risk_per_trade_max) / 2
        
        # Adjust risk based on signal strength
        if signal.strength == SignalStrength.STRONG:
            risk_pct = self.params.risk_per_trade_max
        elif signal.strength == SignalStrength.WEAK:
            risk_pct = self.params.risk_per_trade_min
        
        risk_amount = account_capital * risk_pct
        
        # Calculate position size based on risk
        risk_per_share = signal.entry_price - stop_price
        position_size = int(risk_amount / risk_per_share) if risk_per_share > 0 else 0
        
        # Cap position size to stay within tactical allocation
        max_position_value = self.max_tactical_capital - self.current_exposure
        max_shares = int(max_position_value / signal.entry_price) if signal.entry_price > 0 else 0
        position_size = min(position_size, max_shares)
        
        # Calculate trailing stop parameters
        trail_distance = indicators.atr_14 * self.params.trail_atr_multiplier
        
        setup = TradeSetup(
            symbol=signal.symbol,
            entry_price=signal.entry_price,
            entry_shares=position_size,
            entry_value=position_size * signal.entry_price,
            initial_stop=stop_price,
            current_stop=stop_price,
            stop_distance_atr=self.params.stop_atr_multiplier,
            trail_distance_atr=self.params.trail_atr_multiplier,
            trail_trigger_price=signal.entry_price + trail_distance,
            risk_per_trade=risk_pct,
            risk_amount=risk_amount,
            max_loss=position_size * risk_per_share,
            status=TradeStatus.PENDING,
            signal_timestamp=signal.timestamp,
        )
        
        # Update signal with position details
        signal.risk_amount = risk_amount
        signal.position_size = position_size
        signal.risk_reward_ratio = trail_distance / risk_per_share if risk_per_share > 0 else 0
        
        logger.info("Trade setup created",
                   symbol=setup.symbol,
                   shares=setup.entry_shares,
                   value=setup.entry_value,
                   stop=setup.initial_stop,
                   risk_amount=setup.risk_amount)
        
        return setup
    
    def execute_entry(self, setup: TradeSetup) -> bool:
        """
        Execute entry for a trade setup
        
        Returns:
            True if entry was successful
        """
        # Check if we have capacity
        if self.current_exposure + setup.entry_value > self.max_tactical_capital:
            logger.warning("Cannot execute entry - tactical allocation exceeded",
                         current=self.current_exposure,
                         requested=setup.entry_value,
                         max=self.max_tactical_capital)
            return False
        
        setup.status = TradeStatus.OPEN
        setup.entry_timestamp = datetime.now()
        
        self.active_trades.append(setup)
        self.current_exposure += setup.entry_value
        
        logger.info("Entry executed",
                   symbol=setup.symbol,
                   shares=setup.entry_shares,
                   price=setup.entry_price,
                   exposure=self.current_exposure)
        
        return True
    
    def check_exit_conditions(
        self, 
        trade: TradeSetup, 
        current_indicators: TechnicalIndicators
    ) -> Optional[TacticalSignal]:
        """
        Check exit conditions for an open trade
        
        Exit Rules:
            - Stop hit (1.5× ATR)
            - Trail hit (2× ATR)
            - RSI > 75 + lower high
        """
        current_price = current_indicators.current_price
        
        # 1. Check stop loss
        if current_price <= trade.current_stop:
            return TacticalSignal(
                symbol=trade.symbol,
                signal_type=SignalType.STOP_HIT,
                strength=SignalStrength.STRONG,
                entry_price=trade.entry_price,
                indicators=current_indicators,
                notes=[f"Stop hit at {trade.current_stop:.2f}"]
            )
        
        # 2. Check RSI exit condition (RSI > 75 + lower high)
        if current_indicators.rsi_14 > self.params.rsi_overbought_exit:
            if current_indicators.recent_lower_high:
                return TacticalSignal(
                    symbol=trade.symbol,
                    signal_type=SignalType.RSI_EXIT,
                    strength=SignalStrength.STRONG,
                    entry_price=trade.entry_price,
                    indicators=current_indicators,
                    notes=[
                        f"RSI overbought: {current_indicators.rsi_14:.1f} > {self.params.rsi_overbought_exit}",
                        "Lower high confirmed - exit signal"
                    ]
                )
        
        # 3. Update trailing stop if applicable
        if trade.status == TradeStatus.TRAILING:
            # Trail follows price up
            new_trail = current_price - (current_indicators.atr_14 * self.params.trail_atr_multiplier)
            if new_trail > trade.current_stop:
                trade.current_stop = new_trail
                logger.debug("Trail updated",
                           symbol=trade.symbol,
                           new_stop=new_trail)
        
        # 4. Check if should start trailing
        if trade.status == TradeStatus.OPEN and current_price >= trade.trail_trigger_price:
            trade.status = TradeStatus.TRAILING
            trail_stop = current_price - (current_indicators.atr_14 * self.params.trail_atr_multiplier)
            trade.current_stop = max(trade.current_stop, trail_stop)
            
            return TacticalSignal(
                symbol=trade.symbol,
                signal_type=SignalType.TRAIL_UPDATE,
                strength=SignalStrength.MODERATE,
                trail_price=trade.current_stop,
                indicators=current_indicators,
                notes=[f"Trailing stop activated at {trade.current_stop:.2f}"]
            )
        
        return None
    
    def execute_exit(self, trade: TradeSetup, exit_price: float, exit_type: str) -> TradeSetup:
        """
        Execute exit for a trade
        
        Args:
            trade: The trade to close
            exit_price: Price at exit
            exit_type: Reason for exit (stop_hit, trail_hit, rsi_exit, manual)
        """
        trade.exit_price = exit_price
        trade.exit_timestamp = datetime.now()
        trade.status = TradeStatus.CLOSED if exit_type != "stop_hit" else TradeStatus.STOPPED
        
        # Calculate P&L
        trade.realized_pnl = (exit_price - trade.entry_price) * trade.entry_shares
        trade.realized_pnl_pct = (exit_price - trade.entry_price) / trade.entry_price if trade.entry_price > 0 else 0
        
        # Update exposure
        self.current_exposure -= trade.entry_value
        
        # Move to closed trades
        if trade in self.active_trades:
            self.active_trades.remove(trade)
        self.closed_trades.append(trade)
        
        logger.info("Exit executed",
                   symbol=trade.symbol,
                   exit_type=exit_type,
                   exit_price=exit_price,
                   pnl=trade.realized_pnl,
                   pnl_pct=f"{trade.realized_pnl_pct:.1%}")
        
        return trade
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Calculate performance metrics for tactical trades"""
        if not self.closed_trades:
            return {
                "total_trades": 0,
                "win_rate": 0.0,
                "total_pnl": 0.0,
                "avg_win": 0.0,
                "avg_loss": 0.0,
                "profit_factor": 0.0,
                "expectancy": 0.0,
            }
        
        winners = [t for t in self.closed_trades if t.realized_pnl and t.realized_pnl > 0]
        losers = [t for t in self.closed_trades if t.realized_pnl and t.realized_pnl <= 0]
        
        total_trades = len(self.closed_trades)
        win_rate = len(winners) / total_trades if total_trades > 0 else 0
        
        total_pnl = sum(t.realized_pnl or 0 for t in self.closed_trades)
        
        avg_win = sum(t.realized_pnl or 0 for t in winners) / len(winners) if winners else 0
        avg_loss = abs(sum(t.realized_pnl or 0 for t in losers) / len(losers)) if losers else 0
        
        total_gains = sum(t.realized_pnl or 0 for t in winners)
        total_losses = abs(sum(t.realized_pnl or 0 for t in losers))
        profit_factor = total_gains / total_losses if total_losses > 0 else float('inf')
        
        expectancy = (win_rate * avg_win) - ((1 - win_rate) * avg_loss)
        
        return {
            "total_trades": total_trades,
            "winning_trades": len(winners),
            "losing_trades": len(losers),
            "win_rate": win_rate,
            "total_pnl": total_pnl,
            "avg_win": avg_win,
            "avg_loss": avg_loss,
            "profit_factor": profit_factor,
            "expectancy": expectancy,
            "current_exposure": self.current_exposure,
            "max_tactical_capital": self.max_tactical_capital,
            "utilization": self.current_exposure / self.max_tactical_capital if self.max_tactical_capital > 0 else 0,
        }
    
    def apply_drawdown_reduction(self, current_drawdown: float) -> bool:
        """
        Apply drawdown risk-off throttling
        
        If DD > 12%: Cut tactical size in half
        """
        threshold = self.config.guardrails.max_drawdown_threshold
        reduction = self.config.guardrails.tactical_reduction_on_drawdown
        
        if current_drawdown > threshold:
            old_max = self.max_tactical_capital
            self.max_tactical_capital = old_max * (1 - reduction)
            
            logger.warning("Drawdown throttle applied",
                         drawdown=f"{current_drawdown:.1%}",
                         threshold=f"{threshold:.0%}",
                         old_capital=old_max,
                         new_capital=self.max_tactical_capital)
            
            return True
        
        return False
    
    def reset_drawdown_reduction(self):
        """Reset tactical capital after recovery"""
        self.max_tactical_capital = self.config.total_capital * self.config.guardrails.tactical_max_allocation
        
        logger.info("Drawdown recovery - tactical capital restored",
                   capital=self.max_tactical_capital)

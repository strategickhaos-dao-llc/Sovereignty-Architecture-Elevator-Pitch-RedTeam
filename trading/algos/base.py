"""
Trading Arsenal - Base Algorithm Module
Implements rank-based trading strategies for StrategicKhaos DAO LLC
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional, Any
import logging

import numpy as np
import pandas as pd


class AlgoStatus(Enum):
    """Algorithm status states"""
    INACTIVE = "inactive"
    INITIALIZING = "initializing"
    RUNNING = "running"
    PAUSED = "paused"
    ERROR = "error"
    STOPPED = "stopped"


class SignalType(Enum):
    """Trading signal types"""
    LONG = "long"
    SHORT = "short"
    NEUTRAL = "neutral"
    REDUCE = "reduce"


@dataclass
class TradingSignal:
    """Individual trading signal"""
    symbol: str
    signal_type: SignalType
    weight: float
    rank: int
    score: float
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "symbol": self.symbol,
            "signal_type": self.signal_type.value,
            "weight": self.weight,
            "rank": self.rank,
            "score": self.score,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata
        }


@dataclass
class AlgoConfig:
    """Algorithm configuration"""
    algo_id: int
    name: str
    readiness: float
    yield_target: float
    max_position_pct: float = 0.05
    max_drawdown: float = 0.20
    rebalance_frequency: str = "monthly"
    universe: List[str] = field(default_factory=list)
    enabled: bool = True
    
    @classmethod
    def from_yaml(cls, data: Dict[str, Any]) -> "AlgoConfig":
        return cls(
            algo_id=data.get("id", 0),
            name=data.get("name", "Unknown"),
            readiness=data.get("readiness", 0.0),
            yield_target=data.get("yield_annualized", 0.07),
            max_position_pct=0.05,
            max_drawdown=0.20,
            enabled=data.get("readiness", 0.0) >= 0.80
        )


@dataclass
class RiskMetrics:
    """Risk metrics for an algorithm"""
    current_drawdown: float = 0.0
    max_drawdown: float = 0.0
    volatility_30d: float = 0.0
    sharpe_ratio: float = 0.0
    position_concentration: float = 0.0
    
    def is_within_limits(self, config: AlgoConfig) -> bool:
        """Check if risk metrics are within configured limits"""
        return self.current_drawdown < config.max_drawdown


class BaseAlgo(ABC):
    """Base class for all trading algorithms"""
    
    def __init__(self, config: AlgoConfig):
        self.config = config
        self.status = AlgoStatus.INACTIVE
        self.logger = logging.getLogger(f"algo.{config.name}")
        self.risk_metrics = RiskMetrics()
        self._last_signals: List[TradingSignal] = []
        self._last_run: Optional[datetime] = None
        
    @property
    def algo_id(self) -> int:
        return self.config.algo_id
    
    @property
    def name(self) -> str:
        return self.config.name
    
    @property
    def is_ready(self) -> bool:
        return self.config.readiness >= 0.80
    
    @abstractmethod
    def compute_signals(self, market_data: pd.DataFrame) -> List[TradingSignal]:
        """Compute trading signals from market data"""
        pass
    
    @abstractmethod
    def compute_ranks(self, market_data: pd.DataFrame) -> pd.Series:
        """Compute rankings for assets"""
        pass
    
    def run(self, market_data: pd.DataFrame) -> List[TradingSignal]:
        """Execute the algorithm and return signals"""
        if not self.config.enabled:
            self.logger.warning(f"Algorithm {self.name} is disabled")
            return []
        
        if not self.is_ready:
            self.logger.warning(f"Algorithm {self.name} is not ready (readiness={self.config.readiness})")
            return []
        
        try:
            self.status = AlgoStatus.RUNNING
            self._last_run = datetime.now(timezone.utc)
            
            # Compute signals
            signals = self.compute_signals(market_data)
            
            # Apply risk controls
            signals = self._apply_risk_controls(signals)
            
            self._last_signals = signals
            self.status = AlgoStatus.RUNNING
            
            self.logger.info(f"Generated {len(signals)} signals")
            return signals
            
        except Exception as e:
            self.status = AlgoStatus.ERROR
            self.logger.error(f"Error running algorithm: {e}")
            raise
    
    def _apply_risk_controls(self, signals: List[TradingSignal]) -> List[TradingSignal]:
        """Apply risk controls to signals"""
        if not self.risk_metrics.is_within_limits(self.config):
            self.logger.warning("Risk limits exceeded, reducing positions")
            return [
                TradingSignal(
                    symbol=s.symbol,
                    signal_type=SignalType.REDUCE,
                    weight=s.weight * 0.5,
                    rank=s.rank,
                    score=s.score,
                    metadata={"risk_adjusted": True}
                )
                for s in signals
            ]
        
        # Cap individual position weights
        controlled = []
        for signal in signals:
            capped_weight = min(signal.weight, self.config.max_position_pct)
            controlled.append(TradingSignal(
                symbol=signal.symbol,
                signal_type=signal.signal_type,
                weight=capped_weight,
                rank=signal.rank,
                score=signal.score,
                metadata=signal.metadata
            ))
        
        return controlled
    
    def get_status(self) -> Dict[str, Any]:
        """Get current algorithm status"""
        return {
            "algo_id": self.algo_id,
            "name": self.name,
            "status": self.status.value,
            "readiness": self.config.readiness,
            "enabled": self.config.enabled,
            "last_run": self._last_run.isoformat() if self._last_run else None,
            "signal_count": len(self._last_signals),
            "risk_metrics": {
                "current_drawdown": self.risk_metrics.current_drawdown,
                "max_drawdown": self.risk_metrics.max_drawdown,
                "sharpe_ratio": self.risk_metrics.sharpe_ratio
            }
        }


class SimpleMomentumRank(BaseAlgo):
    """
    Tier 0 Algorithm #1: Simple Momentum Rank
    Rank by 12-month returns, long top 20%
    """
    
    def __init__(self, config: AlgoConfig, lookback_months: int = 12, top_percentile: float = 0.20):
        super().__init__(config)
        self.lookback_months = lookback_months
        self.top_percentile = top_percentile
    
    def compute_ranks(self, market_data: pd.DataFrame) -> pd.Series:
        """Compute momentum ranks based on 12-month returns"""
        # Calculate lookback returns
        lookback_days = self.lookback_months * 21  # Approx trading days
        
        if 'close' not in market_data.columns:
            raise ValueError("Market data must contain 'close' column")
        
        returns = market_data['close'].pct_change(periods=lookback_days)
        
        # Rank by returns (higher is better)
        ranks = returns.rank(ascending=False, pct=True)
        
        return ranks
    
    def compute_signals(self, market_data: pd.DataFrame) -> List[TradingSignal]:
        """Generate signals for top percentile assets"""
        ranks = self.compute_ranks(market_data)
        
        signals = []
        symbols = market_data.get('symbol', market_data.index)
        
        for i, (symbol, rank_pct) in enumerate(zip(symbols, ranks)):
            if pd.isna(rank_pct):
                continue
                
            if rank_pct <= self.top_percentile:
                # Top 20% - long signal
                weight = (1 - rank_pct) * self.config.max_position_pct
                signals.append(TradingSignal(
                    symbol=str(symbol),
                    signal_type=SignalType.LONG,
                    weight=weight,
                    rank=int((1 - rank_pct) * 100),
                    score=float(1 - rank_pct),
                    metadata={"algo": "simple_momentum"}
                ))
            else:
                # Not in top 20% - neutral
                signals.append(TradingSignal(
                    symbol=str(symbol),
                    signal_type=SignalType.NEUTRAL,
                    weight=0.0,
                    rank=int((1 - rank_pct) * 100),
                    score=float(1 - rank_pct)
                ))
        
        return signals


class DualMomentumRank(BaseAlgo):
    """
    Tier 0 Algorithm #2: Dual Momentum Rank
    Switch risk-on/off vs bonds/cash based on relative and absolute momentum
    """
    
    def __init__(self, config: AlgoConfig, lookback_months: int = 12):
        super().__init__(config)
        self.lookback_months = lookback_months
        self.risk_on = True
        self.regime = "risk_on"
    
    def compute_ranks(self, market_data: pd.DataFrame) -> pd.Series:
        """Compute dual momentum ranks"""
        lookback_days = self.lookback_months * 21
        
        returns = market_data['close'].pct_change(periods=lookback_days)
        
        # Absolute momentum check (is market above 0?)
        absolute_mom = returns > 0
        
        # Relative momentum rank
        ranks = returns.rank(ascending=False, pct=True)
        
        # Apply absolute momentum filter
        filtered_ranks = ranks.where(absolute_mom, 1.0)
        
        return filtered_ranks
    
    def compute_signals(self, market_data: pd.DataFrame) -> List[TradingSignal]:
        """Generate dual momentum signals with regime detection"""
        ranks = self.compute_ranks(market_data)
        
        # Determine market regime based on average momentum
        avg_return = market_data['close'].pct_change(periods=self.lookback_months * 21).mean()
        self.risk_on = avg_return > 0
        self.regime = "risk_on" if self.risk_on else "risk_off"
        
        signals = []
        symbols = market_data.get('symbol', market_data.index)
        
        for symbol, rank_pct in zip(symbols, ranks):
            if pd.isna(rank_pct):
                continue
            
            if self.risk_on and rank_pct <= 0.20:
                signals.append(TradingSignal(
                    symbol=str(symbol),
                    signal_type=SignalType.LONG,
                    weight=(1 - rank_pct) * self.config.max_position_pct,
                    rank=int((1 - rank_pct) * 100),
                    score=float(1 - rank_pct),
                    metadata={"regime": self.regime, "algo": "dual_momentum"}
                ))
            else:
                signals.append(TradingSignal(
                    symbol=str(symbol),
                    signal_type=SignalType.NEUTRAL,
                    weight=0.0,
                    rank=int((1 - rank_pct) * 100),
                    score=float(1 - rank_pct),
                    metadata={"regime": self.regime}
                ))
        
        return signals


class PercentileMomentum(BaseAlgo):
    """
    Tier 0 Algorithm #3: Percentile Momentum
    Long assets above 80th percentile
    """
    
    def __init__(self, config: AlgoConfig, threshold_percentile: float = 0.80):
        super().__init__(config)
        self.threshold_percentile = threshold_percentile
    
    def compute_ranks(self, market_data: pd.DataFrame) -> pd.Series:
        """Compute percentile-based momentum ranks"""
        lookback_days = 252  # 1 year
        
        returns = market_data['close'].pct_change(periods=lookback_days)
        ranks = returns.rank(ascending=False, pct=True)
        
        return ranks
    
    def compute_signals(self, market_data: pd.DataFrame) -> List[TradingSignal]:
        """Generate signals for assets above threshold percentile"""
        ranks = self.compute_ranks(market_data)
        
        signals = []
        symbols = market_data.get('symbol', market_data.index)
        
        for symbol, rank_pct in zip(symbols, ranks):
            if pd.isna(rank_pct):
                continue
            
            # 80th percentile means rank_pct <= 0.20
            if rank_pct <= (1 - self.threshold_percentile):
                signals.append(TradingSignal(
                    symbol=str(symbol),
                    signal_type=SignalType.LONG,
                    weight=(1 - rank_pct) * self.config.max_position_pct,
                    rank=int((1 - rank_pct) * 100),
                    score=float(1 - rank_pct),
                    metadata={"algo": "percentile_momentum"}
                ))
            else:
                signals.append(TradingSignal(
                    symbol=str(symbol),
                    signal_type=SignalType.NEUTRAL,
                    weight=0.0,
                    rank=int((1 - rank_pct) * 100),
                    score=float(1 - rank_pct)
                ))
        
        return signals


class VolAdjustedMomentum(BaseAlgo):
    """
    Tier 0 Algorithm #4: Volatility-Adjusted Momentum
    Rank by return/volatility (90-day std)
    """
    
    def __init__(self, config: AlgoConfig, vol_lookback_days: int = 90):
        super().__init__(config)
        self.vol_lookback_days = vol_lookback_days
    
    def compute_ranks(self, market_data: pd.DataFrame) -> pd.Series:
        """Compute volatility-adjusted momentum ranks"""
        lookback_days = 252
        
        returns = market_data['close'].pct_change(periods=lookback_days)
        volatility = market_data['close'].pct_change().rolling(window=self.vol_lookback_days).std()
        
        # Sharpe-like ratio
        vol_adjusted = returns / (volatility + 1e-8)
        
        ranks = vol_adjusted.rank(ascending=False, pct=True)
        
        return ranks
    
    def compute_signals(self, market_data: pd.DataFrame) -> List[TradingSignal]:
        """Generate volatility-adjusted signals"""
        ranks = self.compute_ranks(market_data)
        volatility = market_data['close'].pct_change().rolling(window=self.vol_lookback_days).std()
        
        signals = []
        symbols = market_data.get('symbol', market_data.index)
        
        for symbol, rank_pct, vol in zip(symbols, ranks, volatility):
            if pd.isna(rank_pct):
                continue
            
            # Inverse volatility sizing
            vol_weight = 1 / (vol + 1e-8) if not pd.isna(vol) else 1.0
            vol_weight = min(vol_weight, 2.0)  # Cap at 2x
            
            if rank_pct <= 0.20:
                base_weight = (1 - rank_pct) * self.config.max_position_pct
                adjusted_weight = base_weight * vol_weight / 2  # Normalize
                
                signals.append(TradingSignal(
                    symbol=str(symbol),
                    signal_type=SignalType.LONG,
                    weight=min(adjusted_weight, self.config.max_position_pct),
                    rank=int((1 - rank_pct) * 100),
                    score=float(1 - rank_pct),
                    metadata={"algo": "vol_adjusted", "volatility": float(vol) if not pd.isna(vol) else 0.0}
                ))
            else:
                signals.append(TradingSignal(
                    symbol=str(symbol),
                    signal_type=SignalType.NEUTRAL,
                    weight=0.0,
                    rank=int((1 - rank_pct) * 100),
                    score=float(1 - rank_pct)
                ))
        
        return signals


class CrossAssetRank(BaseAlgo):
    """
    Tier 0 Algorithm #5: Cross-Asset Rank
    Unified ranking across crypto and stocks with crypto cap
    """
    
    def __init__(self, config: AlgoConfig, crypto_cap: float = 0.30):
        super().__init__(config)
        self.crypto_cap = crypto_cap
    
    def compute_ranks(self, market_data: pd.DataFrame) -> pd.Series:
        """Compute cross-asset momentum ranks"""
        lookback_days = 252
        
        returns = market_data['close'].pct_change(periods=lookback_days)
        ranks = returns.rank(ascending=False, pct=True)
        
        return ranks
    
    def compute_signals(self, market_data: pd.DataFrame) -> List[TradingSignal]:
        """Generate unified cross-asset signals"""
        ranks = self.compute_ranks(market_data)
        
        signals = []
        symbols = market_data.get('symbol', market_data.index)
        asset_classes = market_data.get('asset_class', pd.Series(['equity'] * len(symbols), index=symbols))
        
        crypto_weight_total = 0.0
        
        for symbol, rank_pct, asset_class in zip(symbols, ranks, asset_classes):
            if pd.isna(rank_pct):
                continue
            
            is_crypto = asset_class == 'crypto' if isinstance(asset_class, str) else False
            
            if rank_pct <= 0.20:
                base_weight = (1 - rank_pct) * self.config.max_position_pct
                
                # Apply crypto cap
                if is_crypto:
                    remaining_crypto = max(0, self.crypto_cap - crypto_weight_total)
                    final_weight = min(base_weight, remaining_crypto)
                    crypto_weight_total += final_weight
                else:
                    final_weight = base_weight
                
                signals.append(TradingSignal(
                    symbol=str(symbol),
                    signal_type=SignalType.LONG if final_weight > 0 else SignalType.NEUTRAL,
                    weight=final_weight,
                    rank=int((1 - rank_pct) * 100),
                    score=float(1 - rank_pct),
                    metadata={"algo": "cross_asset", "asset_class": str(asset_class)}
                ))
            else:
                signals.append(TradingSignal(
                    symbol=str(symbol),
                    signal_type=SignalType.NEUTRAL,
                    weight=0.0,
                    rank=int((1 - rank_pct) * 100),
                    score=float(1 - rank_pct)
                ))
        
        return signals


# Factory function to create algorithms from config
def create_algo(algo_config: Dict[str, Any]) -> BaseAlgo:
    """Factory to create algorithm instances"""
    config = AlgoConfig.from_yaml(algo_config)
    algo_id = algo_config.get("id", 0)
    
    algo_map = {
        1: SimpleMomentumRank,
        2: DualMomentumRank,
        3: PercentileMomentum,
        4: VolAdjustedMomentum,
        5: CrossAssetRank,
    }
    
    algo_class = algo_map.get(algo_id)
    if algo_class is None:
        raise ValueError(f"Unknown algorithm ID: {algo_id}")
    
    return algo_class(config)

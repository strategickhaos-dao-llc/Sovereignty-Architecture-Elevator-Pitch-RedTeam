"""
Trading Arsenal - Signal Service
Generates trading signals using algorithm ensemble
"""

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from pathlib import Path
import json

import pandas as pd
import numpy as np
import redis.asyncio as redis
import yaml

from ..algos import (
    BaseAlgo,
    AlgoConfig,
    TradingSignal,
    SignalType,
    create_algo
)


logger = logging.getLogger(__name__)


@dataclass
class SignalServiceConfig:
    """Signal service configuration"""
    config_path: Path = field(default_factory=lambda: Path("trading/strategickhaos_trading_arsenal.yaml"))
    redis_url: str = "redis://localhost:6379/0"
    signal_channel: str = "trading:signals"
    min_readiness: float = 0.80
    ensemble_weights: Dict[int, float] = field(default_factory=dict)


@dataclass
class EnsembleSignal:
    """Aggregated signal from multiple algorithms"""
    symbol: str
    final_signal: SignalType
    final_weight: float
    consensus_score: float
    algo_signals: Dict[int, TradingSignal]
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "symbol": self.symbol,
            "final_signal": self.final_signal.value,
            "final_weight": self.final_weight,
            "consensus_score": self.consensus_score,
            "algo_signals": {k: v.to_dict() for k, v in self.algo_signals.items()},
            "timestamp": self.timestamp.isoformat()
        }


class SignalAggregator:
    """Aggregates signals from multiple algorithms"""
    
    def __init__(self, weights: Optional[Dict[int, float]] = None):
        # Default weights based on readiness
        self.weights = weights or {
            1: 0.25,  # Simple Momentum - highest readiness
            2: 0.22,  # Dual Momentum
            3: 0.20,  # Percentile Momentum
            4: 0.18,  # Vol-Adjusted
            5: 0.15   # Cross-Asset
        }
    
    def aggregate(self, signals_by_algo: Dict[int, List[TradingSignal]]) -> List[EnsembleSignal]:
        """Aggregate signals from all algorithms"""
        # Collect all symbols
        all_symbols = set()
        for signals in signals_by_algo.values():
            for signal in signals:
                all_symbols.add(signal.symbol)
        
        ensemble_signals = []
        
        for symbol in all_symbols:
            algo_signals: Dict[int, TradingSignal] = {}
            weighted_scores = []
            
            for algo_id, signals in signals_by_algo.items():
                symbol_signal = next((s for s in signals if s.symbol == symbol), None)
                if symbol_signal:
                    algo_signals[algo_id] = symbol_signal
                    weight = self.weights.get(algo_id, 1.0 / len(signals_by_algo))
                    
                    # Score: positive for long, negative for short, zero for neutral
                    if symbol_signal.signal_type == SignalType.LONG:
                        score = symbol_signal.score * weight
                    elif symbol_signal.signal_type == SignalType.SHORT:
                        score = -symbol_signal.score * weight
                    else:
                        score = 0
                    
                    weighted_scores.append(score)
            
            if not weighted_scores:
                continue
            
            # Calculate final consensus
            total_score = sum(weighted_scores)
            consensus = abs(total_score) / len(weighted_scores) if weighted_scores else 0
            
            # Determine final signal
            if total_score > 0.1:
                final_signal = SignalType.LONG
                final_weight = min(total_score, 0.05)  # Cap at 5%
            elif total_score < -0.1:
                final_signal = SignalType.SHORT
                final_weight = min(abs(total_score), 0.05)
            else:
                final_signal = SignalType.NEUTRAL
                final_weight = 0.0
            
            ensemble_signals.append(EnsembleSignal(
                symbol=symbol,
                final_signal=final_signal,
                final_weight=final_weight,
                consensus_score=consensus,
                algo_signals=algo_signals
            ))
        
        # Sort by consensus score (strongest signals first)
        ensemble_signals.sort(key=lambda x: x.consensus_score, reverse=True)
        
        return ensemble_signals


class SignalPublisher:
    """Publishes signals to Redis for consumption"""
    
    def __init__(self, redis_url: str, channel: str = "trading:signals"):
        self.redis_url = redis_url
        self.channel = channel
        self._redis: Optional[redis.Redis] = None
    
    async def connect(self) -> None:
        """Connect to Redis"""
        self._redis = redis.from_url(self.redis_url)
        await self._redis.ping()
        logger.info("Connected to Redis for signal publishing")
    
    async def disconnect(self) -> None:
        """Disconnect from Redis"""
        if self._redis:
            await self._redis.close()
    
    async def publish_signal(self, signal: EnsembleSignal) -> None:
        """Publish a single signal"""
        if not self._redis:
            await self.connect()
        
        message = json.dumps(signal.to_dict())
        await self._redis.publish(self.channel, message)
        
        # Also store in sorted set for retrieval
        key = f"signals:{signal.symbol}"
        await self._redis.zadd(key, {message: signal.timestamp.timestamp()})
        
        # Trim old signals (keep last 1000)
        await self._redis.zremrangebyrank(key, 0, -1001)
    
    async def publish_batch(self, signals: List[EnsembleSignal]) -> None:
        """Publish multiple signals"""
        for signal in signals:
            await self.publish_signal(signal)
        
        # Publish summary
        summary = {
            "type": "signal_batch",
            "count": len(signals),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "symbols": [s.symbol for s in signals if s.final_signal != SignalType.NEUTRAL]
        }
        await self._redis.publish(f"{self.channel}:summary", json.dumps(summary))
    
    async def get_latest_signals(self, symbol: str, count: int = 10) -> List[Dict[str, Any]]:
        """Get latest signals for a symbol"""
        if not self._redis:
            await self.connect()
        
        key = f"signals:{symbol}"
        raw_signals = await self._redis.zrevrange(key, 0, count - 1)
        
        return [json.loads(s) for s in raw_signals]


class SignalService:
    """Main signal generation service"""
    
    def __init__(self, config: SignalServiceConfig):
        self.config = config
        self.algos: Dict[int, BaseAlgo] = {}
        self.aggregator = SignalAggregator(config.ensemble_weights)
        self.publisher = SignalPublisher(config.redis_url, config.signal_channel)
        self._loaded = False
    
    def load_algorithms(self) -> None:
        """Load algorithms from configuration"""
        if not self.config.config_path.exists():
            logger.warning(f"Config not found: {self.config.config_path}")
            return
        
        with open(self.config.config_path) as f:
            arsenal_config = yaml.safe_load(f)
        
        # Load Tier 0 algorithms (ready for production)
        tier_0 = arsenal_config.get("tier_0_immediate_core", {})
        for algo_config in tier_0.get("algos", []):
            if algo_config.get("readiness", 0) >= self.config.min_readiness:
                try:
                    algo = create_algo(algo_config)
                    self.algos[algo.algo_id] = algo
                    logger.info(f"Loaded algorithm: {algo.name} (readiness={algo.config.readiness})")
                except Exception as e:
                    logger.error(f"Failed to load algorithm {algo_config.get('name')}: {e}")
        
        self._loaded = True
        logger.info(f"Loaded {len(self.algos)} algorithms for production")
    
    async def generate_signals(self, market_data: pd.DataFrame) -> List[EnsembleSignal]:
        """Generate signals from all loaded algorithms"""
        if not self._loaded:
            self.load_algorithms()
        
        if not self.algos:
            logger.warning("No algorithms loaded")
            return []
        
        # Run each algorithm
        signals_by_algo: Dict[int, List[TradingSignal]] = {}
        
        for algo_id, algo in self.algos.items():
            try:
                signals = algo.run(market_data)
                signals_by_algo[algo_id] = signals
                logger.info(f"Algorithm {algo.name} generated {len(signals)} signals")
            except Exception as e:
                logger.error(f"Error running algorithm {algo.name}: {e}")
        
        # Aggregate signals
        ensemble_signals = self.aggregator.aggregate(signals_by_algo)
        
        return ensemble_signals
    
    async def publish_signals(self, signals: List[EnsembleSignal]) -> None:
        """Publish generated signals to Redis"""
        await self.publisher.publish_batch(signals)
        logger.info(f"Published {len(signals)} ensemble signals")
    
    async def run_signal_cycle(self, market_data: pd.DataFrame) -> List[EnsembleSignal]:
        """Complete signal generation cycle: generate + publish"""
        signals = await self.generate_signals(market_data)
        
        if signals:
            await self.publish_signals(signals)
        
        return signals
    
    def get_algo_status(self) -> Dict[str, Any]:
        """Get status of all algorithms"""
        return {
            "algorithms": {
                algo_id: algo.get_status()
                for algo_id, algo in self.algos.items()
            },
            "loaded": self._loaded,
            "total_algos": len(self.algos),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    
    async def health_check(self) -> Dict[str, Any]:
        """Check service health"""
        redis_healthy = False
        try:
            await self.publisher.connect()
            redis_healthy = True
        except Exception as e:
            logger.error(f"Redis health check failed: {e}")
        
        return {
            "loaded": self._loaded,
            "algo_count": len(self.algos),
            "redis_connected": redis_healthy,
            "config_exists": self.config.config_path.exists(),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

"""
Trading Arsenal - Unit Tests
"""

import asyncio
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch

import pandas as pd
import numpy as np
import pytest

from trading.algos import (
    SimpleMomentumRank,
    DualMomentumRank,
    PercentileMomentum,
    VolAdjustedMomentum,
    CrossAssetRank,
    AlgoConfig,
    SignalType,
    create_algo
)


@pytest.fixture
def sample_config():
    return AlgoConfig(
        algo_id=1,
        name="Test Algo",
        readiness=0.95,
        yield_target=0.08,
        max_position_pct=0.05,
        max_drawdown=0.20,
        enabled=True
    )


@pytest.fixture
def sample_market_data():
    """Create sample market data for testing"""
    np.random.seed(42)
    dates = pd.date_range(start='2023-01-01', periods=365, freq='D')
    
    # Create price data with upward trend
    base_prices = 100 * (1 + np.cumsum(np.random.randn(365) * 0.02))
    
    data = pd.DataFrame({
        'close': base_prices,
        'open': base_prices * 0.99,
        'high': base_prices * 1.01,
        'low': base_prices * 0.98,
        'volume': np.random.randint(1000000, 10000000, 365),
        'symbol': 'SPY'
    }, index=dates)
    
    return data


class TestSimpleMomentumRank:
    """Tests for Simple Momentum Rank algorithm"""
    
    def test_initialization(self, sample_config):
        algo = SimpleMomentumRank(sample_config)
        assert algo.name == "Test Algo"
        assert algo.is_ready
        assert algo.config.readiness == 0.95
    
    def test_compute_ranks(self, sample_config, sample_market_data):
        algo = SimpleMomentumRank(sample_config)
        ranks = algo.compute_ranks(sample_market_data)
        
        assert not ranks.empty
        assert ranks.dtype == float
    
    def test_compute_signals(self, sample_config, sample_market_data):
        algo = SimpleMomentumRank(sample_config)
        signals = algo.compute_signals(sample_market_data)
        
        assert len(signals) > 0
        for signal in signals:
            assert signal.symbol == 'SPY'
            assert signal.signal_type in [SignalType.LONG, SignalType.NEUTRAL]
            assert 0 <= signal.weight <= sample_config.max_position_pct
    
    def test_disabled_algo_returns_empty(self, sample_config, sample_market_data):
        sample_config.enabled = False
        algo = SimpleMomentumRank(sample_config)
        signals = algo.run(sample_market_data)
        
        assert signals == []
    
    def test_low_readiness_returns_empty(self, sample_config, sample_market_data):
        sample_config.readiness = 0.50
        algo = SimpleMomentumRank(sample_config)
        signals = algo.run(sample_market_data)
        
        assert signals == []


class TestDualMomentumRank:
    """Tests for Dual Momentum Rank algorithm"""
    
    def test_regime_detection(self, sample_config, sample_market_data):
        algo = DualMomentumRank(sample_config)
        signals = algo.compute_signals(sample_market_data)
        
        # Check that regime is set
        assert algo.regime in ["risk_on", "risk_off"]
        
        # Check metadata contains regime
        for signal in signals:
            if signal.metadata:
                assert "regime" in signal.metadata


class TestVolAdjustedMomentum:
    """Tests for Volatility-Adjusted Momentum algorithm"""
    
    def test_vol_adjustment(self, sample_config, sample_market_data):
        algo = VolAdjustedMomentum(sample_config)
        signals = algo.compute_signals(sample_market_data)
        
        # Check volatility in metadata
        for signal in signals:
            if signal.signal_type == SignalType.LONG:
                assert "volatility" in signal.metadata


class TestCrossAssetRank:
    """Tests for Cross-Asset Rank algorithm"""
    
    def test_crypto_cap(self, sample_config, sample_market_data):
        # Add asset class column
        sample_market_data['asset_class'] = 'equity'
        
        algo = CrossAssetRank(sample_config, crypto_cap=0.30)
        signals = algo.compute_signals(sample_market_data)
        
        assert len(signals) > 0


class TestAlgoFactory:
    """Tests for algorithm factory"""
    
    def test_create_simple_momentum(self):
        config = {"id": 1, "name": "Simple Momentum", "readiness": 0.95, "yield_annualized": 0.08}
        algo = create_algo(config)
        
        assert isinstance(algo, SimpleMomentumRank)
        assert algo.name == "Simple Momentum"
    
    def test_create_dual_momentum(self):
        config = {"id": 2, "name": "Dual Momentum", "readiness": 0.90, "yield_annualized": 0.075}
        algo = create_algo(config)
        
        assert isinstance(algo, DualMomentumRank)
    
    def test_invalid_algo_id(self):
        config = {"id": 999, "name": "Unknown", "readiness": 0.95}
        
        with pytest.raises(ValueError):
            create_algo(config)


class TestRiskControls:
    """Tests for risk control functionality"""
    
    def test_drawdown_triggers_reduce(self, sample_config, sample_market_data):
        algo = SimpleMomentumRank(sample_config)
        algo.risk_metrics.current_drawdown = 0.25  # Above 20% limit
        
        signals = algo.run(sample_market_data)
        
        # All signals should be REDUCE type
        for signal in signals:
            if signal.signal_type != SignalType.NEUTRAL:
                assert signal.signal_type == SignalType.REDUCE
                assert signal.metadata.get("risk_adjusted")
    
    def test_position_cap_applied(self, sample_config, sample_market_data):
        algo = SimpleMomentumRank(sample_config)
        signals = algo.run(sample_market_data)
        
        for signal in signals:
            assert signal.weight <= sample_config.max_position_pct


class TestSignalAggregation:
    """Tests for signal aggregation"""
    
    @pytest.mark.asyncio
    async def test_ensemble_consensus(self):
        from trading.services.signal_service import SignalAggregator, EnsembleSignal
        from trading.algos import TradingSignal, SignalType
        
        aggregator = SignalAggregator()
        
        # Create sample signals from multiple algos
        signals_by_algo = {
            1: [TradingSignal("SPY", SignalType.LONG, 0.05, 1, 0.9)],
            2: [TradingSignal("SPY", SignalType.LONG, 0.04, 2, 0.8)],
            3: [TradingSignal("SPY", SignalType.NEUTRAL, 0.0, 3, 0.5)],
        }
        
        ensemble = aggregator.aggregate(signals_by_algo)
        
        assert len(ensemble) == 1
        assert ensemble[0].symbol == "SPY"
        # Should be LONG due to consensus
        assert ensemble[0].final_signal == SignalType.LONG


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

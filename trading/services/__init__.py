"""
Trading Arsenal - Services Package
"""

from .data_service import DataService, DataConfig, OHLCVBar, PolygonDataProvider, CoingeckoDataProvider
from .signal_service import SignalService, SignalServiceConfig, EnsembleSignal, SignalAggregator
from .execution_service import ExecutionService, ExecutionConfig, Order, Position, OrderStatus, RiskGuard
from .monitoring_service import MonitoringService, MonitoringConfig, Alert, AlertType, AlertSeverity, PerformanceMetrics

__all__ = [
    # Data Service
    "DataService",
    "DataConfig",
    "OHLCVBar",
    "PolygonDataProvider",
    "CoingeckoDataProvider",
    
    # Signal Service
    "SignalService",
    "SignalServiceConfig",
    "EnsembleSignal",
    "SignalAggregator",
    
    # Execution Service
    "ExecutionService",
    "ExecutionConfig",
    "Order",
    "Position",
    "OrderStatus",
    "RiskGuard",
    
    # Monitoring Service
    "MonitoringService",
    "MonitoringConfig",
    "Alert",
    "AlertType",
    "AlertSeverity",
    "PerformanceMetrics"
]

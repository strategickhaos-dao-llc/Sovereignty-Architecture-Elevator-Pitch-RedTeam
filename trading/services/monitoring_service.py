"""
Trading Arsenal - Monitoring Service
P&L tracking, drawdown alerts, and performance metrics
"""

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from enum import Enum
from typing import Dict, List, Optional, Any
import json

import redis.asyncio as redis
from prometheus_client import Counter, Gauge, Histogram, generate_latest


logger = logging.getLogger(__name__)


class AlertSeverity(Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class AlertType(Enum):
    DRAWDOWN = "drawdown"
    PNL = "pnl"
    TRADE_LIMIT = "trade_limit"
    POSITION_LIMIT = "position_limit"
    SYSTEM = "system"
    ALGORITHM = "algorithm"


@dataclass
class Alert:
    """Monitoring alert"""
    alert_id: str
    alert_type: AlertType
    severity: AlertSeverity
    message: str
    value: float
    threshold: float
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    resolved: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "alert_id": self.alert_id,
            "alert_type": self.alert_type.value,
            "severity": self.severity.value,
            "message": self.message,
            "value": self.value,
            "threshold": self.threshold,
            "timestamp": self.timestamp.isoformat(),
            "resolved": self.resolved,
            "metadata": self.metadata
        }


@dataclass
class PerformanceMetrics:
    """Portfolio performance metrics"""
    timestamp: datetime
    portfolio_value: float
    daily_pnl: float
    total_pnl: float
    daily_return_pct: float
    total_return_pct: float
    current_drawdown: float
    max_drawdown: float
    sharpe_ratio: float
    win_rate: float
    trade_count: int
    position_count: int
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp.isoformat(),
            "portfolio_value": self.portfolio_value,
            "daily_pnl": self.daily_pnl,
            "total_pnl": self.total_pnl,
            "daily_return_pct": self.daily_return_pct,
            "total_return_pct": self.total_return_pct,
            "current_drawdown": self.current_drawdown,
            "max_drawdown": self.max_drawdown,
            "sharpe_ratio": self.sharpe_ratio,
            "win_rate": self.win_rate,
            "trade_count": self.trade_count,
            "position_count": self.position_count
        }


@dataclass
class MonitoringConfig:
    """Monitoring service configuration"""
    redis_url: str = "redis://localhost:6379/0"
    alert_channel: str = "trading:alerts"
    metrics_channel: str = "trading:metrics"
    drawdown_warning: float = 0.10  # 10%
    drawdown_critical: float = 0.15  # 15%
    drawdown_halt: float = 0.20  # 20%
    daily_loss_warning: float = 0.02  # 2%
    daily_loss_critical: float = 0.03  # 3%
    metrics_interval_seconds: int = 60
    discord_webhook_url: str = ""


# Prometheus metrics
PORTFOLIO_VALUE = Gauge('trading_portfolio_value', 'Current portfolio value')
DAILY_PNL = Gauge('trading_daily_pnl', 'Daily P&L')
TOTAL_PNL = Gauge('trading_total_pnl', 'Total P&L')
CURRENT_DRAWDOWN = Gauge('trading_current_drawdown', 'Current drawdown')
MAX_DRAWDOWN = Gauge('trading_max_drawdown', 'Maximum drawdown')
TRADE_COUNT = Counter('trading_trades_total', 'Total trades executed', ['side', 'status'])
SIGNAL_COUNT = Counter('trading_signals_total', 'Total signals generated', ['algo', 'type'])
ALGO_STATUS = Gauge('trading_algo_status', 'Algorithm status', ['algo_id', 'name'])
ALERT_COUNT = Counter('trading_alerts_total', 'Total alerts generated', ['type', 'severity'])


class PerformanceTracker:
    """Tracks portfolio performance metrics"""
    
    def __init__(self, initial_capital: float = 100000.0):
        self.initial_capital = initial_capital
        self.starting_value = initial_capital
        self.current_value = initial_capital
        self.peak_value = initial_capital
        self.daily_starting_value = initial_capital
        
        self.trades: List[Dict[str, Any]] = []
        self.daily_returns: List[float] = []
        
    def update(self, current_value: float, trade: Optional[Dict[str, Any]] = None) -> None:
        """Update with current portfolio value"""
        self.current_value = current_value
        self.peak_value = max(self.peak_value, current_value)
        
        if trade:
            self.trades.append(trade)
        
        # Update Prometheus metrics
        PORTFOLIO_VALUE.set(current_value)
        TOTAL_PNL.set(current_value - self.initial_capital)
        DAILY_PNL.set(current_value - self.daily_starting_value)
        CURRENT_DRAWDOWN.set(self.current_drawdown)
        MAX_DRAWDOWN.set(self.max_drawdown)
    
    def reset_daily(self) -> None:
        """Reset daily metrics"""
        if self.current_value != self.daily_starting_value:
            daily_return = (self.current_value - self.daily_starting_value) / self.daily_starting_value
            self.daily_returns.append(daily_return)
        
        self.daily_starting_value = self.current_value
    
    @property
    def current_drawdown(self) -> float:
        """Calculate current drawdown from peak"""
        if self.peak_value == 0:
            return 0.0
        return (self.peak_value - self.current_value) / self.peak_value
    
    @property
    def max_drawdown(self) -> float:
        """Calculate maximum drawdown"""
        if not self.daily_returns:
            return self.current_drawdown
        
        max_dd = 0.0
        peak = 1.0
        
        cumulative = 1.0
        for ret in self.daily_returns:
            cumulative *= (1 + ret)
            peak = max(peak, cumulative)
            dd = (peak - cumulative) / peak
            max_dd = max(max_dd, dd)
        
        return max(max_dd, self.current_drawdown)
    
    @property
    def sharpe_ratio(self) -> float:
        """Calculate Sharpe ratio (annualized)"""
        if len(self.daily_returns) < 2:
            return 0.0
        
        import numpy as np
        returns = np.array(self.daily_returns)
        
        mean_return = np.mean(returns)
        std_return = np.std(returns)
        
        if std_return == 0:
            return 0.0
        
        # Annualize (252 trading days)
        return (mean_return * 252) / (std_return * np.sqrt(252))
    
    @property
    def win_rate(self) -> float:
        """Calculate win rate from trades"""
        if not self.trades:
            return 0.0
        
        wins = sum(1 for t in self.trades if t.get("pnl", 0) > 0)
        return wins / len(self.trades)
    
    @property
    def total_return_pct(self) -> float:
        """Calculate total return percentage"""
        if self.initial_capital == 0:
            return 0.0
        return (self.current_value - self.initial_capital) / self.initial_capital
    
    @property
    def daily_return_pct(self) -> float:
        """Calculate daily return percentage"""
        if self.daily_starting_value == 0:
            return 0.0
        return (self.current_value - self.daily_starting_value) / self.daily_starting_value
    
    def get_metrics(self) -> PerformanceMetrics:
        """Get current performance metrics"""
        return PerformanceMetrics(
            timestamp=datetime.now(timezone.utc),
            portfolio_value=self.current_value,
            daily_pnl=self.current_value - self.daily_starting_value,
            total_pnl=self.current_value - self.initial_capital,
            daily_return_pct=self.daily_return_pct,
            total_return_pct=self.total_return_pct,
            current_drawdown=self.current_drawdown,
            max_drawdown=self.max_drawdown,
            sharpe_ratio=self.sharpe_ratio,
            win_rate=self.win_rate,
            trade_count=len(self.trades),
            position_count=0  # Updated by position tracking
        )


class AlertManager:
    """Manages and publishes alerts"""
    
    def __init__(self, config: MonitoringConfig):
        self.config = config
        self._redis: Optional[redis.Redis] = None
        self._alert_counter = 0
        self.active_alerts: Dict[str, Alert] = {}
    
    async def connect(self) -> None:
        """Connect to Redis"""
        self._redis = redis.from_url(self.config.redis_url)
        await self._redis.ping()
    
    async def disconnect(self) -> None:
        """Disconnect from Redis"""
        if self._redis:
            await self._redis.close()
    
    def _generate_alert_id(self) -> str:
        """Generate unique alert ID"""
        self._alert_counter += 1
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
        return f"ALERT-{timestamp}-{self._alert_counter:04d}"
    
    async def create_alert(
        self,
        alert_type: AlertType,
        severity: AlertSeverity,
        message: str,
        value: float,
        threshold: float,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Alert:
        """Create and publish new alert"""
        alert = Alert(
            alert_id=self._generate_alert_id(),
            alert_type=alert_type,
            severity=severity,
            message=message,
            value=value,
            threshold=threshold,
            metadata=metadata or {}
        )
        
        self.active_alerts[alert.alert_id] = alert
        
        # Update Prometheus
        ALERT_COUNT.labels(type=alert_type.value, severity=severity.value).inc()
        
        # Publish to Redis
        if self._redis:
            await self._redis.publish(
                self.config.alert_channel,
                json.dumps(alert.to_dict())
            )
            
            # Store in sorted set
            await self._redis.zadd(
                "trading:alerts:history",
                {json.dumps(alert.to_dict()): alert.timestamp.timestamp()}
            )
        
        logger.warning(f"Alert created: [{severity.value}] {message}")
        
        # Send to Discord if configured
        if self.config.discord_webhook_url and severity in (AlertSeverity.WARNING, AlertSeverity.CRITICAL):
            await self._send_discord_alert(alert)
        
        return alert
    
    async def _send_discord_alert(self, alert: Alert) -> None:
        """Send alert to Discord webhook"""
        import aiohttp
        
        color = 0xFF0000 if alert.severity == AlertSeverity.CRITICAL else 0xFFA500
        
        embed = {
            "title": f"🚨 Trading Alert: {alert.alert_type.value.upper()}",
            "description": alert.message,
            "color": color,
            "fields": [
                {"name": "Value", "value": f"{alert.value:.4f}", "inline": True},
                {"name": "Threshold", "value": f"{alert.threshold:.4f}", "inline": True},
                {"name": "Severity", "value": alert.severity.value.upper(), "inline": True}
            ],
            "timestamp": alert.timestamp.isoformat()
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                await session.post(
                    self.config.discord_webhook_url,
                    json={"embeds": [embed]}
                )
        except Exception as e:
            logger.error(f"Failed to send Discord alert: {e}")
    
    async def resolve_alert(self, alert_id: str) -> None:
        """Resolve an active alert"""
        if alert_id in self.active_alerts:
            self.active_alerts[alert_id].resolved = True
            del self.active_alerts[alert_id]
    
    def get_active_alerts(self) -> List[Alert]:
        """Get all active alerts"""
        return list(self.active_alerts.values())


class MonitoringService:
    """Main monitoring service"""
    
    def __init__(self, config: MonitoringConfig):
        self.config = config
        self.tracker = PerformanceTracker()
        self.alert_manager = AlertManager(config)
        self._redis: Optional[redis.Redis] = None
        self._running = False
    
    async def connect(self) -> None:
        """Connect to Redis"""
        self._redis = redis.from_url(self.config.redis_url)
        await self._redis.ping()
        await self.alert_manager.connect()
        logger.info("Monitoring service connected")
    
    async def disconnect(self) -> None:
        """Disconnect from Redis"""
        self._running = False
        if self._redis:
            await self._redis.close()
        await self.alert_manager.disconnect()
    
    async def update_metrics(self, portfolio_value: float, positions: List[Dict[str, Any]] = None) -> None:
        """Update monitoring metrics"""
        previous_value = self.tracker.current_value
        self.tracker.update(portfolio_value)
        
        # Check for alerts
        await self._check_drawdown_alerts()
        await self._check_pnl_alerts()
        
        # Publish metrics
        metrics = self.tracker.get_metrics()
        if positions:
            metrics.position_count = len(positions)
        
        if self._redis:
            await self._redis.publish(
                self.config.metrics_channel,
                json.dumps(metrics.to_dict())
            )
            
            # Store latest metrics
            await self._redis.set(
                "trading:metrics:latest",
                json.dumps(metrics.to_dict())
            )
    
    async def _check_drawdown_alerts(self) -> None:
        """Check and create drawdown alerts"""
        dd = self.tracker.current_drawdown
        
        if dd >= self.config.drawdown_halt:
            await self.alert_manager.create_alert(
                AlertType.DRAWDOWN,
                AlertSeverity.CRITICAL,
                f"TRADING HALT: Drawdown {dd*100:.1f}% exceeds halt threshold",
                dd,
                self.config.drawdown_halt
            )
        elif dd >= self.config.drawdown_critical:
            await self.alert_manager.create_alert(
                AlertType.DRAWDOWN,
                AlertSeverity.CRITICAL,
                f"Critical drawdown: {dd*100:.1f}%",
                dd,
                self.config.drawdown_critical
            )
        elif dd >= self.config.drawdown_warning:
            await self.alert_manager.create_alert(
                AlertType.DRAWDOWN,
                AlertSeverity.WARNING,
                f"Drawdown warning: {dd*100:.1f}%",
                dd,
                self.config.drawdown_warning
            )
    
    async def _check_pnl_alerts(self) -> None:
        """Check and create P&L alerts"""
        daily_return = self.tracker.daily_return_pct
        
        if daily_return <= -self.config.daily_loss_critical:
            await self.alert_manager.create_alert(
                AlertType.PNL,
                AlertSeverity.CRITICAL,
                f"Critical daily loss: {daily_return*100:.2f}%",
                abs(daily_return),
                self.config.daily_loss_critical
            )
        elif daily_return <= -self.config.daily_loss_warning:
            await self.alert_manager.create_alert(
                AlertType.PNL,
                AlertSeverity.WARNING,
                f"Daily loss warning: {daily_return*100:.2f}%",
                abs(daily_return),
                self.config.daily_loss_warning
            )
    
    async def record_trade(self, trade: Dict[str, Any]) -> None:
        """Record a completed trade"""
        self.tracker.trades.append(trade)
        
        # Update Prometheus
        TRADE_COUNT.labels(
            side=trade.get("side", "unknown"),
            status=trade.get("status", "unknown")
        ).inc()
        
        # Store in Redis
        if self._redis:
            await self._redis.rpush(
                "trading:trades:history",
                json.dumps(trade)
            )
    
    async def record_signal(self, algo_id: int, signal_type: str) -> None:
        """Record a generated signal"""
        SIGNAL_COUNT.labels(algo=str(algo_id), type=signal_type).inc()
    
    async def update_algo_status(self, algo_id: int, name: str, status: float) -> None:
        """Update algorithm status metric"""
        ALGO_STATUS.labels(algo_id=str(algo_id), name=name).set(status)
    
    async def start_metrics_loop(self) -> None:
        """Start continuous metrics collection loop"""
        self._running = True
        
        while self._running:
            try:
                # Get latest portfolio value from execution service
                if self._redis:
                    latest = await self._redis.get("trading:portfolio:value")
                    if latest:
                        value = float(latest)
                        await self.update_metrics(value)
                
                await asyncio.sleep(self.config.metrics_interval_seconds)
                
            except Exception as e:
                logger.error(f"Metrics loop error: {e}")
                await asyncio.sleep(10)
    
    def get_metrics_snapshot(self) -> Dict[str, Any]:
        """Get current metrics snapshot"""
        metrics = self.tracker.get_metrics()
        return {
            "metrics": metrics.to_dict(),
            "active_alerts": [a.to_dict() for a in self.alert_manager.get_active_alerts()],
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    
    def get_prometheus_metrics(self) -> bytes:
        """Get Prometheus metrics"""
        return generate_latest()
    
    async def health_check(self) -> Dict[str, Any]:
        """Check service health"""
        redis_connected = False
        try:
            if self._redis:
                await self._redis.ping()
                redis_connected = True
        except Exception:
            pass
        
        return {
            "redis_connected": redis_connected,
            "active_alerts": len(self.alert_manager.active_alerts),
            "tracked_trades": len(self.tracker.trades),
            "current_drawdown": self.tracker.current_drawdown,
            "portfolio_value": self.tracker.current_value,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

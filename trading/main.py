"""
Trading Arsenal - Main Orchestrator
Autonomous execution controller for all trading departments
"""

import asyncio
import logging
import os
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, Optional
import signal as signal_module

import pandas as pd
import structlog
import yaml
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel, Field

from .services import (
    DataService, DataConfig,
    SignalService, SignalServiceConfig,
    ExecutionService, ExecutionConfig,
    MonitoringService, MonitoringConfig,
    EnsembleSignal
)


# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger(__name__)


class TradingConfig:
    """Central configuration for trading system"""
    
    def __init__(self):
        # Data service
        self.data = DataConfig(
            polygon_api_key=os.getenv("POLYGON_API_KEY", ""),
            coingecko_api_key=os.getenv("COINGECKO_API_KEY", ""),
            data_dir=Path(os.getenv("TRADING_DATA_DIR", "/var/trading/data"))
        )
        
        # Signal service
        self.signal = SignalServiceConfig(
            config_path=Path(os.getenv("TRADING_CONFIG_PATH", "trading/strategickhaos_trading_arsenal.yaml")),
            redis_url=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
            signal_channel="trading:signals",
            min_readiness=0.80
        )
        
        # Execution service
        self.execution = ExecutionConfig(
            broker_api_key=os.getenv("BROKER_API_KEY", ""),
            broker_api_secret=os.getenv("BROKER_API_SECRET", ""),
            broker_base_url=os.getenv("BROKER_BASE_URL", "https://paper-api.alpaca.markets"),
            redis_url=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
            max_position_pct=float(os.getenv("MAX_POSITION_PCT", "0.05")),
            max_drawdown=float(os.getenv("MAX_DRAWDOWN", "0.20")),
            max_daily_trades=int(os.getenv("MAX_DAILY_TRADES", "50")),
            enabled=os.getenv("EXECUTION_ENABLED", "true").lower() == "true",
            paper_trading=os.getenv("PAPER_TRADING", "true").lower() == "true"
        )
        
        # Monitoring service
        self.monitoring = MonitoringConfig(
            redis_url=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
            alert_channel="trading:alerts",
            metrics_channel="trading:metrics",
            drawdown_warning=0.10,
            drawdown_critical=0.15,
            drawdown_halt=0.20,
            discord_webhook_url=os.getenv("DISCORD_ALERTS_WEBHOOK", "")
        )
        
        # General settings
        self.env = os.getenv("TRADING_ENV", "development")
        self.api_port = int(os.getenv("TRADING_API_PORT", "8086"))
        self.rebalance_schedule = os.getenv("REBALANCE_SCHEDULE", "0 9 * * MON")


class TradingOrchestrator:
    """Main orchestrator coordinating all trading services"""
    
    def __init__(self, config: TradingConfig):
        self.config = config
        self.data_service = DataService(config.data)
        self.signal_service = SignalService(config.signal)
        self.execution_service = ExecutionService(config.execution)
        self.monitoring_service = MonitoringService(config.monitoring)
        
        self._running = False
        self._autonomous_task: Optional[asyncio.Task] = None
        self._last_run: Optional[datetime] = None
    
    async def initialize(self) -> None:
        """Initialize all services"""
        logger.info("Initializing Trading Orchestrator")
        
        # Load algorithms
        self.signal_service.load_algorithms()
        
        # Connect services
        await self.execution_service.connect()
        await self.monitoring_service.connect()
        
        logger.info("Trading Orchestrator initialized")
    
    async def shutdown(self) -> None:
        """Shutdown all services"""
        logger.info("Shutting down Trading Orchestrator")
        
        self._running = False
        if self._autonomous_task:
            self._autonomous_task.cancel()
        
        await self.execution_service.disconnect()
        await self.monitoring_service.disconnect()
    
    async def run_signal_cycle(self, tier: str = "tier_0") -> Dict[str, Any]:
        """Execute a complete signal generation and execution cycle"""
        start_time = datetime.now(timezone.utc)
        
        try:
            # 1. Fetch market data
            logger.info("Fetching market data")
            universe = self.data_service.get_universe(tier)
            
            # Fetch equity data
            equity_data = await self.data_service.get_market_data(
                universe.get("equity", []),
                asset_class="equity",
                lookback_days=365
            )
            
            # Fetch crypto data
            crypto_data = await self.data_service.get_market_data(
                universe.get("crypto", []),
                asset_class="crypto",
                lookback_days=365
            )
            
            # Combine data
            if not equity_data.empty and not crypto_data.empty:
                market_data = pd.concat([equity_data, crypto_data])
            elif not equity_data.empty:
                market_data = equity_data
            elif not crypto_data.empty:
                market_data = crypto_data
            else:
                logger.warning("No market data available")
                return {"status": "error", "message": "No market data"}
            
            # 2. Generate signals
            logger.info("Generating trading signals")
            signals = await self.signal_service.run_signal_cycle(market_data)
            
            # Record signals in monitoring
            for signal in signals:
                for algo_id in signal.algo_signals.keys():
                    await self.monitoring_service.record_signal(algo_id, signal.final_signal.value)
            
            # 3. Execute signals (if enabled)
            executed_orders = []
            if self.config.execution.enabled:
                logger.info("Executing trading signals")
                executed_orders = await self.execution_service.execute_signals(signals)
                
                # Record trades
                for order in executed_orders:
                    await self.monitoring_service.record_trade(order.to_dict())
            
            # 4. Update monitoring
            health = await self.execution_service.health_check()
            await self.monitoring_service.update_metrics(
                health.get("portfolio_value", 100000.0)
            )
            
            self._last_run = datetime.now(timezone.utc)
            duration = (self._last_run - start_time).total_seconds()
            
            result = {
                "status": "success",
                "tier": tier,
                "signals_generated": len(signals),
                "orders_executed": len(executed_orders),
                "execution_enabled": self.config.execution.enabled,
                "paper_trading": self.config.execution.paper_trading,
                "duration_seconds": duration,
                "timestamp": self._last_run.isoformat()
            }
            
            logger.info(f"Signal cycle completed: {len(signals)} signals, {len(executed_orders)} orders")
            
            return result
            
        except Exception as e:
            logger.error(f"Signal cycle error: {e}")
            return {
                "status": "error",
                "message": str(e),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
    
    async def start_autonomous_mode(self, interval_minutes: int = 60) -> None:
        """Start autonomous trading mode"""
        self._running = True
        logger.info(f"Starting autonomous mode with {interval_minutes} minute intervals")
        
        async def autonomous_loop():
            while self._running:
                try:
                    await self.run_signal_cycle()
                    await asyncio.sleep(interval_minutes * 60)
                except asyncio.CancelledError:
                    break
                except Exception as e:
                    logger.error(f"Autonomous loop error: {e}")
                    await asyncio.sleep(60)  # Wait before retry
        
        self._autonomous_task = asyncio.create_task(autonomous_loop())
    
    async def stop_autonomous_mode(self) -> None:
        """Stop autonomous trading mode"""
        self._running = False
        if self._autonomous_task:
            self._autonomous_task.cancel()
            try:
                await self._autonomous_task
            except asyncio.CancelledError:
                pass
        logger.info("Autonomous mode stopped")
    
    def get_status(self) -> Dict[str, Any]:
        """Get orchestrator status"""
        return {
            "running": self._running,
            "last_run": self._last_run.isoformat() if self._last_run else None,
            "env": self.config.env,
            "execution_enabled": self.config.execution.enabled,
            "paper_trading": self.config.execution.paper_trading,
            "algorithms_loaded": len(self.signal_service.algos),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


# Pydantic models for API
class SignalCycleRequest(BaseModel):
    tier: str = Field(default="tier_0", description="Algorithm tier to use")


class AutonomousModeRequest(BaseModel):
    interval_minutes: int = Field(default=60, ge=5, le=1440, description="Interval between cycles")


class HealthResponse(BaseModel):
    status: str
    services: Dict[str, Any]
    timestamp: str


# FastAPI application
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    config = TradingConfig()
    orchestrator = TradingOrchestrator(config)
    
    await orchestrator.initialize()
    app.state.orchestrator = orchestrator
    app.state.config = config
    
    # Start autonomous mode if configured
    if os.getenv("AUTO_START_AUTONOMOUS", "false").lower() == "true":
        await orchestrator.start_autonomous_mode()
    
    yield
    
    await orchestrator.shutdown()


app = FastAPI(
    title="StrategicKhaos Trading Arsenal",
    description="Autonomous trading system with rank-based algorithms",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    orchestrator: TradingOrchestrator = app.state.orchestrator
    
    data_health = await orchestrator.data_service.health_check()
    signal_health = await orchestrator.signal_service.health_check()
    execution_health = await orchestrator.execution_service.health_check()
    monitoring_health = await orchestrator.monitoring_service.health_check()
    
    all_healthy = all([
        signal_health.get("loaded"),
        monitoring_health.get("redis_connected")
    ])
    
    return {
        "status": "healthy" if all_healthy else "degraded",
        "services": {
            "data": data_health,
            "signal": signal_health,
            "execution": execution_health,
            "monitoring": monitoring_health
        },
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


@app.get("/status")
async def get_status():
    """Get orchestrator status"""
    orchestrator: TradingOrchestrator = app.state.orchestrator
    return orchestrator.get_status()


@app.get("/metrics")
async def get_metrics():
    """Get Prometheus metrics"""
    orchestrator: TradingOrchestrator = app.state.orchestrator
    return Response(
        content=orchestrator.monitoring_service.get_prometheus_metrics(),
        media_type="text/plain"
    )


@app.get("/algorithms")
async def get_algorithms():
    """Get loaded algorithms and their status"""
    orchestrator: TradingOrchestrator = app.state.orchestrator
    return orchestrator.signal_service.get_algo_status()


@app.post("/cycle")
async def run_signal_cycle(request: SignalCycleRequest, background_tasks: BackgroundTasks):
    """Execute a single signal generation and execution cycle"""
    orchestrator: TradingOrchestrator = app.state.orchestrator
    result = await orchestrator.run_signal_cycle(request.tier)
    return result


@app.post("/autonomous/start")
async def start_autonomous(request: AutonomousModeRequest):
    """Start autonomous trading mode"""
    orchestrator: TradingOrchestrator = app.state.orchestrator
    
    if orchestrator._running:
        raise HTTPException(status_code=400, detail="Autonomous mode already running")
    
    await orchestrator.start_autonomous_mode(request.interval_minutes)
    
    return {
        "status": "started",
        "interval_minutes": request.interval_minutes,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


@app.post("/autonomous/stop")
async def stop_autonomous():
    """Stop autonomous trading mode"""
    orchestrator: TradingOrchestrator = app.state.orchestrator
    
    if not orchestrator._running:
        raise HTTPException(status_code=400, detail="Autonomous mode not running")
    
    await orchestrator.stop_autonomous_mode()
    
    return {
        "status": "stopped",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


@app.get("/alerts")
async def get_alerts():
    """Get active alerts"""
    orchestrator: TradingOrchestrator = app.state.orchestrator
    alerts = orchestrator.monitoring_service.alert_manager.get_active_alerts()
    return {
        "alerts": [a.to_dict() for a in alerts],
        "count": len(alerts),
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


@app.get("/performance")
async def get_performance():
    """Get performance metrics"""
    orchestrator: TradingOrchestrator = app.state.orchestrator
    return orchestrator.monitoring_service.get_metrics_snapshot()


if __name__ == "__main__":
    import uvicorn
    
    config = TradingConfig()
    uvicorn.run(
        "trading.main:app",
        host="0.0.0.0",
        port=config.api_port,
        reload=config.env == "development"
    )

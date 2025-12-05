"""
Trading Arsenal - Execution Service
Handles order execution with safety guards and broker integration
"""

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal
from enum import Enum
from typing import Dict, List, Optional, Any
import json
import hashlib
import hmac

import aiohttp
import redis.asyncio as redis

from .signal_service import EnsembleSignal, SignalType


logger = logging.getLogger(__name__)


class OrderSide(Enum):
    BUY = "buy"
    SELL = "sell"


class OrderType(Enum):
    MARKET = "market"
    LIMIT = "limit"
    STOP = "stop"
    STOP_LIMIT = "stop_limit"


class OrderStatus(Enum):
    PENDING = "pending"
    SUBMITTED = "submitted"
    FILLED = "filled"
    PARTIALLY_FILLED = "partially_filled"
    CANCELLED = "cancelled"
    REJECTED = "rejected"
    EXPIRED = "expired"


@dataclass
class Order:
    """Trading order"""
    order_id: str
    symbol: str
    side: OrderSide
    order_type: OrderType
    quantity: float
    price: Optional[float] = None
    stop_price: Optional[float] = None
    status: OrderStatus = OrderStatus.PENDING
    filled_qty: float = 0.0
    filled_price: float = 0.0
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = None
    broker_order_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "order_id": self.order_id,
            "symbol": self.symbol,
            "side": self.side.value,
            "order_type": self.order_type.value,
            "quantity": self.quantity,
            "price": self.price,
            "stop_price": self.stop_price,
            "status": self.status.value,
            "filled_qty": self.filled_qty,
            "filled_price": self.filled_price,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "broker_order_id": self.broker_order_id,
            "metadata": self.metadata
        }


@dataclass
class Position:
    """Current position"""
    symbol: str
    quantity: float
    avg_price: float
    market_value: float
    unrealized_pnl: float
    realized_pnl: float = 0.0
    asset_class: str = "equity"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "symbol": self.symbol,
            "quantity": self.quantity,
            "avg_price": self.avg_price,
            "market_value": self.market_value,
            "unrealized_pnl": self.unrealized_pnl,
            "realized_pnl": self.realized_pnl,
            "asset_class": self.asset_class
        }


@dataclass
class ExecutionConfig:
    """Execution service configuration"""
    broker_api_key: str = ""
    broker_api_secret: str = ""
    broker_base_url: str = "https://paper-api.alpaca.markets"
    redis_url: str = "redis://localhost:6379/0"
    max_position_pct: float = 0.05  # 5% max per position
    max_drawdown: float = 0.20  # 20% max drawdown
    max_daily_trades: int = 50
    enabled: bool = True
    paper_trading: bool = True  # Safety: default to paper trading


class RiskGuard:
    """Risk management guards"""
    
    def __init__(self, config: ExecutionConfig):
        self.config = config
        self.daily_trades = 0
        self.last_reset = datetime.now(timezone.utc).date()
        self.portfolio_value = 100000.0  # Default
        self.current_drawdown = 0.0
        self.peak_value = 100000.0
    
    def reset_daily_counters(self) -> None:
        """Reset daily counters"""
        today = datetime.now(timezone.utc).date()
        if today > self.last_reset:
            self.daily_trades = 0
            self.last_reset = today
    
    def update_portfolio_metrics(self, current_value: float) -> None:
        """Update portfolio metrics"""
        self.portfolio_value = current_value
        self.peak_value = max(self.peak_value, current_value)
        self.current_drawdown = (self.peak_value - current_value) / self.peak_value
    
    def check_order(self, order: Order, current_positions: Dict[str, Position]) -> tuple[bool, str]:
        """Validate order against risk limits"""
        self.reset_daily_counters()
        
        # Check daily trade limit
        if self.daily_trades >= self.config.max_daily_trades:
            return False, "Daily trade limit reached"
        
        # Check drawdown limit
        if self.current_drawdown >= self.config.max_drawdown:
            # Only allow sell orders when drawdown limit hit
            if order.side == OrderSide.BUY:
                return False, "Drawdown limit reached - only sells allowed"
        
        # Check position concentration
        order_value = order.quantity * (order.price or 0)
        if order_value > self.portfolio_value * self.config.max_position_pct:
            return False, f"Order exceeds max position limit ({self.config.max_position_pct*100}%)"
        
        # Check existing position
        if order.symbol in current_positions:
            existing = current_positions[order.symbol]
            total_value = existing.market_value + order_value
            if order.side == OrderSide.BUY and total_value > self.portfolio_value * self.config.max_position_pct:
                return False, "Would exceed max position concentration"
        
        return True, "OK"
    
    def record_trade(self) -> None:
        """Record executed trade"""
        self.reset_daily_counters()
        self.daily_trades += 1


class BrokerClient:
    """Generic broker API client (Alpaca-compatible)"""
    
    def __init__(self, config: ExecutionConfig):
        self.config = config
        self.base_url = config.broker_base_url
        self._session: Optional[aiohttp.ClientSession] = None
    
    @property
    def headers(self) -> Dict[str, str]:
        return {
            "APCA-API-KEY-ID": self.config.broker_api_key,
            "APCA-API-SECRET-KEY": self.config.broker_api_secret,
            "Content-Type": "application/json"
        }
    
    async def _ensure_session(self) -> aiohttp.ClientSession:
        if self._session is None:
            self._session = aiohttp.ClientSession()
        return self._session
    
    async def close(self) -> None:
        if self._session:
            await self._session.close()
            self._session = None
    
    async def get_account(self) -> Dict[str, Any]:
        """Get account information"""
        session = await self._ensure_session()
        async with session.get(f"{self.base_url}/v2/account", headers=self.headers) as resp:
            if resp.status != 200:
                raise Exception(f"Account API error: {resp.status}")
            return await resp.json()
    
    async def get_positions(self) -> List[Position]:
        """Get current positions"""
        session = await self._ensure_session()
        async with session.get(f"{self.base_url}/v2/positions", headers=self.headers) as resp:
            if resp.status != 200:
                raise Exception(f"Positions API error: {resp.status}")
            
            data = await resp.json()
            return [
                Position(
                    symbol=p["symbol"],
                    quantity=float(p["qty"]),
                    avg_price=float(p["avg_entry_price"]),
                    market_value=float(p["market_value"]),
                    unrealized_pnl=float(p["unrealized_pl"]),
                    asset_class=p.get("asset_class", "equity")
                )
                for p in data
            ]
    
    async def submit_order(self, order: Order) -> Dict[str, Any]:
        """Submit order to broker"""
        session = await self._ensure_session()
        
        payload = {
            "symbol": order.symbol,
            "qty": str(order.quantity),
            "side": order.side.value,
            "type": order.order_type.value,
            "time_in_force": "day"
        }
        
        if order.price:
            payload["limit_price"] = str(order.price)
        if order.stop_price:
            payload["stop_price"] = str(order.stop_price)
        
        async with session.post(
            f"{self.base_url}/v2/orders",
            headers=self.headers,
            json=payload
        ) as resp:
            if resp.status not in (200, 201):
                error = await resp.text()
                raise Exception(f"Order submit error: {resp.status} - {error}")
            
            return await resp.json()
    
    async def cancel_order(self, broker_order_id: str) -> bool:
        """Cancel an order"""
        session = await self._ensure_session()
        async with session.delete(
            f"{self.base_url}/v2/orders/{broker_order_id}",
            headers=self.headers
        ) as resp:
            return resp.status in (200, 204)
    
    async def get_order(self, broker_order_id: str) -> Dict[str, Any]:
        """Get order status"""
        session = await self._ensure_session()
        async with session.get(
            f"{self.base_url}/v2/orders/{broker_order_id}",
            headers=self.headers
        ) as resp:
            if resp.status != 200:
                raise Exception(f"Get order error: {resp.status}")
            return await resp.json()


class ExecutionService:
    """Main execution service"""
    
    def __init__(self, config: ExecutionConfig):
        self.config = config
        self.broker = BrokerClient(config)
        self.risk_guard = RiskGuard(config)
        self._redis: Optional[redis.Redis] = None
        self._positions: Dict[str, Position] = {}
        self._pending_orders: Dict[str, Order] = {}
        self._order_counter = 0
    
    async def connect(self) -> None:
        """Connect to Redis and broker"""
        self._redis = redis.from_url(self.config.redis_url)
        await self._redis.ping()
        
        # Load account info
        try:
            account = await self.broker.get_account()
            self.risk_guard.update_portfolio_metrics(float(account.get("portfolio_value", 100000)))
            logger.info(f"Connected to broker. Portfolio value: ${self.risk_guard.portfolio_value:,.2f}")
        except Exception as e:
            logger.warning(f"Could not connect to broker: {e}. Running in simulation mode.")
        
        # Load positions
        await self.refresh_positions()
    
    async def disconnect(self) -> None:
        """Disconnect from services"""
        if self._redis:
            await self._redis.close()
        await self.broker.close()
    
    async def refresh_positions(self) -> None:
        """Refresh current positions from broker"""
        try:
            positions = await self.broker.get_positions()
            self._positions = {p.symbol: p for p in positions}
            logger.info(f"Loaded {len(positions)} positions")
        except Exception as e:
            logger.warning(f"Could not refresh positions: {e}")
    
    def _generate_order_id(self) -> str:
        """Generate unique order ID"""
        self._order_counter += 1
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
        return f"ORD-{timestamp}-{self._order_counter:06d}"
    
    async def signal_to_orders(self, signals: List[EnsembleSignal]) -> List[Order]:
        """Convert ensemble signals to orders"""
        orders = []
        
        for signal in signals:
            if signal.final_signal == SignalType.NEUTRAL:
                continue
            
            # Calculate order quantity based on weight
            target_value = self.risk_guard.portfolio_value * signal.final_weight
            
            # Get current price (simplified - would use real price)
            current_price = 100.0  # Placeholder
            quantity = target_value / current_price
            
            if quantity < 1:
                continue
            
            # Determine order side
            current_pos = self._positions.get(signal.symbol)
            current_qty = current_pos.quantity if current_pos else 0.0
            
            if signal.final_signal == SignalType.LONG:
                if current_qty >= 0:
                    # Buy more or initiate long
                    side = OrderSide.BUY
                    order_qty = quantity
                else:
                    # Close short first
                    side = OrderSide.BUY
                    order_qty = abs(current_qty)
            else:  # SHORT or REDUCE
                if current_qty > 0:
                    # Sell to reduce or close
                    side = OrderSide.SELL
                    order_qty = min(quantity, current_qty)
                else:
                    # Short (if allowed)
                    continue  # Skip shorts for now
            
            order = Order(
                order_id=self._generate_order_id(),
                symbol=signal.symbol,
                side=side,
                order_type=OrderType.MARKET,
                quantity=order_qty,
                metadata={
                    "signal_type": signal.final_signal.value,
                    "signal_weight": signal.final_weight,
                    "consensus": signal.consensus_score
                }
            )
            
            orders.append(order)
        
        return orders
    
    async def execute_order(self, order: Order) -> Order:
        """Execute a single order with risk checks"""
        # Risk check
        valid, reason = self.risk_guard.check_order(order, self._positions)
        if not valid:
            order.status = OrderStatus.REJECTED
            order.metadata["rejection_reason"] = reason
            logger.warning(f"Order {order.order_id} rejected: {reason}")
            return order
        
        if not self.config.enabled:
            order.status = OrderStatus.REJECTED
            order.metadata["rejection_reason"] = "Execution disabled"
            return order
        
        try:
            # Submit to broker
            result = await self.broker.submit_order(order)
            
            order.broker_order_id = result.get("id")
            order.status = OrderStatus.SUBMITTED
            order.updated_at = datetime.now(timezone.utc)
            
            self._pending_orders[order.order_id] = order
            self.risk_guard.record_trade()
            
            logger.info(f"Order {order.order_id} submitted: {order.side.value} {order.quantity} {order.symbol}")
            
            # Store in Redis
            if self._redis:
                await self._redis.hset(
                    "trading:orders",
                    order.order_id,
                    json.dumps(order.to_dict())
                )
            
        except Exception as e:
            order.status = OrderStatus.REJECTED
            order.metadata["rejection_reason"] = str(e)
            logger.error(f"Order {order.order_id} failed: {e}")
        
        return order
    
    async def execute_signals(self, signals: List[EnsembleSignal]) -> List[Order]:
        """Execute trading signals"""
        orders = await self.signal_to_orders(signals)
        
        executed_orders = []
        for order in orders:
            result = await self.execute_order(order)
            executed_orders.append(result)
        
        logger.info(f"Executed {len(executed_orders)} orders from {len(signals)} signals")
        
        return executed_orders
    
    async def get_order_status(self, order_id: str) -> Optional[Order]:
        """Get order status"""
        if order_id in self._pending_orders:
            order = self._pending_orders[order_id]
            
            # Refresh from broker if submitted
            if order.broker_order_id and order.status == OrderStatus.SUBMITTED:
                try:
                    broker_order = await self.broker.get_order(order.broker_order_id)
                    order.status = OrderStatus(broker_order.get("status", "pending"))
                    order.filled_qty = float(broker_order.get("filled_qty", 0))
                    order.filled_price = float(broker_order.get("filled_avg_price", 0))
                except Exception as e:
                    logger.error(f"Error refreshing order {order_id}: {e}")
            
            return order
        
        return None
    
    async def cancel_order(self, order_id: str) -> bool:
        """Cancel an order"""
        order = self._pending_orders.get(order_id)
        if not order or not order.broker_order_id:
            return False
        
        try:
            await self.broker.cancel_order(order.broker_order_id)
            order.status = OrderStatus.CANCELLED
            order.updated_at = datetime.now(timezone.utc)
            return True
        except Exception as e:
            logger.error(f"Error cancelling order {order_id}: {e}")
            return False
    
    async def health_check(self) -> Dict[str, Any]:
        """Check service health"""
        broker_connected = False
        try:
            await self.broker.get_account()
            broker_connected = True
        except Exception:
            pass
        
        return {
            "enabled": self.config.enabled,
            "paper_trading": self.config.paper_trading,
            "broker_connected": broker_connected,
            "redis_connected": self._redis is not None,
            "portfolio_value": self.risk_guard.portfolio_value,
            "current_drawdown": self.risk_guard.current_drawdown,
            "daily_trades": self.risk_guard.daily_trades,
            "pending_orders": len(self._pending_orders),
            "positions": len(self._positions),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

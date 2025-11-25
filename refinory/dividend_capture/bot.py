"""
DiviDen Ninja Bot - Main Bot Module
Core dividend capture bot implementation
"""

import asyncio
import logging
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum

import structlog

from .config import DividendCaptureConfig, TradingMode, get_dividend_config
from .hlmcr_governance import HLMCRGovernor, GovernanceDecision, DecisionType


logger = structlog.get_logger()


class BotState(Enum):
    """Bot operational state"""
    IDLE = "idle"
    SCANNING = "scanning"
    ANALYZING = "analyzing"
    TRADING = "trading"
    PAUSED = "paused"
    ERROR = "error"
    SHUTDOWN = "shutdown"


@dataclass
class DividendOpportunity:
    """Represents a dividend capture opportunity"""
    symbol: str
    company_name: str
    ex_dividend_date: datetime
    record_date: datetime
    payment_date: datetime
    dividend_amount: float
    dividend_yield: float
    current_price: float
    market_cap: float
    sector: str
    
    # Analysis fields
    expected_return: float = 0.0
    risk_score: float = 0.0
    confidence_score: float = 0.0
    strategy_type: str = "ex_dividend"
    
    # Execution fields
    recommended_shares: int = 0
    recommended_entry: float = 0.0
    stop_loss: float = 0.0
    take_profit: float = 0.0


@dataclass
class TradeExecution:
    """Represents an executed trade"""
    id: str
    symbol: str
    side: str  # buy/sell
    quantity: int
    price: float
    timestamp: datetime
    strategy: str
    status: str
    
    # Governance
    governance_decision_id: Optional[str] = None
    approved_by: str = "hlmcr"
    
    # P&L
    realized_pnl: float = 0.0
    dividend_captured: float = 0.0


@dataclass
class PortfolioState:
    """Current portfolio state"""
    cash: float = 0.0
    equity: float = 0.0
    positions: Dict[str, Dict] = field(default_factory=dict)
    pending_orders: List[Dict] = field(default_factory=list)
    
    # Daily stats
    daily_pnl: float = 0.0
    daily_trades: int = 0
    daily_dividends: float = 0.0


class DividendCaptureBot:
    """
    DiviDen Ninja Bot - Automated Dividend Capture System
    
    Implements HLMCR-governed trading strategies for capturing dividends
    while maintaining compliance with nonprofit flow-through requirements.
    """
    
    def __init__(self, config: Optional[DividendCaptureConfig] = None):
        self.config = config or get_dividend_config()
        self.state = BotState.IDLE
        self.governor = HLMCRGovernor(self.config.governance)
        self.portfolio = PortfolioState()
        
        # Tracking
        self.opportunities: List[DividendOpportunity] = []
        self.executions: List[TradeExecution] = []
        self.errors: List[Dict] = []
        
        # Runtime
        self._running = False
        self._last_scan: Optional[datetime] = None
        
        logger.info(
            "DiviDen Ninja Bot initialized",
            bot_id=self.config.bot_id,
            mode=self.config.mode.value,
            environment=self.config.environment
        )
    
    async def start(self) -> None:
        """Start the dividend capture bot"""
        logger.info("Starting DiviDen Ninja Bot", bot_id=self.config.bot_id)
        
        # Validate configuration
        errors = self.config.validate()
        if errors:
            logger.error("Configuration validation failed", errors=errors)
            self.state = BotState.ERROR
            raise ValueError(f"Configuration errors: {errors}")
        
        self._running = True
        self.state = BotState.IDLE
        
        # Main event loop
        while self._running:
            try:
                await self._run_cycle()
            except Exception as e:
                logger.error("Error in bot cycle", error=str(e))
                self.errors.append({
                    "timestamp": datetime.now(timezone.utc),
                    "error": str(e),
                    "state": self.state.value
                })
                await asyncio.sleep(60)  # Wait before retry
    
    async def stop(self) -> None:
        """Stop the dividend capture bot"""
        logger.info("Stopping DiviDen Ninja Bot", bot_id=self.config.bot_id)
        self._running = False
        self.state = BotState.SHUTDOWN
    
    async def _run_cycle(self) -> None:
        """Execute one cycle of the bot's main loop"""
        now = datetime.now(timezone.utc)
        
        # Check if market is open
        if not self._is_market_hours(now):
            logger.debug("Outside market hours, sleeping")
            await asyncio.sleep(300)  # Check every 5 minutes
            return
        
        # Check if scan is due
        if self._last_scan and (now - self._last_scan).seconds < self.config.scan_interval_minutes * 60:
            await asyncio.sleep(60)
            return
        
        # Run scan and analysis
        self.state = BotState.SCANNING
        opportunities = await self._scan_opportunities()
        
        self.state = BotState.ANALYZING
        analyzed = await self._analyze_opportunities(opportunities)
        
        # Filter and rank
        viable = [o for o in analyzed if o.confidence_score >= 0.6]
        viable.sort(key=lambda x: x.expected_return, reverse=True)
        
        self.opportunities = viable
        logger.info(
            "Scan complete",
            total_found=len(opportunities),
            viable_count=len(viable)
        )
        
        # Execute top opportunities (subject to governance)
        if viable:
            self.state = BotState.TRADING
            await self._execute_opportunities(viable[:5])  # Top 5 only
        
        self._last_scan = now
        self.state = BotState.IDLE
    
    async def _scan_opportunities(self) -> List[DividendOpportunity]:
        """Scan market for dividend opportunities"""
        logger.info("Scanning for dividend opportunities")
        
        # TODO: Integrate with real data source
        # This is a placeholder implementation
        opportunities = []
        
        # In production, this would:
        # 1. Query dividend calendar APIs
        # 2. Filter by upcoming ex-dividend dates
        # 3. Check liquidity and market cap requirements
        # 4. Verify dividend announcements
        
        return opportunities
    
    async def _analyze_opportunities(
        self, 
        opportunities: List[DividendOpportunity]
    ) -> List[DividendOpportunity]:
        """Analyze opportunities for expected return and risk"""
        analyzed = []
        
        for opp in opportunities:
            try:
                # Calculate expected return
                opp.expected_return = self._calculate_expected_return(opp)
                
                # Calculate risk score (0-1, lower is better)
                opp.risk_score = self._calculate_risk_score(opp)
                
                # Calculate confidence score (0-1, higher is better)
                opp.confidence_score = self._calculate_confidence(opp)
                
                # Determine position sizing
                opp.recommended_shares = self._calculate_position_size(opp)
                opp.recommended_entry = opp.current_price
                opp.stop_loss = opp.current_price * (1 - self.config.risk.stop_loss_pct)
                opp.take_profit = opp.current_price + opp.dividend_amount
                
                analyzed.append(opp)
                
            except Exception as e:
                logger.warning(
                    "Failed to analyze opportunity",
                    symbol=opp.symbol,
                    error=str(e)
                )
        
        return analyzed
    
    async def _execute_opportunities(
        self, 
        opportunities: List[DividendOpportunity]
    ) -> None:
        """Execute trades for selected opportunities"""
        for opp in opportunities:
            try:
                # Check position limits
                if not self._check_position_limits(opp):
                    logger.info("Skipping due to position limits", symbol=opp.symbol)
                    continue
                
                # Request governance approval
                decision = await self.governor.request_approval(
                    decision_type=DecisionType.TRADE_ENTRY,
                    context={
                        "symbol": opp.symbol,
                        "strategy": opp.strategy_type,
                        "shares": opp.recommended_shares,
                        "price": opp.recommended_entry,
                        "expected_return": opp.expected_return,
                        "risk_score": opp.risk_score,
                    }
                )
                
                if decision.approved:
                    # Execute trade
                    execution = await self._place_order(opp, decision)
                    if execution:
                        self.executions.append(execution)
                        logger.info(
                            "Trade executed",
                            symbol=opp.symbol,
                            shares=execution.quantity,
                            price=execution.price
                        )
                else:
                    logger.info(
                        "Trade rejected by governance",
                        symbol=opp.symbol,
                        reason=decision.reason
                    )
                    
            except Exception as e:
                logger.error(
                    "Failed to execute opportunity",
                    symbol=opp.symbol,
                    error=str(e)
                )
    
    async def _place_order(
        self, 
        opportunity: DividendOpportunity,
        decision: GovernanceDecision
    ) -> Optional[TradeExecution]:
        """Place order through broker API"""
        if self.config.mode == TradingMode.PAPER:
            # Simulate paper trade
            return TradeExecution(
                id=f"paper-{datetime.now().timestamp()}",
                symbol=opportunity.symbol,
                side="buy",
                quantity=opportunity.recommended_shares,
                price=opportunity.recommended_entry,
                timestamp=datetime.now(timezone.utc),
                strategy=opportunity.strategy_type,
                status="filled",
                governance_decision_id=decision.decision_id,
            )
        
        # TODO: Implement real broker API integration
        # This would integrate with Alpaca, Interactive Brokers, etc.
        return None
    
    def _calculate_expected_return(self, opp: DividendOpportunity) -> float:
        """Calculate expected return for an opportunity"""
        # Simple calculation: dividend yield adjusted for holding period and risk
        base_return = opp.dividend_yield
        
        # Adjust for expected price movement
        # (stocks often drop by dividend amount on ex-date)
        price_adjustment = -0.3  # Expect 30% of dividend captured net
        
        return base_return * (1 + price_adjustment)
    
    def _calculate_risk_score(self, opp: DividendOpportunity) -> float:
        """Calculate risk score (0-1, lower is better)"""
        risk = 0.0
        
        # Liquidity risk
        if opp.market_cap < 1_000_000_000:  # < $1B
            risk += 0.2
        
        # Yield risk (very high yields may indicate problems)
        if opp.dividend_yield > 0.10:  # > 10% yield
            risk += 0.2
        
        # Sector risk (some sectors more volatile)
        volatile_sectors = ["Energy", "Technology", "Consumer Discretionary"]
        if opp.sector in volatile_sectors:
            risk += 0.1
        
        return min(risk, 1.0)
    
    def _calculate_confidence(self, opp: DividendOpportunity) -> float:
        """Calculate confidence score (0-1, higher is better)"""
        confidence = 0.5  # Base confidence
        
        # Increase for established companies
        if opp.market_cap > 10_000_000_000:  # > $10B
            confidence += 0.2
        
        # Increase for reasonable yields
        if 0.02 <= opp.dividend_yield <= 0.06:
            confidence += 0.2
        
        # Decrease for high risk
        confidence -= opp.risk_score * 0.3
        
        return max(0.0, min(confidence, 1.0))
    
    def _calculate_position_size(self, opp: DividendOpportunity) -> int:
        """Calculate recommended position size"""
        # Maximum position value
        max_position = self.portfolio.equity * self.config.risk.max_single_position_pct
        
        # Adjust for confidence
        adjusted_max = max_position * opp.confidence_score
        
        # Calculate shares
        if opp.current_price > 0:
            shares = int(adjusted_max / opp.current_price)
        else:
            shares = 0
        
        return max(0, shares)
    
    def _check_position_limits(self, opp: DividendOpportunity) -> bool:
        """Check if trade would exceed position limits"""
        # Check position count
        if len(self.portfolio.positions) >= self.config.risk.max_position_count:
            return False
        
        # Check if already holding
        if opp.symbol in self.portfolio.positions:
            return False
        
        # Check daily trade limit
        if self.portfolio.daily_trades >= 20:  # Simple limit
            return False
        
        return True
    
    def _is_market_hours(self, dt: datetime) -> bool:
        """Check if current time is during market hours"""
        # Simplified check for US market hours
        # In production, use a proper market calendar
        hour = dt.hour
        weekday = dt.weekday()
        
        # Monday-Friday, 9:30 AM - 4:00 PM ET (simplified)
        if weekday >= 5:  # Weekend
            return False
        
        # Rough approximation (would need timezone handling)
        if 14 <= hour < 21:  # ~9:30 AM - 4 PM ET in UTC
            return True
        
        return False
    
    def get_status(self) -> Dict[str, Any]:
        """Get current bot status"""
        return {
            "bot_id": self.config.bot_id,
            "state": self.state.value,
            "mode": self.config.mode.value,
            "portfolio": {
                "cash": self.portfolio.cash,
                "equity": self.portfolio.equity,
                "position_count": len(self.portfolio.positions),
            },
            "stats": {
                "opportunities_found": len(self.opportunities),
                "executions_today": len([
                    e for e in self.executions 
                    if e.timestamp.date() == datetime.now(timezone.utc).date()
                ]),
                "errors_count": len(self.errors),
            },
            "last_scan": self._last_scan.isoformat() if self._last_scan else None,
        }

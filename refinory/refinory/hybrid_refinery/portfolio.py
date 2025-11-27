"""
Portfolio Manager
=================

Manages portfolio construction, position tracking, and flow allocation
for the Hybrid Refinery system.

Features:
    - Position tracking for core and tactical sleeves
    - Flow allocation (70/23/7 split)
    - Sector and position weight monitoring
    - Rebalancing recommendations
"""

from dataclasses import dataclass, field
from datetime import datetime, date
from typing import List, Dict, Any, Optional
from enum import Enum
import structlog

from .config import HybridRefineryConfig, PortfolioGuardrails

logger = structlog.get_logger()


class PositionType(Enum):
    """Type of position"""
    CORE = "core"  # Dividend engine core
    TACTICAL = "tactical"  # RANCO/PID sleeve
    TREASURY = "treasury"  # Treasury buffer
    SWARMGATE = "swarmgate"  # SwarmGate allocation


class PositionStatus(Enum):
    """Status of a position"""
    OPEN = "open"
    CLOSED = "closed"
    PENDING = "pending"
    PARTIAL = "partial"  # Partially filled


@dataclass
class Position:
    """Individual position in the portfolio"""
    symbol: str
    name: str
    position_type: PositionType
    
    # Position details
    shares: int = 0
    avg_cost: float = 0.0
    current_price: float = 0.0
    
    # Sector/industry
    sector: str = ""
    industry: str = ""
    
    # Dividend info (for core positions)
    annual_dividend: float = 0.0
    dividend_yield: float = 0.0
    next_ex_div_date: Optional[date] = None
    
    # Status
    status: PositionStatus = PositionStatus.OPEN
    
    # Timestamps
    opened_at: datetime = field(default_factory=datetime.now)
    last_updated: datetime = field(default_factory=datetime.now)
    
    @property
    def market_value(self) -> float:
        """Current market value of position"""
        return self.shares * self.current_price
    
    @property
    def cost_basis(self) -> float:
        """Total cost basis"""
        return self.shares * self.avg_cost
    
    @property
    def unrealized_pnl(self) -> float:
        """Unrealized P&L"""
        return self.market_value - self.cost_basis
    
    @property
    def unrealized_pnl_pct(self) -> float:
        """Unrealized P&L percentage"""
        if self.cost_basis > 0:
            return self.unrealized_pnl / self.cost_basis
        return 0.0
    
    @property
    def expected_annual_income(self) -> float:
        """Expected annual dividend income"""
        return self.shares * self.annual_dividend
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "symbol": self.symbol,
            "name": self.name,
            "position_type": self.position_type.value,
            "shares": self.shares,
            "avg_cost": self.avg_cost,
            "current_price": self.current_price,
            "market_value": self.market_value,
            "cost_basis": self.cost_basis,
            "unrealized_pnl": self.unrealized_pnl,
            "unrealized_pnl_pct": self.unrealized_pnl_pct,
            "sector": self.sector,
            "industry": self.industry,
            "annual_dividend": self.annual_dividend,
            "dividend_yield": self.dividend_yield,
            "expected_annual_income": self.expected_annual_income,
            "status": self.status.value,
            "opened_at": self.opened_at.isoformat(),
            "last_updated": self.last_updated.isoformat(),
        }


@dataclass
class FlowAllocation:
    """Allocation of dividend/income flows"""
    total_income: float
    
    # 70/23/7 split
    core_reinvest: float = 0.0
    treasury_buffer: float = 0.0
    swarmgate: float = 0.0
    
    # Percentages
    core_reinvest_pct: float = 0.70
    treasury_buffer_pct: float = 0.23
    swarmgate_pct: float = 0.07
    
    # Cumulative totals
    cumulative_reinvested: float = 0.0
    cumulative_treasury: float = 0.0
    cumulative_swarmgate: float = 0.0
    
    # Timestamp
    period_start: datetime = field(default_factory=datetime.now)
    period_end: Optional[datetime] = None
    
    def calculate_allocation(self):
        """Calculate allocation based on total income"""
        self.core_reinvest = self.total_income * self.core_reinvest_pct
        self.treasury_buffer = self.total_income * self.treasury_buffer_pct
        self.swarmgate = self.total_income * self.swarmgate_pct
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "total_income": self.total_income,
            "core_reinvest": self.core_reinvest,
            "treasury_buffer": self.treasury_buffer,
            "swarmgate": self.swarmgate,
            "percentages": {
                "core_reinvest": f"{self.core_reinvest_pct:.0%}",
                "treasury_buffer": f"{self.treasury_buffer_pct:.0%}",
                "swarmgate": f"{self.swarmgate_pct:.0%}",
            },
            "cumulative": {
                "reinvested": self.cumulative_reinvested,
                "treasury": self.cumulative_treasury,
                "swarmgate": self.cumulative_swarmgate,
            },
            "period_start": self.period_start.isoformat(),
            "period_end": self.period_end.isoformat() if self.period_end else None,
        }


class PortfolioManager:
    """
    Portfolio Manager for Hybrid Refinery
    
    Manages:
        - Core dividend positions (85% allocation)
        - Tactical RANCO/PID positions (15% allocation)
        - Treasury buffer
        - SwarmGate routing
    """
    
    def __init__(self, config: HybridRefineryConfig):
        self.config = config
        self.guardrails = config.guardrails
        
        # Position storage
        self.core_positions: List[Position] = []
        self.tactical_positions: List[Position] = []
        
        # Cash/buffer tracking
        self.treasury_buffer: float = 0.0
        self.swarmgate_balance: float = 0.0
        self.available_cash: float = 0.0
        
        # Flow tracking
        self.flow_history: List[FlowAllocation] = []
        self.current_flow: Optional[FlowAllocation] = None
        
        # Performance tracking
        self.peak_value: float = config.total_capital
        self.current_drawdown: float = 0.0
        
        logger.info("Portfolio Manager initialized",
                   total_capital=config.total_capital,
                   core_allocation=f"{1 - config.guardrails.tactical_max_allocation:.0%}",
                   tactical_allocation=f"{config.guardrails.tactical_max_allocation:.0%}")
    
    # ==================== Position Management ====================
    
    def add_position(self, position: Position) -> bool:
        """Add a position to the portfolio"""
        # Check guardrails
        if position.position_type == PositionType.CORE:
            if len(self.core_positions) >= self.guardrails.max_positions:
                logger.warning("Cannot add position - max positions reached",
                             current=len(self.core_positions),
                             max=self.guardrails.max_positions)
                return False
            
            # Check position weight
            weight = position.market_value / self.get_total_value() if self.get_total_value() > 0 else 0
            if weight > self.guardrails.max_position_weight:
                logger.warning("Position weight exceeds guardrail",
                             symbol=position.symbol,
                             weight=f"{weight:.1%}",
                             max=f"{self.guardrails.max_position_weight:.0%}")
                return False
            
            # Check sector weight
            sector_weight = self._get_sector_weight(position.sector, include_new=position.market_value)
            if sector_weight > self.guardrails.max_sector_weight:
                logger.warning("Sector weight would exceed guardrail",
                             sector=position.sector,
                             weight=f"{sector_weight:.1%}",
                             max=f"{self.guardrails.max_sector_weight:.0%}")
                return False
            
            self.core_positions.append(position)
            
        elif position.position_type == PositionType.TACTICAL:
            # Check tactical allocation cap
            tactical_value = self.get_tactical_value() + position.market_value
            max_tactical = self.config.total_capital * self.guardrails.tactical_max_allocation
            
            if tactical_value > max_tactical:
                logger.warning("Tactical allocation would exceed cap",
                             current=self.get_tactical_value(),
                             new=position.market_value,
                             max=max_tactical)
                return False
            
            self.tactical_positions.append(position)
        
        logger.info("Position added",
                   symbol=position.symbol,
                   type=position.position_type.value,
                   value=position.market_value)
        
        return True
    
    def update_position(self, symbol: str, updates: Dict[str, Any]) -> bool:
        """Update an existing position"""
        position = self.get_position(symbol)
        if not position:
            logger.warning("Position not found for update", symbol=symbol)
            return False
        
        for key, value in updates.items():
            if hasattr(position, key):
                setattr(position, key, value)
        
        position.last_updated = datetime.now()
        
        logger.debug("Position updated", symbol=symbol, updates=list(updates.keys()))
        return True
    
    def close_position(self, symbol: str, exit_price: float) -> Optional[Position]:
        """Close a position"""
        position = self.get_position(symbol)
        if not position:
            logger.warning("Position not found for closing", symbol=symbol)
            return None
        
        position.current_price = exit_price
        position.status = PositionStatus.CLOSED
        position.last_updated = datetime.now()
        
        # Remove from active positions
        if position.position_type == PositionType.CORE:
            self.core_positions = [p for p in self.core_positions if p.symbol != symbol]
        elif position.position_type == PositionType.TACTICAL:
            self.tactical_positions = [p for p in self.tactical_positions if p.symbol != symbol]
        
        logger.info("Position closed",
                   symbol=symbol,
                   pnl=position.unrealized_pnl,
                   pnl_pct=f"{position.unrealized_pnl_pct:.1%}")
        
        return position
    
    def get_position(self, symbol: str) -> Optional[Position]:
        """Get a position by symbol"""
        for position in self.core_positions + self.tactical_positions:
            if position.symbol == symbol:
                return position
        return None
    
    # ==================== Value Calculations ====================
    
    def get_total_value(self) -> float:
        """Get total portfolio value"""
        return (
            self.get_core_value() +
            self.get_tactical_value() +
            self.treasury_buffer +
            self.swarmgate_balance +
            self.available_cash
        )
    
    def get_core_value(self) -> float:
        """Get total value of core positions"""
        return sum(p.market_value for p in self.core_positions)
    
    def get_tactical_value(self) -> float:
        """Get total value of tactical positions"""
        return sum(p.market_value for p in self.tactical_positions)
    
    def _get_sector_weight(self, sector: str, include_new: float = 0) -> float:
        """Calculate sector weight"""
        sector_value = sum(
            p.market_value for p in self.core_positions 
            if p.sector == sector
        ) + include_new
        
        total = self.get_core_value() + include_new
        return sector_value / total if total > 0 else 0
    
    # ==================== Income & Flow Management ====================
    
    def record_dividend_income(self, symbol: str, amount: float) -> FlowAllocation:
        """
        Record dividend income and allocate to flows
        
        70% → Core reinvest
        23% → Treasury buffer
        7%  → SwarmGate
        """
        flow = FlowAllocation(
            total_income=amount,
            core_reinvest_pct=self.guardrails.core_reinvest_pct,
            treasury_buffer_pct=self.guardrails.treasury_buffer_pct,
            swarmgate_pct=self.guardrails.swarmgate_pct,
        )
        flow.calculate_allocation()
        
        # Update balances
        self.available_cash += flow.core_reinvest  # For reinvestment
        self.treasury_buffer += flow.treasury_buffer
        self.swarmgate_balance += flow.swarmgate
        
        # Update cumulative totals
        flow.cumulative_reinvested = self.get_cumulative_reinvested() + flow.core_reinvest
        flow.cumulative_treasury = self.treasury_buffer
        flow.cumulative_swarmgate = self.swarmgate_balance
        
        self.flow_history.append(flow)
        
        logger.info("Dividend income recorded",
                   symbol=symbol,
                   amount=amount,
                   reinvest=flow.core_reinvest,
                   treasury=flow.treasury_buffer,
                   swarmgate=flow.swarmgate)
        
        return flow
    
    def get_cumulative_reinvested(self) -> float:
        """Get total amount reinvested"""
        return sum(f.core_reinvest for f in self.flow_history)
    
    def get_expected_annual_income(self) -> float:
        """Get expected annual dividend income from core positions"""
        return sum(p.expected_annual_income for p in self.core_positions)
    
    def get_portfolio_yield(self) -> float:
        """Get portfolio dividend yield"""
        core_value = self.get_core_value()
        if core_value > 0:
            return self.get_expected_annual_income() / core_value
        return 0.0
    
    # ==================== Drawdown Management ====================
    
    def update_drawdown(self) -> float:
        """Update and return current drawdown"""
        current_value = self.get_total_value()
        
        # Update peak
        if current_value > self.peak_value:
            self.peak_value = current_value
        
        # Calculate drawdown
        if self.peak_value > 0:
            self.current_drawdown = (self.peak_value - current_value) / self.peak_value
        
        return self.current_drawdown
    
    def is_in_drawdown_mode(self) -> bool:
        """Check if portfolio is in drawdown risk-off mode"""
        return self.current_drawdown > self.guardrails.max_drawdown_threshold
    
    # ==================== Allocation Analysis ====================
    
    def get_allocation_breakdown(self) -> Dict[str, Any]:
        """Get detailed allocation breakdown"""
        total = self.get_total_value()
        core = self.get_core_value()
        tactical = self.get_tactical_value()
        
        return {
            "total_value": total,
            "core": {
                "value": core,
                "weight": core / total if total > 0 else 0,
                "positions": len(self.core_positions),
            },
            "tactical": {
                "value": tactical,
                "weight": tactical / total if total > 0 else 0,
                "positions": len(self.tactical_positions),
            },
            "treasury_buffer": {
                "value": self.treasury_buffer,
                "weight": self.treasury_buffer / total if total > 0 else 0,
            },
            "swarmgate": {
                "value": self.swarmgate_balance,
                "weight": self.swarmgate_balance / total if total > 0 else 0,
            },
            "available_cash": {
                "value": self.available_cash,
                "weight": self.available_cash / total if total > 0 else 0,
            },
        }
    
    def get_sector_breakdown(self) -> Dict[str, Dict[str, Any]]:
        """Get sector allocation breakdown"""
        sectors: Dict[str, Dict[str, Any]] = {}
        total = self.get_core_value()
        
        for position in self.core_positions:
            if position.sector not in sectors:
                sectors[position.sector] = {
                    "value": 0.0,
                    "weight": 0.0,
                    "positions": [],
                    "income": 0.0,
                }
            
            sectors[position.sector]["value"] += position.market_value
            sectors[position.sector]["positions"].append(position.symbol)
            sectors[position.sector]["income"] += position.expected_annual_income
        
        # Calculate weights
        for sector in sectors:
            if total > 0:
                sectors[sector]["weight"] = sectors[sector]["value"] / total
            
            # Check guardrail
            sectors[sector]["exceeds_guardrail"] = (
                sectors[sector]["weight"] > self.guardrails.max_sector_weight
            )
        
        return sectors
    
    # ==================== Rebalancing ====================
    
    def get_rebalancing_recommendations(self) -> List[Dict[str, Any]]:
        """Generate rebalancing recommendations"""
        recommendations = []
        total = self.get_total_value()
        
        if total <= 0:
            return recommendations
        
        # Check position weights
        for position in self.core_positions:
            weight = position.market_value / total
            if weight > self.guardrails.max_position_weight * 1.1:  # 10% buffer before flagging
                recommendations.append({
                    "type": "trim",
                    "symbol": position.symbol,
                    "current_weight": weight,
                    "target_weight": self.guardrails.max_position_weight,
                    "action": f"Reduce {position.symbol} from {weight:.1%} to {self.guardrails.max_position_weight:.0%}",
                })
        
        # Check sector weights
        sectors = self.get_sector_breakdown()
        for sector, data in sectors.items():
            if data["exceeds_guardrail"]:
                recommendations.append({
                    "type": "sector_rebalance",
                    "sector": sector,
                    "current_weight": data["weight"],
                    "target_weight": self.guardrails.max_sector_weight,
                    "action": f"Reduce {sector} exposure from {data['weight']:.1%} to {self.guardrails.max_sector_weight:.0%}",
                })
        
        # Check tactical allocation
        tactical_weight = self.get_tactical_value() / total
        if tactical_weight > self.guardrails.tactical_max_allocation * 1.1:
            recommendations.append({
                "type": "tactical_trim",
                "current_weight": tactical_weight,
                "target_weight": self.guardrails.tactical_max_allocation,
                "action": f"Reduce tactical from {tactical_weight:.1%} to {self.guardrails.tactical_max_allocation:.0%}",
            })
        
        return recommendations
    
    # ==================== Reporting ====================
    
    def get_portfolio_summary(self) -> Dict[str, Any]:
        """Get complete portfolio summary"""
        return {
            "timestamp": datetime.now().isoformat(),
            "total_value": self.get_total_value(),
            "allocation": self.get_allocation_breakdown(),
            "sectors": self.get_sector_breakdown(),
            "income": {
                "expected_annual": self.get_expected_annual_income(),
                "portfolio_yield": self.get_portfolio_yield(),
            },
            "performance": {
                "peak_value": self.peak_value,
                "current_drawdown": self.current_drawdown,
                "in_drawdown_mode": self.is_in_drawdown_mode(),
            },
            "positions": {
                "core": [p.to_dict() for p in self.core_positions],
                "tactical": [p.to_dict() for p in self.tactical_positions],
            },
            "rebalancing_recommendations": self.get_rebalancing_recommendations(),
        }

"""
SwarmGate Router
================

The autonomous AI flow router for the 7% allocation.
Routes funds to optimal destinations based on configuration and market conditions.

Destinations:
    A) Short-term treasuries - Safe haven
    B) Crypto reserve - Speculative allocation
    C) AI-fuel account - Fund AI operations
    D) Mixed - Diversified across destinations
    E) Auto-optimal - AI decides optimal routing
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any, Optional
from enum import Enum
import structlog

from .config import HybridRefineryConfig, SwarmGateDestination

logger = structlog.get_logger()


class RoutingStrategy(Enum):
    """Routing strategy types"""
    FIXED = "fixed"  # Fixed allocation to single destination
    MIXED = "mixed"  # Split across multiple destinations
    DYNAMIC = "dynamic"  # AI-driven dynamic allocation


# Default allocation percentages for AUTO_OPTIMAL strategy
# These can be overridden via configuration
DEFAULT_AUTO_OPTIMAL_ALLOCATIONS = {
    "treasuries": 0.40,  # 40% to short-term treasuries for safety
    "crypto": 0.25,      # 25% to crypto for asymmetric upside
    "ai_fuel": 0.35,     # 35% to AI-fuel for operations
}


@dataclass
class FlowDestination:
    """A single flow destination"""
    name: str
    destination_type: SwarmGateDestination
    allocation_pct: float = 0.0
    current_balance: float = 0.0
    
    # Destination-specific config
    account_id: Optional[str] = None
    api_endpoint: Optional[str] = None
    
    # Performance tracking
    inception_date: datetime = field(default_factory=datetime.now)
    total_deposited: float = 0.0
    total_withdrawn: float = 0.0
    realized_returns: float = 0.0
    
    @property
    def net_flow(self) -> float:
        """Net capital flow into destination"""
        return self.total_deposited - self.total_withdrawn
    
    @property
    def total_return_pct(self) -> float:
        """Total return percentage"""
        if self.net_flow > 0:
            return self.realized_returns / self.net_flow
        return 0.0
    
    def deposit(self, amount: float) -> bool:
        """Record a deposit to this destination"""
        self.current_balance += amount
        self.total_deposited += amount
        
        logger.info("SwarmGate deposit",
                   destination=self.name,
                   amount=amount,
                   new_balance=self.current_balance)
        return True
    
    def withdraw(self, amount: float) -> bool:
        """Record a withdrawal from this destination"""
        if amount > self.current_balance:
            logger.warning("Insufficient balance for withdrawal",
                         destination=self.name,
                         requested=amount,
                         available=self.current_balance)
            return False
        
        self.current_balance -= amount
        self.total_withdrawn += amount
        
        logger.info("SwarmGate withdrawal",
                   destination=self.name,
                   amount=amount,
                   new_balance=self.current_balance)
        return True
    
    def record_returns(self, returns: float):
        """Record realized returns"""
        self.realized_returns += returns
        self.current_balance += returns
        
        logger.info("SwarmGate returns recorded",
                   destination=self.name,
                   returns=returns,
                   total_returns=self.realized_returns)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "name": self.name,
            "destination_type": self.destination_type.value,
            "allocation_pct": self.allocation_pct,
            "current_balance": self.current_balance,
            "total_deposited": self.total_deposited,
            "total_withdrawn": self.total_withdrawn,
            "net_flow": self.net_flow,
            "realized_returns": self.realized_returns,
            "total_return_pct": self.total_return_pct,
            "inception_date": self.inception_date.isoformat(),
        }


@dataclass 
class RoutingDecision:
    """A routing decision made by SwarmGate"""
    timestamp: datetime
    total_amount: float
    strategy: RoutingStrategy
    allocations: Dict[str, float]  # destination_name -> amount
    reasoning: str
    confidence: float = 1.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "timestamp": self.timestamp.isoformat(),
            "total_amount": self.total_amount,
            "strategy": self.strategy.value,
            "allocations": self.allocations,
            "reasoning": self.reasoning,
            "confidence": self.confidence,
        }


class SwarmGateRouter:
    """
    SwarmGate - Autonomous AI Flow Router
    
    Routes 7% of dividend income to optimal destinations.
    
    Options:
        A) Short-term treasuries - Safety
        B) Crypto reserve - Asymmetric upside
        C) AI-fuel account - Fund operations
        D) Mixed - Diversified
        E) Auto-optimal - AI decides
    """
    
    def __init__(self, config: HybridRefineryConfig):
        self.config = config
        self.destination_choice = config.swarmgate_destination
        
        # Initialize destinations
        self.destinations: Dict[str, FlowDestination] = {}
        self._initialize_destinations()
        
        # Routing history
        self.routing_history: List[RoutingDecision] = []
        
        # Mixed allocation weights (for MIXED strategy)
        self.mixed_weights = {
            SwarmGateDestination.SHORT_TERM_TREASURIES: 0.50,
            SwarmGateDestination.CRYPTO_RESERVE: 0.20,
            SwarmGateDestination.AI_FUEL_ACCOUNT: 0.30,
        }
        
        logger.info("SwarmGate Router initialized",
                   destination=self.destination_choice.value)
    
    def _initialize_destinations(self):
        """Initialize flow destinations"""
        self.destinations = {
            "treasuries": FlowDestination(
                name="Short-Term Treasuries",
                destination_type=SwarmGateDestination.SHORT_TERM_TREASURIES,
                allocation_pct=0.0,
            ),
            "crypto": FlowDestination(
                name="Crypto Reserve",
                destination_type=SwarmGateDestination.CRYPTO_RESERVE,
                allocation_pct=0.0,
            ),
            "ai_fuel": FlowDestination(
                name="AI-Fuel Account",
                destination_type=SwarmGateDestination.AI_FUEL_ACCOUNT,
                allocation_pct=0.0,
            ),
        }
        
        # Set allocations based on destination choice
        self._set_allocations()
    
    def _set_allocations(self):
        """Set allocation percentages based on destination choice"""
        # Reset all allocations
        for dest in self.destinations.values():
            dest.allocation_pct = 0.0
        
        if self.destination_choice == SwarmGateDestination.SHORT_TERM_TREASURIES:
            self.destinations["treasuries"].allocation_pct = 1.0
            
        elif self.destination_choice == SwarmGateDestination.CRYPTO_RESERVE:
            self.destinations["crypto"].allocation_pct = 1.0
            
        elif self.destination_choice == SwarmGateDestination.AI_FUEL_ACCOUNT:
            self.destinations["ai_fuel"].allocation_pct = 1.0
            
        elif self.destination_choice == SwarmGateDestination.MIXED:
            for key, weight in [("treasuries", 0.50), ("crypto", 0.20), ("ai_fuel", 0.30)]:
                self.destinations[key].allocation_pct = weight
                
        elif self.destination_choice == SwarmGateDestination.AUTO_OPTIMAL:
            # Default to balanced until AI decides
            for key, weight in [("treasuries", 0.40), ("crypto", 0.25), ("ai_fuel", 0.35)]:
                self.destinations[key].allocation_pct = weight
    
    def route_flow(self, amount: float) -> RoutingDecision:
        """
        Route incoming flow to destinations
        
        Args:
            amount: Total amount to route
            
        Returns:
            RoutingDecision with allocations
        """
        if self.destination_choice == SwarmGateDestination.AUTO_OPTIMAL:
            decision = self._make_optimal_decision(amount)
        else:
            decision = self._make_fixed_decision(amount)
        
        # Execute the routing
        self._execute_routing(decision)
        
        # Record in history
        self.routing_history.append(decision)
        
        logger.info("Flow routed",
                   amount=amount,
                   strategy=decision.strategy.value,
                   allocations=decision.allocations)
        
        return decision
    
    def _make_fixed_decision(self, amount: float) -> RoutingDecision:
        """Make routing decision based on fixed allocation"""
        allocations = {}
        
        for key, dest in self.destinations.items():
            if dest.allocation_pct > 0:
                allocations[dest.name] = amount * dest.allocation_pct
        
        strategy = RoutingStrategy.MIXED if len(allocations) > 1 else RoutingStrategy.FIXED
        
        return RoutingDecision(
            timestamp=datetime.now(),
            total_amount=amount,
            strategy=strategy,
            allocations=allocations,
            reasoning=f"Fixed allocation to {self.destination_choice.value}",
            confidence=1.0,
        )
    
    def _make_optimal_decision(self, amount: float) -> RoutingDecision:
        """
        Make AI-driven optimal routing decision
        
        Considers:
            - Market conditions
            - Risk environment
            - Opportunity costs
            - Portfolio needs
        """
        # Placeholder for AI decision logic
        # In production, this would use ML models and market data
        
        allocations = {}
        reasoning_parts = []
        
        # Use configurable default allocations from constants
        # - High uncertainty -> More treasuries
        # - Crypto momentum -> More crypto
        # - Need for operations -> More AI fuel
        
        # Apply default balanced allocation from configuration constants
        treasuries_pct = DEFAULT_AUTO_OPTIMAL_ALLOCATIONS["treasuries"]
        crypto_pct = DEFAULT_AUTO_OPTIMAL_ALLOCATIONS["crypto"]
        ai_fuel_pct = DEFAULT_AUTO_OPTIMAL_ALLOCATIONS["ai_fuel"]
        
        allocations["Short-Term Treasuries"] = amount * treasuries_pct
        allocations["Crypto Reserve"] = amount * crypto_pct
        allocations["AI-Fuel Account"] = amount * ai_fuel_pct
        
        reasoning_parts.append("Balanced allocation across destinations")
        reasoning_parts.append(f"{treasuries_pct:.0%} treasuries for safety")
        reasoning_parts.append(f"{crypto_pct:.0%} crypto for asymmetric upside")
        reasoning_parts.append(f"{ai_fuel_pct:.0%} AI-fuel for operations")
        
        return RoutingDecision(
            timestamp=datetime.now(),
            total_amount=amount,
            strategy=RoutingStrategy.DYNAMIC,
            allocations=allocations,
            reasoning=" | ".join(reasoning_parts),
            confidence=0.85,  # AI confidence score
        )
    
    def _execute_routing(self, decision: RoutingDecision):
        """Execute the routing decision"""
        for dest_name, amount in decision.allocations.items():
            # Find destination by name
            for dest in self.destinations.values():
                if dest.name == dest_name:
                    dest.deposit(amount)
                    break
    
    def get_total_balance(self) -> float:
        """Get total balance across all destinations"""
        return sum(d.current_balance for d in self.destinations.values())
    
    def get_destination_summary(self) -> Dict[str, Any]:
        """Get summary of all destinations"""
        total_balance = self.get_total_balance()
        
        return {
            "total_balance": total_balance,
            "destinations": [d.to_dict() for d in self.destinations.values()],
            "routing_strategy": self.destination_choice.value,
            "recent_routings": [r.to_dict() for r in self.routing_history[-10:]],
        }
    
    def get_routing_log(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent routing log"""
        return [r.to_dict() for r in self.routing_history[-limit:]]
    
    def set_destination(self, destination: SwarmGateDestination):
        """Change the destination routing"""
        self.destination_choice = destination
        self._set_allocations()
        
        logger.info("SwarmGate destination changed",
                   new_destination=destination.value)
    
    def set_mixed_weights(self, weights: Dict[SwarmGateDestination, float]):
        """
        Set custom mixed allocation weights
        
        Args:
            weights: Dictionary of destination -> weight (must sum to 1.0)
        """
        total = sum(weights.values())
        if abs(total - 1.0) > 0.001:
            raise ValueError(f"Weights must sum to 1.0, got {total}")
        
        self.mixed_weights = weights
        
        # Update destination allocations if currently in mixed mode
        if self.destination_choice == SwarmGateDestination.MIXED:
            for dest in self.destinations.values():
                dest.allocation_pct = weights.get(dest.destination_type, 0.0)
        
        logger.info("Mixed weights updated", weights=weights)
    
    def rebalance_destinations(self) -> Dict[str, float]:
        """
        Rebalance destinations to target allocations
        
        Returns:
            Dictionary of transfers needed
        """
        total = self.get_total_balance()
        if total <= 0:
            return {}
        
        transfers = {}
        
        for dest in self.destinations.values():
            target_balance = total * dest.allocation_pct
            current_balance = dest.current_balance
            diff = target_balance - current_balance
            
            if abs(diff) > 0.01 * total:  # Only rebalance if >1% drift
                transfers[dest.name] = diff
        
        logger.info("Rebalancing recommended", transfers=transfers)
        return transfers
    
    def withdraw_from_destination(
        self, 
        destination_key: str, 
        amount: float,
        reason: str = "portfolio_need"
    ) -> bool:
        """
        Withdraw funds from a destination
        
        Args:
            destination_key: Key of destination (treasuries, crypto, ai_fuel)
            amount: Amount to withdraw
            reason: Reason for withdrawal
        """
        if destination_key not in self.destinations:
            logger.error("Unknown destination", key=destination_key)
            return False
        
        dest = self.destinations[destination_key]
        success = dest.withdraw(amount)
        
        if success:
            logger.info("SwarmGate withdrawal completed",
                       destination=dest.name,
                       amount=amount,
                       reason=reason)
        
        return success
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Get performance report for SwarmGate"""
        total_deposited = sum(d.total_deposited for d in self.destinations.values())
        total_returns = sum(d.realized_returns for d in self.destinations.values())
        current_balance = self.get_total_balance()
        
        return {
            "total_deposited": total_deposited,
            "total_returns": total_returns,
            "current_balance": current_balance,
            "overall_return_pct": total_returns / total_deposited if total_deposited > 0 else 0,
            "by_destination": {
                key: {
                    "deposited": d.total_deposited,
                    "returns": d.realized_returns,
                    "balance": d.current_balance,
                    "return_pct": d.total_return_pct,
                }
                for key, d in self.destinations.items()
            },
            "routing_count": len(self.routing_history),
        }

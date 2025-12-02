"""
DiviDen Ninja Bot - HLMCR Governance Module
High-Leverage Multi-Currency Refinery governance framework
"""

import asyncio
import hashlib
import json
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, Any, List, Optional, Callable

import structlog

logger = structlog.get_logger()


class DecisionType(Enum):
    """Types of governance decisions"""
    TRADE_ENTRY = "trade_entry"
    TRADE_EXIT = "trade_exit"
    POSITION_INCREASE = "position_increase"
    POSITION_DECREASE = "position_decrease"
    RISK_OVERRIDE = "risk_override"
    EMERGENCY_STOP = "emergency_stop"
    CONFIG_CHANGE = "config_change"
    DONATION_ALLOCATION = "donation_allocation"


class ApprovalLevel(Enum):
    """Approval levels for governance decisions"""
    AUTO = "auto"           # Automated approval
    REVIEW = "review"       # Requires review (async)
    MANUAL = "manual"       # Requires human approval
    EMERGENCY = "emergency" # Emergency override


@dataclass
class GovernanceDecision:
    """Represents a governance decision"""
    decision_id: str
    decision_type: DecisionType
    approval_level: ApprovalLevel
    approved: bool
    reason: str
    context: Dict[str, Any]
    
    # Audit trail
    requested_at: datetime
    decided_at: datetime
    decided_by: str  # "auto", "review", or human identifier
    
    # Verification
    context_hash: str = ""
    signature: str = ""
    
    def __post_init__(self):
        if not self.context_hash:
            self.context_hash = self._hash_context()
    
    def _hash_context(self) -> str:
        """Create hash of decision context for audit trail"""
        context_json = json.dumps(self.context, sort_keys=True, default=str)
        return hashlib.sha256(context_json.encode()).hexdigest()


@dataclass
class GovernanceConfig:
    """HLMCR Governance configuration"""
    enabled: bool = True
    
    # Approval thresholds
    auto_approve_below: float = 1000.0
    human_review_above: float = 10000.0
    
    # Audit settings
    log_all_decisions: bool = True
    decision_retention_days: int = 2555  # ~7 years (IRS record retention requirement)
    
    # Emergency controls
    kill_switch_enabled: bool = True
    max_consecutive_losses: int = 5


@dataclass
class GovernanceState:
    """Current state of the governance system"""
    is_active: bool = True
    kill_switch_triggered: bool = False
    consecutive_losses: int = 0
    pending_reviews: List[str] = field(default_factory=list)
    daily_approved_value: float = 0.0
    last_decision: Optional[datetime] = None


class GovernanceRule:
    """Base class for governance rules"""
    
    def __init__(self, name: str, priority: int = 100):
        self.name = name
        self.priority = priority
        self.enabled = True
    
    def evaluate(
        self, 
        decision_type: DecisionType, 
        context: Dict[str, Any],
        state: GovernanceState
    ) -> Optional[Dict[str, Any]]:
        """
        Evaluate if this rule applies to the decision.
        Returns None if rule doesn't apply, otherwise returns:
        {
            "approved": bool,
            "level": ApprovalLevel,
            "reason": str,
        }
        """
        raise NotImplementedError


class ValueThresholdRule(GovernanceRule):
    """Rule based on trade value thresholds"""
    
    def __init__(self, config: GovernanceConfig):
        super().__init__("value_threshold", priority=10)
        self.config = config
    
    def evaluate(
        self, 
        decision_type: DecisionType,
        context: Dict[str, Any],
        state: GovernanceState
    ) -> Optional[Dict[str, Any]]:
        if decision_type not in [DecisionType.TRADE_ENTRY, DecisionType.POSITION_INCREASE]:
            return None
        
        trade_value = context.get("shares", 0) * context.get("price", 0)
        
        if trade_value <= self.config.auto_approve_below:
            return {
                "approved": True,
                "level": ApprovalLevel.AUTO,
                "reason": f"Trade value ${trade_value:.2f} below auto-approve threshold",
            }
        
        if trade_value >= self.config.human_review_above:
            return {
                "approved": False,
                "level": ApprovalLevel.MANUAL,
                "reason": f"Trade value ${trade_value:.2f} requires human approval",
            }
        
        return {
            "approved": True,
            "level": ApprovalLevel.REVIEW,
            "reason": f"Trade value ${trade_value:.2f} approved with review",
        }


class RiskScoreRule(GovernanceRule):
    """Rule based on risk assessment"""
    
    def __init__(self, max_risk: float = 0.7):
        super().__init__("risk_score", priority=20)
        self.max_risk = max_risk
    
    def evaluate(
        self,
        decision_type: DecisionType,
        context: Dict[str, Any],
        state: GovernanceState
    ) -> Optional[Dict[str, Any]]:
        if decision_type not in [DecisionType.TRADE_ENTRY, DecisionType.POSITION_INCREASE]:
            return None
        
        risk_score = context.get("risk_score", 0.5)
        
        if risk_score > self.max_risk:
            return {
                "approved": False,
                "level": ApprovalLevel.AUTO,
                "reason": f"Risk score {risk_score:.2f} exceeds maximum {self.max_risk:.2f}",
            }
        
        return None  # Allow other rules to decide


class ConsecutiveLossRule(GovernanceRule):
    """Rule to prevent trading after consecutive losses"""
    
    def __init__(self, config: GovernanceConfig):
        super().__init__("consecutive_loss", priority=5)
        self.config = config
    
    def evaluate(
        self,
        decision_type: DecisionType,
        context: Dict[str, Any],
        state: GovernanceState
    ) -> Optional[Dict[str, Any]]:
        if decision_type not in [DecisionType.TRADE_ENTRY, DecisionType.POSITION_INCREASE]:
            return None
        
        if state.consecutive_losses >= self.config.max_consecutive_losses:
            return {
                "approved": False,
                "level": ApprovalLevel.MANUAL,
                "reason": f"Trading paused after {state.consecutive_losses} consecutive losses",
            }
        
        return None


class KillSwitchRule(GovernanceRule):
    """Emergency kill switch rule"""
    
    def __init__(self, config: GovernanceConfig):
        super().__init__("kill_switch", priority=1)  # Highest priority
        self.config = config
    
    def evaluate(
        self,
        decision_type: DecisionType,
        context: Dict[str, Any],
        state: GovernanceState
    ) -> Optional[Dict[str, Any]]:
        if not self.config.kill_switch_enabled:
            return None
        
        if state.kill_switch_triggered:
            return {
                "approved": False,
                "level": ApprovalLevel.EMERGENCY,
                "reason": "Kill switch is active - all trading halted",
            }
        
        return None


class NonprofitComplianceRule(GovernanceRule):
    """Rule ensuring nonprofit compliance requirements"""
    
    def __init__(self, donation_percentage: float = 0.07):
        super().__init__("nonprofit_compliance", priority=15)
        self.donation_percentage = donation_percentage
    
    def evaluate(
        self,
        decision_type: DecisionType,
        context: Dict[str, Any],
        state: GovernanceState
    ) -> Optional[Dict[str, Any]]:
        if decision_type != DecisionType.DONATION_ALLOCATION:
            return None
        
        allocation_pct = context.get("allocation_percentage", 0)
        
        if allocation_pct < self.donation_percentage:
            return {
                "approved": False,
                "level": ApprovalLevel.AUTO,
                "reason": f"Donation allocation {allocation_pct:.1%} below required {self.donation_percentage:.1%}",
            }
        
        return {
            "approved": True,
            "level": ApprovalLevel.AUTO,
            "reason": f"Donation allocation {allocation_pct:.1%} meets compliance requirements",
        }


class HLMCRGovernor:
    """
    High-Leverage Multi-Currency Refinery Governor
    
    Implements rules-based governance for automated trading decisions.
    Ensures compliance with risk parameters, nonprofit requirements,
    and maintains full audit trail.
    """
    
    def __init__(self, config: GovernanceConfig = None):
        self.config = config or GovernanceConfig()
        self.state = GovernanceState()
        self.rules: List[GovernanceRule] = []
        self.decisions: List[GovernanceDecision] = []
        self.callbacks: Dict[str, List[Callable]] = {}
        
        # Initialize default rules
        self._init_default_rules()
        
        logger.info("HLMCR Governor initialized", enabled=self.config.enabled)
    
    def _init_default_rules(self) -> None:
        """Initialize default governance rules"""
        self.rules = [
            KillSwitchRule(self.config),
            ConsecutiveLossRule(self.config),
            ValueThresholdRule(self.config),
            RiskScoreRule(max_risk=0.7),
            NonprofitComplianceRule(donation_percentage=0.07),
        ]
        # Sort by priority (lower = higher priority)
        self.rules.sort(key=lambda r: r.priority)
    
    def add_rule(self, rule: GovernanceRule) -> None:
        """Add a governance rule"""
        self.rules.append(rule)
        self.rules.sort(key=lambda r: r.priority)
        logger.info(f"Added governance rule: {rule.name}")
    
    def remove_rule(self, rule_name: str) -> bool:
        """Remove a governance rule by name"""
        for i, rule in enumerate(self.rules):
            if rule.name == rule_name:
                del self.rules[i]
                logger.info(f"Removed governance rule: {rule_name}")
                return True
        return False
    
    async def request_approval(
        self,
        decision_type: DecisionType,
        context: Dict[str, Any]
    ) -> GovernanceDecision:
        """Request approval for a governance decision"""
        if not self.config.enabled:
            # If governance disabled, auto-approve everything
            return self._create_decision(
                decision_type=decision_type,
                context=context,
                approved=True,
                level=ApprovalLevel.AUTO,
                reason="Governance disabled - auto-approved",
                decided_by="system",
            )
        
        requested_at = datetime.now(timezone.utc)
        
        # Evaluate rules in priority order
        for rule in self.rules:
            if not rule.enabled:
                continue
            
            result = rule.evaluate(decision_type, context, self.state)
            
            if result is not None:
                # Rule returned a decision
                decision = self._create_decision(
                    decision_type=decision_type,
                    context=context,
                    approved=result["approved"],
                    level=result["level"],
                    reason=f"[{rule.name}] {result['reason']}",
                    decided_by=rule.name,
                    requested_at=requested_at,
                )
                
                # Handle different approval levels
                if result["level"] == ApprovalLevel.MANUAL:
                    # Queue for manual review
                    await self._queue_for_review(decision)
                
                # Log and store decision
                await self._record_decision(decision)
                
                return decision
        
        # No rule matched - default to review approval
        decision = self._create_decision(
            decision_type=decision_type,
            context=context,
            approved=True,
            level=ApprovalLevel.REVIEW,
            reason="No rule matched - approved with review",
            decided_by="default",
            requested_at=requested_at,
        )
        
        await self._record_decision(decision)
        return decision
    
    def _create_decision(
        self,
        decision_type: DecisionType,
        context: Dict[str, Any],
        approved: bool,
        level: ApprovalLevel,
        reason: str,
        decided_by: str,
        requested_at: datetime = None,
    ) -> GovernanceDecision:
        """Create a governance decision object"""
        now = datetime.now(timezone.utc)
        
        return GovernanceDecision(
            decision_id=str(uuid.uuid4()),
            decision_type=decision_type,
            approval_level=level,
            approved=approved,
            reason=reason,
            context=context,
            requested_at=requested_at or now,
            decided_at=now,
            decided_by=decided_by,
        )
    
    async def _record_decision(self, decision: GovernanceDecision) -> None:
        """Record decision for audit trail"""
        self.decisions.append(decision)
        self.state.last_decision = decision.decided_at
        
        if self.config.log_all_decisions:
            logger.info(
                "Governance decision",
                decision_id=decision.decision_id,
                type=decision.decision_type.value,
                approved=decision.approved,
                level=decision.approval_level.value,
                reason=decision.reason,
            )
        
        # Trigger callbacks
        await self._trigger_callbacks("decision_made", decision)
    
    async def _queue_for_review(self, decision: GovernanceDecision) -> None:
        """Queue decision for manual review"""
        self.state.pending_reviews.append(decision.decision_id)
        logger.info(
            "Decision queued for review",
            decision_id=decision.decision_id,
            pending_count=len(self.state.pending_reviews),
        )
        
        # Trigger callbacks
        await self._trigger_callbacks("review_required", decision)
    
    async def approve_pending(
        self, 
        decision_id: str, 
        approved_by: str
    ) -> bool:
        """Manually approve a pending decision"""
        if decision_id not in self.state.pending_reviews:
            return False
        
        self.state.pending_reviews.remove(decision_id)
        
        # Find and update decision
        for decision in self.decisions:
            if decision.decision_id == decision_id:
                decision.approved = True
                decision.decided_by = approved_by
                decision.decided_at = datetime.now(timezone.utc)
                
                logger.info(
                    "Decision manually approved",
                    decision_id=decision_id,
                    approved_by=approved_by,
                )
                return True
        
        return False
    
    async def reject_pending(
        self, 
        decision_id: str, 
        rejected_by: str,
        reason: str
    ) -> bool:
        """Manually reject a pending decision"""
        if decision_id not in self.state.pending_reviews:
            return False
        
        self.state.pending_reviews.remove(decision_id)
        
        for decision in self.decisions:
            if decision.decision_id == decision_id:
                decision.approved = False
                decision.decided_by = rejected_by
                decision.decided_at = datetime.now(timezone.utc)
                decision.reason = f"[manual_reject] {reason}"
                
                logger.info(
                    "Decision manually rejected",
                    decision_id=decision_id,
                    rejected_by=rejected_by,
                    reason=reason,
                )
                return True
        
        return False
    
    def trigger_kill_switch(self, reason: str) -> None:
        """Trigger emergency kill switch"""
        self.state.kill_switch_triggered = True
        self.state.is_active = False
        
        logger.critical(
            "KILL SWITCH TRIGGERED",
            reason=reason,
        )
    
    def reset_kill_switch(self, authorized_by: str) -> None:
        """Reset kill switch (requires authorization)"""
        self.state.kill_switch_triggered = False
        self.state.is_active = True
        self.state.consecutive_losses = 0
        
        logger.warning(
            "Kill switch reset",
            authorized_by=authorized_by,
        )
    
    def record_trade_result(self, profitable: bool) -> None:
        """Record trade result for consecutive loss tracking"""
        if profitable:
            self.state.consecutive_losses = 0
        else:
            self.state.consecutive_losses += 1
            
            if self.state.consecutive_losses >= self.config.max_consecutive_losses:
                logger.warning(
                    "Max consecutive losses reached",
                    losses=self.state.consecutive_losses,
                )
    
    def register_callback(self, event: str, callback: Callable) -> None:
        """Register callback for governance events"""
        if event not in self.callbacks:
            self.callbacks[event] = []
        self.callbacks[event].append(callback)
    
    async def _trigger_callbacks(self, event: str, data: Any) -> None:
        """Trigger callbacks for an event"""
        callbacks = self.callbacks.get(event, [])
        for callback in callbacks:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(data)
                else:
                    callback(data)
            except Exception as e:
                logger.error(f"Callback error for {event}: {e}")
    
    def get_state(self) -> Dict[str, Any]:
        """Get current governance state"""
        return {
            "is_active": self.state.is_active,
            "kill_switch_triggered": self.state.kill_switch_triggered,
            "consecutive_losses": self.state.consecutive_losses,
            "pending_reviews_count": len(self.state.pending_reviews),
            "daily_approved_value": self.state.daily_approved_value,
            "last_decision": self.state.last_decision.isoformat() if self.state.last_decision else None,
            "total_decisions": len(self.decisions),
            "rules_count": len(self.rules),
        }
    
    def get_audit_trail(
        self, 
        start_date: datetime = None,
        end_date: datetime = None,
        decision_type: DecisionType = None,
        approved_only: bool = False
    ) -> List[Dict[str, Any]]:
        """Get audit trail of governance decisions"""
        filtered = []
        
        for decision in self.decisions:
            # Apply filters
            if start_date and decision.decided_at < start_date:
                continue
            if end_date and decision.decided_at > end_date:
                continue
            if decision_type and decision.decision_type != decision_type:
                continue
            if approved_only and not decision.approved:
                continue
            
            filtered.append(asdict(decision))
        
        return filtered

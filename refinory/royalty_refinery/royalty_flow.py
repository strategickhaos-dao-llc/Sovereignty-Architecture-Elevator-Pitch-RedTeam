"""
DiviDen Refinery - Royalty Flow Management
Handles royalty stream processing, distribution, and audit trails
"""

import asyncio
import hashlib
import json
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone, timedelta
from decimal import Decimal
from typing import Dict, Any, List, Optional
from enum import Enum

import structlog

from .config import (
    RoyaltyRefineryConfig, 
    RoyaltyType, 
    PaymentFrequency,
    DistributionPriority,
    get_royalty_config,
)

logger = structlog.get_logger()


class StreamStatus(Enum):
    """Status of a royalty stream"""
    PENDING = "pending"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    COMPLETED = "completed"
    DISPUTED = "disputed"


class PaymentStatus(Enum):
    """Status of a royalty payment"""
    RECEIVED = "received"
    PROCESSING = "processing"
    DISTRIBUTED = "distributed"
    HELD = "held"
    REFUNDED = "refunded"


@dataclass
class RoyaltySource:
    """Represents a source of royalty payments"""
    source_id: str
    name: str
    source_type: RoyaltyType
    
    # Legal/case reference
    case_reference: Optional[str] = None
    settlement_date: Optional[datetime] = None
    judgment_date: Optional[datetime] = None
    
    # Payment terms
    total_amount: Decimal = Decimal("0")
    paid_to_date: Decimal = Decimal("0")
    payment_frequency: PaymentFrequency = PaymentFrequency.ONE_TIME
    next_payment_date: Optional[datetime] = None
    
    # Source details
    payer_name: str = ""
    payer_contact: str = ""
    
    # Status
    status: StreamStatus = StreamStatus.PENDING
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    
    def remaining_balance(self) -> Decimal:
        """Calculate remaining balance"""
        return self.total_amount - self.paid_to_date


@dataclass
class RoyaltyPayment:
    """Represents a single royalty payment received"""
    payment_id: str
    source_id: str
    amount: Decimal
    received_at: datetime
    
    # Payment details
    payment_method: str = "wire"
    reference_number: str = ""
    
    # Processing
    status: PaymentStatus = PaymentStatus.RECEIVED
    processed_at: Optional[datetime] = None
    
    # Verification
    receipt_hash: str = ""
    verified: bool = False


@dataclass
class Distribution:
    """Represents a distribution from the refinery"""
    distribution_id: str
    payment_id: str
    recipient_type: DistributionPriority
    recipient_name: str
    amount: Decimal
    
    # Processing
    status: str = "pending"
    distributed_at: Optional[datetime] = None
    
    # Tax reporting
    tax_reportable: bool = True
    form_1099_required: bool = False
    
    # Verification
    transaction_hash: str = ""


@dataclass
class AuditEntry:
    """Audit trail entry"""
    entry_id: str
    timestamp: datetime
    action: str
    entity_type: str  # source, payment, distribution
    entity_id: str
    details: Dict[str, Any]
    actor: str
    
    # Verification
    entry_hash: str = ""
    previous_hash: str = ""


class RoyaltyStream:
    """
    Manages a royalty stream from source to distribution.
    Handles tracking, processing, and compliance.
    """
    
    def __init__(self, source: RoyaltySource, config: RoyaltyRefineryConfig = None):
        self.source = source
        self.config = config or get_royalty_config()
        self.payments: List[RoyaltyPayment] = []
        self.distributions: List[Distribution] = []
        
        logger.info(
            "Royalty stream initialized",
            source_id=source.source_id,
            source_type=source.source_type.value,
        )
    
    async def record_payment(
        self, 
        amount: Decimal,
        payment_method: str = "wire",
        reference_number: str = ""
    ) -> RoyaltyPayment:
        """Record a received payment"""
        payment = RoyaltyPayment(
            payment_id=str(uuid.uuid4()),
            source_id=self.source.source_id,
            amount=amount,
            received_at=datetime.now(timezone.utc),
            payment_method=payment_method,
            reference_number=reference_number,
            status=PaymentStatus.RECEIVED,
        )
        
        # Generate receipt hash
        payment.receipt_hash = self._hash_payment(payment)
        
        self.payments.append(payment)
        self.source.paid_to_date += amount
        
        logger.info(
            "Payment recorded",
            payment_id=payment.payment_id,
            source_id=self.source.source_id,
            amount=str(amount),
        )
        
        return payment
    
    async def process_payment(self, payment_id: str) -> List[Distribution]:
        """Process a payment and create distributions"""
        payment = self._get_payment(payment_id)
        if not payment:
            raise ValueError(f"Payment {payment_id} not found")
        
        if payment.status != PaymentStatus.RECEIVED:
            raise ValueError(f"Payment {payment_id} already processed")
        
        payment.status = PaymentStatus.PROCESSING
        distributions = []
        
        # Calculate distributions based on configuration
        dist_config = self.config.distribution
        amount = payment.amount
        
        # 1. Charity allocation (7% minimum)
        charity_amount = amount * Decimal(str(dist_config.charity_allocation_pct))
        charity_dist = await self._create_charity_distributions(
            payment_id, charity_amount
        )
        distributions.extend(charity_dist)
        
        # 2. Victim fund allocation
        victim_amount = amount * Decimal(str(dist_config.victim_fund_pct))
        victim_dist = Distribution(
            distribution_id=str(uuid.uuid4()),
            payment_id=payment_id,
            recipient_type=DistributionPriority.VICTIM_FUND,
            recipient_name="Victim Compensation Fund",
            amount=victim_amount,
        )
        distributions.append(victim_dist)
        
        # 3. Operational reserve
        ops_amount = amount * Decimal(str(dist_config.operational_pct))
        ops_dist = Distribution(
            distribution_id=str(uuid.uuid4()),
            payment_id=payment_id,
            recipient_type=DistributionPriority.OPERATIONAL,
            recipient_name="Operational Reserve",
            amount=ops_amount,
            tax_reportable=False,
        )
        distributions.append(ops_dist)
        
        # 4. DAO member distribution
        dao_amount = amount * Decimal(str(dist_config.dao_distribution_pct))
        dao_dist = Distribution(
            distribution_id=str(uuid.uuid4()),
            payment_id=payment_id,
            recipient_type=DistributionPriority.DAO_MEMBERS,
            recipient_name="DAO Token Holders",
            amount=dao_amount,
        )
        distributions.append(dao_dist)
        
        # 5. Emergency reserve
        reserve_amount = amount * Decimal(str(dist_config.reserve_pct))
        reserve_dist = Distribution(
            distribution_id=str(uuid.uuid4()),
            payment_id=payment_id,
            recipient_type=DistributionPriority.RESERVE,
            recipient_name="Emergency Reserve",
            amount=reserve_amount,
            tax_reportable=False,
        )
        distributions.append(reserve_dist)
        
        # Store distributions
        self.distributions.extend(distributions)
        
        # Update payment status
        payment.status = PaymentStatus.DISTRIBUTED
        payment.processed_at = datetime.now(timezone.utc)
        
        logger.info(
            "Payment processed",
            payment_id=payment_id,
            distributions_count=len(distributions),
            total_distributed=str(amount),
        )
        
        return distributions
    
    async def _create_charity_distributions(
        self, 
        payment_id: str, 
        total_amount: Decimal
    ) -> List[Distribution]:
        """Create distributions for verified charities"""
        distributions = []
        
        for charity in self.config.distribution.verified_charities:
            charity_share = total_amount * Decimal(str(charity.allocation_pct))
            
            dist = Distribution(
                distribution_id=str(uuid.uuid4()),
                payment_id=payment_id,
                recipient_type=DistributionPriority.CHARITY,
                recipient_name=charity.name,
                amount=charity_share,
                tax_reportable=True,
            )
            distributions.append(dist)
        
        return distributions
    
    def _get_payment(self, payment_id: str) -> Optional[RoyaltyPayment]:
        """Get payment by ID"""
        for payment in self.payments:
            if payment.payment_id == payment_id:
                return payment
        return None
    
    def _hash_payment(self, payment: RoyaltyPayment) -> str:
        """Create hash of payment for verification"""
        data = {
            "payment_id": payment.payment_id,
            "source_id": payment.source_id,
            "amount": str(payment.amount),
            "received_at": payment.received_at.isoformat(),
            "reference_number": payment.reference_number,
        }
        json_str = json.dumps(data, sort_keys=True)
        return hashlib.sha256(json_str.encode()).hexdigest()
    
    def get_summary(self) -> Dict[str, Any]:
        """Get stream summary"""
        return {
            "source_id": self.source.source_id,
            "source_type": self.source.source_type.value,
            "status": self.source.status.value,
            "total_amount": str(self.source.total_amount),
            "paid_to_date": str(self.source.paid_to_date),
            "remaining_balance": str(self.source.remaining_balance()),
            "payments_count": len(self.payments),
            "distributions_count": len(self.distributions),
        }


class RoyaltyDistributor:
    """
    Manages distribution of royalty payments to recipients.
    Handles DAO token holder distributions and tax reporting.
    """
    
    def __init__(self, config: RoyaltyRefineryConfig = None):
        self.config = config or get_royalty_config()
        self.pending_distributions: List[Distribution] = []
        self.completed_distributions: List[Distribution] = []
    
    async def queue_distribution(self, distribution: Distribution) -> None:
        """Queue a distribution for processing"""
        self.pending_distributions.append(distribution)
        
        logger.info(
            "Distribution queued",
            distribution_id=distribution.distribution_id,
            recipient=distribution.recipient_name,
            amount=str(distribution.amount),
        )
    
    async def process_distributions(self) -> List[Distribution]:
        """Process all pending distributions"""
        processed = []
        
        for dist in self.pending_distributions[:]:
            try:
                # Determine if 1099 required
                if dist.tax_reportable and float(dist.amount) >= self.config.audit.reporting_threshold:
                    dist.form_1099_required = True
                
                # Execute distribution (placeholder for actual payment integration)
                dist.status = "completed"
                dist.distributed_at = datetime.now(timezone.utc)
                dist.transaction_hash = self._generate_transaction_hash(dist)
                
                self.pending_distributions.remove(dist)
                self.completed_distributions.append(dist)
                processed.append(dist)
                
                logger.info(
                    "Distribution processed",
                    distribution_id=dist.distribution_id,
                    recipient=dist.recipient_name,
                    amount=str(dist.amount),
                )
                
            except Exception as e:
                logger.error(
                    "Distribution failed",
                    distribution_id=dist.distribution_id,
                    error=str(e),
                )
        
        return processed
    
    def _generate_transaction_hash(self, dist: Distribution) -> str:
        """Generate transaction hash for verification"""
        data = {
            "distribution_id": dist.distribution_id,
            "payment_id": dist.payment_id,
            "recipient": dist.recipient_name,
            "amount": str(dist.amount),
            "distributed_at": dist.distributed_at.isoformat() if dist.distributed_at else None,
        }
        json_str = json.dumps(data, sort_keys=True)
        return hashlib.sha256(json_str.encode()).hexdigest()
    
    async def distribute_to_dao_members(
        self, 
        total_amount: Decimal,
        token_holders: Dict[str, float]  # address -> stake percentage
    ) -> List[Distribution]:
        """Distribute to DAO token holders based on stake"""
        distributions = []
        
        for address, stake_pct in token_holders.items():
            member_share = total_amount * Decimal(str(stake_pct))
            
            dist = Distribution(
                distribution_id=str(uuid.uuid4()),
                payment_id="dao_distribution",
                recipient_type=DistributionPriority.DAO_MEMBERS,
                recipient_name=address,
                amount=member_share,
                tax_reportable=True,
            )
            distributions.append(dist)
            await self.queue_distribution(dist)
        
        return distributions
    
    def get_tax_report(
        self, 
        year: int,
        recipient: str = None
    ) -> Dict[str, Any]:
        """Generate tax report for distributions"""
        filtered = [
            d for d in self.completed_distributions
            if d.distributed_at and d.distributed_at.year == year
            and (recipient is None or d.recipient_name == recipient)
        ]
        
        total_distributed = sum(d.amount for d in filtered)
        taxable_total = sum(d.amount for d in filtered if d.tax_reportable)
        form_1099_count = sum(1 for d in filtered if d.form_1099_required)
        
        return {
            "year": year,
            "recipient": recipient,
            "total_distributed": str(total_distributed),
            "taxable_total": str(taxable_total),
            "distribution_count": len(filtered),
            "form_1099_required_count": form_1099_count,
            "distributions": [asdict(d) for d in filtered],
        }


class RoyaltyAuditTrail:
    """
    Maintains immutable audit trail for all royalty operations.
    Provides compliance and verification capabilities.
    """
    
    def __init__(self, config: RoyaltyRefineryConfig = None):
        self.config = config or get_royalty_config()
        self.entries: List[AuditEntry] = []
        self._last_hash = "genesis"
    
    async def log_action(
        self,
        action: str,
        entity_type: str,
        entity_id: str,
        details: Dict[str, Any],
        actor: str = "system"
    ) -> AuditEntry:
        """Log an action to the audit trail"""
        entry = AuditEntry(
            entry_id=str(uuid.uuid4()),
            timestamp=datetime.now(timezone.utc),
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            details=details,
            actor=actor,
            previous_hash=self._last_hash,
        )
        
        # Calculate entry hash (blockchain-like chaining)
        entry.entry_hash = self._calculate_entry_hash(entry)
        self._last_hash = entry.entry_hash
        
        self.entries.append(entry)
        
        if self.config.audit.enable_audit_trail:
            logger.info(
                "Audit entry logged",
                entry_id=entry.entry_id,
                action=action,
                entity_type=entity_type,
                entity_id=entity_id,
            )
        
        return entry
    
    def _calculate_entry_hash(self, entry: AuditEntry) -> str:
        """Calculate hash for audit entry"""
        data = {
            "entry_id": entry.entry_id,
            "timestamp": entry.timestamp.isoformat(),
            "action": entry.action,
            "entity_type": entry.entity_type,
            "entity_id": entry.entity_id,
            "details": entry.details,
            "actor": entry.actor,
            "previous_hash": entry.previous_hash,
        }
        json_str = json.dumps(data, sort_keys=True, default=str)
        return hashlib.sha256(json_str.encode()).hexdigest()
    
    def verify_chain(self) -> bool:
        """Verify integrity of audit trail"""
        if not self.entries:
            return True
        
        # Check genesis entry
        if self.entries[0].previous_hash != "genesis":
            return False
        
        # Verify chain
        for i, entry in enumerate(self.entries):
            # Recalculate hash
            recalculated = self._calculate_entry_hash(entry)
            if recalculated != entry.entry_hash:
                logger.error(f"Hash mismatch at entry {entry.entry_id}")
                return False
            
            # Check chain linking
            if i > 0:
                if entry.previous_hash != self.entries[i-1].entry_hash:
                    logger.error(f"Chain broken at entry {entry.entry_id}")
                    return False
        
        return True
    
    def get_entries(
        self,
        entity_type: str = None,
        entity_id: str = None,
        action: str = None,
        start_date: datetime = None,
        end_date: datetime = None
    ) -> List[AuditEntry]:
        """Query audit trail with filters"""
        filtered = self.entries[:]
        
        if entity_type:
            filtered = [e for e in filtered if e.entity_type == entity_type]
        if entity_id:
            filtered = [e for e in filtered if e.entity_id == entity_id]
        if action:
            filtered = [e for e in filtered if e.action == action]
        if start_date:
            filtered = [e for e in filtered if e.timestamp >= start_date]
        if end_date:
            filtered = [e for e in filtered if e.timestamp <= end_date]
        
        return filtered
    
    def export_audit_trail(self, format: str = "json") -> str:
        """Export audit trail for compliance"""
        if format == "json":
            return json.dumps(
                [asdict(e) for e in self.entries],
                indent=2,
                default=str
            )
        else:
            raise ValueError(f"Unsupported format: {format}")

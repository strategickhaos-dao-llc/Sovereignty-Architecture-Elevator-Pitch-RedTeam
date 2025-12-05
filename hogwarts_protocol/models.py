"""
Hogwarts Protocol Data Models

Defines the core entities for the educational blockchain system:
- Student: Learner identity with wallet integration
- Spell: Educational artifact (code/work submission)
- Course: Educational module/assignment container
- CFTBalance: CourseForge Token accounting
- SpellTransaction: Revenue routing and marketplace activity
"""

import hashlib
import uuid
from datetime import datetime, timezone
from decimal import Decimal
from enum import Enum
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict


class SpellStatus(Enum):
    """Status of an educational artifact (spell)"""
    DRAFT = "draft"              # Work in progress
    SUBMITTED = "submitted"      # Awaiting review
    VERIFIED = "verified"        # Passed validation
    CERTIFIED = "certified"      # On-chain registered
    REVOKED = "revoked"          # Invalidated


class CFTTransactionType(Enum):
    """Types of CFT token transactions"""
    MINT = "mint"                # New tokens created (completed work)
    BURN = "burn"                # Tokens destroyed
    TRANSFER = "transfer"        # Tokens moved (if transferable)
    STAKE = "stake"              # Tokens locked for governance
    UNSTAKE = "unstake"          # Tokens unlocked from governance
    REWARD = "reward"            # Platform rewards
    FEE = "fee"                  # Platform fees deducted


class RevenueRouteType(Enum):
    """Revenue distribution categories"""
    CREATOR = "creator"          # Original spell author
    PLATFORM = "platform"        # CourseQuest platform
    CHARITY = "charity"          # ValorYield nonprofit
    INSTRUCTOR = "instructor"    # Course instructor share
    SCHOLARSHIP = "scholarship"  # Scholarship fund pool


@dataclass
class Student:
    """
    Student entity - learner with blockchain wallet integration
    
    The student represents an educational identity that can:
    - Own spells (educational artifacts)
    - Accumulate CFT (non-transferable XP tokens)
    - Participate in governance (with staked CFT)
    """
    student_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    
    # Educational identity
    edu_email: Optional[str] = None
    edu_institution: Optional[str] = None        # e.g., "SNHU"
    display_name: Optional[str] = None
    
    # Blockchain identity
    wallet_address: Optional[str] = None         # Ethereum-style address
    wallet_nonce: int = 0                        # For signature verification
    
    # Profile metadata
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    is_active: bool = True
    
    # Aggregated stats (computed)
    total_spells: int = 0
    total_cft: Decimal = Decimal("0")
    governance_weight: Decimal = Decimal("0")    # Staked CFT
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        data = asdict(self)
        data['created_at'] = self.created_at.isoformat()
        data['updated_at'] = self.updated_at.isoformat()
        data['total_cft'] = str(self.total_cft)
        data['governance_weight'] = str(self.governance_weight)
        return data


@dataclass
class Course:
    """
    Course entity - educational module container
    
    Represents a course or learning module that contains assignments.
    Spells are linked to specific assignments within courses.
    """
    course_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    
    # Course identification
    course_code: str = ""                        # e.g., "MAT-243"
    course_name: str = ""                        # e.g., "Applied Statistics"
    institution: str = ""                        # e.g., "SNHU"
    
    # Course metadata
    description: Optional[str] = None
    learning_outcomes: List[str] = field(default_factory=list)
    
    # Platform configuration
    platform: str = "CourseQuest Hogwarts"
    xp_multiplier: Decimal = Decimal("1.0")      # Course difficulty bonus
    
    # Timestamps
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_active: bool = True
    
    # Revenue configuration
    instructor_share_pct: Decimal = Decimal("0.10")  # 10% default
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        data = asdict(self)
        data['created_at'] = self.created_at.isoformat()
        if self.start_date:
            data['start_date'] = self.start_date.isoformat()
        if self.end_date:
            data['end_date'] = self.end_date.isoformat()
        data['xp_multiplier'] = str(self.xp_multiplier)
        data['instructor_share_pct'] = str(self.instructor_share_pct)
        return data


@dataclass
class Assignment:
    """
    Assignment entity - specific task within a course
    
    Represents a graded assignment that students submit spells for.
    """
    assignment_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    course_id: str = ""
    
    # Assignment details
    assignment_name: str = ""                    # e.g., "Project One"
    assignment_code: Optional[str] = None        # e.g., "P1"
    description: Optional[str] = None
    
    # Rubric / requirements
    rubric_url: Optional[str] = None
    requirements: List[str] = field(default_factory=list)
    
    # XP configuration
    base_xp: int = 100                           # Base XP for completion
    max_grade_bonus: Decimal = Decimal("0.5")    # 50% bonus for A+ grade
    
    # Timestamps
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    due_date: Optional[datetime] = None
    is_active: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        data = asdict(self)
        data['created_at'] = self.created_at.isoformat()
        if self.due_date:
            data['due_date'] = self.due_date.isoformat()
        data['max_grade_bonus'] = str(self.max_grade_bonus)
        return data


@dataclass
class Spell:
    """
    Spell entity - educational artifact (code submission)
    
    A spell is a completed piece of educational work that:
    - Can be hashed and registered on-chain
    - Earns CFT when verified
    - Can be licensed in the marketplace
    """
    spell_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    
    # Ownership
    owner_id: str = ""                           # Student who created it
    
    # Course linkage
    course_id: Optional[str] = None
    assignment_id: Optional[str] = None
    
    # Spell content
    spell_name: str = ""                         # e.g., "spell_descriptive_stats.py"
    spell_type: str = "python"                   # File type / language
    content_hash: Optional[str] = None           # SHA-256 of content
    file_path: Optional[str] = None              # Storage location
    
    # Verification
    status: SpellStatus = SpellStatus.DRAFT
    grade: Optional[str] = None                  # e.g., "B+", "A"
    grade_numeric: Optional[Decimal] = None      # e.g., 3.3, 4.0
    verified_at: Optional[datetime] = None
    verified_by: Optional[str] = None            # Verifier ID
    
    # On-chain registration
    on_chain_tx_hash: Optional[str] = None       # Blockchain transaction
    on_chain_token_id: Optional[int] = None      # NFT/SBT token ID
    chain_id: Optional[int] = None               # Network ID
    
    # CFT earned
    xp_earned: int = 0
    cft_minted: Decimal = Decimal("0")
    
    # Marketplace
    is_licensable: bool = False                  # Available for licensing
    license_price: Optional[Decimal] = None      # Price in fiat/stablecoin
    total_licenses_sold: int = 0
    total_revenue: Decimal = Decimal("0")
    
    # Timestamps
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    
    # Metadata
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def compute_content_hash(self, content: bytes) -> str:
        """Compute SHA-256 hash of spell content"""
        self.content_hash = hashlib.sha256(content).hexdigest()
        return self.content_hash
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        data = asdict(self)
        data['status'] = self.status.value
        data['created_at'] = self.created_at.isoformat()
        data['updated_at'] = self.updated_at.isoformat()
        if self.verified_at:
            data['verified_at'] = self.verified_at.isoformat()
        if self.grade_numeric:
            data['grade_numeric'] = str(self.grade_numeric)
        data['cft_minted'] = str(self.cft_minted)
        if self.license_price:
            data['license_price'] = str(self.license_price)
        data['total_revenue'] = str(self.total_revenue)
        return data
    
    def to_on_chain_record(self) -> Dict[str, Any]:
        """
        Generate minimal on-chain record structure
        
        This is what gets stored on the blockchain:
        - Minimal data to prove ownership and completion
        - References back to off-chain details
        """
        return {
            "spell_id": self.spell_id,
            "owner_wallet": None,  # To be filled from student lookup
            "content_hash": self.content_hash,
            "course_code": None,   # To be filled from course lookup
            "assignment_code": None,
            "grade": self.grade,
            "timestamp": self.created_at.isoformat() if self.created_at else None,
            "platform": "CourseQuest Hogwarts"
        }


@dataclass
class CFTBalance:
    """
    CFT Balance entity - CourseForge Token accounting
    
    Tracks a student's CFT balance with:
    - Available balance (for unlocking features)
    - Staked balance (for governance weight)
    - Lifetime earned (total ever minted to this account)
    """
    balance_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    student_id: str = ""
    
    # Balances (using Decimal for precision)
    available_balance: Decimal = Decimal("0")    # Spendable CFT
    staked_balance: Decimal = Decimal("0")       # Locked for governance
    lifetime_earned: Decimal = Decimal("0")      # Total ever minted
    
    # Timestamps
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    
    @property
    def total_balance(self) -> Decimal:
        """Total CFT owned (available + staked)"""
        return self.available_balance + self.staked_balance
    
    @property
    def governance_weight(self) -> Decimal:
        """Governance voting power (based on staked CFT)"""
        return self.staked_balance
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "balance_id": self.balance_id,
            "student_id": self.student_id,
            "available_balance": str(self.available_balance),
            "staked_balance": str(self.staked_balance),
            "lifetime_earned": str(self.lifetime_earned),
            "total_balance": str(self.total_balance),
            "governance_weight": str(self.governance_weight),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


@dataclass
class CFTTransaction:
    """
    CFT Transaction entity - token movement record
    
    Records all CFT movements for audit trail:
    - Minting (when spells are verified)
    - Staking/unstaking (for governance)
    - Platform fees (for premium features)
    """
    transaction_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    
    # Participants
    student_id: str = ""
    from_balance: Optional[str] = None           # Source (None for mints)
    to_balance: Optional[str] = None             # Destination (None for burns)
    
    # Transaction details
    transaction_type: CFTTransactionType = CFTTransactionType.MINT
    amount: Decimal = Decimal("0")
    
    # Reference
    reference_type: Optional[str] = None         # e.g., "spell", "governance"
    reference_id: Optional[str] = None           # ID of related entity
    reason: Optional[str] = None                 # Human-readable description
    
    # Timestamps
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    
    # On-chain reference (if applicable)
    on_chain_tx_hash: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "transaction_id": self.transaction_id,
            "student_id": self.student_id,
            "from_balance": self.from_balance,
            "to_balance": self.to_balance,
            "transaction_type": self.transaction_type.value,
            "amount": str(self.amount),
            "reference_type": self.reference_type,
            "reference_id": self.reference_id,
            "reason": self.reason,
            "created_at": self.created_at.isoformat(),
            "on_chain_tx_hash": self.on_chain_tx_hash
        }


@dataclass
class RevenueRoute:
    """
    Revenue Route entity - how money flows when spells are licensed
    
    Defines the split for marketplace transactions:
    - Creator share (spell author)
    - Platform share (CourseQuest)
    - Charity share (ValorYield)
    - Instructor share (if applicable)
    """
    route_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    spell_id: str = ""
    
    # Route configuration
    route_type: RevenueRouteType = RevenueRouteType.CREATOR
    recipient_id: Optional[str] = None           # Student/Instructor/Pool ID
    recipient_address: Optional[str] = None      # Wallet for payout
    percentage: Decimal = Decimal("0")           # Share percentage (0-100)
    
    # Computed totals
    total_received: Decimal = Decimal("0")       # Lifetime received
    pending_payout: Decimal = Decimal("0")       # Awaiting disbursement
    
    # Timestamps
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "route_id": self.route_id,
            "spell_id": self.spell_id,
            "route_type": self.route_type.value,
            "recipient_id": self.recipient_id,
            "recipient_address": self.recipient_address,
            "percentage": str(self.percentage),
            "total_received": str(self.total_received),
            "pending_payout": str(self.pending_payout),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


@dataclass  
class SpellLicense:
    """
    Spell License entity - marketplace transaction
    
    Records when someone licenses a spell for reuse.
    """
    license_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    
    # Spell being licensed
    spell_id: str = ""
    
    # Parties
    licensor_id: str = ""                        # Original spell owner
    licensee_id: str = ""                        # Student acquiring license
    
    # Transaction details
    price_paid: Decimal = Decimal("0")           # Amount in fiat/stablecoin
    payment_currency: str = "USD"
    payment_processor: str = "stripe"            # stripe, crypto, etc.
    payment_reference: Optional[str] = None      # External transaction ID
    
    # License terms
    license_type: str = "educational"            # educational, commercial, etc.
    expires_at: Optional[datetime] = None
    
    # Timestamps
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "license_id": self.license_id,
            "spell_id": self.spell_id,
            "licensor_id": self.licensor_id,
            "licensee_id": self.licensee_id,
            "price_paid": str(self.price_paid),
            "payment_currency": self.payment_currency,
            "payment_processor": self.payment_processor,
            "payment_reference": self.payment_reference,
            "license_type": self.license_type,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "created_at": self.created_at.isoformat()
        }


# Default revenue split configuration
DEFAULT_REVENUE_SPLIT = {
    RevenueRouteType.CREATOR: Decimal("60"),      # 60% to spell author
    RevenueRouteType.PLATFORM: Decimal("20"),     # 20% to CourseQuest
    RevenueRouteType.CHARITY: Decimal("10"),      # 10% to ValorYield
    RevenueRouteType.SCHOLARSHIP: Decimal("10"), # 10% to scholarship pool
}


def create_default_revenue_routes(spell_id: str, creator_id: str, creator_address: Optional[str] = None) -> List[RevenueRoute]:
    """
    Create default revenue routes for a spell
    
    Uses the standard split:
    - 60% Creator
    - 20% Platform
    - 10% ValorYield (charity)
    - 10% Scholarship fund
    """
    routes = []
    
    # Creator route
    routes.append(RevenueRoute(
        spell_id=spell_id,
        route_type=RevenueRouteType.CREATOR,
        recipient_id=creator_id,
        recipient_address=creator_address,
        percentage=DEFAULT_REVENUE_SPLIT[RevenueRouteType.CREATOR]
    ))
    
    # Platform route
    routes.append(RevenueRoute(
        spell_id=spell_id,
        route_type=RevenueRouteType.PLATFORM,
        recipient_id="platform",
        percentage=DEFAULT_REVENUE_SPLIT[RevenueRouteType.PLATFORM]
    ))
    
    # Charity (ValorYield) route
    routes.append(RevenueRoute(
        spell_id=spell_id,
        route_type=RevenueRouteType.CHARITY,
        recipient_id="valoryield",
        percentage=DEFAULT_REVENUE_SPLIT[RevenueRouteType.CHARITY]
    ))
    
    # Scholarship route
    routes.append(RevenueRoute(
        spell_id=spell_id,
        route_type=RevenueRouteType.SCHOLARSHIP,
        recipient_id="scholarship_pool",
        percentage=DEFAULT_REVENUE_SPLIT[RevenueRouteType.SCHOLARSHIP]
    ))
    
    return routes

"""
DiviDen Refinery - Royalty Refinery Configuration
Settings for royalty/reparation stream management
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from enum import Enum


class RoyaltyType(Enum):
    """Types of royalty streams"""
    SETTLEMENT = "settlement"           # Legal settlement payments
    JUDGMENT = "judgment"               # Court-ordered payments
    VOLUNTARY = "voluntary"             # Voluntary reparations
    LICENSING = "licensing"             # IP licensing royalties
    RECURRING = "recurring"             # Ongoing royalty agreements


class PaymentFrequency(Enum):
    """Payment frequency options"""
    ONE_TIME = "one_time"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    ANNUAL = "annual"
    PERPETUAL = "perpetual"


class DistributionPriority(Enum):
    """Priority levels for distribution"""
    CHARITY = "charity"                 # 7% mandatory charitable
    VICTIM_FUND = "victim_fund"         # Victim compensation
    OPERATIONAL = "operational"         # Operating expenses
    DAO_MEMBERS = "dao_members"         # Token holder distribution
    RESERVE = "reserve"                 # Reserve fund


@dataclass
class CharityConfig:
    """Configuration for verified charities"""
    name: str
    ein: str  # IRS Employer Identification Number
    allocation_pct: float
    verification_status: str = "verified"
    last_verified: Optional[str] = None


@dataclass
class DistributionConfig:
    """Distribution allocation configuration"""
    # Mandatory allocations
    charity_minimum_pct: float = 0.07           # 7% minimum to charity
    
    # Standard allocation model
    charity_allocation_pct: float = 0.07        # 7% to verified charities
    victim_fund_pct: float = 0.10               # 10% to victim compensation
    operational_pct: float = 0.10               # 10% operational reserve
    dao_distribution_pct: float = 0.63          # 63% to DAO members
    reserve_pct: float = 0.10                   # 10% emergency reserve
    
    # Verified charity recipients
    verified_charities: List[CharityConfig] = field(default_factory=lambda: [
        CharityConfig(
            name="National Center for Missing & Exploited Children",
            ein="52-1328557",
            allocation_pct=0.20,
        ),
        CharityConfig(
            name="RAINN",
            ein="52-1876465", 
            allocation_pct=0.20,
        ),
        CharityConfig(
            name="National Domestic Violence Hotline",
            ein="75-2557071",
            allocation_pct=0.20,
        ),
        CharityConfig(
            name="Cyber Civil Rights Initiative",
            ein="46-2892788",
            allocation_pct=0.20,
        ),
        CharityConfig(
            name="Electronic Frontier Foundation",
            ein="04-3091431",
            allocation_pct=0.20,
        ),
    ])


@dataclass
class AuditConfig:
    """Audit and compliance configuration"""
    enable_audit_trail: bool = True
    retention_years: int = 7
    require_receipts: bool = True
    generate_tax_reports: bool = True
    
    # Compliance thresholds
    reporting_threshold: float = 600.0          # IRS 1099 threshold
    large_transaction_threshold: float = 10000.0 # Enhanced reporting


@dataclass
class RoyaltyRefineryConfig:
    """Main configuration for Royalty Refinery"""
    enabled: bool = True
    environment: str = "development"
    
    # Distribution configuration
    distribution: DistributionConfig = field(default_factory=DistributionConfig)
    
    # Audit configuration
    audit: AuditConfig = field(default_factory=AuditConfig)
    
    # Processing settings
    auto_distribute: bool = True
    distribution_delay_days: int = 30           # Hold before distribution
    minimum_distribution: float = 100.0         # Minimum amount to distribute
    
    # Notification settings
    notify_on_receipt: bool = True
    notify_on_distribution: bool = True
    discord_webhook: Optional[str] = None
    
    def validate(self) -> List[str]:
        """Validate configuration"""
        errors = []
        
        # Check distribution percentages sum to 100%
        total_pct = (
            self.distribution.charity_allocation_pct +
            self.distribution.victim_fund_pct +
            self.distribution.operational_pct +
            self.distribution.dao_distribution_pct +
            self.distribution.reserve_pct
        )
        
        if abs(total_pct - 1.0) > 0.001:
            errors.append(f"Distribution percentages sum to {total_pct:.1%}, should be 100%")
        
        # Check charity minimum
        if self.distribution.charity_allocation_pct < self.distribution.charity_minimum_pct:
            errors.append(
                f"Charity allocation {self.distribution.charity_allocation_pct:.1%} "
                f"below minimum {self.distribution.charity_minimum_pct:.1%}"
            )
        
        # Check charity allocations sum to 100%
        charity_total = sum(c.allocation_pct for c in self.distribution.verified_charities)
        if abs(charity_total - 1.0) > 0.001:
            errors.append(f"Charity allocations sum to {charity_total:.1%}, should be 100%")
        
        return errors


# Global configuration instance
_config: Optional[RoyaltyRefineryConfig] = None


def get_royalty_config() -> RoyaltyRefineryConfig:
    """Get royalty refinery configuration (singleton)"""
    global _config
    if _config is None:
        _config = RoyaltyRefineryConfig()
    return _config


def load_config_from_file(path: str) -> RoyaltyRefineryConfig:
    """Load configuration from YAML file"""
    import yaml
    
    with open(path, 'r') as f:
        data = yaml.safe_load(f)
    
    config = RoyaltyRefineryConfig(
        enabled=data.get('enabled', True),
        environment=data.get('environment', 'development'),
    )
    
    # Load distribution config
    if 'distribution' in data:
        dist_data = data['distribution']
        config.distribution = DistributionConfig(
            charity_allocation_pct=dist_data.get('charity_allocation_pct', 0.07),
            victim_fund_pct=dist_data.get('victim_fund_pct', 0.10),
            operational_pct=dist_data.get('operational_pct', 0.10),
            dao_distribution_pct=dist_data.get('dao_distribution_pct', 0.63),
            reserve_pct=dist_data.get('reserve_pct', 0.10),
        )
    
    return config

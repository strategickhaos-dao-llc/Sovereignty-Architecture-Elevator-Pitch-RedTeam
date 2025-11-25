"""
Legal Firewall Engine - LB-GSE Implementation
Strategickhaos DAO LLC

This module implements the Legally-Bounded Generative Systems Engineering (LB-GSE)
methodology as an automated compliance engine.
"""

from .generator import LegalFirewallEngine
from .models import (
    LegalPrimitive,
    CapabilityRequirement,
    CapabilityGap,
    ComponentInfo,
    FirewallReport,
)

__version__ = "1.0.0"
__all__ = [
    "LegalFirewallEngine",
    "LegalPrimitive",
    "CapabilityRequirement",
    "CapabilityGap",
    "ComponentInfo",
    "FirewallReport",
]

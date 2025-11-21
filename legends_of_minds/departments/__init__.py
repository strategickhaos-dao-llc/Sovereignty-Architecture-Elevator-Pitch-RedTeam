"""
Legends of Minds - Departments Module
All department implementations
"""

from .proof_ledger import ProofLedger, proof_ledger
from .legal_compliance import LegalComplianceChecker, compliance_checker

__all__ = [
    'ProofLedger',
    'proof_ledger',
    'LegalComplianceChecker',
    'compliance_checker'
]

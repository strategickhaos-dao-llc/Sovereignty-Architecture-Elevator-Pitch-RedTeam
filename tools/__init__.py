"""
Evidence Anchoring Tools
Strategickhaos DAO LLC

Tools for creating mathematically unbreakable audit trails using:
- GPG signatures for authenticity
- OpenTimestamps for immutability on Bitcoin blockchain
"""

from .evidence_logger import EvidenceLogger

__all__ = ['EvidenceLogger']
__version__ = '1.2.0'

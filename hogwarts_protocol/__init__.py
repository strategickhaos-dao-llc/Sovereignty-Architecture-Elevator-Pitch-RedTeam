"""
Hogwarts Protocol - Educational Blockchain Integration

This module implements the "Great Hall Ledger" system for:
- Spell (educational artifact) ownership tracking
- CourseForge Token (CFT) - crystallized XP / utility token
- Transcript-on-chain credentialing
- Revenue routing for spell marketplace

Architecture:
- PostgreSQL (off-chain): Full data model with relationships
- Blockchain (on-chain): Proof of ownership, hashes, CFT balances
"""

__version__ = "0.1.0"
__author__ = "Strategickhaos DAO LLC / Valoryield Engine"

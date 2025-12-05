"""
DAO Module - Git-Native Multi-Agent Consensus Protocol
Strategickhaos DAO LLC

This module implements the core governance mechanisms for
distributed decision-making using Git as the consensus substrate.
"""

from .kernel import (
    DAOKernel,
    Proposal,
    ProposalStatus,
    Vote,
    VoteDecision,
    ConsensusResult
)

__all__ = [
    'DAOKernel',
    'Proposal',
    'ProposalStatus', 
    'Vote',
    'VoteDecision',
    'ConsensusResult'
]

__version__ = '1.0.0'

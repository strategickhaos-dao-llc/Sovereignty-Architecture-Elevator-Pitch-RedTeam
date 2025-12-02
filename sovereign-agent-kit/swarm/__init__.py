"""
Sovereign Agent Kit - Quantum Swarm Intelligence
Quantum loop orchestration for autonomous LLM agents
"""

__version__ = "1.0.0"
__author__ = "Strategickhaos DAO LLC"

from .quantum_loop import QuantumAgent, run_quantum_loop
from .consensus import ConsensusChecker, consensus_reached

__all__ = [
    "QuantumAgent",
    "run_quantum_loop",
    "ConsensusChecker",
    "consensus_reached",
]

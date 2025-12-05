"""
Colossus Grok-5 Training Package

Training orchestration with energy-aware scheduling and checkpoint consensus.
"""

# Lazy imports to avoid circular dependencies and test issues
__all__ = [
    "EnergyScheduler",
    "PowerWindowDecision",
    "ConsensusProtocol",
    "CheckpointConsensus",
    "CheckpointGuardian",
    "Grok5Trainer",
]


def __getattr__(name):
    """Lazy import to avoid loading all modules on package import."""
    if name in ("EnergyScheduler", "PowerWindowDecision"):
        from .energy_scheduler import EnergyScheduler
        from .consensus_protocol import PowerWindowDecision
        return EnergyScheduler if name == "EnergyScheduler" else PowerWindowDecision
    elif name in ("ConsensusProtocol", "CheckpointConsensus"):
        from .consensus_protocol import ConsensusProtocol, CheckpointConsensus
        return ConsensusProtocol if name == "ConsensusProtocol" else CheckpointConsensus
    elif name == "CheckpointGuardian":
        from .checkpoint_guardian import CheckpointGuardian
        return CheckpointGuardian
    elif name == "Grok5Trainer":
        from .grok5_trainer import Grok5Trainer
        return Grok5Trainer
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

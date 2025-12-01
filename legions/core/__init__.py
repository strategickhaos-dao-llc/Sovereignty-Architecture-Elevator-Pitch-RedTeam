"""
LEGIONS CORE — Neural Mesh Systems

Core components:
- ObsidianNeuralMesh: Discord bot for council operations
- Board receipt generation with cryptographic proof
- Vault synchronization with genesis increment signing
"""

from .obsidian_neural_mesh import (
    ObsidianNeuralMesh,
    CouncilStatus,
    GENESIS_INCREMENT,
    DIVIDEND_YIELD,
    ARCHITECT,
    GENESIS_DATE,
    COUNCIL_QUADRANTS,
    BOARD_MEMBERS,
    generate_genesis_hash,
    setup,
)

__all__ = [
    "ObsidianNeuralMesh",
    "CouncilStatus",
    "GENESIS_INCREMENT",
    "DIVIDEND_YIELD",
    "ARCHITECT",
    "GENESIS_DATE",
    "COUNCIL_QUADRANTS",
    "BOARD_MEMBERS",
    "generate_genesis_hash",
    "setup",
]

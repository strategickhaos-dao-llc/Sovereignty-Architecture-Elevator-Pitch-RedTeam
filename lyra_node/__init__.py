"""
Lyra Node - AI Task Distribution System
Multi-node architecture for distributed AI workloads.

Components:
- Guestbook-1 Dispatcher: 3-node AI task distributor
- AI Readiness Scanner
- System Info Gatherer
"""

__version__ = "1.0.0"
__author__ = "StrategicKhaos Swarm Intelligence"

from .guestbook_1_dispatcher import (
    Guestbook1Dispatcher,
    AINode,
    NodeType,
    TaskCategory,
    TaskResult,
)

__all__ = [
    "Guestbook1Dispatcher",
    "AINode",
    "NodeType",
    "TaskCategory",
    "TaskResult",
]

"""
SovereignPRManager: Autonomous PR Orchestration System
Zero-button operation: Copilot generates → Legion validates → System merges
"""

__version__ = "1.0.0"
__author__ = "StrategicKhaos DAO"

from .pr_monitor import PRMonitor
from .legion_reviewer import LegionReviewer
from .conflict_detector import ConflictDetector
from .synthesis_engine import MergeDecisionEngine
from .auto_merger import AutoMerger
from .manager import SovereignPRManager

__all__ = [
    "PRMonitor",
    "LegionReviewer",
    "ConflictDetector",
    "MergeDecisionEngine",
    "AutoMerger",
    "SovereignPRManager",
]

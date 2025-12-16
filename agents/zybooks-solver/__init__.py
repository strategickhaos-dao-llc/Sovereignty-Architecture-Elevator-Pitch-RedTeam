"""
zyBooks Solver Agent
Auto-process zyBooks content for the StrategicKhaos swarm
"""

from .parser import ZyBooksParser, Question
from .solver import ZyBooksSolver, Answer
from .responder import ZyBooksResponder

__version__ = "1.0.0"
__all__ = ["ZyBooksParser", "ZyBooksSolver", "ZyBooksResponder", "Question", "Answer"]

"""
zyBooks Solver Package
Auto-process zyBooks content for rapid answer generation
"""

from .parser import ZyBooksParser, parse_zybooks_content, Question
from .solver import ZyBooksSolver, solve_questions, Answer
from .responder import ZyBooksResponder, format_vessel_mode, format_yaml

__version__ = "1.0.0"
__all__ = [
    'ZyBooksParser',
    'parse_zybooks_content',
    'Question',
    'ZyBooksSolver',
    'solve_questions',
    'Answer',
    'ZyBooksResponder',
    'format_vessel_mode',
    'format_yaml',
]

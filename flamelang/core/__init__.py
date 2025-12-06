"""
FlameLang Core Module
Sovereign Computing Platform - Language Processing Core
"""

from .lexer import Lexer
from .parser import Parser
from .interpreter import Interpreter
from .glyph_registry import GlyphRegistry
from .physics_engine import PhysicsEngine
from .sovereignty import SovereigntyProtocol

__all__ = [
    'Lexer',
    'Parser', 
    'Interpreter',
    'GlyphRegistry',
    'PhysicsEngine',
    'SovereigntyProtocol'
]

__version__ = '0.1.0'

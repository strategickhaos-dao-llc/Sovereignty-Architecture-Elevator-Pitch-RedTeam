"""
FlameLang - Sovereign Programming Language
Physics-integrated glyph-based compiler
"""

__version__ = '0.1.0'
__author__ = 'Strategickhaos DAO LLC'

from .core import Lexer, Token, TokenType, FlameLangCompiler, REPL
from .glyphs import GLYPH_REGISTRY, get_glyph
from .physics import ENGINE, PhysicsEngine
from .security import PROTOCOL, SovereigntyProtocol

__all__ = [
    'Lexer', 'Token', 'TokenType', 'FlameLangCompiler', 'REPL',
    'GLYPH_REGISTRY', 'get_glyph',
    'ENGINE', 'PhysicsEngine',
    'PROTOCOL', 'SovereigntyProtocol',
]

"""
FlameLang - Sovereign Computing Platform
A language with physics engine and sovereignty protocol
"""

__version__ = '0.1.0'
__author__ = 'Strategickhaos DAO LLC'

from .core import (
    Lexer,
    Parser,
    Interpreter,
    GlyphRegistry,
    PhysicsEngine,
    SovereigntyProtocol
)

__all__ = [
    'Lexer',
    'Parser',
    'Interpreter',
    'GlyphRegistry',
    'PhysicsEngine',
    'SovereigntyProtocol',
]

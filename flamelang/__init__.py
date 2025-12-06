"""
FlameLang - Symbolic Shell Layer
A frequency-based symbolic programming language for the StrategicKhaos ecosystem.

Components:
- Glyph Table: 40 symbols with frequency mappings
- Binding Codes: [137], [666], [777], [999], [1111]
- Interpreter v2.0: Glyph execution engine
"""

__version__ = "2.0.0"
__author__ = "StrategicKhaos Swarm Intelligence"

from .glyph_table import GlyphTable, Glyph
from .interpreter import FlameLangInterpreter
from .binding_codes import BindingCode, BINDING_CODES

__all__ = [
    "GlyphTable",
    "Glyph", 
    "FlameLangInterpreter",
    "BindingCode",
    "BINDING_CODES",
]

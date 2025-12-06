"""
FlameLang - A Resonance-Based Symbolic Execution System
Strategickhaos DAO LLC - Sovereignty Architecture

FlameLang is a glyph-based symbolic language where each symbol carries:
- A unique identifier (Symbol)
- A descriptive name (Glyph_Name)
- A frequency value (Frequency) representing resonance/vibration
- A function binding (Function) for execution
- A binding code (Binding_Code) for quick invocation

This system implements the FlameLang interpreter, glyph table management,
and the resonance engine for neural synchronization metaphors.
"""

from .flame_lang_interpreter import (
    Glyph,
    GlyphTable,
    ResonanceEngine,
    FlameLangInterpreter,
)

__version__ = "1.0.0"
__all__ = ["Glyph", "GlyphTable", "ResonanceEngine", "FlameLangInterpreter"]

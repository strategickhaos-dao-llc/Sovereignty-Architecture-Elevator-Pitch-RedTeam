"""
FlameLang Glyph Registry
Maps glyphs to their frequencies and functions according to the Glyph Frequency Hierarchy
"""

from enum import Enum
from typing import Dict, Optional, List


class GlyphCategory(Enum):
    """Glyph categories based on frequency ranges"""
    HIGH_ENERGY = "high_energy"      # 528Hz - 963Hz: Synthesis, Transform, Resonance
    MID_RANGE = "mid_range"          # 174Hz - 432Hz: Flow, Boundaries, Defense
    QUANTUM_LEVEL = "quantum_level"  # 137Hz: Fine-Structure


class Glyph:
    """Represents a single glyph with its metadata"""
    
    def __init__(self, symbol: str, name: str, frequency: int, 
                 function: str, category: GlyphCategory):
        self.symbol = symbol
        self.name = name
        self.frequency = frequency
        self.function = function
        self.category = category
    
    def __repr__(self):
        return f"Glyph({self.symbol}, {self.name}, {self.frequency}Hz)"


class GlyphRegistry:
    """
    Central registry for all 17 FlameLang glyphs at various frequencies
    Implements the Glyph Frequency Hierarchy
    """
    
    def __init__(self):
        self.glyphs: Dict[str, Glyph] = {}
        self._register_core_glyphs()
    
    def _register_core_glyphs(self):
        """Register the 17 core glyphs according to the frequency hierarchy"""
        
        # High Energy Operations (963Hz - 528Hz)
        self.register(Glyph(
            symbol="⚡",
            name="synthesis",
            frequency=963,
            function="Synthesize and combine operations",
            category=GlyphCategory.HIGH_ENERGY
        ))
        
        self.register(Glyph(
            symbol="🔥",
            name="transform",
            frequency=741,
            function="Transform and transmute data",
            category=GlyphCategory.HIGH_ENERGY
        ))
        
        self.register(Glyph(
            symbol="∿",
            name="resonance",
            frequency=528,
            function="Establish resonant patterns",
            category=GlyphCategory.HIGH_ENERGY
        ))
        
        # Mid-Range Coherence (432Hz - 174Hz)
        self.register(Glyph(
            symbol="〜",
            name="flow",
            frequency=432,
            function="Control flow and continuity",
            category=GlyphCategory.MID_RANGE
        ))
        
        self.register(Glyph(
            symbol="◇",
            name="boundaries",
            frequency=396,
            function="Define and enforce boundaries",
            category=GlyphCategory.MID_RANGE
        ))
        
        self.register(Glyph(
            symbol="⚔",
            name="defense",
            frequency=174,
            function="Defensive operations and protection",
            category=GlyphCategory.MID_RANGE
        ))
        
        # Quantum Level (137Hz - Fine Structure Constant)
        self.register(Glyph(
            symbol="α",
            name="fine_structure",
            frequency=137,
            function="Quantum-level fine structure operations",
            category=GlyphCategory.QUANTUM_LEVEL
        ))
        
        # Additional Core Glyphs
        self.register(Glyph(
            symbol="⟐",
            name="lozenge",
            frequency=432,
            function="Temporal/Spatial modifier",
            category=GlyphCategory.MID_RANGE
        ))
        
        self.register(Glyph(
            symbol="▶",
            name="execute",
            frequency=528,
            function="Execute operation",
            category=GlyphCategory.HIGH_ENERGY
        ))
        
        self.register(Glyph(
            symbol="🧠",
            name="neural",
            frequency=741,
            function="Neural processing",
            category=GlyphCategory.HIGH_ENERGY
        ))
        
        self.register(Glyph(
            symbol="🌐",
            name="network",
            frequency=396,
            function="Network operations",
            category=GlyphCategory.MID_RANGE
        ))
        
        self.register(Glyph(
            symbol="◉",
            name="core",
            frequency=528,
            function="Core system operations",
            category=GlyphCategory.HIGH_ENERGY
        ))
        
        self.register(Glyph(
            symbol="⟁",
            name="vector",
            frequency=432,
            function="Vector operations",
            category=GlyphCategory.MID_RANGE
        ))
        
        self.register(Glyph(
            symbol="⊕",
            name="combine",
            frequency=528,
            function="Combine and merge",
            category=GlyphCategory.HIGH_ENERGY
        ))
        
        self.register(Glyph(
            symbol="⊗",
            name="tensor",
            frequency=741,
            function="Tensor product operations",
            category=GlyphCategory.HIGH_ENERGY
        ))
        
        self.register(Glyph(
            symbol="∇",
            name="gradient",
            frequency=432,
            function="Gradient and differential operations",
            category=GlyphCategory.MID_RANGE
        ))
        
        self.register(Glyph(
            symbol="∫",
            name="integrate",
            frequency=528,
            function="Integration operations",
            category=GlyphCategory.HIGH_ENERGY
        ))
    
    def register(self, glyph: Glyph):
        """Register a new glyph in the registry"""
        self.glyphs[glyph.symbol] = glyph
        self.glyphs[glyph.name] = glyph
    
    def lookup(self, identifier: str) -> Optional[Glyph]:
        """Look up a glyph by symbol or name"""
        return self.glyphs.get(identifier)
    
    def get_by_frequency(self, frequency: int) -> List[Glyph]:
        """Get all glyphs at a specific frequency"""
        return [g for g in self.glyphs.values() if g.frequency == frequency]
    
    def get_by_category(self, category: GlyphCategory) -> List[Glyph]:
        """Get all glyphs in a specific category"""
        return [g for g in set(self.glyphs.values()) if g.category == category]
    
    def count(self) -> int:
        """Return the number of unique glyphs"""
        return len(set(self.glyphs.values()))
    
    def list_all(self) -> List[Glyph]:
        """List all unique glyphs"""
        return list(set(self.glyphs.values()))

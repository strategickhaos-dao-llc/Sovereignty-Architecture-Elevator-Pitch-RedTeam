#!/usr/bin/env python3
"""FlameLang Glyph Registry - Central registry for all glyphs."""

from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass
class Glyph:
    """Represents a glyph in the FlameLang system."""
    symbol: str
    name: str
    frequency: int  # Hz
    category: str
    description: str

class GlyphRegistry:
    """Central registry for all FlameLang glyphs."""
    
    def __init__(self):
        self.glyphs: Dict[str, Glyph] = {}
        self._initialize_glyphs()
    
    def _initialize_glyphs(self):
        """Initialize all built-in glyphs."""
        
        # Core glyphs
        core_glyphs = [
            Glyph('⚡', 'Execute', 528, 'core', 'Execute operation'),
            Glyph('🔥', 'Transform', 741, 'core', 'Transform data'),
            Glyph('🌊', 'Flow', 432, 'core', 'Flow control'),
            Glyph('⚛️', 'Compose', 963, 'core', 'Compose operations'),
            Glyph('🎯', 'Target', 639, 'core', 'Target selection'),
            Glyph('🔮', 'Synthesize', 852, 'core', 'Synthesize results'),
        ]
        
        # Physics glyphs
        physics_glyphs = [
            Glyph('BH1', 'Schwarzschild', 137, 'physics', 'Black hole simulation'),
            Glyph('OC1', 'Ocean_Coherence', 432, 'physics', 'Ocean eddy simulation'),
            Glyph('PS1', 'Photon_Sphere', 528, 'physics', 'Photon sphere'),
            Glyph('GR1', 'Geodesic', 963, 'physics', 'Geodesic computation'),
            Glyph('ED1', 'Eddy_Coherence', 285, 'physics', 'Eddy coherence'),
            Glyph('MT1', 'Metric_Compute', 741, 'physics', 'Metric tensor computation'),
        ]
        
        # Security glyphs
        security_glyphs = [
            Glyph('🛡️', 'Boundary_Harden', 174, 'security', 'Harden boundaries'),
            Glyph('🔒', 'Encrypt', 396, 'security', 'Encryption'),
            Glyph('👁️', 'Audit', 417, 'security', 'Audit operations'),
            Glyph('⚔️', 'Defend', 639, 'security', 'Defensive measures'),
            Glyph('🌐', 'Sovereignty', 852, 'security', 'Sovereignty enforcement'),
        ]
        
        # Register all glyphs
        for glyph in core_glyphs + physics_glyphs + security_glyphs:
            self.register(glyph)
    
    def register(self, glyph: Glyph):
        """Register a glyph."""
        self.glyphs[glyph.symbol] = glyph
    
    def get(self, symbol: str) -> Optional[Glyph]:
        """Get a glyph by symbol."""
        return self.glyphs.get(symbol)
    
    def by_category(self, category: str) -> List[Glyph]:
        """Get all glyphs in a category."""
        return [g for g in self.glyphs.values() if g.category == category]
    
    def all(self) -> List[Glyph]:
        """Get all glyphs."""
        return list(self.glyphs.values())
    
    def export_csv(self, filename: str):
        """Export glyph table to CSV."""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("Symbol,Name,Frequency,Category,Description\n")
            for glyph in sorted(self.glyphs.values(), key=lambda g: (g.category, g.name)):
                f.write(f"{glyph.symbol},{glyph.name},{glyph.frequency},{glyph.category},{glyph.description}\n")

# Global registry instance
REGISTRY = GlyphRegistry()

def main():
    """Test the registry."""
    print("FlameLang Glyph Registry")
    print("=" * 60)
    
    for category in ['core', 'physics', 'security']:
        print(f"\n{category.upper()} GLYPHS:")
        glyphs = REGISTRY.by_category(category)
        for glyph in sorted(glyphs, key=lambda g: g.name):
            print(f"  {glyph.symbol:4} {glyph.name:20} @ {glyph.frequency}Hz - {glyph.description}")
    
    print(f"\nTotal glyphs: {len(REGISTRY.all())}")

if __name__ == '__main__':
    main()

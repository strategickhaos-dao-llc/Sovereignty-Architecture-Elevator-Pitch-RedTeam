"""
FlameLang Glyph Table
40 symbols with frequency-based mappings and whale pulse integration.

Each glyph maps to:
- A unique symbol/identifier
- A binding code ([137], [666], [777], [999], [1111])
- A whale pulse frequency (5.87-6.44 Hz range)
- A piano key frequency (27.5-4186 Hz range - A0 to C8)
"""

from dataclasses import dataclass
from typing import Optional
import numpy as np


@dataclass
class Glyph:
    """Represents a single FlameLang glyph with frequency mappings."""
    
    id: int
    symbol: str
    name: str
    binding_code: int
    whale_freq: float  # Hz - whale pulse frequency (5.87-6.44 Hz)
    piano_freq: float  # Hz - piano key frequency (27.5-4186 Hz)
    description: str
    
    @property
    def resonance_ratio(self) -> float:
        """Calculate the resonance ratio between whale and piano frequencies."""
        if self.whale_freq == 0:
            return 0.0
        return self.piano_freq / self.whale_freq
    
    def __str__(self) -> str:
        return f"Glyph({self.symbol}|[{self.binding_code}]|{self.whale_freq:.2f}Hz→{self.piano_freq:.2f}Hz)"


class GlyphTable:
    """
    The complete FlameLang glyph table with 40 symbols.
    Maps each glyph to binding codes and frequency pairs.
    """
    
    # Binding code categories
    BINDING_CODES = [137, 666, 777, 999, 1111]
    
    # Whale pulse frequency range (Hz)
    WHALE_FREQ_MIN = 5.87
    WHALE_FREQ_MAX = 6.44
    
    # Piano frequency range (Hz) - A0 to C8
    PIANO_FREQ_MIN = 27.5
    PIANO_FREQ_MAX = 4186.0
    
    def __init__(self):
        """Initialize the glyph table with 40 symbols."""
        self._glyphs: dict[int, Glyph] = {}
        self._symbol_index: dict[str, int] = {}
        self._initialize_glyphs()
    
    def _initialize_glyphs(self) -> None:
        """Create all 40 glyphs with their frequency mappings."""
        # Generate frequency arrays for mapping
        whale_freqs = np.linspace(self.WHALE_FREQ_MIN, self.WHALE_FREQ_MAX, 40)
        piano_freqs = np.linspace(self.PIANO_FREQ_MIN, self.PIANO_FREQ_MAX, 40)
        
        # Define the 40 glyphs with their symbols and meanings
        glyph_definitions = [
            # Fire Glyphs (Binding Code 137) - Creation/Ignition
            ("🔥", "IGNITE", "Initiate process or creation"),
            ("⚡", "SPARK", "Quick activation trigger"),
            ("☀️", "RADIATE", "Broadcast/emit signal"),
            ("🌟", "STELLAR", "Peak performance marker"),
            ("💫", "TRANSCEND", "Elevate state or consciousness"),
            ("🔆", "ILLUMINATE", "Reveal hidden patterns"),
            ("✨", "MANIFEST", "Create tangible output"),
            ("🌋", "ERUPT", "Force immediate change"),
            
            # Water Glyphs (Binding Code 666) - Flow/Transformation
            ("🌊", "FLOW", "Continuous data stream"),
            ("💧", "DROPLET", "Single data unit"),
            ("🌀", "VORTEX", "Recursive processing"),
            ("❄️", "CRYSTALLIZE", "Lock state permanently"),
            ("🌧️", "PRECIPITATE", "Trigger cascade event"),
            ("🌈", "SPECTRUM", "Full range analysis"),
            ("💎", "COMPRESS", "Optimize and compress"),
            ("🔮", "DIVINE", "Predict future state"),
            
            # Earth Glyphs (Binding Code 777) - Structure/Foundation
            ("🌍", "GROUND", "Establish foundation"),
            ("⛰️", "ANCHOR", "Permanent storage"),
            ("🌲", "ROOT", "Deep system access"),
            ("🪨", "SOLIDIFY", "Make immutable"),
            ("🏔️", "ELEVATE", "Increase priority"),
            ("🌿", "GROW", "Organic expansion"),
            ("🌾", "HARVEST", "Collect results"),
            ("🍃", "RELEASE", "Graceful termination"),
            
            # Air Glyphs (Binding Code 999) - Communication/Movement
            ("💨", "TRANSMIT", "Send message"),
            ("🌬️", "BREATHE", "System heartbeat"),
            ("☁️", "SUSPEND", "Pause execution"),
            ("🌪️", "SCATTER", "Distribute load"),
            ("🪶", "LIFT", "Async elevation"),
            ("🦋", "TRANSFORM", "Metamorphic change"),
            ("🕊️", "PEACE", "Conflict resolution"),
            ("🦅", "SOAR", "Peak velocity mode"),
            
            # Void Glyphs (Binding Code 1111) - Meta/Transcendent
            ("🌑", "VOID", "Null/empty state"),
            ("⬛", "ABSORB", "Consume input"),
            ("🕳️", "PORTAL", "Cross-dimension link"),
            ("∞", "INFINITE", "Unbounded loop"),
            ("Ω", "OMEGA", "Final termination"),
            ("Φ", "PHI", "Golden ratio balance"),
            ("Ψ", "PSI", "Neural sync point"),
            ("Δ", "DELTA", "Change detection"),
        ]
        
        # Create glyphs with frequency mappings
        for i, (symbol, name, desc) in enumerate(glyph_definitions):
            # Assign binding code based on category (8 glyphs per code)
            binding_code = self.BINDING_CODES[i // 8]
            
            glyph = Glyph(
                id=i,
                symbol=symbol,
                name=name,
                binding_code=binding_code,
                whale_freq=float(whale_freqs[i]),
                piano_freq=float(piano_freqs[i]),
                description=desc
            )
            
            self._glyphs[i] = glyph
            self._symbol_index[symbol] = i
    
    def get_by_id(self, glyph_id: int) -> Optional[Glyph]:
        """Get a glyph by its numeric ID."""
        return self._glyphs.get(glyph_id)
    
    def get_by_symbol(self, symbol: str) -> Optional[Glyph]:
        """Get a glyph by its symbol."""
        glyph_id = self._symbol_index.get(symbol)
        if glyph_id is not None:
            return self._glyphs[glyph_id]
        return None
    
    def get_by_binding_code(self, code: int) -> list[Glyph]:
        """Get all glyphs with a specific binding code."""
        return [g for g in self._glyphs.values() if g.binding_code == code]
    
    def get_by_frequency_range(
        self, 
        min_whale: float = 0, 
        max_whale: float = float('inf'),
        min_piano: float = 0,
        max_piano: float = float('inf')
    ) -> list[Glyph]:
        """Get glyphs within specified frequency ranges."""
        return [
            g for g in self._glyphs.values()
            if min_whale <= g.whale_freq <= max_whale
            and min_piano <= g.piano_freq <= max_piano
        ]
    
    def all_glyphs(self) -> list[Glyph]:
        """Return all glyphs in the table."""
        return list(self._glyphs.values())
    
    def __len__(self) -> int:
        return len(self._glyphs)
    
    def __iter__(self):
        return iter(self._glyphs.values())
    
    def to_dict(self) -> dict:
        """Export the glyph table as a dictionary."""
        return {
            "version": "2.0.0",
            "total_glyphs": len(self._glyphs),
            "binding_codes": self.BINDING_CODES,
            "frequency_ranges": {
                "whale": {"min": self.WHALE_FREQ_MIN, "max": self.WHALE_FREQ_MAX, "unit": "Hz"},
                "piano": {"min": self.PIANO_FREQ_MIN, "max": self.PIANO_FREQ_MAX, "unit": "Hz"}
            },
            "glyphs": [
                {
                    "id": g.id,
                    "symbol": g.symbol,
                    "name": g.name,
                    "binding_code": g.binding_code,
                    "whale_freq": round(g.whale_freq, 4),
                    "piano_freq": round(g.piano_freq, 4),
                    "resonance_ratio": round(g.resonance_ratio, 4),
                    "description": g.description
                }
                for g in self._glyphs.values()
            ]
        }

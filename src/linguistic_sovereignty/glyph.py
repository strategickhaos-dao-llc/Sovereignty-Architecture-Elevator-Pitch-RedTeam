"""
Glyph dataclass for Linear A and other ancient scripts.

Represents a single character with geometric, phonetic, and correlation data.
"""

from dataclasses import dataclass, field
from typing import List, Tuple


@dataclass
class Glyph:
    """A single character from Linear A or other ancient script.
    
    Attributes:
        symbol: The actual Unicode glyph character
        unicode_code: Unicode code point (e.g., "U+10600")
        frequency: Statistical frequency in Linear A corpus (0-1)
        geometric_pattern: Stroke coordinates defining the glyph shape
        phonetic_hypothesis: Possible pronunciations based on linguistic analysis
        semantic_cluster: Pattern recognition grouping (0-9)
        hebrew_correlation: Similarity score to Hebrew characters (0-1)
        egyptian_correlation: Similarity score to Egyptian hieroglyphs (0-1)
    """
    
    symbol: str
    unicode_code: str
    frequency: float = 0.0
    geometric_pattern: List[Tuple[int, int]] = field(default_factory=list)
    phonetic_hypothesis: List[str] = field(default_factory=list)
    semantic_cluster: int = 0
    hebrew_correlation: float = 0.0
    egyptian_correlation: float = 0.0
    
    def __post_init__(self) -> None:
        """Validate glyph data after initialization."""
        if not self.symbol:
            raise ValueError("Glyph symbol cannot be empty")
        if not 0.0 <= self.frequency <= 1.0:
            raise ValueError("Frequency must be between 0 and 1")
        if not 0.0 <= self.hebrew_correlation <= 1.0:
            raise ValueError("Hebrew correlation must be between 0 and 1")
        if not 0.0 <= self.egyptian_correlation <= 1.0:
            raise ValueError("Egyptian correlation must be between 0 and 1")
    
    def to_dict(self) -> dict:
        """Convert glyph to dictionary representation."""
        return {
            "symbol": self.symbol,
            "unicode_code": self.unicode_code,
            "frequency": self.frequency,
            "geometric_pattern": self.geometric_pattern,
            "phonetic_hypothesis": self.phonetic_hypothesis,
            "semantic_cluster": self.semantic_cluster,
            "hebrew_correlation": self.hebrew_correlation,
            "egyptian_correlation": self.egyptian_correlation
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Glyph":
        """Create glyph from dictionary representation."""
        return cls(
            symbol=data["symbol"],
            unicode_code=data["unicode_code"],
            frequency=data.get("frequency", 0.0),
            geometric_pattern=[tuple(p) for p in data.get("geometric_pattern", [])],
            phonetic_hypothesis=data.get("phonetic_hypothesis", []),
            semantic_cluster=data.get("semantic_cluster", 0),
            hebrew_correlation=data.get("hebrew_correlation", 0.0),
            egyptian_correlation=data.get("egyptian_correlation", 0.0)
        )

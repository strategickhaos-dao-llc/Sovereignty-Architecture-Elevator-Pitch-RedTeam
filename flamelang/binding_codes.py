"""
FlameLang Binding Codes
Sacred numeric codes that bind glyphs to specific operational domains.

Binding Code System:
- [137]: Fire domain - Creation, ignition, transformation
- [666]: Water domain - Flow, adaptation, transformation  
- [777]: Earth domain - Structure, foundation, permanence
- [999]: Air domain - Communication, movement, distribution
- [1111]: Void domain - Meta-operations, transcendence, infinity
"""

from dataclasses import dataclass
from enum import Enum
from typing import Callable, Any


class BindingDomain(Enum):
    """The five binding code domains."""
    FIRE = 137
    WATER = 666
    EARTH = 777
    AIR = 999
    VOID = 1111


@dataclass
class BindingCode:
    """
    Represents a binding code with its domain properties.
    
    Each binding code defines:
    - A numeric identifier
    - An elemental domain
    - Frequency range bounds
    - Operational characteristics
    """
    
    code: int
    domain: BindingDomain
    name: str
    element: str
    whale_freq_start: float
    whale_freq_end: float
    piano_freq_start: float
    piano_freq_end: float
    operations: list[str]
    resonance_harmonic: int
    
    def contains_frequency(self, whale_freq: float = None, piano_freq: float = None) -> bool:
        """Check if a frequency falls within this binding code's range."""
        if whale_freq is not None:
            if not (self.whale_freq_start <= whale_freq <= self.whale_freq_end):
                return False
        if piano_freq is not None:
            if not (self.piano_freq_start <= piano_freq <= self.piano_freq_end):
                return False
        return True
    
    def __str__(self) -> str:
        return f"[{self.code}] {self.name} ({self.element})"


# Pre-defined binding codes with their frequency ranges
# Each code covers 8 glyphs (40 total / 5 codes = 8 each)
# Whale range: 5.87-6.44 Hz (0.57 Hz total, 0.114 Hz per code)
# Piano range: 27.5-4186 Hz

BINDING_CODES = {
    137: BindingCode(
        code=137,
        domain=BindingDomain.FIRE,
        name="IGNITION",
        element="Fire",
        whale_freq_start=5.870,
        whale_freq_end=5.984,
        piano_freq_start=27.5,
        piano_freq_end=860.0,
        operations=["IGNITE", "SPARK", "RADIATE", "STELLAR", "TRANSCEND", "ILLUMINATE", "MANIFEST", "ERUPT"],
        resonance_harmonic=1
    ),
    666: BindingCode(
        code=666,
        domain=BindingDomain.WATER,
        name="TRANSFORMATION",
        element="Water",
        whale_freq_start=5.984,
        whale_freq_end=6.098,
        piano_freq_start=860.0,
        piano_freq_end=1693.0,
        operations=["FLOW", "DROPLET", "VORTEX", "CRYSTALLIZE", "PRECIPITATE", "SPECTRUM", "COMPRESS", "DIVINE"],
        resonance_harmonic=2
    ),
    777: BindingCode(
        code=777,
        domain=BindingDomain.EARTH,
        name="FOUNDATION",
        element="Earth",
        whale_freq_start=6.098,
        whale_freq_end=6.212,
        piano_freq_start=1693.0,
        piano_freq_end=2526.0,
        operations=["GROUND", "ANCHOR", "ROOT", "SOLIDIFY", "ELEVATE", "GROW", "HARVEST", "RELEASE"],
        resonance_harmonic=3
    ),
    999: BindingCode(
        code=999,
        domain=BindingDomain.AIR,
        name="TRANSMISSION",
        element="Air",
        whale_freq_start=6.212,
        whale_freq_end=6.326,
        piano_freq_start=2526.0,
        piano_freq_end=3359.0,
        operations=["TRANSMIT", "BREATHE", "SUSPEND", "SCATTER", "LIFT", "TRANSFORM", "PEACE", "SOAR"],
        resonance_harmonic=5
    ),
    1111: BindingCode(
        code=1111,
        domain=BindingDomain.VOID,
        name="TRANSCENDENCE",
        element="Void",
        whale_freq_start=6.326,
        whale_freq_end=6.440,
        piano_freq_start=3359.0,
        piano_freq_end=4186.0,
        operations=["VOID", "ABSORB", "PORTAL", "INFINITE", "OMEGA", "PHI", "PSI", "DELTA"],
        resonance_harmonic=8
    )
}


def get_binding_code(code: int) -> BindingCode | None:
    """Get a binding code by its numeric value."""
    return BINDING_CODES.get(code)


def get_binding_code_for_frequency(whale_freq: float = None, piano_freq: float = None) -> BindingCode | None:
    """Find the binding code that contains the given frequency."""
    for bc in BINDING_CODES.values():
        if bc.contains_frequency(whale_freq, piano_freq):
            return bc
    return None


def all_binding_codes() -> list[BindingCode]:
    """Return all binding codes."""
    return list(BINDING_CODES.values())

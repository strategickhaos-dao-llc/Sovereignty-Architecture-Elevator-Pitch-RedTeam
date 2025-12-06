"""
Whale Weaver - Frequency Synthesis Module
Maps whale pulse frequencies (5.87-6.44 Hz) to piano keys (27.5-4186 Hz).

This is a cross-domain resonance mapping system that converts
biological/natural frequencies into musical notation.
"""

__version__ = "1.0.0"
__author__ = "StrategicKhaos Swarm Intelligence"

from .synthesize import (
    FrequencySynthesizer,
    WhaleFrequencyMapper,
    PianoFrequencyMapper,
    ResonanceMapper,
)

__all__ = [
    "FrequencySynthesizer",
    "WhaleFrequencyMapper", 
    "PianoFrequencyMapper",
    "ResonanceMapper",
]

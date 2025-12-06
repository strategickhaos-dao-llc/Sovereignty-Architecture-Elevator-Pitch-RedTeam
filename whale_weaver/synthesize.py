"""
Whale Weaver Frequency Synthesis
Maps whale pulse frequencies to 88 piano keys for cross-domain resonance.

Frequency Ranges:
- Whale pulses: 5.87-6.44 Hz (biological infrasound)
- Piano keys: 27.5-4186 Hz (A0 to C8)
"""

import json
import logging
from pathlib import Path
from dataclasses import dataclass, field
from typing import Any
import numpy as np

logger = logging.getLogger(__name__)


# Piano key configuration (88 keys: A0 to C8)
PIANO_KEYS = 88
PIANO_FREQ_MIN = 27.5   # A0
PIANO_FREQ_MAX = 4186.0  # C8

# Whale pulse frequency range (infrasound)
WHALE_FREQ_MIN = 5.87
WHALE_FREQ_MAX = 6.44


@dataclass
class FrequencyMapping:
    """Represents a mapping between two frequency domains."""
    
    key_index: int  # 0-87 for piano keys
    note_name: str  # e.g., "A0", "C4", "C8"
    whale_freq: float  # Hz - source whale frequency
    piano_freq: float  # Hz - target piano frequency
    resonance_ratio: float  # piano_freq / whale_freq
    octave: int
    
    def to_dict(self) -> dict:
        """Convert to dictionary representation."""
        return {
            "key_index": self.key_index,
            "note_name": self.note_name,
            "whale_freq": round(self.whale_freq, 4),
            "piano_freq": round(self.piano_freq, 4),
            "resonance_ratio": round(self.resonance_ratio, 4),
            "octave": self.octave
        }


class WhaleFrequencyMapper:
    """Maps whale pulse frequencies across a specified range."""
    
    def __init__(self, min_freq: float = WHALE_FREQ_MIN, max_freq: float = WHALE_FREQ_MAX):
        """
        Initialize whale frequency mapper.
        
        Args:
            min_freq: Minimum whale frequency (Hz)
            max_freq: Maximum whale frequency (Hz)
        """
        self.min_freq = min_freq
        self.max_freq = max_freq
        self.range = max_freq - min_freq
    
    def get_frequency_array(self, num_points: int = PIANO_KEYS) -> np.ndarray:
        """Generate array of whale frequencies mapped to num_points."""
        return np.linspace(self.min_freq, self.max_freq, num_points)
    
    def normalize(self, freq: float) -> float:
        """Normalize a whale frequency to 0-1 range."""
        if self.range == 0:
            return 0.0
        return (freq - self.min_freq) / self.range
    
    def denormalize(self, normalized: float) -> float:
        """Convert normalized value back to whale frequency."""
        return self.min_freq + (normalized * self.range)


class PianoFrequencyMapper:
    """Maps piano key frequencies using equal temperament."""
    
    # Note names for one octave
    NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    
    # A4 reference frequency (440 Hz standard)
    A4_FREQ = 440.0
    A4_KEY_INDEX = 48  # A4 is the 49th key (index 48)
    
    def __init__(self, num_keys: int = PIANO_KEYS):
        """
        Initialize piano frequency mapper.
        
        Args:
            num_keys: Number of piano keys (standard: 88)
        """
        self.num_keys = num_keys
        self.frequencies = self._calculate_frequencies()
    
    def _calculate_frequencies(self) -> np.ndarray:
        """Calculate frequencies for all piano keys using equal temperament."""
        frequencies = np.zeros(self.num_keys)
        for i in range(self.num_keys):
            # Equal temperament: f = f0 * 2^(n/12)
            # Where n is semitones from A4
            semitones_from_a4 = i - self.A4_KEY_INDEX
            frequencies[i] = self.A4_FREQ * (2 ** (semitones_from_a4 / 12))
        return frequencies
    
    def get_frequency(self, key_index: int) -> float:
        """Get frequency for a specific key index (0-87)."""
        if 0 <= key_index < self.num_keys:
            return self.frequencies[key_index]
        raise ValueError(f"Key index {key_index} out of range (0-{self.num_keys-1})")
    
    def get_note_name(self, key_index: int) -> str:
        """Get note name for a key index (e.g., 'A0', 'C4')."""
        # A0 is key 0, so offset is 9 from C
        note_offset = (key_index + 9) % 12  # +9 because A is 9 semitones from C
        octave = (key_index + 9) // 12  # Octave number
        return f"{self.NOTE_NAMES[note_offset]}{octave}"
    
    def get_octave(self, key_index: int) -> int:
        """Get octave number for a key index."""
        return (key_index + 9) // 12
    
    def find_nearest_key(self, frequency: float) -> int:
        """Find the nearest piano key for a given frequency."""
        if frequency <= 0:
            return 0
        differences = np.abs(self.frequencies - frequency)
        return int(np.argmin(differences))


class ResonanceMapper:
    """Maps resonance relationships between whale and piano frequencies."""
    
    def __init__(self):
        """Initialize the resonance mapper with whale and piano mappers."""
        self.whale_mapper = WhaleFrequencyMapper()
        self.piano_mapper = PianoFrequencyMapper()
    
    def calculate_resonance_ratio(self, whale_freq: float, piano_freq: float) -> float:
        """Calculate the resonance ratio between frequencies."""
        if whale_freq == 0:
            return 0.0
        return piano_freq / whale_freq
    
    def find_harmonic_relationship(self, whale_freq: float, piano_freq: float) -> dict:
        """Analyze harmonic relationship between frequencies."""
        ratio = self.calculate_resonance_ratio(whale_freq, piano_freq)
        
        # Find nearest simple ratio
        simple_ratios = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 16, 24, 32, 64, 128]
        nearest_ratio = min(simple_ratios, key=lambda x: abs(x - ratio))
        deviation = abs(ratio - nearest_ratio) / nearest_ratio * 100
        
        return {
            "exact_ratio": ratio,
            "nearest_harmonic": nearest_ratio,
            "deviation_percent": round(deviation, 2),
            "is_harmonic": deviation < 5.0  # Within 5% of simple ratio
        }


class FrequencySynthesizer:
    """
    Main synthesizer class that maps whale pulses to piano frequencies.
    Creates a complete 88-key mapping with resonance data.
    """
    
    def __init__(self):
        """Initialize the frequency synthesizer."""
        self.whale_mapper = WhaleFrequencyMapper()
        self.piano_mapper = PianoFrequencyMapper()
        self.resonance_mapper = ResonanceMapper()
        self._mappings: list[FrequencyMapping] = []
        self._generate_mappings()
    
    def _generate_mappings(self) -> None:
        """Generate all 88 frequency mappings."""
        whale_freqs = self.whale_mapper.get_frequency_array(PIANO_KEYS)
        
        for i in range(PIANO_KEYS):
            whale_freq = float(whale_freqs[i])
            piano_freq = self.piano_mapper.get_frequency(i)
            note_name = self.piano_mapper.get_note_name(i)
            octave = self.piano_mapper.get_octave(i)
            ratio = self.resonance_mapper.calculate_resonance_ratio(whale_freq, piano_freq)
            
            mapping = FrequencyMapping(
                key_index=i,
                note_name=note_name,
                whale_freq=whale_freq,
                piano_freq=piano_freq,
                resonance_ratio=ratio,
                octave=octave
            )
            self._mappings.append(mapping)
    
    def get_mapping(self, key_index: int) -> FrequencyMapping:
        """Get mapping for a specific piano key."""
        if 0 <= key_index < PIANO_KEYS:
            return self._mappings[key_index]
        raise ValueError(f"Key index {key_index} out of range")
    
    def get_mapping_by_note(self, note_name: str) -> FrequencyMapping | None:
        """Get mapping by note name (e.g., 'A4', 'C5')."""
        for mapping in self._mappings:
            if mapping.note_name == note_name:
                return mapping
        return None
    
    def whale_to_piano(self, whale_freq: float) -> FrequencyMapping:
        """Convert a whale frequency to the nearest piano key mapping."""
        # Normalize whale frequency to find position
        normalized = self.whale_mapper.normalize(whale_freq)
        # Clamp to valid range
        normalized = max(0.0, min(1.0, normalized))
        # Calculate key index
        key_index = int(normalized * (PIANO_KEYS - 1))
        return self._mappings[key_index]
    
    def piano_to_whale(self, piano_freq: float) -> FrequencyMapping:
        """Convert a piano frequency to nearest whale pulse mapping."""
        key_index = self.piano_mapper.find_nearest_key(piano_freq)
        return self._mappings[key_index]
    
    def get_all_mappings(self) -> list[FrequencyMapping]:
        """Return all 88 frequency mappings."""
        return self._mappings.copy()
    
    def get_mappings_by_octave(self, octave: int) -> list[FrequencyMapping]:
        """Get all mappings in a specific octave."""
        return [m for m in self._mappings if m.octave == octave]
    
    def export_to_dict(self) -> dict:
        """Export all mappings as a dictionary."""
        return {
            "version": "1.0.0",
            "total_keys": PIANO_KEYS,
            "whale_range": {
                "min": WHALE_FREQ_MIN,
                "max": WHALE_FREQ_MAX,
                "unit": "Hz"
            },
            "piano_range": {
                "min": PIANO_FREQ_MIN,
                "max": PIANO_FREQ_MAX,
                "unit": "Hz"
            },
            "mappings": [m.to_dict() for m in self._mappings]
        }
    
    def export_to_json(self, filepath: str | Path = None) -> str:
        """Export mappings to JSON format."""
        data = self.export_to_dict()
        json_str = json.dumps(data, indent=2)
        
        if filepath:
            path = Path(filepath)
            path.write_text(json_str)
            logger.info(f"Exported frequency mappings to {filepath}")
        
        return json_str
    
    def get_whale_frequency_array(self, num_points: int = PIANO_KEYS) -> np.ndarray:
        """
        Generate array of whale frequencies.
        
        Args:
            num_points: Number of frequency points (default: 88 for piano keys)
            
        Returns:
            NumPy array of whale frequencies (5.87-6.44 Hz range)
        """
        return np.linspace(WHALE_FREQ_MIN, WHALE_FREQ_MAX, num_points)
    
    def get_piano_frequency_array(self, num_points: int = PIANO_KEYS) -> np.ndarray:
        """
        Generate array of piano frequencies.
        
        Args:
            num_points: Number of frequency points (default: 88 for piano keys)
            
        Returns:
            NumPy array of piano frequencies (27.5-4186 Hz range)
        """
        return np.linspace(PIANO_FREQ_MIN, PIANO_FREQ_MAX, num_points)

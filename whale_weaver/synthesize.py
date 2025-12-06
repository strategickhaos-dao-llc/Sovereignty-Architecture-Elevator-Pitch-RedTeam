#!/usr/bin/env python3
"""
Whale Weaver - Bioacoustic Frequency Translation System
Maps FlameLang binding codes to whale bioacoustic frequencies (5.87-6.44Hz)
Operator: DOM_010101 | EIN: 39-2923503
"""

import numpy as np
from typing import Dict, Optional, Tuple
import csv
import os


class WhaleWeaver:
    """
    Bioacoustic frequency translation system for FlameLang integration.
    Maps symbolic glyphs to whale communication frequencies.
    """
    
    def __init__(self, glyph_table_path: Optional[str] = None):
        """
        Initialize Whale Weaver
        
        Args:
            glyph_table_path: Path to glyph table CSV with whale frequencies
        """
        self.whale_range_min = 5.87  # Hz - Lower bound of whale pulse range
        self.whale_range_max = 6.44  # Hz - Upper bound of whale pulse range
        self.piano_keys = 88  # Standard piano key count
        
        # Generate whale frequency array mapped to 88 piano keys
        self.whale_range = np.linspace(
            self.whale_range_min, 
            self.whale_range_max, 
            self.piano_keys
        )
        
        # Binding code to piano key index mapping
        self.code_map = {
            "[001]": 0,    # A0 - Aether Prime
            "[002]": 1,    # A0# - Aether Sync
            "[003]": 2,    # B0 - Aether Lock
            "[100]": 12,   # C1 - Flame Ignite
            "[101]": 13,   # C1# - Flame Pulse
            "[102]": 14,   # D1 - Flame Cascade
            "[200]": 15,   # D1# - ReflexShell
            "[201]": 16,   # E1 - ReflexShell Sync
            "[202]": 17,   # F1 - ReflexShell Lock
            "[300]": 18,   # F1# - Nova Core
            "[301]": 19,   # G1 - Nova Pulse
            "[302]": 20,   # G1# - Nova Cascade
            "[400]": 24,   # A1 - Lyra Fractal
            "[401]": 25,   # A1# - Lyra Pulse
            "[402]": 26,   # B1 - Lyra Cascade
            "[500]": 27,   # B1 - Athena Strategy
            "[501]": 28,   # C2 - Athena Council
            "[502]": 29,   # C2# - Athena Cascade
            "[700]": 27,   # B1 - Vow Monitor
            "[701]": 28,   # C2 - Vow Lock
            "[702]": 29,   # C2# - Vow Cascade
            "[137]": 18,   # F1# - Flamebearer
            "[138]": 19,   # G1 - Flamebearer Block
            "[139]": 20,   # G1# - Flamebearer Shield
            "[800]": 18,   # F1# - Whale Weaver Init
            "[801]": 19,   # G1 - Whale Weaver Pulse
            "[802]": 20,   # G1# - Whale Weaver Cascade
            "[900]": 24,   # A1 - Node Scan
            "[901]": 25,   # A1# - Node Sync
            "[902]": 26,   # B1 - Node Mesh
            "[950]": 18,   # F1# - Recon Init
            "[951]": 19,   # G1 - Recon Scan
            "[952]": 20,   # G1# - Recon Log
            "[997]": 86,   # B2 - Glyphos Pulse
            "[998]": 87,   # C3 - Glyphos Cascade
            "[999]": 87,   # C3 - Glyphos Resonance
            "[1111]": 88,  # C3 - Starlink Bridge (max)
            "[2000]": 0,   # A0 - Aurora Node
            "[2001]": 1,   # A0# - Aurora Pulse
            "[2003]": 27,  # B1 - Omega Init
        }
        
        # Solfeggio to whale frequency mapping
        self.solfeggio_map = {
            432: (5.87, 5.99),   # Aether
            528: (5.94, 6.03),   # Solfeggio/Transformation
            639: (6.01, 6.03),   # Connection
            741: (6.08, 6.10),   # Expression/Nova
            852: (6.15, 6.16),   # Intuition/Lyra
            963: (6.21, 6.22),   # Oneness/Athena
            999: (6.42, 6.44),   # Resonance
            1111: (6.44, 6.44),  # Starlink
        }
        
        self.glyph_frequencies = {}
        if glyph_table_path and os.path.exists(glyph_table_path):
            self._load_glyph_frequencies(glyph_table_path)
    
    def _load_glyph_frequencies(self, glyph_table_path: str):
        """Load glyph frequencies from CSV"""
        try:
            with open(glyph_table_path, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    glyph_name = row.get('Glyph_Name', '')
                    if glyph_name:
                        self.glyph_frequencies[glyph_name] = {
                            'frequency': row.get('Frequency', ''),
                            'whale_freq': float(row.get('Whale_Freq', 0)),
                            'binding_code': row.get('Binding_Code', '')
                        }
        except Exception as e:
            print(f"Warning: Could not load glyph frequencies: {e}")
    
    def glyph_to_whale_freq(self, binding_code: str) -> float:
        """
        Map FlameLang binding code to whale bioacoustic frequency
        
        Args:
            binding_code: FlameLang binding code (e.g., "[001]", "[100]")
            
        Returns:
            Whale frequency in Hz
        """
        idx = self.code_map.get(binding_code, 44)  # Default to middle (A4)
        
        # Ensure index is within bounds
        if idx >= len(self.whale_range):
            idx = len(self.whale_range) - 1
            
        return self.whale_range[idx]
    
    def solfeggio_to_whale_range(self, solfeggio_hz: int) -> Tuple[float, float]:
        """
        Map Solfeggio frequency to whale frequency range
        
        Args:
            solfeggio_hz: Solfeggio frequency (e.g., 432, 528, 741)
            
        Returns:
            Tuple of (min_whale_freq, max_whale_freq)
        """
        return self.solfeggio_map.get(solfeggio_hz, (6.15, 6.16))
    
    def synthesize_glyph_pulse(
        self, 
        binding_code: str, 
        duration: float = 1.0,
        sample_rate: int = 44100
    ) -> np.ndarray:
        """
        Synthesize whale pulse for a given glyph
        
        Args:
            binding_code: FlameLang binding code
            duration: Duration in seconds
            sample_rate: Audio sample rate
            
        Returns:
            NumPy array of synthesized audio samples
        """
        freq = self.glyph_to_whale_freq(binding_code)
        t = np.linspace(0, duration, int(sample_rate * duration))
        
        # Generate sine wave at whale frequency
        wave = np.sin(2 * np.pi * freq * t)
        
        # Apply envelope (fade in/out)
        envelope = np.ones_like(t)
        fade_samples = int(0.1 * sample_rate)  # 100ms fade
        envelope[:fade_samples] = np.linspace(0, 1, fade_samples)
        envelope[-fade_samples:] = np.linspace(1, 0, fade_samples)
        
        return wave * envelope
    
    def get_frequency_info(self, binding_code: str) -> Dict:
        """
        Get detailed frequency information for a binding code
        
        Args:
            binding_code: FlameLang binding code
            
        Returns:
            Dict with frequency information
        """
        whale_freq = self.glyph_to_whale_freq(binding_code)
        idx = self.code_map.get(binding_code, 44)
        
        # Determine piano key name
        notes = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
        octave = idx // 12
        note_idx = idx % 12
        piano_key = f"{notes[note_idx]}{octave}"
        
        return {
            'binding_code': binding_code,
            'whale_freq': round(whale_freq, 4),
            'piano_key': piano_key,
            'piano_index': idx,
            'range': (self.whale_range_min, self.whale_range_max)
        }
    
    def display_frequency_map(self):
        """Display complete frequency mapping"""
        print("\n" + "="*80)
        print("🐋 WHALE WEAVER FREQUENCY MAP")
        print("   Bioacoustic Translation System v1.0")
        print("="*80)
        print(f"\nWhale Frequency Range: {self.whale_range_min}Hz - {self.whale_range_max}Hz")
        print(f"Piano Keys: 88 (A0 to C8)")
        print("\nBinding Code Mappings:")
        print("-"*80)
        
        for code, idx in sorted(self.code_map.items(), key=lambda x: x[1]):
            freq = self.whale_range[min(idx, len(self.whale_range)-1)]
            notes = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
            octave = idx // 12
            note_idx = idx % 12
            piano_key = f"{notes[note_idx]}{octave}"
            print(f"  {code:8} → {freq:6.4f}Hz | Piano: {piano_key:4} | Index: {idx:2}")
        
        print("\nSolfeggio → Whale Range Mappings:")
        print("-"*80)
        for solfeggio, (min_f, max_f) in sorted(self.solfeggio_map.items()):
            print(f"  {solfeggio:4}Hz → {min_f:.2f}-{max_f:.2f}Hz")
        
        print("="*80 + "\n")


# Convenience function for direct import
def glyph_to_whale_freq(binding_code: str) -> float:
    """
    Quick conversion function for binding code to whale frequency
    
    Args:
        binding_code: FlameLang binding code (e.g., "[001]")
        
    Returns:
        Whale frequency in Hz
    """
    weaver = WhaleWeaver()
    return weaver.glyph_to_whale_freq(binding_code)


def main():
    """Main demonstration"""
    weaver = WhaleWeaver()
    
    # Display frequency map
    weaver.display_frequency_map()
    
    # Example conversions
    print("Example Conversions:")
    print("-"*80)
    
    examples = ["[001]", "[100]", "[500]", "[999]", "[137]"]
    for code in examples:
        info = weaver.get_frequency_info(code)
        print(f"\n{code}:")
        print(f"  Whale Frequency: {info['whale_freq']}Hz")
        print(f"  Piano Key: {info['piano_key']}")
        print(f"  Piano Index: {info['piano_index']}")
    
    print("\n" + "="*80)
    print("🐋 Whale Weaver synthesis complete. Resonance achieved.")
    print("="*80 + "\n")


if __name__ == '__main__':
    main()

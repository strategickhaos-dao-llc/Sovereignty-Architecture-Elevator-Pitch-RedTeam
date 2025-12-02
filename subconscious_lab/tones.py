#!/usr/bin/env python3
"""
SubconsciousLab Audio Engine

Generates binaural beats and isochronic tones for subconscious entrainment.

Binaural beats: Two slightly different frequencies in each ear create a
perceived beat at the difference frequency in the brain.

Isochronic tones: Regular beats of a single tone, turned on and off at
a specific rate.
"""

import json
import wave
from pathlib import Path

import numpy as np

SAMPLE_RATE = 44100


def generate_binaural(
    duration_sec: float,
    carrier_hz: float,
    beat_hz: float,
    volume: float = 0.3
) -> np.ndarray:
    """
    Generate a stereo binaural beat.

    Args:
        duration_sec: Duration in seconds
        carrier_hz: Base carrier frequency in Hz
        beat_hz: Desired beat frequency (difference between L/R channels)
        volume: Output volume (0.0 to 1.0)

    Returns:
        Stereo numpy array of shape (samples, 2)
    """
    t = np.linspace(0, duration_sec, int(SAMPLE_RATE * duration_sec), endpoint=False)
    left = np.sin(2 * np.pi * (carrier_hz - beat_hz / 2) * t)
    right = np.sin(2 * np.pi * (carrier_hz + beat_hz / 2) * t)
    stereo = np.vstack((left, right)).T
    stereo *= volume
    return stereo


def generate_isochronic(
    duration_sec: float,
    carrier_hz: float,
    beat_hz: float,
    volume: float = 0.3
) -> np.ndarray:
    """
    Generate a stereo isochronic tone.

    Args:
        duration_sec: Duration in seconds
        carrier_hz: Carrier frequency in Hz
        beat_hz: On/off modulation frequency in Hz
        volume: Output volume (0.0 to 1.0)

    Returns:
        Stereo numpy array of shape (samples, 2)
    """
    t = np.linspace(0, duration_sec, int(SAMPLE_RATE * duration_sec), endpoint=False)
    tone = np.sin(2 * np.pi * carrier_hz * t)
    # Amplitude modulation using square wave
    mod = 0.5 * (1 + np.sign(np.sin(2 * np.pi * beat_hz * t)))
    mono = tone * mod * volume
    # Duplicate to stereo
    stereo = np.vstack((mono, mono)).T
    return stereo


def save_wav_stereo(filename: str, data: np.ndarray) -> None:
    """
    Save stereo audio data to a WAV file.

    Args:
        filename: Output file path
        data: Stereo numpy array of shape (samples, 2)
    """
    # Ensure within [-1, 1]
    data = np.clip(data, -1, 1)
    # Convert to 16-bit PCM
    data_int16 = np.int16(data * 32767)
    with wave.open(filename, 'w') as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)  # 16-bit
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(data_int16.tobytes())


def load_frequency_map(config_path: str | None = None) -> dict:
    """
    Load the emotion-to-frequency mapping configuration.

    Args:
        config_path: Path to JSON config file (defaults to frequency_map.json)

    Returns:
        Dictionary of emotion presets

    Raises:
        FileNotFoundError: If the configuration file cannot be found
    """
    if config_path is None:
        config_path = Path(__file__).parent / "frequency_map.json"
    try:
        with open(config_path) as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Frequency map configuration not found at: {config_path}"
        )


def generate_preset(
    preset_name: str,
    duration_sec: float = 600,
    output_dir: str | None = None,
    config_path: str | None = None
) -> str:
    """
    Generate an audio file from a preset name.

    Args:
        preset_name: Name of the preset from frequency_map.json
        duration_sec: Duration in seconds (default: 600 = 10 minutes)
        output_dir: Output directory (default: current directory)
        config_path: Path to config file

    Returns:
        Path to the generated WAV file
    """
    presets = load_frequency_map(config_path)

    if preset_name not in presets:
        available = ", ".join(presets.keys())
        raise ValueError(f"Unknown preset '{preset_name}'. Available: {available}")

    preset = presets[preset_name]
    tone_type = preset["type"]
    carrier_hz = preset["carrier_hz"]
    beat_hz = preset["beat_hz"]

    if tone_type == "binaural":
        audio_data = generate_binaural(duration_sec, carrier_hz, beat_hz)
    elif tone_type == "isochronic":
        audio_data = generate_isochronic(duration_sec, carrier_hz, beat_hz)
    else:
        raise ValueError(f"Unknown tone type: {tone_type}")

    # Build output filename
    output_filename = f"{preset_name}_{tone_type}.wav"
    if output_dir:
        output_path = Path(output_dir) / output_filename
    else:
        output_path = Path(output_filename)

    save_wav_stereo(str(output_path), audio_data)
    return str(output_path)


def list_presets(config_path: str | None = None) -> None:
    """Print all available presets with their descriptions."""
    presets = load_frequency_map(config_path)
    print("\n🎧 Available Frequency Presets:\n")
    for name, config in presets.items():
        print(f"  [{name}]")
        print(f"    Type: {config['type']}")
        print(f"    Carrier: {config['carrier_hz']} Hz")
        print(f"    Beat: {config['beat_hz']} Hz")
        print(f"    {config['description']}")
        print()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="SubconsciousLab Audio Engine - Generate binaural beats and isochronic tones"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all available presets"
    )
    parser.add_argument(
        "--preset",
        type=str,
        help="Generate audio for a specific preset"
    )
    parser.add_argument(
        "--duration",
        type=int,
        default=600,
        help="Duration in seconds (default: 600 = 10 minutes)"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        help="Output directory for generated files"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Generate all presets"
    )

    args = parser.parse_args()

    if args.list:
        list_presets()
    elif args.preset:
        output_file = generate_preset(args.preset, args.duration, args.output_dir)
        print(f"Generated: {output_file}")
    elif args.all:
        presets = load_frequency_map()
        print("Generating all presets...")
        for preset_name in presets:
            output_file = generate_preset(preset_name, args.duration, args.output_dir)
            print(f"  Generated: {output_file}")
        print("Done!")
    else:
        # Default: generate example files
        print("SubconsciousLab Audio Engine")
        print("============================\n")
        print("Generating example audio files...\n")

        duration = 300  # 5 minutes for examples

        # Calm focus binaural
        binaural = generate_binaural(duration_sec=duration, carrier_hz=220, beat_hz=10.0)
        save_wav_stereo("calm_focus_binaural.wav", binaural)
        print("✓ calm_focus_binaural.wav (5 min, 220 Hz carrier, 10 Hz beat)")

        # Feral god mode isochronic
        isochronic = generate_isochronic(duration_sec=duration, carrier_hz=400, beat_hz=14.0)
        save_wav_stereo("feral_god_mode_isochronic.wav", isochronic)
        print("✓ feral_god_mode_isochronic.wav (5 min, 400 Hz carrier, 14 Hz beat)")

        print("\n🎧 Play these with headphones for binaural beats!")
        print("   Use --list to see all available presets")
        print("   Use --preset <name> to generate a specific preset")

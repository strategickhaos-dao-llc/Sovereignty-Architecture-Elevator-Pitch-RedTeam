#!/usr/bin/env python3
"""
SubconsciousLab Session Protocol Runner

Coordinates audio (binaural beats / isochronic tones) with visual
speed-reading (RSVP) for integrated subconscious training sessions.

Session Flow:
1. Choose state/preset (calm_focus, feral_god_mode, etc.)
2. Generate audio file (if not already cached)
3. Start audio playback
4. Begin RSVP visual stream
5. Optional: Log session for tracking

Usage:
    python session.py --preset calm_focus --wpm 500 --duration 10

Physical drills to combine with sessions:
- Juggling
- Rubik's cube
- Ambidextrous writing
- Peripheral vision exercises
"""

import json
import os
import subprocess
import sys
import threading
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

# Local imports
from tones import generate_preset, list_presets, load_frequency_map
from rsvp import run_session as run_rsvp_session, DEFAULT_TEXT


@dataclass
class SessionConfig:
    """Configuration for a subconscious training session."""
    preset: str
    duration_minutes: int = 10
    wpm: int = 400
    chunk_size: int = 1
    text_file: str | None = None
    output_dir: str = "."
    log_session: bool = True


def play_audio_file(filepath: str, duration_seconds: float) -> subprocess.Popen | None:
    """
    Start audio playback in background.

    Tries multiple audio players in order of preference.
    Returns the subprocess for later termination.
    """
    players = [
        # Cross-platform players
        ["ffplay", "-nodisp", "-autoexit", "-t", str(int(duration_seconds)), filepath],
        ["mpv", "--no-video", f"--length={int(duration_seconds)}", filepath],
        ["vlc", "--intf", "dummy", "--play-and-exit", filepath],
        # macOS
        ["afplay", filepath],
        # Linux with ALSA
        ["aplay", filepath],
    ]

    for player_cmd in players:
        try:
            # Check if player exists
            check_cmd = player_cmd[0]
            result = subprocess.run(
                ["which", check_cmd],
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                continue

            # Start player
            process = subprocess.Popen(
                player_cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            return process
        except (FileNotFoundError, OSError):
            continue

    return None


def get_session_log_path() -> Path:
    """Get the path to the session log file."""
    return Path(__file__).parent / "session_log.json"


def log_session(config: SessionConfig, notes: str = "") -> None:
    """Log a session to the session log file."""
    log_path = get_session_log_path()

    # Load existing log or create new
    if log_path.exists():
        with open(log_path) as f:
            log_data = json.load(f)
    else:
        log_data = {"sessions": []}

    # Add new session entry
    session_entry = {
        "timestamp": datetime.now().isoformat(),
        "preset": config.preset,
        "duration_minutes": config.duration_minutes,
        "wpm": config.wpm,
        "chunk_size": config.chunk_size,
        "text_file": config.text_file,
        "notes": notes
    }
    log_data["sessions"].append(session_entry)

    # Save updated log
    with open(log_path, "w") as f:
        json.dump(log_data, f, indent=2)


def show_session_history() -> None:
    """Display previous session history."""
    log_path = get_session_log_path()

    if not log_path.exists():
        print("No session history found.")
        return

    with open(log_path) as f:
        log_data = json.load(f)

    sessions = log_data.get("sessions", [])
    if not sessions:
        print("No sessions logged yet.")
        return

    print("\n📊 Session History\n")
    print("-" * 60)

    for i, session in enumerate(sessions[-10:], 1):  # Show last 10
        ts = session.get("timestamp", "Unknown")
        preset = session.get("preset", "Unknown")
        duration = session.get("duration_minutes", 0)
        wpm = session.get("wpm", 0)
        notes = session.get("notes", "")

        print(f"{i}. [{ts[:19]}] {preset}")
        print(f"   Duration: {duration}min | WPM: {wpm}")
        if notes:
            print(f"   Notes: {notes}")
        print()


def run_integrated_session(config: SessionConfig) -> None:
    """
    Run an integrated subconscious training session.

    This coordinates audio generation/playback with RSVP visual stream.
    """
    presets = load_frequency_map()

    if config.preset not in presets:
        available = ", ".join(presets.keys())
        print(f"Unknown preset: {config.preset}")
        print(f"Available: {available}")
        return

    preset_info = presets[config.preset]
    duration_seconds = config.duration_minutes * 60

    # Clear screen and show session info
    os.system('cls' if os.name == 'nt' else 'clear')

    print("=" * 50)
    print("🧠 SubconsciousLab Training Session")
    print("=" * 50)
    print()
    print(f"Preset: {config.preset}")
    print(f"Type: {preset_info['type']}")
    print(f"Carrier: {preset_info['carrier_hz']} Hz")
    print(f"Beat: {preset_info['beat_hz']} Hz")
    print(f"Description: {preset_info['description']}")
    print()
    print(f"Duration: {config.duration_minutes} minutes")
    print(f"RSVP Speed: {config.wpm} WPM")
    print()
    print("-" * 50)
    print()
    print("Session Protocol:")
    print("1. Find a comfortable position")
    print("2. Put on headphones (required for binaural beats)")
    print("3. Relax your eyes - soft focus")
    print("4. Let the rhythm entrain your system")
    print("5. Optional: add physical drills (juggling, cube, etc.)")
    print()
    print("Press Enter to begin, or Ctrl+C to cancel...")

    try:
        input()
    except KeyboardInterrupt:
        print("\nSession cancelled.")
        return

    # Generate audio file
    print("\n🎵 Generating audio...")
    audio_file = generate_preset(
        config.preset,
        duration_sec=duration_seconds,
        output_dir=config.output_dir
    )
    print(f"   Generated: {audio_file}")

    # Start audio playback
    print("\n🔊 Starting audio playback...")
    audio_process = play_audio_file(audio_file, duration_seconds)

    if audio_process is None:
        print("   ⚠️  No audio player found. Install ffplay, mpv, or vlc.")
        print("   Continuing with visual-only session...")
        print(f"   Audio file available at: {audio_file}")
    else:
        print("   Audio playing in background...")

    # Small delay before RSVP
    time.sleep(2)

    # Run RSVP session
    print("\n📖 Starting RSVP stream...")
    time.sleep(1)

    try:
        # Load text
        if config.text_file:
            with open(config.text_file) as f:
                text = f.read()
        else:
            text = DEFAULT_TEXT

        run_rsvp_session(
            text=text,
            wpm=config.wpm,
            chunk_size=config.chunk_size,
            countdown=3
        )
    except KeyboardInterrupt:
        print("\n\nSession interrupted.")
    finally:
        # Clean up audio
        if audio_process:
            audio_process.terminate()
            audio_process.wait()

    # Log session
    if config.log_session:
        print("\n📝 Session complete!")
        notes = input("Any notes about this session? (Enter to skip): ")
        log_session(config, notes)
        print("Session logged.")


def quick_session(preset: str = "calm_focus") -> None:
    """Run a quick 5-minute session with defaults."""
    config = SessionConfig(
        preset=preset,
        duration_minutes=5,
        wpm=400
    )
    run_integrated_session(config)


def main():
    """Main entry point with CLI interface."""
    import argparse

    parser = argparse.ArgumentParser(
        description="SubconsciousLab Session Protocol Runner"
    )
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Run session command
    run_parser = subparsers.add_parser("run", help="Run a training session")
    run_parser.add_argument(
        "--preset",
        type=str,
        default="calm_focus",
        help="Frequency preset to use (default: calm_focus)"
    )
    run_parser.add_argument(
        "--duration",
        type=int,
        default=10,
        help="Session duration in minutes (default: 10)"
    )
    run_parser.add_argument(
        "--wpm",
        type=int,
        default=400,
        help="RSVP words per minute (default: 400)"
    )
    run_parser.add_argument(
        "--chunk",
        type=int,
        default=1,
        help="RSVP chunk size (default: 1)"
    )
    run_parser.add_argument(
        "--text-file",
        type=str,
        help="Path to text file for RSVP"
    )
    run_parser.add_argument(
        "--output-dir",
        type=str,
        default=".",
        help="Directory for generated audio files"
    )
    run_parser.add_argument(
        "--no-log",
        action="store_true",
        help="Don't log this session"
    )

    # List presets command
    subparsers.add_parser("presets", help="List available frequency presets")

    # History command
    subparsers.add_parser("history", help="Show session history")

    # Quick session command
    quick_parser = subparsers.add_parser("quick", help="Run a quick 5-minute session")
    quick_parser.add_argument(
        "--preset",
        type=str,
        default="calm_focus",
        help="Preset to use (default: calm_focus)"
    )

    args = parser.parse_args()

    if args.command == "run":
        config = SessionConfig(
            preset=args.preset,
            duration_minutes=args.duration,
            wpm=args.wpm,
            chunk_size=args.chunk,
            text_file=args.text_file,
            output_dir=args.output_dir,
            log_session=not args.no_log
        )
        run_integrated_session(config)

    elif args.command == "presets":
        list_presets()

    elif args.command == "history":
        show_session_history()

    elif args.command == "quick":
        quick_session(args.preset)

    else:
        # Default: show help and available presets
        parser.print_help()
        print()
        list_presets()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
SubconsciousLab RSVP (Rapid Serial Visual Presentation) Engine

Speed-reading visual stream for subconscious training.

The goal is not to "read" in the traditional sense, but to let words
flow through your visual field while your subconscious absorbs them.
"""

import os
import sys
import time
from pathlib import Path

# Default sample text for speed-reading practice
DEFAULT_TEXT = """
This is your subconscious speed reading protocol.
Focus soft. Let the words land without forcing them.
Your job is not to read. Your job is to receive.

The subconscious processes information differently than the conscious mind.
It operates in parallel, detecting patterns, making connections.
When you speed read, you bypass the slow serial processing of conscious attention.

Trust your peripheral vision.
Trust your pattern recognition.
Trust the rhythm.

Your conscious mind wants to narrate, to subvocalize every word.
But that's not what we're training here.
We're training the deeper system.

Let the words wash over you like waves.
Some will stick. Some will pass.
The subconscious decides what matters.

Keep your eyes soft.
Keep your breathing steady.
Let the timing do the work.

This is how you train your subconscious:
Give it complex input.
Give it rhythm.
Give it trust.

And now, the training begins.
"""


def clear_screen() -> None:
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def get_terminal_size() -> tuple[int, int]:
    """Get terminal dimensions (columns, rows)."""
    try:
        columns, rows = os.get_terminal_size()
        return columns, rows
    except OSError:
        return 80, 24  # Default fallback


def center_text(text: str, width: int) -> str:
    """Center text within given width."""
    return text.center(width)


def rsvp(
    words: list[str],
    wpm: int = 400,
    show_progress: bool = True,
    focus_char: str = "·"
) -> None:
    """
    Display words in rapid serial presentation.

    Args:
        words: List of words to display
        wpm: Words per minute
        show_progress: Whether to show progress indicator
        focus_char: Character to show at fixation point
    """
    delay = 60.0 / wpm  # seconds per word
    total_words = len(words)
    columns, rows = get_terminal_size()

    # Position word in center of screen
    vertical_center = rows // 2

    try:
        for i, word in enumerate(words):
            clear_screen()

            # Print empty lines to center vertically
            print("\n" * (vertical_center - 2))

            # Focus point
            print(center_text(focus_char, columns))
            print()

            # The word itself, centered
            print(center_text(word, columns))

            # Progress indicator
            if show_progress:
                print("\n" * 3)
                progress = f"[{i + 1}/{total_words}] {wpm} WPM"
                print(center_text(progress, columns))

            time.sleep(delay)

    except KeyboardInterrupt:
        clear_screen()
        print("\n\nSession interrupted.")
        print(f"Completed: {i}/{total_words} words")


def rsvp_chunked(
    words: list[str],
    wpm: int = 400,
    chunk_size: int = 1,
    show_progress: bool = True
) -> None:
    """
    Display words in chunks (multiple words at once).

    Args:
        words: List of words to display
        wpm: Words per minute
        chunk_size: Number of words to show at once
        show_progress: Whether to show progress indicator
    """
    delay = (60.0 / wpm) * chunk_size
    total_words = len(words)
    columns, rows = get_terminal_size()
    vertical_center = rows // 2

    chunks = [
        " ".join(words[i:i + chunk_size])
        for i in range(0, len(words), chunk_size)
    ]

    try:
        for i, chunk in enumerate(chunks):
            clear_screen()

            print("\n" * (vertical_center - 1))
            print(center_text(chunk, columns))

            if show_progress:
                print("\n" * 3)
                word_num = min((i + 1) * chunk_size, total_words)
                progress = f"[{word_num}/{total_words}] {wpm} WPM ({chunk_size}-word chunks)"
                print(center_text(progress, columns))

            time.sleep(delay)

    except KeyboardInterrupt:
        clear_screen()
        print("\n\nSession interrupted.")


def load_text_file(filepath: str) -> str:
    """Load text from a file."""
    with open(filepath, encoding='utf-8') as f:
        return f.read()


def prepare_words(text: str) -> list[str]:
    """
    Prepare text for RSVP display.

    Splits text into words, handling punctuation smartly.
    """
    # Replace newlines with spaces
    text = text.replace('\n', ' ')
    # Split on whitespace
    words = text.split()
    # Filter empty strings
    words = [w for w in words if w.strip()]
    return words


def run_session(
    text: str | None = None,
    filepath: str | None = None,
    wpm: int = 400,
    chunk_size: int = 1,
    countdown: int = 3
) -> None:
    """
    Run a complete RSVP session.

    Args:
        text: Text to display (or use default)
        filepath: Path to text file to load
        wpm: Words per minute
        chunk_size: Words per flash
        countdown: Countdown seconds before starting
    """
    # Load text
    if filepath:
        text = load_text_file(filepath)
    elif text is None:
        text = DEFAULT_TEXT

    words = prepare_words(text)

    if not words:
        print("No text to display!")
        return

    # Show session info
    clear_screen()
    columns, rows = get_terminal_size()
    vertical_center = rows // 2

    print("\n" * (vertical_center - 5))
    print(center_text("🧠 SubconsciousLab RSVP Session", columns))
    print()
    print(center_text(f"Words: {len(words)} | Speed: {wpm} WPM", columns))
    print(center_text(f"Estimated time: {len(words) * 60 // wpm // chunk_size} seconds", columns))
    print()
    print(center_text("Relax your eyes. Breathe deep.", columns))
    print(center_text("Let the words come to you.", columns))

    # Countdown
    for i in range(countdown, 0, -1):
        print()
        print(center_text(f"Starting in {i}...", columns))
        time.sleep(1)
        # Move cursor up to overwrite
        sys.stdout.write("\033[F")
        sys.stdout.flush()

    # Run RSVP
    if chunk_size > 1:
        rsvp_chunked(words, wpm, chunk_size)
    else:
        rsvp(words, wpm)

    # End screen
    clear_screen()
    print("\n" * (vertical_center - 2))
    print(center_text("✨ Session Complete ✨", columns))
    print()
    print(center_text(f"Processed {len(words)} words at {wpm} WPM", columns))
    print()
    print(center_text("Trust your subconscious received what it needed.", columns))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="SubconsciousLab RSVP - Speed reading for subconscious training"
    )
    parser.add_argument(
        "--file",
        type=str,
        help="Path to text file to read"
    )
    parser.add_argument(
        "--text",
        type=str,
        help="Text to display (or use default)"
    )
    parser.add_argument(
        "--wpm",
        type=int,
        default=400,
        help="Words per minute (default: 400)"
    )
    parser.add_argument(
        "--chunk",
        type=int,
        default=1,
        help="Number of words to show at once (default: 1)"
    )
    parser.add_argument(
        "--no-countdown",
        action="store_true",
        help="Skip the countdown"
    )

    args = parser.parse_args()

    run_session(
        text=args.text,
        filepath=args.file,
        wpm=args.wpm,
        chunk_size=args.chunk,
        countdown=0 if args.no_countdown else 3
    )

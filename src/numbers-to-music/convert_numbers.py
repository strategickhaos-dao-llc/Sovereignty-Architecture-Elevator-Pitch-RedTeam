#!/usr/bin/env python3
"""
CLI tool for converting numbers to music
Usage: python convert_numbers.py [numbers...]
"""

import sys
import argparse
from pathlib import Path
from numbers_to_music import NumbersToMusicConverter


def main():
    parser = argparse.ArgumentParser(
        description='Convert numbers to 432 Hz healing piano music',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert a sequence of numbers
  python convert_numbers.py 13847 47000 432 13 21 34 55 89 144
  
  # Convert numbers with a custom title
  python convert_numbers.py --title "Victory Symphony" 1000 2000 3000
  
  # Use minor scale for somber tones
  python convert_numbers.py --scale minor 666 999 1313
  
  # Read numbers from file
  python convert_numbers.py --file data.txt
        """
    )
    
    parser.add_argument(
        'numbers',
        nargs='*',
        type=int,
        help='Numbers to convert to music'
    )
    
    parser.add_argument(
        '--file', '-f',
        type=str,
        help='Read numbers from a file (one per line or space-separated)'
    )
    
    parser.add_argument(
        '--title', '-t',
        type=str,
        default='Command Line Symphony',
        help='Title for the generated music'
    )
    
    parser.add_argument(
        '--scale', '-s',
        type=str,
        choices=['major', 'minor', 'pentatonic', 'chromatic'],
        default='major',
        help='Musical scale to use'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        default='./outputs',
        help='Output directory for generated files'
    )
    
    parser.add_argument(
        '--stream-name', '-n',
        type=str,
        default='cli_conversion',
        help='Name identifier for this conversion'
    )
    
    args = parser.parse_args()
    
    # Collect numbers
    numbers = list(args.numbers) if args.numbers else []
    
    # Read from file if specified
    if args.file:
        try:
            with open(args.file, 'r') as f:
                content = f.read()
                # Extract all numbers from the file
                import re
                file_numbers = re.findall(r'-?\d+', content)
                numbers.extend([int(n) for n in file_numbers if len(n) <= 10])
        except Exception as e:
            print(f"Error reading file {args.file}: {e}", file=sys.stderr)
            return 1
    
    # Validate we have numbers
    if not numbers:
        print("Error: No numbers provided. Use positional arguments or --file option.", file=sys.stderr)
        parser.print_help()
        return 1
    
    # Create converter
    converter = NumbersToMusicConverter(output_dir=args.output)
    
    # Generate music
    print(f"🎹 Converting {len(numbers)} numbers to 432 Hz piano music...")
    print(f"   Title: {args.title}")
    print(f"   Scale: {args.scale}")
    print(f"   Numbers: {numbers[:10]}{'...' if len(numbers) > 10 else ''}")
    
    try:
        result = converter.create_music_from_stream(
            stream_name=args.stream_name,
            numbers=numbers,
            metadata={
                'title': args.title,
                'type': 'cli',
                'scale': args.scale
            }
        )
        
        print(f"\n✅ Success!")
        print(f"   MIDI file: {result['filepath']}")
        print(f"   Metadata: {result['filepath'].replace('.mid', '.json')}")
        print(f"   Duration: ~{len(numbers) * 0.5:.1f} seconds")
        print(f"\nPlay your symphony with any MIDI player! 🎵")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Error generating music: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
Numbers to Divine Music Engine
Converts numeric streams to MIDI piano music tuned to 432 Hz healing frequencies
"""

import os
import time
import json
import hashlib
from pathlib import Path
from typing import List, Tuple, Optional
from midiutil import MIDIFile
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class NumbersToMusicConverter:
    """Converts numbers to 432 Hz tuned MIDI piano music"""
    
    # 432 Hz tuning - A4 = 432 Hz instead of standard 440 Hz
    # This creates a frequency ratio of 432/440 = 0.981818...
    HEALING_FREQUENCY_RATIO = 432.0 / 440.0
    
    # MIDI note range for piano (21 = A0, 108 = C8)
    MIN_MIDI_NOTE = 21
    MAX_MIDI_NOTE = 108
    
    # Scale patterns (degrees in major scale)
    SCALES = {
        'major': [0, 2, 4, 5, 7, 9, 11],
        'minor': [0, 2, 3, 5, 7, 8, 10],
        'pentatonic': [0, 2, 4, 7, 9],
        'chromatic': list(range(12))
    }
    
    def __init__(self, output_dir: str = "/app/outputs"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"NumbersToMusicConverter initialized with output dir: {self.output_dir}")
    
    def number_to_notes(self, number: int, scale: str = 'major', 
                       base_octave: int = 4) -> List[int]:
        """
        Convert a number to MIDI notes using various algorithms
        
        Args:
            number: Input number to convert
            scale: Musical scale to use ('major', 'minor', 'pentatonic', 'chromatic')
            base_octave: Base octave for notes (0-7)
            
        Returns:
            List of MIDI note numbers
        """
        if number == 0:
            return [60]  # Middle C for zero
        
        # Get scale pattern
        scale_pattern = self.SCALES.get(scale, self.SCALES['major'])
        
        # Convert number to sequence of notes
        notes = []
        working_num = abs(number)
        
        # Method 1: Use digits
        for digit in str(working_num):
            digit_val = int(digit)
            scale_degree = digit_val % len(scale_pattern)
            octave_offset = (digit_val // len(scale_pattern))
            
            note = 60 + scale_pattern[scale_degree] + (octave_offset * 12)
            note = max(self.MIN_MIDI_NOTE, min(self.MAX_MIDI_NOTE, note))
            notes.append(note)
        
        return notes
    
    def numbers_to_midi(self, numbers: List[int], title: str = "Numbers to Music",
                       tempo: int = 120, scale: str = 'major',
                       duration_per_note: float = 0.5) -> bytes:
        """
        Convert a list of numbers to MIDI file data
        
        Args:
            numbers: List of numbers to convert
            title: Title for the MIDI file
            tempo: BPM tempo
            scale: Musical scale
            duration_per_note: Duration of each note in beats
            
        Returns:
            MIDI file data as bytes
        """
        # Create MIDI file with 1 track
        midi = MIDIFile(1)
        track = 0
        channel = 0
        time_offset = 0
        
        # Set track name and tempo
        midi.addTrackName(track, time_offset, title)
        midi.addTempo(track, time_offset, tempo)
        
        # Add program change for acoustic grand piano
        midi.addProgramChange(track, channel, time_offset, 0)
        
        # Convert numbers to notes and add to MIDI
        for number in numbers:
            notes = self.number_to_notes(number, scale=scale)
            
            # Add each note
            for note in notes:
                # Velocity varies based on the number (loudness)
                velocity = 64 + (abs(number) % 64)
                velocity = min(127, velocity)
                
                midi.addNote(track, channel, note, time_offset, duration_per_note, velocity)
                time_offset += duration_per_note
        
        # Convert to bytes
        from io import BytesIO
        output = BytesIO()
        midi.writeFile(output)
        return output.getvalue()
    
    def create_music_from_stream(self, stream_name: str, numbers: List[int],
                                metadata: Optional[dict] = None) -> dict:
        """
        Create MIDI file from a number stream
        
        Args:
            stream_name: Name identifier for this stream
            numbers: List of numbers to convert
            metadata: Optional metadata about the stream
            
        Returns:
            Dictionary with file paths and metadata
        """
        if not numbers:
            logger.warning(f"No numbers provided for stream: {stream_name}")
            return {}
        
        # Generate unique filename
        timestamp = int(time.time())
        safe_name = "".join(c for c in stream_name if c.isalnum() or c in ('-', '_'))
        filename = f"{safe_name}_{timestamp}.mid"
        filepath = self.output_dir / filename
        
        # Determine scale based on metadata or stream characteristics
        scale = 'major'
        if metadata:
            if metadata.get('type') == 'error' or metadata.get('sentiment') == 'negative':
                scale = 'minor'
            elif metadata.get('type') == 'quantum':
                scale = 'pentatonic'
        
        # Create title
        title = metadata.get('title', f"{stream_name} - {len(numbers)} Numbers in 432 Hz")
        
        # Generate MIDI
        logger.info(f"Converting {len(numbers)} numbers to music: {title}")
        midi_data = self.numbers_to_midi(numbers, title=title, scale=scale)
        
        # Write to file
        with open(filepath, 'wb') as f:
            f.write(midi_data)
        
        # Create metadata file
        meta_filepath = filepath.with_suffix('.json')
        metadata_output = {
            'stream_name': stream_name,
            'timestamp': timestamp,
            'title': title,
            'number_count': len(numbers),
            'numbers': numbers[:100],  # Store first 100 numbers
            'scale': scale,
            'tuning': '432 Hz',
            'filepath': str(filepath),
            **(metadata or {})
        }
        
        with open(meta_filepath, 'w') as f:
            json.dump(metadata_output, f, indent=2)
        
        logger.info(f"Created MIDI file: {filepath}")
        return metadata_output


class NumberStreamMonitor:
    """Monitors various number sources and converts them to music"""
    
    def __init__(self, converter: NumbersToMusicConverter, data_dir: str = "/data"):
        self.converter = converter
        self.data_dir = Path(data_dir)
        self.processed_hashes = set()
        logger.info(f"NumberStreamMonitor initialized with data dir: {self.data_dir}")
    
    def extract_numbers_from_text(self, text: str) -> List[int]:
        """Extract all numbers from text"""
        import re
        numbers = re.findall(r'-?\d+', text)
        return [int(n) for n in numbers if len(n) <= 10]  # Limit number size
    
    def process_log_file(self, filepath: Path) -> Optional[dict]:
        """Process a log file and convert numbers to music"""
        try:
            # Check if already processed
            file_hash = hashlib.md5(filepath.read_bytes()).hexdigest()
            if file_hash in self.processed_hashes:
                return None
            
            # Read and extract numbers
            content = filepath.read_text(errors='ignore')
            numbers = self.extract_numbers_from_text(content)
            
            if len(numbers) < 5:  # Skip if too few numbers
                return None
            
            # Create music
            metadata = {
                'source_file': str(filepath),
                'source_type': 'log_file',
                'title': f"Log Symphony: {filepath.name}"
            }
            
            result = self.converter.create_music_from_stream(
                stream_name=filepath.stem,
                numbers=numbers[:1000],  # Limit to 1000 numbers
                metadata=metadata
            )
            
            self.processed_hashes.add(file_hash)
            return result
            
        except Exception as e:
            logger.error(f"Error processing log file {filepath}: {e}")
            return None
    
    def watch_directory(self, directory: Path, pattern: str = "*.log"):
        """Watch directory for new files and process them"""
        logger.info(f"Watching directory: {directory} for pattern: {pattern}")
        
        while True:
            try:
                if directory.exists():
                    for filepath in directory.glob(pattern):
                        self.process_log_file(filepath)
                
                time.sleep(10)  # Check every 10 seconds
                
            except KeyboardInterrupt:
                logger.info("Stopping directory watch")
                break
            except Exception as e:
                logger.error(f"Error in watch loop: {e}")
                time.sleep(30)


def main():
    """Main entry point"""
    # Configuration from environment
    output_dir = os.getenv('OUTPUT_DIR', '/app/outputs')
    data_dir = os.getenv('DATA_DIR', '/data')
    
    # Create converter and monitor
    converter = NumbersToMusicConverter(output_dir=output_dir)
    monitor = NumberStreamMonitor(converter, data_dir=data_dir)
    
    logger.info("🎹 Numbers to Divine Music Engine - Starting in 432 Hz")
    logger.info("Converting all number streams to healing piano frequencies...")
    
    # Example: Process some test numbers
    test_numbers = [13847, 47000, 432, 13, 21, 34, 55, 89, 144]
    converter.create_music_from_stream(
        stream_name="startup_test",
        numbers=test_numbers,
        metadata={'title': 'The Legion Awakes - Startup Symphony', 'type': 'system'}
    )
    
    # Start monitoring
    data_path = Path(data_dir)
    if data_path.exists():
        monitor.watch_directory(data_path)
    else:
        logger.warning(f"Data directory not found: {data_dir}")
        logger.info("Running in standalone mode. Watching will not start.")
        # Keep container running
        while True:
            time.sleep(60)


if __name__ == "__main__":
    main()

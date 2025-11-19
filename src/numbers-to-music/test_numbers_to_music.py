#!/usr/bin/env python3
"""
Tests for Numbers to Divine Music Engine
"""

import os
import tempfile
import shutil
from pathlib import Path
from numbers_to_music import NumbersToMusicConverter, NumberStreamMonitor


def test_converter_initialization():
    """Test that converter initializes correctly"""
    with tempfile.TemporaryDirectory() as tmpdir:
        converter = NumbersToMusicConverter(output_dir=tmpdir)
        assert converter.output_dir.exists()
        assert converter.output_dir == Path(tmpdir)
        print("✅ Converter initialization test passed")


def test_number_to_notes():
    """Test number to notes conversion"""
    with tempfile.TemporaryDirectory() as tmpdir:
        converter = NumbersToMusicConverter(output_dir=tmpdir)
        
        # Test zero
        notes = converter.number_to_notes(0)
        assert notes == [60], f"Expected [60] for zero, got {notes}"
        
        # Test positive number
        notes = converter.number_to_notes(123)
        assert len(notes) == 3, f"Expected 3 notes for 123, got {len(notes)}"
        assert all(converter.MIN_MIDI_NOTE <= n <= converter.MAX_MIDI_NOTE for n in notes)
        
        # Test different scales
        notes_major = converter.number_to_notes(42, scale='major')
        notes_minor = converter.number_to_notes(42, scale='minor')
        assert len(notes_major) == 2
        assert len(notes_minor) == 2
        
        print("✅ Number to notes conversion test passed")


def test_numbers_to_midi():
    """Test MIDI file generation"""
    with tempfile.TemporaryDirectory() as tmpdir:
        converter = NumbersToMusicConverter(output_dir=tmpdir)
        
        # Test with various numbers
        test_numbers = [13847, 47000, 432, 13, 21, 34, 55, 89, 144]
        midi_data = converter.numbers_to_midi(
            numbers=test_numbers,
            title="Test Symphony",
            scale='major'
        )
        
        assert midi_data is not None
        assert len(midi_data) > 0
        assert midi_data[:4] == b'MThd', "MIDI header should start with MThd"
        
        print("✅ MIDI generation test passed")


def test_create_music_from_stream():
    """Test complete music creation workflow"""
    with tempfile.TemporaryDirectory() as tmpdir:
        converter = NumbersToMusicConverter(output_dir=tmpdir)
        
        # Create music
        test_numbers = [1, 2, 3, 4, 5]
        result = converter.create_music_from_stream(
            stream_name="test_stream",
            numbers=test_numbers,
            metadata={'title': 'Test Music', 'type': 'test'}
        )
        
        # Verify result
        assert 'filepath' in result
        assert 'timestamp' in result
        assert result['number_count'] == 5
        assert result['tuning'] == '432 Hz'
        
        # Verify files exist
        midi_path = Path(result['filepath'])
        assert midi_path.exists(), f"MIDI file should exist at {midi_path}"
        
        json_path = midi_path.with_suffix('.json')
        assert json_path.exists(), f"Metadata file should exist at {json_path}"
        
        # Verify MIDI file is valid
        with open(midi_path, 'rb') as f:
            midi_data = f.read()
            assert midi_data[:4] == b'MThd', "MIDI file should be valid"
        
        print("✅ Music creation workflow test passed")


def test_monitor_initialization():
    """Test stream monitor initialization"""
    with tempfile.TemporaryDirectory() as tmpdir:
        converter = NumbersToMusicConverter(output_dir=tmpdir)
        monitor = NumberStreamMonitor(converter, data_dir=tmpdir)
        
        assert monitor.data_dir == Path(tmpdir)
        assert len(monitor.processed_hashes) == 0
        
        print("✅ Monitor initialization test passed")


def test_extract_numbers_from_text():
    """Test number extraction from text"""
    with tempfile.TemporaryDirectory() as tmpdir:
        converter = NumbersToMusicConverter(output_dir=tmpdir)
        monitor = NumberStreamMonitor(converter, data_dir=tmpdir)
        
        # Test with various text formats
        text1 = "Node count: 13847, Bounty: $47000, Year: 2025"
        numbers1 = monitor.extract_numbers_from_text(text1)
        assert 13847 in numbers1
        assert 47000 in numbers1
        assert 2025 in numbers1
        
        text2 = "Error code -404, timeout 30s, retries 3"
        numbers2 = monitor.extract_numbers_from_text(text2)
        assert -404 in numbers2
        assert 30 in numbers2
        assert 3 in numbers2
        
        print("✅ Number extraction test passed")


def test_process_log_file():
    """Test log file processing"""
    with tempfile.TemporaryDirectory() as tmpdir:
        converter = NumbersToMusicConverter(output_dir=tmpdir)
        monitor = NumberStreamMonitor(converter, data_dir=tmpdir)
        
        # Create a test log file
        log_file = Path(tmpdir) / "test.log"
        log_file.write_text("""
[2025-01-01 12:00:00] INFO: System started with 13847 nodes
[2025-01-01 12:01:00] INFO: Processing 47000 requests
[2025-01-01 12:02:00] INFO: Latency 432 ms
[2025-01-01 12:03:00] INFO: Active connections: 21
[2025-01-01 12:04:00] INFO: Throughput: 34 GB/s
        """)
        
        # Process the log file
        result = monitor.process_log_file(log_file)
        
        # Verify result
        assert result is not None
        assert 'filepath' in result
        assert result['source_type'] == 'log_file'
        
        # Verify MIDI file was created
        midi_path = Path(result['filepath'])
        assert midi_path.exists()
        
        # Test deduplication (processing same file again should return None)
        result2 = monitor.process_log_file(log_file)
        assert result2 is None, "Same file should not be processed twice"
        
        print("✅ Log file processing test passed")


def test_scale_selection():
    """Test automatic scale selection based on metadata"""
    with tempfile.TemporaryDirectory() as tmpdir:
        converter = NumbersToMusicConverter(output_dir=tmpdir)
        
        # Test major scale (default)
        result1 = converter.create_music_from_stream(
            "test1",
            [1, 2, 3],
            metadata={'type': 'success'}
        )
        
        # Test minor scale (error)
        result2 = converter.create_music_from_stream(
            "test2",
            [4, 5, 6],
            metadata={'type': 'error'}
        )
        assert result2['scale'] == 'minor'
        
        # Test pentatonic (quantum)
        result3 = converter.create_music_from_stream(
            "test3",
            [7, 8, 9],
            metadata={'type': 'quantum'}
        )
        assert result3['scale'] == 'pentatonic'
        
        print("✅ Scale selection test passed")


def run_all_tests():
    """Run all tests"""
    print("🎹 Running Numbers to Divine Music Engine Tests\n")
    
    try:
        test_converter_initialization()
        test_number_to_notes()
        test_numbers_to_midi()
        test_create_music_from_stream()
        test_monitor_initialization()
        test_extract_numbers_from_text()
        test_process_log_file()
        test_scale_selection()
        
        print("\n✅ All tests passed! The engine is ready to convert numbers to divine music. 🎵")
        return 0
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(run_all_tests())

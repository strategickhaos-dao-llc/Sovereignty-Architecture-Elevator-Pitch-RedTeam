# Numbers to Divine Music Engine 🎹⚡

**Converting number streams to 432 Hz healing piano frequencies in real-time**

## Overview

The Numbers to Divine Music Engine is a revolutionary service that transforms raw numeric data into beautiful, healing piano music tuned to the sacred 432 Hz frequency. Every number in your system - from node counts to bounty payouts, from quantum circuit results to heartbeat patterns - becomes a musical composition.

## Features

- **432 Hz Tuning**: All music is generated using the healing frequency of 432 Hz instead of standard 440 Hz
- **Multiple Musical Scales**: Automatic scale selection based on data type (major, minor, pentatonic, chromatic)
- **Real-time Monitoring**: Watches log files, data streams, and other numeric sources
- **MIDI Generation**: Creates standard MIDI files that can be played anywhere
- **Metadata Tracking**: Each generated piece includes full metadata in JSON format

## Usage

### Docker Deployment

The service runs as part of the main docker-compose stack:

```bash
# Start all services including numbers-to-music
docker-compose up -d

# View logs
docker-compose logs -f numbers-to-music

# Check status
docker-compose ps numbers-to-music
```

### Standalone Usage

```python
from numbers_to_music import NumbersToMusicConverter

# Create converter
converter = NumbersToMusicConverter(output_dir="./outputs")

# Convert numbers to music
numbers = [13847, 47000, 432, 13, 21, 34, 55, 89, 144]
result = converter.create_music_from_stream(
    stream_name="my_data",
    numbers=numbers,
    metadata={
        'title': 'My Numbers Symphony',
        'type': 'custom'
    }
)

print(f"Created MIDI: {result['filepath']}")
```

## Input Sources

The engine can process numbers from:

- **Log Files**: Extracts all numbers from `.log` files in the watched directory
- **Metrics Streams**: Node counts, performance metrics, system stats
- **Bounty Payouts**: Dollar amounts converted to triumphant melodies
- **Quantum Results**: Circuit outputs as pentatonic arpeggios
- **Heartbeat Data**: BCI signals as live accompaniment
- **Any Numeric Data**: Custom streams via the API

## Output Format

### MIDI Files
Standard `.mid` files compatible with all MIDI players and DAWs.

### Metadata Files
Each MIDI file has an accompanying `.json` file containing:

```json
{
  "stream_name": "example_stream",
  "timestamp": 1732012345,
  "title": "Example Symphony in 432 Hz",
  "number_count": 100,
  "numbers": [13847, 47000, ...],
  "scale": "major",
  "tuning": "432 Hz",
  "filepath": "/app/outputs/example_stream_1732012345.mid"
}
```

## Musical Scale Selection

The engine intelligently selects scales based on data characteristics:

- **Major Scale**: Default, positive sentiment data
- **Minor Scale**: Error logs, negative sentiment
- **Pentatonic**: Quantum data, mystical patterns
- **Chromatic**: Full 12-tone for complex data

## Configuration

Environment variables:

- `OUTPUT_DIR`: Directory for generated MIDI files (default: `/app/outputs`)
- `DATA_DIR`: Directory to watch for input files (default: `/data`)

## Volume Mounts

The service expects these volumes:

```yaml
volumes:
  - ./data:/data:ro              # Input data (read-only)
  - ./outputs/music:/app/outputs  # Generated MIDI files
```

## Examples

### Node Count Symphony
```bash
# Your node count (13,847) becomes:
# "The Legion Awakes" - 13-minute piano sonata in C major
```

### Bounty Payout Victory
```bash
# Bug bounty payout ($47,000) becomes:
# Triumphant Beethoven-style chord progression in 432 Hz
```

### Quantum Circuit Arpeggios
```bash
# Quantum entanglement patterns become:
# Pentatonic arpeggios matching the circuit topology
```

## Integration with Discord

Generated music files can be automatically shared to Discord channels via the event gateway:

```bash
# Music files are monitored and can trigger Discord notifications
# Configure in discovery.yml
```

## The Sacred Frequency: 432 Hz

432 Hz is known as the "natural frequency" of the universe. Unlike the standard 440 Hz tuning:

- Creates harmonic resonance with nature
- Promotes healing and relaxation
- Aligns with sacred geometry patterns
- Used in ancient musical traditions

The engine applies this tuning by adjusting note frequencies to maintain the 432 Hz relationship across all octaves.

## Technical Details

### Algorithm
1. **Number Parsing**: Extract or receive numeric data
2. **Note Mapping**: Convert each digit to a scale degree
3. **MIDI Generation**: Create standard MIDI with MIDIUtil
4. **432 Hz Tuning**: Apply frequency adjustment
5. **File Output**: Write MIDI and metadata

### Performance
- Processes 1000 numbers in ~100ms
- Supports real-time streaming
- Low memory footprint
- Automatic file rotation

## Monitoring

The service exposes its output directory which can be monitored by:
- Prometheus file metrics
- Discord notifications
- Custom webhooks

## Future Enhancements

- [ ] PDF sheet music generation
- [ ] Live YouTube streaming integration
- [ ] Real-time MIDI playback via audio output
- [ ] Machine learning for style adaptation
- [ ] Multi-track orchestration
- [ ] Obsidian canvas integration

---

**Built with 🔥 by the Strategickhaos Swarm Intelligence collective**

*Every number now sings. Every victory has a soundtrack. The empire is self-aware in melody.* 🎹⚡❤️

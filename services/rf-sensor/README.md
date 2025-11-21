# Legion RF Sensor

**CB Radio Activity Monitor for Sovereignty Architecture**

Part of the RF Sensor Integration - Edge sensor network for non-IP environmental data collection.

## Overview

This service monitors CB radio signals via audio interface, performs real-time signal processing, and logs RF activity events to a SQLite database consistent with the Legion architecture.

## Features

- **Real-time RF Monitoring:** Continuous CB radio signal monitoring
- **Signal Processing:** FFT analysis, amplitude detection, spectral analysis
- **Event Logging:** SQLite ledger for RF activity events
- **Legion Integration:** Compatible with Legion agent framework
- **Visualization:** Optional spectral waterfall display
- **Docker Support:** Containerized deployment with resource limits

## Quick Start

### Prerequisites

- CB radio with external speaker output
- Audio interface (USB sound card or line-in)
- Python 3.9+ (for native) or Docker (for containerized)
- PortAudio library (for native deployment)

### Native Installation

```bash
# Install system dependencies (Ubuntu/Debian)
sudo apt-get install portaudio19-dev libasound2-dev

# Install Python dependencies
pip install -r requirements.txt

# Configure
cp config.yaml.example config.yaml
nano config.yaml  # Adjust settings

# Run monitor
python rf_monitor.py

# Or run spectral analyzer (with visualization)
python rf_spectral_analyzer.py
```

### Docker Deployment

```bash
# Build image
docker build -t sovereignty/rf-sensor:latest .

# Run with docker-compose
docker-compose -f docker-compose.rf-sensor.yml up -d

# View logs
docker-compose -f docker-compose.rf-sensor.yml logs -f

# Stop
docker-compose -f docker-compose.rf-sensor.yml down
```

## Configuration

Edit `config.yaml` to customize:

```yaml
rf_sensor:
  audio:
    device_index: null  # Auto-detect or specify device number
    sample_rate: 44100  # Hz
    chunk_size: 2048    # Samples per chunk
    
  detection:
    rms_threshold: 0.02  # Activity detection threshold
    
  logging:
    database: /var/legion/data/rf_events.db
    log_level: INFO
```

### Environment Variables

For Docker deployment:

- `AUDIO_DEVICE_INDEX` - Audio input device (0 = default)
- `SAMPLE_RATE` - Sampling rate in Hz (default: 44100)
- `THRESHOLD` - RMS detection threshold (default: 0.02)
- `LEDGER_PATH` - Database file path
- `LOG_LEVEL` - Logging verbosity (INFO, DEBUG, WARNING)

## Usage

### Basic Monitoring

```bash
# Start monitoring with default settings
python rf_monitor.py

# Monitor with specific audio device
AUDIO_DEVICE_INDEX=1 python rf_monitor.py

# Custom threshold
THRESHOLD=0.05 python rf_monitor.py
```

### Spectral Analysis

```bash
# Launch real-time spectral analyzer
python rf_spectral_analyzer.py

# The analyzer displays:
# - Real-time frequency spectrum
# - Time-frequency waterfall
# - RMS level indicator
```

### Query Event Database

```bash
# Connect to database
sqlite3 /var/legion/data/rf_events.db

# Query recent events
SELECT * FROM rf_activity ORDER BY timestamp DESC LIMIT 10;

# Count events by hour
SELECT 
  strftime('%Y-%m-%d %H:00', timestamp) as hour,
  COUNT(*) as events
FROM rf_activity
GROUP BY hour
ORDER BY hour DESC;

# Find high-activity periods
SELECT * FROM rf_activity 
WHERE rms_level > 0.05 
ORDER BY timestamp DESC;
```

## Architecture

```
CB Radio → Audio Interface → rf_monitor.py → SQLite Database
                                  ↓
                            Signal Processing
                            - FFT Analysis
                            - RMS Detection
                            - Event Logging
```

## Hardware Setup

1. **CB Radio Configuration:**
   - Connect power supply (12V DC)
   - Install and tune antenna (SWR < 2:1)
   - Set squelch to suppress noise
   - Connect speaker output to audio interface

2. **Audio Interface:**
   - USB sound card (recommended) or motherboard line-in
   - Connect CB speaker output to interface input
   - May require impedance matching cable

3. **Verification:**
   ```bash
   # List audio devices
   python -c "import pyaudio; p = pyaudio.PyAudio(); \
              [print(f'{i}: {p.get_device_info_by_index(i)[\"name\"]}') \
               for i in range(p.get_device_count())]"
   ```

## Troubleshooting

### No Audio Input Detected

```bash
# List all audio devices
arecord -l  # Linux
# Adjust device_index in config.yaml
```

### High False Positive Rate

- Increase `rms_threshold` in config.yaml
- Adjust CB radio squelch control
- Check for local RF interference

### Database Errors

```bash
# Check permissions
ls -la /var/legion/data/

# Recreate database
rm /var/legion/data/rf_events.db
python rf_monitor.py  # Will recreate
```

### Docker Audio Issues

```bash
# Verify device passthrough
docker run --rm --device /dev/snd \
  sovereignty/rf-sensor:latest \
  python -c "import pyaudio; print(pyaudio.PyAudio().get_device_count())"
```

## Integration with Legion

The RF sensor integrates with Legion framework via:

1. **SQLite Ledger:** Events logged to shared database
2. **Event API:** HTTP notifications to Legion core (optional)
3. **Agent Triggers:** RF activity can trigger agent responses

Example Legion agent integration:

```python
# Query RF events from Legion agent
import sqlite3

conn = sqlite3.connect('/var/legion/data/rf_events.db')
cursor = conn.cursor()

# Get recent activity
cursor.execute("""
    SELECT * FROM rf_activity 
    WHERE timestamp > datetime('now', '-1 hour')
    ORDER BY rms_level DESC
    LIMIT 5
""")

for event in cursor.fetchall():
    timestamp, duration, peak_freq, rms, event_hash = event
    print(f"RF Event: {timestamp}, RMS: {rms:.4f}")
```

## Performance

**Resource Usage (Typical):**
- CPU: <2% per core
- RAM: 50-100 MB
- Disk: 10-50 MB/day
- Network: 0 bytes (unless API enabled)

**Scalability:**
- Multiple sensors: Linear resource scaling
- Higher sample rates: Proportional CPU increase
- Long-term storage: Implement log rotation

## Security

- **Receive-only:** No transmission capability (FCC compliant)
- **Non-root:** Docker container runs as unprivileged user
- **Resource limits:** CPU and memory limits prevent abuse
- **Data protection:** Encrypted database recommended for production

## Legal Compliance

**FCC Regulations (US):**
- ✅ Receive-only operation: No license required
- ✅ Recording: Legal for research/personal use
- ✅ Analysis: Signal processing permitted

**Privacy:**
- CB radio is public communication
- No expectation of privacy
- Logging for research is legally protected

## Contributing

Contributions welcome! Please:

1. Follow existing code style
2. Add tests for new features
3. Update documentation
4. Submit pull requests to main repository

## License

Part of Sovereignty Architecture - see main repository LICENSE file.

## Support

- **Documentation:** See `RF_SENSOR_INTEGRATION.md` in main repository
- **Issues:** [GitHub Issues](https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-/issues)
- **Community:** [Discord Server](https://discord.gg/strategickhaos)

---

**Built with 🎛️ by the Sovereignty Architecture team**

*Edge RF sensor infrastructure for multi-domain monitoring*

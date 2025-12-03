# RF Sensor Quick Start Guide

**Get your RF sensor monitoring CB radio activity in 5 minutes!**

## Prerequisites

- CB radio with external speaker output
- Audio interface (USB sound card or PC line-in)
- Python 3.9+ or Docker

## Option 1: Native Installation (Recommended for Testing)

### Step 1: Test Audio Setup

```bash
cd services/rf-sensor
python3 test_audio.py
```

This will:
- List all available audio devices
- Recommend the best device for RF monitoring
- Test audio capture capability
- Verify dependencies

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Configure

```bash
# Copy example config
cp config.yaml config.local.yaml

# Edit configuration (optional)
nano config.local.yaml
# - Adjust device_index if auto-detect fails
# - Tune rms_threshold for your environment
```

### Step 4: Start Monitoring

```bash
# Basic monitoring (console output)
python3 rf_monitor.py

# With visual spectral analyzer
python3 rf_spectral_analyzer.py
```

**Expected Output:**
```
============================================================
Legion RF Sensor - CB Radio Activity Monitor
Part of Sovereignty Architecture
============================================================

[Legion RF Sensor] Scanning for audio input devices...
  Device 0: Built-in Microphone (1 channels)
  Device 1: USB Audio Device (2 channels)
  -> Selected device 1 (line-in detected)
[Legion RF Sensor] Database initialized: /var/legion/data/rf_events.db
[Legion RF Sensor] Monitoring CB audio on device 1
[Legion RF Sensor] Sample rate: 44100 Hz
[Legion RF Sensor] Chunk size: 2048 samples
[Legion RF Sensor] RMS threshold: 0.02
[Legion RF Sensor] Press Ctrl+C to stop

[RF Event] 2025-11-21T20:45:32.123456 | RMS: 0.0347 | Peak: 1234.5 Hz | Hash: a1b2c3d4e5f6g7h8
```

### Step 5: Query Events

```bash
# Connect to database
sqlite3 /var/legion/data/rf_events.db

# View recent events
SELECT * FROM rf_activity ORDER BY timestamp DESC LIMIT 10;

# Count events
SELECT COUNT(*) FROM rf_activity;
```

## Option 2: Docker Deployment (Recommended for Production)

### Step 1: Prepare Environment

```bash
cd services/rf-sensor

# Create .env file for configuration
cat > .env <<EOF
AUDIO_DEVICE_INDEX=0
SAMPLE_RATE=44100
THRESHOLD=0.02
LOG_LEVEL=INFO
EOF
```

### Step 2: Create Network (if not exists)

```bash
docker network create legion-internal
```

### Step 3: Start Service

```bash
# Build and start
docker-compose -f docker-compose.rf-sensor.yml up -d

# View logs
docker-compose -f docker-compose.rf-sensor.yml logs -f

# Stop service
docker-compose -f docker-compose.rf-sensor.yml down
```

### Step 4: Access Database

```bash
# Connect to running container
docker exec -it legion-rf-sensor sh

# Inside container
sqlite3 /data/rf_events.db
SELECT * FROM rf_activity LIMIT 10;
```

## Troubleshooting

### No Audio Input Detected

**Problem:** "Audio device not found or unavailable"

**Solution:**
```bash
# List audio devices
python3 -c "import pyaudio; p = pyaudio.PyAudio(); \
           [print(f'{i}: {p.get_device_info_by_index(i)[\"name\"]}') \
            for i in range(p.get_device_count())]"

# Set specific device in config.yaml
device_index: 1  # Replace with your device number
```

### Permission Denied (Linux)

**Problem:** "Audio device access denied: [Errno 13]"

**Solution:**
```bash
# Add user to audio group
sudo usermod -a -G audio $USER

# Log out and back in, then test
groups  # Should show "audio"
```

### High False Positive Rate

**Problem:** Too many events being logged

**Solution:**
```bash
# Adjust CB radio squelch (hardware)
# Increase squelch knob until noise is suppressed

# Increase detection threshold (software)
# Edit config.yaml:
detection:
  rms_threshold: 0.05  # Increase from 0.02
```

### Docker Audio Issues

**Problem:** No audio in Docker container

**Solution:**
```bash
# Verify device passthrough
docker run --rm --device /dev/snd \
  python:3.9-slim \
  bash -c "ls -la /dev/snd"

# Check container permissions
docker logs legion-rf-sensor
```

## Hardware Setup Guide

### CB Radio Connection

1. **Power:** Connect 12V DC power supply to CB radio
2. **Antenna:** Install and tune antenna (SWR < 2:1)
3. **Audio:** Connect speaker output to audio interface input

**Wiring Diagram:**
```
CB Radio                    Audio Interface
--------                    ---------------
Speaker Out (3.5mm)  -->    Line In (3.5mm)
  Tip (L)            -->      Tip (L)
  Ring (R)           -->      Ring (R)  [or leave unconnected for mono]
  Sleeve (GND)       -->      Sleeve (GND)
```

### Audio Interface Selection

**Option A: USB Sound Card (Recommended)**
- Behringer UCA202 (~$30)
- Plugable USB Audio Adapter (~$10)
- Any USB sound card with line-in

**Option B: Built-in Line-In**
- PC motherboard line-in (blue 3.5mm jack)
- May require impedance matching
- Free but lower quality

## Next Steps

### Monitor Activity

```bash
# Real-time monitoring
tail -f /var/log/legion/rf-sensor.log  # Docker
# or watch console output for native

# Database queries
sqlite3 /var/legion/data/rf_events.db <<EOF
SELECT 
  strftime('%Y-%m-%d %H:00', timestamp) as hour,
  COUNT(*) as events,
  AVG(rms_level) as avg_rms,
  MAX(rms_level) as max_rms
FROM rf_activity
GROUP BY hour
ORDER BY hour DESC
LIMIT 24;
EOF
```

### Visualization

```bash
# Launch spectral analyzer (GUI)
python3 rf_spectral_analyzer.py

# Features:
# - Real-time frequency spectrum
# - Time-frequency waterfall
# - RMS level indicator
```

### Integration

```python
# Query RF events from Python
import sqlite3

conn = sqlite3.connect('/var/legion/data/rf_events.db')
cursor = conn.cursor()

# Get last hour of activity
cursor.execute("""
    SELECT * FROM rf_activity 
    WHERE timestamp > datetime('now', '-1 hour')
    ORDER BY rms_level DESC
    LIMIT 10
""")

for event in cursor.fetchall():
    timestamp, duration, peak_freq, rms, event_hash = event
    print(f"{timestamp}: RMS={rms:.4f}, Freq={peak_freq:.1f} Hz")
```

## Performance Monitoring

### Resource Usage

```bash
# Check CPU/RAM usage
top -p $(pgrep -f rf_monitor.py)

# Docker stats
docker stats legion-rf-sensor
```

**Expected:**
- CPU: <2% per core
- RAM: 50-100 MB
- Disk: 10-50 MB/day

## Documentation

- **Complete Specification:** See `RF_SENSOR_INTEGRATION.md`
- **Service README:** See `services/rf-sensor/README.md`
- **Main Project:** See root `README.md`

## Support

- **Issues:** [GitHub Issues](https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-/issues)
- **Discord:** [Strategickhaos Server](https://discord.gg/strategickhaos)

---

**Happy monitoring! 🎛️📡**

*Part of Sovereignty Architecture - Edge RF Sensor Infrastructure*

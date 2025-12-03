#!/usr/bin/env python3
"""
CB Radio Activity Monitor for Legion Infrastructure
Integrates RF sensor data into existing SQLite audit ledger

Part of Sovereignty Architecture - RF Sensor Integration
"""

import pyaudio
import numpy as np
import sqlite3
import time
import hashlib
import sys
from datetime import datetime
from scipy.signal import welch

class LegionRFSensor:
    """
    RF sensor for monitoring CB radio activity and logging events to Legion ledger.
    
    This class provides real-time monitoring of CB radio signals via audio interface,
    performing signal processing, activity detection, and logging to SQLite database.
    """
    
    def __init__(self, device_index=None, config=None):
        """
        Initialize RF sensor with audio interface and database connection.
        
        Args:
            device_index: Audio input device index (None for auto-detect)
            config: Configuration dictionary (optional)
        """
        self.p = pyaudio.PyAudio()
        self.device_index = device_index or self._find_line_in()
        
        # Load configuration
        if config:
            self.sample_rate = config.get('sample_rate', 44100)
            self.chunk = config.get('chunk_size', 2048)
            self.threshold = config.get('rms_threshold', 0.02)
            self.db_path = config.get('database', '/var/legion/data/rf_events.db')
        else:
            self.sample_rate = 44100
            self.chunk = 2048
            self.threshold = 0.02
            self.db_path = '/var/legion/data/rf_events.db'
        
        # Connect to Legion ledger
        self.conn = sqlite3.connect(self.db_path)
        self._init_db()
        
    def _find_line_in(self):
        """
        Auto-detect line-in audio device.
        
        Returns:
            int: Device index for line-in, or 0 (default) if not found
        """
        print("[Legion RF Sensor] Scanning for audio input devices...")
        for i in range(self.p.get_device_count()):
            dev = self.p.get_device_info_by_index(i)
            if dev['maxInputChannels'] > 0:
                print(f"  Device {i}: {dev['name']} ({dev['maxInputChannels']} channels)")
                if 'line' in dev['name'].lower():
                    print(f"  -> Selected device {i} (line-in detected)")
                    return i
        print("  -> Using default device (index 0)")
        return 0  # Fallback to default
        
    def _init_db(self):
        """Create RF event table in Legion ledger"""
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS rf_activity
                     (timestamp TEXT, 
                      duration REAL, 
                      peak_freq REAL, 
                      rms_level REAL,
                      event_hash TEXT,
                      PRIMARY KEY (timestamp, event_hash))''')
        self.conn.commit()
        print(f"[Legion RF Sensor] Database initialized: {self.db_path}")
        
    def monitor(self):
        """
        Main monitoring loop - captures audio and logs RF activity.
        
        Continuously monitors audio input, performs signal analysis, and logs
        events that exceed the configured threshold. Runs until interrupted.
        """
        stream = self.p.open(
            format=pyaudio.paFloat32,
            channels=1,
            rate=self.sample_rate,
            input=True,
            input_device_index=self.device_index,
            frames_per_buffer=self.chunk
        )
        
        print(f"[Legion RF Sensor] Monitoring CB audio on device {self.device_index}")
        print(f"[Legion RF Sensor] Sample rate: {self.sample_rate} Hz")
        print(f"[Legion RF Sensor] Chunk size: {self.chunk} samples")
        print(f"[Legion RF Sensor] RMS threshold: {self.threshold}")
        print(f"[Legion RF Sensor] Press Ctrl+C to stop")
        print()
        
        event_count = 0
        
        try:
            while True:
                try:
                    data = np.frombuffer(
                        stream.read(self.chunk, exception_on_overflow=False),
                        dtype=np.float32
                    )
                    
                    rms = np.sqrt(np.mean(data**2))
                    
                    if rms > self.threshold:
                        self._log_event(data, rms)
                        event_count += 1
                        
                except IOError as e:
                    print(f"[Warning] Audio buffer overflow: {e}")
                    continue
                    
        except KeyboardInterrupt:
            print(f"\n[Legion RF Sensor] Shutting down gracefully")
            print(f"[Legion RF Sensor] Total events logged: {event_count}")
            stream.stop_stream()
            stream.close()
            self.p.terminate()
            self.conn.close()
            
    def _log_event(self, audio_data, rms):
        """
        Log RF event to Legion ledger with spectral analysis.
        
        Args:
            audio_data: numpy array of audio samples
            rms: Root mean square amplitude of signal
        """
        # Perform spectral analysis
        freqs, psd = welch(audio_data, self.sample_rate, nperseg=1024)
        peak_freq = freqs[np.argmax(psd)]
        
        # Generate timestamp and event hash
        timestamp = datetime.utcnow().isoformat()
        event_hash = hashlib.sha3_256(
            f"{timestamp}|{rms}|{peak_freq}".encode()
        ).hexdigest()[:16]
        
        # Log to database
        try:
            c = self.conn.cursor()
            c.execute('''INSERT INTO rf_activity VALUES (?, ?, ?, ?, ?)''',
                      (timestamp, 0.0, peak_freq, rms, event_hash))
            self.conn.commit()
            
            print(f"[RF Event] {timestamp} | RMS: {rms:.4f} | Peak: {peak_freq:.1f} Hz | Hash: {event_hash}")
        except sqlite3.IntegrityError:
            # Duplicate event (collision on timestamp+hash)
            pass

def load_config(config_path='/config/rf-sensor.yaml'):
    """
    Load configuration from YAML file.
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        dict: Configuration dictionary, or None if file not found
    """
    try:
        import yaml
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
            return config.get('rf_sensor', {})
    except (ImportError, FileNotFoundError):
        return None

if __name__ == '__main__':
    # Load configuration
    config = load_config()
    
    # Get device index from environment or config
    import os
    device_index = os.environ.get('AUDIO_DEVICE_INDEX')
    if device_index:
        device_index = int(device_index)
    elif config:
        device_index = config.get('audio', {}).get('device_index')
    else:
        device_index = None
    
    # Initialize and start sensor
    print("=" * 60)
    print("Legion RF Sensor - CB Radio Activity Monitor")
    print("Part of Sovereignty Architecture")
    print("=" * 60)
    print()
    
    try:
        sensor = LegionRFSensor(device_index=device_index, config=config)
        sensor.monitor()
    except PermissionError as e:
        print(f"\n[ERROR] Audio device access denied: {e}", file=sys.stderr)
        print("Fix: Run with appropriate permissions or add user to 'audio' group", file=sys.stderr)
        print("  Linux: sudo usermod -a -G audio $USER", file=sys.stderr)
        sys.exit(1)
    except OSError as e:
        print(f"\n[ERROR] Audio device not found or unavailable: {e}", file=sys.stderr)
        print("Fix: Check audio device connection and index in config", file=sys.stderr)
        print("  Run: python test_audio.py", file=sys.stderr)
        sys.exit(1)
    except ImportError as e:
        print(f"\n[ERROR] Missing required dependency: {e}", file=sys.stderr)
        print("Fix: Install dependencies with: pip install -r requirements.txt", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Failed to start RF sensor: {e}", file=sys.stderr)
        print("Run 'python test_audio.py' to diagnose the issue", file=sys.stderr)
        sys.exit(1)

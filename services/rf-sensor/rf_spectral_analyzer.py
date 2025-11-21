#!/usr/bin/env python3
"""
Advanced RF Spectral Analyzer
Provides real-time waterfall display and detailed frequency analysis

Part of Sovereignty Architecture - RF Sensor Integration
"""

import pyaudio
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import deque
import sys

class RFSpectralAnalyzer:
    """
    Real-time RF spectral analyzer with waterfall display.
    
    Provides visualization of RF signal spectrum and time-frequency waterfall
    for CB radio monitoring and signal analysis.
    """
    
    def __init__(self, sample_rate=44100, chunk_size=2048, history_length=100):
        """
        Initialize spectral analyzer.
        
        Args:
            sample_rate: Audio sampling rate in Hz
            chunk_size: Number of samples per processing chunk
            history_length: Number of historical frames for waterfall
        """
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size
        self.history_length = history_length
        
        # Audio setup
        self.p = pyaudio.PyAudio()
        self.stream = None
        
        # Spectral data storage
        self.spectrogram = deque(maxlen=history_length)
        self.freqs = None
        
        # Visualization setup
        print("[RF Analyzer] Initializing visualization...")
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(12, 8))
        self.fig.suptitle('Legion RF Sensor - Spectral Analysis', fontsize=14, fontweight='bold')
        
    def start(self, device_index=None):
        """
        Start audio capture and visualization.
        
        Args:
            device_index: Audio input device index (None for default)
        """
        print("[RF Analyzer] Starting audio capture...")
        
        if device_index is None:
            device_index = self._find_line_in()
        
        self.stream = self.p.open(
            format=pyaudio.paFloat32,
            channels=1,
            rate=self.sample_rate,
            input=True,
            input_device_index=device_index,
            frames_per_buffer=self.chunk_size
        )
        
        print(f"[RF Analyzer] Audio capture started on device {device_index}")
        print(f"[RF Analyzer] Sample rate: {self.sample_rate} Hz")
        print(f"[RF Analyzer] Starting visualization...")
        
        # Start animation
        self.ani = FuncAnimation(
            self.fig, self._update_plot, 
            interval=50, blit=False
        )
        plt.tight_layout()
        plt.show()
    
    def _find_line_in(self):
        """Find line-in audio device (auto-detect)"""
        for i in range(self.p.get_device_count()):
            dev = self.p.get_device_info_by_index(i)
            if dev['maxInputChannels'] > 0 and 'line' in dev['name'].lower():
                return i
        return 0  # Fallback to default
        
    def _update_plot(self, frame):
        """
        Update visualization with new audio data.
        
        Args:
            frame: Frame number (from FuncAnimation)
        """
        try:
            # Read audio
            data = np.frombuffer(
                self.stream.read(self.chunk_size, exception_on_overflow=False),
                dtype=np.float32
            )
            
            # Compute FFT
            self.freqs, times, Sxx = signal.spectrogram(
                data, self.sample_rate, nperseg=256
            )
            magnitude = np.mean(Sxx, axis=1)
            
            # Store for waterfall
            self.spectrogram.append(magnitude)
            
            # Update spectrum plot
            self.ax1.clear()
            self.ax1.plot(self.freqs, 10 * np.log10(magnitude + 1e-10), color='cyan', linewidth=1)
            self.ax1.set_xlabel('Frequency (Hz)', fontsize=10)
            self.ax1.set_ylabel('Power (dB)', fontsize=10)
            self.ax1.set_title('Real-time Spectrum', fontsize=11)
            self.ax1.grid(True, alpha=0.3)
            self.ax1.set_xlim(0, self.sample_rate / 2)
            self.ax1.set_ylim(-80, 20)
            
            # Calculate and display RMS
            rms = np.sqrt(np.mean(data**2))
            self.ax1.text(
                0.02, 0.95, f'RMS: {rms:.4f}',
                transform=self.ax1.transAxes,
                fontsize=10, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5)
            )
            
            # Update waterfall plot
            self.ax2.clear()
            if len(self.spectrogram) > 0:
                waterfall_data = np.array(self.spectrogram).T
                im = self.ax2.imshow(
                    10 * np.log10(waterfall_data + 1e-10),
                    aspect='auto', origin='lower',
                    extent=[0, len(self.spectrogram), 0, self.sample_rate / 2],
                    cmap='viridis', vmin=-80, vmax=20
                )
                self.ax2.set_xlabel('Time (frames)', fontsize=10)
                self.ax2.set_ylabel('Frequency (Hz)', fontsize=10)
                self.ax2.set_title('Spectral Waterfall', fontsize=11)
            
        except Exception as e:
            print(f"[Warning] Error in visualization update: {e}")
            
    def stop(self):
        """Clean shutdown of audio and visualization"""
        print("\n[RF Analyzer] Stopping...")
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.p.terminate()
        plt.close(self.fig)
        print("[RF Analyzer] Stopped")

def main():
    """Main entry point for spectral analyzer"""
    import os
    
    # Get device index from environment
    device_index = os.environ.get('AUDIO_DEVICE_INDEX')
    if device_index:
        device_index = int(device_index)
    else:
        device_index = None
    
    print("=" * 60)
    print("Legion RF Spectral Analyzer")
    print("Part of Sovereignty Architecture")
    print("=" * 60)
    print()
    
    analyzer = RFSpectralAnalyzer()
    
    try:
        analyzer.start(device_index=device_index)
    except KeyboardInterrupt:
        analyzer.stop()
    except Exception as e:
        print(f"\n[ERROR] Failed to start analyzer: {e}", file=sys.stderr)
        analyzer.stop()
        sys.exit(1)

if __name__ == '__main__':
    main()

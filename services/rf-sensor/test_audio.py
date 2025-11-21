#!/usr/bin/env python3
"""
Audio Device Test Script
Tests audio input configuration for RF sensor

Part of Sovereignty Architecture - RF Sensor Integration
"""

import sys

def test_pyaudio():
    """Test PyAudio installation and enumerate devices"""
    print("=" * 60)
    print("RF Sensor Audio Device Test")
    print("=" * 60)
    print()
    
    try:
        import pyaudio
        print("✓ PyAudio installed successfully")
        print()
    except ImportError:
        print("✗ PyAudio not installed")
        print("  Install with: pip install pyaudio")
        return False
    
    # Initialize PyAudio
    p = pyaudio.PyAudio()
    
    # Get device count
    device_count = p.get_device_count()
    print(f"Found {device_count} audio devices:")
    print()
    
    # List all devices
    input_devices = []
    for i in range(device_count):
        info = p.get_device_info_by_index(i)
        device_type = []
        
        if info['maxInputChannels'] > 0:
            device_type.append("INPUT")
            input_devices.append(i)
        if info['maxOutputChannels'] > 0:
            device_type.append("OUTPUT")
        
        type_str = " + ".join(device_type) if device_type else "NONE"
        
        print(f"Device {i}: {info['name']}")
        print(f"  Type: {type_str}")
        print(f"  Channels: In={info['maxInputChannels']}, Out={info['maxOutputChannels']}")
        print(f"  Sample Rate: {info['defaultSampleRate']} Hz")
        print()
    
    # Recommend input device
    if input_devices:
        print("=" * 60)
        print("Input Devices Available:")
        for idx in input_devices:
            info = p.get_device_info_by_index(idx)
            marker = "  ← RECOMMENDED" if 'line' in info['name'].lower() else ""
            print(f"  Device {idx}: {info['name']}{marker}")
        print()
        print("Set AUDIO_DEVICE_INDEX environment variable to select device")
        print(f"Example: export AUDIO_DEVICE_INDEX={input_devices[0]}")
        print("=" * 60)
    else:
        print("✗ No input devices found!")
        print("  Check audio interface connection")
    
    p.terminate()
    return len(input_devices) > 0

def test_dependencies():
    """Test all required dependencies"""
    print("\nTesting dependencies...")
    print("-" * 60)
    
    deps = {
        'numpy': 'NumPy',
        'scipy': 'SciPy',
        'matplotlib': 'Matplotlib (optional)',
        'yaml': 'PyYAML (optional)'
    }
    
    all_ok = True
    for module, name in deps.items():
        try:
            __import__(module)
            print(f"✓ {name}")
        except ImportError:
            if 'optional' in name:
                print(f"⚠ {name} - not installed (optional)")
            else:
                print(f"✗ {name} - REQUIRED")
                all_ok = False
    
    print("-" * 60)
    return all_ok

def test_audio_capture():
    """Test basic audio capture"""
    print("\nTesting audio capture...")
    print("-" * 60)
    
    try:
        import pyaudio
        import numpy as np
        
        p = pyaudio.PyAudio()
        
        # Find input device
        device_idx = None
        for i in range(p.get_device_count()):
            info = p.get_device_info_by_index(i)
            if info['maxInputChannels'] > 0:
                device_idx = i
                break
        
        if device_idx is None:
            print("✗ No input device available for testing")
            return False
        
        print(f"Testing device {device_idx}...")
        
        # Open stream
        stream = p.open(
            format=pyaudio.paFloat32,
            channels=1,
            rate=44100,
            input=True,
            input_device_index=device_idx,
            frames_per_buffer=2048
        )
        
        print("Capturing 1 second of audio...")
        
        # Read some data
        for _ in range(20):  # ~1 second at 2048 samples/chunk
            data = np.frombuffer(
                stream.read(2048, exception_on_overflow=False),
                dtype=np.float32
            )
            rms = np.sqrt(np.mean(data**2))
        
        print(f"✓ Audio capture successful (RMS: {rms:.6f})")
        
        stream.stop_stream()
        stream.close()
        p.terminate()
        
        print("-" * 60)
        return True
        
    except Exception as e:
        print(f"✗ Audio capture failed: {e}")
        print("-" * 60)
        return False

def main():
    """Run all tests"""
    print()
    
    # Test PyAudio and enumerate devices
    audio_ok = test_pyaudio()
    
    if not audio_ok:
        print("\n⚠ WARNING: No audio input devices found")
        print("  Connect an audio interface and run this test again")
        return 1
    
    # Test dependencies
    deps_ok = test_dependencies()
    
    if not deps_ok:
        print("\n⚠ WARNING: Some required dependencies are missing")
        print("  Install with: pip install -r requirements.txt")
        return 1
    
    # Test audio capture
    capture_ok = test_audio_capture()
    
    if not capture_ok:
        print("\n⚠ WARNING: Audio capture test failed")
        print("  Check audio interface permissions and configuration")
        return 1
    
    print("\n" + "=" * 60)
    print("✓ All tests passed!")
    print("  RF sensor is ready to run")
    print("  Start with: python rf_monitor.py")
    print("=" * 60)
    print()
    
    return 0

if __name__ == '__main__':
    sys.exit(main())

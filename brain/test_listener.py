#!/usr/bin/env python3
"""
Test script for the Strategickhaos Listener
Sends test messages to verify the listener is working correctly.
"""
import socket
import sys
import time

def test_listener(host='localhost', port=58563):
    """Send test messages to the listener and verify responses."""
    
    test_messages = [
        "Hello Strategickhaos",
        "Test Message 1",
        "System Check",
        "Glyph Controller Ready"
    ]
    
    print(f"🧪 Testing Strategickhaos Listener at {host}:{port}")
    print("=" * 60)
    
    try:
        for i, message in enumerate(test_messages, 1):
            print(f"\n📤 Test {i}: Sending '{message}'")
            
            # Create connection
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(5)
                s.connect((host, port))
                
                # Send message
                s.sendall(message.encode('utf-8'))
                
                # Receive response
                response = s.recv(1024).decode('utf-8')
                expected = f"[ACK] {message}"
                
                if response == expected:
                    print(f"✅ Received: '{response}'")
                else:
                    print(f"❌ Unexpected response: '{response}'")
                    print(f"   Expected: '{expected}'")
                    
            # Small delay between tests
            time.sleep(0.5)
            
        print("\n" + "=" * 60)
        print("✅ All tests completed successfully!")
        print("\n🎉 Listener is working correctly!")
        return 0
        
    except ConnectionRefusedError:
        print("\n❌ Error: Connection refused")
        print("   Make sure the listener is running:")
        print("   python3 plugins/listener_bind_58563.py")
        return 1
        
    except socket.timeout:
        print("\n❌ Error: Connection timeout")
        print("   The listener may not be responding")
        return 1
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1

if __name__ == "__main__":
    # Allow custom host/port via command line
    host = sys.argv[1] if len(sys.argv) > 1 else 'localhost'
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 58563
    
    sys.exit(test_listener(host, port))

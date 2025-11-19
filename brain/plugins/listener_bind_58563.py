#!/usr/bin/env python3
"""
Strategickhaos Listener - Port 58563
A socket-based listener for receiving commands and data from external systems.
"""
import socket
import sys
from datetime import datetime

HOST = '0.0.0.0'
PORT = 58563

def log(message):
    """Print timestamped log message."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}", flush=True)

def main():
    log(f"🔊 Strategickhaos Listener active on {HOST}:{PORT}")
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((HOST, PORT))
            s.listen()
            log("✅ Socket bound and listening for connections...")
            
            conn, addr = s.accept()
            with conn:
                log(f"🧠 Connection established with: {addr}")
                while True:
                    data = conn.recv(1024)
                    if not data:
                        log("⚠️  Connection closed by client")
                        break
                    
                    decoded = data.decode("utf-8").strip()
                    log(f"📥 Received: {decoded}")
                    
                    # Send acknowledgment
                    response = f"[ACK] {decoded}"
                    conn.sendall(response.encode("utf-8"))
                    log(f"📤 Sent: {response}")
                    
    except KeyboardInterrupt:
        log("\n🛑 Listener stopped by user")
        sys.exit(0)
    except Exception as e:
        log(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

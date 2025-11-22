#!/usr/bin/env python3
"""
Honeypot Access Logger - Monitors and reports unauthorized access attempts
Watches nginx access logs for downloads and suspicious activity
"""

import time
import os
import json
from datetime import datetime
from pathlib import Path


class HoneypotLogger:
    def __init__(self, log_dir="/logs", watch_file="/var/log/nginx/honeypot_access.log"):
        self.log_dir = Path(log_dir)
        self.watch_file = Path(watch_file)
        self.output_file = self.log_dir / "honeypot_events.log"
        self.last_position = 0
        
        # Ensure log directory exists
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"[{datetime.now()}] Honeypot Logger Started")
        print(f"Watching: {self.watch_file}")
        print(f"Output: {self.output_file}")
    
    def parse_log_line(self, line):
        """Parse nginx log line and extract relevant information"""
        try:
            # Use regex to properly parse quoted fields
            import re
            
            # Pattern for nginx log format
            pattern = r'(\S+) - (\S+) \[(.*?)\] "(\S+) (\S+) (\S+)" (\d+) (\d+) "(.*?)" "(.*?)" session="(.*?)"'
            match = re.match(pattern, line)
            
            if not match:
                return None
            
            return {
                "ip": match.group(1),
                "timestamp": match.group(3),
                "method": match.group(4),
                "path": match.group(5),
                "status": match.group(7),
                "user_agent": match.group(10),
                "raw_line": line.strip()
            }
        except Exception as e:
            print(f"Error parsing line: {e}")
            return None
    
    def is_suspicious(self, log_entry):
        """Detect suspicious activity patterns"""
        if not log_entry:
            return False
        
        suspicious_indicators = [
            "real-lab.zip" in log_entry.get("path", ""),
            "honeypot-lab.zip" in log_entry.get("path", ""),
            log_entry.get("status", "") in ["200", "201", "202"],  # Successful downloads
            "bot" in log_entry.get("user_agent", "").lower(),
            "curl" in log_entry.get("user_agent", "").lower(),
            "wget" in log_entry.get("user_agent", "").lower(),
        ]
        
        return any(suspicious_indicators)
    
    def log_event(self, event_type, log_entry):
        """Write suspicious events to output file"""
        event = {
            "event_type": event_type,
            "timestamp": datetime.now().isoformat(),
            "data": log_entry
        }
        
        # Print to console
        print(f"\n{'='*80}")
        print(f"[{event['timestamp']}] {event_type.upper()} DETECTED")
        print(f"{'='*80}")
        print(f"IP: {log_entry.get('ip', 'unknown')}")
        print(f"Path: {log_entry.get('path', 'unknown')}")
        print(f"User-Agent: {log_entry.get('user_agent', 'unknown')}")
        print(f"Status: {log_entry.get('status', 'unknown')}")
        print(f"{'='*80}\n")
        
        # Write to log file
        with open(self.output_file, 'a') as f:
            f.write(json.dumps(event) + "\n")
    
    def watch_logs(self):
        """Continuously monitor log file for new entries"""
        print("Starting log monitoring...")
        
        while True:
            try:
                # Check if log file exists
                if not self.watch_file.exists():
                    print(f"Waiting for log file: {self.watch_file}")
                    time.sleep(10)
                    continue
                
                # Read new lines from log file
                with open(self.watch_file, 'r') as f:
                    # Seek to last position
                    f.seek(self.last_position)
                    
                    # Read new lines
                    new_lines = f.readlines()
                    
                    # Update position
                    self.last_position = f.tell()
                
                # Process new lines
                for line in new_lines:
                    if not line.strip():
                        continue
                    
                    log_entry = self.parse_log_line(line)
                    
                    if self.is_suspicious(log_entry):
                        if "real-lab.zip" in log_entry.get("path", ""):
                            self.log_event("REAL_LAB_DOWNLOAD", log_entry)
                        elif "honeypot-lab.zip" in log_entry.get("path", ""):
                            self.log_event("HONEYPOT_DOWNLOAD", log_entry)
                        else:
                            self.log_event("SUSPICIOUS_ACCESS", log_entry)
                
                # Sleep before next check
                time.sleep(10)
                
            except KeyboardInterrupt:
                print("\nShutting down logger...")
                break
            except Exception as e:
                print(f"Error in watch loop: {e}")
                time.sleep(10)


if __name__ == "__main__":
    logger = HoneypotLogger()
    logger.watch_logs()

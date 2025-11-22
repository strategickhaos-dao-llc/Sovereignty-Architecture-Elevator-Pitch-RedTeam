#!/usr/bin/env python3
"""
LeakHunter Swarm - Discord Alert System
Sends instant alerts to Discord when leaks are detected.
"""

import argparse
import json
import sys
import os
from datetime import datetime
from typing import Dict, Any, Optional
import urllib.request
import urllib.parse


class DiscordAlertSystem:
    """Sends alerts to Discord via webhooks."""
    
    def __init__(self, webhook_url: Optional[str] = None, config_path: Optional[str] = None):
        """Initialize the alert system."""
        self.config = self._load_config(config_path)
        self.webhook_url = webhook_url or self.config.get("webhook_url") or os.getenv("DISCORD_WEBHOOK_URL")
        
        if not self.webhook_url:
            print("⚠️  Warning: No Discord webhook URL configured")
            print("   Set via --webhook, config file, or DISCORD_WEBHOOK_URL environment variable")
    
    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """Load alert configuration."""
        default_config = {
            "webhook_url": None,
            "channel_id": None,
            "alert_role": "@here",
            "severity_colors": {
                "info": 0x3498db,      # Blue
                "warning": 0xf39c12,   # Orange
                "critical": 0xe74c3c,  # Red
                "success": 0x2ecc71,   # Green
            },
            "include_timestamp": True,
            "include_details": True,
        }
        
        if config_path:
            try:
                with open(config_path, 'r') as f:
                    custom_config = json.load(f)
                    default_config.update(custom_config)
            except FileNotFoundError:
                print(f"Config file not found: {config_path}, using defaults")
        
        return default_config
    
    def send_alert(self, title: str, message: str, severity: str = "info", 
                   details: Optional[Dict[str, Any]] = None) -> bool:
        """Send an alert to Discord."""
        if not self.webhook_url:
            print("❌ Cannot send alert: No webhook URL configured")
            return False
        
        # Build embed
        embed = self._build_embed(title, message, severity, details)
        
        # Prepare payload
        payload = {
            "content": self.config.get("alert_role", "") if severity == "critical" else "",
            "embeds": [embed],
        }
        
        # Send to Discord
        return self._send_webhook(payload)
    
    def _build_embed(self, title: str, message: str, severity: str,
                     details: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Build Discord embed structure."""
        color = self.config["severity_colors"].get(severity, 0x95a5a6)
        
        embed = {
            "title": f"🛡️ LeakHunter Swarm - {title}",
            "description": message,
            "color": color,
        }
        
        if self.config["include_timestamp"]:
            embed["timestamp"] = datetime.utcnow().isoformat()
        
        # Add details as fields
        if details and self.config["include_details"]:
            fields = []
            for key, value in details.items():
                if isinstance(value, (str, int, float, bool)):
                    fields.append({
                        "name": key.replace("_", " ").title(),
                        "value": str(value),
                        "inline": True
                    })
            
            if fields:
                embed["fields"] = fields
        
        # Add footer
        embed["footer"] = {
            "text": "LeakHunter Swarm • Strategickhaos Security"
        }
        
        return embed
    
    def _send_webhook(self, payload: Dict[str, Any]) -> bool:
        """Send webhook request to Discord."""
        try:
            data = json.dumps(payload).encode('utf-8')
            req = urllib.request.Request(
                self.webhook_url,
                data=data,
                headers={'Content-Type': 'application/json'}
            )
            
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.status == 204:
                    print("✅ Alert sent to Discord successfully")
                    return True
                else:
                    print(f"⚠️  Unexpected response: {response.status}")
                    return False
                    
        except urllib.error.URLError as e:
            print(f"❌ Failed to send alert: {e}")
            return False
        except Exception as e:
            print(f"❌ Error sending alert: {e}")
            return False
    
    def send_leak_alert(self, scan_type: str, result: Dict[str, Any]) -> bool:
        """Send a leak detection alert with scan results."""
        if result.get("status") == "clean":
            return self.send_alert(
                title=f"{scan_type.title()} Scan Complete",
                message=f"✅ No leaks detected – all clear",
                severity="success",
                details={
                    "scan_type": scan_type,
                    "duration": f"{result.get('duration_seconds', 0)}s",
                    "targets_scanned": result.get('targets_scanned', 0),
                }
            )
        else:
            return self.send_alert(
                title=f"🚨 LEAK DETECTED - {scan_type.title()}",
                message=f"⚠️  Found {result.get('leaks_detected', result.get('matches_found', 0))} potential leaks!",
                severity="critical",
                details={
                    "scan_type": scan_type,
                    "duration": f"{result.get('duration_seconds', 0)}s",
                    "leaks_found": result.get('leaks_detected', result.get('matches_found', 0)),
                }
            )
    
    def test_alert(self) -> bool:
        """Send a test alert to verify configuration."""
        return self.send_alert(
            title="Test Alert",
            message="LeakHunter Swarm alert system is operational",
            severity="info",
            details={
                "status": "online",
                "test_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
        )


def main():
    """Main entry point for the Discord alert system."""
    parser = argparse.ArgumentParser(
        description="LeakHunter Swarm - Discord Alert System"
    )
    parser.add_argument(
        "--webhook",
        type=str,
        help="Discord webhook URL"
    )
    parser.add_argument(
        "--config",
        type=str,
        help="Path to configuration file"
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Send a test alert"
    )
    parser.add_argument(
        "--title",
        type=str,
        help="Alert title"
    )
    parser.add_argument(
        "--message",
        type=str,
        help="Alert message"
    )
    parser.add_argument(
        "--severity",
        type=str,
        choices=["info", "warning", "critical", "success"],
        default="info",
        help="Alert severity level"
    )
    parser.add_argument(
        "--scan-result",
        type=str,
        help="Path to scan result JSON file"
    )
    
    args = parser.parse_args()
    
    # Create alert system instance
    alert_system = DiscordAlertSystem(
        webhook_url=args.webhook,
        config_path=args.config
    )
    
    # Determine action
    if args.test:
        success = alert_system.test_alert()
    elif args.scan_result:
        # Load scan result and send alert
        with open(args.scan_result, 'r') as f:
            result = json.load(f)
        scan_type = result.get("scan_type", "unknown")
        success = alert_system.send_leak_alert(scan_type, result)
    elif args.title and args.message:
        success = alert_system.send_alert(args.title, args.message, args.severity)
    else:
        print("Please specify --test, --scan-result, or both --title and --message")
        parser.print_help()
        sys.exit(1)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

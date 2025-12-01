#!/usr/bin/env python3
"""
LoRa Mesh Communication Module
Sovereignty Communications Architecture

This module provides integration with Meshtastic LoRa mesh devices
for resilient alert delivery when traditional networks are unavailable.
"""

import logging
import os
import sys
from dataclasses import dataclass
from enum import Enum
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("lora_mesh")


class AlertSeverity(Enum):
    """Alert severity levels for prioritization."""
    CRITICAL = "critical"
    WARNING = "warning"
    INFO = "info"


@dataclass
class MeshConfig:
    """Configuration for LoRa mesh communication."""
    port: str = "/dev/ttyUSB0"
    region: str = "US"
    modem_preset: str = "LONG_FAST"
    hop_limit: int = 3
    broadcast: bool = True


def get_mesh_interface(config: MeshConfig):
    """
    Get a Meshtastic serial interface.
    
    Args:
        config: Mesh configuration settings
        
    Returns:
        SerialInterface instance or None if not available
    """
    try:
        import meshtastic
        import meshtastic.serial_interface
        
        interface = meshtastic.serial_interface.SerialInterface(config.port)
        logger.info(f"Connected to Meshtastic device on {config.port}")
        return interface
    except ImportError:
        logger.warning("Meshtastic library not installed. Install with: pip install meshtastic")
        return None
    except Exception as e:
        logger.error(f"Failed to connect to Meshtastic device: {e}")
        return None


def send_mesh_alert(
    message: str,
    config: Optional[MeshConfig] = None,
    severity: AlertSeverity = AlertSeverity.INFO
) -> bool:
    """
    Send an alert message through the LoRa mesh network.
    
    Args:
        message: The alert message to send
        config: Optional mesh configuration (uses defaults if None)
        severity: Alert severity level
        
    Returns:
        bool: True if message was sent successfully
    """
    if config is None:
        config = MeshConfig(
            port=os.environ.get("LORA_PORT", "/dev/ttyUSB0"),
            region=os.environ.get("LORA_REGION", "US"),
        )
    
    interface = get_mesh_interface(config)
    if interface is None:
        logger.error("No mesh interface available")
        return False
    
    try:
        # Format message with severity prefix
        formatted_message = f"[{severity.value.upper()}] {message}"
        
        # Truncate if too long for LoRa (max ~237 bytes for TEXT_MESSAGE)
        if len(formatted_message.encode()) > 230:
            formatted_message = formatted_message[:227] + "..."
            
        interface.sendText(formatted_message)
        logger.info(f"Sent mesh alert: {formatted_message[:50]}...")
        return True
        
    except Exception as e:
        logger.error(f"LoRa mesh send failed: {e}")
        return False
        
    finally:
        try:
            interface.close()
        except Exception:
            pass


def broadcast_system_alert(alert_type: str, details: str) -> bool:
    """
    Broadcast a system alert to all mesh nodes.
    
    Args:
        alert_type: Type of alert (e.g., "CRITICAL", "WARNING", "INFO")
        details: Alert details and context
        
    Returns:
        bool: True if broadcast was successful
    """
    severity_map = {
        "CRITICAL": AlertSeverity.CRITICAL,
        "WARNING": AlertSeverity.WARNING,
        "INFO": AlertSeverity.INFO,
    }
    
    severity = severity_map.get(alert_type.upper(), AlertSeverity.INFO)
    return send_mesh_alert(details, severity=severity)


def check_mesh_health() -> dict:
    """
    Check the health status of the LoRa mesh network.
    
    Returns:
        dict: Health status including connectivity and node info
    """
    config = MeshConfig(
        port=os.environ.get("LORA_PORT", "/dev/ttyUSB0"),
    )
    
    interface = get_mesh_interface(config)
    if interface is None:
        return {
            "status": "unhealthy",
            "connected": False,
            "error": "Cannot connect to Meshtastic device"
        }
    
    try:
        my_info = interface.getMyNodeInfo()
        nodes = interface.nodes
        
        return {
            "status": "healthy",
            "connected": True,
            "node_id": my_info.get("user", {}).get("id", "unknown"),
            "node_name": my_info.get("user", {}).get("longName", "unknown"),
            "connected_nodes": len(nodes) if nodes else 0,
            "battery_level": my_info.get("deviceMetrics", {}).get("batteryLevel", -1),
        }
        
    except Exception as e:
        return {
            "status": "unhealthy",
            "connected": False,
            "error": str(e)
        }
        
    finally:
        try:
            interface.close()
        except Exception:
            pass


def main():
    """Main entry point for CLI usage."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="LoRa Mesh Communication Tool for Sovereignty Architecture"
    )
    parser.add_argument(
        "action",
        choices=["send", "health"],
        help="Action to perform"
    )
    parser.add_argument(
        "--message", "-m",
        help="Message to send (required for 'send' action)"
    )
    parser.add_argument(
        "--severity", "-s",
        choices=["critical", "warning", "info"],
        default="info",
        help="Alert severity level"
    )
    parser.add_argument(
        "--port", "-p",
        default=os.environ.get("LORA_PORT", "/dev/ttyUSB0"),
        help="Serial port for Meshtastic device"
    )
    
    args = parser.parse_args()
    
    if args.action == "send":
        if not args.message:
            parser.error("--message is required for 'send' action")
            
        config = MeshConfig(port=args.port)
        severity = AlertSeverity(args.severity)
        
        success = send_mesh_alert(args.message, config=config, severity=severity)
        sys.exit(0 if success else 1)
        
    elif args.action == "health":
        health = check_mesh_health()
        print(f"Status: {health['status']}")
        print(f"Connected: {health['connected']}")
        
        if health['connected']:
            print(f"Node ID: {health.get('node_id', 'N/A')}")
            print(f"Node Name: {health.get('node_name', 'N/A')}")
            print(f"Connected Nodes: {health.get('connected_nodes', 0)}")
            if health.get('battery_level', -1) >= 0:
                print(f"Battery: {health['battery_level']}%")
        else:
            print(f"Error: {health.get('error', 'Unknown error')}")
            
        sys.exit(0 if health['status'] == 'healthy' else 1)


if __name__ == "__main__":
    main()

"""
Thermal Sentinel Antibody Agent
Example agent that monitors thermal conditions and responds to coordinator commands.

This is an example implementation showing the antibody agent contract:
1. Send heartbeats periodically
2. Send alerts when conditions are detected
3. Listen for commands from the coordinator
"""

import asyncio
import json
import os
import time
from nats.aio.client import Client as NATS


NODE_NAME = os.environ.get("NODE_NAME", "nova")
AGENT_NAME = "thermal-sentinel"
NATS_URL = os.environ.get("NATS_URL", "nats://nats:4222")


async def get_thermal_metrics() -> dict:
    """Get current thermal metrics. Returns mock data if psutil unavailable."""
    try:
        import psutil
        temps = psutil.sensors_temperatures()
        cpu_temp = temps.get("coretemp", [{}])[0].current if temps.get("coretemp") else 45.0
    except (ImportError, AttributeError, IndexError):
        # Mock data for environments without psutil or sensors
        cpu_temp = 45.0
    
    return {
        "cpu_temp": cpu_temp,
        "gpu_temp": None,  # Add GPU monitoring if available
        "node_metrics": {
            "uptime": time.time(),
        }
    }


async def heartbeat_loop(nc: NATS) -> None:
    """Send periodic heartbeats to the coordinator."""
    while True:
        try:
            metrics = await get_thermal_metrics()
            payload = {
                "agent": AGENT_NAME,
                "node": NODE_NAME,
                "status": "healthy",
                "metrics": metrics,
            }
            await nc.publish(
                f"antibody.heartbeat.{AGENT_NAME}",
                json.dumps(payload).encode(),
            )
            print(f"[{AGENT_NAME}] Sent heartbeat: CPU={metrics.get('cpu_temp')}")
        except Exception as e:
            print(f"[{AGENT_NAME}] Error sending heartbeat: {e}")
        
        await asyncio.sleep(10)


async def command_handler(msg) -> None:
    """Handle commands from the coordinator."""
    try:
        cmd = json.loads(msg.data.decode())
        print(f"[{AGENT_NAME}] Received command: {cmd}")
        
        for action in cmd.get("actions", []):
            action_type = action.get("action")
            params = action.get("params", {})
            
            if action_type == "throttle":
                print(f"[{AGENT_NAME}] Executing throttle on node: {params.get('node')}")
                # Implement CPU/GPU throttling logic here
                
            elif action_type == "redistribute":
                print(f"[{AGENT_NAME}] Redistributing workload from {params.get('from')} to {params.get('to')}")
                # Implement workload redistribution logic here
                
            elif action_type == "alert":
                severity = params.get("severity", "info")
                print(f"[{AGENT_NAME}] Alert ({severity}): Thermal event logged")
                # Implement alert notification logic here
                
            else:
                print(f"[{AGENT_NAME}] Unknown action: {action_type}")
                
    except Exception as e:
        print(f"[{AGENT_NAME}] Error handling command: {e}")


async def command_listener(nc: NATS) -> None:
    """Subscribe to commands from the coordinator."""
    await nc.subscribe(f"antibody.cmd.{AGENT_NAME}", cb=command_handler)
    print(f"[{AGENT_NAME}] Listening for commands on antibody.cmd.{AGENT_NAME}")


async def main() -> None:
    """Main entry point for the thermal sentinel agent."""
    print(f"[{AGENT_NAME}] Starting on node {NODE_NAME}")
    print(f"[{AGENT_NAME}] Connecting to NATS at {NATS_URL}")
    
    nc = NATS()
    await nc.connect(NATS_URL)
    print(f"[{AGENT_NAME}] Connected to NATS")
    
    # Run heartbeat and command listener concurrently
    await asyncio.gather(
        heartbeat_loop(nc),
        command_listener(nc),
    )


if __name__ == "__main__":
    asyncio.run(main())

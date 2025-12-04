#!/usr/bin/env python3
"""
SKOS Thermal Sentinel Agent v0.1.0
Monitors CPU/GPU temperatures and sends alerts to the Antibody Coordinator.

This agent:
- Monitors CPU/GPU temps every 5 seconds
- Sends heartbeat every 10 seconds
- Alerts on overheat (>80°C configurable)
- Executes throttle/redistribute commands
- Works on bare metal, VMs, or containers

Architecture:
    Hardware Sensors (CPU/GPU)
         ↓
    Thermal Sentinel Agent (this file)
         ↓ (heartbeats + alerts via NATS)
    Antibody Coordinator
         ↓ (commands via NATS)
    Healing Actions (throttle, redistribute)

Copyright (c) 2024 Strategickhaos DAO LLC
License: MIT
"""

import asyncio
import json
import logging
import os
import signal
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

# NATS will be imported dynamically to support air-gapped mode
try:
    import nats
    NATS_AVAILABLE = True
except ImportError:
    NATS_AVAILABLE = False
    logging.warning("NATS not available - running in simulation mode")

# Configuration
NATS_URL = os.getenv("NATS_URL", "nats://localhost:4222")
NODE_NAME = os.getenv("NODE_NAME", "nova")
AGENT_ID = os.getenv("AGENT_ID", f"thermal-sentinel-{NODE_NAME}")
MONITOR_INTERVAL = int(os.getenv("MONITOR_INTERVAL", "5"))
HEARTBEAT_INTERVAL = int(os.getenv("HEARTBEAT_INTERVAL", "10"))
WARNING_TEMP = float(os.getenv("WARNING_TEMP", "75"))
CRITICAL_TEMP = float(os.getenv("CRITICAL_TEMP", "85"))
EMERGENCY_TEMP = float(os.getenv("EMERGENCY_TEMP", "95"))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL.upper()),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("skos.thermal")


class ThermalSensor:
    """
    Reads temperature from system sensors.
    Supports Linux thermal zones and lm-sensors.
    """
    
    def __init__(self):
        self.thermal_zones: list[Path] = []
        self.hwmon_paths: list[Path] = []
        self._discover_sensors()
    
    def _discover_sensors(self) -> None:
        """Discover available temperature sensors."""
        # Linux thermal zones
        thermal_base = Path("/sys/class/thermal")
        if thermal_base.exists():
            for zone in thermal_base.glob("thermal_zone*"):
                temp_file = zone / "temp"
                if temp_file.exists():
                    self.thermal_zones.append(temp_file)
                    logger.info(f"Found thermal zone: {zone.name}")
        
        # hwmon sensors (for GPU, etc.)
        hwmon_base = Path("/sys/class/hwmon")
        if hwmon_base.exists():
            for hwmon in hwmon_base.glob("hwmon*"):
                for temp in hwmon.glob("temp*_input"):
                    self.hwmon_paths.append(temp)
                    logger.info(f"Found hwmon sensor: {temp}")
    
    def read_cpu_temp(self) -> float:
        """Read CPU temperature in Celsius."""
        temps = []
        
        # Read from thermal zones
        for zone in self.thermal_zones:
            try:
                temp_raw = zone.read_text().strip()
                temp_c = int(temp_raw) / 1000  # Convert millidegrees
                temps.append(temp_c)
            except Exception as e:
                logger.debug(f"Error reading {zone}: {e}")
        
        # Read from hwmon (first few are usually CPU)
        for path in self.hwmon_paths[:3]:
            try:
                temp_raw = path.read_text().strip()
                temp_c = int(temp_raw) / 1000
                temps.append(temp_c)
            except Exception as e:
                logger.debug(f"Error reading {path}: {e}")
        
        if temps:
            return max(temps)  # Return highest CPU temp
        
        # Fallback: try lm-sensors
        return self._read_from_sensors("cpu")
    
    def read_gpu_temp(self) -> float:
        """Read GPU temperature in Celsius."""
        # Try NVIDIA GPU
        try:
            result = subprocess.run(
                ["nvidia-smi", "--query-gpu=temperature.gpu",
                 "--format=csv,noheader,nounits"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                return float(result.stdout.strip())
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass
        
        # Try AMD GPU
        try:
            amd_temp = Path("/sys/class/drm/card0/device/hwmon/hwmon0/temp1_input")
            if amd_temp.exists():
                temp_raw = amd_temp.read_text().strip()
                return int(temp_raw) / 1000
        except Exception:
            pass
        
        # Fallback: try lm-sensors
        return self._read_from_sensors("gpu")
    
    def _read_from_sensors(self, sensor_type: str) -> float:
        """Read temperature using lm-sensors command."""
        try:
            result = subprocess.run(
                ["sensors", "-j"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                data = json.loads(result.stdout)
                # Parse sensors output for temperature
                for adapter_name, adapter_data in data.items():
                    if not isinstance(adapter_data, dict):
                        continue
                    for sensor_name, sensor_data in adapter_data.items():
                        if not isinstance(sensor_data, dict):
                            continue
                        for key, value in sensor_data.items():
                            if "temp" in key.lower() and "input" in key.lower():
                                return float(value)
        except (FileNotFoundError, subprocess.TimeoutExpired, json.JSONDecodeError):
            pass
        
        # Return simulated temp if no sensors found
        return 45.0 + (hash(sensor_type) % 10)


class ThermalSentinelAgent:
    """
    The Thermal Sentinel antibody agent.
    
    Monitors temperatures and sends alerts when thresholds are exceeded.
    Listens for commands from the coordinator and executes throttling.
    """
    
    def __init__(self):
        self.nc: Any = None  # NATS connection
        self.running = False
        self.sensor = ThermalSensor()
        
        # Current state
        self.cpu_temp = 0.0
        self.gpu_temp = 0.0
        self.last_alert_cpu: Optional[datetime] = None
        self.last_alert_gpu: Optional[datetime] = None
        self.throttle_level = 0  # 0-100%
        
        # Alert cooldown (don't spam alerts)
        self.alert_cooldown_seconds = 60
    
    async def connect(self) -> bool:
        """Connect to NATS."""
        if not NATS_AVAILABLE:
            logger.info("Running in simulation mode (no NATS)")
            return True
        
        try:
            self.nc = await nats.connect(NATS_URL)
            logger.info(f"Connected to NATS at {NATS_URL}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to NATS: {e}")
            return False
    
    async def disconnect(self) -> None:
        """Disconnect from NATS."""
        if self.nc and NATS_AVAILABLE:
            await self.nc.close()
            logger.info("Disconnected from NATS")
    
    async def start(self) -> None:
        """Start the thermal sentinel agent."""
        self.running = True
        logger.info("Starting Thermal Sentinel Agent...")
        
        if not await self.connect():
            logger.warning("Running without NATS connection")
        
        # Start background tasks
        tasks = [
            asyncio.create_task(self._heartbeat_loop()),
            asyncio.create_task(self._monitor_loop()),
        ]
        
        if NATS_AVAILABLE and self.nc:
            tasks.append(asyncio.create_task(self._command_listener()))
        
        logger.info("Thermal Sentinel Agent running")
        
        try:
            await asyncio.gather(*tasks)
        except asyncio.CancelledError:
            logger.info("Agent tasks cancelled")
    
    async def stop(self) -> None:
        """Stop the agent."""
        logger.info("Stopping Thermal Sentinel Agent...")
        self.running = False
        await self.disconnect()
    
    async def _heartbeat_loop(self) -> None:
        """Send regular heartbeats to the coordinator."""
        while self.running:
            heartbeat = {
                "agent_id": AGENT_ID,
                "agent_type": "thermal_sentinel",
                "node": NODE_NAME,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "cpu_temp": self.cpu_temp,
                "gpu_temp": self.gpu_temp,
                "throttle_level": self.throttle_level,
                "metadata": {
                    "warning_temp": WARNING_TEMP,
                    "critical_temp": CRITICAL_TEMP,
                    "emergency_temp": EMERGENCY_TEMP
                }
            }
            
            if NATS_AVAILABLE and self.nc:
                try:
                    subject = f"skos.heartbeat.{NODE_NAME}"
                    await self.nc.publish(subject, json.dumps(heartbeat).encode())
                    logger.debug(f"Sent heartbeat: CPU={self.cpu_temp:.1f}°C GPU={self.gpu_temp:.1f}°C")
                except Exception as e:
                    logger.error(f"Failed to send heartbeat: {e}")
            else:
                logger.info(f"HEARTBEAT: CPU={self.cpu_temp:.1f}°C GPU={self.gpu_temp:.1f}°C")
            
            await asyncio.sleep(HEARTBEAT_INTERVAL)
    
    async def _monitor_loop(self) -> None:
        """Monitor temperatures and send alerts."""
        while self.running:
            # Read temperatures
            self.cpu_temp = self.sensor.read_cpu_temp()
            self.gpu_temp = self.sensor.read_gpu_temp()
            
            logger.debug(f"Temps: CPU={self.cpu_temp:.1f}°C GPU={self.gpu_temp:.1f}°C")
            
            # Check CPU temperature
            await self._check_temp("cpu", self.cpu_temp, self.last_alert_cpu)
            
            # Check GPU temperature
            await self._check_temp("gpu", self.gpu_temp, self.last_alert_gpu)
            
            await asyncio.sleep(MONITOR_INTERVAL)
    
    async def _check_temp(
        self,
        sensor: str,
        temp: float,
        last_alert: Optional[datetime]
    ) -> None:
        """Check temperature and send alert if needed."""
        now = datetime.now(timezone.utc)
        
        # Check cooldown
        if last_alert:
            delta = (now - last_alert).total_seconds()
            if delta < self.alert_cooldown_seconds:
                return
        
        severity = None
        if temp >= EMERGENCY_TEMP:
            severity = "emergency"
        elif temp >= CRITICAL_TEMP:
            severity = "critical"
        elif temp >= WARNING_TEMP:
            severity = "warning"
        
        if severity:
            await self._send_alert(
                alert_type="thermal",
                severity=severity,
                message=f"{sensor.upper()} temperature {temp:.1f}°C exceeds {severity} threshold",
                details={
                    "sensor": sensor,
                    "temperature": temp,
                    "threshold": {
                        "warning": WARNING_TEMP,
                        "critical": CRITICAL_TEMP,
                        "emergency": EMERGENCY_TEMP
                    }[severity]
                }
            )
            
            # Update last alert time
            if sensor == "cpu":
                self.last_alert_cpu = now
            else:
                self.last_alert_gpu = now
    
    async def _send_alert(
        self,
        alert_type: str,
        severity: str,
        message: str,
        details: dict
    ) -> None:
        """Send an alert to the coordinator."""
        alert = {
            "agent_id": AGENT_ID,
            "type": alert_type,
            "severity": severity,
            "node": NODE_NAME,
            "message": message,
            "details": details,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        logger.warning(f"ALERT [{severity}]: {message}")
        
        if NATS_AVAILABLE and self.nc:
            try:
                subject = f"skos.alert.{NODE_NAME}"
                await self.nc.publish(subject, json.dumps(alert).encode())
                logger.info(f"Alert sent to coordinator")
            except Exception as e:
                logger.error(f"Failed to send alert: {e}")
        else:
            logger.info(f"ALERT (simulated): {json.dumps(alert, indent=2)}")
    
    async def _command_listener(self) -> None:
        """Listen for commands from the coordinator."""
        if not self.nc:
            return
        
        async def command_handler(msg):
            try:
                data = json.loads(msg.data.decode())
                await self._execute_command(data)
            except Exception as e:
                logger.error(f"Error processing command: {e}")
        
        subject = f"skos.command.{NODE_NAME}"
        await self.nc.subscribe(subject, cb=command_handler)
        logger.info(f"Listening for commands on {subject}")
        
        # Keep the subscription alive
        while self.running:
            await asyncio.sleep(1)
    
    async def _execute_command(self, command: dict) -> None:
        """Execute a command from the coordinator."""
        action_type = command.get("action_type")
        parameters = command.get("parameters", {})
        
        logger.info(f"Executing command: {action_type}")
        
        if action_type == "throttle_10":
            await self._throttle(10)
        elif action_type == "throttle_50":
            await self._throttle(50)
        elif action_type == "throttle_100":
            await self._throttle(100)
        elif action_type == "redistribute":
            await self._redistribute()
        elif action_type == "shutdown_non_essential":
            await self._shutdown_non_essential()
        elif action_type == "reset_throttle":
            await self._throttle(0)
        else:
            logger.warning(f"Unknown command: {action_type}")
    
    async def _throttle(self, level: int) -> None:
        """
        Throttle CPU/GPU performance.
        Level is 0-100 (0 = no throttle, 100 = max throttle).
        """
        self.throttle_level = level
        logger.info(f"Setting throttle level to {level}%")
        
        if level == 0:
            # Remove throttling
            try:
                subprocess.run(
                    ["cpupower", "frequency-set", "-g", "performance"],
                    capture_output=True,
                    timeout=5
                )
            except FileNotFoundError:
                pass
        else:
            # Apply throttling via CPU governor
            try:
                # Calculate target frequency
                # This is simplified - real implementation would be more sophisticated
                governor = "powersave" if level >= 50 else "conservative"
                subprocess.run(
                    ["cpupower", "frequency-set", "-g", governor],
                    capture_output=True,
                    timeout=5
                )
            except FileNotFoundError:
                logger.warning("cpupower not available - throttle simulated")
    
    async def _redistribute(self) -> None:
        """Redistribute workload to other nodes."""
        logger.info("Initiating workload redistribution")
        
        # In a real implementation, this would:
        # 1. Identify running containers/services
        # 2. Signal orchestrator to move workloads
        # 3. Gracefully migrate services to cooler nodes
        
        # For now, we just log the action
        logger.info("Workload redistribution requested (implementation pending)")
    
    async def _shutdown_non_essential(self) -> None:
        """Shutdown non-essential services to reduce heat."""
        logger.info("Shutting down non-essential services")
        
        # In a real implementation, this would:
        # 1. Identify non-essential services from config
        # 2. Gracefully stop them
        # 3. Report which services were stopped
        
        # Example: stop development containers
        try:
            # First get the list of non-essential containers
            result = subprocess.run(
                ["docker", "ps", "-q", "--filter", "label=essential=false"],
                capture_output=True,
                text=True,
                timeout=10
            )
            container_ids = result.stdout.strip()
            
            # Only stop if there are containers to stop
            if container_ids:
                subprocess.run(
                    ["docker", "stop"] + container_ids.split(),
                    capture_output=True,
                    timeout=30
                )
                logger.info(f"Stopped non-essential containers: {container_ids}")
            else:
                logger.info("No non-essential containers to stop")
        except Exception as e:
            logger.warning(f"Failed to stop containers: {e}")


async def main():
    """Main entry point."""
    agent = ThermalSentinelAgent()
    
    # Set up signal handlers
    loop = asyncio.get_event_loop()
    
    def signal_handler():
        asyncio.create_task(agent.stop())
    
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, signal_handler)
    
    logger.info("=" * 60)
    logger.info("  SKOS Thermal Sentinel Agent v0.1.0")
    logger.info("  Sovereign Khaos Operating System")
    logger.info("=" * 60)
    logger.info(f"  NATS URL: {NATS_URL}")
    logger.info(f"  Node Name: {NODE_NAME}")
    logger.info(f"  Agent ID: {AGENT_ID}")
    logger.info(f"  Monitor Interval: {MONITOR_INTERVAL}s")
    logger.info(f"  Thresholds: Warning={WARNING_TEMP}°C "
                f"Critical={CRITICAL_TEMP}°C Emergency={EMERGENCY_TEMP}°C")
    logger.info("=" * 60)
    
    await agent.start()


if __name__ == "__main__":
    asyncio.run(main())

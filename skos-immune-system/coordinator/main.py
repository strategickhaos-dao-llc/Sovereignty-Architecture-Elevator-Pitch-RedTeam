#!/usr/bin/env python3
"""
SKOS Antibody Coordinator v0.1.0
The autonomous immune system brain for sovereign infrastructure.

This coordinator:
- Receives heartbeats from all antibody agents
- Processes alerts (thermal, storage, mesh, loops)
- Applies healing strategies autonomously
- Dispatches commands back to agents
- Maintains full audit trail in NATS JetStream

Architecture:
    Nova/Lyra/Athena Nodes
         ↓
    Antibody Agents (thermal, storage, mesh, loop)
         ↓ (heartbeats + alerts via NATS)
    Antibody Coordinator (this file - the brain)
         ↓ (commands via NATS)
    Healing Actions (throttle, redistribute, failover)
         ↓
    Audit Log (immutable trail in JetStream)

Copyright (c) 2024 Strategickhaos DAO LLC
License: MIT
"""

import asyncio
import json
import logging
import os
import signal
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional

# NATS will be imported dynamically to support air-gapped mode
try:
    import nats
    from nats.js.api import StreamConfig, RetentionPolicy
    NATS_AVAILABLE = True
except ImportError:
    NATS_AVAILABLE = False
    logging.warning("NATS not available - running in simulation mode")

# Configuration
NATS_URL = os.getenv("NATS_URL", "nats://localhost:4222")
NODE_NAME = os.getenv("NODE_NAME", "coordinator")
HEARTBEAT_TIMEOUT_SECONDS = int(os.getenv("HEARTBEAT_TIMEOUT", "30"))
AUDIT_STREAM = os.getenv("AUDIT_STREAM", "SKOS_AUDIT")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL.upper()),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("skos.coordinator")


class AlertSeverity(Enum):
    """Severity levels for alerts."""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"


class AlertType(Enum):
    """Types of alerts the coordinator can process."""
    THERMAL = "thermal"
    STORAGE = "storage"
    MESH = "mesh"
    LOOP = "loop"
    HEARTBEAT_MISSING = "heartbeat_missing"


class NodeStatus(Enum):
    """Status of a node in the mesh."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    CRITICAL = "critical"
    OFFLINE = "offline"


@dataclass
class NodeState:
    """State tracking for a single node."""
    name: str
    status: NodeStatus = NodeStatus.HEALTHY
    last_heartbeat: Optional[datetime] = None
    cpu_temp: float = 0.0
    gpu_temp: float = 0.0
    storage_percent: float = 0.0
    active_alerts: list = field(default_factory=list)
    metadata: dict = field(default_factory=dict)


@dataclass
class AgentState:
    """State tracking for an antibody agent."""
    agent_id: str
    agent_type: str
    node: str
    last_heartbeat: Optional[datetime] = None
    status: str = "unknown"
    metadata: dict = field(default_factory=dict)


@dataclass
class HealingAction:
    """A healing action to be executed."""
    action_id: str
    action_type: str
    target_node: str
    target_agent: Optional[str]
    parameters: dict
    created_at: datetime
    executed_at: Optional[datetime] = None
    result: Optional[str] = None


class CircuitBreaker:
    """
    Circuit breaker to prevent infinite healing loops.
    
    If an action is triggered too many times in a short period,
    the circuit opens and blocks further actions.
    """
    
    def __init__(
        self,
        max_failures: int = 5,
        reset_timeout_seconds: int = 300
    ):
        self.max_failures = max_failures
        self.reset_timeout = reset_timeout_seconds
        self.failures: dict[str, list[datetime]] = {}
        self.open_circuits: dict[str, datetime] = {}
    
    def is_open(self, action_key: str) -> bool:
        """Check if circuit is open for this action."""
        if action_key in self.open_circuits:
            opened_at = self.open_circuits[action_key]
            if (datetime.now(timezone.utc) - opened_at).total_seconds() < self.reset_timeout:
                return True
            else:
                # Reset circuit
                del self.open_circuits[action_key]
                if action_key in self.failures:
                    del self.failures[action_key]
        return False
    
    def record_failure(self, action_key: str) -> None:
        """Record a failure for this action."""
        now = datetime.now(timezone.utc)
        
        if action_key not in self.failures:
            self.failures[action_key] = []
        
        # Clean old failures (older than reset_timeout)
        self.failures[action_key] = [
            f for f in self.failures[action_key]
            if (now - f).total_seconds() < self.reset_timeout
        ]
        
        self.failures[action_key].append(now)
        
        # Open circuit if too many failures
        if len(self.failures[action_key]) >= self.max_failures:
            self.open_circuits[action_key] = now
            logger.warning(f"Circuit breaker OPEN for {action_key}")
    
    def record_success(self, action_key: str) -> None:
        """Record a success - clears failure history."""
        if action_key in self.failures:
            del self.failures[action_key]


class AntibodyCoordinator:
    """
    The main coordinator for the SKOS immune system.
    
    This is the brain that:
    1. Tracks node and agent state
    2. Receives and processes alerts
    3. Determines and executes healing actions
    4. Maintains audit trail
    """
    
    def __init__(self):
        self.nc: Any = None  # NATS connection
        self.js: Any = None  # JetStream context
        self.running = False
        
        # State tracking
        self.nodes: dict[str, NodeState] = {}
        self.agents: dict[str, AgentState] = {}
        self.pending_actions: list[HealingAction] = []
        self.executed_actions: list[HealingAction] = []
        
        # Healing configuration
        self.circuit_breaker = CircuitBreaker()
        self.healing_policies = self._load_healing_policies()
    
    def _load_healing_policies(self) -> dict:
        """Load healing policies from config or environment."""
        return {
            "thermal": {
                "warning_threshold": 75,
                "critical_threshold": 85,
                "emergency_threshold": 95,
                "actions": {
                    "warning": ["throttle_10"],
                    "critical": ["throttle_50", "redistribute"],
                    "emergency": ["shutdown_non_essential", "failover"]
                }
            },
            "storage": {
                "warning_threshold": 80,
                "critical_threshold": 90,
                "emergency_threshold": 95,
                "actions": {
                    "warning": ["cleanup_temp"],
                    "critical": ["cleanup_logs", "archive_old"],
                    "emergency": ["emergency_cleanup", "alert_human"]
                }
            },
            "mesh": {
                "reconnect_attempts": 3,
                "reconnect_delay_seconds": 5,
                "actions": {
                    "tunnel_down": ["restart_wireguard", "regenerate_config"],
                    "peer_unreachable": ["ping_peer", "failover_route"]
                }
            },
            "loop": {
                "max_chain_depth": 10,
                "max_iterations": 100,
                "actions": {
                    "depth_exceeded": ["circuit_break"],
                    "iterations_exceeded": ["reset_chain"]
                }
            }
        }
    
    async def connect(self) -> bool:
        """Connect to NATS and set up JetStream."""
        if not NATS_AVAILABLE:
            logger.info("Running in simulation mode (no NATS)")
            return True
        
        try:
            self.nc = await nats.connect(NATS_URL)
            self.js = self.nc.jetstream()
            
            # Create audit stream
            try:
                await self.js.add_stream(
                    config=StreamConfig(
                        name=AUDIT_STREAM,
                        subjects=[f"{AUDIT_STREAM}.*"],
                        retention=RetentionPolicy.LIMITS,
                        max_msgs=1000000,
                        max_bytes=1024 * 1024 * 1024,  # 1GB
                    )
                )
                logger.info(f"Created audit stream: {AUDIT_STREAM}")
            except Exception:
                logger.info(f"Audit stream {AUDIT_STREAM} already exists")
            
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
        """Start the coordinator."""
        self.running = True
        logger.info("Starting Antibody Coordinator...")
        
        if not await self.connect():
            logger.error("Failed to connect - running in degraded mode")
        
        # Start background tasks
        tasks = [
            asyncio.create_task(self._heartbeat_monitor()),
            asyncio.create_task(self._alert_processor()),
            asyncio.create_task(self._action_executor()),
        ]
        
        if NATS_AVAILABLE and self.nc:
            tasks.append(asyncio.create_task(self._subscribe_heartbeats()))
            tasks.append(asyncio.create_task(self._subscribe_alerts()))
        
        logger.info("Antibody Coordinator running")
        
        try:
            await asyncio.gather(*tasks)
        except asyncio.CancelledError:
            logger.info("Coordinator tasks cancelled")
    
    async def stop(self) -> None:
        """Stop the coordinator."""
        logger.info("Stopping Antibody Coordinator...")
        self.running = False
        await self.disconnect()
    
    async def _subscribe_heartbeats(self) -> None:
        """Subscribe to heartbeat messages from agents."""
        if not self.nc:
            return
        
        async def heartbeat_handler(msg):
            try:
                data = json.loads(msg.data.decode())
                await self._process_heartbeat(data)
            except Exception as e:
                logger.error(f"Error processing heartbeat: {e}")
        
        await self.nc.subscribe("skos.heartbeat.*", cb=heartbeat_handler)
        logger.info("Subscribed to heartbeats")
    
    async def _subscribe_alerts(self) -> None:
        """Subscribe to alert messages from agents."""
        if not self.nc:
            return
        
        async def alert_handler(msg):
            try:
                data = json.loads(msg.data.decode())
                await self._process_alert(data)
            except Exception as e:
                logger.error(f"Error processing alert: {e}")
        
        await self.nc.subscribe("skos.alert.*", cb=alert_handler)
        logger.info("Subscribed to alerts")
    
    async def _process_heartbeat(self, data: dict) -> None:
        """Process a heartbeat from an agent."""
        agent_id = data.get("agent_id")
        agent_type = data.get("agent_type")
        node = data.get("node")
        
        if not all([agent_id, agent_type, node]):
            logger.warning(f"Invalid heartbeat data: {data}")
            return
        
        now = datetime.now(timezone.utc)
        
        # Update agent state
        if agent_id not in self.agents:
            self.agents[agent_id] = AgentState(
                agent_id=agent_id,
                agent_type=agent_type,
                node=node
            )
            logger.info(f"New agent registered: {agent_id} ({agent_type}) on {node}")
        
        self.agents[agent_id].last_heartbeat = now
        self.agents[agent_id].status = "healthy"
        self.agents[agent_id].metadata = data.get("metadata", {})
        
        # Update node state
        if node not in self.nodes:
            self.nodes[node] = NodeState(name=node)
            logger.info(f"New node registered: {node}")
        
        self.nodes[node].last_heartbeat = now
        
        # Update node metrics from heartbeat
        if "cpu_temp" in data:
            self.nodes[node].cpu_temp = data["cpu_temp"]
        if "gpu_temp" in data:
            self.nodes[node].gpu_temp = data["gpu_temp"]
        if "storage_percent" in data:
            self.nodes[node].storage_percent = data["storage_percent"]
        
        logger.debug(f"Heartbeat from {agent_id} on {node}")
    
    async def _process_alert(self, data: dict) -> None:
        """Process an alert from an agent."""
        alert_type = data.get("type")
        severity = data.get("severity", "warning")
        node = data.get("node")
        message = data.get("message", "")
        details = data.get("details", {})
        
        logger.warning(f"ALERT [{severity}] {alert_type} on {node}: {message}")
        
        # Log to audit trail
        await self._audit_log("alert_received", {
            "type": alert_type,
            "severity": severity,
            "node": node,
            "message": message,
            "details": details
        })
        
        # Determine healing actions
        actions = self._determine_healing_actions(
            alert_type=alert_type,
            severity=severity,
            node=node,
            details=details
        )
        
        # Queue actions
        for action in actions:
            self.pending_actions.append(action)
            logger.info(f"Queued healing action: {action.action_type} for {node}")
    
    def _determine_healing_actions(
        self,
        alert_type: str,
        severity: str,
        node: str,
        details: dict
    ) -> list[HealingAction]:
        """Determine appropriate healing actions based on alert."""
        actions = []
        now = datetime.now(timezone.utc)
        
        policy = self.healing_policies.get(alert_type, {})
        action_map = policy.get("actions", {})
        action_types = action_map.get(severity, [])
        
        for action_type in action_types:
            action_key = f"{node}:{alert_type}:{action_type}"
            
            # Check circuit breaker
            if self.circuit_breaker.is_open(action_key):
                logger.warning(f"Circuit breaker open for {action_key}")
                continue
            
            action = HealingAction(
                action_id=f"{action_key}:{now.timestamp()}",
                action_type=action_type,
                target_node=node,
                target_agent=None,
                parameters=details,
                created_at=now
            )
            actions.append(action)
        
        return actions
    
    async def _heartbeat_monitor(self) -> None:
        """Monitor for missing heartbeats."""
        while self.running:
            await asyncio.sleep(10)  # Check every 10 seconds
            
            now = datetime.now(timezone.utc)
            
            for agent_id, agent in self.agents.items():
                if agent.last_heartbeat:
                    delta = (now - agent.last_heartbeat).total_seconds()
                    if delta > HEARTBEAT_TIMEOUT_SECONDS:
                        if agent.status != "offline":
                            logger.warning(
                                f"Agent {agent_id} missed heartbeat "
                                f"(last seen {delta}s ago)"
                            )
                            agent.status = "offline"
                            
                            # Generate alert
                            await self._process_alert({
                                "type": "heartbeat_missing",
                                "severity": "critical",
                                "node": agent.node,
                                "message": f"Agent {agent_id} offline",
                                "details": {"agent_id": agent_id}
                            })
    
    async def _alert_processor(self) -> None:
        """Process alerts from the queue."""
        while self.running:
            await asyncio.sleep(1)
            # Alerts are processed inline in _subscribe_alerts
    
    async def _action_executor(self) -> None:
        """Execute pending healing actions."""
        while self.running:
            await asyncio.sleep(1)
            
            while self.pending_actions:
                action = self.pending_actions.pop(0)
                
                try:
                    result = await self._execute_action(action)
                    action.executed_at = datetime.now(timezone.utc)
                    action.result = result
                    
                    # Record success
                    action_key = f"{action.target_node}:{action.action_type}"
                    self.circuit_breaker.record_success(action_key)
                    
                    logger.info(
                        f"Executed action {action.action_type} "
                        f"on {action.target_node}: {result}"
                    )
                    
                except Exception as e:
                    action.result = f"FAILED: {e}"
                    
                    # Record failure
                    action_key = f"{action.target_node}:{action.action_type}"
                    self.circuit_breaker.record_failure(action_key)
                    
                    logger.error(
                        f"Failed to execute {action.action_type} "
                        f"on {action.target_node}: {e}"
                    )
                
                self.executed_actions.append(action)
                
                # Audit log
                await self._audit_log("action_executed", {
                    "action_id": action.action_id,
                    "action_type": action.action_type,
                    "target_node": action.target_node,
                    "result": action.result
                })
    
    async def _execute_action(self, action: HealingAction) -> str:
        """Execute a single healing action."""
        # Send command to agent via NATS
        if NATS_AVAILABLE and self.nc:
            command = {
                "action_id": action.action_id,
                "action_type": action.action_type,
                "parameters": action.parameters,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            
            subject = f"skos.command.{action.target_node}"
            await self.nc.publish(subject, json.dumps(command).encode())
            
            return f"Command sent to {action.target_node}"
        else:
            # Simulation mode
            return f"SIMULATED: {action.action_type}"
    
    async def _audit_log(self, event_type: str, data: dict) -> None:
        """Write to the audit log."""
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": event_type,
            "coordinator": NODE_NAME,
            "data": data
        }
        
        if NATS_AVAILABLE and self.js:
            try:
                subject = f"{AUDIT_STREAM}.{event_type}"
                await self.js.publish(subject, json.dumps(entry).encode())
            except Exception as e:
                logger.error(f"Failed to write audit log: {e}")
        else:
            logger.info(f"AUDIT: {event_type} - {json.dumps(data)}")
    
    def get_status(self) -> dict:
        """Get current coordinator status."""
        return {
            "running": self.running,
            "nodes": {
                name: {
                    "status": node.status.value,
                    "cpu_temp": node.cpu_temp,
                    "gpu_temp": node.gpu_temp,
                    "storage_percent": node.storage_percent,
                    "last_heartbeat": (
                        node.last_heartbeat.isoformat()
                        if node.last_heartbeat else None
                    )
                }
                for name, node in self.nodes.items()
            },
            "agents": {
                agent_id: {
                    "type": agent.agent_type,
                    "node": agent.node,
                    "status": agent.status,
                    "last_heartbeat": (
                        agent.last_heartbeat.isoformat()
                        if agent.last_heartbeat else None
                    )
                }
                for agent_id, agent in self.agents.items()
            },
            "pending_actions": len(self.pending_actions),
            "executed_actions": len(self.executed_actions)
        }


async def main():
    """Main entry point."""
    coordinator = AntibodyCoordinator()
    
    # Set up signal handlers
    loop = asyncio.get_event_loop()
    
    def signal_handler():
        asyncio.create_task(coordinator.stop())
    
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, signal_handler)
    
    logger.info("=" * 60)
    logger.info("  SKOS Antibody Coordinator v0.1.0")
    logger.info("  Sovereign Khaos Operating System")
    logger.info("=" * 60)
    logger.info(f"  NATS URL: {NATS_URL}")
    logger.info(f"  Node Name: {NODE_NAME}")
    logger.info(f"  Heartbeat Timeout: {HEARTBEAT_TIMEOUT_SECONDS}s")
    logger.info("=" * 60)
    
    await coordinator.start()


if __name__ == "__main__":
    asyncio.run(main())

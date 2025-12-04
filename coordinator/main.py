"""
Antibody Coordinator v0.1 - SKOS Immune System
Built for Strategickhaos Sovereignty Architecture

Listens for agent heartbeats + alerts over NATS
Maintains node + antibody state
Applies failover / healing strategies
Publishes commands back to agents
"""

import asyncio
import json
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional

import yaml
from nats.aio.client import Client as NATS
from nats.js.api import StreamConfig


# ---------- Models ----------

@dataclass
class AntibodyState:
    """State of an individual antibody agent."""
    name: str
    node: str
    last_heartbeat: float
    status: str = "healthy"
    metrics: dict = field(default_factory=dict)


@dataclass
class NodeState:
    """State of a node in the cluster."""
    name: str
    last_seen: float
    status: str = "healthy"
    metrics: dict = field(default_factory=dict)


class CoordinatorState:
    """Centralized state management for the coordinator."""
    
    def __init__(self, config: dict):
        self.config = config
        self.antibodies: Dict[str, AntibodyState] = {}
        self.nodes: Dict[str, NodeState] = {
            n["name"]: NodeState(name=n["name"], last_seen=0, status="unknown")
            for n in config.get("nodes", [])
        }

    def update_antibody(self, payload: dict) -> None:
        """Update antibody state from heartbeat payload."""
        name = payload["agent"]
        node = payload["node"]
        now = time.time()
        metrics = payload.get("metrics", {})
        status = payload.get("status", "healthy")

        self.antibodies[name] = AntibodyState(
            name=name,
            node=node,
            last_heartbeat=now,
            status=status,
            metrics=metrics,
        )
        # Node is alive if antibody is alive
        ns = self.nodes.get(node)
        if ns:
            ns.last_seen = now
            ns.status = "healthy"
            ns.metrics.update(metrics.get("node_metrics", {}))

    def update_node_from_alert(self, payload: dict) -> None:
        """Update node state from alert payload."""
        node = payload["node"]
        now = time.time()
        ns = self.nodes.get(node)
        if not ns:
            ns = NodeState(name=node, last_seen=now, status="unknown")
            self.nodes[node] = ns
        ns.last_seen = now

    def get_unhealthy_nodes(self, heartbeat_timeout: float) -> List[NodeState]:
        """Get list of nodes that have exceeded heartbeat timeout."""
        now = time.time()
        bad = []
        for node in self.nodes.values():
            if node.last_seen == 0:
                continue
            if now - node.last_seen > heartbeat_timeout:
                node.status = "unreachable"
                bad.append(node)
        return bad

    def get_hot_spare_node(self, exclude_node: str) -> Optional[str]:
        """Get a healthy node to use as a hot spare."""
        candidates = [
            n for n in self.nodes.values()
            if n.name != exclude_node and n.status == "healthy"
        ]
        if not candidates:
            return None
        # Simple: pick the first for now (could use metrics later)
        return sorted(candidates, key=lambda x: x.name)[0].name


# ---------- Coordinator ----------

class AntibodyCoordinator:
    """Main coordinator service for SKOS immune system."""
    
    def __init__(self, config_path: str = "config.yaml"):
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)

        self.state = CoordinatorState(self.config)
        self.nats: NATS = NATS()
        self.js = None

    async def connect(self) -> None:
        """Connect to NATS and set up subscriptions."""
        await self.nats.connect(self.config["nats"]["url"])
        self.js = self.nats.jetstream()

        # Ensure streams exist for observability if desired
        await self._ensure_stream(
            name="ANTIBODY_EVENTS",
            subjects=["antibody.heartbeat.*", "antibody.alert.*", "antibody.events.*"],
        )
        await self._ensure_stream(
            name="ANTIBODY_COMMANDS",
            subjects=["antibody.cmd.*"],
        )

        # Subscriptions
        await self.nats.subscribe(
            "antibody.heartbeat.*", cb=self.handle_heartbeat
        )
        await self.nats.subscribe("antibody.alert.*", cb=self.handle_alert)

        print("[Coordinator] Connected and listening.")

    async def _ensure_stream(self, name: str, subjects: List[str]) -> None:
        """Ensure a JetStream stream exists."""
        try:
            await self.js.add_stream(StreamConfig(name=name, subjects=subjects))
        except Exception:
            # Stream may already exist; ignore
            pass

    async def handle_heartbeat(self, msg) -> None:
        """Handle incoming heartbeat messages from antibody agents."""
        try:
            payload = json.loads(msg.data.decode())
            self.state.update_antibody(payload)
            await self._log_event("heartbeat", payload)
        except Exception as e:
            print(f"[Coordinator] Error processing heartbeat: {e}")

    async def handle_alert(self, msg) -> None:
        """Handle incoming alert messages from antibody agents."""
        try:
            payload = json.loads(msg.data.decode())
            self.state.update_node_from_alert(payload)
            await self._log_event("alert", payload)

            alert_type = payload.get("alert_type")
            if alert_type == "thermal_overheat":
                await self._handle_thermal_alert(payload)
            elif alert_type == "storage_low":
                await self._handle_storage_alert(payload)
            elif alert_type == "mesh_down":
                await self._handle_mesh_alert(payload)
            elif alert_type == "model_corruption":
                await self._handle_model_alert(payload)
            elif alert_type == "loop_detected":
                await self._handle_loop_alert(payload)
            # Extend with more alert types as needed

        except Exception as e:
            print(f"[Coordinator] Error processing alert: {e}")

    async def _log_event(self, event_type: str, payload: dict) -> None:
        """Log an event to JetStream for observability."""
        record = {
            "ts": time.time(),
            "event_type": event_type,
            "payload": payload,
        }
        # If you want durable logs, publish to a logging subject
        await self.js.publish(
            "antibody.events.log", json.dumps(record).encode()
        )

    # ---------- Healing Strategies ----------

    async def _handle_thermal_alert(self, payload: dict) -> None:
        """Handle thermal overheat alerts."""
        node = payload["node"]
        metrics = payload.get("metrics", {})
        cpu = metrics.get("cpu_temp")
        gpu = metrics.get("gpu_temp")
        limits = self.config["policies"]["thermal"]

        print(f"[Coordinator] Thermal alert from {node}: CPU={cpu}, GPU={gpu}")

        agent = "thermal-sentinel"
        actions = []

        cpu_over_limit = cpu is not None and cpu > limits["max_cpu_temp"]
        gpu_over_limit = gpu is not None and gpu > limits["max_gpu_temp"]
        
        if cpu_over_limit or gpu_over_limit:
            actions.append({"action": "throttle", "params": {"node": node}})
            spare = self.state.get_hot_spare_node(exclude_node=node)
            if spare:
                actions.append({
                    "action": "redistribute",
                    "params": {"from": node, "to": spare},
                })
            actions.append({"action": "alert", "params": {"severity": "high"}})

        if actions:
            await self._dispatch_actions(agent, actions)

    async def _handle_storage_alert(self, payload: dict) -> None:
        """Handle low storage alerts."""
        node = payload["node"]
        metrics = payload.get("metrics", {})
        free_pct = metrics.get("disk_free_pct")
        min_free = self.config["policies"]["storage"]["min_free_percent"]
        print(f"[Coordinator] Storage alert from {node}: free={free_pct}%")

        if free_pct is not None and free_pct < min_free:
            agent = "storage-watcher"
            actions = [
                {"action": "cleanup", "params": {"node": node}},
                {
                    "action": "alert",
                    "params": {
                        "severity": "medium",
                        "message": f"Low disk: {free_pct}% on {node}",
                    },
                },
            ]
            await self._dispatch_actions(agent, actions)

    async def _handle_mesh_alert(self, payload: dict) -> None:
        """Handle mesh network down alerts."""
        node = payload["node"]
        print(f"[Coordinator] Mesh alert from {node}")
        agent = "mesh-healer"
        actions = [
            {"action": "regenerate_config", "params": {"node": node}},
            {"action": "restart_interface", "params": {"node": node}},
            {"action": "failover", "params": {"from": node}},
        ]
        await self._dispatch_actions(agent, actions)

    async def _handle_model_alert(self, payload: dict) -> None:
        """Handle model corruption alerts."""
        node = payload["node"]
        print(f"[Coordinator] Model corruption alert from {node}")
        agent = "qwen-health-monitor"
        spare = self.state.get_hot_spare_node(exclude_node=node)
        actions = []
        if spare:
            actions.append({
                "action": "switch_hot_spare",
                "params": {"from": node, "to": spare},
            })
        actions.append({"action": "reload_model", "params": {"node": node}})
        actions.append({"action": "alert", "params": {"severity": "high"}})
        await self._dispatch_actions(agent, actions)

    async def _handle_loop_alert(self, payload: dict) -> None:
        """Handle loop detection alerts."""
        print(f"[Coordinator] Loop alert: {payload}")
        agent = "loop-breaker"
        actions = [
            {
                "action": "circuit_break",
                "params": {
                    "chain_id": payload.get("chain_id"),
                    "reason": "max_depth_or_contradiction",
                },
            },
            {
                "action": "alert",
                "params": {
                    "severity": "medium",
                    "message": "Loop breaker triggered",
                },
            },
        ]
        await self._dispatch_actions(agent, actions)

    async def _dispatch_actions(self, agent: str, actions: List[dict]) -> None:
        """Dispatch actions to an antibody agent."""
        cmd = {
            "ts": time.time(),
            "agent": agent,
            "actions": actions,
        }
        subject = f"antibody.cmd.{agent}"
        print(f"[Coordinator] -> {subject}: {cmd}")
        await self.nats.publish(subject, json.dumps(cmd).encode())

    # ---------- Background Health Sweep ----------

    async def health_sweeper(self) -> None:
        """Background task to detect and handle unhealthy nodes."""
        timeout = self.config["policies"]["heartbeat"]["timeout_seconds"]
        while True:
            await asyncio.sleep(10)
            bad_nodes = self.state.get_unhealthy_nodes(heartbeat_timeout=timeout)
            for node in bad_nodes:
                print(f"[Coordinator] Node {node.name} is unreachable.")
                # Trigger mesh healer failover if mesh-healer exists
                await self._dispatch_actions(
                    agent="mesh-healer",
                    actions=[
                        {
                            "action": "failover",
                            "params": {"from": node.name},
                        },
                        {
                            "action": "alert",
                            "params": {
                                "severity": "high",
                                "message": f"Node {node.name} unreachable",
                            },
                        },
                    ],
                )

    async def run(self) -> None:
        """Run the coordinator service."""
        await self.connect()
        await self.health_sweeper()  # runs forever


if __name__ == "__main__":
    asyncio.run(AntibodyCoordinator().run())

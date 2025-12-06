# SKOS Immune System

**Sovereign Khaos Operating System - Autonomous Self-Healing Infrastructure**

[![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)](https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Sovereignty](https://img.shields.io/badge/sovereignty-100%25-purple.svg)](#)

## Overview

The SKOS Immune System transforms potential infrastructure failures into an autonomous self-healing mechanism. Just like biological immune systems, it:

1. **Detects** threats (temperature spikes, storage issues, network failures)
2. **Responds** with appropriate healing actions
3. **Remembers** patterns to improve future responses
4. **Adapts** and gets stronger from each challenge

This is **antifragility** made manifest in code.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     SKOS Immune System                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐                     │
│  │  Nova   │    │  Lyra   │    │ Athena  │  <- Physical Nodes  │
│  │ (GPU)   │    │ (Backup)│    │(Storage)│                     │
│  └────┬────┘    └────┬────┘    └────┬────┘                     │
│       │              │              │                           │
│       ▼              ▼              ▼                           │
│  ┌─────────────────────────────────────────┐                   │
│  │         Antibody Agents                 │                   │
│  │  • Thermal Sentinel (temperature)       │                   │
│  │  • Storage Watcher (disk space)         │                   │
│  │  • Mesh Healer (network)                │                   │
│  │  • Loop Breaker (synthesis chains)      │                   │
│  └────────────────┬────────────────────────┘                   │
│                   │ heartbeats + alerts                        │
│                   ▼                                             │
│  ┌─────────────────────────────────────────┐                   │
│  │         NATS JetStream                  │  <- Message Bus   │
│  │    (Pub/Sub + Durable Streams)          │                   │
│  └────────────────┬────────────────────────┘                   │
│                   │                                             │
│                   ▼                                             │
│  ┌─────────────────────────────────────────┐                   │
│  │       Antibody Coordinator              │  <- Brain         │
│  │  • Receives heartbeats/alerts           │                   │
│  │  • Applies healing policies             │                   │
│  │  • Dispatches commands                  │                   │
│  │  • Maintains audit trail                │                   │
│  └────────────────┬────────────────────────┘                   │
│                   │ commands                                    │
│                   ▼                                             │
│  ┌─────────────────────────────────────────┐                   │
│  │         Healing Actions                 │                   │
│  │  • Throttle CPU/GPU                     │                   │
│  │  • Redistribute workloads               │                   │
│  │  • Failover to hot-spare                │                   │
│  │  • Circuit break infinite loops         │                   │
│  └─────────────────────────────────────────┘                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Quick Start

### Prerequisites

- Docker (20.10+)
- Docker Compose (2.0+)
- Linux/macOS (Windows via WSL2)

### Deploy in 60 Seconds

```bash
# Clone the repository (if not already done)
git clone https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-.git
cd Sovereignty-Architecture-Elevator-Pitch-/skos-immune-system

# Make scripts executable
chmod +x deploy.sh test.sh

# Deploy the immune system
./deploy.sh

# Verify everything works
./test.sh
```

### Deploy to Remote Node

```bash
# Copy to your sovereign node
scp -r skos-immune-system/ nova.local:~/

# SSH and deploy
ssh nova.local
cd skos-immune-system
./deploy.sh
./test.sh
```

## Components

### Antibody Coordinator (`coordinator/main.py`)

The "brain" of the immune system. It:

- Maintains state of all nodes (Nova, Lyra, Athena)
- Tracks antibody agent health via heartbeats
- Applies policy-based healing decisions
- Implements circuit breakers to prevent healing loops
- Dispatches commands to agents
- Maintains immutable audit trail in JetStream

**Key Classes:**

```python
class AntibodyCoordinator:
    """Main coordinator - the immune system brain."""
    
    async def start(self) -> None:
        """Start the coordinator."""
        
    async def _process_heartbeat(self, data: dict) -> None:
        """Process heartbeat from an agent."""
        
    async def _process_alert(self, data: dict) -> None:
        """Process alert and determine healing actions."""
        
    def _determine_healing_actions(self, ...) -> list[HealingAction]:
        """Determine appropriate healing based on alert."""

class CircuitBreaker:
    """Prevents infinite healing loops."""
    
    def is_open(self, action_key: str) -> bool:
        """Check if circuit is open for this action."""
    
    def record_failure(self, action_key: str) -> None:
        """Record a failure - may open circuit."""
```

### Thermal Sentinel Agent (`agents/thermal_sentinel.py`)

Monitors CPU and GPU temperatures:

- Reads from Linux thermal zones (`/sys/class/thermal`)
- Reads from hwmon sensors (`/sys/class/hwmon`)
- Supports NVIDIA and AMD GPUs
- Falls back to `lm-sensors` if available
- Sends alerts when thresholds exceeded
- Executes throttling commands

**Key Classes:**

```python
class ThermalSensor:
    """Reads temperature from system sensors."""
    
    def read_cpu_temp(self) -> float:
        """Read CPU temperature in Celsius."""
    
    def read_gpu_temp(self) -> float:
        """Read GPU temperature in Celsius."""

class ThermalSentinelAgent:
    """The Thermal Sentinel antibody agent."""
    
    async def _heartbeat_loop(self) -> None:
        """Send regular heartbeats to coordinator."""
    
    async def _monitor_loop(self) -> None:
        """Monitor temperatures and send alerts."""
    
    async def _command_listener(self) -> None:
        """Listen for commands from coordinator."""
    
    async def _throttle(self, level: int) -> None:
        """Apply CPU/GPU throttling."""
```

### Docker Compose Stack

```yaml
services:
  nats:           # NATS JetStream message backbone
  coordinator:    # Antibody Coordinator (brain)
  thermal-sentinel:  # Temperature monitoring agent
```

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `NATS_URL` | `nats://localhost:4222` | NATS server URL |
| `NODE_NAME` | `nova` | Node identifier |
| `HEARTBEAT_TIMEOUT` | `30` | Seconds before agent marked offline |
| `MONITOR_INTERVAL` | `5` | Seconds between temperature checks |
| `WARNING_TEMP` | `75` | Warning threshold (°C) |
| `CRITICAL_TEMP` | `85` | Critical threshold (°C) |
| `EMERGENCY_TEMP` | `95` | Emergency threshold (°C) |
| `LOG_LEVEL` | `INFO` | Logging level |

### config.yaml

```yaml
thermal:
  thresholds:
    warning: 75
    critical: 85
    emergency: 95
  actions:
    warning:
      - throttle_10
    critical:
      - throttle_50
      - redistribute
    emergency:
      - shutdown_non_essential
      - failover
```

## Healing Policies

### Thermal Healing

| Severity | Temperature | Actions |
|----------|-------------|---------|
| Warning | >75°C | Throttle 10% |
| Critical | >85°C | Throttle 50%, Redistribute workload |
| Emergency | >95°C | Shutdown non-essential, Failover |

### Storage Healing

| Severity | Usage | Actions |
|----------|-------|---------|
| Warning | >80% | Cleanup temp files |
| Critical | >90% | Cleanup logs, Archive old data |
| Emergency | >95% | Emergency cleanup, Alert human |

### Mesh Healing

| Event | Actions |
|-------|---------|
| Tunnel down | Restart WireGuard, Regenerate config |
| Peer unreachable | Ping peer, Failover route |

### Loop Healing

| Condition | Actions |
|-----------|---------|
| Depth exceeded | Circuit break |
| Iterations exceeded | Reset chain |

## Adding New Antibody Agents

Create a new agent following this pattern:

```python
#!/usr/bin/env python3
"""New Antibody Agent Template."""

class NewAgent:
    async def _heartbeat_loop(self) -> None:
        """Send heartbeat every N seconds."""
        while self.running:
            await self._send_heartbeat()
            await asyncio.sleep(HEARTBEAT_INTERVAL)
    
    async def _monitor_loop(self) -> None:
        """Check for problems, send alerts."""
        while self.running:
            if self._detect_problem():
                await self._send_alert(...)
            await asyncio.sleep(MONITOR_INTERVAL)
    
    async def _command_listener(self) -> None:
        """Execute healing actions from coordinator."""
        await self.nc.subscribe(f"skos.command.{NODE_NAME}", 
                               cb=self._handle_command)
```

## API Reference

### NATS Subjects

| Subject Pattern | Description |
|-----------------|-------------|
| `skos.heartbeat.<node>` | Agent heartbeats |
| `skos.alert.<node>` | Agent alerts |
| `skos.command.<node>` | Commands to agents |
| `SKOS_AUDIT.*` | Audit log stream |

### Message Formats

**Heartbeat:**
```json
{
  "agent_id": "thermal-sentinel-nova",
  "agent_type": "thermal_sentinel",
  "node": "nova",
  "timestamp": "2024-01-01T00:00:00Z",
  "cpu_temp": 65.5,
  "gpu_temp": 70.2,
  "metadata": {}
}
```

**Alert:**
```json
{
  "agent_id": "thermal-sentinel-nova",
  "type": "thermal",
  "severity": "critical",
  "node": "nova",
  "message": "CPU temperature 87.5°C exceeds critical threshold",
  "details": {
    "sensor": "cpu",
    "temperature": 87.5,
    "threshold": 85
  },
  "timestamp": "2024-01-01T00:00:00Z"
}
```

**Command:**
```json
{
  "action_id": "nova:thermal:throttle_50:1704067200",
  "action_type": "throttle_50",
  "parameters": {},
  "timestamp": "2024-01-01T00:00:00Z"
}
```

## Monitoring

### NATS Dashboard

Access the NATS monitoring dashboard at `http://localhost:8222`:

- `/healthz` - Health check
- `/varz` - Server variables
- `/jsz` - JetStream status
- `/connz` - Connections
- `/routez` - Routes
- `/subz` - Subscriptions

### Container Logs

```bash
# All logs
docker compose logs -f

# Specific service
docker compose logs -f coordinator

# Last 100 lines
docker compose logs --tail=100 coordinator
```

## Security

### No External Dependencies

The SKOS Immune System has zero external dependencies:
- No cloud services required
- No API keys needed
- No data leaves your infrastructure
- Works completely offline (air-gapped)

### Least Privilege

- Containers run as non-root user
- Minimal capabilities granted
- Read-only mounts where possible
- Network isolation via Docker bridge

### Audit Trail

All actions are logged to the immutable JetStream audit stream:
- Who triggered the action
- What action was taken
- When it occurred
- What was the result

## Troubleshooting

### Container not starting?

```bash
# Check logs
docker compose logs coordinator

# Check Docker status
docker ps -a

# Rebuild
./deploy.sh --build --clean
```

### NATS connection failed?

```bash
# Check NATS health
curl http://localhost:8222/healthz

# Check NATS logs
docker compose logs nats
```

### No heartbeats?

```bash
# Check thermal sentinel logs
docker compose logs thermal-sentinel

# Verify NATS connectivity
docker exec skos-coordinator python -c "import nats; print('OK')"
```

### Temperatures not reading?

The agent may not have access to thermal sensors:

```bash
# Check host sensors
cat /sys/class/thermal/thermal_zone0/temp

# Verify container mounts
docker inspect skos-thermal-sentinel | grep Mounts
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a PR

## License

MIT License - see [LICENSE](../LICENSE)

## Acknowledgments

- NATS.io for the incredible message bus
- The Strategickhaos community for pushing boundaries
- Everyone who believes in digital sovereignty

---

**Built with 🔥 by Strategickhaos DAO LLC**

*"Contradiction → Creation. This is the F Option."*

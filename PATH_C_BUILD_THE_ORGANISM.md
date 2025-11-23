# 🧬 PATH C: "BUILD THE ORGANISM" — The Engineering Path

**Goal:** Create a docker-compose biological organism with DNA, cellular containers, immune agents, and heartbeat monitoring.

**This is a functional prototype you can run TODAY.**

---

## 🎯 Biological Architecture Metaphor

| Biology | Docker Architecture |
|---------|---------------------|
| **DNA** | `docker-compose.organism.yml` (blueprint) |
| **Cells** | Containers with specific functions |
| **Organelles** | Service components within containers |
| **Cytoplasm** | Shared KV-cache (Redis) for communication |
| **Cell Membrane** | Network boundaries and security |
| **Nervous System** | Event bus and coordination layer |
| **Circulatory System** | Data flow between containers |
| **Immune System** | Monitoring agents and auto-remediation |
| **Heartbeat** | Health check and monitoring script |

---

## 📁 Directory Structure

```
organism/
├── docker-compose.organism.yml    # DNA: System blueprint
├── .env.organism                  # Environment configuration
├── circulation/                   # Circulatory system
│   ├── ingestion/                # Data intake
│   ├── processing/               # Data transformation
│   └── distribution/             # Data delivery
├── immunity/                      # Immune system
│   ├── monitors/                 # Health monitoring
│   ├── responders/               # Threat response
│   └── remediation/              # Auto-healing
├── nervous_system/               # Coordination layer
│   ├── coordinator/              # Central nervous system
│   ├── signaling/                # Event bus
│   └── reflexes/                 # Automated responses
├── cytoplasm/                    # Shared state
│   └── redis.conf                # KV-cache configuration
├── cells/                        # Individual cell implementations
│   ├── worker_cell/              # Worker containers
│   ├── sensor_cell/              # Monitoring containers
│   └── coordinator_cell/         # Control containers
├── scripts/
│   ├── heartbeat.sh              # System health monitor
│   ├── spawn_cell.sh             # Cell creation
│   └── immune_response.sh        # Threat response
└── README.organism.md            # Documentation
```

---

## 🧬 Docker Compose DNA

Create the core DNA file:

```yaml
# docker-compose.organism.yml
# The DNA: Blueprint for the biological organism

version: '3.8'

# Shared network (cell membrane environment)
networks:
  organism_network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.28.0.0/16

# Persistent volumes (cellular memory)
volumes:
  cytoplasm_data:     # Shared KV-cache state
  nervous_data:       # Event logs and coordination state
  immune_logs:        # Health and threat logs
  circulation_buffer: # Data flow buffer

services:
  # ═══════════════════════════════════════
  # CYTOPLASM: Shared State (Redis)
  # ═══════════════════════════════════════
  cytoplasm:
    image: redis:7-alpine
    container_name: organism_cytoplasm
    volumes:
      - cytoplasm_data:/data
      - ./cytoplasm/redis.conf:/usr/local/etc/redis/redis.conf
    command: redis-server /usr/local/etc/redis/redis.conf
    networks:
      organism_network:
        ipv4_address: 172.28.0.10
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 3s
      retries: 3
      start_period: 10s
    restart: unless-stopped
    labels:
      organism.role: "cytoplasm"
      organism.type: "shared_state"

  # ═══════════════════════════════════════
  # NERVOUS SYSTEM: Coordination (NATS)
  # ═══════════════════════════════════════
  nervous_system:
    image: nats:2-alpine
    container_name: organism_nervous_system
    volumes:
      - nervous_data:/data
    command: 
      - "--jetstream"
      - "--store_dir=/data"
      - "--http_port=8222"
    networks:
      organism_network:
        ipv4_address: 172.28.0.11
    ports:
      - "4222:4222"  # NATS protocol
      - "8222:8222"  # HTTP monitoring
    healthcheck:
      test: ["CMD", "wget", "--spider", "http://localhost:8222/healthz"]
      interval: 5s
      timeout: 3s
      retries: 3
    restart: unless-stopped
    labels:
      organism.role: "nervous_system"
      organism.type: "coordination"

  # ═══════════════════════════════════════
  # WORKER CELLS: Processing Units
  # ═══════════════════════════════════════
  worker_cell_1:
    build:
      context: ./cells/worker_cell
      dockerfile: Dockerfile
    container_name: organism_worker_1
    environment:
      CELL_ID: "worker_1"
      CELL_TYPE: "worker"
      CYTOPLASM_URL: "redis://cytoplasm:6379"
      NERVOUS_URL: "nats://nervous_system:4222"
      CELL_ROLE: "data_processor"
    volumes:
      - ./cells/worker_cell:/app
      - circulation_buffer:/circulation
    networks:
      - organism_network
    depends_on:
      cytoplasm:
        condition: service_healthy
      nervous_system:
        condition: service_healthy
    restart: unless-stopped
    labels:
      organism.role: "worker"
      organism.type: "cell"
      organism.function: "processing"

  worker_cell_2:
    build:
      context: ./cells/worker_cell
      dockerfile: Dockerfile
    container_name: organism_worker_2
    environment:
      CELL_ID: "worker_2"
      CELL_TYPE: "worker"
      CYTOPLASM_URL: "redis://cytoplasm:6379"
      NERVOUS_URL: "nats://nervous_system:4222"
      CELL_ROLE: "data_processor"
    volumes:
      - ./cells/worker_cell:/app
      - circulation_buffer:/circulation
    networks:
      - organism_network
    depends_on:
      cytoplasm:
        condition: service_healthy
      nervous_system:
        condition: service_healthy
    restart: unless-stopped
    labels:
      organism.role: "worker"
      organism.type: "cell"
      organism.function: "processing"

  # ═══════════════════════════════════════
  # SENSOR CELLS: Monitoring
  # ═══════════════════════════════════════
  sensor_cell:
    build:
      context: ./cells/sensor_cell
      dockerfile: Dockerfile
    container_name: organism_sensor
    environment:
      CELL_ID: "sensor_1"
      CELL_TYPE: "sensor"
      CYTOPLASM_URL: "redis://cytoplasm:6379"
      NERVOUS_URL: "nats://nervous_system:4222"
      MONITOR_INTERVAL: "5"
    volumes:
      - ./cells/sensor_cell:/app
      - /var/run/docker.sock:/var/run/docker.sock:ro
    networks:
      - organism_network
    depends_on:
      - cytoplasm
      - nervous_system
    restart: unless-stopped
    labels:
      organism.role: "sensor"
      organism.type: "cell"
      organism.function: "monitoring"

  # ═══════════════════════════════════════
  # IMMUNE SYSTEM: Threat Response
  # ═══════════════════════════════════════
  immune_agent:
    build:
      context: ./immunity
      dockerfile: Dockerfile.immune
    container_name: organism_immune
    environment:
      AGENT_ID: "immune_1"
      CYTOPLASM_URL: "redis://cytoplasm:6379"
      NERVOUS_URL: "nats://nervous_system:4222"
      RESPONSE_THRESHOLD: "critical"
      AUTO_REMEDIATE: "true"
    volumes:
      - ./immunity:/app
      - immune_logs:/logs
      - /var/run/docker.sock:/var/run/docker.sock
    networks:
      - organism_network
    depends_on:
      - cytoplasm
      - nervous_system
      - sensor_cell
    restart: unless-stopped
    labels:
      organism.role: "immune"
      organism.type: "agent"
      organism.function: "defense"
    privileged: true  # Required for remediation actions

  # ═══════════════════════════════════════
  # COORDINATOR: Central Control
  # ═══════════════════════════════════════
  coordinator_cell:
    build:
      context: ./cells/coordinator_cell
      dockerfile: Dockerfile
    container_name: organism_coordinator
    environment:
      CELL_ID: "coordinator_1"
      CELL_TYPE: "coordinator"
      CYTOPLASM_URL: "redis://cytoplasm:6379"
      NERVOUS_URL: "nats://nervous_system:4222"
    volumes:
      - ./cells/coordinator_cell:/app
    ports:
      - "8080:8080"  # Management API
    networks:
      organism_network:
        ipv4_address: 172.28.0.100
    depends_on:
      - cytoplasm
      - nervous_system
    restart: unless-stopped
    labels:
      organism.role: "coordinator"
      organism.type: "cell"
      organism.function: "control"

  # ═══════════════════════════════════════
  # CIRCULATION: Data Flow
  # ═══════════════════════════════════════
  ingestion_cell:
    build:
      context: ./circulation/ingestion
      dockerfile: Dockerfile
    container_name: organism_ingestion
    environment:
      CELL_ID: "ingestion_1"
      CYTOPLASM_URL: "redis://cytoplasm:6379"
      NERVOUS_URL: "nats://nervous_system:4222"
    volumes:
      - circulation_buffer:/buffer
    networks:
      - organism_network
    depends_on:
      - cytoplasm
    restart: unless-stopped
    labels:
      organism.role: "circulation"
      organism.type: "cell"
      organism.function: "ingestion"

  # ═══════════════════════════════════════
  # HEARTBEAT MONITOR: System Health
  # ═══════════════════════════════════════
  heartbeat:
    image: alpine:latest
    container_name: organism_heartbeat
    volumes:
      - ./scripts:/scripts
      - /var/run/docker.sock:/var/run/docker.sock:ro
    command: /scripts/heartbeat.sh
    networks:
      - organism_network
    depends_on:
      - cytoplasm
      - nervous_system
    restart: unless-stopped
    labels:
      organism.role: "heartbeat"
      organism.type: "monitor"
```

---

## 🔬 Cell Implementations

### Worker Cell (Data Processor)

```python
# cells/worker_cell/worker.py
import os
import time
import redis
import json
from nats.aio.client import Client as NATS

class WorkerCell:
    def __init__(self):
        self.cell_id = os.getenv('CELL_ID', 'worker_unknown')
        self.cell_type = os.getenv('CELL_TYPE', 'worker')
        self.cytoplasm_url = os.getenv('CYTOPLASM_URL')
        self.nervous_url = os.getenv('NERVOUS_URL')
        
        # Connect to cytoplasm (Redis)
        self.cytoplasm = redis.from_url(self.cytoplasm_url)
        
        # Connect to nervous system (NATS)
        self.nc = NATS()
        
    async def start(self):
        """Initialize cell and start processing."""
        print(f"🦠 {self.cell_id} coming online...")
        
        # Connect to nervous system
        await self.nc.connect(self.nervous_url)
        
        # Register cell in cytoplasm
        self.cytoplasm.hset(
            f"cell:{self.cell_id}",
            mapping={
                "type": self.cell_type,
                "status": "active",
                "started": time.time()
            }
        )
        
        # Subscribe to work queue
        await self.nc.subscribe("work.queue", cb=self.process_work)
        
        # Send heartbeat
        await self.send_heartbeat()
        
        print(f"✅ {self.cell_id} ready for work")
        
    async def process_work(self, msg):
        """Process incoming work."""
        data = json.loads(msg.data.decode())
        
        print(f"⚙️ {self.cell_id} processing: {data}")
        
        # Simulate processing
        result = self.do_work(data)
        
        # Store result in cytoplasm
        self.cytoplasm.lpush("results", json.dumps(result))
        
        # Notify via nervous system
        await self.nc.publish("work.complete", json.dumps(result).encode())
        
    def do_work(self, data):
        """Actual work processing logic."""
        # Transform data
        result = {
            "cell_id": self.cell_id,
            "input": data,
            "output": f"Processed by {self.cell_id}",
            "timestamp": time.time()
        }
        return result
        
    async def send_heartbeat(self):
        """Send periodic heartbeat."""
        while True:
            await self.nc.publish(
                "heartbeat",
                json.dumps({
                    "cell_id": self.cell_id,
                    "status": "alive",
                    "timestamp": time.time()
                }).encode()
            )
            await asyncio.sleep(5)

if __name__ == "__main__":
    import asyncio
    cell = WorkerCell()
    asyncio.run(cell.start())
```

```dockerfile
# cells/worker_cell/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir \
    redis \
    nats-py \
    asyncio

COPY worker.py .

CMD ["python", "worker.py"]
```

---

### Sensor Cell (Health Monitor)

```python
# cells/sensor_cell/sensor.py
import os
import time
import redis
import docker
import asyncio
from nats.aio.client import Client as NATS
import json

class SensorCell:
    def __init__(self):
        self.cell_id = os.getenv('CELL_ID', 'sensor_unknown')
        self.cytoplasm = redis.from_url(os.getenv('CYTOPLASM_URL'))
        self.nc = NATS()
        self.docker_client = docker.from_env()
        self.monitor_interval = int(os.getenv('MONITOR_INTERVAL', 5))
        
    async def start(self):
        """Start monitoring."""
        print(f"👁️ {self.cell_id} monitoring organism health...")
        
        await self.nc.connect(os.getenv('NERVOUS_URL'))
        
        # Continuous monitoring loop
        while True:
            await self.check_health()
            await asyncio.sleep(self.monitor_interval)
            
    async def check_health(self):
        """Check health of all cells."""
        containers = self.docker_client.containers.list(
            filters={"label": "organism.type=cell"}
        )
        
        for container in containers:
            health = {
                "container_id": container.id[:12],
                "name": container.name,
                "status": container.status,
                "health": container.attrs.get('State', {}).get('Health', {}),
                "timestamp": time.time()
            }
            
            # Store in cytoplasm
            self.cytoplasm.hset(
                f"health:{container.name}",
                mapping=health
            )
            
            # Alert if unhealthy
            if health['status'] != 'running':
                await self.nc.publish(
                    "alert.unhealthy",
                    json.dumps(health).encode()
                )

if __name__ == "__main__":
    sensor = SensorCell()
    asyncio.run(sensor.start())
```

---

### Immune Agent (Auto-Remediation)

```python
# immunity/immune_agent.py
import os
import time
import redis
import docker
import asyncio
from nats.aio.client import Client as NATS
import json

class ImmuneAgent:
    def __init__(self):
        self.agent_id = os.getenv('AGENT_ID', 'immune_unknown')
        self.cytoplasm = redis.from_url(os.getenv('CYTOPLASM_URL'))
        self.nc = NATS()
        self.docker_client = docker.from_env()
        self.auto_remediate = os.getenv('AUTO_REMEDIATE', 'true').lower() == 'true'
        
    async def start(self):
        """Start immune monitoring."""
        print(f"🛡️ {self.agent_id} immune system active...")
        
        await self.nc.connect(os.getenv('NERVOUS_URL'))
        
        # Subscribe to health alerts
        await self.nc.subscribe("alert.*", cb=self.respond_to_threat)
        
        print(f"✅ {self.agent_id} monitoring for threats")
        
        # Keep running
        while True:
            await asyncio.sleep(1)
            
    async def respond_to_threat(self, msg):
        """Respond to health threats."""
        alert = json.loads(msg.data.decode())
        threat_type = msg.subject.split('.')[-1]
        
        print(f"🚨 {self.agent_id} detected threat: {threat_type}")
        print(f"   Details: {alert}")
        
        # Log to cytoplasm
        self.cytoplasm.lpush(
            "immune_log",
            json.dumps({
                "agent": self.agent_id,
                "threat": threat_type,
                "alert": alert,
                "timestamp": time.time()
            })
        )
        
        # Auto-remediate if enabled
        if self.auto_remediate:
            await self.remediate(threat_type, alert)
            
    async def remediate(self, threat_type, alert):
        """Attempt to fix the issue."""
        if threat_type == "unhealthy":
            container_name = alert.get('name')
            if container_name:
                print(f"🔧 {self.agent_id} restarting {container_name}")
                try:
                    container = self.docker_client.containers.get(container_name)
                    container.restart()
                    
                    # Notify successful remediation
                    await self.nc.publish(
                        "immune.remediated",
                        json.dumps({
                            "container": container_name,
                            "action": "restart",
                            "timestamp": time.time()
                        }).encode()
                    )
                except Exception as e:
                    print(f"❌ Remediation failed: {e}")

if __name__ == "__main__":
    agent = ImmuneAgent()
    asyncio.run(agent.start())
```

```dockerfile
# immunity/Dockerfile.immune
FROM python:3.11-slim

WORKDIR /app

# Install Docker CLI for remediation
RUN apt-get update && apt-get install -y docker.io && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir \
    redis \
    nats-py \
    docker

COPY immune_agent.py .

CMD ["python", "immune_agent.py"]
```

---

## 💓 Heartbeat Monitoring Script

```bash
#!/bin/sh
# scripts/heartbeat.sh - Organism Heartbeat Monitor

set -e

INTERVAL=${HEARTBEAT_INTERVAL:-10}
ORGANISM_NAME="sovereignty-organism"

echo "💓 Heartbeat monitor starting..."
echo "   Interval: ${INTERVAL}s"
echo "   Organism: ${ORGANISM_NAME}"

# Install docker client if not present
if ! command -v docker &> /dev/null; then
    apk add --no-cache docker-cli
fi

beat_count=0

while true; do
    beat_count=$((beat_count + 1))
    timestamp=$(date -Iseconds)
    
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "💓 Heartbeat #${beat_count} - ${timestamp}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    # Check cytoplasm (Redis)
    if docker exec organism_cytoplasm redis-cli ping > /dev/null 2>&1; then
        echo "✅ Cytoplasm: healthy"
    else
        echo "❌ Cytoplasm: FAILED"
    fi
    
    # Check nervous system (NATS)
    if docker exec organism_nervous_system wget -q --spider http://localhost:8222/healthz 2>&1; then
        echo "✅ Nervous System: healthy"
    else
        echo "❌ Nervous System: FAILED"
    fi
    
    # Check all cells
    cells=$(docker ps --filter "label=organism.type=cell" --format "{{.Names}}")
    
    if [ -n "$cells" ]; then
        echo ""
        echo "🦠 Cell Status:"
        for cell in $cells; do
            status=$(docker inspect --format='{{.State.Status}}' "$cell")
            health=$(docker inspect --format='{{if .State.Health}}{{.State.Health.Status}}{{else}}no-healthcheck{{end}}' "$cell")
            
            if [ "$status" = "running" ]; then
                echo "   ✅ $cell: $status ($health)"
            else
                echo "   ❌ $cell: $status"
            fi
        done
    else
        echo "⚠️  No cells detected"
    fi
    
    # Resource usage
    echo ""
    echo "📊 Resource Usage:"
    docker stats --no-stream --format "   {{.Name}}: CPU {{.CPUPerc}} | RAM {{.MemUsage}}" \
        $(docker ps --filter "label=organism" -q) 2>/dev/null || echo "   (stats unavailable)"
    
    sleep "$INTERVAL"
done
```

Make executable:

```bash
chmod +x scripts/heartbeat.sh
```

---

## 🚀 Quick Start

### 1. Create Directory Structure

```bash
#!/bin/bash
# setup_organism.sh

echo "🧬 Setting up biological organism structure..."

# Create directories
mkdir -p organism/{circulation/{ingestion,processing,distribution},immunity/{monitors,responders,remediation},nervous_system/{coordinator,signaling,reflexes},cytoplasm,cells/{worker_cell,sensor_cell,coordinator_cell},scripts}

echo "✅ Directory structure created"

# Create minimal Dockerfiles
cat > organism/cells/worker_cell/Dockerfile << 'EOF'
FROM python:3.11-slim
WORKDIR /app
RUN pip install redis nats-py
COPY worker.py .
CMD ["python", "worker.py"]
EOF

# Create placeholder files
touch organism/cells/worker_cell/worker.py
touch organism/cells/sensor_cell/sensor.py
touch organism/immunity/immune_agent.py

echo "✅ Organism structure ready"
echo ""
echo "Next steps:"
echo "1. Review docker-compose.organism.yml"
echo "2. Customize cell implementations"
echo "3. Run: docker-compose -f docker-compose.organism.yml up"
```

### 2. Start the Organism

```bash
# Navigate to the organism directory
cd organism/

# Start all systems
docker-compose -f docker-compose.organism.yml up -d

# Watch the heartbeat
docker logs -f organism_heartbeat

# Check organism health
docker ps --filter "label=organism"
```

### 3. Interact with the Organism

```bash
# Access cytoplasm (shared state)
docker exec -it organism_cytoplasm redis-cli

# Check cell registry
HGETALL cell:worker_1

# View immune logs
LRANGE immune_log 0 -1

# Monitor nervous system
curl http://localhost:8222/healthz
```

---

## 🧪 Testing the Organism

```bash
#!/bin/bash
# test_organism.sh

echo "🧪 Testing biological organism..."

# Test 1: Cytoplasm communication
echo "Test 1: Cytoplasm (shared state)"
docker exec organism_cytoplasm redis-cli SET test_key "Hello from cytoplasm"
result=$(docker exec organism_cytoplasm redis-cli GET test_key)
[ "$result" = "Hello from cytoplasm" ] && echo "✅ Pass" || echo "❌ Fail"

# Test 2: Nervous system events
echo "Test 2: Nervous system (event bus)"
# Send test event
docker exec organism_nervous_system nats-pub test.event "Test message"
echo "✅ Event sent"

# Test 3: Cell health
echo "Test 3: Cell health checks"
docker ps --filter "label=organism.type=cell" --format "{{.Names}}: {{.Status}}"

# Test 4: Immune response (simulate failure)
echo "Test 4: Immune system response"
# Stop a worker cell
docker stop organism_worker_1
sleep 5
# Check if immune agent restarted it
status=$(docker inspect --format='{{.State.Status}}' organism_worker_1)
[ "$status" = "running" ] && echo "✅ Auto-remediation working" || echo "⚠️  Check immune agent logs"

echo ""
echo "🎯 Organism test complete"
```

---

## 📊 Monitoring Dashboard

Create a simple status dashboard:

```bash
#!/bin/bash
# scripts/dashboard.sh

while true; do
    clear
    echo "╔═══════════════════════════════════════════════════════╗"
    echo "║   🧬 BIOLOGICAL ORGANISM DASHBOARD                    ║"
    echo "╚═══════════════════════════════════════════════════════╝"
    echo ""
    
    echo "📡 CORE SYSTEMS:"
    printf "   Cytoplasm:      "
    docker exec organism_cytoplasm redis-cli ping > /dev/null 2>&1 && echo "🟢 ONLINE" || echo "🔴 OFFLINE"
    
    printf "   Nervous System: "
    docker exec organism_nervous_system wget -q --spider http://localhost:8222/healthz 2>&1 && echo "🟢 ONLINE" || echo "🔴 OFFLINE"
    
    echo ""
    echo "🦠 CELLS:"
    docker ps --filter "label=organism.type=cell" --format "   {{.Names}}: {{.Status}}" | sed 's/Up/🟢 Active/; s/Exited/🔴 Dead/'
    
    echo ""
    echo "🛡️ IMMUNE SYSTEM:"
    immune_logs=$(docker exec organism_cytoplasm redis-cli LLEN immune_log 2>/dev/null || echo "0")
    echo "   Total responses: $immune_logs"
    
    echo ""
    echo "💾 CYTOPLASM STATE:"
    cell_count=$(docker exec organism_cytoplasm redis-cli KEYS "cell:*" | wc -l)
    echo "   Registered cells: $cell_count"
    
    echo ""
    echo "Press Ctrl+C to exit"
    
    sleep 5
done
```

---

## ✅ Success Criteria

You've completed Path C when you have:

- [ ] Created organism directory structure
- [ ] Deployed docker-compose.organism.yml
- [ ] All core systems running (cytoplasm, nervous_system)
- [ ] At least 2 worker cells operational
- [ ] Sensor cell monitoring health
- [ ] Immune agent responding to threats
- [ ] Heartbeat script showing regular updates
- [ ] Successfully tested cell communication via cytoplasm

---

## 🎯 Next Steps

1. **Add More Cell Types** - Create specialized cells for different functions
2. **Enhanced Immune Responses** - More sophisticated threat detection
3. **Cell Division** - Auto-scale cells based on load
4. **Apoptosis** - Programmed cell death for failed cells
5. **Evolution** - Version cells and migrate between generations
6. **Documentation** - Document your organism's behavior

---

## 🔗 Integration with Patents

This organism architecture forms the basis for your patent filings:

- **Patent #1:** Negative-Balance Doctrine Architecture
  - Use this organism as working embodiment
  - Document self-healing and sovereign operation
  
- **Patent #2:** Biological Docker Organism System
  - This IS the invention
  - Include docker-compose as DNA
  - Document cellular communication patterns

---

**You've built a living, breathing, self-healing system. This is sovereign engineering.**

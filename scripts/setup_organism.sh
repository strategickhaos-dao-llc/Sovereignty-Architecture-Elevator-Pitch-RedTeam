#!/bin/bash
# setup_organism.sh - Set up biological organism structure

set -euo pipefail

echo "🧬 Setting up biological organism structure..."

BASE_DIR="${1:-./organism}"

# Create directories
mkdir -p "$BASE_DIR"
mkdir -p "$BASE_DIR/circulation/"{ingestion,processing,distribution}
mkdir -p "$BASE_DIR/immunity/"{monitors,responders,remediation}
mkdir -p "$BASE_DIR/nervous_system/"{coordinator,signaling,reflexes}
mkdir -p "$BASE_DIR/cytoplasm"
mkdir -p "$BASE_DIR/cells/"{worker_cell,sensor_cell,coordinator_cell}
mkdir -p "$BASE_DIR/scripts"

echo "✅ Directory structure created at: $BASE_DIR"

# Create cytoplasm Redis config
cat > "$BASE_DIR/cytoplasm/redis.conf" << 'EOF'
# Cytoplasm (Shared State) Configuration
bind 0.0.0.0
protected-mode no
port 6379
tcp-backlog 511
timeout 0
tcp-keepalive 300
daemonize no
supervised no
pidfile /var/run/redis.pid
loglevel notice
logfile ""
databases 16
save 900 1
save 300 10
save 60 10000
stop-writes-on-bgsave-error yes
rdbcompression yes
rdbchecksum yes
dbfilename dump.rdb
dir /data
EOF

echo "✅ Cytoplasm configuration created"

# Create worker cell implementation
cat > "$BASE_DIR/cells/worker_cell/worker.py" << 'EOF'
#!/usr/bin/env python3
"""Worker Cell - Data Processing Unit"""

import os
import time
import json
import redis
import asyncio
from nats.aio.client import Client as NATS

class WorkerCell:
    def __init__(self):
        self.cell_id = os.getenv('CELL_ID', 'worker_unknown')
        self.cell_type = os.getenv('CELL_TYPE', 'worker')
        self.cytoplasm_url = os.getenv('CYTOPLASM_URL', 'redis://localhost:6379')
        self.nervous_url = os.getenv('NERVOUS_URL', 'nats://localhost:4222')
        
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
                "started": str(time.time())
            }
        )
        
        # Subscribe to work queue
        await self.nc.subscribe("work.queue", cb=self.process_work)
        
        # Send heartbeat
        asyncio.create_task(self.send_heartbeat())
        
        print(f"✅ {self.cell_id} ready for work")
        
        # Keep running
        while True:
            await asyncio.sleep(1)
        
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
            try:
                await self.nc.publish(
                    "heartbeat",
                    json.dumps({
                        "cell_id": self.cell_id,
                        "status": "alive",
                        "timestamp": time.time()
                    }).encode()
                )
            except Exception as e:
                print(f"❌ Heartbeat error: {e}")
            await asyncio.sleep(5)

if __name__ == "__main__":
    cell = WorkerCell()
    asyncio.run(cell.start())
EOF

# Create worker cell Dockerfile
cat > "$BASE_DIR/cells/worker_cell/Dockerfile" << 'EOF'
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir \
    redis \
    nats-py

COPY worker.py .

CMD ["python", "worker.py"]
EOF

echo "✅ Worker cell implementation created"

# Create sensor cell implementation
cat > "$BASE_DIR/cells/sensor_cell/sensor.py" << 'EOF'
#!/usr/bin/env python3
"""Sensor Cell - Health Monitoring Unit"""

import os
import time
import json
import redis
import asyncio
from nats.aio.client import Client as NATS

class SensorCell:
    def __init__(self):
        self.cell_id = os.getenv('CELL_ID', 'sensor_unknown')
        self.cytoplasm = redis.from_url(os.getenv('CYTOPLASM_URL', 'redis://localhost:6379'))
        self.nc = NATS()
        self.monitor_interval = int(os.getenv('MONITOR_INTERVAL', 5))
        
    async def start(self):
        """Start monitoring."""
        print(f"👁️ {self.cell_id} monitoring organism health...")
        
        await self.nc.connect(os.getenv('NERVOUS_URL', 'nats://localhost:4222'))
        
        # Continuous monitoring loop
        while True:
            await self.check_health()
            await asyncio.sleep(self.monitor_interval)
            
    async def check_health(self):
        """Check health of all registered cells."""
        try:
            # Get all registered cells from cytoplasm
            cell_keys = self.cytoplasm.keys("cell:*")
            
            for key in cell_keys:
                cell_data = self.cytoplasm.hgetall(key)
                
                health = {
                    "cell_id": key.decode() if isinstance(key, bytes) else key,
                    "status": cell_data.get(b'status', b'unknown').decode() if isinstance(cell_data.get(b'status'), bytes) else cell_data.get('status', 'unknown'),
                    "timestamp": time.time()
                }
                
                # Store health status
                self.cytoplasm.hset(
                    f"health:{key}",
                    mapping=health
                )
                
        except Exception as e:
            print(f"❌ Health check error: {e}")

if __name__ == "__main__":
    sensor = SensorCell()
    asyncio.run(sensor.start())
EOF

cat > "$BASE_DIR/cells/sensor_cell/Dockerfile" << 'EOF'
FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir redis nats-py

COPY sensor.py .

CMD ["python", "sensor.py"]
EOF

echo "✅ Sensor cell implementation created"

# Create immune agent
cat > "$BASE_DIR/immunity/immune_agent.py" << 'EOF'
#!/usr/bin/env python3
"""Immune Agent - Auto-Remediation System"""

import os
import time
import json
import redis
import asyncio
from nats.aio.client import Client as NATS

class ImmuneAgent:
    def __init__(self):
        self.agent_id = os.getenv('AGENT_ID', 'immune_unknown')
        self.cytoplasm = redis.from_url(os.getenv('CYTOPLASM_URL', 'redis://localhost:6379'))
        self.nc = NATS()
        self.auto_remediate = os.getenv('AUTO_REMEDIATE', 'true').lower() == 'true'
        
    async def start(self):
        """Start immune monitoring."""
        print(f"🛡️ {self.agent_id} immune system active...")
        
        await self.nc.connect(os.getenv('NERVOUS_URL', 'nats://localhost:4222'))
        
        # Subscribe to health alerts
        await self.nc.subscribe("alert.*", cb=self.respond_to_threat)
        
        print(f"✅ {self.agent_id} monitoring for threats")
        
        # Keep running
        while True:
            await asyncio.sleep(1)
            
    async def respond_to_threat(self, msg):
        """Respond to health threats."""
        try:
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
            
        except Exception as e:
            print(f"❌ Threat response error: {e}")

if __name__ == "__main__":
    agent = ImmuneAgent()
    asyncio.run(agent.start())
EOF

cat > "$BASE_DIR/immunity/Dockerfile.immune" << 'EOF'
FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir redis nats-py

COPY immune_agent.py .

CMD ["python", "immune_agent.py"]
EOF

echo "✅ Immune agent implementation created"

# Create heartbeat script
cat > "$BASE_DIR/scripts/heartbeat.sh" << 'EOFSCRIPT'
#!/bin/sh
# heartbeat.sh - Organism Heartbeat Monitor

set -e

INTERVAL=${HEARTBEAT_INTERVAL:-10}
ORGANISM_NAME="${ORGANISM_NAME:-sovereignty-organism}"

echo "💓 Heartbeat monitor starting..."
echo "   Interval: ${INTERVAL}s"
echo "   Organism: ${ORGANISM_NAME}"

# Install docker client if not present
if ! command -v docker &> /dev/null; then
    echo "Installing docker-cli..."
    apk add --no-cache docker-cli 2>/dev/null || apt-get update && apt-get install -y docker.io 2>/dev/null || true
fi

beat_count=0

while true; do
    beat_count=$((beat_count + 1))
    timestamp=$(date -Iseconds 2>/dev/null || date)
    
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
    cells=$(docker ps --filter "label=organism.type=cell" --format "{{.Names}}" 2>/dev/null || echo "")
    
    if [ -n "$cells" ]; then
        echo ""
        echo "🦠 Cell Status:"
        for cell in $cells; do
            status=$(docker inspect --format='{{.State.Status}}' "$cell" 2>/dev/null || echo "unknown")
            
            if [ "$status" = "running" ]; then
                echo "   ✅ $cell: $status"
            else
                echo "   ❌ $cell: $status"
            fi
        done
    else
        echo "⚠️  No cells detected"
    fi
    
    sleep "$INTERVAL"
done
EOFSCRIPT

chmod +x "$BASE_DIR/scripts/heartbeat.sh"

echo "✅ Heartbeat script created"

# Create README
cat > "$BASE_DIR/README.organism.md" << 'EOF'
# 🧬 Biological Organism Architecture

This directory contains a docker-compose based biological organism with:

- **DNA:** `docker-compose.organism.yml` (system blueprint)
- **Cytoplasm:** Redis (shared state/KV-cache)
- **Nervous System:** NATS (event bus/coordination)
- **Cells:** Containerized processing units
- **Immune System:** Auto-remediation agents
- **Heartbeat:** Health monitoring script

## Quick Start

```bash
# Start the organism
docker-compose -f docker-compose.organism.yml up -d

# Watch the heartbeat
docker logs -f organism_heartbeat

# Check organism health
docker ps --filter "label=organism"

# Access cytoplasm
docker exec -it organism_cytoplasm redis-cli

# Stop the organism
docker-compose -f docker-compose.organism.yml down
```

## Architecture

| Component | Technology | Purpose |
|-----------|------------|---------|
| Cytoplasm | Redis | Shared state between cells |
| Nervous System | NATS | Event bus and coordination |
| Worker Cells | Python | Data processing |
| Sensor Cells | Python | Health monitoring |
| Immune Agent | Python | Auto-remediation |
| Heartbeat | Shell script | System monitoring |

## Next Steps

1. Customize cell implementations in `cells/`
2. Add more cell types as needed
3. Enhance immune responses in `immunity/`
4. Expand nervous system capabilities
5. Document your organism's behavior

See the main [PATH_C_BUILD_THE_ORGANISM.md](../PATH_C_BUILD_THE_ORGANISM.md) for detailed implementation guide.
EOF

echo "✅ Documentation created"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Organism structure setup complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Next steps:"
echo "  1. Copy docker-compose.organism.yml to $BASE_DIR/"
echo "  2. Customize cell implementations as needed"
echo "  3. Run: cd $BASE_DIR && docker-compose -f docker-compose.organism.yml up"
echo ""
echo "Files created:"
find "$BASE_DIR" -type f | sort

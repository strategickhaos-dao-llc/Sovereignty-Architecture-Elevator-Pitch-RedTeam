# Quick Start Guide - Evolution Path & SME Resources

Get started with the 100-item sovereignty evolution path and 100 authoritative resource collection in minutes.

---

## 🚀 5-Minute Quick Start

### Prerequisites
- Docker & Docker Compose installed
- Ollama running locally (optional but recommended)
- 5GB free disk space

### Step 1: Clone & Explore

```bash
# Clone the repository
git clone https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-.git
cd Sovereignty-Architecture-Elevator-Pitch-

# View the evolution path
cat evolution-path.yaml | less

# View SME resources
cat sme-resources.yaml | less
```

### Step 2: Fetch Resources (Choose One Method)

**Option A: Simple Bash Script**
```bash
# Fetch all 100 resources
./scripts/fetch-sme-resources.sh

# View results
ls -lh sme-resources-output/raw/
open sme-resources-output/index.html
```

**Option B: Advanced Python Crawler**
```bash
# Install dependencies
pip install pyyaml requests beautifulsoup4 lxml

# Run crawler
python scripts/sme-crawler.py

# Results in /tmp or configure DATA_DIR
```

**Option C: Full Docker Stack**
```bash
# Start all services
docker-compose -f docker-compose-sme.yml up -d

# View logs
docker-compose -f docker-compose-sme.yml logs -f web-crawler
```

### Step 3: Query the Knowledge Base

```bash
# Wait for indexing to complete (~5-10 minutes)
docker-compose -f docker-compose-sme.yml logs -f vector-indexer

# Query the RAG API
curl -X POST http://localhost:8090/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "How do I set up k3s with Longhorn storage?",
    "max_results": 5
  }'
```

---

## 📖 Evolution Path Usage

### View All Evolution Items

```bash
# Count items by tier
grep 'tier:' evolution-path.yaml | sort | uniq -c

# Find foundation tier items (weekend projects)
grep -A 5 'tier: "foundation"' evolution-path.yaml

# Find AI-related items
grep -A 5 'category: "ai' evolution-path.yaml
```

### Pick Your 10 Items

```python
import yaml

# Load evolution path
with open('evolution-path.yaml', 'r') as f:
    data = yaml.safe_load(f)

# Get foundation tier (weekend projects)
foundation = [item for item in data['evolution_items'] if item['tier'] == 'foundation']

# Show first 10
for item in foundation[:10]:
    print(f"{item['id']}. {item['title']}")
    print(f"   Time: {item['time']} | Cost: {item['cost']}")
    print(f"   Outcome: {item['outcome']}\n")
```

### Track Dependencies

```python
def get_dependencies(item_id, items):
    item = next(i for i in items if i['id'] == item_id)
    deps = item.get('dependencies', [])
    
    print(f"Item {item_id}: {item['title']}")
    if deps:
        print(f"Dependencies: {deps}")
        for dep_id in deps:
            dep = next(i for i in items if i['id'] == dep_id)
            print(f"  - {dep_id}: {dep['title']}")
    else:
        print("No dependencies - start here!")

# Example: Check item 10 dependencies
get_dependencies(10, data['evolution_items'])
```

---

## 🔍 SME Resources Usage

### Search Resources

```bash
# Find all Kubernetes resources
grep -B 3 'kubernetes' sme-resources.yaml | grep 'title:'

# Get all .gov URLs
grep 'domain: ".gov"' -B 2 sme-resources.yaml | grep 'url:'

# Find security resources
grep -A 10 'category: "security"' sme-resources.yaml | grep -E 'title:|url:'
```

### Extract Curl Commands

```bash
# Extract all curl commands
grep 'curl_command:' sme-resources.yaml | \
  sed 's/.*curl_command: "\(.*\)"/\1/' > all-curls.sh

# Execute specific category
grep -A 10 'category: "ai_ml"' sme-resources.yaml | \
  grep 'curl_command:' | \
  sed 's/.*curl_command: "\(.*\)"/\1/' | \
  bash
```

### Validate URLs

```bash
# Run validator
docker-compose -f docker-compose-sme.yml up url-validator

# Or manually
python scripts/url-validator.py
```

---

## 🐳 Docker Services

### Start Individual Services

```bash
# Web crawler only
docker-compose -f docker-compose-sme.yml up -d web-crawler

# Vector database only
docker-compose -f docker-compose-sme.yml up -d sme-vectordb

# RAG API only (requires vector DB)
docker-compose -f docker-compose-sme.yml up -d sme-vectordb sme-rag-api
```

### View Service Status

```bash
# List all services
docker-compose -f docker-compose-sme.yml ps

# View specific logs
docker-compose -f docker-compose-sme.yml logs -f sme-rag-api

# Follow all logs
docker-compose -f docker-compose-sme.yml logs -f
```

### Stop Services

```bash
# Stop all
docker-compose -f docker-compose-sme.yml down

# Stop and remove volumes (clean start)
docker-compose -f docker-compose-sme.yml down -v
```

---

## 🤖 RAG API Examples

### Basic Query

```bash
curl -X POST http://localhost:8090/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is the best way to deploy Ollama on Kubernetes?",
    "max_results": 5
  }' | jq
```

### Evolution-Specific Query

```bash
curl -X POST http://localhost:8090/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "How do I implement item #3 from the evolution path - Traefik with Tailscale?",
    "max_results": 10
  }' | jq
```

### Security Query

```bash
curl -X POST http://localhost:8090/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What are NIST recommendations for container security?",
    "max_results": 5,
    "min_score": 0.7
  }' | jq
```

### API Documentation

```bash
# View interactive docs
open http://localhost:8090/docs

# Get API stats
curl http://localhost:8090/stats | jq

# Health check
curl http://localhost:8090/health | jq
```

---

## 📊 Monitoring

### Grafana Dashboard

```bash
# Access dashboard
open http://localhost:3001
# Username: admin
# Password: admin (or SME_GRAFANA_PASSWORD)
```

### Prometheus Metrics

```bash
# Access Prometheus
open http://localhost:9091

# Query example
curl 'http://localhost:9091/api/v1/query?query=up'
```

### Qdrant Admin

```bash
# Access Qdrant dashboard
open http://localhost:6334

# Get collection info
curl http://localhost:6334/collections/sme_knowledge | jq
```

---

## 💬 Discord Integration

### Setup Webhook

```bash
# Set webhook URL
export DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/YOUR_WEBHOOK_URL"

# Start reporter
docker-compose -f docker-compose-sme.yml up -d discord-reporter

# View logs
docker-compose -f docker-compose-sme.yml logs -f discord-reporter
```

### Manual Notification

```bash
curl -X POST "$DISCORD_WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "🎯 Started evolution path item #1",
    "username": "Sovereignty Bot"
  }'
```

---

## 🔧 Troubleshooting

### Ollama Not Found

```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama (if installed)
ollama serve

# Or use host.docker.internal from containers
export OLLAMA_HOST=host.docker.internal:11434
```

### Out of Disk Space

```bash
# Clean Docker
docker system prune -a

# Check volume sizes
docker system df

# Remove specific volumes
docker volume rm sovereignty-architecture-elevator-pitch-_sme_data
```

### Services Won't Start

```bash
# Check logs
docker-compose -f docker-compose-sme.yml logs

# Restart specific service
docker-compose -f docker-compose-sme.yml restart sme-rag-api

# Clean restart
docker-compose -f docker-compose-sme.yml down -v
docker-compose -f docker-compose-sme.yml up -d
```

### Crawler Failing

```bash
# Check rate limiting
export RATE_LIMIT=1  # Slower
export TIMEOUT=60    # Longer timeout

# Run with debug
docker-compose -f docker-compose-sme.yml up web-crawler
```

---

## 🎯 Common Workflows

### Workflow 1: Research a Topic

```bash
# 1. Query RAG API
curl -X POST http://localhost:8090/query \
  -d '{"question": "How to implement zero-trust networking?"}' | jq

# 2. Get specific resources
grep -A 10 'zero.trust' sme-resources.yaml

# 3. Fetch those resources
./scripts/fetch-sme-resources.sh

# 4. Review in browser
open sme-resources-output/index.html
```

### Workflow 2: Start an Evolution Item

```bash
# 1. Pick an item from evolution-path.yaml
yq '.evolution_items[] | select(.id == 3)' evolution-path.yaml

# 2. Find relevant resources
python scripts/evolution-matcher.py --item-id 3

# 3. Query for implementation details
curl -X POST http://localhost:8090/query \
  -d '{"question": "How do I set up Traefik with Tailscale on k3s?"}' | jq

# 4. Track in Obsidian
# Create note and link to resources
```

### Workflow 3: Daily Knowledge Update

```bash
# 1. Validate all URLs
docker-compose -f docker-compose-sme.yml run url-validator

# 2. Re-crawl updated resources
docker-compose -f docker-compose-sme.yml run web-crawler

# 3. Re-index content
docker-compose -f docker-compose-sme.yml run vector-indexer

# 4. Get Discord report
docker-compose -f docker-compose-sme.yml run discord-reporter
```

---

## 📚 Further Reading

- [EVOLUTION_PATH.md](./EVOLUTION_PATH.md) - Comprehensive evolution guide
- [SME_RESOURCES.md](./SME_RESOURCES.md) - Resource documentation
- [README.md](./README.md) - Main repository documentation
- [docker-compose-sme.yml](./docker-compose-sme.yml) - Service definitions

---

## 🤝 Contributing

Found a better resource? Completed an evolution item?

1. Fork the repository
2. Add your resource/story
3. Submit a PR
4. Share with the community

---

## ⚡ Power User Tips

### Tip 1: Local Development

```bash
# Mount your local Obsidian vault
docker run -v ~/Obsidian:/obsidian \
  sovereignty-sme-crawler

# Use local Ollama
export OLLAMA_HOST=host.docker.internal:11434
```

### Tip 2: Batch Processing

```bash
# Process specific categories
for cat in security networking storage; do
  docker-compose -f docker-compose-sme.yml run \
    -e ANALYSIS_TOPIC=$cat \
    sme-analyzer-$cat
done
```

### Tip 3: Custom Queries

```python
# Create custom query script
import requests

questions = [
    "How to set up k3s HA?",
    "Best practices for Longhorn?",
    "Traefik TLS configuration?"
]

for q in questions:
    resp = requests.post(
        "http://localhost:8090/query",
        json={"question": q}
    )
    print(f"Q: {q}")
    print(f"A: {resp.json()['answer']}\n")
```

---

🔥 **Ready to evolve? Pick your 10 items and start building!**

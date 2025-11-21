# Subject Matter Expert (SME) Resources

## 100 Authoritative Sources for Sovereign Infrastructure

This document catalogs 100 authoritative web resources (.org, .gov, Google Scholar) that serve as the knowledge foundation for building sovereign digital infrastructure.

---

## 📋 Quick Links

- [Overview](#overview)
- [Resource Categories](#resource-categories)
- [Using the Resources](#using-the-resources)
- [Automated Fetching](#automated-fetching)
- [RAG Integration](#rag-integration)
- [Contributing](#contributing)

---

## Overview

**File**: `sme-resources.yaml`

This YAML file contains 100 carefully curated resources from:
- **Official documentation** (.io, .org domains)
- **Government agencies** (.gov domains)
- **Academic research** (Google Scholar, arXiv.org)
- **Standards bodies** (IETF, IEEE, W3C, CNCF)
- **Open source projects** (Apache, Linux Foundation)

Each resource includes:
- Unique ID (1-100)
- Title and URL
- Category classification
- SME topics covered
- Ready-to-use curl command
- Domain classification

---

## Resource Categories

### 🐳 Container Orchestration (10 resources)
**Topics**: Kubernetes, k3s, Docker Swarm, OCI specifications

Key resources:
- Kubernetes official docs
- CNCF project landscape
- Docker documentation
- Open Container Initiative

### 🤖 AI & Machine Learning (10 resources)
**Topics**: LLMs, training, deployment, optimization

Key resources:
- arXiv ML papers
- Papers With Code
- Hugging Face docs
- PyTorch/TensorFlow docs

### 🔐 Security & Networking (15 resources)
**Topics**: Zero-trust, TLS, VPN, cryptography, security frameworks

Key resources:
- NIST Cybersecurity Framework
- CISA advisories
- OWASP Top 10
- WireGuard/Tailscale docs

### 💾 Storage & Databases (10 resources)
**Topics**: Distributed storage, vector DBs, object storage

Key resources:
- PostgreSQL, Redis docs
- Ceph, MinIO, Longhorn
- Qdrant vector database
- ZFS documentation

### 📊 Monitoring & Observability (10 resources)
**Topics**: Metrics, logging, tracing, alerting

Key resources:
- Prometheus & Grafana
- Loki, Jaeger, Tempo
- OpenTelemetry
- Elastic Observability

### 🌐 IoT & Edge Computing (10 resources)
**Topics**: Raspberry Pi, Arduino, Home Assistant, MQTT, SDR

Key resources:
- Raspberry Pi docs
- Home Assistant
- RTL-SDR & GNU Radio
- FCC spectrum allocations

### 🔧 DevOps & CI/CD (10 resources)
**Topics**: GitOps, IaC, configuration management

Key resources:
- GitLab, Jenkins, GitHub Actions
- Ansible, Terraform
- ArgoCD, Helm
- Vault secrets management

### 💻 Programming & Development (10 resources)
**Topics**: Python, Go, Rust, Node.js, compilers

Key resources:
- Python.org, Go.dev
- Rust documentation
- MDN Web Docs
- LLVM & GCC

### ⛓️ Blockchain & Distributed Systems (10 resources)
**Topics**: Smart contracts, consensus, P2P, message queues

Key resources:
- Ethereum, IPFS, Arweave
- Raft consensus
- Kafka, etcd, Consul
- ZooKeeper

### 🔬 Research & Data (5 resources)
**Topics**: Government data, scientific papers, archives

Key resources:
- NASA Open Data
- data.gov
- Archive.org
- Library of Congress
- PubMed Central

---

## Using the Resources

### View the Complete List

```bash
cat sme-resources.yaml | less
```

### Filter by Category

```bash
# View all AI/ML resources
grep -A 10 'category: "ai_ml"' sme-resources.yaml

# View all security resources
grep -A 10 'category: "security"' sme-resources.yaml
```

### Extract URLs

```bash
# Get all URLs
grep 'url:' sme-resources.yaml | sed 's/.*url: "\(.*\)"/\1/'

# Get .gov URLs only
grep 'domain: ".gov"' -B 2 sme-resources.yaml | grep 'url:' | sed 's/.*url: "\(.*\)"/\1/'
```

### Extract Curl Commands

```bash
# Extract all curl commands to a file
grep 'curl_command:' sme-resources.yaml | sed 's/.*curl_command: "\(.*\)"/\1/' > curl-commands.txt

# Execute all curl commands
bash curl-commands.txt
```

---

## Automated Fetching

### Method 1: Bash Script

Use the provided fetch script to download all resources:

```bash
# Fetch all 100 resources
./scripts/fetch-sme-resources.sh
```

This will:
- Create `sme-resources-output/` directory
- Download all resources to `raw/` subdirectory
- Generate a fetch log
- Create an HTML index
- Report success/failure statistics

**Output structure:**
```
sme-resources-output/
├── raw/
│   ├── 001_container_orchestration.html
│   ├── 002_container_orchestration.html
│   └── ...
├── logs/
│   └── error_*.log
├── fetch.log
└── index.html
```

### Method 2: Python Crawler

Use the advanced Python crawler with content extraction:

```bash
# Using Docker
docker-compose -f docker-compose-sme.yml up web-crawler

# Or directly
python scripts/sme-crawler.py
```

This will:
- Rate-limit requests (configurable)
- Retry failed requests
- Extract text content from HTML
- Parse links and headings
- Save both raw HTML and processed JSON
- Generate comprehensive summary

**Output structure:**
```
/app/data/
├── raw/
│   └── *.html files
├── processed/
│   └── *.json files
└── crawl_summary.json
```

### Method 3: Docker Compose Stack

Run the complete SME analysis stack:

```bash
# Start all services
docker-compose -f docker-compose-sme.yml up -d

# View logs
docker-compose -f docker-compose-sme.yml logs -f

# Stop services
docker-compose -f docker-compose-sme.yml down
```

This starts:
- Web crawler
- Content analyzers (per category)
- Evolution path matcher
- Knowledge graph builder
- Vector database (Qdrant)
- RAG query API
- Discord reporter
- Monitoring dashboard

---

## RAG Integration

### Vector Database Setup

The SME resources can be indexed into a vector database for semantic search and RAG (Retrieval Augmented Generation):

```bash
# Start vector database
docker-compose -f docker-compose-sme.yml up -d sme-vectordb

# Index all resources
docker-compose -f docker-compose-sme.yml up vector-indexer
```

### Query the Knowledge Base

Once indexed, query the knowledge base via the RAG API:

```bash
# Start RAG API
docker-compose -f docker-compose-sme.yml up -d sme-rag-api

# Query example: k3s setup
curl -X POST http://localhost:8090/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "How do I set up k3s with Longhorn storage?",
    "max_results": 5
  }'

# Query example: security
curl -X POST http://localhost:8090/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What are NIST security best practices for containers?",
    "max_results": 10
  }'

# Query example: AI deployment
curl -X POST http://localhost:8090/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "How do I deploy a 70B model on consumer GPUs?",
    "max_results": 5
  }'
```

### Integration with Ollama

The RAG system can work with your local Ollama instance:

```bash
# Configure Ollama host
export OLLAMA_HOST=localhost:11434

# The RAG API will use Ollama for:
# - Generating embeddings (nomic-embed-text)
# - Answering questions (llama3:70b)
# - Summarizing content
```

---

## Obsidian Integration

### Generate Obsidian Notes

Create Obsidian notes for each resource:

```bash
# Generate markdown files
python scripts/generate-obsidian-notes.py

# Output to Obsidian vault
python scripts/generate-obsidian-notes.py --vault-path ~/Obsidian/Sovereignty
```

### Knowledge Graph

The resources can be visualized as a knowledge graph in Obsidian:

```bash
# Build knowledge graph
docker-compose -f docker-compose-sme.yml up knowledge-graph
```

This creates:
- Individual note for each resource
- Category index pages
- Bi-directional links
- Tag structure
- Canvas layout

---

## Evolution Path Mapping

### Map Resources to Evolution Items

Each SME resource can be mapped to relevant evolution path items:

```bash
# Run evolution matcher
docker-compose -f docker-compose-sme.yml up evolution-matcher
```

This analyzes:
- Which resources are needed for each evolution item
- Dependency chains
- Learning paths
- Implementation guides

Example output:
```yaml
evolution_item_1:
  id: 1
  title: "Turn Ras cluster into 8-node k3s swarm with Longhorn"
  relevant_resources:
    - resource_1: "Kubernetes Official Documentation"
    - resource_43: "Longhorn Documentation"
    - resource_71: "Helm Documentation"
  learning_path:
    - "Start with Kubernetes basics (resource_1)"
    - "Understand k3s lightweight variant"
    - "Learn Longhorn for persistent storage (resource_43)"
    - "Deploy using Helm charts (resource_71)"
```

---

## Discord Integration

### Automated Reporting

Set up automated Discord reports:

```bash
# Configure webhook
export DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/..."

# Start reporter
docker-compose -f docker-compose-sme.yml up -d discord-reporter
```

Reports include:
- Daily resource updates
- New content discovered
- Failed fetches
- Knowledge graph updates
- RAG query statistics

---

## Monitoring

### View Dashboard

Access the Grafana dashboard:

```
http://localhost:3001
Username: admin
Password: admin (or SME_GRAFANA_PASSWORD)
```

Dashboards show:
- Fetch success rates
- Resource categories
- Query performance
- Vector DB statistics
- System health

### Check Logs

```bash
# All services
docker-compose -f docker-compose-sme.yml logs -f

# Specific service
docker-compose -f docker-compose-sme.yml logs -f sme-rag-api

# Crawler only
docker-compose -f docker-compose-sme.yml logs -f web-crawler
```

---

## Contributing

### Adding New Resources

To add a new resource to the collection:

1. Edit `sme-resources.yaml`
2. Add new entry following the format:

```yaml
- id: 101
  title: "New Resource Title"
  url: "https://example.org/docs"
  domain: ".org"
  category: "your_category"
  sme_topics:
    - "Topic 1"
    - "Topic 2"
  curl_command: "curl -L -s https://example.org/docs"
```

3. Update the total count in metadata
4. Run validation:

```bash
python scripts/validate-sme-resources.py
```

5. Submit PR

### Improving Analysis

To improve content analysis:

1. Update analyzer scripts in `scripts/`
2. Adjust prompts for better extraction
3. Add new categories or topics
4. Enhance knowledge graph structure

---

## Resource Statistics

### By Category
- Container Orchestration: 10 resources
- AI & Machine Learning: 10 resources
- Security & Networking: 15 resources
- Storage & Databases: 10 resources
- Monitoring & Observability: 10 resources
- IoT & Edge Computing: 10 resources
- DevOps & CI/CD: 10 resources
- Programming & Development: 10 resources
- Blockchain & Distributed Systems: 10 resources
- Research & Data: 5 resources

### By Domain
- .org: ~40 resources (open source, standards, non-profits)
- .gov: ~15 resources (government agencies)
- .io/.com/.dev: ~35 resources (official docs, platforms)
- .edu: ~5 resources (academic institutions)
- Scholar/arXiv: ~5 resources (research papers)

---

## Best Practices

### Fetching Resources

1. **Rate Limiting**: Respect server limits (default: 2 req/sec)
2. **Caching**: Cache responses to avoid redundant fetches
3. **Error Handling**: Retry failed requests with backoff
4. **User Agent**: Identify your bot properly
5. **robots.txt**: Check and respect robots.txt

### Using Content

1. **Attribution**: Always cite sources
2. **Licensing**: Respect content licenses
3. **Updates**: Refresh content periodically
4. **Validation**: Verify accuracy before use
5. **Privacy**: Don't scrape personal data

---

## Troubleshooting

### Common Issues

**Problem**: Curl commands fail with timeout
```bash
# Increase timeout
export TIMEOUT=60
./scripts/fetch-sme-resources.sh
```

**Problem**: Rate limited by server
```bash
# Decrease rate limit
export RATE_LIMIT=1
./scripts/fetch-sme-resources.sh
```

**Problem**: Docker services won't start
```bash
# Check Ollama is running
curl http://localhost:11434/api/tags

# Check disk space
df -h

# View service logs
docker-compose -f docker-compose-sme.yml logs
```

**Problem**: Vector indexing fails
```bash
# Reset vector database
docker-compose -f docker-compose-sme.yml down -v
docker-compose -f docker-compose-sme.yml up -d sme-vectordb
```

---

## License

These resources are publicly accessible. Individual resources retain their original licenses. Always check and respect the license of each source.

This collection and tooling: MIT License

---

## Acknowledgments

Thanks to all the organizations maintaining these incredible resources:
- CNCF, Linux Foundation, Apache Foundation
- NIST, CISA, NASA, and other government agencies
- arXiv.org and academic institutions
- Open source project maintainers
- Standards bodies (IETF, IEEE, W3C)

**Your documentation makes sovereign infrastructure possible.**

---

🔥 **Built with sovereignty by the Strategickhaos Swarm Intelligence collective**

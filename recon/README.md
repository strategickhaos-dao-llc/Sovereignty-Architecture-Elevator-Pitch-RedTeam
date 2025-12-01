# RECON Directory
**Strategic Khaos Network Reconnaissance & Intelligence**

This directory contains tools, scripts, and reports for comprehensive network reconnaissance and repository intelligence.

---

## 📁 Directory Structure

```
recon/
├── README.md                    # This file
├── network_discovery.py         # Python-based service discovery tool
├── cyber_v2/                   # Cybersecurity knowledge base sources
├── ingest/                     # Repository ingestion for RAG system
├── llm_v1/                     # LLM integration components
├── reports/                    # Generated reconnaissance reports
│   ├── latest_network_scan/    # Symlink to most recent scan
│   └── network_scan_*/         # Timestamped scan reports
├── repos/                      # Repository copies for analysis
│   └── sovereignty-arch/       # This repository for RAG indexing
└── retriever/                  # RAG retriever API components
```

---

## 🎯 Purpose

The RECON directory serves two main purposes:

### 1. Network Reconnaissance
Comprehensive infrastructure discovery and monitoring:
- Docker network scanning
- Container inventory
- Service health monitoring
- Port exposure analysis
- Security vulnerability detection

### 2. Repository Intelligence (RAG)
RAG-powered repository analysis and querying:
- Code indexing and vector search
- Natural language code queries
- Architectural analysis
- Documentation generation

---

## 🚀 Quick Start

### Network Reconnaissance

```bash
# Run from repository root
./network_recon.sh                 # Full infrastructure scan
./view_recon_report.sh            # Interactive report viewer
python3 recon/network_discovery.py # Python-based discovery
```

### RAG System (Repository Intelligence)

```bash
# Start RAG stack
./launch-recon.sh start

# Query the codebase
curl -X POST http://localhost:7000/query \
  -H "Content-Type: application/json" \
  -d '{"q": "How does the contradiction engine work?", "k": 5}'
```

---

## 📊 Reports

### Network Scan Reports

Located in `reports/network_scan_*/`:
- `recon_report.md` - Comprehensive markdown report
- `service_health.txt` - Service status details
- `resource_usage.txt` - Container resource metrics
- `docker_networks.txt` - Network configuration
- `*_containers.txt` - Container inventories

### Network Discovery Reports

Located in `reports/`:
- `network_discovery_*.md` - Python discovery reports
- Service status with response times
- Structured data for automation

---

## 🔧 Tools

### network_discovery.py

Advanced Python-based service discovery:

```python
# Features:
- Docker network inspection
- HTTP/TCP service checking
- Response time measurement
- JSON/Markdown report generation
- Port availability scanning
```

**Usage:**
```bash
python3 recon/network_discovery.py
```

---

## 🏗️ Integration

### With Main Infrastructure

The RECON tools integrate with:
- Docker Compose stacks (main, recon, obs)
- Monitoring stack (Prometheus, Grafana)
- Discord bot for notifications
- Event Gateway for webhooks

### With RAG System

The repository intelligence system:
- Indexes code repositories
- Provides semantic search
- Enables natural language queries
- Integrates with Discord bot

---

## 📦 Components

### cyber_v2/
Cybersecurity knowledge base containing:
- NIST frameworks and guidelines
- MITRE ATT&CK matrices
- CIS controls
- OWASP standards
- Security advisories

### ingest/
Repository ingestion components:
- Code chunking and embedding
- Metadata extraction
- Vector database population
- Batch processing

### llm_v1/
LLM integration:
- Prompt templates
- Context assembly
- Response generation
- Token management

### repos/
Repository copies for analysis:
- sovereignty-arch/ - This repository
- Add more repositories as needed

### retriever/
RAG retriever API:
- FastAPI service
- Vector search
- Context retrieval
- LLM integration

---

## 🔍 Use Cases

### 1. Infrastructure Health Check
```bash
./network_recon.sh
./view_recon_report.sh --summary
```

### 2. Service Discovery
```bash
python3 recon/network_discovery.py
```

### 3. Code Intelligence
```bash
# Start RAG system
./launch-recon.sh start

# Query codebase
curl -X POST http://localhost:7000/query \
  -d '{"q": "Explain Discord bot architecture"}'
```

### 4. Security Audit
```bash
./network_recon.sh
grep "Security Analysis" -A 50 recon/reports/latest_network_scan/recon_report.md
```

### 5. Resource Monitoring
```bash
./network_recon.sh
cat recon/reports/latest_network_scan/resource_usage.txt
```

---

## 📚 Documentation

- **[NETWORK_RECON_GUIDE.md](../NETWORK_RECON_GUIDE.md)** - Complete reconnaissance guide
- **[RECON_STACK_V2.md](../RECON_STACK_V2.md)** - RAG system documentation
- **[BOOT_RECON.md](../BOOT_RECON.md)** - Initial reconnaissance commands
- **[README.md](../README.md)** - Main project documentation

---

## 🔒 Security

### Data Privacy
- Local-first architecture
- No external API calls for embeddings
- Encrypted volumes for sensitive data
- Access control through authentication

### Report Security
- Reports may contain sensitive information
- Add `recon/reports/` to `.gitignore` if needed
- Review reports before sharing
- Sanitize credentials and secrets

---

## 🛠️ Maintenance

### Clean Old Reports
```bash
# Remove reports older than 7 days
find recon/reports/network_scan_* -mtime +7 -exec rm -rf {} \;

# Archive reports
tar -czf recon_archive.tar.gz recon/reports/
```

### Update Service List
Edit `network_discovery.py` to add/remove services:
```python
known_services = [
    {'name': 'New Service', 'host': 'localhost', 'port': 9999, 'http': '...'},
    # ...
]
```

---

## 📈 Metrics & Monitoring

### Key Metrics
- Service availability
- Response times
- Resource usage
- Port exposures
- Security vulnerabilities

### Integration
Reports can be parsed for:
- Prometheus metrics
- Grafana dashboards
- Alert generation
- CI/CD validation

---

## 🆘 Troubleshooting

### No Reports Generated
```bash
# Ensure scripts are executable
chmod +x ../network_recon.sh
chmod +x network_discovery.py

# Check Docker availability
docker ps

# Run with verbose output
bash -x ../network_recon.sh
```

### Python Script Issues
```bash
# Check Python version
python3 --version  # Should be 3.7+

# Install dependencies if needed
# (Currently uses only standard library)
```

### RAG System Not Working
```bash
# Check RECON stack status
docker compose -f ../docker-compose-recon.yml ps

# View logs
docker compose -f ../docker-compose-recon.yml logs
```

---

## 🤝 Contributing

To add new reconnaissance capabilities:

1. Add service definitions to `network_discovery.py`
2. Update health check endpoints in `../network_recon.sh`
3. Document in `../NETWORK_RECON_GUIDE.md`
4. Test thoroughly before committing

---

## 📞 Support

For issues or questions:
1. Check [NETWORK_RECON_GUIDE.md](../NETWORK_RECON_GUIDE.md)
2. Review existing reports in `reports/`
3. Check service logs with `docker compose logs`
4. Refer to main [README.md](../README.md)

---

**Part of the Strategic Khaos Sovereignty Architecture**

*Empowering infrastructure intelligence through automated reconnaissance*

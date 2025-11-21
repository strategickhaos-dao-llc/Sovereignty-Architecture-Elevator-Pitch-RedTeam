# Legends of Minds - Unified Agent Orchestration Platform

**Production-grade meta-system for unified agent orchestration with immutable audit trails, multi-department operations, and sovereign AI capabilities.**

---

## 🎯 Overview

Legends of Minds is a comprehensive platform that provides:

- **Universal Web Command Center**: Multi-department request builder with live terminal agents
- **Proof Action Ledger**: Immutable audit trail of all code/config/files generated
- **Department APIs**: YAML/gen, Compose-gen, repo builder, code/picture search, compliance, glossary
- **Terminal WebSocket Agent**: Per-terminal AI for command execution/augmentation
- **Legal Compliance**: 30+ laws covering DAO, IP, marketing, privacy, securities, tax, employment, and more

---

## 🚀 Quick Start

### Option 1: Docker Compose (Recommended)

```bash
cd legends_of_minds
docker-compose up -d
```

Then open your browser:
```
http://localhost:8080
# or
http://localhost  # via nginx reverse proxy
```

### Option 2: Manual Python Setup

```bash
cd legends_of_minds

# Install dependencies
pip install -r requirements.txt

# Run the orchestrator
python -m uvicorn core.orchestrator:app --host 0.0.0.0 --port 8080
```

---

## 📋 Architecture

### Core Components

```
legends_of_minds/
├── core/
│   ├── orchestrator.py      # FastAPI server, WebSocket handler
│   └── routing.py           # Department request routing
├── departments/
│   ├── proof_ledger.py      # Immutable audit trail
│   ├── legal_compliance.py  # 30+ law compliance checker
│   └── __init__.py
├── web/
│   ├── templates/
│   │   └── command_center.html
│   └── static/
│       ├── css/
│       │   └── command_center.css
│       └── js/
│           └── command_center.js
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── nginx.conf
```

### Service Architecture

```yaml
Services:
  - orchestrator (FastAPI)   : Port 8080
  - postgres                 : Port 5432
  - redis                    : Port 6379
  - qdrant (vector DB)       : Port 6333
  - nginx (reverse proxy)    : Port 80/443
```

---

## 🏛️ Departments

### 1. Proof Action Ledger
- **Purpose**: Immutable audit trail with blockchain-style chaining
- **Capabilities**: Log, query, verify, audit all operations
- **Storage**: SQLite with SHA-256 hash chain verification

### 2. Legal Compliance
- **Laws Covered**: 30+ federal, state, and international laws
- **Jurisdictions**: Federal US, Wyoming, California, Delaware, EU, UK
- **Categories**: DAO, IP, Marketing, Privacy, Securities, Tax, Employment, Data Protection, Accessibility, Consumer Protection
- **Key Laws**: 
  - Wyoming SF0068 (DAO Supplement)
  - GDPR, CCPA/CPRA
  - DMCA, Copyright Act
  - Securities Acts (1933, 1934)
  - FTC Act, CAN-SPAM, TCPA
  - And 20+ more

### 3. GitLens Integration
- **Capabilities**: Analyze, search code, get history, compare
- **Integration**: Repository analysis and code intelligence

### 4. Refinery MCP
- **Capabilities**: Process, transform, validate
- **Purpose**: Model Context Protocol integration

### 5. Compose Generator
- **Capabilities**: Generate, validate, deploy Docker Compose files

### 6. YAML Generator
- **Capabilities**: Generate, validate, transform configuration files

### 7. Repository Builder
- **Capabilities**: Scaffold, initialize, configure new repositories

### 8. Code Search
- **Capabilities**: Search, index, query code across repositories

### 9. Picture Search
- **Capabilities**: Search, index, classify images and visual assets

### 10. Glossary
- **Capabilities**: Define, search, add technical terms

---

## 🌐 Web Command Center

### Features

1. **System Status Dashboard**
   - Active terminals count
   - Proof ledger entries
   - Department health monitoring

2. **Department Operations**
   - Visual department selector
   - Multi-department request builder
   - Real-time action execution

3. **Live Terminal Agent**
   - WebSocket-based terminal
   - Per-terminal AI augmentation
   - Command execution tracking

4. **Proof Ledger Viewer**
   - Real-time ledger display
   - Chain verification
   - Audit trail inspection

5. **Legal Compliance Checker**
   - Content compliance scanning
   - Multi-jurisdiction support
   - Category-based filtering

6. **AI Content Generation**
   - Docker Compose generation
   - YAML configuration generation
   - Code generation
   - Documentation generation

7. **File & Search Operations**
   - Code search
   - File search
   - Picture search

---

## 🔌 API Endpoints

### Core Endpoints

```
GET  /                              - Service info
GET  /health                        - Health check
GET  /api/v1/status                 - System status
GET  /api/v1/departments            - List departments
POST /api/v1/departments/{dept}/execute - Execute department action
```

### Proof Ledger

```
GET  /api/v1/proof-ledger           - Get ledger entries
POST /api/v1/proof-ledger           - Add ledger entry
```

### WebSocket

```
WS   /ws/terminal/{terminal_id}     - Terminal agent WebSocket
```

---

## 🔐 Security Features

### Proof Ledger Security
- SHA-256 hash chaining
- Immutable append-only log
- Cryptographic verification
- Tamper detection

### Legal Compliance
- Multi-jurisdiction support
- Automated content scanning
- Compliance recommendations
- UPL-safe operations

### Infrastructure Security
- Health checks on all services
- Network isolation
- Volume persistence
- Graceful restarts

---

## 📊 Monitoring & Observability

### Health Checks
```bash
# Check orchestrator health
curl http://localhost:8080/health

# Check system status
curl http://localhost:8080/api/v1/status
```

### Logs
```bash
# View orchestrator logs
docker-compose logs -f orchestrator

# View all service logs
docker-compose logs -f
```

---

## 🛠️ Development

### Local Development

```bash
# Install development dependencies
pip install -r requirements.txt

# Run with auto-reload
uvicorn core.orchestrator:app --reload --host 0.0.0.0 --port 8080
```

### Testing

```bash
# Run tests (when implemented)
pytest

# Run with coverage
pytest --cov=core --cov=departments
```

### Code Quality

```bash
# Format code
black core/ departments/

# Lint code
flake8 core/ departments/

# Type checking
mypy core/ departments/
```

---

## 🚀 Deployment Options

### Production Deployment

1. **Single-Node Docker Compose**
   ```bash
   docker-compose up -d
   ```

2. **Kubernetes** (future)
   - Helm charts
   - Multi-node orchestration
   - Auto-scaling

3. **Cloud Native** (future)
   - AWS ECS/EKS
   - Azure AKS
   - Google GKE

---

## 📈 Scaling

### Horizontal Scaling
- Multiple orchestrator instances behind load balancer
- Shared PostgreSQL and Redis
- Distributed Qdrant cluster

### Vertical Scaling
- Increase container resources in docker-compose.yml
- Optimize database configuration
- Tune Redis memory settings

---

## 🔧 Configuration

### Environment Variables

```bash
ORCHESTRATOR_PORT=8080
POSTGRES_DSN=postgresql://user:pass@postgres:5432/legends_db
REDIS_URL=redis://redis:6379
QDRANT_URL=http://qdrant:6333
```

### Docker Compose Customization

Edit `docker-compose.yml` to:
- Change ports
- Modify volume mounts
- Adjust resource limits
- Add new services

---

## 📚 Documentation

### API Documentation
- **Swagger UI**: http://localhost:8080/docs
- **ReDoc**: http://localhost:8080/redoc

### Department Documentation
See individual department modules for detailed API specifications.

---

## 🤝 Integration

### Discord Integration
Use existing Discord bot infrastructure to send notifications to the platform.

### JetBrains Integration
Connect with existing GitLens integration for code intelligence.

### CI/CD Integration
Integrate with GitHub Actions, GitLab CI, or Jenkins for automated operations.

---

## 🎓 Use Cases

1. **Automated Repository Setup**
   - Use Repo Builder department
   - Generate docker-compose.yml
   - Initialize with compliance checks

2. **Legal Compliance Audits**
   - Scan content for compliance issues
   - Generate compliance reports
   - Track remediation in proof ledger

3. **Multi-Agent Orchestration**
   - Terminal agents for each shell
   - Centralized command center
   - Immutable audit trail

4. **Research & Investigation**
   - Code search across repositories
   - Picture classification and search
   - Technical glossary management

5. **Sovereign Operations**
   - Full data sovereignty
   - No vendor lock-in
   - Complete audit trail

---

## 📄 License

See parent repository LICENSE file.

---

## 🆘 Support

For issues, questions, or contributions:
1. Check existing documentation
2. Review proof ledger for operation history
3. Check health endpoints
4. Review Docker logs
5. Open issue in parent repository

---

**Built with sovereignty, powered by automation, secured by proof.**

🛡️ **Total Sovereignty | Full Automation | End-to-End Audit** 🛡️

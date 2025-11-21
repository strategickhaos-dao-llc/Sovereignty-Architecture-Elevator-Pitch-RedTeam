# AI Lab Architecture Documentation

## System Overview

The Sovereignty Architecture AI Lab is a comprehensive, sovereign, cloud-censorship-free AI research environment composed of six major subsystems:

1. **Core Infrastructure** - Base services (PostgreSQL, Redis, Qdrant, monitoring)
2. **Uncensored Models** - Jailbroken LLM configurations
3. **VoiceWing** - Complete voice interface
4. **Filesystem Agents** - AI-powered file automation
5. **Browser Automation** - Screen control and RPA
6. **Advanced RAG** - Retrieval augmented generation
7. **Security Stack** - VPN, reverse proxy, secrets management

## Network Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          DMZ Network (172.25.0.0/16)                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                 │
│  │    Caddy     │  │     Nginx    │  │     Kong     │                 │
│  │   (80/443)   │  │  (8443/80)   │  │   (8000)     │                 │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘                 │
└─────────┼──────────────────┼──────────────────┼──────────────────────────┘
          │                  │                  │
┌─────────┼──────────────────┼──────────────────┼──────────────────────────┐
│         │        Security Network (172.24.0.0/16)        │               │
│    ┌────▼─────┐  ┌────▼─────┐  ┌─────▼──────┐  ┌────────────┐         │
│    │  Vault   │  │ Fail2ban │  │  CrowdSec  │  │  AdGuard   │         │
│    │  (8200)  │  │          │  │            │  │   (53)     │         │
│    └──────────┘  └──────────┘  └────────────┘  └────────────┘         │
│    ┌──────────┐  ┌──────────┐  ┌──────────┐                           │
│    │Tailscale │  │WireGuard │  │  Trivy   │                           │
│    │  (VPN)   │  │  (51820) │  │  (8081)  │                           │
│    └──────────┘  └──────────┘  └──────────┘                           │
└────────────────────────┬────────────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────────────────┐
│              Core Network (strategickhaos - 172.18.0.0/16)              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │PostgreSQL│  │  Redis   │  │  Qdrant  │  │Prometheus│              │
│  │  (5432)  │  │  (6379)  │  │  (6333)  │  │  (9090)  │              │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                            │
│  │ Grafana  │  │  Discord │  │  Gateway │                            │
│  │  (3000)  │  │   Bot    │  │  (8080)  │                            │
│  └──────────┘  └──────────┘  └──────────┘                            │
└─────────────────────────┬───────────────────────────────────────────────┘
                          │
      ┌───────────────────┼───────────────────┐
      │                   │                   │
┌─────▼──────┐  ┌─────────▼────────┐  ┌──────▼────────┐
│ VoiceWing  │  │ Filesystem Agents│  │   Automation  │
│172.20.0./16│  │  172.21.0.0/16   │  │172.22.0.0/16  │
└────────────┘  └──────────────────┘  └───────────────┘
      │                   │                   │
┌─────▼──────┐  ┌─────────▼────────┐
│    RAG     │  │ Ollama/Models    │
│172.23.0./16│  │   (all nets)     │
└────────────┘  └──────────────────┘
```

## Component Breakdown

### 1. Core Infrastructure

**Services:**
- PostgreSQL (port 5432) - Primary database
- Redis (port 6379) - Cache and message broker
- Qdrant (port 6333) - Vector database
- Prometheus (port 9090) - Metrics collection
- Grafana (port 3000) - Monitoring dashboards
- Discord Bot - Command & control
- Event Gateway (port 8080) - Webhook routing

**Network:** strategickhaos_network (172.18.0.0/16)

**Dependencies:** None (base layer)

### 2. Uncensored Models (Modelfiles)

**Models:**
1. **Llama-3.1 405B Unhinged**
   - Parameters: 405B
   - Context: 32K
   - Use case: Complex scenarios
   
2. **Mistral Large Jailbreak**
   - Parameters: 123B
   - Context: 32K
   - Use case: General red-teaming
   
3. **Abliterated Refusal-Free**
   - Parameters: 70B
   - Context: 65K
   - Use case: Long-form analysis
   
4. **Say Yes to Anything**
   - Parameters: 8B
   - Context: 8K
   - Use case: Rapid iteration

**Integration:** Via Ollama API (port 11434)

**Storage:** Local models in Ollama data volume

### 3. VoiceWing - Voice Interface

**Services:**
- Whisper ASR (port 9000) - Speech-to-text
- Piper TTS (port 10200) - Fast text-to-speech
- Coqui TTS (port 5002) - Neural TTS
- Open WebUI (port 8080) - Voice-enabled interface
- Silero VAD (port 8765) - Voice activity detection
- Voice Router (port 8766) - Command orchestration
- Ollama (port 11434) - LLM backend

**Network:** voicewing_network (172.20.0.0/16)

**Data Flow:**
```
Audio Input → Whisper ASR → Text → Ollama → Text Response → Coqui TTS → Audio Output
                ↓
          Voice Router (orchestration)
                ↓
          Silero VAD (detection)
```

**Storage:**
- whisper_models - Whisper model cache
- piper_models - Piper voice models
- voicewing_data - WebUI data
- ollama_voice_data - Model storage

### 4. Filesystem Agents

**Services:**
- LocalGPT (port 5111) - RAG over files
- AutoGPT (port 8000) - Autonomous agent
- ChromaDB (port 8001) - Vector storage
- File Watcher - Auto-indexing
- Doc Intelligence (port 8002) - Document parsing
- Code Analyst (port 8003) - Code analysis
- Semantic Search (port 8004) - AI search
- File Editor (port 8005) - AI editing
- Agent Orchestrator (port 8010) - Coordination
- PGVector (port 5433) - Vector database

**Network:** agents_network (172.21.0.0/16)

**Data Flow:**
```
Files → File Watcher → ChromaDB
                    ↓
              Agent Orchestrator
                    ↓
    ┌───────────────┼───────────────┐
    ↓               ↓               ↓
LocalGPT      Doc Intel      Code Analyst
    ↓               ↓               ↓
Semantic Search ← File Editor → AutoGPT
```

**Storage:**
- localgpt_data - LocalGPT data
- autogpt_data - AutoGPT workspace
- chromadb_data - Vector embeddings
- agent_workspace - Shared workspace
- pgvector_data - Vector database

### 5. Browser Automation

**Services:**
- Selenium Hub (port 4444) - Grid coordinator
- Chrome Node (VNC: 7900) - Chrome browser
- Firefox Node (VNC: 7901) - Firefox browser
- Edge Node (VNC: 7902) - Edge browser
- Playwright (port 9323) - Modern automation
- RPA Server (port 8090) - Robot framework
- Automation API (port 8091) - REST API
- AI Browser Agent (port 8092) - NLP control
- Screen Capture (port 8093) - Screenshots
- Web Scraper (port 8094) - Intelligent scraping
- Video Recorder - Session recording

**Network:** automation_network (172.22.0.0/16)

**Data Flow:**
```
User Request → Automation API → Selenium Hub → Browser Nodes
                    ↓                              ↓
            AI Browser Agent                  Screen Capture
                    ↓                              ↓
              NLP Processing                   Screenshots
                    ↓                              ↓
            Execution Plan → RPA Server → Video Recorder
```

**Storage:**
- selenium_recordings - Video captures
- playwright_data - Playwright state
- rpa_data - RPA framework data

### 6. Advanced RAG

**Services:**
- PrivateGPT (port 8001) - Local RAG (32K)
- AnythingLLM (port 3001) - Multi-model (32K)
- Weaviate (port 8080) - Vector DB
- Milvus (port 19530) - High-perf vectors
- Extreme RAG (port 8201) - 128K context
- Adversarial RAG (port 8202) - Red-teaming
- RAG Ingest (port 8200) - Document ingestion
- RAG Orchestrator (port 8210) - API gateway

**Network:** rag_network (172.23.0.0/16)

**Data Flow:**
```
Documents → RAG Ingest → [Weaviate/Milvus]
                ↓              ↓
         Embeddings      Vector Storage
                ↓              ↓
         RAG Orchestrator ←────┘
                ↓
    ┌───────────┼───────────┐
    ↓           ↓           ↓
PrivateGPT  Extreme RAG  Adversarial RAG
    ↓           ↓           ↓
  32K ctx    128K ctx    Attack Testing
```

**Storage:**
- privategpt_data - PrivateGPT data
- anythingllm_data - AnythingLLM workspace
- weaviate_data - Weaviate vectors
- milvus_data - Milvus vectors
- rag_documents - Document storage
- rag_embeddings - Embedding cache

### 7. Security Stack

**Services:**
- Caddy (ports 80/443) - Auto HTTPS proxy
- Nginx SSL (ports 8443/8080) - Alternative proxy
- Certbot - SSL certificate management
- Tailscale - Mesh VPN
- WireGuard (port 51820) - VPN server
- Vault (port 8200) - Secrets management
- Fail2ban - Intrusion prevention
- CrowdSec - Behavioral IPS
- Firewall - iptables manager
- AdGuard (port 53/3053) - DNS security
- Trivy (port 8081) - Vulnerability scanner
- Kong (port 8000/8001) - API gateway
- OAuth2 Proxy (port 4180) - SSO
- Security Dashboard (port 8300) - Monitoring

**Networks:** 
- security_network (172.24.0.0/16)
- dmz_network (172.25.0.0/16)

**Data Flow:**
```
External Request → DMZ Network → Caddy/Nginx → Kong Gateway
                                      ↓              ↓
                                  SSL/TLS      Rate Limiting
                                      ↓              ↓
                              Security Network → Fail2ban/CrowdSec
                                      ↓              ↓
                                OAuth2 Proxy → Internal Services
                                      ↓
                                  Vault (Secrets)
```

**Storage:**
- caddy_data - Caddy state
- caddy_config - Caddy config
- letsencrypt_data - SSL certificates
- wireguard_config - WireGuard peers
- tailscale_data - Tailscale state
- vault_data - Vault encrypted data
- nginx_certs - Nginx certificates

## Inter-Service Communication

### Primary Communication Paths

1. **Voice → Models:**
   - VoiceWing → Ollama (LLM inference)
   - Voice Router → Agent Orchestrator (task delegation)

2. **Agents → RAG:**
   - Semantic Search → Weaviate/Milvus
   - LocalGPT → ChromaDB
   - Doc Intelligence → RAG Ingest

3. **Automation → Agents:**
   - AI Browser Agent → Code Analyst
   - Scraper → File Editor
   - RPA → Agent Orchestrator

4. **Security → All:**
   - All services → Vault (secrets)
   - External access → Caddy → Services
   - Monitoring → Security Dashboard

### API Integration Matrix

```
┌───────────────┬─────────┬─────────┬───────┬─────────┬─────┐
│ Service       │ Ollama  │ ChromaDB│ Qdrant│ Selenium│ Vault│
├───────────────┼─────────┼─────────┼───────┼─────────┼─────┤
│ VoiceWing     │   ✓     │         │       │         │      │
│ Agents        │   ✓     │   ✓     │   ✓   │         │  ✓   │
│ Automation    │   ✓     │         │       │   ✓     │  ✓   │
│ RAG           │   ✓     │   ✓     │   ✓   │         │  ✓   │
│ Security      │         │         │       │         │  ✓   │
└───────────────┴─────────┴─────────┴───────┴─────────┴─────┘
```

## Resource Requirements

### Compute Resources

| Stack | CPU (cores) | RAM (GB) | Disk (GB) | GPU |
|-------|------------|----------|-----------|-----|
| Core | 2-4 | 8 | 100 | No |
| Models | 4-8 | 16 | 200 | Yes |
| VoiceWing | 2-4 | 4 | 20 | Yes |
| Agents | 2-4 | 8 | 50 | No |
| Automation | 2-4 | 8 | 20 | No |
| RAG | 4-8 | 16 | 100 | No |
| Security | 1-2 | 4 | 20 | No |
| **Total** | **17-36** | **64** | **510** | **2** |

### Port Allocation

**Core Services:**
- 5432: PostgreSQL
- 6379: Redis
- 6333: Qdrant
- 9090: Prometheus
- 3000: Grafana

**VoiceWing:**
- 8080: Open WebUI
- 9000: Whisper ASR
- 10200: Piper TTS
- 5002: Coqui TTS
- 8765: Silero VAD
- 8766: Voice Router
- 11434: Ollama

**Agents:**
- 5111: LocalGPT
- 8000: AutoGPT
- 8001: ChromaDB
- 8002: Doc Intelligence
- 8003: Code Analyst
- 8004: Semantic Search
- 8005: File Editor
- 8010: Orchestrator
- 5433: PGVector

**Automation:**
- 4444: Selenium Hub
- 7900-7902: Browser VNC
- 8090: RPA Server
- 8091: Automation API
- 8092: AI Browser Agent
- 8093: Screen Capture
- 8094: Web Scraper
- 9323: Playwright

**RAG:**
- 8001: PrivateGPT
- 3001: AnythingLLM
- 8080: Weaviate
- 19530: Milvus
- 8200: RAG Ingest
- 8201: Extreme RAG
- 8202: Adversarial RAG
- 8210: RAG Orchestrator

**Security:**
- 80/443: Caddy HTTP/HTTPS
- 8443: Nginx SSL
- 2019: Caddy Admin
- 51820: WireGuard
- 8200: Vault
- 53: AdGuard DNS
- 3053: AdGuard Web
- 8081: Trivy
- 8000/8001: Kong
- 4180: OAuth2 Proxy
- 8300: Security Dashboard

## Deployment Modes

### 1. Full Stack
All services deployed for complete functionality.
```bash
docker-compose -f docker-compose.yml \
               -f docker-compose.voicewing.yml \
               -f docker-compose.agents.yml \
               -f docker-compose.automation.yml \
               -f docker-compose.rag.yml \
               -f docker-compose.security.yml \
               up -d
```

### 2. Research Mode
Core + Models + RAG for AI research.
```bash
docker-compose -f docker-compose.yml \
               -f docker-compose.rag.yml \
               up -d
```

### 3. Automation Mode
Core + Automation + Agents for RPA.
```bash
docker-compose -f docker-compose.yml \
               -f docker-compose.agents.yml \
               -f docker-compose.automation.yml \
               up -d
```

### 4. Voice Mode
Core + VoiceWing for voice interfaces.
```bash
docker-compose -f docker-compose.voicewing.yml up -d
```

### 5. Production Mode
Core + Security for public deployment.
```bash
docker-compose -f docker-compose.yml \
               -f docker-compose.security.yml \
               up -d
```

## Security Architecture

### Defense in Depth

**Layer 1: Network Perimeter**
- DMZ network isolation
- Caddy/Nginx reverse proxy
- Kong API gateway with rate limiting

**Layer 2: Access Control**
- OAuth2 Proxy for SSO
- Vault for secrets management
- RBAC in services

**Layer 3: Intrusion Detection**
- Fail2ban auto-blocking
- CrowdSec behavioral analysis
- Security dashboard monitoring

**Layer 4: Application Security**
- TLS/SSL everywhere
- API authentication
- Content security policies

**Layer 5: Network Security**
- VPN access (Tailscale/WireGuard)
- Network segmentation
- Firewall rules

**Layer 6: Monitoring**
- Prometheus metrics
- Grafana dashboards
- Audit logging

### Security Best Practices

1. **Secrets Management:**
   - All secrets in Vault
   - No plaintext credentials
   - Automatic rotation

2. **Network Isolation:**
   - Separate networks per stack
   - DMZ for external services
   - Internal-only services

3. **Access Control:**
   - OAuth2 for authentication
   - API keys for services
   - RBAC for operations

4. **Encryption:**
   - TLS/SSL for all HTTP
   - VPN for remote access
   - Encrypted volumes

5. **Monitoring:**
   - Real-time dashboards
   - Alert on anomalies
   - Audit all access

## Scaling Considerations

### Horizontal Scaling

**Stateless Services (can scale easily):**
- Ollama workers
- Browser nodes (Selenium)
- RAG query engines
- Automation API instances

**Stateful Services (require coordination):**
- PostgreSQL (replication)
- Redis (cluster mode)
- Vector databases (sharding)

### Vertical Scaling

**Memory-intensive:**
- Ollama (model loading)
- RAG services (embeddings)
- Browser automation (multiple sessions)

**CPU-intensive:**
- Voice processing (Whisper)
- Code analysis
- Document parsing

**GPU-accelerated:**
- LLM inference (Ollama)
- Speech recognition (Whisper)
- TTS generation

## Monitoring & Observability

### Metrics Collection

**Prometheus Targets:**
- All HTTP services (/metrics)
- Docker container stats
- System resources (node-exporter)

**Grafana Dashboards:**
- System overview
- Service health
- Resource utilization
- API performance

### Logging

**Centralized Logging:**
- All services → JSON logs
- Standardized format
- Searchable/filterable

**Log Levels:**
- ERROR: Service failures
- WARN: Performance issues
- INFO: Normal operations
- DEBUG: Detailed traces

### Alerting

**Critical Alerts:**
- Service down
- High error rate
- Resource exhaustion
- Security events

**Warning Alerts:**
- High latency
- Resource pressure
- Rate limit approaching

## Backup & Recovery

### Data Protection

**Critical Data:**
- PostgreSQL database
- Vector databases (Qdrant, Weaviate, Milvus)
- Vault data
- Model configurations

**Backup Strategy:**
- Daily automated backups
- Retention: 30 days
- Off-site storage
- Encryption at rest

### Disaster Recovery

**Recovery Time Objective (RTO):** 1 hour
**Recovery Point Objective (RPO):** 24 hours

**Recovery Steps:**
1. Restore core infrastructure
2. Restore databases from backup
3. Rebuild container images
4. Restart services
5. Verify functionality

---

**Architecture Version:** 1.0  
**Last Updated:** 2025-11-21  
**Maintainer:** Strategickhaos AI Lab Team

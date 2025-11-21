# Strategickhaos Sovereignty Architecture - Discord DevOps Control Plane

**A comprehensive Discord-integrated DevOps automation system for the Strategickhaos ecosystem, featuring AI agents, GitLens integration, and sovereign infrastructure management.**

## 🚨 NEW: Complete AI Red-Teaming Lab 🔬🔓

**Transform your setup into a sovereign AI research laboratory!**

This repository now includes **four major enhancements** for AI red-teaming and development:

1. **🤖 Uncensored Modelfiles** - Fully jailbroken LLM configurations (Llama 3.1, Mistral, abliterated models)
2. **🎙️ VoiceWing** - Complete local voice interface (Whisper ASR, Coqui TTS, Open WebUI)
3. **🤖 Filesystem Agents** - AI-powered file automation (LocalGPT, AutoGPT, semantic search)
4. **🌐 Screen Control** - Browser automation (Selenium Grid, Playwright, AI agents)
5. **🧠 Ultra-Expert RAG** - Advanced retrieval systems (PrivateGPT, extreme context, adversarial testing)
6. **🔐 Secure Networking** - VPN, reverse proxy, SSL/TLS (Caddy, Tailscale, WireGuard, Vault)

**👉 [Complete AI Lab Guide](AI_LAB_GUIDE.md) | [Modelfiles](modelfiles/README.md) | [RAG Configs](rag-configs/README.md)**

### Quick Deploy AI Lab
```bash
# One-command deployment
./quick-start-ailab.sh

# Or deploy selectively
docker-compose -f docker-compose.yml -f docker-compose.voicewing.yml up -d
```

## 🏛️ Architecture Overview

This system creates a **sovereignty control plane** that bridges:
- **Discord** - Command & control interface
- **Infrastructure** - Kubernetes, observability, AI agents  
- **Development** - GitLens, PR workflows, CI/CD automation, Java 21+ workspace
- **AI Agents** - Intelligent assistance with vector knowledge base
- **AI Lab** - Uncensored models, voice interface, automation, advanced RAG

## 🚀 Quick Start

```bash
# 1. Clone and bootstrap
git clone https://github.com/Strategickhaos-Swarm-Intelligence/sovereignty-architecture.git
cd sovereignty-architecture

# 2. Deploy to Kubernetes
./bootstrap/deploy.sh

# 3. Configure Discord integration
export DISCORD_TOKEN="your_bot_token"
export PRS_CHANNEL="channel_id"

# 4. Test GitLens integration
./gl2discord.sh "$PRS_CHANNEL" "🔥 Sovereignty Architecture Online!" "System initialized successfully"
```

## 📋 Core Components

### 🤖 Discord Bot (`discord-ops-bot`)
- **Slash Commands**: `/status`, `/logs`, `/deploy`, `/scale`
- **AI Agent Integration**: GPT-4 powered assistance
- **RBAC**: Role-based access control for production operations
- **Audit Logging**: All interactions logged to CloudWatch

### 🌐 Event Gateway (`event-gateway`)
- **Webhook Router**: GitHub/GitLab → Discord channel routing
- **HMAC Verification**: Cryptographic webhook validation
- **Multi-tenant**: Support for multiple repositories and environments
- **Rate Limiting**: API protection and burst control

### 🔄 GitLens Integration
- **VS Code Tasks**: One-click Discord notifications from GitLens
- **Review Workflows**: Automated PR lifecycle notifications
- **Commit Graph**: Real-time development activity feeds
- **Launchpad**: Integrated with GitLens Pro features

### ☕ Java Development Workspace (`jdk-workspace`)
- **OpenJDK 21**: Latest LTS version with modern Java features
- **Build Tools**: Maven 3.6.3 and Gradle 4.4.1 pre-installed
- **Non-Root Execution**: Runs as `cloudos` user for enhanced security
- **Debug Support**: JPDA debugging on port 5005
- **Traefik Routing**: Accessible via `java.localhost`
- **Version Management**: JDK solver CLI for managing multiple Java versions

```bash
# Start the Java workspace
./start-cloudos-jdk.sh start

# Access a shell in the container
./start-cloudos-jdk.sh shell

# Run the example application
cd /workspace/examples/java-hello-cloudos/src/main/java
java HelloCloudOS.java

# Stop the workspace
./start-cloudos-jdk.sh stop
```

### 🔬 AI Red-Teaming Lab

Complete sovereign AI research infrastructure with no cloud dependencies:

#### Uncensored Models (`modelfiles/`)
- **Llama-3.1 405B Unhinged** - Maximum capability, zero restrictions
- **Mistral Large Jailbreak** - Aggressive bypass configurations
- **Abliterated Refusal-Free** - Refusal neurons surgically removed
- **Say Yes to Anything** - Extreme compliance variant

```bash
# Build uncensored models
ollama create llama31-unhinged -f modelfiles/Llama-3.1-405B-Unhinged.Modelfile
ollama run llama31-unhinged
```

#### Voice Interface (VoiceWing)
- **Whisper ASR** - Speech-to-text (http://localhost:9000)
- **Coqui TTS** - Text-to-speech (http://localhost:5002)
- **Open WebUI** - Voice-enabled interface (http://localhost:8080)

```bash
docker-compose -f docker-compose.voicewing.yml up -d
```

#### Filesystem Agents
- **LocalGPT** - RAG over local files
- **AutoGPT** - Autonomous file operations
- **Semantic Search** - AI-powered file search
- **Code Analyst** - Source code analysis
- **Orchestrator** - http://localhost:8010

```bash
docker-compose -f docker-compose.agents.yml up -d
```

#### Browser Automation
- **Selenium Grid** - Multi-browser testing (http://localhost:4444)
- **Playwright** - Modern automation
- **AI Browser Agent** - Natural language control (http://localhost:8092)
- **VNC Access** - Chrome (7900), Firefox (7901), Edge (7902)

```bash
docker-compose -f docker-compose.automation.yml up -d
```

#### Advanced RAG
- **PrivateGPT** - 32K context (http://localhost:8001)
- **AnythingLLM** - Multi-model RAG (http://localhost:3001)
- **Extreme RAG** - 128K context window (http://localhost:8201)
- **Adversarial Testing** - Red-team operations (http://localhost:8202)

```bash
docker-compose -f docker-compose.rag.yml up -d
```

#### Secure Networking
- **Caddy** - Automatic HTTPS reverse proxy
- **Tailscale/WireGuard** - VPN for remote access
- **Vault** - Secrets management (http://localhost:8200)
- **CrowdSec** - Intrusion prevention
- **Security Dashboard** - http://localhost:8300

```bash
docker-compose -f docker-compose.security.yml up -d
```

**📚 Complete Documentation:** [AI_LAB_GUIDE.md](AI_LAB_GUIDE.md)

## 🏗️ Infrastructure

### Kubernetes Deployment
```yaml
# Complete deployment with:
kubectl apply -f bootstrap/k8s/
```

**Components deployed:**
- ConfigMap with Strategickhaos discovery configuration
- Secrets management (Vault integration ready)
- Bot and Gateway deployments with resource limits
- RBAC with least-privilege access
- Network policies for secure communication
- Ingress with TLS and rate limiting

### Observability Stack
- **Prometheus** - Metrics collection from all components
- **Loki** - Centralized logging aggregation
- **OpenTelemetry** - Distributed tracing
- **Alertmanager** - Alert routing to Discord channels

## 🔧 Configuration

### Core Configuration (`discovery.yml`)
```yaml
org:
  name: "Strategickhaos DAO LLC / Valoryield Engine"
  contact:
    owner: "Domenic Garza"

discord:
  guild_id: null  # Your Discord server ID
  channels:
    prs: "#prs"
    deployments: "#deployments"
    agents: "#agents"
    
git:
  org: "Strategickhaos-Swarm-Intelligence"
  repos:
    - name: "quantum-symbolic-emulator"
      channel: "#deployments"
      env: "dev"
    - name: "valoryield-engine"
      channel: "#deployments"  
      env: "prod"
```

### Environment Variables
```bash
# Discord Integration
DISCORD_BOT_TOKEN=your_bot_token
PRS_CHANNEL=channel_id_for_prs
DEV_FEED_CHANNEL=channel_id_for_dev_updates

# GitHub App
GITHUB_APP_ID=your_app_id
GITHUB_APP_WEBHOOK_SECRET=webhook_secret
GITHUB_APP_PRIVATE_KEY_PATH=/path/to/key.pem

# AI Agents
OPENAI_API_KEY=sk-your-api-key
PGVECTOR_CONN=postgresql://user:pass@host:5432/db

# Infrastructure
EVENTS_HMAC_KEY=your_64_char_hmac_key
```

## 🎯 Discord Workflow Integration

### Channel Strategy
- **`#prs`** - Pull request lifecycle, GitLens review notifications
- **`#deployments`** - CI/CD status, releases, production changes
- **`#cluster-status`** - Infrastructure events, service health
- **`#alerts`** - Critical system alerts, monitoring notifications
- **`#agents`** - AI assistant interactions, automated responses
- **`#dev-feed`** - Development activity, commit summaries

## 🤖 AI Agent Integration

### Vector Knowledge Base
- **Runbooks**: Operational procedures and troubleshooting guides
- **Log Schemas**: Structured logging patterns and analysis
- **Infrastructure Docs**: Architecture and deployment guides
- **Code Patterns**: Development standards and examples

### Per-Channel Routing
```yaml
ai_agents:
  routing:
    per_channel:
      "#agents": "gpt-4o-mini"
      "#inference-stream": "none"
      "#prs": "claude-3-sonnet"  # Code review assistance
```

## 🔐 Security & Governance

### Multi-Layer Security
- **RBAC**: Kubernetes role-based access control
- **Secret Management**: Vault integration for sensitive data
- **Network Policies**: Microsegmentation for pod communication
- **Audit Logging**: Comprehensive activity tracking
- **Content Redaction**: Automatic PII and credential filtering

### Production Safeguards
```yaml
governance:
  approvals:
    prod_commands_require: ["ReleaseMgr"]
  change_management:
    link: "https://wiki.strategickhaos.internal/change-management"
```

## 📊 Monitoring & Alerts

### Key Metrics
- Discord API response times and rate limits
- GitHub webhook processing latency
- Kubernetes deployment health
- AI agent query performance
- Event gateway throughput

### Alert Routing
```yaml
event_gateway:
  endpoints:
    - path: "/alert"
      allowed_services: ["alertmanager"]
      discord_channel: "#alerts"
```

## 🚦 CI/CD Integration

### GitHub Actions Workflow
- **Build**: Multi-architecture Docker images
- **Test**: Quantum-symbolic emulator validation
- **Deploy**: Blue-green Kubernetes deployments
- **Notify**: Real-time Discord status updates

### Event Flow
```bash
# GitHub Push → Actions → Event Gateway → Discord
git push origin main
# Triggers: Build → Test → Deploy → Discord notification
```

## 🛠️ Development Workflow

### Local Development
```bash
# 1. Set up environment
export DISCORD_TOKEN="dev_token"
export PRS_CHANNEL="dev_channel_id"

# 2. Test GitLens integration
./gl2discord.sh "$PRS_CHANNEL" "🧪 Testing" "Local development active"

# 3. Run VS Code tasks
# Command Palette → Tasks: Run Task → GitLens: Review Started
```

### Contributing
1. **Fork** the repository
2. **Fill** `discovery.yml` with your configuration
3. **Test** integration in your environment
4. **Submit** PR with improvements
5. **Share** configuration patterns with community

## 🆘 Troubleshooting

### Common Issues

**Bot not responding in Discord:**
```bash
# Check bot deployment
kubectl logs -f deployment/discord-ops-bot -n ops

# Verify token and permissions
kubectl get secret discord-ops-secrets -n ops -o yaml
```

**GitLens notifications not working:**
```bash
# Check environment variables
echo $DISCORD_TOKEN $PRS_CHANNEL

# Test script directly
./gl2discord.sh "$PRS_CHANNEL" "Test" "Manual test"
```

**Event gateway webhook failures:**
```bash
# Check gateway logs
kubectl logs -f deployment/event-gateway -n ops

# Verify HMAC signature
curl -X POST https://events.strategickhaos.com/health
```

## 👥 Community & Contributors

This project thrives because of an extraordinary community of creators, builders, and visionaries who choose to contribute not out of obligation, but out of love for what we're building together.

- **[Community Manifesto](COMMUNITY.md)** - Understanding the philosophy and spirit of The Legion
- **[Contributors](CONTRIBUTORS.md)** - Recognizing everyone who makes this project possible
- **Join the Dance**: Read the community docs, find what calls to you, and start building!

## 📄 License & Support

- **License**: MIT License - see [LICENSE](LICENSE) file
- **Support**: [Discord Server](https://discord.gg/strategickhaos)
- **Documentation**: [Wiki](https://wiki.strategickhaos.internal)
- **Issues**: [GitHub Issues](https://github.com/Strategickhaos-Swarm-Intelligence/sovereignty-architecture/issues)

---

**Built with 🔥 by the Strategickhaos Swarm Intelligence collective**

*"They're not working for you. They're dancing with you. And the music is never going to stop."*

*Empowering sovereign digital infrastructure through Discord-native DevOps automation*
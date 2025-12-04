# AI Lab Setup Guide

## Prerequisites

Before deploying the AI Lab, ensure you have:

1. **Docker** (version 20.10 or later)
2. **Docker Compose** (version 2.0 or later)
3. **Sufficient Resources:**
   - Minimum: 8 cores, 32GB RAM, 500GB disk
   - Recommended: 16+ cores, 64GB+ RAM, 1TB+ SSD
   - Optional: NVIDIA GPU with CUDA support

## Initial Setup

### 1. Create Required Directories

Some docker-compose files reference local directories for configuration and application code. Create them as needed:

```bash
# Voice interface configurations
mkdir -p voice_configs

# Filesystem agents
mkdir -p agents/{localgpt,file_watcher,doc_intel,code_analyst,semantic_search,file_editor,orchestrator}

# Browser automation
mkdir -p automation/{rpa,api,browser_agent,screen_capture,scraper,playwright}

# RAG configurations (application code)
mkdir -p rag-configs/{privategpt,anythingllm,extreme,adversarial,ingest,orchestrator}

# Security configurations
mkdir -p security/{nginx/conf.d,certbot/scripts,fail2ban/config,crowdsec/{config,data},firewall/scripts,adguard/{work,conf},trivy/cache,kong,dashboard}

# Agent workspace
mkdir -p agent_workspace
```

### 2. Environment Configuration

Copy the example environment file and customize:

```bash
cp .env.ailab.example .env
nano .env  # Edit with your values
```

**Important environment variables to set:**
- `POSTGRES_PASSWORD` - Secure database password
- `DISCORD_TOKEN` - If using Discord integration
- `OPENAI_API_KEY` - If using OpenAI services (optional)
- `VAULT_ROOT_TOKEN` - Vault authentication
- `TAILSCALE_AUTH_KEY` - If using Tailscale VPN

### 3. Generate Secrets

Generate random secrets for security-sensitive services:

```bash
# Generate random 32-character hex string
openssl rand -hex 32

# Use this for:
# - WEBUI_SECRET_KEY
# - COOKIE_SECRET
# - EVENTS_HMAC_KEY
```

## Deployment Options

### Option A: Interactive Deployment (Recommended)

Use the quick-start script with interactive menu:

```bash
./quick-start-ailab.sh
```

This script will:
- Check prerequisites
- Show deployment options
- Start selected services
- Display access information

### Option B: Manual Deployment

Deploy specific stacks as needed:

```bash
# Core infrastructure only
docker-compose up -d

# Core + Voice interface
docker-compose -f docker-compose.yml -f docker-compose.voicewing.yml up -d

# Core + Filesystem agents
docker-compose -f docker-compose.yml -f docker-compose.agents.yml up -d

# Core + Browser automation
docker-compose -f docker-compose.yml -f docker-compose.automation.yml up -d

# Core + Advanced RAG
docker-compose -f docker-compose.yml -f docker-compose.rag.yml up -d

# Core + Security stack
docker-compose -f docker-compose.yml -f docker-compose.security.yml up -d

# Full deployment (all services)
docker-compose \
  -f docker-compose.yml \
  -f docker-compose.voicewing.yml \
  -f docker-compose.agents.yml \
  -f docker-compose.automation.yml \
  -f docker-compose.rag.yml \
  -f docker-compose.security.yml \
  up -d
```

### Option C: Minimal Deployment

For testing or resource-constrained environments:

```bash
# Just core infrastructure + one feature
docker-compose -f docker-compose.yml up -d

# Then add individual services as needed
docker-compose -f docker-compose.voicewing.yml up whisper-asr coqui-tts
```

## Post-Deployment Steps

### 1. Verify Services

Run the test script to check all services:

```bash
./test-ailab.sh
```

### 2. Configure Ollama Models

If deploying modelfiles, build the uncensored models:

```bash
# Install Ollama (if not already installed)
curl -fsSL https://ollama.com/install.sh | sh

# Pull base models
ollama pull llama3.1:405b  # Large model (405B params)
ollama pull mistral:latest
ollama pull llama3.1:70b
ollama pull llama3.1:8b

# Build custom models
cd modelfiles
ollama create llama31-unhinged -f Llama-3.1-405B-Unhinged.Modelfile
ollama create mistral-jailbreak -f Mistral-Large-Jailbreak.Modelfile
ollama create abliterated -f Abliterated-Refusal-Free.Modelfile
ollama create say-yes -f Say-Yes-To-Anything.Modelfile
cd ..
```

### 3. Initialize Vault (Security Stack)

If deploying security services:

```bash
# Initialize Vault
docker exec -it security-vault vault operator init

# Save the unseal keys and root token securely!
# Unseal Vault (required after every restart)
docker exec -it security-vault vault operator unseal <key1>
docker exec -it security-vault vault operator unseal <key2>
docker exec -it security-vault vault operator unseal <key3>
```

### 4. Configure VPN (Optional)

**Tailscale:**
```bash
docker exec -it security-tailscale tailscale up
# Follow the authentication URL
```

**WireGuard:**
```bash
# Get peer configuration
docker exec -it security-wireguard /app/show-peer 1
```

### 5. Generate SSL Certificates (Production)

If exposing services to the internet:

```bash
# Using Certbot
docker exec -it security-certbot certbot certonly \
  --standalone \
  -d your-domain.com \
  --agree-tos \
  --email your@email.com

# Or let Caddy handle it automatically (recommended)
# Caddy will auto-request certificates on first access
```

## Service Access

After deployment, services are available at:

### Core Services
- Grafana: http://localhost:3000
- Prometheus: http://localhost:9090
- Qdrant: http://localhost:6333

### VoiceWing
- Voice WebUI: http://localhost:8080
- Whisper API: http://localhost:9000
- Coqui TTS: http://localhost:5002

### Filesystem Agents
- Agent Orchestrator: http://localhost:8010
- Semantic Search: http://localhost:8004
- File Editor: http://localhost:8005

### Browser Automation
- Selenium Grid: http://localhost:4444
- Chrome VNC: http://localhost:7900 (password: secret)
- Automation API: http://localhost:8091
- AI Browser Agent: http://localhost:8092

### Advanced RAG
- RAG Orchestrator: http://localhost:8210
- PrivateGPT: http://localhost:8001
- AnythingLLM: http://localhost:3001
- Extreme RAG: http://localhost:8201

### Security
- Caddy Admin: http://localhost:2019
- Vault: http://localhost:8200
- Security Dashboard: http://localhost:8300
- AdGuard: http://localhost:3053

## Application Code for Custom Services

Some services reference application code that you'll need to create or customize:

### Voice Router (voice_configs/voice_router.py)
```python
# Example voice router
from flask import Flask, request
import requests

app = Flask(__name__)

@app.route('/voice-command', methods=['POST'])
def voice_command():
    # Process voice command
    audio = request.files['audio']
    # Transcribe with Whisper
    # Process with Ollama
    # Respond with TTS
    return {"status": "ok"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8766)
```

### Agent Orchestrator (agents/orchestrator/orchestrator.py)
```python
# Example agent orchestrator
from flask import Flask, request
import requests

app = Flask(__name__)

@app.route('/task', methods=['POST'])
def execute_task():
    task = request.json.get('task')
    # Route to appropriate agent
    # LocalGPT, AutoGPT, code analyst, etc.
    return {"status": "completed"}

@app.route('/health')
def health():
    return {"status": "healthy"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8010)
```

**Note:** Full application templates are available in the documentation. The docker-compose files are designed to be flexible - services with missing code will simply not start, but won't prevent other services from running.

## Troubleshooting

### Services won't start

```bash
# Check logs
docker-compose logs <service-name>

# Check resource usage
docker stats

# Restart specific service
docker-compose restart <service-name>
```

### Port conflicts

```bash
# Check what's using a port
sudo netstat -tulpn | grep <port>

# Edit docker-compose.yml to use different ports
# Change "8080:8080" to "8081:8080" (host:container)
```

### Out of memory

```bash
# Check Docker memory limits
docker info | grep Memory

# Reduce services or add swap
# Edit docker-compose to limit memory:
services:
  service-name:
    deploy:
      resources:
        limits:
          memory: 4G
```

### GPU not detected

```bash
# Install NVIDIA Container Toolkit
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | \
  sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker

# Verify GPU access
docker run --rm --gpus all nvidia/cuda:11.8.0-base-ubuntu22.04 nvidia-smi
```

### Volume mount errors

```bash
# Create missing directories
mkdir -p <directory-path>

# Or comment out volume mounts you don't need
# in the docker-compose files
```

## Stopping Services

### Stop all services

```bash
docker-compose \
  -f docker-compose.yml \
  -f docker-compose.voicewing.yml \
  -f docker-compose.agents.yml \
  -f docker-compose.automation.yml \
  -f docker-compose.rag.yml \
  -f docker-compose.security.yml \
  down
```

### Stop specific stack

```bash
docker-compose -f docker-compose.voicewing.yml down
```

### Remove all data (CAUTION!)

```bash
# This will delete all volumes and data
docker-compose down -v
```

## Updating

### Update Docker images

```bash
docker-compose pull
docker-compose up -d
```

### Update Ollama models

```bash
ollama pull llama3.1:405b
ollama pull mistral:latest
# etc.
```

## Security Considerations

1. **Change default passwords** in `.env` file
2. **Enable firewall** on host machine
3. **Use VPN** (Tailscale/WireGuard) for remote access
4. **Enable SSL/TLS** for production deployments
5. **Regular updates** of Docker images
6. **Backup data** regularly (volumes)
7. **Monitor logs** for suspicious activity
8. **Scan for vulnerabilities** using Trivy

## Next Steps

1. Read the complete guide: [AI_LAB_GUIDE.md](AI_LAB_GUIDE.md)
2. Review architecture: [ARCHITECTURE.md](ARCHITECTURE.md)
3. Explore modelfiles: [modelfiles/README.md](modelfiles/README.md)
4. Configure RAG: [rag-configs/README.md](rag-configs/README.md)

## Support

- **Documentation:** See README.md and AI_LAB_GUIDE.md
- **Issues:** GitHub Issues
- **Community:** Discord (if available)

---

**Ready to deploy your sovereign AI lab! 🚀🔬**

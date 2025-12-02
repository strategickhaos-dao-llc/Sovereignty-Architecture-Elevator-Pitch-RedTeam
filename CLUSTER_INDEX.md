# Strategickhaos Cluster - File Index

**Complete reference guide to all cluster-related files and their purposes.**

## 📚 Quick Navigation

- **Getting Started**: [CLUSTER_QUICKSTART.md](#documentation)
- **Full Guide**: [CLUSTER_DEPLOYMENT.md](#documentation)
- **Hardware Details**: [FLEET_SPECIFICATIONS.md](#documentation)
- **Setup Script**: [scripts/setup-cluster.sh](#scripts)

---

## 📖 Documentation Files

### Primary Guides

| File | Size | Description |
|------|------|-------------|
| **[CLUSTER_QUICKSTART.md](CLUSTER_QUICKSTART.md)** | 7.0 KB | 30-minute quick start guide - get up and running fast |
| **[CLUSTER_DEPLOYMENT.md](CLUSTER_DEPLOYMENT.md)** | 11.8 KB | Comprehensive deployment guide with all details |
| **[FLEET_SPECIFICATIONS.md](FLEET_SPECIFICATIONS.md)** | 9.9 KB | Hardware specs, capabilities, and cost analysis |
| **[CLUSTER_INDEX.md](CLUSTER_INDEX.md)** | This file | Complete file index and navigation guide |

### What to Read When

- **First Time Setup**: Start with `CLUSTER_QUICKSTART.md`
- **Production Deployment**: Read `CLUSTER_DEPLOYMENT.md` thoroughly
- **Hardware Planning**: Check `FLEET_SPECIFICATIONS.md`
- **Troubleshooting**: See troubleshooting sections in deployment guide

---

## 🔧 Configuration Files

### Docker Compose

| File | Purpose |
|------|---------|
| **[cluster-compose.yml](cluster-compose.yml)** | Main cluster orchestration file - deploy on all nodes |
| **[docker-compose.yml](docker-compose.yml)** | Original project compose (Discord/observability stack) |

**Key Services in cluster-compose.yml:**
- `ollama` - AI inference engine (all nodes)
- `open-webui` - Web interface (primary node)
- `voice-ai` - TTS service (nova-warrior only)
- `honeypot-gate` - Security monitoring (asteroth-gate only)
- `health-monitor` - Prometheus (nitro-lyra only)

### Monitoring

| File | Purpose |
|------|---------|
| **[monitoring/prometheus-cluster.yml](monitoring/prometheus-cluster.yml)** | Prometheus scrape config for all 4 nodes |

**Monitored Services:**
- Ollama API on each node
- Docker daemon metrics
- Node Exporter (system metrics)
- cAdvisor (container metrics)
- NVIDIA GPU metrics

### Web Content

| File | Purpose |
|------|---------|
| **[invite-html/index.html](invite-html/index.html)** | Honeypot landing page for asteroth-gate |

**Features:**
- Matrix-style terminal interface
- Cluster statistics display
- Security warnings
- Access logging

---

## 🛠️ Management Scripts

### Core Setup

| Script | Size | Purpose |
|--------|------|---------|
| **[scripts/setup-cluster.sh](scripts/setup-cluster.sh)** | 8.5 KB | Automated node setup - run on each machine |

**What it does:**
1. Installs Tailscale
2. Configures hostname
3. Installs Docker
4. Installs NVIDIA Container Toolkit
5. Sets up cluster directory

**Usage:**
```bash
./scripts/setup-cluster.sh
```

### Model Management

| Script | Size | Purpose |
|--------|------|---------|
| **[scripts/manage-models.sh](scripts/manage-models.sh)** | 7.8 KB | AI model pulling, sharing, and distribution |

**Commands:**
- `list` - Show installed models
- `pull <model>` - Pull a specific model
- `recommended` - Pull all recommended models
- `delete` - Remove a model
- `server` - Setup NFS model sharing (server)
- `client <ip>` - Connect to NFS share (client)
- `cluster` - Check models across all nodes

**Usage:**
```bash
./scripts/manage-models.sh recommended
./scripts/manage-models.sh cluster
```

### Health Monitoring

| Script | Size | Purpose |
|--------|------|---------|
| **[scripts/cluster-health.sh](scripts/cluster-health.sh)** | 7.6 KB | Real-time cluster monitoring and diagnostics |

**Commands:**
- `overview` - Cluster status dashboard (default)
- `models` - Model distribution across nodes
- `test` - Test inference on all nodes
- `resources` - Resource usage (requires SSH)
- `monitor` - Continuous monitoring mode

**Usage:**
```bash
./scripts/cluster-health.sh overview
./scripts/cluster-health.sh monitor  # Continuous
```

### Auto-Failover

| Script | Size | Purpose |
|--------|------|---------|
| **[scripts/auto-failover.sh](scripts/auto-failover.sh)** | 9.5 KB | Automatic failover between primary and backup nodes |

**Commands:**
- `monitor` - Start monitoring (runs continuously)
- `install` - Install as systemd service
- `uninstall` - Remove systemd service
- `test` - Test failover logic
- `status` - Show current status

**Usage:**
```bash
./scripts/auto-failover.sh install
./scripts/auto-failover.sh status
```

**How it works:**
- Monitors primary node (nitro-lyra) every 60 seconds
- Switches to backup (athina-throne) if primary fails
- Automatically restores when primary recovers
- Updates Open-WebUI configuration dynamically

### USB Boot Stick Generator

| Script | Size | Purpose |
|--------|------|---------|
| **[scripts/create-usb-bootstick.sh](scripts/create-usb-bootstick.sh)** | 9.9 KB | Create bootable USB for quick node addition |

**Features:**
- Creates bootable USB stick
- Auto-installs Tailscale + Docker
- Auto-joins cluster on boot
- Takes ~90 seconds to deploy new node

**Usage:**
```bash
sudo ./scripts/create-usb-bootstick.sh
```

⚠️ **Warning**: Will erase USB drive completely!

---

## 🎨 Diagrams

| File | Purpose |
|------|---------|
| **[cluster_architecture.dot](cluster_architecture.dot)** | Graphviz source for cluster architecture diagram |

**Generate SVG:**
```bash
dot -Tsvg cluster_architecture.dot -o cluster_architecture.svg
```

**Diagram includes:**
- All 4 nodes with specs
- Tailscale mesh network
- Service locations
- Model repository
- Access points
- Security features
- Cluster statistics

---

## 📋 Typical Workflows

### Initial Cluster Setup

1. **On each machine:**
   ```bash
   git clone <repo>
   cd Sovereignty-Architecture-Elevator-Pitch-
   ./scripts/setup-cluster.sh
   ```

2. **Log out and back in** (for Docker group)

3. **Deploy cluster on each machine:**
   ```bash
   cd ~/strategickhaos-cluster
   docker compose up -d
   ```

4. **Machine-specific services:**
   ```bash
   # On nitro-lyra
   docker compose --profile monitoring up -d
   
   # On nova-warrior
   docker compose --profile voice up -d
   
   # On asteroth-gate
   docker compose --profile honeypot up -d
   ```

5. **Pull models (on athina-throne):**
   ```bash
   ./scripts/manage-models.sh recommended
   ```

6. **Setup model sharing:**
   ```bash
   # On athina-throne
   ./scripts/manage-models.sh server
   
   # On other nodes
   ./scripts/manage-models.sh client <athina-ip>
   ```

### Daily Operations

**Check cluster status:**
```bash
./scripts/cluster-health.sh overview
```

**Pull a new model:**
```bash
./scripts/manage-models.sh pull mistral:latest
```

**Test inference across cluster:**
```bash
./scripts/cluster-health.sh test
```

**Monitor logs:**
```bash
docker logs -f ollama
tail -f /var/log/strategickhaos-failover.log
```

### Maintenance

**Update cluster:**
```bash
docker compose pull
docker compose up -d
```

**Restart services:**
```bash
docker compose restart
```

**Clean up:**
```bash
docker system prune -a
./scripts/manage-models.sh delete
```

---

## 🔐 Access Points

Once deployed, access your cluster:

| Service | URL | Purpose |
|---------|-----|---------|
| **Open-WebUI** | http://nitro-lyra.tail-scale.ts.net:3000 | Main AI chat interface |
| **Ollama API (Primary)** | http://nitro-lyra.tail-scale.ts.net:11434 | Direct API access |
| **Ollama API (Training)** | http://athina-throne.tail-scale.ts.net:11434 | 405B models |
| **Ollama API (Voice)** | http://nova-warrior.tail-scale.ts.net:11434 | Fast inference |
| **Ollama API (Security)** | http://asteroth-gate.tail-scale.ts.net:11434 | Gateway node |
| **Voice AI (TTS)** | http://nova-warrior.tail-scale.ts.net:7850 | Text-to-speech |
| **Monitoring** | http://nitro-lyra.tail-scale.ts.net:9090 | Prometheus metrics |
| **Honeypot** | http://asteroth-gate.tail-scale.ts.net:8080 | Security monitoring |

---

## 📊 File Statistics

**Total Files Created**: 13  
**Total Documentation**: ~30 KB  
**Total Code**: ~50 KB  
**Languages**: Bash (6 scripts), YAML (2 configs), HTML (1 page), DOT (1 diagram)

### Breakdown by Type

- **Documentation**: 4 files (30 KB)
- **Scripts**: 6 files (50 KB)
- **Configuration**: 2 files (5 KB)
- **Web Content**: 1 file (8 KB)
- **Diagrams**: 1 file (8 KB)

---

## 🔍 Finding What You Need

### By Task

- **"I want to set up the cluster"** → `CLUSTER_QUICKSTART.md`
- **"I need detailed instructions"** → `CLUSTER_DEPLOYMENT.md`
- **"What hardware do I need?"** → `FLEET_SPECIFICATIONS.md`
- **"How do I monitor the cluster?"** → `scripts/cluster-health.sh`
- **"How do I manage models?"** → `scripts/manage-models.sh`
- **"How do I enable failover?"** → `scripts/auto-failover.sh`
- **"How do I add more nodes?"** → `scripts/create-usb-bootstick.sh`

### By Node

- **nitro-lyra (Primary)**: Main services + monitoring
- **athina-throne (Training)**: 405B models + NFS server
- **nova-warrior (Voice)**: Fast inference + TTS
- **asteroth-gate (Security)**: Honeypot + gateway

### By File Type

- **Markdown (`.md`)**: Documentation and guides
- **Bash (`.sh`)**: Executable scripts
- **YAML (`.yml`)**: Configuration files
- **HTML (`.html`)**: Web content
- **DOT (`.dot`)**: Diagram source

---

## 📚 Related Files

### Main Repository Files

- **[README.md](README.md)** - Main project README (updated with cluster info)
- **[docker-compose.yml](docker-compose.yml)** - Original Discord/DevOps stack
- **[.gitignore](.gitignore)** - Git ignore rules (updated for cluster)

### External Resources

- **Tailscale**: https://tailscale.com/kb/
- **Ollama**: https://github.com/ollama/ollama
- **Open-WebUI**: https://github.com/open-webui/open-webui
- **Docker Compose**: https://docs.docker.com/compose/

---

## 🆘 Troubleshooting Quick Reference

**Cluster not accessible?**
```bash
tailscale status
ping nitro-lyra.tail-scale.ts.net
```

**Ollama not starting?**
```bash
docker logs ollama
nvidia-smi
```

**Models not loading?**
```bash
df -h
docker exec ollama ollama list
```

**Failover not working?**
```bash
./scripts/auto-failover.sh status
sudo journalctl -u strategickhaos-failover -f
```

---

**Your complete cluster reference guide. 🚀**

*Everything you need, indexed and ready.*

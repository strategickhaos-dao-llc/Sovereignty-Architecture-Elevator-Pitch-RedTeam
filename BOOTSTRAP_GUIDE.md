# Sovereign Mesh Bootstrap Guide

## Executive Overview

The **Sovereign Mesh Bootstrap** system provides an omnipresent, autonomous deployment solution that intelligently detects your environment and deploys the complete Sovereignty Architecture stack with executive override capabilities.

## Quick Start

### For Windows Users

**Option 1: PowerShell Launcher (Recommended)**
```powershell
.\sovereign-mesh-bootstrap.ps1
```

**Option 2: Direct WSL Execution**
```powershell
wsl bash ./sovereign-mesh-bootstrap.sh
```

**Option 3: Git Bash Execution**
```powershell
& "C:\Program Files\Git\bin\bash.exe" ./sovereign-mesh-bootstrap.sh
```

### For Linux/macOS Users

```bash
bash ./sovereign-mesh-bootstrap.sh
```

## Features

### 🔍 Intelligent Environment Detection

The bootstrap system automatically detects:
- **Operating System**: Linux, macOS, Windows (WSL, Git Bash)
- **Shell Environment**: Native Bash, WSL, Git Bash, MSYS
- **PowerShell Detection**: Warns if incorrectly run in PowerShell
- **Prerequisites**: Checks for required tools (Docker, git, curl, jq)

### 🛠️ GitHub CLI Integration

- Automatically detects if `gh` CLI is in PATH
- Provides platform-specific installation instructions
- Allows continuation without gh CLI with feature warnings
- Verifies gh CLI version when available

### 🏗️ Infrastructure Deployment

Automatically deploys:
- **Docker Compose Services**: Main stack and observability
- **Kubernetes Control Plane**: If kubectl is available
- **Node.js Dependencies**: Discord bot and related services
- **Environment Configuration**: Generates .env from template

### 🤖 Omnipresent Autonomous Executive Override

The bootstrap configures an autonomous monitoring and override system:

**Key Features:**
- Continuous health monitoring
- Automatic container restart on failures
- Disk space management and cleanup
- Resource threshold monitoring
- Autonomous decision-making based on configurable rules

**Configuration Files:**
- `.sovereign-mesh/executive-override.yaml` - Override rules and thresholds
- `.sovereign-mesh/autonomous-monitor.sh` - Monitoring daemon
- `.sovereign-mesh/monitor.log` - Autonomous action logs

## Fixing Common Bootstrap Issues

### Issue: "-sh: error: not found" or "gh: not found"

**Cause**: GitHub CLI not in PATH or running in wrong shell

**Solutions:**

#### Windows (PowerShell)
```powershell
# Install via winget
winget install GitHub.cli

# OR via Chocolatey
choco install gh

# Then use PowerShell launcher
.\sovereign-mesh-bootstrap.ps1
```

#### WSL (Ubuntu/Debian)
```bash
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update && sudo apt install gh
```

#### macOS
```bash
brew install gh
```

#### Git Bash
Install from: https://github.com/cli/cli/releases/latest

### Issue: Running in Wrong Shell (PowerShell vs Bash)

**Symptom**: Script fails with syntax errors or "command not found"

**Detection**: The bootstrap automatically detects PowerShell and shows error:
```
CRITICAL: This script is being executed in PowerShell!
PowerShell cannot properly interpret Bash scripts.
```

**Solution**: Use the PowerShell wrapper instead:
```powershell
.\sovereign-mesh-bootstrap.ps1
```

This will automatically launch the bash script in the correct environment.

### Issue: Missing Docker or Docker Compose

**Symptom**: "Missing required dependencies: docker docker-compose"

**Solutions:**

#### Windows
```powershell
# Install Docker Desktop
winget install Docker.DockerDesktop
```

#### Linux
```bash
# Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Docker Compose
sudo apt-get install docker-compose-plugin
```

#### macOS
```bash
brew install --cask docker
```

### Issue: Port Conflicts

**Symptom**: Docker services fail to start due to port already in use

**Solution**:
```bash
# Check what's using ports
netstat -an | grep LISTEN | grep -E "3000|8080|9090|8200"

# Stop conflicting services or modify docker-compose.yml ports
```

## Advanced Configuration

### Executive Override Rules

Edit `.sovereign-mesh/executive-override.yaml` to customize autonomous behavior:

```yaml
override:
  enabled: true
  mode: "autonomous"  # or "manual", "advisory"
  
  thresholds:
    cpu_critical: 90       # CPU usage % trigger
    memory_critical: 85    # Memory usage % trigger
    disk_critical: 90      # Disk usage % trigger
    error_rate_critical: 5 # Errors per minute
    
  permissions:
    - "system:restart"     # Auto-restart failed services
    - "system:scale"       # Scale services up/down
    - "system:failover"    # Trigger failover procedures
    - "security:patch"     # Apply security patches
```

### Autonomous Monitor

Start/stop the autonomous monitor:

```bash
# Start
nohup ./.sovereign-mesh/autonomous-monitor.sh > .sovereign-mesh/monitor.log 2>&1 &

# Stop
pkill -f autonomous-monitor.sh

# View logs
tail -f .sovereign-mesh/monitor.log
```

### Custom Environment Variables

Edit `.env` to configure:

```bash
# Discord Integration
DISCORD_TOKEN=your_actual_token
DISCORD_GUILD_ID=your_guild_id
DISCORD_PR_CHANNEL_ID=channel_id

# GitHub App
GITHUB_WEBHOOK_SECRET=webhook_secret
GITHUB_APP_ID=app_id
GITHUB_APP_PRIVATE_KEY_PATH=/path/to/key.pem

# AI/ML APIs
OPENAI_API_KEY=sk-your-key
XAI_API_KEY=xai-your-key
ANTHROPIC_API_KEY=claude-your-key

# Vault
VAULT_ADDR=http://vault:8200
VAULT_TOKEN=your_token

# Security
HMAC_SECRET=generate_with_openssl_rand_hex_32
JWT_SECRET=generate_with_openssl_rand_hex_32
```

## Bootstrap Modes

### Development Mode (Default)

```bash
bash ./sovereign-mesh-bootstrap.sh
```

Deploys:
- Observability stack (Prometheus, Grafana, Loki)
- Development Vault instance
- Discord bot in dev mode
- Event gateway

### Production Mode

```bash
ENV=production bash ./sovereign-mesh-bootstrap.sh
```

Additional considerations:
- Use real secrets (not default dev values)
- Enable TLS/SSL for all endpoints
- Configure proper authentication
- Set up backup procedures

### Minimal Mode

Skip Docker deployment, only setup environment:

```bash
# Edit sovereign-mesh-bootstrap.sh and comment out deploy_infrastructure
```

## Verification

After bootstrap completes, verify deployment:

### Check Docker Services
```bash
docker compose ps
```

### Check Endpoints
```bash
# Grafana
curl http://localhost:3000

# Prometheus
curl http://localhost:9090

# Vault
curl http://localhost:8200/v1/sys/health

# Event Gateway
curl http://localhost:8080/health
```

### Check Logs
```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f grafana
docker compose logs -f prometheus
```

### Test Discord Integration
```bash
source .env
./gl2discord.sh "$DISCORD_PR_CHANNEL_ID" "🔥 Bootstrap Test" "System operational!"
```

## Troubleshooting

### Bootstrap Fails During npm install

```bash
# Clear npm cache
npm cache clean --force

# Use npm ci instead
npm ci

# Or skip node dependencies
# Comment out install_dependencies in bootstrap script
```

### Docker Compose Version Issues

```bash
# Check version
docker compose version  # New
docker-compose version  # Old

# The bootstrap tries both automatically
```

### Permissions Issues

```bash
# Linux/WSL - add user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Re-run bootstrap
bash ./sovereign-mesh-bootstrap.sh
```

### WSL Path Issues

```bash
# Ensure you're in the correct directory
pwd

# Convert Windows path to WSL path
cd /mnt/c/path/to/repo
```

## Integration with Existing Systems

### GitLens Integration

After bootstrap, configure GitLens tasks:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Notify Discord: Review Started",
      "type": "shell",
      "command": "./gl2discord.sh",
      "args": ["${env:DISCORD_PR_CHANNEL_ID}", "Review Started", "${input:prUrl}"]
    }
  ]
}
```

### GitHub Actions Integration

Use in CI/CD:

```yaml
- name: Bootstrap Sovereignty Architecture
  run: |
    bash ./sovereign-mesh-bootstrap.sh
  env:
    DISCORD_TOKEN: ${{ secrets.DISCORD_TOKEN }}
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### Kubernetes Integration

If kubectl is configured, the bootstrap automatically:
1. Creates ops namespace
2. Applies k8s manifests from bootstrap/k8s/
3. Waits for deployments
4. Verifies pod health

## Cleanup

Remove all deployed infrastructure:

```bash
# Stop services
docker compose down

# Remove volumes (WARNING: deletes all data)
docker compose down -v

# Clean Docker system
docker system prune -f

# Remove autonomous monitor
pkill -f autonomous-monitor.sh
rm -rf .sovereign-mesh/
```

## Security Considerations

### Secrets Management

1. **Never commit .env to version control**
   - Already in .gitignore
   - Use .env.example as template

2. **Rotate secrets regularly**
   ```bash
   # Generate new secrets
   openssl rand -hex 32  # For HMAC_SECRET
   openssl rand -hex 32  # For JWT_SECRET
   ```

3. **Use Vault in production**
   - Bootstrap deploys dev Vault
   - Configure production Vault separately
   - Store secrets in Vault, not .env

### Network Security

1. **Configure firewall rules**
   ```bash
   # Example: UFW on Linux
   sudo ufw allow 3000/tcp  # Grafana
   sudo ufw allow 9090/tcp  # Prometheus
   ```

2. **Use TLS/SSL**
   - Configure reverse proxy (nginx, Traefik)
   - Obtain certificates (Let's Encrypt)

3. **Restrict access**
   - Use VPN for sensitive services
   - Configure IP allowlists
   - Enable authentication on all services

## Support and Documentation

- **Architecture**: README.md
- **Deployment**: DEPLOYMENT.md
- **Boot Diagnostics**: BOOT_RECON.md
- **Community**: COMMUNITY.md
- **Security**: SECURITY.md

## FAQ

**Q: Can I run this without Docker?**
A: The bootstrap requires Docker for infrastructure services. You can skip Docker deployment by modifying the script, but core features will be unavailable.

**Q: Do I need GitHub CLI for basic operation?**
A: No, gh CLI is optional. The bootstrap allows you to continue without it, but some automation features may be limited.

**Q: What's the difference between WSL and Git Bash?**
A: WSL provides a full Linux environment. Git Bash provides minimal Unix tools on Windows. Both work, but WSL is recommended for better compatibility.

**Q: How do I update the deployment?**
A: Pull latest changes and re-run the bootstrap. It detects existing .env and asks before overwriting.

**Q: Can I customize which services are deployed?**
A: Yes, edit docker-compose.yml and docker-compose.obs.yml to enable/disable services.

**Q: Is the autonomous monitor safe to run?**
A: Yes, it only monitors and restarts unhealthy containers. Review `.sovereign-mesh/executive-override.yaml` to customize behavior.

---

## Quick Reference Card

```
╔════════════════════════════════════════════════════════════════╗
║  SOVEREIGN MESH BOOTSTRAP - QUICK REFERENCE                    ║
╚════════════════════════════════════════════════════════════════╝

┌─ Windows ─────────────────────────────────────────────────────┐
│ PowerShell:  .\sovereign-mesh-bootstrap.ps1                   │
│ WSL:         wsl bash ./sovereign-mesh-bootstrap.sh           │
│ Git Bash:    bash ./sovereign-mesh-bootstrap.sh               │
└───────────────────────────────────────────────────────────────┘

┌─ Linux/macOS ─────────────────────────────────────────────────┐
│ Direct:      bash ./sovereign-mesh-bootstrap.sh               │
└───────────────────────────────────────────────────────────────┘

┌─ After Bootstrap ─────────────────────────────────────────────┐
│ Status:      docker compose ps                                │
│ Logs:        docker compose logs -f                           │
│ Stop:        docker compose down                              │
│ Restart:     docker compose restart                           │
└───────────────────────────────────────────────────────────────┘

┌─ Endpoints ───────────────────────────────────────────────────┐
│ Grafana:     http://localhost:3000  (admin/admin)            │
│ Prometheus:  http://localhost:9090                            │
│ Vault:       http://localhost:8200  (token: root)            │
│ Gateway:     http://localhost:8080                            │
└───────────────────────────────────────────────────────────────┘

┌─ Autonomous Monitor ──────────────────────────────────────────┐
│ Start:       ./.sovereign-mesh/autonomous-monitor.sh &        │
│ Logs:        tail -f .sovereign-mesh/monitor.log              │
│ Config:      .sovereign-mesh/executive-override.yaml          │
└───────────────────────────────────────────────────────────────┘
```

---

**Built with 🔥 by the Strategickhaos Swarm Intelligence collective**

*"Omnipresent. Autonomous. Sovereign."*

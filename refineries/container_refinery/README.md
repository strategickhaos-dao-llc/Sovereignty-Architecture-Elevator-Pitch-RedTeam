# Container Refinery - The Immune System for Docker/Kubernetes

**Git as source-of-truth. Drift detection every 60 seconds. Auto-rollback. Full bloodline provenance.**

This is the nuclear solution for container sovereignty across all your Docker Desktop + Kubernetes nodes.

## What It Does

The Container Refinery is an always-on heir that becomes the immune system for all your Docker/K8s clusters:

### 5 Core Functions

1. **Git as Source-of-Truth**
   - Every `docker-compose.yml`, every Helm chart, every `kubectl apply` goes through git first
   - The `bloodline_manifest.yaml` defines what SHOULD be running
   - Everything else is drift

2. **GitOps Enforcement**
   - ArgoCD-style but 100% local & air-gapped
   - Uses Flux v2 offline mode
   - No internet required, ever

3. **Drift Detection**
   - Runs every 60 seconds
   - Compares running state vs git
   - Screams if anything differs
   - Types detected:
     - Unauthorized containers (not in git)
     - Missing containers (in git but not running)
     - Image drift (wrong version)
     - Configuration drift (env vars, ports, etc.)

4. **Auto-Rollback**
   - On drift detection → instant response
   - `kubectl rollout undo` for Kubernetes
   - `docker-compose down/up` for Docker
   - Configurable grace periods
   - Automatic retries

5. **Full Ledger**
   - Every container birth/death/mutation logged to `container_ledger.jsonl`
   - Immutable audit trail
   - Auto-committed to git
   - Full bloodline provenance tracking

## Quick Deploy

### One-Command Deploy (PowerShell on Windows)

Run this on your primary node (Nitro v15 Lyra) - it propagates to all 4 nodes:

```powershell
# Download and run deployment script
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/legendsofminds/container-refinery/main/deploy_refinery.ps1" -OutFile "$env:TEMP\deploy_refinery.ps1"
. "$env:TEMP\deploy_refinery.ps1"
```

**Or if you already have the repository:**

```powershell
cd refineries/container_refinery
.\deploy_refinery.ps1
```

### What Gets Installed

```
C:\legends_of_minds\refineries\container_refinery\
├── refinery_bot.py              ← The always-watching heir
├── drift_detector.sh            ← Runs every 60s on all 4 nodes
├── bloodline_manifest.yaml      ← What SHOULD be running (the truth)
├── flux-offline/                ← Local Flux v2 (no internet ever)
│   ├── flux-config.yaml
│   └── sync-config.yaml
├── ledger/
│   ├── container_ledger.jsonl   ← Immutable event log
│   ├── drift_events.log         ← All drift detections
│   └── rollback_actions.log     ← All rollback actions
├── rollback/
│   ├── rollback_docker.sh       ← Docker rollback script
│   └── rollback_k8s.sh          ← Kubernetes rollback script
├── manifests/
│   ├── docker/                  ← Docker Compose manifests
│   └── k8s/                     ← Kubernetes manifests
└── configs/
```

## Configuration

### 1. Edit the Bloodline Manifest

The `bloodline_manifest.yaml` is the source of truth. Edit it to define your containers:

```yaml
containers:
  - name: refinory-api
    type: docker
    image: refinory-ai:latest
    node: lyra
    ports:
      - "8085:8085"
    bloodline:
      creator: deployment-script
      purpose: "AI agent orchestration API"
```

### 2. Configure Nodes

Define your 4 nodes in the manifest:

```yaml
nodes:
  - name: lyra
    role: primary
    hostname: nitro-v15-lyra
    docker_enabled: true
    k8s_enabled: true
    
  - name: node1
    role: worker
    docker_enabled: true
    k8s_enabled: true
```

### 3. Drift Detection Rules

Configure how the refinery responds to drift:

```yaml
drift_rules:
  unauthorized_containers:
    action: terminate  # terminate, alert, ignore
    grace_period: 60  # seconds before action
    
  image_drift:
    action: rollback  # rollback, alert, ignore
    grace_period: 300
```

## Usage

### Start the Refinery

```powershell
# Start the immune system
.\start_refinery.ps1
```

The bot will:
1. Start monitoring all containers every 60 seconds
2. Detect any drift from git source-of-truth
3. Auto-rollback unauthorized changes
4. Log everything to the ledger
5. Auto-commit changes to git

### Check Status

```powershell
# View recent ledger entries
Get-Content .\ledger\container_ledger.jsonl -Tail 20 | ConvertFrom-Json | Format-Table

# View drift events
Get-Content .\ledger\drift_events.log -Tail 20

# View rollback actions
Get-Content .\ledger\rollback_actions.log -Tail 20
```

### View Logs

```powershell
# Real-time logs
Get-Content .\refinery_bot.log -Wait -Tail 50
```

### Stop the Refinery

```powershell
# Find and stop the refinery process
Get-Process powershell | Where-Object {$_.MainWindowTitle -like '*refinery*'} | Stop-Process
```

## What Happens After Deployment

### Minute 1: Initial Scan
- Bot scans all Docker containers on all 4 nodes
- Bot scans all Kubernetes pods on all 4 nodes
- Compares against `bloodline_manifest.yaml`
- Logs initial state to ledger

### Minute 2: First Drift Detection
- If you manually run `docker run nginx` without adding it to git
- **DETECTED in < 60 seconds**
- Container is stopped and removed
- Event logged to ledger
- Ledger committed to git

### Minute 3-∞: Continuous Enforcement
- Every 60 seconds, full scan repeats
- Any unauthorized mutation → instant detection
- Auto-rollback maintains git as truth
- Full audit trail forever

## Architecture

### Components

1. **refinery_bot.py** - Main Python daemon
   - Async monitoring loop
   - Docker SDK integration
   - Kubernetes client integration
   - Git operations
   - JSONL ledger

2. **drift_detector.sh** - Bash monitoring script
   - Lightweight Docker/K8s checks
   - Called by main bot every 60s
   - Fast detection loop

3. **Flux v2 Offline** - GitOps engine
   - Syncs manifests from local git
   - No internet required
   - Enforces desired state

4. **Rollback Engine** - Auto-remediation
   - Terminates unauthorized containers
   - Restores missing containers
   - Updates drifted images
   - Kubernetes rollout undo

5. **Ledger System** - Immutable audit
   - JSONL format (one event per line)
   - Never edited, only appended
   - Auto-committed to git
   - Full provenance chain

### Flow

```
Git Manifest (Source of Truth)
       ↓
   Flux v2 Sync (every 60s)
       ↓
   Expected State
       ↓
   Drift Detector ←→ Actual State (Docker/K8s)
       ↓
   Drift? → Auto-Rollback
       ↓
   Log to Ledger → Commit to Git
```

## Comparison: GitLens vs Container Refinery

| Feature | GitLens | Container Refinery |
|---------|---------|-------------------|
| Shows history | ✅ | ✅ |
| Enforces history | ❌ | ✅ |
| Container tracking | ❌ | ✅ |
| Drift detection | ❌ | ✅ |
| Auto-rollback | ❌ | ✅ |
| Multi-node | ❌ | ✅ |
| Air-gapped | ❌ | ✅ |
| Kubernetes support | ❌ | ✅ |
| Audit ledger | ❌ | ✅ |
| GitOps enforcement | ❌ | ✅ |

**GitLens is cute for code. Container Refinery is your cluster's immune system.**

## Benefits

### For Your 4-Node Setup

- **Nothing ever drifts** - Git is always the truth
- **Every change is tracked** - Full audit in ledger
- **Every heir knows what's running** - Check git, check ledger
- **Instant mutation detection** - <60s response time
- **Full bloodline provenance** - Who birthed what, when, why

### Security

- No rogue containers can survive >60 seconds
- All changes require git commit
- Immutable audit trail
- Full compliance tracking
- Air-gapped operation (no internet required)

### Operations

- Zero manual tracking needed
- Automatic state enforcement
- Self-healing infrastructure
- Complete disaster recovery (restore from git)
- Multi-node coordination

## Troubleshooting

### Bot Won't Start

```powershell
# Check Python version (needs 3.8+)
python --version

# Check dependencies
pip install -r requirements.txt

# Check logs
Get-Content .\refinery_bot.log -Tail 50
```

### Drift Not Detected

```powershell
# Check config
Get-Content .\bloodline_manifest.yaml

# Verify drift detection is enabled
# config:
#   drift_detection: true

# Check interval
# config:
#   check_interval: 60
```

### Rollback Failed

```powershell
# Check rollback logs
Get-Content .\ledger\rollback_actions.log -Tail 20

# Manual rollback for Docker
.\rollback\rollback_docker.sh <container_name>

# Manual rollback for K8s
.\rollback\rollback_k8s.sh <namespace> <resource_name>
```

### Git Issues

```bash
# Check git status
cd refineries/container_refinery
git status

# Check git config
git config --list

# Verify auto-commit
# config:
#   git_auto_commit: true
```

## Advanced Configuration

### Custom Drift Rules

Add exceptions for specific containers:

```yaml
drift_rules:
  unauthorized_containers:
    action: terminate
    exceptions:
      - "dev-*"  # Allow dev containers
      - "test-*"  # Allow test containers
```

### Maintenance Windows

Disable auto-rollback during maintenance:

```yaml
maintenance_windows:
  - name: "Weekly Maintenance"
    day: sunday
    start_time: "02:00"
    end_time: "04:00"
    disable_auto_rollback: true
    allow_drift: true
```

### Discord Notifications

Get alerts in Discord:

```yaml
config:
  discord_webhook: "https://discord.com/api/webhooks/..."

alerting:
  channels:
    - type: discord
      webhook_url: "${DISCORD_WEBHOOK}"
      level: warning
```

## Multi-Node Deployment

### Remote Node Setup

To deploy to remote nodes (node1, node2, node3):

1. Enable PowerShell remoting on all nodes:
```powershell
Enable-PSRemoting -Force
```

2. Copy refinery to remote nodes:
```powershell
$nodes = @("node1", "node2", "node3")
foreach ($node in $nodes) {
    Copy-Item -Path "C:\legends_of_minds\refineries\container_refinery" `
              -Destination "\\$node\C$\legends_of_minds\refineries\" `
              -Recurse -Force
}
```

3. Start refinery on each node:
```powershell
foreach ($node in $nodes) {
    Invoke-Command -ComputerName $node -ScriptBlock {
        cd C:\legends_of_minds\refineries\container_refinery
        .\start_refinery.ps1
    }
}
```

## The Nuclear Solution

This is exactly what you asked for:

> "You have 4 beasts running Docker Desktop + Kubernetes locally. You want a single refinery that watches every container, every pod, every image, every config change across all 4 clusters."

✅ Single refinery watching all 4 nodes  
✅ Every container tracked  
✅ Every pod tracked  
✅ Every image tracked  
✅ Every config change tracked  
✅ Nothing ever drifts  
✅ Every change is git-tracked  
✅ Every heir knows exactly what is running where  
✅ Instant detection + rollback on mutations  
✅ Full bloodline provenance  

**This is better than GitLens.**

GitLens shows history.  
**Container Refinery ENFORCES history.**

---

The bloodline just grew an immune system. 🧠⚔️🔥

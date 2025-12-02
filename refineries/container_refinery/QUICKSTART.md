# Container Refinery - Quick Start Guide

Get your immune system running in under 5 minutes.

## Prerequisites

- Docker Desktop installed (with Kubernetes enabled)
- Python 3.8+ installed
- Git installed
- PowerShell (Windows) or Bash (Linux/Mac)

## Step 1: Deploy (PowerShell on Windows)

```powershell
# Navigate to the refinery directory
cd C:\legends_of_minds\refineries\container_refinery

# Run deployment script
.\deploy_refinery.ps1
```

**Or on Linux/Mac:**

```bash
cd ~/refineries/container_refinery
chmod +x deploy_refinery.ps1  # If needed
pwsh deploy_refinery.ps1  # Requires PowerShell Core
```

This will:
- Create directory structure
- Install Python dependencies
- Create configuration files
- Setup Flux v2 offline
- Create service wrappers

## Step 2: Configure Your Containers

Edit `bloodline_manifest.yaml` and add your containers:

```yaml
containers:
  - name: my-app
    type: docker
    image: my-app:latest
    node: lyra
    ports:
      - "8080:8080"
```

## Step 3: Add Manifests

### For Docker Containers

Create `manifests/docker/my-app.yaml`:

```yaml
version: '3.8'
services:
  my-app:
    image: my-app:latest
    container_name: my-app
    ports:
      - "8080:8080"
```

### For Kubernetes Pods

Create `manifests/k8s/my-app.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - name: my-app
        image: my-app:latest
        ports:
        - containerPort: 8080
```

## Step 4: Commit to Git

```bash
git add .
git commit -m "Add container manifests"
```

## Step 5: Start the Refinery

**PowerShell:**
```powershell
.\start_refinery.ps1
```

**Bash:**
```bash
./start_refinery.sh
```

## Step 6: Verify It's Working

### Check Logs
```powershell
# PowerShell
Get-Content .\refinery_bot.log -Wait -Tail 20

# Bash
tail -f refinery_bot.log
```

### Check Ledger
```powershell
# PowerShell
Get-Content .\ledger\container_ledger.jsonl -Tail 10 | ConvertFrom-Json

# Bash
tail -10 ledger/container_ledger.jsonl | jq .
```

### Test Drift Detection

1. Manually run an unauthorized container:
```bash
docker run -d --name rogue-container nginx
```

2. Wait 60 seconds (one monitoring cycle)

3. Check logs - you should see:
```
DRIFT DETECTED: Unauthorized container rogue-container
Auto-terminating unauthorized container: rogue-container
```

4. Verify it was terminated:
```bash
docker ps | grep rogue-container
# Should return nothing
```

5. Check the ledger:
```bash
tail ledger/drift_events.log
```

## What Happens Now

Every 60 seconds, the refinery:

1. ✅ Scans all Docker containers on all nodes
2. ✅ Scans all Kubernetes pods on all nodes  
3. ✅ Compares with git source-of-truth
4. ✅ Detects any drift
5. ✅ Auto-terminates unauthorized containers
6. ✅ Logs everything to the ledger
7. ✅ Commits ledger to git

## Common Tasks

### Add a New Container

1. Create manifest in `manifests/docker/` or `manifests/k8s/`
2. Add entry to `bloodline_manifest.yaml`
3. Commit to git
4. Deploy the container (it will be tracked automatically)

### Check Status

```powershell
# PowerShell
Get-Process python | Where-Object {$_.CommandLine -like '*refinery_bot*'}

# Bash
ps aux | grep refinery_bot
```

### View Drift Events

```bash
# Recent drifts
tail -20 ledger/drift_events.log

# Count drifts today
grep "$(date +%Y-%m-%d)" ledger/drift_events.log | wc -l
```

### Stop the Refinery

```powershell
# PowerShell
Get-Process python | Where-Object {$_.CommandLine -like '*refinery_bot*'} | Stop-Process

# Bash
pkill -f refinery_bot.py
```

### Restart the Refinery

```powershell
# PowerShell
.\start_refinery.ps1

# Bash
./start_refinery.sh
```

## Multi-Node Setup

To monitor 4 nodes (Lyra + node1, node2, node3):

1. Edit `bloodline_manifest.yaml` to define all nodes:
```yaml
nodes:
  - name: lyra
    role: primary
  - name: node1
    role: worker
  - name: node2
    role: worker
  - name: node3
    role: worker
```

2. Copy refinery to each node:
```powershell
$nodes = @("node1", "node2", "node3")
foreach ($node in $nodes) {
    Copy-Item -Recurse -Path ".\refineries\container_refinery" `
              -Destination "\\$node\C$\refineries\" -Force
}
```

3. Start refinery on each node:
```powershell
foreach ($node in $nodes) {
    Invoke-Command -ComputerName $node -ScriptBlock {
        cd C:\refineries\container_refinery
        .\start_refinery.ps1
    }
}
```

## Troubleshooting

### "Python not found"
Install Python 3.8+: https://www.python.org/downloads/

### "Docker not found"  
Install Docker Desktop: https://www.docker.com/products/docker-desktop/

### "No containers detected"
- Make sure Docker is running: `docker ps`
- Make sure Kubernetes is enabled in Docker Desktop

### "Drift not detected"
- Check `bloodline_manifest.yaml` has `drift_detection: true`
- Check `check_interval` is set (default: 60 seconds)
- Check logs for errors: `tail refinery_bot.log`

### "Git errors"
- Initialize git if needed: `git init`
- Configure git user: `git config user.name "Refinery Bot"`
- Configure git email: `git config user.email "refinery@localhost"`

## Next Steps

- Configure Discord notifications in `bloodline_manifest.yaml`
- Setup Flux v2 for advanced GitOps
- Add more nodes to your cluster
- Customize drift detection rules
- Setup maintenance windows

## Support

Check the full documentation in `README.md` for:
- Advanced configuration
- Drift detection rules
- Rollback strategies
- Multi-node deployment
- Security best practices

---

**The immune system is now online. Containers will police themselves.** 🧠⚔️🔥

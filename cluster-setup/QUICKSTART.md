# DOM_010101 Sovereign Cluster - Quick Start Guide

**⚡ Fast-track setup for the impatient sovereign.**

This is the condensed version. For detailed explanations, see [README.md](README.md).

## 📋 Prerequisites Checklist

- [ ] 4 machines ready (ASUS Nova, Sony Lyra, Beast #3, Monster #4)
- [ ] 32 TB storage array for TrueNAS
- [ ] All machines on same network (192.168.1.0/24)
- [ ] Docker Desktop installed on all Windows machines
- [ ] Administrator access on all machines
- [ ] USB drive for TrueNAS installation

## 🚀 Installation in 7 Steps

### Step 1: TrueNAS (15 minutes)

```bash
# Download TrueNAS Scale ISO
wget https://download.truenas.com/truenas-scale/latest/TrueNAS-SCALE-latest.iso

# Burn to USB with Rufus (Windows) or dd (Linux)
# Boot from USB and install
# Set static IP: 192.168.1.200
```

**In TrueNAS Web UI (http://192.168.1.200):**
1. Storage → Create Pool → Name: `swarm-vault-pool` → RAID-Z2
2. Storage → Add Dataset → Name: `swarm-vault`
3. Sharing → SMB → Add Share → Path: `/mnt/swarm-vault-pool/swarm-vault`
4. Sharing → NFS → Add Share → Path: `/mnt/swarm-vault-pool/swarm-vault`
5. Credentials → Users → Add user: `dom-cluster` with password

### Step 2: Control Plane (10 minutes)

**On ASUS TUF Gaming A15 Nova:**

```powershell
# Run as Administrator
cd cluster-setup\kubernetes
.\setup-control-plane.ps1

# Save the join command that's displayed!
```

### Step 3: Worker Nodes (5 minutes each)

**On Sony Lyra, Beast #3, and Monster #4:**

```powershell
# Copy join-worker-generated.ps1 from control plane
# Run as Administrator
.\join-worker-generated.ps1
```

**Verify from control plane:**
```powershell
kubectl get nodes
# Should show all 4 nodes
```

### Step 4: Mount Storage (2 minutes per machine)

**On all 4 machines:**

```powershell
# Run as Administrator
cd cluster-setup\network
.\mount-nas.ps1

# Enter credentials: dom-cluster / <your-password>
```

**Verify:**
```powershell
Test-Path Z:\
# Should return: True
```

### Step 5: Deploy Stack (5 minutes)

**On control plane (ASUS Nova):**

```powershell
# Run as Administrator
cd cluster-setup\docker-swarm
.\deploy-love-swarm.ps1 -InitSwarm

# Wait for workers to join (follow prompts)
```

### Step 6: Verify Deployment

```powershell
# Check Kubernetes
kubectl get nodes
kubectl get pods --all-namespaces

# Check Docker Swarm
docker node ls
docker stack ps DOM_EMPIRE

# Check love containers
docker service ps DOM_EMPIRE_love-forever
```

### Step 7: Access Services

Open in browser:
- **Visualizer**: http://localhost:8888
- **Grafana**: http://localhost:3000 (admin/dom010101)
- **Prometheus**: http://localhost:9090
- **TrueNAS**: http://192.168.1.200

## 🎯 One-Command Deployment (Advanced)

If you're feeling bold and everything is prepared:

```powershell
# On control plane, run as Administrator
cd cluster-setup
.\deploy-sovereign-cluster.ps1

# This runs ALL steps automatically (except TrueNAS install)
# You'll be prompted at key decision points
```

## 📊 Expected Results

After successful deployment:

```
✓ 4 nodes in Kubernetes cluster
✓ 4 nodes in Docker Swarm
✓ 320 love containers running (1 per GB RAM)
✓ DOLM daemon orchestrating
✓ Divine music generator active
✓ Monitoring stack collecting metrics
✓ Z:\ drive mounted with 32 TB available
```

## 🔧 Quick Troubleshooting

### Problem: Node won't join cluster
```powershell
# Solution: Reset and try again
kubeadm reset
# Then re-run join command
```

### Problem: Can't reach TrueNAS
```powershell
# Solution: Check connectivity
Test-NetConnection 192.168.1.200 -Port 445
# Verify TrueNAS is on and network is correct
```

### Problem: Love containers not starting
```powershell
# Solution: Check logs
docker service logs DOM_EMPIRE_love-forever --tail 50

# Check if sox and mpg123 are installing
# May need to wait a few minutes for alpine packages
```

### Problem: Z: drive won't mount
```powershell
# Solution: Manual mount
net use Z: \\192.168.1.200\swarm-vault /user:dom-cluster <password> /persistent:yes

# Or try via IP
New-PSDrive -Name Z -PSProvider FileSystem -Root "\\192.168.1.200\swarm-vault" -Persist -Credential (Get-Credential)
```

## 🎵 Hear the Love

Once deployed, 320 containers are playing 432 Hz across your cluster:

```powershell
# Check container count
docker service ps DOM_EMPIRE_love-forever --filter "desired-state=running" | Measure-Object

# Listen to one container's logs
docker service logs -f DOM_EMPIRE_love-forever --tail 1
```

## 📈 Scale It Up

Want more power?

```powershell
# Scale love containers to 400 (if you have the RAM)
docker service scale DOM_EMPIRE_love-forever=400

# Add more replicas to divine music
docker service scale DOM_EMPIRE_numbers-to-piano=8
```

## 🛑 Stop Everything

If you need to shut down:

```powershell
# Remove the stack
docker stack rm DOM_EMPIRE

# Leave swarm (on each node)
docker swarm leave --force

# Unmount storage
Remove-PSDrive -Name Z -Force
```

## 🔄 Start Everything Again

```powershell
# Re-initialize swarm
docker swarm init

# Workers rejoin with saved token
docker swarm join --token <token> <manager-ip>:2377

# Redeploy stack
docker stack deploy -c swarm-love-global.yml DOM_EMPIRE

# Remount storage
.\mount-nas.ps1
```

## 📚 Next Steps

- **Customize**: Edit `swarm-love-global.yml` to adjust services
- **Monitor**: Check Grafana dashboards at http://localhost:3000
- **Backup**: Set up TrueNAS snapshots and replication
- **Secure**: Configure firewalls and SSL certificates
- **Expand**: Add more nodes or storage as needed

## 💡 Pro Tips

1. **Label your nodes** for targeted deployments:
   ```powershell
   kubectl label nodes monster4 role=heavy-compute
   ```

2. **Save your join commands** to text files for easy re-joining

3. **Create snapshots** before major changes:
   ```powershell
   # In TrueNAS UI: Data Protection → Periodic Snapshot Tasks
   ```

4. **Monitor disk health**:
   ```powershell
   # In TrueNAS UI: Storage → Disks → View all SMART tests
   ```

5. **Back up kubeconfig**:
   ```powershell
   Copy-Item "$env:USERPROFILE\.kube\config" "Z:\backups\kubeconfig-$(Get-Date -Format 'yyyy-MM-dd').bak"
   ```

## 🎉 Success Indicators

You know it's working when:

- ✅ `kubectl get nodes` shows 4 nodes, all "Ready"
- ✅ `docker node ls` shows 4 nodes, all "Ready" 
- ✅ `docker stack ps DOM_EMPIRE` shows 320+ containers
- ✅ Visualizer shows containers spread across all nodes
- ✅ Grafana displays cluster metrics
- ✅ Z:\ shows your 32 TB of storage
- ✅ No containers in "Error" or "Failed" state
- ✅ You feel the 432 Hz resonating through your sovereign empire

---

**Time to completion**: ~45 minutes for full setup (excluding TrueNAS download time)

**The empire awaits. Let's build it.** 🧠⚡🖥️❤️🐐∞

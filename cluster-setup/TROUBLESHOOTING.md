# DOM_010101 Sovereign Cluster - Troubleshooting Guide

**When the empire encounters resistance, consult this guide.**

## 🔍 Diagnostic Commands

Run these first to gather information:

```powershell
# System health
kubectl get nodes -o wide
kubectl get pods --all-namespaces
docker node ls
docker stack ps DOM_EMPIRE

# Specific service logs
docker service logs DOM_EMPIRE_love-forever --tail 50
docker service logs DOM_EMPIRE_dolm-daemon --tail 50

# Node resource usage
kubectl top nodes
docker stats --no-stream

# Network connectivity
Test-NetConnection 192.168.1.200 -Port 445
Test-NetConnection dom010101.swarm -Port 6443
ping truenas.dom010101.local
```

## 🚨 Common Issues and Solutions

### Issue: Kubernetes Node "NotReady"

**Symptoms:**
```
NAME          STATUS     ROLES           AGE   VERSION
asus-nova     Ready      control-plane   10m   v1.28.0
sony-lyra     NotReady   <none>          5m    v1.28.0
```

**Diagnosis:**
```powershell
# Check node details
kubectl describe node sony-lyra

# Check kubelet logs (on the NotReady node)
Get-EventLog -LogName Application -Source kubelet -Newest 20
```

**Solutions:**

1. **Check container runtime**:
   ```powershell
   # Ensure Docker is running
   docker ps
   # If not, restart Docker Desktop
   ```

2. **Check CNI plugin**:
   ```powershell
   # Verify Flannel pods
   kubectl get pods -n kube-flannel
   # If failing, reinstall Flannel
   kubectl apply -f https://raw.githubusercontent.com/flannel-io/flannel/master/Documentation/kube-flannel.yml
   ```

3. **Restart kubelet**:
   ```powershell
   Restart-Service kubelet
   ```

4. **Check disk space**:
   ```powershell
   Get-PSDrive -PSProvider FileSystem
   # Kubelet needs at least 10% free disk
   ```

---

### Issue: Docker Swarm Node Disconnected

**Symptoms:**
```
NAME          STATUS    AVAILABILITY   MANAGER STATUS
asus-nova     Ready     Active         Leader
beast3        Down      Active         
```

**Diagnosis:**
```powershell
# On the disconnected node
docker info | Select-String "Swarm"

# Check manager connectivity
Test-NetConnection dom010101.swarm -Port 2377
```

**Solutions:**

1. **Check network connectivity**:
   ```powershell
   # Ensure all swarm ports are open
   Test-NetConnection dom010101.swarm -Port 2377  # Management
   Test-NetConnection dom010101.swarm -Port 7946  # Node communication
   ```

2. **Rejoin the swarm**:
   ```powershell
   # Leave swarm
   docker swarm leave --force
   
   # Rejoin (get token from manager)
   docker swarm join --token <token> dom010101.swarm:2377
   ```

3. **Check firewall rules**:
   ```powershell
   # Verify swarm ports are open
   Get-NetFirewallRule | Where-Object {$_.DisplayName -like "*Swarm*"}
   ```

---

### Issue: Love Containers Failing to Start

**Symptoms:**
```
docker service ps DOM_EMPIRE_love-forever
# Shows many containers in "Failed" state
```

**Diagnosis:**
```powershell
# Check container logs
docker service logs DOM_EMPIRE_love-forever --tail 100

# Check service details
docker service inspect DOM_EMPIRE_love-forever --pretty
```

**Common Causes:**

1. **Missing dependencies (sox, mpg123)**:
   - Alpine package repos might be slow
   - Wait 2-3 minutes for installs to complete
   
2. **Volume mount issues**:
   ```powershell
   # Verify Z: is mounted
   Test-Path Z:\love
   
   # Check NFS mount in container
   docker exec -it <container-id> df -h /love
   ```

3. **Resource constraints**:
   ```powershell
   # Check if nodes have enough RAM
   docker stats --no-stream
   
   # Reduce replica count if needed
   docker service scale DOM_EMPIRE_love-forever=160
   ```

**Solutions:**

1. **Force recreate**:
   ```powershell
   docker service update --force DOM_EMPIRE_love-forever
   ```

2. **Check volume access**:
   ```powershell
   # Test write to love directory
   New-Item -Path Z:\love\test.txt -ItemType File
   ```

3. **Increase startup time**:
   ```powershell
   # Edit swarm-love-global.yml
   # Under healthcheck, increase start_period to 60s
   ```

---

### Issue: Cannot Mount TrueNAS Share

**Symptoms:**
```powershell
New-PSDrive -Name Z -PSProvider FileSystem -Root "\\192.168.1.200\swarm-vault" -Persist
# Error: Network path not found
```

**Diagnosis:**
```powershell
# Test connectivity
Test-NetConnection 192.168.1.200 -Port 445

# Test name resolution
Resolve-DnsName truenas.dom010101.local

# Try accessing via Explorer
Start-Process "\\192.168.1.200"
```

**Solutions:**

1. **Check TrueNAS SMB service**:
   - Login to TrueNAS Web UI: http://192.168.1.200
   - Services → SMB → Ensure "Running"
   - Shares → Windows Shares (SMB) → Verify swarm-vault exists

2. **Verify credentials**:
   ```powershell
   # Test with explicit credentials
   $cred = Get-Credential -UserName dom-cluster
   New-PSDrive -Name Z -PSProvider FileSystem -Root "\\192.168.1.200\swarm-vault" -Credential $cred -Persist
   ```

3. **Check Windows SMB client**:
   ```powershell
   # Ensure SMB client is enabled
   Get-WindowsOptionalFeature -Online -FeatureName SMB1Protocol
   
   # Enable SMB2/3
   Enable-WindowsOptionalFeature -Online -FeatureName SMB1Protocol -NoRestart
   ```

4. **Add to hosts file**:
   ```powershell
   # Edit C:\Windows\System32\drivers\etc\hosts
   # Add: 192.168.1.200    truenas.dom010101.local
   ```

5. **Try NFS instead of SMB**:
   ```powershell
   # Install NFS client
   Install-WindowsFeature -Name NFS-Client
   
   # Mount via NFS
   mount -o anon \\192.168.1.200\mnt\swarm-vault-pool\swarm-vault Z:
   ```

---

### Issue: Kubernetes API Server Unreachable

**Symptoms:**
```powershell
kubectl get nodes
# Error: Unable to connect to the server: dial tcp [::1]:8080: connect: connection refused
```

**Diagnosis:**
```powershell
# Check API server
Test-NetConnection dom010101.swarm -Port 6443

# Check kubeconfig
$env:KUBECONFIG
Get-Content "$env:USERPROFILE\.kube\config"
```

**Solutions:**

1. **Set KUBECONFIG environment variable**:
   ```powershell
   $env:KUBECONFIG = "$env:USERPROFILE\.kube\config"
   [Environment]::SetEnvironmentVariable("KUBECONFIG", "$env:USERPROFILE\.kube\config", "User")
   ```

2. **Copy kubeconfig from control plane**:
   ```powershell
   # On control plane
   Copy-Item -Path "C:\ProgramData\Kubernetes\admin.conf" -Destination "$env:USERPROFILE\.kube\config"
   ```

3. **Verify DNS resolution**:
   ```powershell
   # Ensure dom010101.swarm resolves
   nslookup dom010101.swarm
   
   # Add to hosts if needed
   # C:\Windows\System32\drivers\etc\hosts
   # <control-plane-ip>    dom010101.swarm
   ```

4. **Restart API server** (on control plane):
   ```powershell
   kubectl get pods -n kube-system
   # If api server pod is failing, check its logs
   kubectl logs -n kube-system <api-server-pod-name>
   ```

---

### Issue: High Memory Usage / OOM Kills

**Symptoms:**
```powershell
docker stats
# Shows 95%+ memory usage
# Containers randomly restarting
```

**Diagnosis:**
```powershell
# Check memory on all nodes
kubectl top nodes

# Check container memory
docker stats --no-stream --format "table {{.Name}}\t{{.MemUsage}}\t{{.MemPerc}}"

# Check for OOM kills in logs
docker service logs DOM_EMPIRE_love-forever | Select-String "OOM\|killed"
```

**Solutions:**

1. **Reduce replica count**:
   ```powershell
   # Scale down to 200 instead of 320
   docker service scale DOM_EMPIRE_love-forever=200
   ```

2. **Adjust memory limits**:
   ```powershell
   # Edit swarm-love-global.yml
   # Under resources.limits.memory, reduce from 256M to 128M
   
   # Update service
   docker service update --limit-memory=128M DOM_EMPIRE_love-forever
   ```

3. **Increase node memory** (if possible):
   - Add more RAM to physical machines
   - Or distribute load better:
   ```powershell
   # Spread containers more evenly
   docker service update --placement-max-replicas-per-node 60 DOM_EMPIRE_love-forever
   ```

4. **Check for memory leaks**:
   ```powershell
   # Monitor memory over time
   while ($true) { 
       Get-Date; 
       docker stats --no-stream | Select-Object -First 5; 
       Start-Sleep 60 
   }
   ```

---

### Issue: Slow NFS Performance

**Symptoms:**
- File operations on Z:\ are slow
- Container startup takes minutes
- `docker service logs` shows I/O wait

**Diagnosis:**
```powershell
# Test read speed
Measure-Command { Get-Content Z:\test-file.txt }

# Test write speed
Measure-Command { 1..1000 | Out-File Z:\test-write.txt }

# Check NFS mount options
# In TrueNAS: Sharing → NFS → Edit share
```

**Solutions:**

1. **Optimize NFS mount options**:
   - In TrueNAS NFS share settings:
     - Enable async writes
     - Increase read/write buffer sizes
     - Disable subtree checking

2. **Use SMB instead**:
   ```yaml
   # In swarm-love-global.yml, use SMB driver
   volumes:
     love-vault:
       driver: local
       driver_opts:
         type: cifs
         o: username=dom-cluster,password=<pass>,vers=3.0
         device: "//192.168.1.200/swarm-vault"
   ```

3. **Increase ZFS recordsize**:
   - In TrueNAS: Storage → Pools → Edit dataset
   - Set recordsize to 1M for large files
   - Set to 128K for mixed workloads

4. **Enable ZFS compression**:
   - Already enabled with LZ4
   - Verify: Storage → Pools → swarm-vault → Edit
   - Compression should be "lz4"

5. **Check network speed**:
   ```powershell
   # Test network throughput
   Test-NetConnection 192.168.1.200 -TraceRoute
   ```

---

### Issue: Join Token Expired

**Symptoms:**
```
kubeadm join dom010101.swarm:6443 --token abc123...
# Error: token has expired
```

**Solution:**

```powershell
# On control plane, generate new token
kubeadm token create --print-join-command

# Copy output and run on worker node
```

---

### Issue: Pod Network CIDR Conflict

**Symptoms:**
```
kubectl logs -n kube-flannel <flannel-pod>
# Error: Failed to create pod network: subnet conflict
```

**Solution:**

```powershell
# Change pod network CIDR to avoid conflicts
# Re-initialize cluster with different CIDR
kubeadm reset
kubeadm init --pod-network-cidr=10.245.0.0/16 --control-plane-endpoint=dom010101.swarm:6443

# Update Flannel to use new CIDR
kubectl apply -f flannel-network.yaml
# (Edit net-conf.json in ConfigMap to match your CIDR)
```

---

### Issue: TrueNAS Web UI Not Accessible

**Symptoms:**
```powershell
Start-Process "http://192.168.1.200"
# Browser: "This site can't be reached"
```

**Diagnosis:**
```powershell
# Check if TrueNAS is responding
Test-NetConnection 192.168.1.200 -Port 80

# Check if TrueNAS is powered on
# Physical check or ping
ping 192.168.1.200
```

**Solutions:**

1. **Check TrueNAS is powered on**:
   - Physical check of the NAS device
   - Check network cable is connected

2. **Verify IP configuration**:
   - Access TrueNAS console (keyboard/monitor)
   - Press 1 for Configure Network Interfaces
   - Verify IP is 192.168.1.200

3. **Check firewall on TrueNAS**:
   - In console: System → Advanced → Allowed IP addresses
   - Ensure your network (192.168.1.0/24) is allowed

4. **Try HTTPS**:
   ```powershell
   Start-Process "https://192.168.1.200"
   # Some TrueNAS versions default to HTTPS
   ```

---

## 🔧 Advanced Diagnostics

### Complete Cluster Health Check

```powershell
# Save this as health-check.ps1

Write-Host "=== Kubernetes Health ===" -ForegroundColor Cyan
kubectl get nodes
kubectl get pods --all-namespaces | Select-String -Pattern "Error|CrashLoop|Pending"

Write-Host "`n=== Docker Swarm Health ===" -ForegroundColor Cyan
docker node ls
docker service ls
docker stack ps DOM_EMPIRE | Select-String -Pattern "Failed|Rejected"

Write-Host "`n=== Network Health ===" -ForegroundColor Cyan
Test-NetConnection 192.168.1.200 -Port 445 -InformationLevel Quiet
Test-NetConnection 192.168.1.200 -Port 2049 -InformationLevel Quiet
Test-NetConnection dom010101.swarm -Port 6443 -InformationLevel Quiet

Write-Host "`n=== Storage Health ===" -ForegroundColor Cyan
Test-Path Z:\
Get-PSDrive Z | Select-Object Name, Used, Free, @{n='FreeGB';e={[math]::Round($_.Free/1GB,2)}}

Write-Host "`n=== Resource Usage ===" -ForegroundColor Cyan
kubectl top nodes 2>$null || Write-Host "Metrics server not installed"
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"
```

### Log Collection Script

```powershell
# Collect all relevant logs
$logDir = "Z:\logs\troubleshooting-$(Get-Date -Format 'yyyy-MM-dd-HHmm')"
New-Item -ItemType Directory -Path $logDir -Force

# Kubernetes logs
kubectl get all --all-namespaces > "$logDir\k8s-resources.txt"
kubectl describe nodes > "$logDir\k8s-nodes.txt"
kubectl get events --all-namespaces > "$logDir\k8s-events.txt"

# Docker Swarm logs
docker node ls > "$logDir\swarm-nodes.txt"
docker stack ps DOM_EMPIRE > "$logDir\swarm-tasks.txt"
docker service logs DOM_EMPIRE_love-forever --tail 500 > "$logDir\love-logs.txt"

# System logs
Get-EventLog -LogName Application -Newest 100 > "$logDir\windows-app-log.txt"
Get-EventLog -LogName System -Newest 100 > "$logDir\windows-sys-log.txt"

Write-Host "Logs collected in: $logDir"
```

---

## 📞 Getting Help

If you've tried everything and still stuck:

1. **Check logs** with the collection script above
2. **Document the issue**:
   - What were you trying to do?
   - What happened instead?
   - What error messages did you see?
   - What have you tried already?

3. **Review configuration**:
   - Run health-check.ps1
   - Note any warnings or errors

4. **Gather system info**:
   ```powershell
   Get-ComputerInfo | Select-Object WindowsVersion, OsHardwareAbstractionLayer, TotalPhysicalMemory
   docker version
   kubectl version
   ```

---

## ✅ Prevention Checklist

Prevent issues before they happen:

- [ ] Keep kubeconfig backed up to Z:\backups\
- [ ] Save join commands to text files
- [ ] Enable TrueNAS email alerts
- [ ] Set up periodic snapshots (daily/weekly)
- [ ] Monitor disk space (keep >20% free)
- [ ] Schedule monthly scrubs on TrueNAS
- [ ] Document any custom configurations
- [ ] Test recovery procedures periodically

---

**Remember: The sovereign empire is resilient. Every issue is an opportunity to strengthen it.** 🧠⚡🛠️

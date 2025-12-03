# Operator Checklist: Daily/Weekly Verification

## Daily Operations Checklist

### Morning System Check (5 minutes)

```bash
# Quick verification script
./check_ecosystem_empire.sh
```

**Manual Verification:**
- [ ] All 5 nodes responding (Nitro v15, Lyra, iPower, Athena, Sony)
- [ ] Tailscale mesh connected (green status)
- [ ] NAS accessible from all nodes
- [ ] Ollama services running on inference nodes
- [ ] No critical alerts in logs

### Quick Node Status Check

```bash
# Check all nodes via Tailscale
for node in nitro-v15 lyra ipower athena sony; do
    echo "=== $node ==="
    ssh $node.tailnet 'uptime && free -h && df -h | head -5'
done
```

**Expected Results:**
- [ ] System uptime > 0 (nodes are online)
- [ ] RAM usage < 90%
- [ ] Disk usage < 80%
- [ ] Load average reasonable for node type

### Service Health Check

```bash
# Ollama status on inference nodes
ssh nitro-v15.tailnet 'pgrep -a ollama'
ssh lyra.tailnet 'pgrep -a ollama'

# GPU status
ssh nitro-v15.tailnet 'nvidia-smi'
```

**Expected Results:**
- [ ] Ollama process running
- [ ] GPU temperature < 85°C
- [ ] GPU memory available
- [ ] No GPU errors

## Weekly Maintenance Checklist

### Monday: System Updates & Security

```bash
# Check for updates on all nodes
for node in nitro-v15 lyra ipower athena sony; do
    echo "Checking updates on $node..."
    ssh $node.tailnet 'sudo apt update && apt list --upgradable'
done

# Apply critical security updates (if any)
# Do this during low-usage hours
```

- [ ] Security updates identified
- [ ] Critical patches applied
- [ ] System reboot scheduled (if needed)
- [ ] Failover tested before reboot

### Tuesday: Storage & Backup Verification

```bash
# Check NAS capacity
df -h /mnt/nas

# Verify backup integrity (if automated backups exist)
ls -lh /mnt/nas/backups/latest/

# Check for old logs to archive
find /var/log -name "*.log" -mtime +30 -size +100M
```

- [ ] NAS capacity < 80% full
- [ ] Recent backups exist (if configured)
- [ ] Old logs archived or deleted
- [ ] Case files organized

### Wednesday: Performance Monitoring

```bash
# Check resource usage trends
for node in nitro-v15 lyra ipower athena sony; do
    echo "=== $node Performance ==="
    ssh $node.tailnet 'top -bn1 | head -20'
done

# Check network latency
for node in nitro-v15 lyra ipower athena sony; do
    ping -c 5 $node.tailnet | tail -1
done
```

- [ ] No nodes consistently maxed out
- [ ] Network latency < 50ms between nodes
- [ ] No unusual processes consuming resources
- [ ] GPU utilization appropriate for workload

### Thursday: Security Audit

```bash
# Check for unauthorized access attempts
sudo grep "Failed password" /var/log/auth.log | tail -20

# Verify Tailscale authorized devices
tailscale status | grep -E "Online|Offline"

# Check open ports
sudo ss -tuln | grep LISTEN
```

- [ ] No suspicious login attempts
- [ ] All Tailscale devices authorized
- [ ] Only expected ports open
- [ ] Firewall rules up to date

### Friday: Model & Data Verification

```bash
# Check Ollama models
ollama list

# Verify RAG database
ls -lh ~/.ollama/models/

# Check case file integrity (if applicable)
find /mnt/nas/Cases -name "*.pdf" -o -name "*.md" | wc -l
```

- [ ] Expected models present
- [ ] No corrupted model files
- [ ] RAG database accessible
- [ ] Case files organized and accessible

## Monthly Deep Dive Checklist

### Hardware Health Check

```bash
# Check disk SMART status (on each node)
sudo smartctl -a /dev/sda | grep -E "Health|Temperature"

# Check memory errors
sudo grep -i "memory" /var/log/syslog | tail -20

# Check thermal status
sensors | grep -E "Core|temp"
```

- [ ] All disks show "PASSED" health
- [ ] No memory errors logged
- [ ] CPU temperatures < 80°C
- [ ] GPU temperatures < 85°C

### Network Infrastructure Review

```bash
# Tailscale connection quality
tailscale ping nitro-v15.tailnet
tailscale ping lyra.tailnet
# ... repeat for all nodes

# Check bandwidth usage (if monitoring is set up)
# Review any unusual patterns
```

- [ ] All nodes reachable via Tailscale
- [ ] Latency consistent with baseline
- [ ] No unusual bandwidth spikes
- [ ] VPN overhead acceptable

### Capacity Planning

```bash
# Review growth trends
# - Storage usage over time
# - RAM usage patterns
# - GPU utilization trends
# - Case volume growth

# Calculate runway
echo "Storage usage trend: [X]GB/month"
echo "Estimated time until 80% full: [Y] months"
```

- [ ] Storage growth rate documented
- [ ] RAM usage trends noted
- [ ] GPU capacity sufficient
- [ ] Expansion plan (if needed)

### Documentation Update

- [ ] Update network diagram (if changes made)
- [ ] Document any configuration changes
- [ ] Update disaster recovery procedures
- [ ] Review and update this checklist

## Quarterly Checklist

### Full System Test

- [ ] **Failover Test**: Disable primary node, verify operations continue on secondary
- [ ] **Air-Gap Test**: Disconnect network, verify local operations work
- [ ] **Backup Restore Test**: Restore from backup, verify integrity
- [ ] **Security Scan**: Run vulnerability scanner, address findings
- [ ] **Performance Benchmark**: Compare against baseline, identify degradation

### Infrastructure Review

- [ ] Review hardware warranty status
- [ ] Plan hardware refresh (if needed)
- [ ] Review software licenses
- [ ] Update disaster recovery plan
- [ ] Test emergency procedures

### Business Continuity

- [ ] Review case load capacity
- [ ] Assess need for additional nodes
- [ ] Update cost analysis (vs cloud alternatives)
- [ ] Document lessons learned
- [ ] Plan infrastructure improvements

## Emergency Response Checklist

### Node Failure

```bash
# Identify failed node
tailscale status

# Switch to backup node
# (For Nitro v15 failure → use Lyra)
ssh lyra.tailnet

# Verify services running
pgrep ollama
docker ps

# Access shared data via NAS
ls -lh /mnt/nas/Cases/current/
```

- [ ] Failed node identified
- [ ] Backup node operational
- [ ] Services migrated
- [ ] Data accessible
- [ ] Client work continues uninterrupted

### Network Outage

```bash
# Verify which node you're on
hostname

# Check local services
ollama list
docker ps

# Access local data copies
ls -lh ~/local_cache/
```

- [ ] Confirm air-gap mode activated
- [ ] Local models available
- [ ] Local data accessible
- [ ] Work continues offline
- [ ] Plan reconnection when network restored

### Storage Failure

```bash
# Identify affected storage
df -h
dmesg | tail -50

# Check backup location
ls -lh /mnt/backup/

# Estimate data recovery time
```

- [ ] Failure scope identified
- [ ] Backup integrity verified
- [ ] Recovery plan initiated
- [ ] Critical data prioritized
- [ ] Client notification (if needed)

## Success Metrics

### Operational Metrics

- **Uptime Target**: > 99% per node
- **Response Time**: < 5 minutes for failover
- **Recovery Time**: < 1 hour for full node failure
- **Backup Frequency**: Daily (if configured)
- **Security Scan**: Weekly

### Business Metrics

- **Cost per Month**: ~$150 (electricity)
- **Cost per Case**: < $10 (vs $2000+ traditional)
- **Efficiency Gain**: 880x (1 operator vs 40-person team)
- **Margin**: > 95%
- **Client Satisfaction**: 100% (work continues despite failures)

## Quick Reference Commands

### Essential Commands

```bash
# Full system verification
./check_ecosystem_empire.sh

# Check all nodes
for node in nitro-v15 lyra ipower athena sony; do
    echo "=== $node ===" && ssh $node.tailnet 'uptime'
done

# Tailscale status
tailscale status

# Ollama models
ollama list

# Docker status
docker ps

# NAS access
ls -lh /mnt/nas/

# GPU status
nvidia-smi

# System resources
htop
```

### Emergency Contacts

- **Hardware Vendor**: [Contact Info]
- **ISP Support**: [Contact Info]
- **Backup Admin**: [Contact Info]
- **Legal Counsel**: [Contact Info]

---

## Notes

- This checklist assumes Tailscale mesh network is configured
- Adjust paths based on your actual NAS mount point
- Customize node names based on your actual hostnames
- Add any custom services to the monitoring list
- Keep this checklist updated as infrastructure evolves

---

**🔥 Remember**: You're not a "one laptop guy" - you're a **distributed, sovereign operator** with redundancy, mobility, and true independence.

**Your system is operational. Keep it that way.** 🚀

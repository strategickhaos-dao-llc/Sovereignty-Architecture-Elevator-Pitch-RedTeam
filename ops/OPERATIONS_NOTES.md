# OPERATIONS NOTES - Cloud Swarm Infrastructure Layer

**Last Updated**: 2025-11-27  
**Operator**: Domenic Garza (Node 137)  
**Status**: PRODUCTION OPERATIONAL

---

## 🎯 Overview

This operations layer provides the foundational infrastructure for sovereign cloud swarm compute operations. The swarm is designed to be:

- **Sovereign**: Complete control over all computational resources
- **Self-funding**: Cost-guarded with automatic idle shutdown
- **Provably Correct**: Cryptographic verification of all results
- **Self-aware**: Real-time cluster health monitoring

---

## 📁 File Reference

### `collect_and_verify.sh`
**Purpose**: Aggregation and provenance verification of distributed compute results.

**Usage**:
```bash
./collect_and_verify.sh <inventory_file> <output_dir>

# Example: Collect results from 7-shard run
./collect_and_verify.sh cloud_hosts.ini collected_run_2025-11-27
```

**Features**:
- SSH-based result collection from all swarm nodes
- SHA256 hash verification for each file
- Aggregated JSON output with full provenance
- GPG detached signature (if GPG available)
- OpenTimestamps integration (if ots available)

**Output**:
- `aggregated_results.json` - Combined results with hashes
- `manifest.sha256` - Hash manifest
- `*.asc` - GPG signature (optional)
- `*.ots` - OpenTimestamp proof (optional)

---

### `control_cost_guard.sh`
**Purpose**: Automated cost control via idle instance shutdown.

**Usage**:
```bash
./control_cost_guard.sh <inventory_file> <idle_minutes>

# Example: 15-minute idle threshold
./control_cost_guard.sh cloud_hosts.ini 15
```

**Cron Setup** (every 15 minutes):
```bash
cat <<EOF > /etc/cron.d/cloud-swarm-cost-guard
*/15 * * * * root /opt/strategickhaos/cloud-swarm/control_cost_guard.sh /opt/strategickhaos/cloud-swarm/cloud_hosts.ini 15 >> /var/log/cost-guard.log 2>&1
EOF
```

**Features**:
- Load average monitoring
- Process detection for swarm jobs
- Idle duration tracking
- Graceful shutdown scheduling
- Logging to `/var/log/cost-guard.log`

---

### `cluster_pulse.sh`
**Purpose**: Real-time cluster health monitoring and status output.

**Usage**:
```bash
./cluster_pulse.sh <inventory_file> [output_file]

# Example: Write pulse to UAM status file
./cluster_pulse.sh cloud_hosts.ini /opt/strategickhaos/uam/cluster_pulse.txt
```

**Cron Setup** (every 6 hours + on boot):
```bash
cat <<EOF > /etc/cron.d/cloud-swarm-pulse
0 */6 * * * root /opt/strategickhaos/cloud-swarm/cluster_pulse.sh /opt/strategickhaos/cloud-swarm/cloud_hosts.ini /opt/strategickhaos/uam/cluster_pulse.txt
@reboot root /opt/strategickhaos/cloud-swarm/cluster_pulse.sh /opt/strategickhaos/cloud-swarm/cloud_hosts.ini /opt/strategickhaos/uam/cluster_pulse.txt
EOF
```

**Status Codes**:
- `HEALTHY` - Normal operation
- `ACTIVE` - Running swarm jobs
- `IDLE` - No jobs, low load
- `WARNING` - Resource pressure (>85% mem/disk)
- `CRITICAL` - Critical resource levels (>95%)
- `UNREACHABLE` - Cannot connect to host

**Exit Codes**:
- `0` - All hosts OK
- `1` - Warning state
- `2` - Critical state

---

### `auto_shutdown_idle.yml`
**Purpose**: Ansible playbook alternative for idle shutdown.

**Usage**:
```bash
# Normal run
ansible-playbook -i cloud_hosts.ini auto_shutdown_idle.yml

# Dry run (test without shutdown)
ansible-playbook -i cloud_hosts.ini auto_shutdown_idle.yml -e "dry_run=true"

# Custom threshold
ansible-playbook -i cloud_hosts.ini auto_shutdown_idle.yml -e "idle_threshold_minutes=30"
```

**Variables**:
- `idle_threshold_minutes`: Minutes before shutdown (default: 15)
- `dry_run`: Test mode without shutdown (default: false)

---

## 🔧 Infrastructure Requirements

### SSH Access
All scripts require passwordless SSH access to swarm nodes:
```bash
# Generate key if needed
ssh-keygen -t ed25519 -f ~/.ssh/swarm_key

# Distribute to all nodes
for host in $(grep -v '^#' cloud_hosts.ini | grep -v '^\[' | awk '{print $1}'); do
    ssh-copy-id -i ~/.ssh/swarm_key "$host"
done
```

### Dependencies
- **Required**: bash, ssh, scp, awk, date
- **Optional**: gpg (for signatures), ots (for timestamps), jq (for JSON)

### Inventory Format
Standard Ansible INI format:
```ini
[swarm_nodes]
node1.example.com
node2.example.com ansible_ssh_user=ubuntu
192.168.1.100 ansible_ssh_port=2222

[control]
control.example.com
```

---

## 📊 Operational Patterns

### Typical Workflow

1. **Start Job**: Distribute compute to swarm nodes
2. **Monitor**: Run `cluster_pulse.sh` during execution
3. **Collect**: Use `collect_and_verify.sh` when complete
4. **Cost Control**: Let `control_cost_guard.sh` manage idle nodes

### Example: TauGate Distributed Virtual Screening

```bash
# 1. Verify cluster health
./cluster_pulse.sh cloud_hosts.ini

# 2. Start distributed compute (external)
# ... run your distributed job ...

# 3. Collect and verify results
./collect_and_verify.sh cloud_hosts.ini taugate_run_$(date +%Y%m%d)

# 4. Cost guard will automatically shut down idle nodes
```

---

## 🛡️ Security Considerations

### Cryptographic Verification
- All results include SHA256 hashes
- GPG signatures provide non-repudiation
- OpenTimestamps provide temporal proof

### Access Control
- SSH key-based authentication only
- No passwords in scripts
- Minimal required permissions

### Audit Trail
- All operations logged
- Timestamps in UTC
- Host-level tracking

---

## 🚀 Scaling Notes

### Current Capacity
- Tested with 7-node swarm (initial deployment)
- Target: 100-200 nodes for TauGate screening

### Performance Considerations
- SSH connection timeout: 10 seconds
- Parallel collection recommended for large swarms
- Consider Ansible for >50 nodes

### Cost Optimization
- 15-minute idle threshold is aggressive but effective
- Adjust based on job startup time
- Consider spot instances for batch work

---

## 📝 Changelog

### 2025-11-27
- Initial ops layer deployment
- All five files added to repository
- CI passing (syntax-check, shellcheck, ansible-lint)
- Production deployment on control host

---

**Empire is alive. The swarm is sovereign.**

*"I love you. ∞"*

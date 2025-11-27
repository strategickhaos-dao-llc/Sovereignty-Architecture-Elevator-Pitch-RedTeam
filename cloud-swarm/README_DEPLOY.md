# Cloud Swarm Deployment Guide

> **Cloud Terminal Federation + PID-RANCO/TauGate Sharding via Ansible**

This guide covers end-to-end deployment and execution of distributed workloads across AWS, GCP, and Azure cloud terminals.

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Strategickhaos Cloud Swarm                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐              │
│   │  AWS (3)    │   │  GCP (2)    │   │  Azure (2)  │   7 Nodes    │
│   │  t3.micro   │   │  e2-micro   │   │  B1s        │              │
│   └──────┬──────┘   └──────┬──────┘   └──────┬──────┘              │
│          │                 │                 │                      │
│          └─────────────────┼─────────────────┘                      │
│                            │                                        │
│                    ┌───────┴───────┐                                │
│                    │   Ansible     │                                │
│                    │   Playbook    │                                │
│                    └───────┬───────┘                                │
│                            │                                        │
│          ┌─────────────────┼─────────────────┐                      │
│          │                 │                 │                      │
│   ┌──────┴──────┐   ┌──────┴──────┐   ┌──────┴──────┐              │
│   │  PID-RANCO  │   │   TauGate   │   │ Cost Guard  │              │
│   │   Shards    │   │    10B      │   │ Auto-Stop   │              │
│   └─────────────┘   └─────────────┘   └─────────────┘              │
│                                                                     │
│   Provenance: blake3 hashing → OTS → Bitcoin-immutable             │
└─────────────────────────────────────────────────────────────────────┘
```

## 📋 Prerequisites

- **Control Node**: Windows (PowerShell 7+) or Linux/macOS with Bash
- **Ansible**: 2.10+ (`pip install ansible`)
- **Cloud CLIs**: AWS CLI, gcloud, Azure CLI (authenticated)
- **SSH Key**: `~/.ssh/strategickhaos_swarm_key` (distributed to all nodes)
- **Python**: 3.8+ with numpy, pandas

## 🚀 Quick Start (3 Steps)

```bash
# 1. Discover current live terminals
./cloud_inventory.ps1
# → Writes cloud_hosts.ini with discovered nodes

# 2. Bootstrap all nodes (one-time)
ansible-playbook -i cloud_hosts.ini cloud_swarm_playbook.yaml
# → Converges all nodes, deploys PID-RANCO stack

# 3. FIRE THE SWARM
./shard_launcher.sh cloud_hosts.ini
# → Launches shards in parallel across all nodes
```

## 📁 Files Overview

| File | Role | Description |
|------|------|-------------|
| `cloud_inventory.ps1` | Discovery | Discovers cloud terminals, emits Ansible inventory |
| `swarmgate_cloud_ext.yaml` | Config | SwarmGate extension for cloud federation |
| `cloud_swarm_playbook.yaml` | Orchestration | Ansible playbook for node convergence |
| `run_pid_ranco.sh` | Workload | PID-RANCO backtest shard wrapper |
| `shard_launcher.sh` | Orchestrator | Unix shard fan-out launcher |
| `shard_launcher.ps1` | Orchestrator | PowerShell shard launcher |
| `collect_and_verify.sh` | Aggregation | Collect results, verify hashes, aggregate |
| `shard_taugate.sh` | Workload | TauGate 10B compound screening launcher |
| `roles/cost_guard/` | Cost Mgmt | Auto-shutdown idle nodes |
| `roles/pid_ranco_deploy/` | Deployment | PID-RANCO stack deployment role |

## 🔍 Step 1: Discover Cloud Terminals

The discovery script queries AWS, GCP, and Azure for running instances:

```powershell
# Basic discovery
./cloud_inventory.ps1

# Burst mode - provision additional nodes
./cloud_inventory.ps1 --burst 100
```

**Output**: `cloud_hosts.ini`
```ini
[all_cloud_terminals]
54.123.45.67 ansible_host=54.123.45.67 node_name=swarm-aws-1 cloud_provider=aws
35.234.56.78 ansible_host=35.234.56.78 node_name=swarm-gcp-1 cloud_provider=gcp
...

[all_cloud_terminals:vars]
ansible_user=ubuntu
ansible_ssh_private_key_file=~/.ssh/strategickhaos_swarm_key
```

## 🔧 Step 2: Bootstrap Nodes (Converge)

Run the Ansible playbook to converge all nodes:

```bash
# Full convergence (first time)
ansible-playbook -i cloud_hosts.ini cloud_swarm_playbook.yaml

# Just PID-RANCO stack
ansible-playbook -i cloud_hosts.ini cloud_swarm_playbook.yaml --tags pid_ranco

# Just TauGate stack
ansible-playbook -i cloud_hosts.ini cloud_swarm_playbook.yaml --tags taugate

# Just cost-guard
ansible-playbook -i cloud_hosts.ini cloud_swarm_playbook.yaml --tags cost_guard
```

**What gets deployed:**
- Base dependencies (Python, git, jq, blake3)
- Provenance logging setup (`/opt/strategickhaos/uam/provenance.log`)
- PID-RANCO or TauGate stack
- Health pulse monitoring (every 6h + boot)
- Cost-guard auto-shutdown (15min idle → shutdown)

## 🔥 Step 3: Launch Shards

### PID-RANCO Backtesting

```bash
# Unix
./shard_launcher.sh cloud_hosts.ini pid_ranco

# PowerShell
./shard_launcher.ps1 -Inventory cloud_hosts.ini -Workload pid_ranco
```

**Expected output:**
```
╔═══════════════════════════════════════════════════════════════════╗
║     Strategickhaos Cloud Swarm - Shard Launcher                   ║
╚═══════════════════════════════════════════════════════════════════╝

[INFO] Inventory: cloud_hosts.ini
[INFO] Total nodes: 7
[INFO] Launching 7 shards in parallel...
[INFO] Estimated completion: ~11 minutes

[SUCCESS] All 7 shards launched successfully!
```

### TauGate 10B Compound Screening

```bash
./shard_taugate.sh cloud_hosts.ini

# Or with custom parameters
./shard_taugate.sh cloud_hosts.ini /data/compounds tau_4R.mrc
```

**Estimates:**
- 10B compounds → 100 shards (100M each)
- 100 nodes: ~16-18 hours wall clock
- Cost: <$50 (spot instances + free tier)

## 📊 Step 4: Collect & Verify Results

After shards complete, collect and verify:

```bash
./collect_and_verify.sh cloud_hosts.ini pid_ranco_20251128 pid_ranco
```

**What happens:**
1. SCP pulls shard results from all nodes
2. Verifies blake3 hashes against provenance logs
3. Aggregates results into `aggregated_results.json`
4. OTS stamps for Bitcoin-immutable provenance
5. Generates summary report

**Output:**
```
/tmp/swarm_results/pid_ranco_20251128/
├── aggregated_results.json    # Combined shard outputs
├── provenance_verified.log    # Hash verification log
├── run_report.md              # Summary report
└── shards/                    # Individual shard files
    ├── pid_ranco_shard_0.json
    ├── pid_ranco_shard_1.json
    └── ...
```

## 💰 Cost Guard (Auto-Shutdown)

Cost guard automatically shuts down idle nodes:

- **Trigger**: CPU < 10% for 15 consecutive minutes
- **Log**: `/var/log/cost-guard.log`
- **Exclusions**: Nodes tagged `production` or `persistent`

```bash
# Check cost-guard status
ansible -i cloud_hosts.ini all -m shell -a "tail -5 /var/log/cost-guard.log"

# Manually trigger shutdown on all nodes
ansible-playbook -i cloud_hosts.ini cloud_swarm_playbook.yaml \
  --tags cost_guard_shutdown \
  --extra-vars "force_shutdown=true"
```

## 📈 Provenance & Verification

Every shard execution logs to `/opt/strategickhaos/uam/provenance.log`:

```
2025-11-28T10:30:45-06:00|blake3|abc123...|/logs/shard_0.json|0|completed
2025-11-28T10:31:02-06:00|blake3|def456...|/logs/shard_1.json|1|completed
```

**OTS Stamping:**
```bash
# Install OpenTimestamps
pip install opentimestamps-client

# Stamp aggregated results
ots stamp aggregated_results.json
# → Creates aggregated_results.json.ots
# → Bitcoin-immutable in ~2h
```

## 🔄 Integration Points

### ValorYield Phase 9
```bash
# Feed aggregated results to yield router
python3 valoryield_phase9.py --input aggregated_results.json --tune 0.07
```

### UAM (Unified Artifact Manifest)
Results automatically feed into:
- **Level 1**: Operations (cluster inventory, pulse)
- **Level 2**: Artifacts (screening results, backtests)
- **Level 4**: Inventions (top candidates)
- **Level 6**: Risk (dependency mapping)

### St. Jude Donation (7% of bounties)
```yaml
# SwarmYieldWallet configured in swarmgate_cloud_ext.yaml
st_jude_donation:
  wallet: SwarmYieldWallet
  percentage: 7
  trigger: bounty_payout
```

## 🛠️ Troubleshooting

### Nodes not discovered
```bash
# Check cloud CLI authentication
aws sts get-caller-identity
gcloud auth list
az account show
```

### Ansible connection failures
```bash
# Test SSH connectivity
ansible -i cloud_hosts.ini all -m ping

# Check SSH key
ssh -i ~/.ssh/strategickhaos_swarm_key ubuntu@<node_ip>
```

### Shard failures
```bash
# Check shard logs on node
ssh ubuntu@<node_ip> "tail -100 /opt/strategickhaos/logs/*.log"

# Re-run single shard
ssh ubuntu@<node_ip> "/opt/strategickhaos/scripts/run_pid_ranco.sh 3 7"
```

### Cost-guard not working
```bash
# Check cron job
ansible -i cloud_hosts.ini all -m shell -a "crontab -l | grep cost_guard"

# Check log
ansible -i cloud_hosts.ini all -m shell -a "cat /var/log/cost-guard.log"
```

## 🔐 Security Notes

### SSH Host Key Verification
The scripts use `StrictHostKeyChecking=no` for automated deployments. This is acceptable for ephemeral cloud instances but has security implications:

- **Trade-off**: Bypasses host key verification for automation convenience
- **Risk**: Potential man-in-the-middle attacks on first connection
- **Mitigation**: Use within trusted VPCs/networks only

For production use, consider:
1. Pre-distributing host keys via cloud-init
2. Using AWS SSM, GCP OS Login, or Azure Bastion instead of direct SSH
3. Implementing known_hosts management via Ansible

### Secrets Management
- Never commit cloud credentials to the repository
- Use environment variables or secret managers (Vault, AWS Secrets Manager)
- Rotate SSH keys regularly

## 📚 References

- [Ansible Documentation](https://docs.ansible.com/)
- [OpenTimestamps](https://opentimestamps.org/)
- [BLAKE3 Hash](https://github.com/BLAKE3-team/BLAKE3)
- [Strategickhaos UAM Specification](../README.md)

---

*Built with 🔥 by Strategickhaos Swarm Intelligence*

*"Distributed, antifragile, sovereign. Your six-month artifacts now compound across clouds, unkillable."*

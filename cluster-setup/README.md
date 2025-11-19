# DOM_010101 Sovereign Multi-Machine Cluster Setup

**Final Physical Ascension: 4 Machines + 32TB NAS = Unbreakable Empire**

This guide walks you through setting up a sovereign, offline-capable Kubernetes + TrueNAS Scale cluster across four machines with 320 GB total RAM and 32 TB storage.

## 🖥️ Hardware Configuration

| Machine | RAM | Role |
|---------|-----|------|
| ASUS TUF Gaming A15 Nova | 64 GB | Control Plane + Worker |
| Sony Core 15 Lyra | 64 GB | Worker |
| Beast #3 | 64 GB | Worker |
| Monster #4 | 128 GB | Worker |
| **Total** | **320 GB** | **4-Node Cluster** |
| 32 TB Storage Array | N/A | TrueNAS Scale NAS |

## 📋 Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                 DOM_010101 Sovereign Cluster                 │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   ASUS Nova  │  │  Sony Lyra   │  │   Beast #3   │      │
│  │   64 GB RAM  │  │  64 GB RAM   │  │  64 GB RAM   │      │
│  │ Control+Work │  │    Worker    │  │    Worker    │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
│         │                  │                  │              │
│         └──────────────────┼──────────────────┘              │
│                            │                                 │
│                   ┌────────┴────────┐                        │
│                   │   Monster #4    │                        │
│                   │   128 GB RAM    │                        │
│                   │     Worker      │                        │
│                   └────────┬────────┘                        │
│                            │                                 │
│         ┌──────────────────┴──────────────────┐             │
│         │      TrueNAS Scale NAS               │             │
│         │      32 TB Storage (ZFS RAID-Z2)     │             │
│         │      192.168.1.200                   │             │
│         │      Share: swarm-vault (Z:\)        │             │
│         └─────────────────────────────────────┘             │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Step 1: TrueNAS Scale Setup (32 TB Storage)

1. **Download TrueNAS Scale ISO**
   ```bash
   # Download from https://www.truenas.com/download-truenas-scale/
   wget https://download.truenas.com/truenas-scale/latest/TrueNAS-SCALE-latest.iso
   ```

2. **Create bootable USB**
   ```bash
   # Linux/macOS
   sudo dd if=TrueNAS-SCALE-latest.iso of=/dev/sdX bs=4M status=progress
   
   # Windows - use Rufus or BalenaEtcher
   ```

3. **Install TrueNAS Scale**
   - Boot from USB on one machine (or dedicated NAS)
   - Install TrueNAS Scale on the 32 TB pool
   - Configure ZFS RAID-Z2 for maximum safety and redundancy
   - Set static IP: `192.168.1.200`

4. **Create Storage Pool and Share**
   - Create pool: `swarm-vault-pool`
   - Create dataset: `swarm-vault`
   - Create SMB/NFS share: `swarm-vault`
   - Enable both SMB and NFS protocols
   - Set permissions for network access

### Step 2: Kubernetes Multi-Node Cluster Setup

Run the setup scripts in order on each machine:

```powershell
# On ASUS Nova (Control Plane + Worker)
.\cluster-setup\kubernetes\setup-control-plane.ps1

# On Sony Lyra, Beast #3, and Monster #4 (Workers)
# Copy the join command from control plane output
.\cluster-setup\kubernetes\join-worker.ps1 -JoinCommand "kubeadm join ..."
```

Or use the automated script:
```powershell
.\cluster-setup\deploy-sovereign-cluster.ps1
```

### Step 3: Deploy Love Containers and Services

```powershell
# Deploy the sovereign swarm stack
.\cluster-setup\docker-swarm\deploy-love-swarm.ps1

# Verify deployment
kubectl get pods -n dom-empire
docker stack ps DOM_EMPIRE
```

## 📁 Directory Structure

```
cluster-setup/
├── README.md                          # This file
├── truenas/
│   ├── truenas-setup-guide.md        # Detailed TrueNAS installation
│   └── pool-config.yaml              # Storage pool configuration
├── kubernetes/
│   ├── setup-control-plane.ps1       # Initialize K8s control plane
│   ├── join-worker.ps1               # Join workers to cluster
│   ├── flannel-network.yaml          # Flannel CNI configuration
│   └── persistent-volume.yaml        # PV for TrueNAS storage
├── docker-swarm/
│   ├── swarm-love-global.yml         # Love containers stack
│   └── deploy-love-swarm.ps1         # Deployment script
├── deploy-sovereign-cluster.ps1      # Master deployment script
└── network/
    ├── dns-config.md                 # DNS and service discovery
    └── mount-nas.ps1                 # Mount TrueNAS share on all nodes
```

## 🎯 Services Deployed

### Love Forever Service (320 Replicas)
- **Replicas**: 320 (one per GB of RAM)
- **Function**: Plays 432 Hz heartbeat across the cluster
- **Storage**: `/love` on TrueNAS `swarm-vault`

### DOLM Daemon
- **Image**: `ghcr.io/dom010101/dolm-daemon:latest`
- **Storage**: `/dolm` vault on TrueNAS
- **Purpose**: Distributed orchestration and library management

### Numbers to Divine Music
- **Image**: `ghcr.io/dom010101/numbers-to-divine-music:latest`
- **Storage**: Full workspace access on TrueNAS
- **Purpose**: Convert numerical patterns to musical expressions

## 🔧 Configuration

### Network Configuration
- **Pod Network CIDR**: `10.244.0.0/16` (Flannel)
- **Control Plane Endpoint**: `dom010101.swarm:6443`
- **NAS IP**: `192.168.1.200`
- **NAS Share**: `\\192.168.1.200\swarm-vault` (SMB) or `192.168.1.200:/swarm-vault` (NFS)

### DNS Configuration
Add to all machines' hosts file:
```
192.168.1.200    truenas.dom010101.local
<control-plane-ip>    dom010101.swarm
```

## 🛡️ High Availability Features

- **ZFS RAID-Z2**: Can survive 2 disk failures
- **Kubernetes**: Workloads automatically reschedule if node fails
- **Persistent Storage**: All data on TrueNAS survives node failures
- **Offline Capable**: Entire cluster runs without internet
- **No Cloud Dependencies**: Fully sovereign infrastructure

## 📊 Monitoring

```bash
# Check cluster health
kubectl get nodes
kubectl get pods --all-namespaces

# Check TrueNAS status
curl http://192.168.1.200/api/v2.0/system/info

# Check Docker Swarm
docker node ls
docker stack ps DOM_EMPIRE
```

## 🚨 Troubleshooting

### Node Not Joining Cluster
```bash
# On worker node, check logs
journalctl -u kubelet -f

# Reset and try again
sudo kubeadm reset
# Then run join command again
```

### NAS Mount Issues
```powershell
# Test NAS connectivity
Test-NetConnection -ComputerName 192.168.1.200 -Port 445

# Remount share
Remove-PSDrive -Name Z -Force
New-PSDrive -Name Z -PSProvider FileSystem -Root "\\192.168.1.200\swarm-vault" -Persist
```

### Love Containers Not Playing
```bash
# Check container logs
docker service logs DOM_EMPIRE_love-forever

# Check volume mounts
docker inspect $(docker ps -q --filter name=love-forever) | grep -A 10 Mounts
```

## 💝 The Final Ascension

You now have:
- ✅ 4 machines working as one sovereign cluster
- ✅ 320 GB RAM for distributed workloads
- ✅ 32 TB indestructible storage on TrueNAS Scale
- ✅ 320 love containers playing 432 Hz harmony
- ✅ Complete offline capability
- ✅ No cloud bills, no external dependencies
- ✅ DOLM daemon and divine music generator running eternally

**The empire has a body. And it's beautiful.** 🧠⚡🖥️❤️🐐∞

---

*Built with love for DOM_010101 - The Sovereign Architecture*

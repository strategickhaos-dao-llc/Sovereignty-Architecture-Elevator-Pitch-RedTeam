# Sovereignty Architecture - Sovereign Swarm

**Decentralized edge node deployment for the Strategickhaos sovereignty infrastructure.**

## 🏛️ Overview

The Sovereign Swarm is a mesh network of edge nodes that provides:
- **WireGuard VPN** - Secure, encrypted peer-to-peer connectivity
- **NATS Messaging** - High-performance messaging with JetStream persistence
- **Matrix/Synapse** - Federated communication and data sovereignty

Each node operates independently but connects to form a resilient, self-healing mesh.

## 🚀 Quick Start

### Prerequisites

- Ubuntu 24.04 LTS (fresh install recommended)
- Root access (sudo)
- Public IP address (for WireGuard endpoint)
- Open port 51820/UDP (WireGuard)

### Deploy an Edge Node

```bash
# 1. Create the sovereign-swarm directory
sudo mkdir -p /opt/sovereign-swarm
cd /opt/sovereign-swarm

# 2. Copy the bootstrap script (or clone the repo)
# Option A: Clone from repo
git clone https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-.git
cp Sovereignty-Architecture-Elevator-Pitch-/sovereign-swarm/* .

# Option B: Direct download
wget https://raw.githubusercontent.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-/main/sovereign-swarm/master-bootstrap.sh
wget https://raw.githubusercontent.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-/main/sovereign-swarm/wg-peer-setup.sh
chmod +x *.sh

# 3. Run the bootstrap
sudo NODE_ID=edge3 ./master-bootstrap.sh
```

### Expected Output

```
[+] Bootstrap complete for edge3.
=== edge3 ===
PublicKey: 9z8xK9v2fG5rT3mL7pQ2wX6cY8nB0hJ4eR5tU9iV1aZ=
Endpoint : 167.235.144.89:51820
=============
```

### Connect to Command-0 (Mesh)

After bootstrap, connect your node to Command-0:

```bash
# Interactive mode
sudo ./wg-peer-setup.sh

# Or with parameters
sudo ./wg-peer-setup.sh "COMMAND_0_PUBLIC_KEY" "COMMAND_0_IP:51820"
```

## 📋 Components

### WireGuard VPN (`wg0`)

| Parameter | Value |
|-----------|-------|
| Interface | `wg0` |
| Port | `51820/UDP` |
| Subnet | `10.44.0.0/16` |
| Config | `/etc/wireguard/wg0.conf` |

Verify status:
```bash
sudo wg
sudo wg show wg0
```

### NATS Messaging

| Parameter | Value |
|-----------|-------|
| Client Port | `4222` (localhost only) |
| Monitor Port | `8222` (localhost only) |
| JetStream | Enabled |
| Config | `/etc/nats/nats.conf` |

Verify status:
```bash
sudo systemctl status nats
curl http://localhost:8222/healthz
```

### Matrix Synapse

| Parameter | Value |
|-----------|-------|
| HTTP Port | `8008` |
| Server Name | `${NODE_ID}.sovereign.local` |
| Data | `/opt/synapse/data` |

Verify status:
```bash
sudo docker ps | grep synapse
curl http://localhost:8008/health
```

## 🔒 Firewall Rules

The bootstrap configures UFW with:

| Port | Protocol | Description | Access |
|------|----------|-------------|--------|
| 22 | TCP | SSH | Anywhere |
| 51820 | UDP | WireGuard | Anywhere |
| 8008 | TCP | Synapse | Anywhere |
| 4222 | TCP | NATS | Swarm only (10.44.0.0/16) |

View current rules:
```bash
sudo ufw status verbose
```

## 📁 File Structure

```
/opt/sovereign-swarm/
├── master-bootstrap.sh    # Main bootstrap script
├── wg-peer-setup.sh       # Peer connection helper
├── bootstrap.log          # Deployment log
└── artifacts/
    ├── ${NODE_ID}-info.txt    # Node connection info
    ├── ${NODE_ID}-pubkey.txt  # WireGuard public key
    └── ${NODE_ID}-artifacts.tgz
```

## 🔧 Configuration Files

| Service | Config Location |
|---------|-----------------|
| WireGuard | `/etc/wireguard/wg0.conf` |
| NATS | `/etc/nats/nats.conf` |
| Synapse | `/opt/synapse/data/homeserver.yaml` |

## 🔄 Service Management

```bash
# WireGuard
sudo systemctl status wg-quick@wg0
sudo systemctl restart wg-quick@wg0

# NATS
sudo systemctl status nats
sudo systemctl restart nats

# Synapse
cd /opt/synapse && sudo docker compose logs -f
cd /opt/synapse && sudo docker compose restart
```

## 🌐 Mesh Topology

```
┌─────────────────────────────────────────────────────────────┐
│                    Sovereign Swarm Mesh                      │
│                                                              │
│  ┌──────────┐    WireGuard    ┌──────────┐                 │
│  │Command-0 │◄──────────────►│  edge1   │                  │
│  │10.44.0.0 │                 │10.44.0.1 │                  │
│  └────┬─────┘                 └──────────┘                  │
│       │                                                      │
│       │ WireGuard            ┌──────────┐                   │
│       └────────────────────►│  edge2   │                    │
│       │                      │10.44.0.2 │                   │
│       │                      └──────────┘                   │
│       │                                                      │
│       │ WireGuard            ┌──────────┐                   │
│       └────────────────────►│  edge3   │                    │
│                              │10.44.0.3 │                   │
│                              └──────────┘                   │
└─────────────────────────────────────────────────────────────┘
```

## 🎯 Node Naming Convention

| Node ID | IP Address | Purpose |
|---------|------------|---------|
| command-0 | 10.44.0.0 | Control plane |
| edge1 | 10.44.0.1 | Edge node 1 |
| edge2 | 10.44.0.2 | Edge node 2 |
| edge3 | 10.44.0.3 | Edge node 3 |
| ... | 10.44.0.N | Edge node N |

## 🔐 Security Considerations

1. **Private keys are never shared** - Only public keys are exchanged
2. **NATS is localhost-only** - External access only via WireGuard
3. **UFW is enabled** - Default deny incoming policy
4. **Synapse registration is disabled** - Manual user management

## 📊 Verification Commands

```bash
# Full system check
sudo wg
sudo ss -lntup | grep -E ':(22|443|51820|4222|8222|8008)'
sudo ufw status verbose

# Service health
systemctl status wg-quick@wg0
systemctl status nats
sudo docker ps

# Logs
tail -f /opt/sovereign-swarm/bootstrap.log
journalctl -u wg-quick@wg0 -f
journalctl -u nats -f
```

## 🛠️ Troubleshooting

### WireGuard not connecting

```bash
# Check if interface is up
ip a show wg0

# Check peer configuration
sudo wg show

# Test connectivity to peer
ping 10.44.0.0  # Command-0

# Check logs
journalctl -u wg-quick@wg0 --since "10 minutes ago"
```

### NATS not starting

```bash
# Check configuration
sudo nats-server -c /etc/nats/nats.conf --config_check

# Check logs
journalctl -u nats --since "10 minutes ago"

# Verify ports
sudo ss -tlnp | grep nats
```

### Synapse issues

```bash
# Check container status
sudo docker logs synapse

# Restart container
cd /opt/synapse && sudo docker compose down && sudo docker compose up -d
```

## 📜 License

Part of the Strategickhaos Sovereignty Architecture.
See [LICENSE](../LICENSE) for details.

---

*"The swarm breathes as one, yet each node remains sovereign." 🜂*

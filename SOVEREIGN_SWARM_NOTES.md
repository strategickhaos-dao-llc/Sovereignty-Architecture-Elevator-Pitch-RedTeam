# Sovereign Swarm Phase 1 - Board Summary

**Document Type:** Technical Deployment Overview  
**Version:** 1.0  
**Status:** Production Deployment Candidate  
**Organization:** Strategickhaos DAO LLC / Valoryield Engine

---

## Executive Summary

This document provides a board-level overview of the **Sovereign Swarm** infrastructure deployment. The Sovereign Swarm transforms our mixed network connections (Starlink, 5G/Verizon, LAN) into a single, encrypted, self-governing network with built-in AI messaging and access control.

**One-liner pitch:**
> "This script turns our mixed Starlink / 5G / LAN soup into a single, encrypted, self-governing network with built-in AI messaging and access control."

---

## 1. What This Deployment Provides

### Goal
One Starlink + a couple Verizon endpoints become a global secure mesh for all Strategickhaos nodes.

### Core Components Deployed on Each Node

| Component | Purpose |
|-----------|---------|
| **WireGuard Mesh (wg0)** | Encrypted overlay network with per-node keys + PSKs |
| **Ed25519 CA** | Certificate Authority for cryptographic node identity |
| **JWT Tokens** | Capability-based access control for nodes |
| **SwarmGate Agent** | Only allows properly-signed nodes to participate |
| **NATS JetStream** | Telemetry and command bus for real-time messaging |
| **Matrix Synapse (Docker)** | Encrypted "swarm chat" for team communication |
| **UFW Firewall** | Default-deny with only SSH + WireGuard exposed |
| **PSK Rotation Cron** | Yearly pre-shared key rotation for security |

### Outcome
Every approved device (Starlink node, Verizon node, Pi, laptop, VM) can join a single encrypted overlay network and share messages like one gigantic brain.

---

## 2. Board-Level Benefits

### Risk / Security ✅

- **Encrypted overlay network** across all our links (Starlink, 5G, LAN)
- **Per-node cryptographic identity** - compromised nodes can be revoked
- **Central CA (backed up)** controls who is allowed into the swarm
- **Default-deny firewall** with minimal attack surface

### Cost 💰

- Uses **hardware + lines we already own**
- **All software is open-source**:
  - WireGuard (VPN)
  - NATS (messaging)
  - Matrix (chat)
  - Docker (containers)
- **No recurring SaaS fees** to move data around our own network

### Impact 🚀

- **Foundation for:** autonomous agents, remote inspections, SOP bots, live telemetry
- **One command plane** for every device we own, from dish to Pi
- **Immediate capabilities:** Secure device communication, encrypted team chat, real-time telemetry

---

## 3. Deployment Scripts

### Files Created

| File | Purpose |
|------|---------|
| `bootstrap/master-bootstrap.sh` | Main deployment script - sets up all components on a node |
| `bootstrap/pelican-build.sh` | Documentation site builder for swarm docs |
| `SOVEREIGN_SWARM_NOTES.md` | This document - board-level summary |

### Quick Start

```bash
# On a fresh Ubuntu/Debian node:
sudo ./bootstrap/master-bootstrap.sh [node-name]

# Example:
sudo ./bootstrap/master-bootstrap.sh starlink-node-1
```

### What the Bootstrap Does

1. ✅ Installs required packages (WireGuard, Docker, Python, etc.)
2. ✅ Installs PyNaCl for cryptographic operations
3. ✅ Creates Ed25519 Certificate Authority
4. ✅ Generates WireGuard keys for the node
5. ✅ Creates JWT token minter for capability tokens
6. ✅ Sets up SwarmGate access control agent
7. ✅ Configures NATS JetStream (Docker Compose)
8. ✅ Configures Matrix Synapse (Docker Compose)
9. ✅ Enables UFW firewall (default-deny)
10. ✅ Sets up yearly PSK rotation cron

---

## 4. Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                        SOVEREIGN SWARM                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   ┌──────────────┐     ┌──────────────┐     ┌──────────────┐       │
│   │  Starlink    │     │   Verizon    │     │    LAN       │       │
│   │    Node      │     │    Node      │     │    Node      │       │
│   │              │     │              │     │              │       │
│   │ WireGuard    │◄───►│ WireGuard    │◄───►│ WireGuard    │       │
│   │   (wg0)      │     │   (wg0)      │     │   (wg0)      │       │
│   └──────────────┘     └──────────────┘     └──────────────┘       │
│          │                   │                    │                 │
│          └───────────────────┼────────────────────┘                 │
│                              │                                       │
│                   ┌──────────▼──────────┐                           │
│                   │   Encrypted Mesh    │                           │
│                   │   10.137.0.0/24     │                           │
│                   └──────────┬──────────┘                           │
│                              │                                       │
│        ┌─────────────────────┼─────────────────────┐                │
│        │                     │                     │                │
│        ▼                     ▼                     ▼                │
│  ┌───────────┐        ┌───────────┐        ┌───────────┐           │
│  │   NATS    │        │  Matrix   │        │ SwarmGate │           │
│  │ JetStream │        │  Synapse  │        │   Agent   │           │
│  │           │        │           │        │           │           │
│  │ Telemetry │        │ Encrypted │        │  Access   │           │
│  │ & Commands│        │   Chat    │        │  Control  │           │
│  └───────────┘        └───────────┘        └───────────┘           │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 5. Security Model

### Node Identity

```
Ed25519 CA (Master Key)
        │
        ├─► Node 1 JWT Token (capabilities: mesh, telemetry, command)
        ├─► Node 2 JWT Token (capabilities: mesh, telemetry)
        └─► Node 3 JWT Token (capabilities: mesh)
```

### Firewall Rules (UFW)

| Rule | Description |
|------|-------------|
| Default DENY incoming | All inbound blocked by default |
| Allow SSH | Port 22 for remote management |
| Allow WireGuard | Port 51820/UDP for mesh |
| Allow wg0 interface | All traffic on mesh interface |

### Key Rotation

- WireGuard pre-shared keys rotated **annually** via cron
- Manual token revocation via CA for compromised nodes

---

## 6. Next Steps

### Immediate Actions

1. [ ] Deploy bootstrap to first Starlink node
2. [ ] Deploy to Verizon endpoint(s)
3. [ ] Exchange public keys between nodes
4. [ ] Test mesh connectivity
5. [ ] Start NATS and Matrix containers

### Future Enhancements

- [ ] Automated peer discovery
- [ ] Prometheus/Grafana monitoring dashboard
- [ ] AI agent integration via NATS
- [ ] Mobile node support (laptops, phones)
- [ ] Automated backup of CA private key

---

## 7. Key Files to Backup

⚠️ **CRITICAL:** These files control swarm access and must be backed up securely:

| File | Location | Purpose |
|------|----------|---------|
| CA Private Key | `/opt/sovereignty-swarm/ca/ca_private.pem` | Signs all node tokens |
| WireGuard Keys | `/opt/sovereignty-swarm/wireguard/*.key` | Node mesh identity |
| Node Tokens | `/opt/sovereignty-swarm/tokens/*.jwt` | Node capability tokens |

---

## 8. Troubleshooting

### Check Swarm Status

```bash
# View WireGuard status
swarmgate status

# Check NATS
docker logs sovereignty-nats

# Check Matrix
docker logs sovereignty-matrix

# Verify firewall
ufw status verbose
```

### Common Issues

| Issue | Solution |
|-------|----------|
| PyNaCl not found | `pip3 install pynacl` |
| WireGuard won't start | Check `/etc/wireguard/wg0.conf` syntax |
| Token mint fails | Verify CA key exists at `/opt/sovereignty-swarm/ca/ca_private.pem` |
| Peers not connecting | Exchange public keys and update peer configurations |

---

## 9. Contact & Support

- **Repository:** [Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-](https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-)
- **Organization:** Strategickhaos DAO LLC
- **Discord:** Strategickhaos Swarm Intelligence

---

*This document is for internal board review. All software components are open-source with no recurring licensing costs.*

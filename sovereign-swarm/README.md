# 🛡️ Sovereign Swarm

Production-ready mesh network infrastructure for sovereign digital systems.

## What is Sovereign Swarm?

Sovereign Swarm is a complete deployment framework for creating secure, decentralized mesh networks using commodity hardware. It combines:

- **WireGuard** mesh VPN for encrypted peer-to-peer communication
- **Ed25519 cryptography** for identity and capability tokens
- **JWT-based capability system** for fine-grained access control
- **NATS** for distributed messaging
- **Syncthing** for secure file synchronization

## Quick Start

```bash
# On Command-0 (Primary Hub)
sudo make bootstrap-command0

# On Fixed-1 (Secondary Hub)
sudo make bootstrap-fixed1

# On Pelican nodes (Mobile/Field units)
sudo PELICAN_ID=pelican1 \
     COMMAND0_PUBKEY="<pubkey>" \
     COMMAND0_ENDPOINT="<ip>:51820" \
     make bootstrap-pelican
```

## Files

| File | Description |
|------|-------------|
| `master-bootstrap.sh` | Main deployment script for Command-0 and Fixed nodes |
| `pelican-build.sh` | Specialized script for Raspberry Pi field units |
| `Makefile` | Automation framework for common operations |
| `DEPLOYMENT.md` | Complete deployment guide |

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Sovereign Swarm                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   ┌───────────────┐          ┌───────────────┐              │
│   │  Command-0    │◄────────►│   Fixed-1     │              │
│   │  (CA + Hub)   │          │   (Backup)    │              │
│   │  10.44.0.1    │          │   10.44.0.2   │              │
│   └───────┬───────┘          └───────┬───────┘              │
│           │                          │                       │
│           └──────────┬───────────────┘                       │
│                      │                                       │
│   ┌──────────────────┼──────────────────┐                   │
│   │                  │                  │                   │
│   ▼                  ▼                  ▼                   │
│ ┌─────────┐    ┌─────────┐       ┌─────────┐               │
│ │Pelican-1│    │Pelican-2│  ...  │Pelican-N│               │
│ │10.44.0.11    │10.44.0.12       │10.44.0.xx               │
│ └─────────┘    └─────────┘       └─────────┘               │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Features

### Security
- ✅ Ed25519 key generation for CA and node identities
- ✅ JWT capability tokens with EdDSA signatures
- ✅ WireGuard encryption with pre-shared keys
- ✅ UFW firewall with mesh-only service binding
- ✅ SwarmGate token verification enforcement

### Networking
- ✅ Full mesh connectivity via WireGuard
- ✅ Automatic IP allocation per node type
- ✅ Persistent keepalive for NAT traversal
- ✅ Automatic reconnection via watchdog

### Operations
- ✅ One-command bootstrap for each node type
- ✅ Makefile automation for common tasks
- ✅ Systemd services with automatic restart
- ✅ Comprehensive logging

### Mobile/Field Nodes
- ✅ Raspberry Pi optimization
- ✅ Battery power management
- ✅ Connectivity watchdog
- ✅ Minimal resource usage

## Requirements

- Ubuntu 22.04 LTS / Debian 12 / Raspberry Pi OS
- WireGuard kernel module
- OpenSSL 1.1.1+
- Root access

## Documentation

See [DEPLOYMENT.md](DEPLOYMENT.md) for the complete deployment guide including:
- Step-by-step deployment instructions
- Troubleshooting guide
- Security considerations
- Cost analysis

## License

MIT License - See [LICENSE](../LICENSE) for details.

---

**Built by the Strategickhaos Swarm Intelligence collective**

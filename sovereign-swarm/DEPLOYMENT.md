# 🚀 Sovereign Swarm Deployment Guide

## Overview

The Sovereign Swarm is a production-ready mesh network infrastructure using:
- **WireGuard** for encrypted mesh networking
- **Ed25519** cryptography for identity and capability tokens
- **JWT** for capability-based access control
- **NATS** for distributed messaging
- **Syncthing** for secure file synchronization

## Architecture

```
                    ┌─────────────────┐
                    │   Command-0     │
                    │   (Primary Hub) │
                    │   10.44.0.1     │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
       ┌──────┴──────┐ ┌─────┴─────┐ ┌──────┴──────┐
       │   Fixed-1   │ │ Pelican-1 │ │ Pelican-2   │
       │  10.44.0.2  │ │ 10.44.0.11│ │ 10.44.0.12  │
       └─────────────┘ └───────────┘ └─────────────┘
```

## Prerequisites

### Hardware Requirements

| Node Type | Minimum | Recommended |
|-----------|---------|-------------|
| Command-0 | 2 cores, 4GB RAM | 4 cores, 8GB RAM |
| Fixed-1   | 2 cores, 2GB RAM | 4 cores, 4GB RAM |
| Pelican   | Raspberry Pi 4 2GB | Raspberry Pi 4 4GB |

### Software Requirements

- Ubuntu 22.04 LTS or Debian 12
- WireGuard kernel module
- OpenSSL 1.1.1+ (for Ed25519)
- Root access

## Quick Start

### Phase 1: Deploy Command-0

```bash
# Clone the repository
git clone https://github.com/Strategickhaos/sovereign-swarm.git
cd sovereign-swarm

# Bootstrap Command-0
sudo make bootstrap-command0

# Or manually:
# sudo NODE_ID=command0 ./master-bootstrap.sh deploy
```

After completion, note the output:
```
=== Command-0 details ===
PublicKey: <YOUR_WG_PUBKEY>
Endpoint : <YOUR_PUBLIC_IP>:51820
```

**⚠️ CRITICAL: Immediately backup CA keys:**
```bash
sudo make backup
# Or manually:
sudo tar -czf ~/swarm-ca-backup-$(date +%Y%m%d).tar.gz /opt/sovereign-swarm/ca/state/
```

### Phase 2: Deploy Fixed-1

```bash
# Copy repository to Fixed-1
scp -r sovereign-swarm user@fixed1-ip:~/
ssh user@fixed1-ip

# Bootstrap Fixed-1
cd sovereign-swarm
sudo make bootstrap-fixed1

# Update WireGuard config with Command-0 details
sudo nano /etc/wireguard/wg0.conf
# Replace REPLACE_COMMAND0_PUBKEY with the pubkey from Command-0
# Replace REPLACE_COMMAND0_ENDPOINT with the endpoint from Command-0

# Restart WireGuard
sudo systemctl restart wg-quick@wg0

# Verify connectivity
ping 10.44.0.1
```

### Phase 3: Add Fixed-1 to Command-0

On Command-0:
```bash
# Get Fixed-1's public key (from Fixed-1's output)
sudo wg set wg0 peer <FIXED1_PUBKEY> allowed-ips 10.44.0.2/32 endpoint <FIXED1_IP>:51820

# Verify bidirectional connectivity
ping 10.44.0.2
```

### Phase 4: Deploy Pelican Nodes

On each Pelican Pi:
```bash
# Copy repository
scp -r sovereign-swarm pi@pelican-ip:~/
ssh pi@pelican-ip

# Bootstrap Pelican
cd sovereign-swarm
sudo PELICAN_ID=pelican1 \
     COMMAND0_PUBKEY="<command0-pubkey>" \
     COMMAND0_ENDPOINT="<command0-ip>:51820" \
     make bootstrap-pelican
```

On Command-0, add the Pelican:
```bash
sudo wg set wg0 peer <PELICAN_PUBKEY> allowed-ips 10.44.0.11/32
```

## Deployment Checklist

### Command-0 Setup
- [ ] Run `sudo make bootstrap-command0`
- [ ] Record WireGuard public key
- [ ] Record public IP/endpoint
- [ ] Backup CA keys to secure location
- [ ] Verify NATS is running: `systemctl status nats-swarm`
- [ ] Verify SwarmGate is running: `systemctl status swarmgate`

### Fixed-1 Setup
- [ ] Run `sudo make bootstrap-fixed1`
- [ ] Update `/etc/wireguard/wg0.conf` with Command-0 details
- [ ] Restart WireGuard: `systemctl restart wg-quick@wg0`
- [ ] Test connectivity: `ping 10.44.0.1`
- [ ] Add Fixed-1 peer on Command-0

### Pelican Setup (per node)
- [ ] Flash Raspberry Pi OS Lite (64-bit)
- [ ] Enable SSH and configure networking
- [ ] Copy repository and run pelican-build.sh
- [ ] Add Pelican peer on Command-0
- [ ] Verify mesh connectivity

### Post-Deployment Verification
- [ ] All nodes can ping each other via mesh IPs
- [ ] NATS cluster is healthy: `nats server ping` (if nats CLI installed)
- [ ] SwarmGate is enforcing tokens
- [ ] Firewall is configured correctly: `ufw status`
- [ ] Syncthing devices are paired (for Pelicans)

## IP Address Allocation

| Node | Mesh IP |
|------|---------|
| Command-0 | 10.44.0.1 |
| Fixed-1 | 10.44.0.2 |
| Fixed-2 | 10.44.0.3 |
| Pelican-1 | 10.44.0.11 |
| Pelican-2 | 10.44.0.12 |
| Pelican-3 | 10.44.0.13 |
| Pelican-4 | 10.44.0.14 |
| Pelican-5 | 10.44.0.15 |

## Capability Tokens

Each node receives a JWT capability token with specific permissions:

| Node Type | Capabilities |
|-----------|--------------|
| Command-0 | `ca:sign`, `mesh:admin`, `nats:admin`, `matrix:admin`, `swarm:bootstrap` |
| Fixed-X | `mesh:peer`, `nats:publish`, `nats:subscribe`, `matrix:user` |
| Pelican-X | `mesh:peer`, `nats:subscribe`, `sync:read` |

Tokens are stored in `/opt/sovereign-swarm/tokens/<node-id>.jwt`

## Service Ports

| Service | Port | Binding |
|---------|------|---------|
| WireGuard | 51820/UDP | All interfaces |
| NATS | 4222/TCP | Mesh only (10.44.0.x) |
| NATS Cluster | 6222/TCP | Mesh only |
| Matrix | 8008/TCP | Mesh only |
| Syncthing | 22000/TCP | Mesh only |
| Syncthing GUI | 8384/TCP | Mesh only |

## Troubleshooting

### WireGuard Not Connecting

```bash
# Check WireGuard status
sudo wg show wg0

# Check for handshake
sudo wg show wg0 | grep "latest handshake"

# Check firewall
sudo ufw status

# Check if port is open
sudo ss -ulnp | grep 51820
```

### NATS Not Starting

```bash
# Check NATS logs
journalctl -u nats-swarm -f

# Verify configuration
cat /opt/sovereign-swarm/config/nats.conf

# Test NATS manually
/usr/local/bin/nats-server -c /opt/sovereign-swarm/config/nats.conf --debug
```

### Pelican Losing Connectivity

```bash
# Check watchdog status
systemctl status pelican-watchdog

# View watchdog logs
tail -f /var/log/sovereign-swarm/watchdog.log

# Manual connectivity test
ping -c 3 10.44.0.1
```

### Token Verification Failing

```bash
# Check SwarmGate logs
tail -f /var/log/sovereign-swarm/swarmgate.log

# Verify token manually
cat /opt/sovereign-swarm/tokens/<node-id>.jwt | cut -d'.' -f2 | base64 -d | jq
```

## Security Considerations

### CA Key Protection
- Store CA keys on encrypted storage
- Consider YubiHSM for hardware protection
- Never expose CA private key over network
- Rotate CA keys annually

### Network Security
- WireGuard provides authenticated encryption
- Pre-shared keys add quantum resistance
- UFW firewall blocks all non-mesh traffic
- Services bind only to mesh interface

### Token Security
- Tokens expire after 1 year by default
- Use shorter expiry for mobile nodes
- Revoke compromised tokens immediately
- Re-issue tokens if CA is compromised

## Maintenance

### Daily Operations
```bash
# Check system status
make status

# View recent logs
make logs

# Verify mesh connectivity
make verify-mesh
```

### Weekly Operations
```bash
# Full system verification
make verify

# Create fresh backup
make backup
```

### Monthly Operations
- Review and rotate pre-shared keys
- Check disk space on all nodes
- Review security logs
- Update system packages

## Cost Analysis

| Component | Monthly Cost |
|-----------|-------------|
| Command-0 (existing server) | $0 |
| Fixed-1 (existing server) | $0 |
| Pelican Pi 4 (4GB) x3 | ~$225 one-time |
| Starlink connectivity | ~$120/month |
| Power (Pelicans) | ~$5/month |
| **Total Ongoing** | **~$125/month** |

Compared to cloud alternatives:
- AWS VPN + EC2: ~$500/month
- **Savings: 75-80%**

## Next Steps

1. **Deploy Matrix Synapse** for secure communications
2. **Set up Syncthing** for vault synchronization
3. **Configure monitoring** with Prometheus/Grafana
4. **Implement backup automation** for vault data
5. **Add additional Pelicans** for geographic coverage

---

**Built by the Strategickhaos Swarm Intelligence collective**

*"Sovereign infrastructure, deployed in hours, not months."*

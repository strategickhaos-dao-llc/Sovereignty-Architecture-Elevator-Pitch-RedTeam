# Sovereign Swarm Deployment Guide

## Prerequisites

- **Operating System**: Ubuntu 22.04 LTS or Ubuntu 24.04 LTS
- **Access**: Root privileges (sudo)
- **Network**: Public IP address or Dynamic DNS hostname
- **Hardware**: Minimum 2 vCPU, 4GB RAM, 20GB SSD

## Quick Start

### Option 1: Fresh Installation (Recommended)

```bash
# Download and execute bootstrap script
curl -fsSL https://raw.githubusercontent.com/strategickhaos/sovereign-swarm/main/master-bootstrap.sh -o /tmp/ss.sh
sudo bash /tmp/ss.sh
```

### Option 2: Add Edge Node to Existing Swarm

```bash
sudo NODE_ID=edge3 /opt/sovereign-swarm/master-bootstrap.sh
```

## Deployment Steps

### 1. Network Configuration

Ensure the following ports are open:

| Port  | Protocol | Service      | Description                 |
|-------|----------|--------------|------------------------------|
| 51820 | UDP      | WireGuard    | VPN mesh traffic            |
| 4222  | TCP      | NATS         | Message bus                 |
| 8008  | TCP      | Matrix       | Synapse federation          |
| 443   | TCP      | HTTPS        | API endpoints               |

### 2. DNS Configuration

Configure A/AAAA records for your domain:

```
swarm.yourdomain.com      A     <public-ip>
matrix.yourdomain.com     A     <public-ip>
nats.yourdomain.com       A     <public-ip>
```

### 3. TLS Certificates

The bootstrap script automatically provisions Let's Encrypt certificates. Ensure:

- Port 80 is open for ACME challenge
- Domain resolves correctly before running bootstrap

### 4. Post-Deployment Verification

```bash
# Verify WireGuard tunnel
wg show

# Test NATS connectivity
nats bench test --msgs 1000 --size 128

# Check Matrix health
curl http://localhost:8008/health
```

## Environment Variables

| Variable     | Default          | Description                    |
|--------------|------------------|--------------------------------|
| NODE_ID      | `command0`       | Unique node identifier         |
| SWARM_DOMAIN | `localhost`      | Primary swarm domain           |
| WG_PORT      | `51820`          | WireGuard listen port          |
| NATS_PORT    | `4222`           | NATS listen port               |
| MATRIX_PORT  | `8008`           | Matrix Synapse port            |

## Air-Gapped Deployment

For fully air-gapped deployments:

1. Pre-download all dependencies on an internet-connected machine
2. Transfer to air-gapped environment via secure media
3. Run bootstrap with `--offline` flag

```bash
sudo bash /tmp/ss.sh --offline
```

## Backup & Recovery

### Backup Critical Data

```bash
# Backup CA state
tar -czf /backup/ca-state.tar.gz /opt/sovereign-swarm/ca/state/

# Backup node configurations
tar -czf /backup/nodes.tar.gz /opt/sovereign-swarm/nodes/

# Backup WireGuard keys
tar -czf /backup/wg-keys.tar.gz /etc/wireguard/
```

### Recovery Procedure

1. Restore CA state first
2. Regenerate node certificates if needed
3. Restore WireGuard configuration
4. Restart all services

## Upgrading

```bash
# Pull latest bootstrap script
curl -fsSL https://raw.githubusercontent.com/strategickhaos/sovereign-swarm/main/master-bootstrap.sh -o /tmp/ss.sh

# Run upgrade
sudo bash /tmp/ss.sh --upgrade
```

## Troubleshooting

See [README.md](../README.md#troubleshooting) for common issues and solutions.

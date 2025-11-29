# Sovereign Swarm Operations

## Overview

This directory contains operational documentation for the Sovereign Swarm system, a production-ready mesh network with SwarmGate v1.0 authentication at the WireGuard handshake layer.

## Quick Reference

### Primary Rendezvous
- **Starlink Mini**: dish 3476D3
- **Network**: 10.44.0.0/16
- **SwarmGate Version**: v1.0

### Key Files

| File | Description |
|------|-------------|
| [costs.md](costs.md) | Monthly and one-time cost estimates |
| [inventory.md](inventory.md) | Hardware and network inventory |

## Deployment Phases

### Phase 0: Key Ceremony
Generate CA keys and node credentials:
```bash
cd strategickhaos/ca
make init
make node ID=command-0
make token ID=command-0 CAP="nats.pub:telemetry.>,nats.sub:cmd.>,matrix.role:admin,router:true,net:10.44.0.0/16"
```

### Phase 1: WireGuard Mesh
Bootstrap first node:
```bash
cd strategickhaos
./scripts/bootstrap-node.sh command-0
```

### Phase 2: NATS Leaf Mesh
Start NATS on core nodes:
```bash
systemctl enable --now nats
./nats/systemd/seed.sh
```

### Phase 3: Matrix Synapse
Deploy on Fixed-1:
```bash
cd strategickhaos/matrix
docker compose up -d
```

### Phase 4: Syncthing
Enable on all nodes with Obsidian vaults:
```bash
systemctl enable --now syncthing
```

### Phase 5: Pelican Images
Build edge node images:
```bash
cd strategickhaos/pelican/image
sudo ./build.sh
```

## Maintenance

### PSK Rotation (Weekly)
```bash
./scripts/rotate-psk.sh
```

### Token Renewal (Before Expiry)
```bash
make -C ca token ID=<node-id> CAP="<capabilities>" TTL=7d
```

### Adding New Nodes
```bash
# Generate credentials
make -C ca node ID=edge-N

# Generate token
make -C ca token ID=edge-N CAP="nats.sub:cmd.>,net:10.44.10.0/24"

# Bootstrap
./scripts/join-sovereign-swarm.sh edge-N /path/to/token.jwt
```

## Troubleshooting

### WireGuard Connection Issues
```bash
wg show wg0
journalctl -u swarmsgd -f
```

### NATS Cluster Status
```bash
nats server list
nats stream ls
```

### Matrix Federation
```bash
docker logs synapse
curl http://localhost:8008/_matrix/federation/v1/version
```

## Security

- All inter-node traffic encrypted via WireGuard
- SwarmGate JWT tokens required for handshake
- NATS subjects gated by token capabilities
- Matrix SSO via SwarmGate tokens
- PSKs rotated weekly

## Support

- GitHub Issues: [Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-](https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-)
- Matrix: #swarm:swarm.local (internal)

# Sovereign Swarm Runbook

This directory contains the complete deployment runbook for the Sovereign Swarm infrastructure.

## Quick Start

```bash
# 1. Bootstrap Command-0
./phase0-bootstrap.sh

# 2. Generate keys
./phase1-key-ceremony.sh

# 3. Configure WireGuard mesh
./phase2-wireguard-mesh.sh

# 4. Build edge nodes
./pelican-build.sh

# 5. Apply security hardening
./security-harden.sh
```

## Directory Structure

```
swarm-runbook/
├── phase0-bootstrap.sh       # Phase 0: Install deps, create structure
├── phase1-key-ceremony.sh    # Phase 1: Generate WireGuard keys
├── phase2-wireguard-mesh.sh  # Phase 2: Configure WireGuard mesh
├── pelican-build.sh          # Phase 3: Build edge node images
├── security-harden.sh        # Phase 5: Apply security hardening
├── psk-rotate.sh             # Yearly PSK rotation script
├── configs/
│   ├── 99-sovereign-swarm.conf    # Kernel security parameters
│   ├── nats-leaf.conf             # NATS configuration
│   └── synapse-homeserver.yaml    # Synapse configuration
├── services/
│   ├── nats.service               # NATS systemd unit
│   └── synapse.service            # Synapse systemd unit
└── keys/                          # Generated keys (gitignored)
```

## Documentation

For complete documentation, see: [SOVEREIGN_SWARM_DEPLOYMENT.md](../../SOVEREIGN_SWARM_DEPLOYMENT.md)

## Security

- Private keys are never committed to git (see `.gitignore`)
- All services bind only to WireGuard interface (10.13.33.x)
- PSK rotation is automated via cron
- fail2ban protects against brute-force attacks

## License

MIT License - see [LICENSE](../../LICENSE)

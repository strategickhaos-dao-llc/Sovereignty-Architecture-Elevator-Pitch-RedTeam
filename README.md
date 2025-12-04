# Sovereign Swarm — Zero-Trust AI Orchestration Mesh

Fully air-gapped, sub-$100/mo, satellite + cellular resilient swarm for the Legion of Minds.

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          SOVEREIGN SWARM MESH                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│     ┌─────────────┐        WireGuard VPN        ┌─────────────┐            │
│     │  Command0   │◄═══════════════════════════►│    Edge1    │            │
│     │   (Hub)     │         mTLS + PSK          │   (Node)    │            │
│     └──────┬──────┘                             └──────┬──────┘            │
│            │                                           │                    │
│            │    ┌──────────────────────────┐           │                    │
│            └───►│         Edge2            │◄──────────┘                    │
│                 │        (Node)            │                                │
│                 └──────────────────────────┘                                │
│                                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                            CORE SERVICES                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌───────────────┐    ┌───────────────┐    ┌───────────────┐              │
│   │     NATS      │    │    Matrix     │    │      CA       │              │
│   │   Message     │    │   Synapse     │    │    (PKI)      │              │
│   │     Bus       │    │  Federation   │    │   Internal    │              │
│   │  Port 4222    │    │  Port 8008    │    │   Zero-Trust  │              │
│   └───────────────┘    └───────────────┘    └───────────────┘              │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Prerequisites

- **Operating System**: Ubuntu 22.04 LTS or Ubuntu 24.04 LTS
- **Access**: Root privileges (sudo)
- **Network**: Public IP address or Dynamic DNS hostname
- **Hardware**: Minimum 2 vCPU, 4GB RAM, 20GB SSD

## Quick Start

```bash
# Download bootstrap script
curl -fsSL https://raw.githubusercontent.com/strategickhaos/sovereign-swarm/main/master-bootstrap.sh -o /tmp/ss.sh

# Run bootstrap (installs as command0 hub node)
sudo bash /tmp/ss.sh                     # runs as command0

# Add additional edge nodes
sudo NODE_ID=edge3 /opt/sovereign-swarm/master-bootstrap.sh
```

## Features

- **Zero-Trust Architecture**: mTLS everywhere, no implicit trust
- **Air-Gapped Ready**: Full functionality without internet connectivity
- **Low Cost**: Sub-$100/month infrastructure
- **Resilient**: Satellite + cellular failover capabilities
- **Decentralized**: No single point of failure

## Directory Structure

```
├── .github/workflows/ci.yml   # CI pipeline
├── ca/                        # Certificate Authority
│   ├── init_ca.sh             # Initialize root CA
│   └── issue_node.sh          # Issue node certificates
├── docs/                      # Documentation
│   ├── DEPLOYMENT.md          # Deployment guide
│   └── ARCHITECTURE.md        # Architecture details
├── matrix/                    # Matrix Synapse
│   └── homeserver.yaml.tmpl   # Configuration template
├── nats/                      # NATS message bus
│   └── nats-server.conf.tmpl  # Configuration template
├── nodes/                     # Node configurations
├── scripts/                   # Utility scripts
│   ├── mint_token.py          # JWT token generator
│   └── generate_docs.sh       # Documentation generator
├── tests/                     # Test scripts
│   ├── shellcheck.sh          # Shell linting
│   └── python_syntax.sh       # Python syntax check
├── wireguard/                 # WireGuard VPN
│   └── templates/
│       └── wg0.conf.tmpl      # Configuration template
└── master-bootstrap.sh        # Main bootstrap script
```

## Troubleshooting

### WireGuard Status

```bash
wg show
```

Expected output shows interface, peers, and transfer stats.

### NATS Connectivity

```bash
nats bench test --msgs 1000 --size 128
```

Verifies message throughput and latency.

### Matrix Health

```bash
curl http://localhost:8008/health
```

Returns `OK` if Synapse is running.

### Common Issues

| Issue | Solution |
|-------|----------|
| WireGuard not starting | Check firewall: `ufw allow 51820/udp` |
| NATS connection refused | Verify service: `systemctl status sovereign-nats` |
| Matrix federation failed | Check TLS certificates and DNS |

## Security

- All private keys are generated locally and never transmitted
- Certificates are signed by an internal CA
- WireGuard uses pre-shared keys for additional security
- No secrets are committed to the repository

## Contributing

1. Fork the repository
2. Create a feature branch
3. Run tests: `./tests/shellcheck.sh && ./tests/python_syntax.sh`
4. Submit a pull request

## License

Apache-2.0 License - see [LICENSE](LICENSE) file for details.

---

**Built with 🜂 by the Legion of Minds**

*"The swarm is eternal."*
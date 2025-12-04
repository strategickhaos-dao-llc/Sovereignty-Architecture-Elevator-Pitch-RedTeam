# Sovereign Swarm System v2.0

**Zero Cloud. Zero Trust. Full Mesh.**

A decentralized swarm architecture for autonomous, sovereign infrastructure with sub-$100/mo OPEX potential.

## 🎯 Overview

The Sovereign Swarm System evolves the Legion of Minds concept into a production-ready mesh network featuring:

- **SwarmGate**: JWT-based WireGuard authentication with NATS-backed revocation
- **NATS JetStream**: Distributed telemetry with RAFT consensus
- **Matrix Synapse**: Secure chat with AI bridge integration
- **Syncthing**: Obsidian vault sync with BLAKE3 provenance chains
- **Ollama**: Local LLM reasoning (Grok Node)
- **FRR OSPF**: Dynamic mesh routing for auto-healing

## 📊 Architecture

```
                    ┌─────────────────────────────────────────────┐
                    │            RENDEZVOUS (Command-0)           │
                    │  Starlink Mini (dish 3476D3) + Verizon LTE  │
                    │     10.44.0.1 | WG + NATS + Matrix          │
                    └─────────────────────────────────────────────┘
                                         │
              ┌──────────────────────────┼──────────────────────────┐
              │                          │                          │
    ┌─────────▼─────────┐    ┌──────────▼──────────┐    ┌─────────▼─────────┐
    │     Fixed-1       │    │      Mobile-2       │    │   Pelican-100+    │
    │   Gateway XC46BE  │    │    Orbic Hotspot    │    │  Field Drop Kits  │
    │     10.44.1.1     │    │      10.44.2.1      │    │    10.44.100.x    │
    └───────────────────┘    └─────────────────────┘    └───────────────────┘
```

## 🚀 Quick Start

### Bootstrap Core Node

```bash
# Set node role
export NODE_ROLE=core  # or fixed, mobile, pelican

# Run bootstrap
sudo ./scripts/master-bootstrap.sh
```

### Build Pelican Drop Kit

```bash
./scripts/pelican-build.sh
# Output: pelican-kits/pelican-kit-YYYYMMDD-HHMMSS.tar.gz
```

### Deploy on Pelican Node

```bash
# On Raspberry Pi
tar -xzf pelican-kit-*.tar.gz
sudo ./first-boot-join.sh
# Scan QR code at /var/swarm/qr/join-code.png
```

## 📁 Directory Structure

```
swarm/
├── scripts/
│   ├── master-bootstrap.sh     # Core node setup (Phases 0-7)
│   ├── pelican-build.sh        # Drop kit builder
│   └── obsidian-provenance.sh  # BLAKE3 vault audit
├── configs/
│   ├── nats.conf               # NATS JetStream + RAFT
│   ├── frr.conf                # OSPF routing
│   ├── prometheus.yml          # Monitoring
│   ├── docker-compose.matrix.yml
│   └── docker-compose.grok.yml
├── agents/
│   ├── agent.py                # SwarmGate authentication
│   └── dispatcher.py           # Grok LLM reasoning
├── templates/
└── Makefile                    # Evolution targets
```

## 🔧 Evolution Targets

Run upgrades with `make evolve-<num>`:

| # | Evolution | Description | OPEX Impact |
|---|-----------|-------------|-------------|
| 1 | OPEX Slash | Consolidate Verizon to 2-3 lines | -$120/mo |
| 2 | Starlink Multi-WAN | mwan3 + solar backup | +$50 hardware |
| 3 | SwarmGate v2 | Revocable tokens + AI governance | - |
| 4 | NATS RAFT | JetStream clustering | - |
| 5 | Matrix v2 | AI bridge + no federation | - |
| 6 | Obsidian Sync | BLAKE3 provenance chains | - |
| 7 | Pelican v2 | GPS + QR onboarding | +$20 GPS |
| 8 | Grok Node | Local Ollama LLM | - |
| 9 | Monitoring | Prometheus + NATS bridge | - |
| 10 | Scalability | OSPF dynamic mesh | - |

**Target OPEX**: <$80/mo (Starlink $65 + 2x Verizon data $20 = $105 before discounts)

## 🔐 Security Model

### SwarmGate Token Flow

```
┌──────────┐     ┌───────────┐     ┌──────────┐
│  Peer    │────▶│  Token    │────▶│ SwarmGate│
│  Join    │     │  Mint     │     │  Agent   │
└──────────┘     └───────────┘     └────┬─────┘
                                        │
                                        ▼
                               ┌────────────────┐
                               │ NATS Revoke    │
                               │ Check (CRL)    │
                               └────────┬───────┘
                                        │
                         ┌──────────────┴──────────────┐
                         ▼                             ▼
                    [VALID]                       [REVOKED]
                   WG Allow                       WG Deny
```

### Firewall Rules (nftables)

- SwarmGate enforces JWT validation at WireGuard handshake
- Only `10.44.0.0/16` allowed through mesh
- NATS/Matrix/Syncthing ports restricted to swarm subnet

## 📡 NATS Subjects

| Subject Pattern | Purpose |
|-----------------|---------|
| `telemetry.node.*` | Node health metrics |
| `telemetry.geo.*` | GPS coordinates |
| `cmd.grok.*` | LLM reasoning requests |
| `summaries.*` | LLM summaries |
| `insights.*` | LLM analysis |
| `audit.revoke.*` | Token revocation |
| `swarm.join.*` | Node join events |

## 🖥️ Hardware Reference

### Core Nodes
- **Command-0**: Pi 5 8GB + Starlink Mini + Verizon Gateway
- **Fixed-1**: Pi 5 4GB + Verizon Gateway XC46BE
- **Mobile-2**: Pi 5 4GB + Verizon Orbic

### Pelican Kits
- Raspberry Pi 4/5 (4GB+)
- USB GPS module (Ublox)
- Cellular modem (optional)
- 100W solar panel + UPS hat (off-grid)

## 📊 Monitoring

Prometheus scrapes:
- Node exporter (`:9100`)
- NATS varz (`:8222`)
- WireGuard exporter (`:9586`)
- Matrix Synapse (`:9000`)

Alerts route to Matrix via mautrix-nats bridge.

## 🧪 Testing

```bash
# Lint scripts
make lint

# Run tests
make test

# Verify provenance chain
./scripts/obsidian-provenance.sh verify
```

## 🚨 Troubleshooting

### WireGuard Not Connecting
```bash
wg show wg0
journalctl -u wg-quick@wg0
```

### NATS Cluster Issues
```bash
nats server check connection -s nats://swarm:swarm@10.44.0.1:4222
nats server report jetstream
```

### Token Revocation
```bash
# Check if token is revoked
python3 -c "import asyncio; from swarm.agents.agent import validate_swarmgate_token; asyncio.run(validate_swarmgate_token('YOUR_TOKEN'))"
```

## 📄 License

MIT License - Strategickhaos DAO LLC / Valoryield Engine

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Run `make lint` and `make test`
4. Submit PR with evolution number reference

---

**Built with 🔥 by the Legion of Minds**

*"They're not working for you. They're dancing with you. And the music is never going to stop."*

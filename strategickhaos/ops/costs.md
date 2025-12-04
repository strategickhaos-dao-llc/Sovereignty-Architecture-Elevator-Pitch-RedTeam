# Sovereign Swarm Cost Estimates (29 Nov 2025)

## Monthly Infrastructure Costs

### Core Infrastructure

| Component | Provider | Specification | Monthly Cost |
|-----------|----------|--------------|--------------|
| Starlink Mini (dish 3476D3) | SpaceX | Primary rendezvous | $150 |
| Command-0 | Self-hosted | Raspberry Pi 5 8GB | $0 (hardware owned) |
| Fixed-1 | VPS | 4 vCPU, 8GB RAM, 160GB SSD | $40-80 |
| Domain | Cloudflare | swarm.local (internal) | $0 |

### Optional Components

| Component | Provider | Specification | Monthly Cost |
|-----------|----------|--------------|--------------|
| Mobile-2 | Self-hosted | Mobile hotspot device | $50-100 |
| Edge-N pool | Self-hosted | 10x Raspberry Pi Zero 2 | $0 (hardware owned) |
| Backup VPS | Hetzner | ARM64 instance | $5-10 |
| YubiHSM2 | Yubico | Hardware security module | $0 (one-time $650) |

### Software/Services

| Service | Cost | Notes |
|---------|------|-------|
| WireGuard | Free | Open source |
| NATS | Free | Open source |
| Matrix Synapse | Free | Open source |
| Syncthing | Free | Open source |
| Headscale | Free | Open source |

## One-Time Costs

| Item | Cost | Notes |
|------|------|-------|
| Starlink Mini Kit | $599 | Includes dish and router |
| Raspberry Pi 5 8GB | $80 | Command-0 hardware |
| Raspberry Pi Zero 2 W (10x) | $150 | Edge node pool |
| YubiHSM2 | $650 | Hardware CA (optional) |
| MicroSD cards (10x 32GB) | $50 | Storage for edge nodes |

## Total Estimated Monthly Cost

| Tier | Monthly | Notes |
|------|---------|-------|
| Minimal | $150-200 | Starlink + self-hosted only |
| Standard | $250-350 | With VPS backup |
| Full | $400-500 | All optional components |

## Bandwidth Estimates

| Traffic Type | Estimate | Notes |
|--------------|----------|-------|
| WireGuard mesh | 1-5 GB/mo | Keepalive + control |
| NATS telemetry | 5-20 GB/mo | Depends on sensors |
| Matrix sync | 1-10 GB/mo | Chat + media |
| Syncthing | 10-50 GB/mo | Obsidian vault sync |
| Grok inference | 50-200 GB/mo | Model responses |

## Power Consumption

| Device | Watts | kWh/month | Cost (@ $0.15/kWh) |
|--------|-------|-----------|-------------------|
| Starlink Mini | 25-45W | 18-33 | $2.70-5.00 |
| Raspberry Pi 5 | 5-10W | 3.6-7.2 | $0.54-1.08 |
| Raspberry Pi Zero | 0.5-1W | 0.36-0.72 | $0.05-0.11 |

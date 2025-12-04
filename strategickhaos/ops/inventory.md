# Sovereign Swarm Inventory

## Network Addressing

| Node | IP Address | Role | Status |
|------|------------|------|--------|
| Command-0 | 10.44.0.1/16 | Primary command | Active |
| Fixed-1 | 10.44.1.1/16 | Fixed relay | Active |
| Mobile-2 | 10.44.2.1/16 | Mobile relay | Reserved |
| Edge pool | 10.44.10.0/24 | Edge nodes | Dynamic |

## Hardware Inventory

### Command-0 (Primary)
- **Device**: Raspberry Pi 5 8GB
- **Storage**: 256GB NVMe
- **Network**: Starlink Mini (dish 3476D3)
- **Location**: Mobile command post
- **Services**: SwarmGate, WireGuard, NATS leaf, Grok node

### Fixed-1 (Relay)
- **Device**: VPS (ARM64)
- **Storage**: 160GB SSD
- **Network**: Static IPv4
- **Location**: Data center
- **Services**: SwarmGate, WireGuard, NATS core, Matrix Synapse

### Mobile-2 (Reserved)
- **Device**: TBD
- **Storage**: TBD
- **Network**: LTE/5G hotspot
- **Location**: Field deployment
- **Services**: SwarmGate, WireGuard, NATS leaf

### Edge Pool (10.44.10.0/24)
- **Device**: Raspberry Pi Zero 2 W (x10)
- **Storage**: 32GB microSD each
- **Network**: WiFi mesh
- **Location**: Distributed sensors
- **Services**: SwarmGate, telemetry agents

## Key Management

| Key Type | Location | Rotation | Notes |
|----------|----------|----------|-------|
| SwarmCA Ed25519 | YubiHSM2 / ca/state/ | Annual | Root of trust |
| WireGuard keys | nodes/<id>/wg.key | Per-node | Auto-generated |
| Node Ed25519 | nodes/<id>/ed25519.key | Per-node | For JWT signing |
| PSK | /etc/wireguard/psk/ | Weekly | Via rotate-psk.sh |

## Service Ports

| Service | Port | Protocol | Access |
|---------|------|----------|--------|
| WireGuard | 51820 | UDP | Public |
| NATS client | 4222 | TCP | WG mesh only |
| NATS cluster | 6222 | TCP | WG mesh only |
| NATS leaf | 7422 | TCP | WG mesh only |
| Matrix client | 8008 | TCP | WG mesh only |
| Matrix federation | 8448 | TCP | WG mesh only |
| Syncthing GUI | 8384 | TCP | WG mesh only |
| Syncthing sync | 22000 | TCP | WG mesh only |
| Headscale | 8090 | TCP | Localhost |

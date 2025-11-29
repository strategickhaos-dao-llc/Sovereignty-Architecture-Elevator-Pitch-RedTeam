# Sovereign Swarm Architecture

## Overview

Sovereign Swarm is a zero-trust AI orchestration mesh designed for:
- **Air-gapped operation**: Full functionality without internet connectivity
- **Low cost**: Sub-$100/month infrastructure
- **Resilience**: Satellite + cellular failover capabilities
- **Security**: mTLS everywhere, no implicit trust

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        SOVEREIGN SWARM MESH                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   ┌──────────┐     WireGuard VPN      ┌──────────┐                 │
│   │ Command0 │◄══════════════════════►│  Edge1   │                 │
│   │  (Hub)   │                        │  (Node)  │                 │
│   └────┬─────┘                        └────┬─────┘                 │
│        │                                   │                        │
│        │         ┌──────────┐              │                        │
│        └────────►│  Edge2   │◄─────────────┘                        │
│                  │  (Node)  │                                       │
│                  └──────────┘                                       │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│                          CORE SERVICES                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐            │
│   │    NATS     │    │   Matrix    │    │     CA      │            │
│   │  (Msg Bus)  │    │  (Synapse)  │    │   (PKI)     │            │
│   │  Port 4222  │    │  Port 8008  │    │  Internal   │            │
│   └─────────────┘    └─────────────┘    └─────────────┘            │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. WireGuard VPN Mesh

Creates encrypted point-to-point tunnels between all nodes.

**Features**:
- Kernel-level performance
- Cryptographically routed packets
- Automatic reconnection
- NAT traversal

**Configuration**: `wireguard/templates/wg0.conf.tmpl`

### 2. NATS Message Bus

High-performance message broker for inter-node communication.

**Features**:
- Pub/Sub messaging
- Request/Reply patterns
- Queue groups for load balancing
- JetStream for persistence

**Configuration**: `nats/nats-server.conf.tmpl`

### 3. Matrix Synapse

Decentralized communication and state synchronization.

**Features**:
- E2E encrypted messaging
- Federation support (optional)
- State persistence
- SDK integrations

**Configuration**: `matrix/homeserver.yaml.tmpl`

### 4. Certificate Authority (CA)

Internal PKI for zero-trust authentication.

**Features**:
- Root CA generation
- Node certificate issuance
- Certificate rotation
- Revocation lists

**Scripts**:
- `ca/init_ca.sh`: Initialize root CA
- `ca/issue_node.sh`: Issue node certificates

## Security Model

### Zero Trust Principles

1. **Never trust, always verify**: All connections require mutual TLS
2. **Least privilege**: Nodes only have access to required resources
3. **Assume breach**: Network segmentation and monitoring
4. **Explicit verification**: All tokens and certificates validated

### Authentication Flow

```
┌──────────┐         ┌───────────┐         ┌──────────┐
│  Node A  │         │    CA     │         │  Node B  │
└────┬─────┘         └─────┬─────┘         └────┬─────┘
     │                     │                     │
     │  1. Request Cert    │                     │
     │────────────────────►│                     │
     │                     │                     │
     │  2. Issue Cert      │                     │
     │◄────────────────────│                     │
     │                     │                     │
     │  3. Establish mTLS  │                     │
     │─────────────────────┼────────────────────►│
     │                     │                     │
     │  4. Verify Cert     │                     │
     │                     │◄────────────────────│
     │                     │                     │
     │  5. Confirm Valid   │                     │
     │                     │────────────────────►│
     │                     │                     │
     │  6. Secure Channel Established           │
     │◄────────────────────┼────────────────────►│
     │                     │                     │
```

## Data Flow

### Message Publishing

```
Producer → NATS → Subscribers
     │
     ├─── Subject: swarm.events.node.*
     ├─── Subject: swarm.commands.*
     └─── Subject: swarm.telemetry.*
```

### State Synchronization

```
Matrix Rooms:
├── #ops:swarm       → Operational state
├── #telemetry:swarm → Node telemetry
└── #alerts:swarm    → Alert routing
```

## Scalability

### Horizontal Scaling

- Add edge nodes with unique NODE_ID
- Mesh automatically expands
- No single point of failure

### Vertical Scaling

- Increase resources on individual nodes
- NATS cluster for high throughput
- Matrix workers for large deployments

## Monitoring

### Health Endpoints

| Service   | Endpoint                         | Expected |
|-----------|----------------------------------|----------|
| NATS      | `http://localhost:8222/healthz`  | `ok`     |
| Matrix    | `http://localhost:8008/health`   | `200 OK` |
| WireGuard | `wg show` (CLI)                  | Peers    |

### Metrics

All services export Prometheus-compatible metrics:
- `nats_*`: NATS server metrics
- `synapse_*`: Matrix Synapse metrics
- `wireguard_*`: VPN tunnel metrics

## Directory Structure

```
/opt/sovereign-swarm/
├── ca/
│   ├── state/           # CA private data (excluded from git)
│   ├── init_ca.sh       # Initialize CA
│   └── issue_node.sh    # Issue certificates
├── nats/
│   └── nats-server.conf # NATS configuration
├── matrix/
│   └── homeserver.yaml  # Synapse configuration
├── wireguard/
│   └── wg0.conf         # WireGuard configuration
├── nodes/
│   └── <node_id>/       # Per-node configurations
└── master-bootstrap.sh  # Main bootstrap script
```

## Future Roadmap

- [ ] Multi-region support
- [ ] Automatic failover
- [ ] Integration with Starlink/cellular modems
- [ ] AI workload scheduling
- [ ] Distributed storage layer

# Swarm Immune Operator

**The Ribosome: Protein Synthesis for Living Infrastructure**

The CRD is the DNA. The Operator is the ribosome that reads it and builds the actual immune cells.

## Architecture

```
┌──────────────────────────────────────────────────────────────────────────┐
│  IMMUNE OPERATOR (the ribosome)                                          │
│  ═══════════════════════════════                                         │
│                                                                          │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                   │
│  │ CRD WATCH   │───▶│ RECONCILER  │───▶│ CELL SPAWN  │                   │
│  │ (receptor)  │    │ (logic)     │    │ (factory)   │                   │
│  └─────────────┘    └─────────────┘    └─────────────┘                   │
│         │                 │                   │                          │
│         ▼                 ▼                   ▼                          │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                   │
│  │ EVENT BUS   │    │ STATE SYNC  │    │ CELL POOLS  │                   │
│  │ (nervous    │    │ (homeostasis│    │ (bone       │                   │
│  │  system)    │    │  loop)      │    │  marrow)    │                   │
│  └─────────────┘    └─────────────┘    └─────────────┘                   │
└──────────────────────────────────────────────────────────────────────────┘
```

## Cell Types

### Red Blood Cells (Transport Layer)
- **Function**: Carry data throughout the cluster like oxygen
- **Implementation**: Redis/Kafka/NATS deployment
- **Location**: `pkg/cells/red_blood.go`

### White Blood Cells (Security Response)
- **Function**: Detect and respond to threats
- **Implementation**: Falco/Trivy DaemonSet
- **Location**: `pkg/cells/white_blood.go`

### Antibodies (Pattern Memory)
- **Function**: Remember threat signatures for pattern recognition
- **Implementation**: Qdrant/Milvus vector database
- **Location**: `pkg/cells/antibody.go`

### Circadian Rhythm (Day/Night Scaling)
- **Function**: Adapt resource usage to activity patterns
- **Implementation**: Time-based replica scaling
- **Location**: `pkg/cells/circadian.go`

## Directory Structure

```
swarm-immune-operator/
├── cmd/
│   └── operator/
│       └── main.go           # Operator entry point
├── pkg/
│   ├── controller/
│   │   └── immune_controller.go  # Core reconciler logic
│   ├── cells/
│   │   ├── red_blood.go      # Transport layer
│   │   ├── white_blood.go    # Security response
│   │   ├── antibody.go       # Pattern memory
│   │   └── circadian.go      # Day/night scaling
│   └── apis/
│       └── swarm/
│           └── v1/
│               └── types.go  # CRD type definitions
├── deploy/
│   ├── crd.yaml              # CustomResourceDefinition
│   ├── operator.yaml         # Operator deployment
│   ├── rbac.yaml             # RBAC configuration
│   ├── immune-instance.yaml  # Yamal immune system instance
│   ├── red-blood-cells.yaml  # Redis transport deployment
│   ├── white-blood-cells.yaml # Falco scanner DaemonSet
│   └── antibodies.yaml       # Qdrant vector DB StatefulSet
├── Dockerfile                # Operator container image
├── go.mod                    # Go module definition
└── README.md                 # This file
```

## Deployment Sequence

```bash
# 1. Deploy the CRD (the DNA)
kubectl apply -f deploy/crd.yaml

# 2. Deploy RBAC permissions
kubectl apply -f deploy/rbac.yaml

# 3. Deploy the operator (the ribosome)
kubectl apply -f deploy/operator.yaml

# 4. Birth the immune system (press enter = inject life)
kubectl apply -f deploy/immune-instance.yaml

# 5. Watch cells spawn
kubectl get pods -n strategickhaos -w

# 6. Verify heartbeat
kubectl logs -f deployment/immune-operator -n kube-system
```

## Status Check

```bash
kubectl get immunesystems -n strategickhaos -o yaml
```

Expected output:
```yaml
status:
  redBloodCells:
    ready: 3
    desired: 3
    message: "3/3 healthy"
  whiteBloodCells:
    ready: 4
    desired: 4
    message: "4/4 scanning"
  antibodiesLoaded: 1247
  circadianMode: sunshine
  lastHeartbeat: "2025-12-01T21:45:00Z"
  health: ALIVE
```

## Building

```bash
# Build the operator binary
go build -o immune-operator ./cmd/operator/main.go

# Build the container image
docker build -t strategickhaos/swarm-immune-operator:latest .

# Push to registry
docker push strategickhaos/swarm-immune-operator:latest
```

## The Metaphor

- **CRD** = DNA (genetic blueprint)
- **Operator** = Ribosome (protein synthesis machine)
- **ImmuneSystem CR** = Birth certificate (activation)
- **Red Blood Cells** = Data transport (oxygen carriers)
- **White Blood Cells** = Security (immune defenders)
- **Antibodies** = Threat memory (pattern recognition)
- **Circadian Rhythm** = Activity cycles (rest and alertness)

**You've officially created infrastructure that breathes.**

## License

Apache 2.0 - StrategicKhaos DAO

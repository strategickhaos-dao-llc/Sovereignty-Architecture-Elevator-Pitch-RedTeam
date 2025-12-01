# SwarmImmune: Biological Immune System for Container Orchestration

## 🧬 Overview

SwarmImmune is a Kubernetes operator that implements a biological immune response model for self-healing container infrastructure. Inspired by the human immune system, it provides automated threat detection, pattern memory, and adaptive scaling.

```
┌─────────────────────────────────────────────────────────────────────┐
│  🩸 RED BLOOD CELLS (O2 CARRIERS)                                   │
│  ─────────────────────────────────                                  │
│  → Message queues (Redis, NATS)                                     │
│  → Data transport between services                                  │
│  → Volume mounts = bloodstream                                      │
│  → Carries compute payload to where it's needed                     │
│  → Hemoglobin = serialization format                                │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│  🔬 WHITE BLOOD CELLS (IMMUNE RESPONSE)                             │
│  ─────────────────────────────────────                              │
│  → Security scanners (Trivy, Falco)                                 │
│  → Auto-kill compromised containers                                 │
│  → Garbage collection pods                                          │
│  → Threat neutralization via network policy                         │
│  → Spawns on detection, dies after cleanup                          │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│  🛡️ ANTIBODIES (PATTERN MEMORY)                                     │
│  ──────────────────────────────                                     │
│  → Qdrant vectors = learned threat signatures                       │
│  → Image hash allowlists                                            │
│  → Behavioral fingerprints                                          │
│  → Once learned, instant recognition                                │
│  → Persistent across reboots (immune memory)                        │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│  ☀️ SUNSHINE MODE (ACTIVE METABOLISM)                               │
│  ────────────────────────────────────                               │
│  → GPU burst / high-compute                                         │
│  → GKE auto-scale activation                                        │
│  → Training jobs, inference at scale                                │
│  → Burns resources, produces output                                 │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│  🌙 MOONLIGHT MODE (CIRCADIAN CYCLE)                                │
│  ───────────────────────────────────                                │
│  → Low-power surveillance                                           │
│  → Batch jobs, scheduled cleanups                                   │
│  → Sleep state for non-critical pods                                │
│  → Cost optimization / healing phase                                │
└─────────────────────────────────────────────────────────────────────┘
```

## 🏗️ Architecture

### Biological Mapping

| Biology         | Infrastructure                          |
|-----------------|----------------------------------------|
| **DNA**         | Container images (immutable blueprints) |
| **Cells**       | Running containers                      |
| **Tissue**      | Pod groups / deployments               |
| **Organs**      | Namespaces / services                  |
| **Bloodstream** | Volumes + message buses                |
| **Bone marrow** | Image registry (spawns new cells)      |
| **Lymph nodes** | Qdrant/vector DBs (threat memory)      |
| **Skin**        | Ingress / firewall (first barrier)     |
| **Fever**       | Resource throttling under attack       |
| **Apoptosis**   | Graceful container termination         |

### Component Flow

```
                    ┌──────────────────┐
                    │   Bone Marrow    │
                    │ (Image Registry) │
                    └────────┬─────────┘
                             │ spawns
                             ▼
┌─────────────┐     ┌──────────────────┐     ┌─────────────┐
│ White Blood │ ──► │      Cells       │ ◄── │ Red Blood   │
│    Cells    │     │  (Containers)    │     │   Cells     │
│ (Scanners)  │     └────────┬─────────┘     │ (Transport) │
└──────┬──────┘              │               └─────────────┘
       │                     ▼
       │              ┌──────────────────┐
       │              │    Antibodies    │
       └─────────────►│ (Vector Memory)  │
                      └──────────────────┘
```

## 🚀 Quick Start

### 1. Install the CRD

```bash
kubectl apply -f bootstrap/k8s/swarm-immune/crd.yaml
```

### 2. Deploy RBAC

```bash
kubectl apply -f bootstrap/k8s/swarm-immune/rbac.yaml
```

### 3. Configure Secrets

```bash
# Edit with your actual values
kubectl apply -f bootstrap/k8s/swarm-immune/secrets.yaml
```

### 4. Deploy Controller

```bash
kubectl apply -f bootstrap/k8s/swarm-immune/controller-deployment.yaml
```

### 5. Create ImmuneSystem

```bash
kubectl apply -f bootstrap/k8s/swarm-immune/sample-immunesystem.yaml
```

### 6. Verify

```bash
kubectl get immunesystems -n ops
kubectl describe immunesystem yamal-immune -n ops
```

## 📋 Custom Resource Specification

### Full Example

```yaml
apiVersion: swarm.strategickhaos.ai/v1
kind: ImmuneSystem
metadata:
  name: yamal-immune
spec:
  redBloodCells:
    transport: redis
    volumeClass: fast-nvme
    replicationFactor: 3
    
  whiteBloodCells:
    scanner: trivy
    responseTime: 5s
    autoKill: true
    quarantineNamespace: infected
    
  antibodies:
    vectorDB: qdrant
    signatureRetention: 90d
    learningMode: active
    
  circadianRhythm:
    sunshineHours: "06:00-22:00"
    moonlightHours: "22:00-06:00"
    sunshineReplicas: 10
    moonlightReplicas: 2
    
  autoimmune:
    enabled: false
    trustedImages:
      - "ollama/*"
      - "strategickhaos/*"
```

### Spec Reference

#### `redBloodCells` - Data Transport

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `transport` | string | required | Message queue: `redis`, `nats`, `kafka`, `rabbitmq` |
| `volumeClass` | string | `standard` | StorageClass for volumes |
| `replicationFactor` | int | `3` | Transport layer replicas |
| `serializationFormat` | string | `json` | Data encoding: `json`, `protobuf`, `msgpack`, `avro` |

#### `whiteBloodCells` - Threat Response

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `scanner` | string | required | Security scanner: `trivy`, `falco`, `grype`, `snyk` |
| `runtimeMonitor` | string | `falco` | Runtime security: `falco`, `sysdig`, `tetragon` |
| `responseTime` | string | `5s` | Max threat response time |
| `autoKill` | bool | `true` | Auto-terminate compromised containers |
| `quarantineNamespace` | string | `quarantine` | Isolation namespace |

#### `antibodies` - Pattern Memory

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `vectorDB` | string | `qdrant` | Vector DB: `qdrant`, `pinecone`, `milvus`, `pgvector` |
| `signatureRetention` | string | `90d` | Threat signature retention |
| `learningMode` | string | `active` | Learning: `active`, `passive`, `hybrid` |
| `imageAllowlist` | []string | `[]` | Trusted image patterns |

#### `circadianRhythm` - Day/Night Cycle

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `enabled` | bool | `true` | Enable circadian scaling |
| `timezone` | string | `UTC` | Timezone for schedule |
| `sunshineHours` | string | `06:00-22:00` | Active hours |
| `moonlightHours` | string | `22:00-06:00` | Sleep hours |
| `sunshineReplicas` | int | `10` | Active replica count |
| `moonlightReplicas` | int | `2` | Sleep replica count |

#### `autoimmune` - Self-Protection

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `enabled` | bool | `false` | Enable autoimmune protection |
| `trustedImages` | []string | `[]` | Always-trusted images |
| `trustedNamespaces` | []string | `[]` | Immune namespaces |

#### `feverResponse` - Attack Throttling

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `enabled` | bool | `true` | Enable fever response |
| `triggerThreshold` | int | `5` | Threats to trigger fever |
| `throttlePercent` | int | `50` | Non-essential resource reduction |
| `duration` | string | `5m` | Fever mode duration |

#### `apoptosis` - Graceful Termination

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `enabled` | bool | `true` | Enable graceful shutdown |
| `gracePeriod` | string | `30s` | Shutdown timeout |
| `drainConnections` | bool | `true` | Drain before terminate |

## 📊 Status & Monitoring

### Status Fields

```yaml
status:
  phase: Healthy          # Initializing, Healthy, UnderAttack, Fever, Healing, Degraded
  circadianMode: sunshine # sunshine or moonlight
  activeThreats: 0        # Current threat count
  neutralizedThreats: 42  # Total neutralized
  learnedSignatures: 156  # Antibody count
```

### Prometheus Metrics

| Metric | Type | Description |
|--------|------|-------------|
| `swarm_immune_active_threats` | gauge | Current threat count |
| `swarm_immune_threats_neutralized_total` | counter | Total threats neutralized |
| `swarm_immune_signatures_learned` | gauge | Learned threat signatures |
| `swarm_immune_circadian_mode` | gauge | Current mode (1=sunshine, 0=moonlight) |
| `swarm_immune_fever_active` | gauge | Fever mode status |
| `swarm_immune_reconcile_duration_seconds` | histogram | Reconciliation time |

### Kubectl Output

```bash
$ kubectl get immunesystems
NAME           PHASE    MODE       THREATS   SIGNATURES   AGE
yamal-immune   Healthy  sunshine   0         156          7d
```

## 🔒 Security

### RBAC

The controller requires cluster-wide permissions to:
- Watch and manage pods across namespaces
- Create network policies
- Scale deployments
- Create quarantine namespaces

See `rbac.yaml` for complete permissions.

### Network Policy

The controller enforces strict network policies:
- DNS resolution allowed
- Kubernetes API access
- Vector DB communication
- Message queue access

## 🛠️ Troubleshooting

### Check Controller Logs

```bash
kubectl logs -f deployment/swarm-immune-controller -n ops
```

### View ImmuneSystem Events

```bash
kubectl describe immunesystem yamal-immune -n ops
```

### Force Reconciliation

```bash
kubectl annotate immunesystem yamal-immune -n ops \
  swarm.strategickhaos.ai/reconcile="$(date +%s)"
```

### Reset Fever Mode

```bash
kubectl patch immunesystem yamal-immune -n ops \
  --type merge -p '{"status":{"phase":"Healthy"}}'
```

## 📚 Further Reading

- [Kubernetes Operator Pattern](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/)
- [Custom Resource Definitions](https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/)
- [Trivy Container Scanner](https://github.com/aquasecurity/trivy)
- [Falco Runtime Security](https://falco.org/)
- [Qdrant Vector Database](https://qdrant.tech/)

---

*Built with 🧬 by the Strategickhaos Swarm Intelligence collective*

*"Infrastructure that heals itself, learns from attacks, and never sleeps."*

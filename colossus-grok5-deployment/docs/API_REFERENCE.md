# API Reference

## Colossus Grok-5 Deployment Suite

This document provides API reference for the Python modules in the Grok-5 deployment suite.

## Data Pipeline (`src/data/`)

### XProvenancePipeline

Main data ingestion pipeline with provenance tracking.

```python
from src.data import XProvenancePipeline

pipeline = XProvenancePipeline(
    db=database_instance,
    toxicity_model=model,
    ots_client=ots_client,
    batch_size=1000,
    logger=logger
)

# Ingest stream of tweets
stats = pipeline.ingest_stream(tweets)
print(f"Processed: {stats.total_processed}")
print(f"Accepted: {stats.accepted}")
print(f"Filtered: {stats.filtered}")

# Verify a batch
is_valid = pipeline.verify_batch(root, ots_proof)
```

### ToxicityFilter

Content toxicity filtering.

```python
from src.data import ToxicityFilter

filter = ToxicityFilter(threshold=0.30)

# Score text
score = filter.score("Hello world")

# Check if text passes filter
passes = filter.filter("Some text")

# Get detailed analysis
result = filter.analyze("Some text")
print(f"Score: {result.score}")
print(f"Passed: {result.passed}")
print(f"Categories: {result.categories}")
```

### MerkleBatchBuilder

Merkle tree construction for batch verification.

```python
from src.data import MerkleBatchBuilder

builder = MerkleBatchBuilder(batch_size=1000)

# Add leaves
builder.add_leaf(hash_hex)
builder.add_data(raw_bytes)

# Check status
print(f"Leaves: {builder.leaf_count}")
print(f"Full: {builder.is_full}")

# Finalize and get root
root = builder.finalize_root()

# Get proof for a leaf
proof = builder.get_proof(leaf_index)

# Reset for next batch
builder.reset()
```

### OpenTimestampsAnchor

Blockchain timestamping for provenance.

```python
from src.data import OpenTimestampsAnchor

anchor = OpenTimestampsAnchor(client=ots_client)

# Anchor a Merkle root
proof = anchor.anchor(merkle_root)

# Verify a timestamp
result = anchor.verify(merkle_root, proof)
print(f"Verified: {result.verified}")

# Get proof info
info = anchor.get_info(proof)
```

## Training (`src/training/`)

### EnergyScheduler

Energy-aware scheduling for training.

```python
from src.training import EnergyScheduler

scheduler = EnergyScheduler(
    power_client=power_client,
    megapack_client=megapack_client,
    power_limit_mw=250.0,
    soc_min=0.4
)

# Get current status
status = scheduler.get_status()
print(f"Power: {status.power_mw}MW")
print(f"SoC: {status.soc}")

# Evaluate window
decision = scheduler.evaluate_window()
if decision.allowed:
    # Proceed with training at suggested_scale
    scale = decision.suggested_scale
else:
    # Wait for delay_seconds
    time.sleep(decision.delay_seconds)

# Wait for suitable window
decision = scheduler.wait_for_window(max_wait_seconds=3600)
```

### PowerWindowDecision

Decision from energy scheduler.

```python
@dataclass
class PowerWindowDecision:
    allowed: bool           # Whether training is allowed
    reason: str             # "OK", "GRID_CONSTRAINT", "OFFPEAK_REQUIRED"
    suggested_scale: float  # Recommended scale factor (0.0-1.0)
    delay_seconds: int      # Seconds to wait if not allowed
```

### ConsensusProtocol

Checkpoint consensus across nodes.

```python
from src.training import ConsensusProtocol

protocol = ConsensusProtocol(threshold=0.99)

# Register nodes
protocol.register_node("node-1")
protocol.register_node("node-2")

# Initiate consensus
result = protocol.initiate_consensus(
    checkpoint_hash="abc123...",
    step=10000
)

if result.is_agreed:
    # Checkpoint accepted
    print(f"Consensus: {result.fraction}")
else:
    # Checkpoint rejected
    print(f"Reason: {result.state}")
```

### CheckpointGuardian

Checkpoint lifecycle management.

```python
from src.training import CheckpointGuardian

guardian = CheckpointGuardian(
    storage=storage_backend,
    checkpoint_dir="/checkpoints"
)

# Create checkpoint
metadata = guardian.create_checkpoint(
    step=10000,
    model_state=model.state_dict()
)

# Load checkpoint
data = guardian.load_checkpoint(step=10000)

# Get latest
latest = guardian.get_latest_checkpoint()

# List all
checkpoints = guardian.list_checkpoints()

# Verify
is_valid = guardian.verify_checkpoint(step=10000)
```

### Grok5Trainer

Main training loop.

```python
from src.training import Grok5Trainer

trainer = Grok5Trainer(
    model=model,
    optimizer=optimizer,
    energy_scheduler=scheduler,
    checkpoint_guardian=guardian,
    checkpoint_interval=1000,
    max_steps=1000000
)

# Start training
trainer.train(data_loader)

# Stop training
trainer.stop()

# Resume from checkpoint
trainer.resume(step=10000)  # Specific step
trainer.resume()            # Latest checkpoint

# Get current state
state = trainer.get_state()
```

## Verification (`src/verification/`)

### SafetyGate

Pre-deployment safety checks.

```python
from src.verification import SafetyGate

gate = SafetyGate(
    metrics_client=metrics,
    provenance_client=provenance,
    checkpoint_client=checkpoints,
    eval_client=evaluator
)

# Run all checks
report = gate.evaluate()
if report.ok:
    # Safe to deploy
    print(f"Passed {report.checks_passed}/{report.checks_total}")
else:
    # Deployment blocked
    for reason in report.reasons:
        print(f"Failed: {reason}")

# Individual checks
passed, msg = gate.check_power()
passed, msg = gate.check_consensus()
```

### SafetyReport

Result from safety gate.

```python
@dataclass
class SafetyReport:
    ok: bool                # Overall pass/fail
    reasons: list[str]      # Failure reasons
    timestamp: datetime
    checks_passed: int
    checks_total: int

    @property
    def pass_rate(self) -> float:
        return self.checks_passed / self.checks_total
```

### UnifiedVerifier

Orchestrates all verification.

```python
from src.verification import UnifiedVerifier

verifier = UnifiedVerifier(
    safety_gate=gate,
    audit_logger=logger,
    opa_endpoint="http://opa:8181"
)

# Run full verification
result = verifier.verify(deployment_id="deploy-123")
if result.deployment_approved:
    # Proceed with deployment
    pass

# Quick check (safety gate only)
if verifier.quick_check():
    # Safe to proceed
    pass

# Manual override
verifier.approve_manual(
    deployment_id="deploy-123",
    approver="admin@xai.com",
    notes="Emergency override approved"
)
```

### AuditLogger

Immutable audit logging.

```python
from src.verification import AuditLogger, AuditEvent

logger = AuditLogger(log_dir="/var/log/grok5/audit")

# Log an event
event = AuditEvent(
    event_type="deployment_start",
    deployment_id="deploy-123",
    user="admin",
    details={"version": "1.0.0"}
)
logged = logger.log(event)
print(f"Hash: {logged.hash}")

# Verify chain integrity
is_valid = logger.verify_chain()

# Query events
events = logger.get_events(
    event_type="deployment_start",
    start=datetime(2024, 1, 1)
)

# Export chain
logger.export("/backup/audit.json")
```

## Utilities (`src/utils/`)

### blake3_hasher

BLAKE3 hashing utilities.

```python
from src.utils import blake3_hex, blake3_bytes

# Hash to hex string
hash_str = blake3_hex(b"data")

# Hash to bytes
hash_bytes = blake3_bytes(b"data")
```

### ConfigLoader

Configuration loading with environment overrides.

```python
from src.utils import ConfigLoader

loader = ConfigLoader(config_path="/etc/grok5/config.yaml")
config = loader.load()

print(config.training.batch_size)
print(config.energy.power_limit_mw)
print(config.safety.hallucination_threshold)

# Force reload
config = loader.reload()
```

## Prometheus Metrics

All exported metrics:

| Metric | Type | Description |
|--------|------|-------------|
| `colossus_power_mw` | Gauge | Current power consumption |
| `megapack_soc` | Gauge | Battery state of charge |
| `grok5_training_step` | Gauge | Current training step |
| `grok5_training_loss` | Gauge | Current training loss |
| `grok5_hallucination_rate` | Gauge | Model hallucination rate |
| `grok5_bias_score` | Gauge | Model bias score |
| `checkpoint_consensus_fraction` | Gauge | Checkpoint agreement |
| `provenance_batches_total` | Counter | Batches processed |
| `provenance_records_total` | Counter | Records ingested |
| `grok5_safety_gate_passed` | Gauge | Safety gate status |

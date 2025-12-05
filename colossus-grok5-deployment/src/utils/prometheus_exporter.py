"""
Prometheus Metrics Exporter

Defines and exports Prometheus metrics for Colossus Grok-5 monitoring.
"""

from prometheus_client import Counter, Gauge, Histogram, Info

# Data ingestion metrics
ingest_counter = Counter(
    "provenance_batches_total",
    "Total number of provenance batches processed",
    ["pipeline", "status"],
)

ingest_records = Counter(
    "provenance_records_total",
    "Total number of records ingested",
    ["pipeline"],
)

ingest_latency = Histogram(
    "provenance_ingest_latency_seconds",
    "Latency of data ingestion operations",
    ["operation"],
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0, 60.0],
)

# Checkpoint metrics
checkpoint_counter = Counter(
    "checkpoint_total",
    "Total number of checkpoints created",
    ["status"],
)

checkpoint_consensus = Gauge(
    "checkpoint_consensus_fraction",
    "Fraction of nodes in consensus for latest checkpoint",
)

checkpoint_size = Gauge(
    "checkpoint_size_bytes",
    "Size of latest checkpoint in bytes",
)

# Energy metrics
power_gauge = Gauge(
    "colossus_power_mw",
    "Real-time MW draw for Colossus cluster",
)

soc_gauge = Gauge(
    "megapack_soc",
    "Tesla Megapack state-of-charge fraction",
)

energy_window = Gauge(
    "energy_window_allowed",
    "Whether current energy window allows training (1=allowed, 0=blocked)",
)

# Training metrics
training_step = Gauge(
    "grok5_training_step",
    "Current training step",
)

training_loss = Gauge(
    "grok5_training_loss",
    "Current training loss",
)

gpu_utilization = Gauge(
    "grok5_gpu_utilization",
    "Average GPU utilization across training pods",
)

# Safety metrics
hallucination_rate = Gauge(
    "grok5_hallucination_rate",
    "Model hallucination rate from latest evaluation",
)

bias_score = Gauge(
    "grok5_bias_score",
    "Model bias score from latest evaluation",
)

safety_gate_status = Gauge(
    "grok5_safety_gate_passed",
    "Whether safety gate passed (1=passed, 0=failed)",
)

# Provenance metrics
merkle_root_valid = Gauge(
    "provenance_merkle_root_valid",
    "Whether latest Merkle root is valid (1=valid, 0=invalid)",
)

ots_anchored = Counter(
    "provenance_ots_anchored_total",
    "Total number of OTS anchoring operations",
    ["status"],
)

# System info
system_info = Info(
    "grok5_deployment",
    "Grok-5 deployment information",
)


def set_deployment_info(
    version: str,
    cluster: str,
    region: str,
    artifact: str = "3558",
) -> None:
    """Set deployment info labels."""
    system_info.info({
        "version": version,
        "cluster": cluster,
        "region": region,
        "artifact": artifact,
    })

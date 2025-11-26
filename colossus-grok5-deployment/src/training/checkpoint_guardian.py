"""
Checkpoint Guardian

Manages checkpoint creation, validation, and storage with consensus.
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Optional, Protocol

try:
    from ..utils.blake3_hasher import blake3_hex
    from ..utils.prometheus_exporter import checkpoint_counter, checkpoint_consensus
except ImportError:
    from utils.blake3_hasher import blake3_hex
    from utils.prometheus_exporter import checkpoint_counter, checkpoint_consensus

from .consensus_protocol import ConsensusProtocol, CheckpointConsensus


class CheckpointStorage(Protocol):
    """Protocol for checkpoint storage."""

    def save(self, path: str, data: bytes) -> None:
        """Save checkpoint data."""
        ...

    def load(self, path: str) -> bytes:
        """Load checkpoint data."""
        ...

    def exists(self, path: str) -> bool:
        """Check if checkpoint exists."""
        ...


@dataclass
class CheckpointMetadata:
    """Metadata for a checkpoint."""

    step: int
    hash: str
    size_bytes: int
    timestamp: datetime = field(default_factory=datetime.utcnow)
    consensus: Optional[CheckpointConsensus] = None
    path: Optional[str] = None


class CheckpointGuardian:
    """
    Checkpoint guardian for Grok-5 training.

    Manages checkpoint lifecycle:
    1. Create checkpoint from model state
    2. Compute hash for verification
    3. Initiate consensus across nodes
    4. Store only if consensus reached
    5. Maintain audit trail
    """

    def __init__(
        self,
        storage: Optional[CheckpointStorage] = None,
        consensus: Optional[ConsensusProtocol] = None,
        checkpoint_dir: str = "/checkpoints",
        logger: Optional[logging.Logger] = None,
    ):
        """
        Initialize checkpoint guardian.

        Args:
            storage: Checkpoint storage backend
            consensus: Consensus protocol instance
            checkpoint_dir: Directory for checkpoints
            logger: Logger instance
        """
        self.storage = storage
        self.consensus = consensus or ConsensusProtocol()
        self.checkpoint_dir = Path(checkpoint_dir)
        self.log = logger or logging.getLogger(__name__)
        self._checkpoints: dict[int, CheckpointMetadata] = {}

    def create_checkpoint(
        self,
        step: int,
        model_state: Any,
        force: bool = False,
    ) -> Optional[CheckpointMetadata]:
        """
        Create and validate a checkpoint.

        Args:
            step: Training step number
            model_state: Model state dictionary or bytes
            force: Skip consensus check

        Returns:
            CheckpointMetadata if successful, None otherwise
        """
        self.log.info(f"Creating checkpoint for step {step}")

        # Serialize model state
        if isinstance(model_state, bytes):
            data = model_state
        else:
            import pickle
            data = pickle.dumps(model_state)

        # Compute hash
        checkpoint_hash = blake3_hex(data)

        # Create metadata
        metadata = CheckpointMetadata(
            step=step,
            hash=checkpoint_hash,
            size_bytes=len(data),
        )

        # Initiate consensus (unless forced)
        if not force:
            consensus_result = self.consensus.initiate_consensus(
                checkpoint_hash=checkpoint_hash,
                step=step,
            )
            metadata.consensus = consensus_result

            # Update Prometheus metric
            checkpoint_consensus.set(consensus_result.fraction)

            if not consensus_result.is_agreed:
                self.log.warning(
                    f"Checkpoint rejected: step={step} "
                    f"consensus={consensus_result.fraction:.4f}"
                )
                checkpoint_counter.labels(status="rejected").inc()
                return None

        # Store checkpoint
        path = self._get_checkpoint_path(step)
        metadata.path = str(path)

        if self.storage:
            try:
                self.storage.save(str(path), data)
            except Exception as e:
                self.log.error(f"Failed to save checkpoint: {e}")
                checkpoint_counter.labels(status="failed").inc()
                return None
        else:
            # Fallback to local filesystem
            self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)

        # Record checkpoint
        self._checkpoints[step] = metadata
        checkpoint_counter.labels(status="success").inc()

        self.log.info(
            f"Checkpoint saved: step={step} "
            f"hash={checkpoint_hash[:16]}... "
            f"size={len(data)} bytes"
        )

        return metadata

    def load_checkpoint(self, step: int) -> Optional[bytes]:
        """
        Load a checkpoint by step number.

        Args:
            step: Training step number

        Returns:
            Checkpoint data bytes, or None if not found
        """
        metadata = self._checkpoints.get(step)
        if not metadata or not metadata.path:
            return None

        path = Path(metadata.path)

        if self.storage:
            try:
                data = self.storage.load(str(path))
            except Exception as e:
                self.log.error(f"Failed to load checkpoint: {e}")
                return None
        else:
            if not path.exists():
                return None
            data = path.read_bytes()

        # Verify hash
        computed_hash = blake3_hex(data)
        if computed_hash != metadata.hash:
            self.log.error(
                f"Checkpoint hash mismatch: step={step} "
                f"expected={metadata.hash[:16]}... "
                f"got={computed_hash[:16]}..."
            )
            return None

        return data

    def get_latest_checkpoint(self) -> Optional[CheckpointMetadata]:
        """
        Get metadata for the latest checkpoint.

        Returns:
            CheckpointMetadata for latest checkpoint
        """
        if not self._checkpoints:
            return None
        latest_step = max(self._checkpoints.keys())
        return self._checkpoints[latest_step]

    def verify_checkpoint(self, step: int) -> bool:
        """
        Verify a checkpoint's integrity.

        Args:
            step: Training step number

        Returns:
            True if checkpoint is valid
        """
        metadata = self._checkpoints.get(step)
        if not metadata:
            return False

        data = self.load_checkpoint(step)
        if not data:
            return False

        # Hash verification already done in load_checkpoint
        return True

    def latest_consensus_fraction(self) -> float:
        """
        Get consensus fraction from latest checkpoint.

        Returns:
            Consensus fraction (0.0 - 1.0)
        """
        return self.consensus.latest_consensus_fraction()

    def _get_checkpoint_path(self, step: int) -> Path:
        """Get path for a checkpoint."""
        return self.checkpoint_dir / f"checkpoint_step_{step:08d}.bin"

    def list_checkpoints(self) -> list[CheckpointMetadata]:
        """
        List all checkpoints.

        Returns:
            List of checkpoint metadata
        """
        return list(self._checkpoints.values())

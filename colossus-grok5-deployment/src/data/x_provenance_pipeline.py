"""
X (Twitter) Provenance Pipeline

Main data pipeline for ingesting X streams with provenance tracking.
"""

import logging
from dataclasses import dataclass
from typing import Any, Iterable, Optional, Protocol

from .merkle_tree import MerkleBatchBuilder
from .ots_anchoring import OpenTimestampsAnchor
from .toxicity_filter import ToxicityFilter

try:
    from ..utils.blake3_hasher import blake3_hex
    from ..utils.prometheus_exporter import ingest_counter, ingest_records
except ImportError:
    from utils.blake3_hasher import blake3_hex
    from utils.prometheus_exporter import ingest_counter, ingest_records


class ProvenanceDB(Protocol):
    """Protocol for provenance database."""

    def store_provenance_batch(
        self,
        records: list[dict],
        root: str,
        ots_proof: bytes,
    ) -> None:
        """Store a batch of provenance records."""
        ...


@dataclass
class IngestStats:
    """Statistics for ingestion operation."""

    total_processed: int = 0
    accepted: int = 0
    filtered: int = 0
    batches: int = 0


MAX_TOXICITY = 0.30  # keep < 0.3 toxicity slice


class XProvenancePipeline:
    """
    X (Twitter) data ingestion pipeline with provenance tracking.

    Ingests tweets from X streams, filters toxic content, builds
    Merkle trees for batch provenance, and anchors roots with OTS.
    """

    def __init__(
        self,
        db: ProvenanceDB,
        toxicity_model: Optional[Any] = None,
        ots_client: Optional[Any] = None,
        batch_size: int = 1000,
        logger: Optional[logging.Logger] = None,
    ):
        """
        Initialize X provenance pipeline.

        Args:
            db: Provenance database
            toxicity_model: Toxicity scoring model
            ots_client: OpenTimestamps client
            batch_size: Records per batch (default: 1000)
            logger: Logger instance
        """
        self.db = db
        self.filter = ToxicityFilter(toxicity_model, threshold=MAX_TOXICITY)
        self.merkle = MerkleBatchBuilder(batch_size=batch_size)
        self.ots = OpenTimestampsAnchor(ots_client)
        self.log = logger or logging.getLogger(__name__)
        self._stats = IngestStats()

    def ingest_stream(self, tweets: Iterable[dict]) -> IngestStats:
        """
        Ingest a stream of tweets with provenance tracking.

        Args:
            tweets: Iterable of tweet dictionaries with 'id' and 'text' fields

        Returns:
            IngestStats with processing statistics
        """
        self._stats = IngestStats()
        batch: list[dict] = []

        for t in tweets:
            self._stats.total_processed += 1
            txt = t.get("text", "")

            # Filter toxic content
            score = self.filter.score(txt)
            if score > MAX_TOXICITY:
                self._stats.filtered += 1
                continue  # drop junk

            # Compute hash and add to Merkle tree
            h = blake3_hex(txt.encode("utf-8"))
            self.merkle.add_leaf(h)

            batch.append({
                "tweet_id": t["id"],
                "hash": h,
                "toxicity": score,
            })

            self._stats.accepted += 1

            # Flush batch when full
            if len(batch) >= self.merkle.batch_size:
                self._flush_batch(batch)
                batch = []

        # Flush remaining records
        if batch:
            self._flush_batch(batch)

        self.log.info(
            f"[provenance] Ingestion complete: "
            f"processed={self._stats.total_processed} "
            f"accepted={self._stats.accepted} "
            f"filtered={self._stats.filtered} "
            f"batches={self._stats.batches}"
        )

        return self._stats

    def _flush_batch(self, batch: list[dict]) -> None:
        """
        Flush a batch of records to storage.

        Args:
            batch: List of record dictionaries
        """
        if not batch:
            return

        # Finalize Merkle root
        root = self.merkle.finalize_root()

        # Anchor to OTS
        ots_proof = self.ots.anchor(root)

        # Store batch
        self.db.store_provenance_batch(batch, root=root, ots_proof=ots_proof)

        # Update metrics
        ingest_counter.labels(pipeline="x_provenance", status="success").inc()
        ingest_records.labels(pipeline="x_provenance").inc(len(batch))

        self._stats.batches += 1

        self.log.info(
            f"[provenance] batch={len(batch)} "
            f"root={root[:16]}... "
            f"ots={ots_proof[:16] if isinstance(ots_proof, bytes) else ots_proof}..."
        )

        # Reset for next batch
        self.merkle.reset()

    def verify_batch(self, root: str, ots_proof: bytes) -> bool:
        """
        Verify a batch by its Merkle root and OTS proof.

        Args:
            root: Merkle root hash
            ots_proof: OTS proof bytes

        Returns:
            True if verification passes
        """
        result = self.ots.verify(root, ots_proof)
        return result.verified

    @property
    def stats(self) -> IngestStats:
        """Get current ingestion statistics."""
        return self._stats

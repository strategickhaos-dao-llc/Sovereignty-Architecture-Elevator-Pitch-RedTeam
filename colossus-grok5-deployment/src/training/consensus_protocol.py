"""
Consensus Protocol

Multi-node checkpoint consensus for distributed training.
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, Protocol


class ConsensusState(Enum):
    """State of checkpoint consensus."""

    PENDING = "pending"
    VOTING = "voting"
    AGREED = "agreed"
    REJECTED = "rejected"
    TIMEOUT = "timeout"


@dataclass
class PowerWindowDecision:
    """Decision from energy scheduler about training window."""

    allowed: bool
    reason: str
    suggested_scale: float
    delay_seconds: int


@dataclass
class CheckpointVote:
    """Vote from a node on a checkpoint."""

    node_id: str
    checkpoint_hash: str
    step: int
    approved: bool
    timestamp: datetime = field(default_factory=datetime.utcnow)
    signature: Optional[bytes] = None


@dataclass
class CheckpointConsensus:
    """Result of checkpoint consensus."""

    checkpoint_hash: str
    step: int
    state: ConsensusState
    votes_for: int
    votes_against: int
    total_nodes: int
    fraction: float
    timestamp: datetime = field(default_factory=datetime.utcnow)

    @property
    def is_agreed(self) -> bool:
        """Check if consensus was reached."""
        return self.state == ConsensusState.AGREED


class NodeClient(Protocol):
    """Protocol for node communication client."""

    def request_vote(self, node_id: str, checkpoint_hash: str, step: int) -> CheckpointVote:
        """Request a vote from a node."""
        ...

    def broadcast_consensus(self, consensus: CheckpointConsensus) -> None:
        """Broadcast consensus result to all nodes."""
        ...


class ConsensusProtocol:
    """
    Checkpoint consensus protocol for distributed training.

    Ensures checkpoint integrity across 550K GPU nodes by requiring
    99% agreement before accepting a checkpoint.
    """

    DEFAULT_THRESHOLD = 0.99
    DEFAULT_TIMEOUT_SECONDS = 300

    def __init__(
        self,
        node_client: Optional[NodeClient] = None,
        threshold: float = DEFAULT_THRESHOLD,
        timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
        logger: Optional[logging.Logger] = None,
    ):
        """
        Initialize consensus protocol.

        Args:
            node_client: Client for node communication
            threshold: Minimum agreement fraction (default: 0.99)
            timeout_seconds: Voting timeout (default: 300)
            logger: Logger instance
        """
        self.client = node_client
        self.threshold = threshold
        self.timeout_seconds = timeout_seconds
        self.log = logger or logging.getLogger(__name__)
        self._active_nodes: set[str] = set()
        self._votes: dict[str, list[CheckpointVote]] = {}

    def register_node(self, node_id: str) -> None:
        """
        Register an active node.

        Args:
            node_id: Unique node identifier
        """
        self._active_nodes.add(node_id)
        self.log.debug(f"Registered node: {node_id}")

    def unregister_node(self, node_id: str) -> None:
        """
        Unregister a node.

        Args:
            node_id: Node to unregister
        """
        self._active_nodes.discard(node_id)
        self.log.debug(f"Unregistered node: {node_id}")

    @property
    def node_count(self) -> int:
        """Get number of active nodes."""
        return len(self._active_nodes)

    def initiate_consensus(
        self,
        checkpoint_hash: str,
        step: int,
    ) -> CheckpointConsensus:
        """
        Initiate consensus for a checkpoint.

        Args:
            checkpoint_hash: Hash of the checkpoint
            step: Training step number

        Returns:
            CheckpointConsensus result
        """
        if not self._active_nodes:
            self.log.warning("No active nodes for consensus")
            return CheckpointConsensus(
                checkpoint_hash=checkpoint_hash,
                step=step,
                state=ConsensusState.REJECTED,
                votes_for=0,
                votes_against=0,
                total_nodes=0,
                fraction=0.0,
            )

        self.log.info(
            f"Initiating consensus for step {step} "
            f"(hash: {checkpoint_hash[:16]}..., nodes: {len(self._active_nodes)})"
        )

        votes = self._collect_votes(checkpoint_hash, step)
        return self._evaluate_votes(checkpoint_hash, step, votes)

    def _collect_votes(
        self,
        checkpoint_hash: str,
        step: int,
    ) -> list[CheckpointVote]:
        """Collect votes from all nodes."""
        votes = []

        for node_id in self._active_nodes:
            try:
                if self.client:
                    vote = self.client.request_vote(node_id, checkpoint_hash, step)
                else:
                    # Simulated voting for development
                    vote = CheckpointVote(
                        node_id=node_id,
                        checkpoint_hash=checkpoint_hash,
                        step=step,
                        approved=True,
                    )
                votes.append(vote)
            except Exception as e:
                self.log.warning(f"Failed to get vote from {node_id}: {e}")

        # Store votes for audit
        self._votes[checkpoint_hash] = votes
        return votes

    def _evaluate_votes(
        self,
        checkpoint_hash: str,
        step: int,
        votes: list[CheckpointVote],
    ) -> CheckpointConsensus:
        """Evaluate collected votes."""
        total = len(self._active_nodes)
        votes_for = sum(1 for v in votes if v.approved)
        votes_against = len(votes) - votes_for
        fraction = votes_for / total if total > 0 else 0.0

        if fraction >= self.threshold:
            state = ConsensusState.AGREED
        else:
            state = ConsensusState.REJECTED

        result = CheckpointConsensus(
            checkpoint_hash=checkpoint_hash,
            step=step,
            state=state,
            votes_for=votes_for,
            votes_against=votes_against,
            total_nodes=total,
            fraction=fraction,
        )

        self.log.info(
            f"Consensus result: step={step} "
            f"state={state.value} "
            f"fraction={fraction:.4f} ({votes_for}/{total})"
        )

        # Broadcast result
        if self.client:
            try:
                self.client.broadcast_consensus(result)
            except Exception as e:
                self.log.error(f"Failed to broadcast consensus: {e}")

        return result

    def get_votes(self, checkpoint_hash: str) -> list[CheckpointVote]:
        """
        Get votes for a checkpoint.

        Args:
            checkpoint_hash: Checkpoint hash

        Returns:
            List of votes
        """
        return self._votes.get(checkpoint_hash, [])

    def latest_consensus_fraction(self) -> float:
        """
        Get fraction from most recent consensus.

        Returns:
            Latest consensus fraction
        """
        if not self._votes:
            return 0.0

        # Get most recent votes
        latest_hash = list(self._votes.keys())[-1]
        votes = self._votes[latest_hash]
        total = len(self._active_nodes)

        if total == 0:
            return 0.0

        votes_for = sum(1 for v in votes if v.approved)
        return votes_for / total

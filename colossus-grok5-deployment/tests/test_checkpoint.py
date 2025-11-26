#!/usr/bin/env python3
"""
Tests for Checkpoint System

Artifact #3558 - Colossus Grok-5 Deployment Suite
"""

import pytest
from unittest.mock import MagicMock, patch
import sys
import os
import tempfile

# Add src to path FIRST
src_path = os.path.join(os.path.dirname(__file__), '..', 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# Import directly from module files to avoid __init__.py import cascades
from training.consensus_protocol import (
    ConsensusProtocol,
    CheckpointConsensus,
    CheckpointVote,
    ConsensusState,
    PowerWindowDecision,
)
from training.checkpoint_guardian import CheckpointGuardian, CheckpointMetadata


class TestConsensusProtocol:
    """Tests for Consensus Protocol."""

    def test_register_node(self):
        """Test node registration."""
        protocol = ConsensusProtocol()
        protocol.register_node("node-1")
        protocol.register_node("node-2")
        assert protocol.node_count == 2

    def test_unregister_node(self):
        """Test node unregistration."""
        protocol = ConsensusProtocol()
        protocol.register_node("node-1")
        protocol.unregister_node("node-1")
        assert protocol.node_count == 0

    def test_consensus_with_all_agree(self):
        """Test consensus when all nodes agree."""
        protocol = ConsensusProtocol(threshold=0.99)
        for i in range(100):
            protocol.register_node(f"node-{i}")

        result = protocol.initiate_consensus("hash123", step=1000)
        assert result.is_agreed
        assert result.fraction >= 0.99

    def test_consensus_no_nodes(self):
        """Test consensus with no nodes."""
        protocol = ConsensusProtocol()
        result = protocol.initiate_consensus("hash123", step=1000)
        assert result.state == ConsensusState.REJECTED
        assert result.total_nodes == 0

    def test_latest_consensus_fraction(self):
        """Test getting latest consensus fraction."""
        protocol = ConsensusProtocol()
        protocol.register_node("node-1")
        protocol.initiate_consensus("hash123", step=1)
        fraction = protocol.latest_consensus_fraction()
        assert 0.0 <= fraction <= 1.0


class TestCheckpointGuardian:
    """Tests for Checkpoint Guardian."""

    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.guardian = CheckpointGuardian(
            checkpoint_dir=self.temp_dir
        )
        # Register nodes for consensus
        for i in range(10):
            self.guardian.consensus.register_node(f"node-{i}")

    def test_create_checkpoint(self):
        """Test checkpoint creation."""
        state = {"weights": [1, 2, 3], "step": 100}
        metadata = self.guardian.create_checkpoint(step=100, model_state=state)
        assert metadata is not None
        assert metadata.step == 100
        assert len(metadata.hash) == 64

    def test_create_checkpoint_force(self):
        """Test forced checkpoint creation."""
        # Even without nodes, force should work
        guardian = CheckpointGuardian(checkpoint_dir=self.temp_dir)
        state = {"weights": [1, 2, 3]}
        metadata = guardian.create_checkpoint(step=1, model_state=state, force=True)
        assert metadata is not None

    def test_load_checkpoint(self):
        """Test loading checkpoint."""
        state = {"test": "data"}
        self.guardian.create_checkpoint(step=1, model_state=state)
        data = self.guardian.load_checkpoint(step=1)
        assert data is not None

    def test_get_latest_checkpoint(self):
        """Test getting latest checkpoint."""
        self.guardian.create_checkpoint(step=1, model_state={"a": 1})
        self.guardian.create_checkpoint(step=2, model_state={"b": 2})
        latest = self.guardian.get_latest_checkpoint()
        assert latest is not None
        assert latest.step == 2

    def test_list_checkpoints(self):
        """Test listing checkpoints."""
        self.guardian.create_checkpoint(step=1, model_state={})
        self.guardian.create_checkpoint(step=2, model_state={})
        checkpoints = self.guardian.list_checkpoints()
        assert len(checkpoints) == 2

    def test_verify_checkpoint(self):
        """Test checkpoint verification."""
        self.guardian.create_checkpoint(step=1, model_state={"test": True})
        assert self.guardian.verify_checkpoint(step=1)
        assert not self.guardian.verify_checkpoint(step=999)

    def test_latest_consensus_fraction(self):
        """Test getting latest consensus fraction."""
        self.guardian.create_checkpoint(step=1, model_state={})
        fraction = self.guardian.latest_consensus_fraction()
        assert 0.0 <= fraction <= 1.0


class TestCheckpointConsensus:
    """Tests for CheckpointConsensus dataclass."""

    def test_is_agreed_true(self):
        """Test is_agreed returns True for AGREED state."""
        consensus = CheckpointConsensus(
            checkpoint_hash="abc",
            step=1,
            state=ConsensusState.AGREED,
            votes_for=99,
            votes_against=1,
            total_nodes=100,
            fraction=0.99,
        )
        assert consensus.is_agreed

    def test_is_agreed_false(self):
        """Test is_agreed returns False for non-AGREED states."""
        for state in [ConsensusState.REJECTED, ConsensusState.PENDING, ConsensusState.TIMEOUT]:
            consensus = CheckpointConsensus(
                checkpoint_hash="abc",
                step=1,
                state=state,
                votes_for=50,
                votes_against=50,
                total_nodes=100,
                fraction=0.5,
            )
            assert not consensus.is_agreed


class TestCheckpointVote:
    """Tests for CheckpointVote dataclass."""

    def test_vote_creation(self):
        """Test vote creation with defaults."""
        vote = CheckpointVote(
            node_id="node-1",
            checkpoint_hash="hash123",
            step=100,
            approved=True,
        )
        assert vote.node_id == "node-1"
        assert vote.approved
        assert vote.timestamp is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

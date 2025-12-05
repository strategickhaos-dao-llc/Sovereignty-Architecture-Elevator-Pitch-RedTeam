#!/usr/bin/env python3
"""
Tests for Data Provenance Pipeline

Artifact #3558 - Colossus Grok-5 Deployment Suite
"""

import pytest
from unittest.mock import MagicMock, patch
import sys
import os

# Add src to path FIRST
src_path = os.path.join(os.path.dirname(__file__), '..', 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# Import individual modules directly (not from __init__.py) to avoid cascade
from utils.blake3_hasher import blake3_hex, blake3_bytes
from data.toxicity_filter import ToxicityFilter, ToxicityResult
from data.merkle_tree import MerkleBatchBuilder, MerkleProof
from data.ots_anchoring import OpenTimestampsAnchor
from data.x_provenance_pipeline import XProvenancePipeline


class TestBlake3Hasher:
    """Tests for BLAKE3 hashing utilities."""

    def test_blake3_hex_empty(self):
        """Test hashing empty bytes."""
        result = blake3_hex(b"")
        assert isinstance(result, str)
        assert len(result) == 64  # 32 bytes = 64 hex chars

    def test_blake3_hex_deterministic(self):
        """Test that hashing is deterministic."""
        data = b"test data for hashing"
        result1 = blake3_hex(data)
        result2 = blake3_hex(data)
        assert result1 == result2

    def test_blake3_hex_different_inputs(self):
        """Test that different inputs produce different hashes."""
        result1 = blake3_hex(b"input one")
        result2 = blake3_hex(b"input two")
        assert result1 != result2

    def test_blake3_bytes(self):
        """Test bytes output."""
        result = blake3_bytes(b"test")
        assert isinstance(result, bytes)
        assert len(result) == 32


class TestToxicityFilter:
    """Tests for Toxicity Filter."""

    def test_empty_text_returns_zero(self):
        """Test that empty text returns 0 toxicity."""
        filter = ToxicityFilter()
        assert filter.score("") == 0.0
        assert filter.score("   ") == 0.0

    def test_clean_text_passes(self):
        """Test that clean text passes filter."""
        filter = ToxicityFilter(threshold=0.30)
        assert filter.filter("Hello, this is a friendly message!")

    def test_toxic_keywords_detected(self):
        """Test that toxic keywords increase score."""
        filter = ToxicityFilter()
        clean_score = filter.score("Hello world")
        toxic_score = filter.score("I hate this violent attack")
        assert toxic_score > clean_score

    def test_threshold_enforcement(self):
        """Test threshold is enforced."""
        filter = ToxicityFilter(threshold=0.1)
        # High toxicity text should not pass
        assert not filter.filter("hate kill attack")

    def test_analyze_returns_result(self):
        """Test analyze returns ToxicityResult."""
        filter = ToxicityFilter()
        result = filter.analyze("Hello world")
        assert isinstance(result, ToxicityResult)
        assert result.passed
        assert isinstance(result.categories, dict)


class TestMerkleBatchBuilder:
    """Tests for Merkle Tree Builder."""

    def test_add_leaf(self):
        """Test adding leaves."""
        builder = MerkleBatchBuilder(batch_size=10)
        hash_hex = blake3_hex(b"test data")
        builder.add_leaf(hash_hex)
        assert builder.leaf_count == 1

    def test_finalize_root(self):
        """Test finalizing Merkle root."""
        builder = MerkleBatchBuilder()
        builder.add_leaf(blake3_hex(b"leaf1"))
        builder.add_leaf(blake3_hex(b"leaf2"))
        root = builder.finalize_root()
        assert isinstance(root, str)
        assert len(root) == 64

    def test_root_deterministic(self):
        """Test that same leaves produce same root."""
        builder1 = MerkleBatchBuilder()
        builder1.add_leaf(blake3_hex(b"a"))
        builder1.add_leaf(blake3_hex(b"b"))
        root1 = builder1.finalize_root()

        builder2 = MerkleBatchBuilder()
        builder2.add_leaf(blake3_hex(b"a"))
        builder2.add_leaf(blake3_hex(b"b"))
        root2 = builder2.finalize_root()

        assert root1 == root2

    def test_different_leaves_different_root(self):
        """Test that different leaves produce different roots."""
        builder1 = MerkleBatchBuilder()
        builder1.add_leaf(blake3_hex(b"a"))
        root1 = builder1.finalize_root()

        builder2 = MerkleBatchBuilder()
        builder2.add_leaf(blake3_hex(b"b"))
        root2 = builder2.finalize_root()

        assert root1 != root2

    def test_reset(self):
        """Test reset clears state."""
        builder = MerkleBatchBuilder()
        builder.add_leaf(blake3_hex(b"test"))
        builder.finalize_root()
        builder.reset()
        assert builder.leaf_count == 0

    def test_batch_size_detection(self):
        """Test is_full detects batch size."""
        builder = MerkleBatchBuilder(batch_size=3)
        assert not builder.is_full
        builder.add_leaf(blake3_hex(b"1"))
        builder.add_leaf(blake3_hex(b"2"))
        assert not builder.is_full
        builder.add_leaf(blake3_hex(b"3"))
        assert builder.is_full


class TestOpenTimestampsAnchor:
    """Tests for OpenTimestamps Anchoring."""

    def test_anchor_creates_proof(self):
        """Test anchoring creates a proof."""
        anchor = OpenTimestampsAnchor()
        root = blake3_hex(b"merkle root")
        proof = anchor.anchor(root)
        assert isinstance(proof, bytes)
        assert len(proof) > 0

    def test_stub_proof_verifies(self):
        """Test stub proof verification."""
        anchor = OpenTimestampsAnchor()
        root = blake3_hex(b"test root")
        proof = anchor.anchor(root)
        result = anchor.verify(root, proof)
        assert result.verified

    def test_wrong_root_fails_verification(self):
        """Test verification fails with wrong root."""
        anchor = OpenTimestampsAnchor()
        root1 = blake3_hex(b"root 1")
        root2 = blake3_hex(b"root 2")
        proof = anchor.anchor(root1)
        result = anchor.verify(root2, proof)
        assert not result.verified

    def test_get_info(self):
        """Test getting proof info."""
        anchor = OpenTimestampsAnchor()
        root = blake3_hex(b"test")
        proof = anchor.anchor(root)
        info = anchor.get_info(proof)
        assert "proof_size" in info
        assert "is_stub" in info


class TestXProvenancePipeline:
    """Tests for X Provenance Pipeline."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_db = MagicMock()

    def test_ingest_clean_data(self):
        """Test ingesting clean data."""
        pipeline = XProvenancePipeline(db=self.mock_db)
        tweets = [
            {"id": "1", "text": "Hello world"},
            {"id": "2", "text": "Testing provenance"},
        ]
        stats = pipeline.ingest_stream(tweets)
        assert stats.total_processed == 2
        assert stats.accepted == 2
        assert stats.filtered == 0

    def test_filters_toxic_content(self):
        """Test that toxic content is filtered."""
        pipeline = XProvenancePipeline(db=self.mock_db)
        tweets = [
            {"id": "1", "text": "Hello world"},
            {"id": "2", "text": "hate kill attack violent racist"},
        ]
        stats = pipeline.ingest_stream(tweets)
        assert stats.filtered > 0
        assert stats.accepted < stats.total_processed

    def test_batch_flushing(self):
        """Test batch flushing occurs."""
        pipeline = XProvenancePipeline(db=self.mock_db, batch_size=2)
        tweets = [
            {"id": str(i), "text": f"Tweet {i}"}
            for i in range(5)
        ]
        stats = pipeline.ingest_stream(tweets)
        assert stats.batches >= 2

    def test_empty_stream(self):
        """Test handling empty stream."""
        pipeline = XProvenancePipeline(db=self.mock_db)
        stats = pipeline.ingest_stream([])
        assert stats.total_processed == 0
        assert stats.batches == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

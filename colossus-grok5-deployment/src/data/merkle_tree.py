"""
Merkle Tree Builder

Builds Merkle trees for batch data provenance verification.
"""

import logging
from dataclasses import dataclass, field
from typing import Optional

try:
    from ..utils.blake3_hasher import blake3_bytes, blake3_hex
except ImportError:
    from utils.blake3_hasher import blake3_bytes, blake3_hex


@dataclass
class MerkleNode:
    """Node in a Merkle tree."""

    hash: bytes
    left: Optional["MerkleNode"] = None
    right: Optional["MerkleNode"] = None

    @property
    def hex(self) -> str:
        """Get hex representation of hash."""
        return self.hash.hex()


@dataclass
class MerkleProof:
    """Proof for a leaf in a Merkle tree."""

    leaf_hash: str
    leaf_index: int
    proof_hashes: list[str]
    root_hash: str

    def verify(self, leaf_data: bytes) -> bool:
        """
        Verify proof for leaf data.

        Args:
            leaf_data: Original leaf data

        Returns:
            True if proof is valid
        """
        current = blake3_bytes(leaf_data)

        if current.hex() != self.leaf_hash:
            return False

        idx = self.leaf_index
        for proof_hash in self.proof_hashes:
            sibling = bytes.fromhex(proof_hash)
            if idx % 2 == 0:
                combined = current + sibling
            else:
                combined = sibling + current
            current = blake3_bytes(combined)
            idx //= 2

        return current.hex() == self.root_hash


class MerkleBatchBuilder:
    """
    Builds Merkle trees for batches of data.

    Used for data provenance tracking in Grok-5 training pipeline.
    """

    def __init__(
        self,
        batch_size: int = 1000,
        logger: Optional[logging.Logger] = None,
    ):
        """
        Initialize Merkle batch builder.

        Args:
            batch_size: Maximum leaves per tree (default: 1000)
            logger: Logger instance
        """
        self.batch_size = batch_size
        self.log = logger or logging.getLogger(__name__)
        self._leaves: list[bytes] = []
        self._root: Optional[MerkleNode] = None

    def add_leaf(self, hash_hex: str) -> None:
        """
        Add a leaf hash to the current batch.

        Args:
            hash_hex: Hex-encoded hash of the data
        """
        self._leaves.append(bytes.fromhex(hash_hex))

        if len(self._leaves) >= self.batch_size:
            self.log.debug(f"Batch full at {len(self._leaves)} leaves")

    def add_data(self, data: bytes) -> str:
        """
        Add data directly, computing hash.

        Args:
            data: Raw data to add

        Returns:
            Hex-encoded hash of the data
        """
        hash_hex = blake3_hex(data)
        self.add_leaf(hash_hex)
        return hash_hex

    @property
    def leaf_count(self) -> int:
        """Get current number of leaves."""
        return len(self._leaves)

    @property
    def is_full(self) -> bool:
        """Check if batch is full."""
        return len(self._leaves) >= self.batch_size

    def finalize_root(self) -> str:
        """
        Build tree and return root hash.

        Returns:
            Hex-encoded Merkle root hash
        """
        if not self._leaves:
            raise ValueError("Cannot finalize empty batch")

        # Pad to power of 2
        leaves = list(self._leaves)
        while len(leaves) & (len(leaves) - 1):
            leaves.append(leaves[-1])  # Duplicate last leaf

        # Build tree bottom-up
        nodes = [MerkleNode(hash=leaf) for leaf in leaves]

        while len(nodes) > 1:
            next_level = []
            for i in range(0, len(nodes), 2):
                left = nodes[i]
                right = nodes[i + 1] if i + 1 < len(nodes) else nodes[i]
                combined = left.hash + right.hash
                parent = MerkleNode(
                    hash=blake3_bytes(combined),
                    left=left,
                    right=right,
                )
                next_level.append(parent)
            nodes = next_level

        self._root = nodes[0]
        return self._root.hex

    def get_proof(self, leaf_index: int) -> MerkleProof:
        """
        Get Merkle proof for a leaf.

        Args:
            leaf_index: Index of the leaf

        Returns:
            MerkleProof for verification
        """
        if self._root is None:
            raise ValueError("Tree not finalized")

        if leaf_index < 0 or leaf_index >= len(self._leaves):
            raise ValueError(f"Invalid leaf index: {leaf_index}")

        # Build proof path
        proof_hashes = []
        leaves = list(self._leaves)

        # Pad to power of 2
        while len(leaves) & (len(leaves) - 1):
            leaves.append(leaves[-1])

        nodes = leaves
        idx = leaf_index

        while len(nodes) > 1:
            next_level = []
            for i in range(0, len(nodes), 2):
                left = nodes[i]
                right = nodes[i + 1] if i + 1 < len(nodes) else nodes[i]

                # Add sibling to proof
                if i == (idx // 2) * 2:
                    sibling_idx = i + 1 if idx % 2 == 0 else i
                    if sibling_idx < len(nodes):
                        sibling = nodes[sibling_idx]
                        if isinstance(sibling, bytes):
                            proof_hashes.append(sibling.hex())
                        else:
                            proof_hashes.append(sibling)

                # Compute parent
                if isinstance(left, bytes) and isinstance(right, bytes):
                    parent = blake3_bytes(left + right)
                else:
                    parent = blake3_bytes(left + right)
                next_level.append(parent)

            nodes = next_level
            idx //= 2

        return MerkleProof(
            leaf_hash=self._leaves[leaf_index].hex(),
            leaf_index=leaf_index,
            proof_hashes=proof_hashes,
            root_hash=self._root.hex,
        )

    def reset(self) -> None:
        """Reset builder for next batch."""
        self._leaves = []
        self._root = None
        self.log.debug("Merkle builder reset")

    def verify_root(self, expected_root: str) -> bool:
        """
        Verify current tree root matches expected.

        Args:
            expected_root: Expected root hash (hex)

        Returns:
            True if roots match
        """
        if self._root is None:
            return False
        return self._root.hex == expected_root

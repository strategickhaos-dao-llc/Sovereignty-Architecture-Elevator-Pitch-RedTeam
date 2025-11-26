"""
OpenTimestamps Anchoring

Anchors Merkle roots to Bitcoin blockchain for cryptographic provenance.
"""

import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Protocol


class OTSClient(Protocol):
    """Protocol for OpenTimestamps client."""

    def stamp(self, digest: bytes) -> bytes:
        """Create timestamp for digest."""
        ...

    def verify(self, digest: bytes, proof: bytes) -> bool:
        """Verify timestamp proof."""
        ...


@dataclass
class TimestampProof:
    """Proof of timestamp anchoring."""

    digest: str
    proof: bytes
    timestamp: datetime
    block_height: Optional[int] = None
    tx_id: Optional[str] = None
    verified: bool = False


class OpenTimestampsAnchor:
    """
    OpenTimestamps anchoring for data provenance.

    Anchors Merkle roots to Bitcoin blockchain to provide
    cryptographic proof of data existence at a specific time.
    """

    def __init__(
        self,
        client: Optional[OTSClient] = None,
        calendar_urls: Optional[list[str]] = None,
        logger: Optional[logging.Logger] = None,
    ):
        """
        Initialize OpenTimestamps anchor.

        Args:
            client: OTS client instance
            calendar_urls: List of calendar server URLs
            logger: Logger instance
        """
        self.client = client
        self.calendar_urls = calendar_urls or [
            "https://alice.btc.calendar.opentimestamps.org",
            "https://bob.btc.calendar.opentimestamps.org",
        ]
        self.log = logger or logging.getLogger(__name__)

    def anchor(self, merkle_root: str) -> bytes:
        """
        Anchor a Merkle root hash.

        Args:
            merkle_root: Hex-encoded Merkle root hash

        Returns:
            OTS proof bytes
        """
        digest = bytes.fromhex(merkle_root)

        if self.client is not None:
            try:
                proof = self.client.stamp(digest)
                self.log.info(
                    f"Anchored root {merkle_root[:16]}... "
                    f"(proof size: {len(proof)} bytes)"
                )
                return proof
            except Exception as e:
                self.log.error(f"OTS stamping failed: {e}")
                raise

        # Fallback: create stub proof for development
        return self._create_stub_proof(digest)

    def verify(self, merkle_root: str, proof: bytes) -> TimestampProof:
        """
        Verify a timestamp proof.

        Args:
            merkle_root: Hex-encoded Merkle root hash
            proof: OTS proof bytes

        Returns:
            TimestampProof with verification result
        """
        digest = bytes.fromhex(merkle_root)

        result = TimestampProof(
            digest=merkle_root,
            proof=proof,
            timestamp=datetime.utcnow(),
        )

        if self.client is not None:
            try:
                result.verified = self.client.verify(digest, proof)
                self.log.info(
                    f"Verified root {merkle_root[:16]}... "
                    f"verified={result.verified}"
                )
            except Exception as e:
                self.log.error(f"OTS verification failed: {e}")
                result.verified = False
        else:
            # Stub verification for development
            result.verified = self._verify_stub_proof(digest, proof)

        return result

    def upgrade_proof(self, proof: bytes) -> Optional[bytes]:
        """
        Upgrade a pending proof to a Bitcoin-anchored proof.

        Args:
            proof: Existing OTS proof bytes

        Returns:
            Upgraded proof bytes, or None if not ready
        """
        if self.client is None:
            self.log.warning("No OTS client configured for proof upgrade")
            return None

        # In production, this would check if the proof is pending
        # and upgrade it to a Bitcoin-anchored proof
        return proof

    def get_info(self, proof: bytes) -> dict:
        """
        Get information about a proof.

        Args:
            proof: OTS proof bytes

        Returns:
            Dictionary with proof information
        """
        return {
            "proof_size": len(proof),
            "is_stub": proof.startswith(b"STUB:"),
            "calendars": self.calendar_urls,
        }

    def _create_stub_proof(self, digest: bytes) -> bytes:
        """Create stub proof for development/testing."""
        timestamp = datetime.utcnow().isoformat()
        stub = f"STUB:{timestamp}:{digest.hex()}"
        self.log.warning("Using stub OTS proof (development mode)")
        return stub.encode("utf-8")

    def _verify_stub_proof(self, digest: bytes, proof: bytes) -> bool:
        """Verify stub proof for development/testing."""
        try:
            proof_str = proof.decode("utf-8")
            if not proof_str.startswith("STUB:"):
                return False
            # Format is STUB:{timestamp}:{digest_hex}
            # Find the last colon which separates timestamp from digest
            last_colon = proof_str.rfind(":")
            if last_colon == -1:
                return False
            proof_digest = proof_str[last_colon + 1:]
            return proof_digest == digest.hex()
        except Exception:
            return False

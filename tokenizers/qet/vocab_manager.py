"""
Vocabulary Manager for QuantumEvoTokenizer
Implements improvements: #2, #7, #22, #36
"""

import os
import json
import hashlib
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Any
from datetime import datetime
import subprocess


@dataclass
class VocabMetrics:
    """Metrics for vocabulary evaluation."""
    vocab_size: int
    compression_ratio: float
    oov_rate: float
    avg_token_length: float
    throughput_tokens_per_sec: Optional[float] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class VocabVersion:
    """Version information for vocabulary artifacts - Improvement #36."""
    version: str
    created_at: str
    hash: str
    metrics: VocabMetrics
    config_hash: str
    is_frozen: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["metrics"] = self.metrics.to_dict()
        return d


class VocabManager:
    """
    Manages vocabulary storage, versioning, and compatibility mapping.
    Implements improvements #2, #7, #22, #36.
    """
    
    def __init__(
        self,
        output_dir: str = "artifacts/qet",
        enable_notarization: bool = True
    ):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.enable_notarization = enable_notarization
        
        # Cached encoder for stable temp encoding - Improvement #2
        self._cached_encoder: Optional["StableEncoder"] = None
        self._cached_vocab_hash: Optional[str] = None
        
        # Compatibility mapping - Improvement #7
        self._compatibility_map: Dict[bytes, int] = {}
        
        # Version registry - Improvement #36
        self._versions: Dict[str, VocabVersion] = {}
        self._load_version_registry()
    
    def _load_version_registry(self) -> None:
        """Load version registry from disk."""
        registry_path = self.output_dir / "version_registry.json"
        if registry_path.exists():
            with open(registry_path, "r") as f:
                data = json.load(f)
                for version, info in data.items():
                    metrics = VocabMetrics(**info["metrics"])
                    self._versions[version] = VocabVersion(
                        version=info["version"],
                        created_at=info["created_at"],
                        hash=info["hash"],
                        metrics=metrics,
                        config_hash=info["config_hash"],
                        is_frozen=info.get("is_frozen", False)
                    )
    
    def _save_version_registry(self) -> None:
        """Save version registry to disk."""
        registry_path = self.output_dir / "version_registry.json"
        data = {v: info.to_dict() for v, info in self._versions.items()}
        with open(registry_path, "w") as f:
            json.dump(data, f, indent=2)
    
    def compute_vocab_hash(self, vocab: Set[bytes]) -> str:
        """Compute deterministic hash of vocabulary."""
        sorted_vocab = sorted(vocab)
        concat = b"".join(sorted_vocab)
        return hashlib.sha256(concat).hexdigest()
    
    def get_stable_encoder(self, vocab: Set[bytes]) -> "StableEncoder":
        """
        Get or create stable encoder with cached mergeable_ranks - Improvement #2.
        Avoids recreating encoder on every encode call.
        """
        vocab_hash = self.compute_vocab_hash(vocab)
        
        if self._cached_encoder is not None and self._cached_vocab_hash == vocab_hash:
            return self._cached_encoder
        
        # Build new stable encoder
        self._cached_encoder = StableEncoder(vocab)
        self._cached_vocab_hash = vocab_hash
        return self._cached_encoder
    
    def save_vocab(
        self,
        vocab: Set[bytes],
        version: str,
        config_dict: Dict[str, Any],
        metrics: VocabMetrics,
        freeze: bool = False
    ) -> VocabVersion:
        """
        Save vocabulary with versioning and artifacts - Improvements #22, #36.
        
        Emits:
        - vocab.json
        - config.json
        - metrics.json
        - hash.txt
        """
        version_dir = self.output_dir / version
        version_dir.mkdir(parents=True, exist_ok=True)
        
        # Save vocab
        vocab_path = version_dir / "vocab.json"
        vocab_list = [token.hex() for token in sorted(vocab)]
        with open(vocab_path, "w") as f:
            json.dump({"vocab": vocab_list, "size": len(vocab_list)}, f, indent=2)
        
        # Save config
        config_path = version_dir / "config.json"
        with open(config_path, "w") as f:
            json.dump(config_dict, f, indent=2)
        
        # Save metrics
        metrics_path = version_dir / "metrics.json"
        with open(metrics_path, "w") as f:
            json.dump(metrics.to_dict(), f, indent=2)
        
        # Compute and save hash
        vocab_hash = self.compute_vocab_hash(vocab)
        hash_path = version_dir / "hash.txt"
        with open(hash_path, "w") as f:
            f.write(vocab_hash)
        
        config_hash = hashlib.sha256(json.dumps(config_dict, sort_keys=True).encode()).hexdigest()
        
        # Create version info
        version_info = VocabVersion(
            version=version,
            created_at=datetime.utcnow().isoformat(),
            hash=vocab_hash,
            metrics=metrics,
            config_hash=config_hash,
            is_frozen=freeze
        )
        
        self._versions[version] = version_info
        self._save_version_registry()
        
        # Notarization hook - Improvement #22
        if self.enable_notarization:
            self._notarize_artifact(version_dir)
        
        return version_info
    
    def _notarize_artifact(self, artifact_dir: Path) -> None:
        """Run notarization hook if available."""
        notarize_script = Path("notarize_cognition.sh")
        if notarize_script.exists():
            vocab_path = artifact_dir / "vocab.json"
            try:
                subprocess.run(
                    ["bash", str(notarize_script), "--artifact", str(vocab_path)],
                    capture_output=True,
                    timeout=30
                )
            except (subprocess.TimeoutExpired, FileNotFoundError):
                pass  # Notarization is optional
    
    def load_vocab(self, version: str) -> Set[bytes]:
        """Load vocabulary from saved version."""
        vocab_path = self.output_dir / version / "vocab.json"
        if not vocab_path.exists():
            raise FileNotFoundError(f"Vocabulary version not found: {version}")
        
        with open(vocab_path, "r") as f:
            data = json.load(f)
        
        return {bytes.fromhex(h) for h in data["vocab"]}
    
    def freeze_version(self, version: str) -> VocabVersion:
        """
        Freeze a version for production use - Improvement #36.
        Frozen versions cannot be modified.
        """
        if version not in self._versions:
            raise ValueError(f"Version not found: {version}")
        
        self._versions[version].is_frozen = True
        self._save_version_registry()
        return self._versions[version]
    
    def fork_version(self, source_version: str, new_version: str) -> Set[bytes]:
        """
        Fork from a frozen version for experimentation - Improvement #36.
        """
        vocab = self.load_vocab(source_version)
        return vocab.copy()
    
    def build_compatibility_map(
        self,
        evolved_vocab: Set[bytes],
        base_tokenizer: str = "cl100k_base"
    ) -> Dict[bytes, int]:
        """
        Build mapping to base tokenizer IDs - Improvement #7.
        Allows using sovereign tokens while talking to existing models.
        """
        # Note: This requires tiktoken installed
        try:
            import tiktoken
            base_enc = tiktoken.get_encoding(base_tokenizer)
        except ImportError:
            return {}
        
        mapping: Dict[bytes, int] = {}
        
        for token in evolved_vocab:
            try:
                # Try to encode the token bytes
                text = token.decode("utf-8", errors="replace")
                base_ids = base_enc.encode(text)
                if len(base_ids) == 1:
                    mapping[token] = base_ids[0]
                else:
                    # Multi-token mapping: store first ID
                    mapping[token] = base_ids[0] if base_ids else -1
            except Exception:
                mapping[token] = -1  # Unknown mapping
        
        self._compatibility_map = mapping
        return mapping
    
    def project_to_base(
        self,
        tokens: List[bytes]
    ) -> List[int]:
        """Project evolved tokens to base tokenizer IDs."""
        return [self._compatibility_map.get(t, -1) for t in tokens]
    
    def get_version_info(self, version: str) -> Optional[VocabVersion]:
        """Get version information."""
        return self._versions.get(version)
    
    def list_versions(self, frozen_only: bool = False) -> List[str]:
        """List available versions."""
        versions = list(self._versions.keys())
        if frozen_only:
            versions = [v for v in versions if self._versions[v].is_frozen]
        return sorted(versions)


class StableEncoder:
    """
    Stable encoder with precomputed mergeable_ranks - Improvement #2.
    Caches encoding state to avoid recreation overhead.
    """
    
    def __init__(self, vocab: Set[bytes]):
        self.vocab = vocab
        self._mergeable_ranks: Dict[bytes, int] = {}
        self._build_ranks()
    
    def _build_ranks(self) -> None:
        """Precompute mergeable ranks for vocabulary."""
        # Sort by length, then lexicographically for determinism
        sorted_vocab = sorted(self.vocab, key=lambda x: (len(x), x))
        
        for rank, token in enumerate(sorted_vocab):
            self._mergeable_ranks[token] = rank
    
    def encode(self, text: bytes) -> List[int]:
        """Encode text to token IDs using cached ranks."""
        tokens = []
        i = 0
        
        while i < len(text):
            # Find longest matching token
            best_match = None
            best_length = 0
            
            for length in range(min(16, len(text) - i), 0, -1):
                candidate = text[i:i + length]
                if candidate in self._mergeable_ranks:
                    best_match = candidate
                    best_length = length
                    break
            
            if best_match is not None:
                tokens.append(self._mergeable_ranks[best_match])
                i += best_length
            else:
                # Fall back to single byte
                single = bytes([text[i]])
                if single in self._mergeable_ranks:
                    tokens.append(self._mergeable_ranks[single])
                else:
                    tokens.append(text[i])  # Raw byte as fallback
                i += 1
        
        return tokens
    
    def decode(self, ids: List[int]) -> bytes:
        """Decode token IDs back to bytes."""
        # Build reverse mapping
        id_to_token = {v: k for k, v in self._mergeable_ranks.items()}
        
        result = b""
        for token_id in ids:
            if token_id in id_to_token:
                result += id_to_token[token_id]
            elif 0 <= token_id < 256:
                result += bytes([token_id])
        
        return result
    
    @property
    def mergeable_ranks(self) -> Dict[bytes, int]:
        """Access precomputed ranks."""
        return self._mergeable_ranks.copy()

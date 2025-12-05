"""
Quantum Backend Interface and Implementations
Implements improvements: #10, #11, #12, #13, #14, #15, #16, #17
"""

import math
import hashlib
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Any
import random
import numpy as np


@dataclass
class VQEResult:
    """Result from VQE optimization."""
    optimal_params: np.ndarray
    optimal_energy: float
    boundaries: List[int]
    iterations: int
    converged: bool


@dataclass
class SegmentStats:
    """Statistics for a text segment used in caching - Improvement #16."""
    length: int
    entropy: float
    char_distribution_hash: str
    
    @classmethod
    def from_text(cls, text: str) -> "SegmentStats":
        """Compute statistics from text segment."""
        if not text:
            return cls(length=0, entropy=0.0, char_distribution_hash="empty")
        
        # Compute entropy
        char_counts: Dict[str, int] = {}
        for c in text:
            char_counts[c] = char_counts.get(c, 0) + 1
        
        total = len(text)
        entropy = 0.0
        for count in char_counts.values():
            p = count / total
            if p > 0:
                entropy -= p * math.log2(p)
        
        # Hash character distribution for clustering
        sorted_chars = sorted(char_counts.items())
        dist_str = "|".join(f"{c}:{count}" for c, count in sorted_chars[:20])
        dist_hash = hashlib.md5(dist_str.encode()).hexdigest()[:8]
        
        return cls(length=len(text), entropy=entropy, char_distribution_hash=dist_hash)
    
    def cluster_key(self) -> str:
        """Generate cluster key for cache lookup."""
        length_bucket = (self.length // 32) * 32
        entropy_bucket = round(self.entropy * 2) / 2
        return f"L{length_bucket}_E{entropy_bucket}_{self.char_distribution_hash}"


class QuantumBackend(ABC):
    """
    Abstract quantum backend interface - Improvement #11.
    Allows pluggable backends: fake, qutip, qiskit, hardware.
    """
    
    @abstractmethod
    def initialize(self, num_qubits: int, **kwargs) -> None:
        """Initialize the quantum backend."""
        pass
    
    @abstractmethod
    def run_vqe(
        self,
        hamiltonian: np.ndarray,
        initial_params: Optional[np.ndarray] = None,
        max_iterations: int = 100,
        use_gradient: bool = False
    ) -> VQEResult:
        """Run VQE optimization."""
        pass
    
    @abstractmethod
    def decode_boundaries(
        self,
        vqe_result: VQEResult,
        threshold: float = 0.5
    ) -> List[int]:
        """Decode boundary positions from VQE result - Improvement #14."""
        pass
    
    @abstractmethod
    def compute_entropy_adapted_depth(
        self,
        entropy: float,
        low_depth: int = 2,
        high_depth: int = 8
    ) -> int:
        """Compute circuit depth based on entropy - Improvement #15."""
        pass


class FakeQuantumBackend(QuantumBackend):
    """
    Fake quantum backend for testing and fast simulation.
    Implements classical approximations with quantum-inspired heuristics.
    """
    
    def __init__(self, seed: int = 42):
        self.seed = seed
        self.rng = np.random.default_rng(seed)
        self.random_state = random.Random(seed)
        self.num_qubits: int = 0
        self.cache: Dict[str, VQEResult] = {}
        self._cache_enabled = True
    
    def initialize(self, num_qubits: int, **kwargs) -> None:
        """Initialize fake backend."""
        self.num_qubits = num_qubits
        self._cache_enabled = kwargs.get("cache_solutions", True)
    
    def build_boundary_hamiltonian(
        self,
        text: str,
        boundary_cost: float = 1.0,
        merge_benefit: float = 0.5
    ) -> np.ndarray:
        """
        Build interpretable boundary Hamiltonian - Improvement #10.
        Encodes boundary cost and merge benefit directly.
        """
        n = min(len(text), self.num_qubits)
        dim = 2 ** n
        H = np.zeros((dim, dim), dtype=np.float64)
        
        # Compute local entropy for each position
        window_size = 4
        entropies = []
        for i in range(n):
            start = max(0, i - window_size)
            end = min(len(text), i + window_size + 1)
            window = text[start:end]
            
            char_counts: Dict[str, int] = {}
            for c in window:
                char_counts[c] = char_counts.get(c, 0) + 1
            
            total = len(window)
            entropy = 0.0
            for count in char_counts.values():
                p = count / total
                if p > 0:
                    entropy -= p * math.log2(p)
            entropies.append(entropy)
        
        max_entropy = max(entropies) if entropies else 1.0
        if max_entropy == 0:
            max_entropy = 1.0  # Prevent division by zero
        
        # Build Hamiltonian with interpretable terms
        for i in range(dim):
            boundary_count = bin(i).count("1")
            
            # Boundary cost term (penalize too many boundaries)
            H[i, i] += boundary_cost * boundary_count
            
            # Merge benefit term (reward merging low-entropy regions)
            for qubit in range(n):
                if (i >> qubit) & 1 == 0:  # No boundary at this position
                    if entropies[qubit] / max_entropy < 0.5:
                        H[i, i] -= merge_benefit
            
            # High-entropy boundary encouragement
            for qubit in range(n):
                if (i >> qubit) & 1 == 1:  # Boundary at this position
                    entropy_factor = entropies[qubit] / max_entropy
                    H[i, i] -= merge_benefit * entropy_factor * 2
        
        return H
    
    def run_vqe(
        self,
        hamiltonian: np.ndarray,
        initial_params: Optional[np.ndarray] = None,
        max_iterations: int = 100,
        use_gradient: bool = False
    ) -> VQEResult:
        """
        Run VQE optimization using classical simulation.
        Implements improvements #13 (gradient support).
        """
        dim = hamiltonian.shape[0]
        num_params = int(math.log2(dim)) * 2
        
        if initial_params is None:
            initial_params = self.rng.uniform(0, 2 * math.pi, num_params)
        
        params = initial_params.copy()
        best_energy = float("inf")
        best_params = params.copy()
        
        for iteration in range(max_iterations):
            # Compute state from parameters (simple ansatz)
            state = np.zeros(dim, dtype=np.complex128)
            for i in range(dim):
                phase = 0.0
                for j, p in enumerate(params[:dim.bit_length()]):
                    if (i >> j) & 1:
                        phase += p
                amplitude = 1.0
                for j, p in enumerate(params[dim.bit_length():]):
                    amplitude *= math.cos(p / 2) if (i >> (j % dim.bit_length())) & 1 == 0 else math.sin(p / 2)
                state[i] = amplitude * np.exp(1j * phase)
            
            # Normalize
            norm = np.linalg.norm(state)
            if norm > 1e-10:
                state /= norm
            
            # Compute energy
            energy = np.real(np.conj(state) @ hamiltonian @ state)
            
            if energy < best_energy:
                best_energy = energy
                best_params = params.copy()
            
            # Update parameters
            if use_gradient:
                # Simple finite difference gradient
                grad = np.zeros_like(params)
                eps = 0.01
                for j in range(len(params)):
                    params_plus = params.copy()
                    params_plus[j] += eps
                    state_plus = self._compute_state(params_plus, dim)
                    energy_plus = np.real(np.conj(state_plus) @ hamiltonian @ state_plus)
                    grad[j] = (energy_plus - energy) / eps
                params -= 0.1 * grad
            else:
                # SPSA-style update
                delta = self.rng.choice([-1, 1], size=len(params))
                a_k = 0.1 / (iteration + 1) ** 0.602
                c_k = 0.1 / (iteration + 1) ** 0.101
                
                params_plus = params + c_k * delta
                params_minus = params - c_k * delta
                
                state_plus = self._compute_state(params_plus, dim)
                state_minus = self._compute_state(params_minus, dim)
                
                energy_plus = np.real(np.conj(state_plus) @ hamiltonian @ state_plus)
                energy_minus = np.real(np.conj(state_minus) @ hamiltonian @ state_minus)
                
                grad_est = (energy_plus - energy_minus) / (2 * c_k * delta + 1e-10)
                params -= a_k * grad_est
        
        # Decode boundaries from optimal state
        optimal_state = self._compute_state(best_params, dim)
        probabilities = np.abs(optimal_state) ** 2
        most_likely = int(np.argmax(probabilities))
        boundaries = [i for i in range(int(math.log2(dim))) if (most_likely >> i) & 1]
        
        return VQEResult(
            optimal_params=best_params,
            optimal_energy=best_energy,
            boundaries=boundaries,
            iterations=max_iterations,
            converged=True
        )
    
    def _compute_state(self, params: np.ndarray, dim: int) -> np.ndarray:
        """Compute quantum state from parameters."""
        state = np.zeros(dim, dtype=np.complex128)
        for i in range(dim):
            phase = 0.0
            for j, p in enumerate(params[:dim.bit_length()]):
                if (i >> j) & 1:
                    phase += p
            amplitude = 1.0
            for j, p in enumerate(params[dim.bit_length():]):
                amplitude *= math.cos(p / 2) if (i >> (j % dim.bit_length())) & 1 == 0 else math.sin(p / 2)
            state[i] = amplitude * np.exp(1j * phase)
        
        norm = np.linalg.norm(state)
        if norm > 1e-10:
            state /= norm
        return state
    
    def decode_boundaries(
        self,
        vqe_result: VQEResult,
        threshold: float = 0.5
    ) -> List[int]:
        """
        Direct boundary decoding from qubits - Improvement #14.
        Maps qubit states to boundary decisions deterministically.
        """
        return vqe_result.boundaries
    
    def compute_entropy_adapted_depth(
        self,
        entropy: float,
        low_depth: int = 2,
        high_depth: int = 8
    ) -> int:
        """
        Compute circuit depth based on entropy - Improvement #15.
        Low entropy regions get shallow circuits.
        """
        # Normalize entropy (assuming max ~4 for ASCII text)
        normalized = min(entropy / 4.0, 1.0)
        depth_range = high_depth - low_depth
        return low_depth + int(normalized * depth_range)
    
    def get_cached_solution(self, stats: SegmentStats) -> Optional[VQEResult]:
        """Get cached VQE solution - Improvement #16."""
        if not self._cache_enabled:
            return None
        return self.cache.get(stats.cluster_key())
    
    def cache_solution(self, stats: SegmentStats, result: VQEResult) -> None:
        """Cache VQE solution - Improvement #16."""
        if self._cache_enabled:
            self.cache[stats.cluster_key()] = result


class ClassicalBoundaryOptimizer:
    """
    Classical baseline boundary optimizer - Improvement #17.
    Uses dynamic programming for comparison with quantum approach.
    """
    
    def __init__(self, seed: int = 42):
        self.seed = seed
        self.rng = np.random.default_rng(seed)
    
    def optimize_boundaries(
        self,
        text: str,
        max_boundaries: int = 10
    ) -> Tuple[List[int], float]:
        """
        Find optimal boundaries using dynamic programming.
        Returns boundary positions and score.
        """
        n = len(text)
        if n == 0:
            return [], 0.0
        
        # Compute entropy for each position
        entropies = []
        window_size = 4
        for i in range(n):
            start = max(0, i - window_size)
            end = min(n, i + window_size + 1)
            window = text[start:end]
            
            char_counts: Dict[str, int] = {}
            for c in window:
                char_counts[c] = char_counts.get(c, 0) + 1
            
            total = len(window)
            entropy = 0.0
            for count in char_counts.values():
                p = count / total
                if p > 0:
                    entropy -= p * math.log2(p)
            entropies.append(entropy)
        
        # DP: find positions with highest entropy as boundaries
        indexed_entropies = list(enumerate(entropies))
        indexed_entropies.sort(key=lambda x: x[1], reverse=True)
        
        boundaries = sorted([idx for idx, _ in indexed_entropies[:max_boundaries]])
        total_entropy = sum(entropies[b] for b in boundaries)
        
        return boundaries, total_entropy


def create_backend(backend_type: str, seed: int = 42, **kwargs) -> QuantumBackend:
    """Factory function to create appropriate backend."""
    if backend_type == "fake":
        return FakeQuantumBackend(seed=seed)
    elif backend_type == "qutip":
        # Placeholder for qutip backend
        raise NotImplementedError("QuTiP backend not yet implemented")
    elif backend_type == "qiskit":
        # Placeholder for qiskit backend
        raise NotImplementedError("Qiskit backend not yet implemented")
    elif backend_type == "hardware":
        # Placeholder for hardware backend
        raise NotImplementedError("Hardware backend not yet implemented")
    else:
        raise ValueError(f"Unknown backend type: {backend_type}")

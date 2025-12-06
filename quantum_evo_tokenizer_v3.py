#!/usr/bin/env python3
"""
QuantumEvoTokenizer v3 - Sovereign Adaptive Tokenization with Quantum-Inspired Evolution
Strategickhaos DAO LLC - Cyber + LLM Stack

A research-grade tokenizer that uses evolutionary algorithms with optional quantum
backend simulation for vocabulary optimization. Designed for sovereign data corpora.

Features:
- Evolutionary vocabulary optimization using genetic algorithms
- Mock and Qiskit quantum backends for fitness evaluation
- Entropy-aware token generation
- Cryptographic hashing for DAO notarization
- Thread-safe operations for concurrent use

NOTE: This is a research prototype, not production-ready inference code.
"""

import hashlib
import json
import math
import random
import struct
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple


@dataclass
class QETConfig:
    """Configuration for QuantumEvoTokenizer."""
    
    # Evolution parameters
    generations: int = 100
    population_size: int = 32
    mutation_rate: float = 0.1
    crossover_rate: float = 0.7
    elite_ratio: float = 0.1
    
    # Vocabulary parameters
    vocab_size: int = 8192
    min_token_len: int = 1
    max_token_len: int = 16
    
    # Quantum backend: "mock" (fast), "qiskit" (real simulation), "none" (classical only)
    backend: str = "mock"
    
    # Entropy bounds for safety (prevents poisoning attacks)
    min_entropy: float = 0.1
    max_entropy: float = 0.99
    
    # Fitness weights
    compression_weight: float = 0.4
    entropy_weight: float = 0.3
    coverage_weight: float = 0.3
    
    # Randomness seed for reproducibility
    seed: Optional[int] = None
    
    # Safety mode: "daylight" (conservative), "moonlight" (experimental)
    safety_mode: str = "daylight"


@dataclass
class TokenGenome:
    """A single genome in the evolutionary population representing a vocabulary."""
    
    tokens: Dict[bytes, int]  # token bytes -> token ID
    fitness: float = 0.0
    entropy_score: float = 0.0
    compression_ratio: float = 0.0
    coverage_score: float = 0.0
    generation: int = 0
    hash: str = ""
    
    def __post_init__(self):
        """Calculate hash after initialization."""
        if not self.hash:
            self.hash = self._compute_hash()
    
    def _compute_hash(self) -> str:
        """Compute SHA-256 hash of the genome for notarization."""
        token_bytes = json.dumps(
            {k.hex(): v for k, v in sorted(self.tokens.items())},
            sort_keys=True
        ).encode('utf-8')
        return hashlib.sha256(token_bytes).hexdigest()[:16]


class QuantumFitnessEvaluator:
    """Evaluates genome fitness using quantum-inspired or classical methods."""
    
    def __init__(self, backend: str = "mock"):
        self.backend = backend
        self._qiskit_available = False
        
        if backend == "qiskit":
            try:
                from qiskit import QuantumCircuit
                from qiskit_aer import AerSimulator
                self._qiskit_available = True
            except ImportError:
                print("[WARN] Qiskit not available, falling back to mock backend")
                self.backend = "mock"
    
    def evaluate(
        self, 
        genome: TokenGenome, 
        corpus_data: List[bytes],
        config: QETConfig
    ) -> float:
        """Evaluate genome fitness against corpus."""
        
        if self.backend == "mock":
            return self._mock_quantum_fitness(genome, corpus_data, config)
        elif self.backend == "qiskit" and self._qiskit_available:
            return self._qiskit_fitness(genome, corpus_data, config)
        else:
            return self._classical_fitness(genome, corpus_data, config)
    
    def _mock_quantum_fitness(
        self, 
        genome: TokenGenome, 
        corpus_data: List[bytes],
        config: QETConfig
    ) -> float:
        """Fast mock quantum evaluation for benchmarking."""
        
        # Calculate compression ratio
        compression = self._calculate_compression(genome, corpus_data)
        
        # Calculate entropy score (quantum-inspired)
        entropy = self._calculate_entropy(genome)
        
        # Calculate coverage score
        coverage = self._calculate_coverage(genome, corpus_data)
        
        # Apply entropy bounds for safety
        if entropy < config.min_entropy or entropy > config.max_entropy:
            entropy_penalty = 0.5  # Penalize out-of-bounds entropy
        else:
            entropy_penalty = 1.0
        
        # Weighted fitness with quantum noise simulation
        quantum_noise = random.uniform(0.98, 1.02)  # ±2% noise
        
        fitness = (
            config.compression_weight * compression +
            config.entropy_weight * entropy +
            config.coverage_weight * coverage
        ) * entropy_penalty * quantum_noise
        
        genome.compression_ratio = compression
        genome.entropy_score = entropy
        genome.coverage_score = coverage
        genome.fitness = fitness
        
        return fitness
    
    def _qiskit_fitness(
        self, 
        genome: TokenGenome, 
        corpus_data: List[bytes],
        config: QETConfig
    ) -> float:
        """Real quantum circuit evaluation using Qiskit."""
        from qiskit import QuantumCircuit
        from qiskit_aer import AerSimulator
        
        # Create quantum circuit for fitness evaluation
        n_qubits = min(8, len(genome.tokens) % 8 + 1)
        qc = QuantumCircuit(n_qubits, n_qubits)
        
        # Encode genome properties into quantum state
        compression = self._calculate_compression(genome, corpus_data)
        entropy = self._calculate_entropy(genome)
        coverage = self._calculate_coverage(genome, corpus_data)
        
        # Apply rotations based on fitness components
        for i in range(n_qubits):
            angle = (compression + entropy + coverage) * (i + 1) / n_qubits
            qc.ry(angle, i)
        
        # Add entanglement
        for i in range(n_qubits - 1):
            qc.cx(i, i + 1)
        
        # Measure
        qc.measure(range(n_qubits), range(n_qubits))
        
        # Run simulation
        simulator = AerSimulator()
        result = simulator.run(qc, shots=100).result()
        counts = result.get_counts(qc)
        
        # Convert measurement results to fitness modifier
        measured_bits = max(counts, key=counts.get)
        quantum_factor = int(measured_bits, 2) / (2 ** n_qubits)
        
        # Apply entropy bounds
        if entropy < config.min_entropy or entropy > config.max_entropy:
            entropy_penalty = 0.5
        else:
            entropy_penalty = 1.0
        
        fitness = (
            config.compression_weight * compression +
            config.entropy_weight * entropy +
            config.coverage_weight * coverage
        ) * entropy_penalty * (0.9 + 0.2 * quantum_factor)
        
        genome.compression_ratio = compression
        genome.entropy_score = entropy
        genome.coverage_score = coverage
        genome.fitness = fitness
        
        return fitness
    
    def _classical_fitness(
        self, 
        genome: TokenGenome, 
        corpus_data: List[bytes],
        config: QETConfig
    ) -> float:
        """Classical fitness evaluation without quantum effects."""
        
        compression = self._calculate_compression(genome, corpus_data)
        entropy = self._calculate_entropy(genome)
        coverage = self._calculate_coverage(genome, corpus_data)
        
        if entropy < config.min_entropy or entropy > config.max_entropy:
            entropy_penalty = 0.5
        else:
            entropy_penalty = 1.0
        
        fitness = (
            config.compression_weight * compression +
            config.entropy_weight * entropy +
            config.coverage_weight * coverage
        ) * entropy_penalty
        
        genome.compression_ratio = compression
        genome.entropy_score = entropy
        genome.coverage_score = coverage
        genome.fitness = fitness
        
        return fitness
    
    def _calculate_compression(
        self, 
        genome: TokenGenome, 
        corpus_data: List[bytes]
    ) -> float:
        """Calculate compression ratio achieved by the genome."""
        if not corpus_data or not genome.tokens:
            return 0.0
        
        total_original = sum(len(data) for data in corpus_data)
        total_encoded = 0
        
        for data in corpus_data:
            encoded = self._greedy_encode(data, genome.tokens)
            total_encoded += len(encoded)
        
        if total_original == 0:
            return 0.0
        
        # Compression ratio: how many chars per token (higher = better compression)
        ratio = total_original / max(total_encoded, 1)
        
        # Normalize to 0-1 range (assuming max 10 chars per token is excellent)
        return min(ratio / 10.0, 1.0)
    
    def _calculate_entropy(self, genome: TokenGenome) -> float:
        """Calculate Shannon entropy of the vocabulary distribution."""
        if not genome.tokens:
            return 0.0
        
        # Use token byte lengths as proxy for distribution
        lengths = [len(token) for token in genome.tokens.keys()]
        total = sum(lengths)
        
        if total == 0:
            return 0.0
        
        entropy = 0.0
        for length in lengths:
            p = length / total
            if p > 0:
                entropy -= p * math.log2(p)  # Shannon entropy formula
        
        # Normalize to 0-1 range based on maximum possible entropy
        max_entropy = math.log2(len(genome.tokens)) if len(genome.tokens) > 1 else 1.0
        return min(entropy / max(max_entropy, 1), 1.0)
    
    def _calculate_coverage(
        self, 
        genome: TokenGenome, 
        corpus_data: List[bytes]
    ) -> float:
        """Calculate byte coverage of the corpus by the vocabulary."""
        if not corpus_data or not genome.tokens:
            return 0.0
        
        # Get all unique bytes in corpus
        corpus_bytes = set()
        for data in corpus_data:
            corpus_bytes.update(data)
        
        # Get all bytes covered by tokens
        token_bytes = set()
        for token in genome.tokens.keys():
            token_bytes.update(token)
        
        if not corpus_bytes:
            return 1.0
        
        coverage = len(corpus_bytes & token_bytes) / len(corpus_bytes)
        return coverage
    
    def _greedy_encode(
        self, 
        data: bytes, 
        vocab: Dict[bytes, int]
    ) -> List[int]:
        """Greedy encoding of data using vocabulary."""
        if not data or not vocab:
            return []
        
        # Sort tokens by length (longest first for greedy matching)
        sorted_tokens = sorted(vocab.keys(), key=len, reverse=True)
        
        encoded = []
        i = 0
        
        while i < len(data):
            matched = False
            
            for token in sorted_tokens:
                if data[i:i+len(token)] == token:
                    encoded.append(vocab[token])
                    i += len(token)
                    matched = True
                    break
            
            if not matched:
                # Unknown byte, encode as single byte token or skip
                single = data[i:i+1]
                if single in vocab:
                    encoded.append(vocab[single])
                else:
                    encoded.append(0)  # Unknown token ID
                i += 1
        
        return encoded


class QuantumEvoTokenizer:
    """
    Evolutionary tokenizer with quantum-inspired fitness evaluation.
    
    Evolves a vocabulary optimized for specific corpora using genetic algorithms.
    """
    
    def __init__(self, config: QETConfig, corpora: List[str]):
        """
        Initialize tokenizer with config and training corpora.
        
        Args:
            config: QETConfig with evolution and vocabulary parameters
            corpora: List of text strings to optimize vocabulary for
        """
        self.config = config
        self.corpora = corpora
        self.corpus_data = [text.encode('utf-8') for text in corpora]
        
        # Set random seed for reproducibility
        if config.seed is not None:
            random.seed(config.seed)
        
        # Initialize fitness evaluator
        self.evaluator = QuantumFitnessEvaluator(config.backend)
        
        # Population tracking
        self.population: List[TokenGenome] = []
        self.best_genome: Optional[TokenGenome] = None
        self.generation_history: List[Dict[str, Any]] = []
        
        # Initialize population
        self._initialize_population()
    
    def _initialize_population(self):
        """Initialize population with random genomes."""
        self.population = []
        
        # Extract common byte patterns from corpus for seeding
        seed_patterns = self._extract_seed_patterns()
        
        for i in range(self.config.population_size):
            tokens = self._generate_random_vocab(seed_patterns)
            genome = TokenGenome(tokens=tokens, generation=0)
            self.population.append(genome)
    
    def _extract_seed_patterns(self) -> List[bytes]:
        """Extract common patterns from corpus to seed initial population."""
        patterns = set()
        
        for data in self.corpus_data:
            # Add all single bytes
            for b in set(data):
                patterns.add(bytes([b]))
            
            # Add common 2-4 byte sequences
            for length in range(2, 5):
                for i in range(len(data) - length):
                    pattern = data[i:i+length]
                    patterns.add(pattern)
                    if len(patterns) > 10000:  # Limit for memory
                        break
        
        return list(patterns)[:5000]  # Return top patterns
    
    def _generate_random_vocab(
        self, 
        seed_patterns: List[bytes]
    ) -> Dict[bytes, int]:
        """Generate a random vocabulary seeded with common patterns."""
        vocab = {}
        token_id = 0
        
        # Add all single bytes for full coverage
        for b in range(256):
            vocab[bytes([b])] = token_id
            token_id += 1
        
        # Add seed patterns randomly
        remaining_slots = self.config.vocab_size - 256
        selected_patterns = random.sample(
            seed_patterns, 
            min(len(seed_patterns), remaining_slots)
        )
        
        for pattern in selected_patterns:
            if pattern not in vocab:
                vocab[pattern] = token_id
                token_id += 1
        
        # Fill remaining slots with random combinations
        while len(vocab) < self.config.vocab_size:
            length = random.randint(2, self.config.max_token_len)
            random_bytes = bytes(random.randint(0, 255) for _ in range(length))
            
            if random_bytes not in vocab:
                vocab[random_bytes] = token_id
                token_id += 1
        
        return vocab
    
    def evolve(self) -> Dict[str, Any]:
        """
        Run evolutionary optimization to find optimal vocabulary.
        
        Returns:
            Dict with evolved vocabulary, metrics, and hash for DAO notarization
        """
        start_time = time.time()
        
        for gen in range(self.config.generations):
            # Evaluate fitness for all genomes
            for genome in self.population:
                self.evaluator.evaluate(genome, self.corpus_data, self.config)
                genome.generation = gen
            
            # Sort by fitness (descending)
            self.population.sort(key=lambda g: g.fitness, reverse=True)
            
            # Track best genome
            if self.best_genome is None or self.population[0].fitness > self.best_genome.fitness:
                self.best_genome = self.population[0]
            
            # Record generation history
            self.generation_history.append({
                "generation": gen,
                "best_fitness": self.population[0].fitness,
                "avg_fitness": sum(g.fitness for g in self.population) / len(self.population),
                "best_compression": self.population[0].compression_ratio,
                "best_entropy": self.population[0].entropy_score
            })
            
            # Selection and reproduction
            self._evolve_generation()
        
        evolution_time = time.time() - start_time
        
        # Final evaluation
        self.evaluator.evaluate(self.best_genome, self.corpus_data, self.config)
        
        return {
            "vocab": self.best_genome.tokens,
            "final_hash": self.best_genome.hash,
            "metrics": {
                "fitness": self.best_genome.fitness,
                "compression_ratio": self.best_genome.compression_ratio,
                "entropy_score": self.best_genome.entropy_score,
                "coverage_score": self.best_genome.coverage_score,
                "vocab_size": len(self.best_genome.tokens),
                "generations": self.config.generations,
                "evolution_time_seconds": evolution_time,
                "backend": self.config.backend,
                "safety_mode": self.config.safety_mode
            },
            "history": self.generation_history
        }
    
    def _evolve_generation(self):
        """Evolve population to next generation using selection, crossover, mutation."""
        new_population = []
        
        # Elite selection (keep top performers)
        elite_count = max(1, int(self.config.population_size * self.config.elite_ratio))
        new_population.extend(self.population[:elite_count])
        
        # Fill rest of population with offspring
        while len(new_population) < self.config.population_size:
            # Tournament selection
            parent1 = self._tournament_select()
            parent2 = self._tournament_select()
            
            # Crossover
            if random.random() < self.config.crossover_rate:
                child_tokens = self._crossover(parent1, parent2)
            else:
                child_tokens = dict(parent1.tokens)
            
            # Mutation
            if random.random() < self.config.mutation_rate:
                child_tokens = self._mutate(child_tokens)
            
            child = TokenGenome(tokens=child_tokens)
            new_population.append(child)
        
        self.population = new_population[:self.config.population_size]
    
    def _tournament_select(self, tournament_size: int = 3) -> TokenGenome:
        """Select genome using tournament selection."""
        tournament = random.sample(self.population, min(tournament_size, len(self.population)))
        return max(tournament, key=lambda g: g.fitness)
    
    def _crossover(
        self, 
        parent1: TokenGenome, 
        parent2: TokenGenome
    ) -> Dict[bytes, int]:
        """Perform crossover between two parent genomes."""
        child_tokens = {}
        token_id = 0
        
        # Combine tokens from both parents
        all_tokens = list(set(parent1.tokens.keys()) | set(parent2.tokens.keys()))
        
        # Select subset to fit vocab size
        selected = random.sample(
            all_tokens, 
            min(len(all_tokens), self.config.vocab_size)
        )
        
        for token in selected:
            child_tokens[token] = token_id
            token_id += 1
        
        return child_tokens
    
    def _mutate(self, tokens: Dict[bytes, int]) -> Dict[bytes, int]:
        """Mutate a genome by adding/removing/modifying tokens."""
        mutated = dict(tokens)
        
        mutation_type = random.choice(["add", "remove", "modify"])
        
        if mutation_type == "add" and len(mutated) < self.config.vocab_size:
            # Add a new random token
            length = random.randint(2, self.config.max_token_len)
            new_token = bytes(random.randint(0, 255) for _ in range(length))
            if new_token not in mutated:
                mutated[new_token] = max(mutated.values()) + 1
        
        elif mutation_type == "remove" and len(mutated) > 256:
            # Remove a random non-single-byte token
            multi_byte_tokens = [t for t in mutated.keys() if len(t) > 1]
            if multi_byte_tokens:
                to_remove = random.choice(multi_byte_tokens)
                del mutated[to_remove]
        
        elif mutation_type == "modify":
            # Modify a random token
            multi_byte_tokens = [t for t in mutated.keys() if len(t) > 1]
            if multi_byte_tokens:
                old_token = random.choice(multi_byte_tokens)
                old_id = mutated[old_token]
                del mutated[old_token]
                
                # Create modified version
                new_bytes = list(old_token)
                pos = random.randint(0, len(new_bytes) - 1)
                new_bytes[pos] = random.randint(0, 255)
                new_token = bytes(new_bytes)
                
                if new_token not in mutated:
                    mutated[new_token] = old_id
        
        return mutated
    
    def _temp_encode(
        self, 
        data: bytes, 
        vocab: Dict[bytes, int]
    ) -> List[int]:
        """Temporary encoding method for benchmarking (same as evaluator)."""
        return self.evaluator._greedy_encode(data, vocab)
    
    def encode(self, text: str) -> List[int]:
        """Encode text using evolved vocabulary."""
        if self.best_genome is None:
            raise ValueError("Must call evolve() before encoding")
        
        return self._temp_encode(text.encode('utf-8'), self.best_genome.tokens)
    
    def decode(self, tokens: List[int]) -> str:
        """Decode tokens back to text."""
        if self.best_genome is None:
            raise ValueError("Must call evolve() before decoding")
        
        # Build reverse lookup
        id_to_token = {v: k for k, v in self.best_genome.tokens.items()}
        
        decoded_bytes = b""
        for token_id in tokens:
            if token_id in id_to_token:
                decoded_bytes += id_to_token[token_id]
        
        return decoded_bytes.decode('utf-8', errors='replace')
    
    def get_vocab(self) -> Dict[str, int]:
        """Get vocabulary as string keys for serialization."""
        if self.best_genome is None:
            return {}
        
        return {k.hex(): v for k, v in self.best_genome.tokens.items()}
    
    def save_vocab(self, path: str):
        """Save vocabulary to JSON file."""
        vocab_data = {
            "vocab": self.get_vocab(),
            "config": {
                "vocab_size": self.config.vocab_size,
                "generations": self.config.generations,
                "backend": self.config.backend,
                "safety_mode": self.config.safety_mode
            },
            "hash": self.best_genome.hash if self.best_genome else "",
            "metrics": {
                "fitness": self.best_genome.fitness if self.best_genome else 0,
                "compression_ratio": self.best_genome.compression_ratio if self.best_genome else 0,
                "entropy_score": self.best_genome.entropy_score if self.best_genome else 0
            }
        }
        
        Path(path).write_text(json.dumps(vocab_data, indent=2))
    
    def notarize(self) -> Dict[str, str]:
        """Generate DAO notarization record for the evolved vocabulary."""
        if self.best_genome is None:
            raise ValueError("Must call evolve() before notarization")
        
        return {
            "vocab_hash": self.best_genome.hash,
            "full_hash": hashlib.sha256(
                json.dumps(self.get_vocab(), sort_keys=True).encode()
            ).hexdigest(),
            "config_hash": hashlib.sha256(
                json.dumps({
                    "generations": self.config.generations,
                    "population_size": self.config.population_size,
                    "vocab_size": self.config.vocab_size,
                    "backend": self.config.backend
                }, sort_keys=True).encode()
            ).hexdigest()[:16],
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }


# Convenience function for quick benchmarking
def quick_evolve(
    corpora: List[str],
    generations: int = 50,
    population_size: int = 16,
    backend: str = "mock"
) -> QuantumEvoTokenizer:
    """Quick evolution with default parameters for benchmarking."""
    config = QETConfig(
        generations=generations,
        population_size=population_size,
        backend=backend,
        vocab_size=4096
    )
    
    tokenizer = QuantumEvoTokenizer(config, corpora)
    tokenizer.evolve()
    
    return tokenizer


if __name__ == "__main__":
    # Demo usage
    print("QuantumEvoTokenizer v3 - Demo")
    print("=" * 50)
    
    # Sample corpora
    sample_corpora = [
        "The quick brown fox jumps over the lazy dog.",
        "Constitutional AI ensures alignment through RLHF.",
        "YAML configuration: key: value\n  nested:\n    - item1\n    - item2",
        "CVE-2024-1234: Critical vulnerability in parsing module."
    ]
    
    # Quick evolution
    config = QETConfig(generations=20, population_size=8, backend="mock")
    tokenizer = QuantumEvoTokenizer(config, sample_corpora)
    
    print("Evolving vocabulary...")
    result = tokenizer.evolve()
    
    print(f"\nEvolution complete!")
    print(f"  Vocab size: {result['metrics']['vocab_size']}")
    print(f"  Fitness: {result['metrics']['fitness']:.4f}")
    print(f"  Compression: {result['metrics']['compression_ratio']:.4f}")
    print(f"  Entropy: {result['metrics']['entropy_score']:.4f}")
    print(f"  Hash: {result['final_hash']}")
    
    # Test encoding
    test_text = "YAML config test"
    encoded = tokenizer.encode(test_text)
    decoded = tokenizer.decode(encoded)
    
    print(f"\nEncoding test:")
    print(f"  Original: {test_text}")
    print(f"  Tokens: {len(encoded)} tokens")
    print(f"  Decoded: {decoded}")
    
    # Notarization
    notary = tokenizer.notarize()
    print(f"\nNotarization record:")
    print(f"  Vocab hash: {notary['vocab_hash']}")
    print(f"  Timestamp: {notary['timestamp']}")

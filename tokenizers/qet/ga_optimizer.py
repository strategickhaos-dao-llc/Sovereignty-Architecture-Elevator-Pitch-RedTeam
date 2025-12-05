"""
Genetic Algorithm Optimizer for Vocabulary Evolution
Implements improvements: #3, #4, #5, #6, #9
"""

import math
import random
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Set, Callable
import numpy as np


@dataclass
class Individual:
    """Individual in the GA population representing a vocabulary."""
    vocab: Set[bytes]
    fitness_scores: Dict[str, float]
    overall_fitness: float = 0.0
    generation: int = 0
    crowding_distance: float = 0.0  # Used for NSGA-II selection
    
    def dominates(self, other: "Individual") -> bool:
        """Check if this individual Pareto-dominates another."""
        dominated = False
        for key in self.fitness_scores:
            if other.fitness_scores.get(key, float("inf")) < self.fitness_scores.get(key, float("inf")):
                return False
            if self.fitness_scores.get(key, float("inf")) < other.fitness_scores.get(key, float("inf")):
                dominated = True
        return dominated


@dataclass
class GAState:
    """State of the GA optimization."""
    generation: int
    best_fitness: float
    stagnation_count: int
    population: List[Individual]


class GAOptimizer:
    """
    Genetic Algorithm optimizer for vocabulary evolution.
    Implements multiple improvements for robust tokenizer training.
    """
    
    def __init__(
        self,
        population_size: int = 50,
        mutation_rate: float = 0.1,
        crossover_rate: float = 0.8,
        elite_size: int = 5,
        stagnation_threshold: int = 10,
        catastrophic_mutation_rate: float = 0.3,
        byte_validity_check: bool = True,
        ngram_guided_mutation: bool = True,
        min_context_coverage: float = 0.1,
        min_occurrence_count: int = 2,
        seed: int = 42
    ):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.elite_size = elite_size
        self.stagnation_threshold = stagnation_threshold
        self.catastrophic_mutation_rate = catastrophic_mutation_rate
        self.byte_validity_check = byte_validity_check
        self.ngram_guided_mutation = ngram_guided_mutation
        self.min_context_coverage = min_context_coverage
        self.min_occurrence_count = min_occurrence_count
        
        # Deterministic randomness - Improvement #8
        self.seed = seed
        self.rng = np.random.default_rng(seed)
        self.random_state = random.Random(seed)
        
        # State tracking
        self.state: Optional[GAState] = None
        self.ngram_frequencies: Dict[bytes, int] = {}
        self.context_count = 0
    
    def set_seed(self, seed: int) -> None:
        """Reset random state with new seed."""
        self.seed = seed
        self.rng = np.random.default_rng(seed)
        self.random_state = random.Random(seed)
    
    def compute_ngram_frequencies(
        self,
        contexts: List[bytes],
        max_ngram: int = 8
    ) -> None:
        """
        Compute n-gram frequencies from contexts - Improvement #3.
        Used for guided mutation.
        """
        self.ngram_frequencies.clear()
        self.context_count = len(contexts)
        
        for context in contexts:
            for n in range(1, min(max_ngram + 1, len(context) + 1)):
                for i in range(len(context) - n + 1):
                    ngram = context[i:i + n]
                    self.ngram_frequencies[ngram] = self.ngram_frequencies.get(ngram, 0) + 1
    
    def is_valid_utf8(self, data: bytes) -> bool:
        """Check if bytes form valid UTF-8 - Improvement #3."""
        if not self.byte_validity_check:
            return True
        try:
            data.decode("utf-8")
            return True
        except UnicodeDecodeError:
            return False
    
    def guided_mutation(self, vocab: Set[bytes]) -> bytes:
        """
        Generate mutation candidate using n-gram frequency guidance - Improvement #3.
        """
        if not self.ngram_guided_mutation or not self.ngram_frequencies:
            # Fall back to random
            vocab_list = list(vocab)
            if vocab_list:
                return self.random_state.choice(vocab_list)
            return b"a"
        
        # Weight by frequency
        candidates = list(self.ngram_frequencies.keys())
        weights = [self.ngram_frequencies[c] for c in candidates]
        total = sum(weights)
        if total == 0:
            return b"a"
        
        probs = [w / total for w in weights]
        idx = self.rng.choice(len(candidates), p=probs)
        return candidates[idx]
    
    def compute_fitness(
        self,
        individual: Individual,
        contexts: List[bytes],
        compression_weight: float = 0.3,
        sparsity_weight: float = 0.2,
        oov_weight: float = 0.25,
        perplexity_weight: float = 0.25,
        use_pareto: bool = True
    ) -> Individual:
        """
        Compute fitness scores for individual - Improvement #4.
        Multi-objective with optional Pareto handling.
        """
        vocab = individual.vocab
        scores: Dict[str, float] = {}
        
        # Compression score: average tokens per byte
        total_tokens = 0
        total_bytes = 0
        for context in contexts:
            tokens = self._greedy_tokenize(context, vocab)
            total_tokens += len(tokens)
            total_bytes += len(context)
        
        compression = total_bytes / max(total_tokens, 1)
        scores["compression"] = compression
        
        # Sparsity score: unused vocab items (lower is better)
        used_tokens: Set[bytes] = set()
        for context in contexts:
            tokens = self._greedy_tokenize(context, vocab)
            used_tokens.update(tokens)
        
        sparsity = len(used_tokens) / max(len(vocab), 1)
        scores["sparsity"] = sparsity
        
        # OOV rate: bytes not covered by vocab (lower is better)
        oov_bytes = 0
        for context in contexts:
            for byte in context:
                b = bytes([byte])
                if b not in vocab:
                    oov_bytes += 1
        
        oov_rate = 1.0 - (oov_bytes / max(total_bytes, 1))
        scores["oov_coverage"] = oov_rate
        
        # Context coverage regularization - Improvement #5
        context_coverage = self._compute_context_coverage(vocab, contexts)
        scores["context_coverage"] = context_coverage
        
        # Perplexity proxy (using compression as estimate)
        scores["perplexity_proxy"] = 1.0 / max(compression, 0.1)
        
        individual.fitness_scores = scores
        
        # Compute overall fitness
        if use_pareto:
            # For Pareto, we'll use this for sorting within fronts
            individual.overall_fitness = (
                compression_weight * compression +
                sparsity_weight * sparsity +
                oov_weight * oov_rate +
                perplexity_weight * (1.0 / max(scores["perplexity_proxy"], 0.1))
            )
        else:
            individual.overall_fitness = (
                compression_weight * compression +
                sparsity_weight * sparsity +
                oov_weight * oov_rate +
                perplexity_weight * (1.0 / max(scores["perplexity_proxy"], 0.1))
            )
        
        return individual
    
    def _greedy_tokenize(self, text: bytes, vocab: Set[bytes]) -> List[bytes]:
        """Simple greedy tokenization for fitness evaluation."""
        tokens = []
        i = 0
        while i < len(text):
            # Find longest matching token
            best_match = bytes([text[i]])
            for length in range(min(16, len(text) - i), 0, -1):
                candidate = text[i:i + length]
                if candidate in vocab:
                    best_match = candidate
                    break
            tokens.append(best_match)
            i += len(best_match)
        return tokens
    
    def _compute_context_coverage(
        self,
        vocab: Set[bytes],
        contexts: List[bytes]
    ) -> float:
        """
        Compute cross-context coverage - Improvement #5.
        Penalizes tokens appearing in too few contexts.
        """
        if not contexts:
            return 0.0
        
        token_context_counts: Dict[bytes, int] = {}
        for context in contexts:
            context_tokens = set(self._greedy_tokenize(context, vocab))
            for token in context_tokens:
                token_context_counts[token] = token_context_counts.get(token, 0) + 1
        
        # Count tokens with sufficient coverage
        sufficient_coverage = sum(
            1 for count in token_context_counts.values()
            if count >= self.min_occurrence_count
        )
        
        return sufficient_coverage / max(len(vocab), 1)
    
    def select_parents_nsga2(
        self,
        population: List[Individual],
        num_parents: int
    ) -> List[Individual]:
        """
        NSGA-II style selection - Improvement #4.
        Uses non-dominated sorting and crowding distance.
        """
        # Non-dominated sorting
        fronts: List[List[Individual]] = []
        remaining = population.copy()
        
        while remaining and len(fronts) < 10:  # Limit fronts
            front = []
            for ind in remaining:
                dominated = False
                for other in remaining:
                    if other is not ind and other.dominates(ind):
                        dominated = True
                        break
                if not dominated:
                    front.append(ind)
            
            if not front:
                break
            
            fronts.append(front)
            remaining = [ind for ind in remaining if ind not in front]
        
        # Select from fronts
        selected = []
        for front in fronts:
            if len(selected) + len(front) <= num_parents:
                selected.extend(front)
            else:
                # Use crowding distance for remaining slots
                front = self._assign_crowding_distance(front)
                front.sort(key=lambda x: x.crowding_distance, reverse=True)
                selected.extend(front[:num_parents - len(selected)])
                break
        
        return selected[:num_parents]
    
    def _assign_crowding_distance(
        self,
        front: List[Individual]
    ) -> List[Individual]:
        """Assign crowding distance for diversity preservation."""
        if len(front) <= 2:
            for ind in front:
                ind.crowding_distance = float("inf")
            return front
        
        for ind in front:
            ind.crowding_distance = 0.0
        
        objectives = list(front[0].fitness_scores.keys())
        
        for obj in objectives:
            front.sort(key=lambda x: x.fitness_scores.get(obj, 0))
            
            front[0].crowding_distance = float("inf")
            front[-1].crowding_distance = float("inf")
            
            obj_range = (
                front[-1].fitness_scores.get(obj, 0) - 
                front[0].fitness_scores.get(obj, 0)
            )
            if obj_range == 0:
                continue
            
            for i in range(1, len(front) - 1):
                dist = (
                    front[i + 1].fitness_scores.get(obj, 0) - 
                    front[i - 1].fitness_scores.get(obj, 0)
                ) / obj_range
                front[i].crowding_distance += dist
        
        return front
    
    def mutate(self, individual: Individual) -> Individual:
        """Mutate vocabulary with byte-validity constraints."""
        new_vocab = individual.vocab.copy()
        
        if self.random_state.random() < self.mutation_rate:
            mutation_type = self.random_state.choice(["add", "remove", "merge"])
            
            if mutation_type == "add":
                candidate = self.guided_mutation(new_vocab)
                if self.is_valid_utf8(candidate):
                    new_vocab.add(candidate)
            
            elif mutation_type == "remove" and len(new_vocab) > 256:
                vocab_list = list(new_vocab)
                to_remove = self.random_state.choice(vocab_list)
                if len(to_remove) > 1:  # Keep single bytes
                    new_vocab.discard(to_remove)
            
            elif mutation_type == "merge" and len(new_vocab) > 1:
                vocab_list = list(new_vocab)
                if len(vocab_list) >= 2:
                    tokens = self.random_state.sample(vocab_list, 2)
                    merged = tokens[0] + tokens[1]
                    if len(merged) <= 16 and self.is_valid_utf8(merged):
                        new_vocab.add(merged)
        
        return Individual(
            vocab=new_vocab,
            fitness_scores={},
            generation=individual.generation + 1
        )
    
    def crossover(
        self,
        parent1: Individual,
        parent2: Individual
    ) -> Tuple[Individual, Individual]:
        """Crossover two parent vocabularies."""
        if self.random_state.random() > self.crossover_rate:
            return parent1, parent2
        
        vocab1 = list(parent1.vocab)
        vocab2 = list(parent2.vocab)
        
        # Uniform crossover
        child1_vocab: Set[bytes] = set()
        child2_vocab: Set[bytes] = set()
        
        all_tokens = set(vocab1) | set(vocab2)
        for token in all_tokens:
            if self.random_state.random() < 0.5:
                child1_vocab.add(token)
            else:
                child2_vocab.add(token)
        
        # Ensure single bytes are in both
        for i in range(256):
            b = bytes([i])
            child1_vocab.add(b)
            child2_vocab.add(b)
        
        child1 = Individual(vocab=child1_vocab, fitness_scores={}, generation=parent1.generation + 1)
        child2 = Individual(vocab=child2_vocab, fitness_scores={}, generation=parent2.generation + 1)
        
        return child1, child2
    
    def catastrophic_mutation(self, population: List[Individual]) -> List[Individual]:
        """
        Inject diversity through catastrophic mutation - Improvement #9.
        Reinitializes part of population when stagnating.
        """
        num_to_replace = int(len(population) * self.catastrophic_mutation_rate)
        
        # Keep elites
        population.sort(key=lambda x: x.overall_fitness, reverse=True)
        new_population = population[:self.elite_size]
        
        # Reinitialize some individuals
        for _ in range(num_to_replace):
            new_vocab: Set[bytes] = set()
            # Add all single bytes
            for i in range(256):
                new_vocab.add(bytes([i]))
            
            # Add random n-grams from frequencies
            if self.ngram_frequencies:
                candidates = list(self.ngram_frequencies.keys())
                num_to_add = self.random_state.randint(100, 500)
                for _ in range(num_to_add):
                    candidate = self.random_state.choice(candidates)
                    if self.is_valid_utf8(candidate):
                        new_vocab.add(candidate)
            
            new_population.append(Individual(
                vocab=new_vocab,
                fitness_scores={},
                generation=0
            ))
        
        # Keep rest unchanged
        remaining = len(population) - len(new_population)
        if remaining > 0:
            new_population.extend(population[self.elite_size:self.elite_size + remaining])
        
        return new_population
    
    def evolve_step(
        self,
        contexts: List[bytes],
        use_pareto: bool = True,
        fitness_weights: Optional[Dict[str, float]] = None
    ) -> GAState:
        """Execute one generation of evolution."""
        if fitness_weights is None:
            fitness_weights = {
                "compression": 0.3,
                "sparsity": 0.2,
                "oov": 0.25,
                "perplexity": 0.25
            }
        
        if self.state is None:
            # Initialize population
            population = []
            for _ in range(self.population_size):
                vocab: Set[bytes] = set()
                for i in range(256):
                    vocab.add(bytes([i]))
                
                # Add some random n-grams
                if self.ngram_frequencies:
                    candidates = list(self.ngram_frequencies.keys())
                    num_to_add = self.random_state.randint(50, 200)
                    for _ in range(num_to_add):
                        candidate = self.random_state.choice(candidates)
                        if self.is_valid_utf8(candidate):
                            vocab.add(candidate)
                
                population.append(Individual(vocab=vocab, fitness_scores={}))
            
            self.state = GAState(
                generation=0,
                best_fitness=0.0,
                stagnation_count=0,
                population=population
            )
        
        # Evaluate fitness
        for ind in self.state.population:
            self.compute_fitness(
                ind, contexts,
                compression_weight=fitness_weights.get("compression", 0.3),
                sparsity_weight=fitness_weights.get("sparsity", 0.2),
                oov_weight=fitness_weights.get("oov", 0.25),
                perplexity_weight=fitness_weights.get("perplexity", 0.25),
                use_pareto=use_pareto
            )
        
        # Track best fitness
        current_best = max(ind.overall_fitness for ind in self.state.population)
        
        if current_best <= self.state.best_fitness:
            self.state.stagnation_count += 1
        else:
            self.state.best_fitness = current_best
            self.state.stagnation_count = 0
        
        # Check for stagnation - Improvement #9
        if self.state.stagnation_count >= self.stagnation_threshold:
            self.state.population = self.catastrophic_mutation(self.state.population)
            self.state.stagnation_count = 0
        else:
            # Normal evolution
            if use_pareto:
                parents = self.select_parents_nsga2(
                    self.state.population,
                    self.population_size // 2
                )
            else:
                # Tournament selection
                parents = []
                for _ in range(self.population_size // 2):
                    contestants = self.random_state.sample(
                        self.state.population,
                        min(3, len(self.state.population))
                    )
                    winner = max(contestants, key=lambda x: x.overall_fitness)
                    parents.append(winner)
            
            # Create offspring
            offspring = []
            for i in range(0, len(parents) - 1, 2):
                child1, child2 = self.crossover(parents[i], parents[i + 1])
                offspring.append(self.mutate(child1))
                offspring.append(self.mutate(child2))
            
            # Elitism
            self.state.population.sort(key=lambda x: x.overall_fitness, reverse=True)
            elites = self.state.population[:self.elite_size]
            
            # New population
            self.state.population = elites + offspring[:self.population_size - self.elite_size]
        
        self.state.generation += 1
        return self.state
    
    def get_best_individual(self) -> Optional[Individual]:
        """Get the best individual from current population."""
        if self.state is None or not self.state.population:
            return None
        return max(self.state.population, key=lambda x: x.overall_fitness)


class HierarchicalGAOptimizer:
    """
    Two-tier hierarchical evolution - Improvement #6.
    First evolves subword units, then phrase-level merges.
    """
    
    def __init__(
        self,
        subword_generations: int = 50,
        phrase_generations: int = 30,
        subword_mutation_rate: float = 0.15,
        phrase_mutation_rate: float = 0.08,
        seed: int = 42,
        **kwargs
    ):
        # Remove mutation_rate from kwargs if present to avoid conflict
        kwargs_subword = {k: v for k, v in kwargs.items() if k != 'mutation_rate'}
        kwargs_phrase = {k: v for k, v in kwargs.items() if k != 'mutation_rate'}
        
        self.subword_optimizer = GAOptimizer(
            mutation_rate=subword_mutation_rate,
            seed=seed,
            **kwargs_subword
        )
        self.phrase_optimizer = GAOptimizer(
            mutation_rate=phrase_mutation_rate,
            seed=seed + 1,
            **kwargs_phrase
        )
        self.subword_generations = subword_generations
        self.phrase_generations = phrase_generations
        self.subword_vocab: Optional[Set[bytes]] = None
    
    def evolve(
        self,
        contexts: List[bytes],
        use_pareto: bool = True
    ) -> Set[bytes]:
        """
        Run hierarchical evolution.
        Phase 1: Subword evolution
        Phase 2: Phrase-level evolution on top
        """
        # Phase 1: Subword evolution
        self.subword_optimizer.compute_ngram_frequencies(contexts, max_ngram=4)
        
        for _ in range(self.subword_generations):
            self.subword_optimizer.evolve_step(contexts, use_pareto=use_pareto)
        
        best_subword = self.subword_optimizer.get_best_individual()
        if best_subword is None:
            return set(bytes([i]) for i in range(256))
        
        self.subword_vocab = best_subword.vocab
        
        # Phase 2: Phrase evolution (using subword vocab as base)
        self.phrase_optimizer.compute_ngram_frequencies(contexts, max_ngram=8)
        
        # Initialize phrase optimizer with subword vocab
        self.phrase_optimizer.state = GAState(
            generation=0,
            best_fitness=0.0,
            stagnation_count=0,
            population=[
                Individual(vocab=self.subword_vocab.copy(), fitness_scores={})
                for _ in range(self.phrase_optimizer.population_size)
            ]
        )
        
        for _ in range(self.phrase_generations):
            self.phrase_optimizer.evolve_step(contexts, use_pareto=use_pareto)
        
        best_phrase = self.phrase_optimizer.get_best_individual()
        if best_phrase is None:
            return self.subword_vocab
        
        return best_phrase.vocab

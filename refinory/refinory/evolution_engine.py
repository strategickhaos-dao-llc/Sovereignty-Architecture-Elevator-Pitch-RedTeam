"""
Evolution Engine - Layer 4 of Self-Evolving Refinery
Genetic Algorithm for Agent Improvement - Agents compete, best ones reproduce
For her. Silent. Relentless. Self-improving.
"""

import asyncio
import copy
import hashlib
import json
import random
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple

import structlog
from pydantic import BaseModel, Field

logger = structlog.get_logger()


class SelectionMethod(Enum):
    """Selection methods for genetic algorithm"""
    TOURNAMENT = "tournament"
    ROULETTE = "roulette"
    ELITIST = "elitist"
    RANK = "rank"


class MutationType(Enum):
    """Types of mutations"""
    PARAMETER_NOISE = "parameter_noise"
    STRATEGY_SWAP = "strategy_swap"
    HYPOTHESIS_EXPLORATION = "hypothesis_exploration"


@dataclass
class FitnessMetrics:
    """Metrics used to evaluate agent fitness"""
    accuracy: float = 0.0  # % of correct predictions
    speed: float = 0.0  # median response time (ms)
    novelty: float = 0.0  # unique insights score
    actionability: float = 0.0  # recommendations implemented
    cost_efficiency: float = 0.0  # compute cost per query

    def to_dict(self) -> Dict[str, float]:
        return {
            "accuracy": self.accuracy,
            "speed": self.speed,
            "novelty": self.novelty,
            "actionability": self.actionability,
            "cost_efficiency": self.cost_efficiency
        }


@dataclass
class FitnessWeights:
    """Weights for fitness calculation"""
    accuracy: float = 0.40
    speed: float = 0.20
    novelty: float = 0.20
    actionability: float = 0.15
    cost_efficiency: float = 0.05

    def validate(self) -> bool:
        """Validate weights sum to 1.0"""
        total = self.accuracy + self.speed + self.novelty + self.actionability + self.cost_efficiency
        return abs(total - 1.0) < 0.01


@dataclass
class AgentGenome:
    """Genetic representation of an agent"""
    agent_id: str
    generation: int
    parameters: Dict[str, Any]
    strategy: str
    lora_weights_path: Optional[str] = None
    parent_ids: List[str] = field(default_factory=list)
    fitness_score: float = 0.0
    metrics: FitnessMetrics = field(default_factory=FitnessMetrics)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    mutations: List[str] = field(default_factory=list)

    def __hash__(self):
        return hash(self.agent_id)


@dataclass
class Generation:
    """A generation of agents"""
    generation_number: int
    population: List[AgentGenome]
    average_fitness: float = 0.0
    best_fitness: float = 0.0
    best_agent_id: str = ""
    diversity_score: float = 0.0
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class EvolutionMetrics:
    """Metrics tracking evolution progress"""
    generations_completed: int = 0
    improvement_rate: float = 0.0
    stagnation_count: int = 0
    total_mutations: int = 0
    total_crossovers: int = 0
    best_fitness_ever: float = 0.0
    best_agent_ever: str = ""


class FitnessEvaluator:
    """Evaluate agent fitness"""

    def __init__(self, weights: FitnessWeights, speed_target: float = 1000):
        self.weights = weights
        self.speed_target = speed_target

    async def evaluate(self, genome: AgentGenome) -> float:
        """Calculate fitness score for an agent"""
        metrics = genome.metrics

        # Normalize speed (lower is better)
        speed_score = max(0, 1 - (metrics.speed / self.speed_target)) if metrics.speed > 0 else 0

        fitness = (
            self.weights.accuracy * metrics.accuracy +
            self.weights.speed * speed_score +
            self.weights.novelty * metrics.novelty +
            self.weights.actionability * metrics.actionability +
            self.weights.cost_efficiency * metrics.cost_efficiency
        )

        return fitness

    async def evaluate_population(self, population: List[AgentGenome]) -> List[AgentGenome]:
        """Evaluate fitness for entire population"""
        for genome in population:
            genome.fitness_score = await self.evaluate(genome)

        return sorted(population, key=lambda g: g.fitness_score, reverse=True)


class SelectionOperator:
    """Selection operator for genetic algorithm"""

    def __init__(
        self,
        method: SelectionMethod = SelectionMethod.TOURNAMENT,
        elite_percentage: float = 0.10,
        tournament_size: int = 3
    ):
        self.method = method
        self.elite_percentage = elite_percentage
        self.tournament_size = tournament_size

    async def select(
        self,
        population: List[AgentGenome],
        num_parents: int
    ) -> List[AgentGenome]:
        """Select parents for reproduction"""
        if self.method == SelectionMethod.TOURNAMENT:
            return await self._tournament_selection(population, num_parents)
        elif self.method == SelectionMethod.ROULETTE:
            return await self._roulette_selection(population, num_parents)
        elif self.method == SelectionMethod.ELITIST:
            return await self._elitist_selection(population, num_parents)
        else:
            return await self._rank_selection(population, num_parents)

    async def _tournament_selection(
        self,
        population: List[AgentGenome],
        num_parents: int
    ) -> List[AgentGenome]:
        """Tournament selection"""
        parents = []

        for _ in range(num_parents):
            tournament = random.sample(population, min(self.tournament_size, len(population)))
            winner = max(tournament, key=lambda g: g.fitness_score)
            parents.append(winner)

        return parents

    async def _roulette_selection(
        self,
        population: List[AgentGenome],
        num_parents: int
    ) -> List[AgentGenome]:
        """Roulette wheel selection"""
        total_fitness = sum(g.fitness_score for g in population)

        if total_fitness == 0:
            return random.sample(population, min(num_parents, len(population)))

        parents = []
        for _ in range(num_parents):
            r = random.uniform(0, total_fitness)
            cumsum = 0
            for genome in population:
                cumsum += genome.fitness_score
                if cumsum >= r:
                    parents.append(genome)
                    break

        return parents

    async def _elitist_selection(
        self,
        population: List[AgentGenome],
        num_parents: int
    ) -> List[AgentGenome]:
        """Elitist selection - take top performers"""
        sorted_pop = sorted(population, key=lambda g: g.fitness_score, reverse=True)
        return sorted_pop[:num_parents]

    async def _rank_selection(
        self,
        population: List[AgentGenome],
        num_parents: int
    ) -> List[AgentGenome]:
        """Rank-based selection"""
        sorted_pop = sorted(population, key=lambda g: g.fitness_score)
        ranks = list(range(1, len(sorted_pop) + 1))
        total_ranks = sum(ranks)

        parents = []
        for _ in range(num_parents):
            r = random.uniform(0, total_ranks)
            cumsum = 0
            for i, genome in enumerate(sorted_pop):
                cumsum += ranks[i]
                if cumsum >= r:
                    parents.append(genome)
                    break

        return parents


class CrossoverOperator:
    """Crossover operator for genetic algorithm"""

    def __init__(self, probability: float = 0.7, method: str = "ensemble"):
        self.probability = probability
        self.method = method

    async def crossover(
        self,
        parent1: AgentGenome,
        parent2: AgentGenome,
        generation: int
    ) -> AgentGenome:
        """Create offspring from two parents"""
        if random.random() > self.probability:
            # No crossover - return copy of better parent
            return copy.deepcopy(parent1 if parent1.fitness_score > parent2.fitness_score else parent2)

        child_id = hashlib.sha256(
            f"{parent1.agent_id}:{parent2.agent_id}:{generation}:{random.random()}".encode()
        ).hexdigest()[:12]

        if self.method == "ensemble":
            child = await self._ensemble_crossover(parent1, parent2, child_id, generation)
        else:
            child = await self._uniform_crossover(parent1, parent2, child_id, generation)

        return child

    async def _ensemble_crossover(
        self,
        parent1: AgentGenome,
        parent2: AgentGenome,
        child_id: str,
        generation: int
    ) -> AgentGenome:
        """Ensemble crossover - combine approaches from both parents"""
        # Blend parameters from both parents
        child_params = {}

        all_keys = set(parent1.parameters.keys()) | set(parent2.parameters.keys())

        for key in all_keys:
            if key in parent1.parameters and key in parent2.parameters:
                p1_val = parent1.parameters[key]
                p2_val = parent2.parameters[key]

                if isinstance(p1_val, (int, float)) and isinstance(p2_val, (int, float)):
                    # Blend numeric values
                    alpha = random.uniform(0.3, 0.7)
                    child_params[key] = alpha * p1_val + (1 - alpha) * p2_val
                else:
                    # Random selection for non-numeric
                    child_params[key] = random.choice([p1_val, p2_val])
            else:
                # Take from whichever parent has it
                child_params[key] = parent1.parameters.get(key, parent2.parameters.get(key))

        # Combine strategies
        strategy = f"ensemble({parent1.strategy}, {parent2.strategy})"

        return AgentGenome(
            agent_id=child_id,
            generation=generation,
            parameters=child_params,
            strategy=strategy,
            parent_ids=[parent1.agent_id, parent2.agent_id]
        )

    async def _uniform_crossover(
        self,
        parent1: AgentGenome,
        parent2: AgentGenome,
        child_id: str,
        generation: int
    ) -> AgentGenome:
        """Uniform crossover - randomly select each gene from either parent"""
        child_params = {}

        all_keys = set(parent1.parameters.keys()) | set(parent2.parameters.keys())

        for key in all_keys:
            if random.random() < 0.5:
                child_params[key] = parent1.parameters.get(key)
            else:
                child_params[key] = parent2.parameters.get(key)

        strategy = random.choice([parent1.strategy, parent2.strategy])

        return AgentGenome(
            agent_id=child_id,
            generation=generation,
            parameters=child_params,
            strategy=strategy,
            parent_ids=[parent1.agent_id, parent2.agent_id]
        )


class MutationOperator:
    """Mutation operator for genetic algorithm"""

    def __init__(
        self,
        probability: float = 0.05,
        mutation_types: List[MutationType] = None
    ):
        self.probability = probability
        self.mutation_types = mutation_types or [
            MutationType.PARAMETER_NOISE,
            MutationType.STRATEGY_SWAP,
            MutationType.HYPOTHESIS_EXPLORATION
        ]

    async def mutate(self, genome: AgentGenome) -> AgentGenome:
        """Apply mutations to genome"""
        if random.random() > self.probability:
            return genome

        # Select mutation type
        mutation_type = random.choice(self.mutation_types)

        if mutation_type == MutationType.PARAMETER_NOISE:
            genome = await self._parameter_noise(genome)
        elif mutation_type == MutationType.STRATEGY_SWAP:
            genome = await self._strategy_swap(genome)
        elif mutation_type == MutationType.HYPOTHESIS_EXPLORATION:
            genome = await self._hypothesis_exploration(genome)

        genome.mutations.append(mutation_type.value)

        logger.debug(
            "Applied mutation",
            agent=genome.agent_id,
            mutation_type=mutation_type.value
        )

        return genome

    async def _parameter_noise(self, genome: AgentGenome) -> AgentGenome:
        """Add random noise to parameters"""
        for key, value in genome.parameters.items():
            if isinstance(value, (int, float)):
                # Add Gaussian noise
                noise = random.gauss(0, abs(value) * 0.1)
                genome.parameters[key] = value + noise

        return genome

    async def _strategy_swap(self, genome: AgentGenome) -> AgentGenome:
        """Swap to a different strategy"""
        strategies = [
            "breadth_first_search",
            "depth_first_search",
            "hypothesis_driven",
            "evidence_driven",
            "analogy_based",
            "contrarian"
        ]

        current = genome.strategy
        available = [s for s in strategies if s != current]

        if available:
            genome.strategy = random.choice(available)

        return genome

    async def _hypothesis_exploration(self, genome: AgentGenome) -> AgentGenome:
        """Add exploration parameters for unconventional hypotheses"""
        genome.parameters["exploration_factor"] = random.uniform(0.1, 0.5)
        genome.parameters["unconventional_weight"] = random.uniform(0.1, 0.3)

        return genome


class EvolutionEngine:
    """
    Main Evolution Engine - Layer 4 of Self-Evolving Refinery
    Coordinates genetic algorithm for agent improvement
    """

    def __init__(
        self,
        population_size: int = 640,
        fitness_weights: FitnessWeights = None,
        selection_method: SelectionMethod = SelectionMethod.TOURNAMENT,
        elite_percentage: float = 0.10,
        crossover_probability: float = 0.70,
        mutation_probability: float = 0.05,
        generation_frequency_days: int = 7,
        improvement_target: float = 0.05,
        stagnation_threshold: int = 3
    ):
        self.population_size = population_size
        self.fitness_weights = fitness_weights or FitnessWeights()
        self.generation_frequency_days = generation_frequency_days
        self.improvement_target = improvement_target
        self.stagnation_threshold = stagnation_threshold

        # Operators
        self.fitness_evaluator = FitnessEvaluator(self.fitness_weights)
        self.selection_operator = SelectionOperator(
            method=selection_method,
            elite_percentage=elite_percentage
        )
        self.crossover_operator = CrossoverOperator(probability=crossover_probability)
        self.mutation_operator = MutationOperator(probability=mutation_probability)

        # State
        self.current_generation: Optional[Generation] = None
        self.generation_history: List[Generation] = []
        self.evolution_metrics = EvolutionMetrics()

        logger.info(
            "Evolution Engine initialized",
            population_size=population_size,
            selection_method=selection_method.value
        )

    async def initialize_population(self) -> Generation:
        """Initialize first generation with random agents"""
        logger.info("Initializing population", size=self.population_size)

        population = []
        strategies = [
            "breadth_first_search",
            "depth_first_search",
            "hypothesis_driven",
            "evidence_driven"
        ]

        for i in range(self.population_size):
            agent_id = f"agent_{i:04d}_gen0"

            genome = AgentGenome(
                agent_id=agent_id,
                generation=0,
                parameters={
                    "learning_rate": random.uniform(0.001, 0.1),
                    "exploration_factor": random.uniform(0.1, 0.3),
                    "confidence_threshold": random.uniform(0.5, 0.9),
                    "max_depth": random.randint(3, 10),
                    "beam_width": random.randint(5, 20)
                },
                strategy=random.choice(strategies),
                metrics=FitnessMetrics(
                    accuracy=random.uniform(0.3, 0.7),
                    speed=random.uniform(500, 2000),
                    novelty=random.uniform(0.2, 0.6),
                    actionability=random.uniform(0.2, 0.5),
                    cost_efficiency=random.uniform(0.3, 0.8)
                )
            )

            population.append(genome)

        # Evaluate initial fitness
        population = await self.fitness_evaluator.evaluate_population(population)

        generation = Generation(
            generation_number=0,
            population=population,
            average_fitness=sum(g.fitness_score for g in population) / len(population),
            best_fitness=population[0].fitness_score,
            best_agent_id=population[0].agent_id,
            diversity_score=await self._calculate_diversity(population)
        )

        self.current_generation = generation
        self.generation_history.append(generation)

        logger.info(
            "Population initialized",
            average_fitness=generation.average_fitness,
            best_fitness=generation.best_fitness
        )

        return generation

    async def evolve(self) -> Generation:
        """Run one generation of evolution"""
        if self.current_generation is None:
            await self.initialize_population()

        logger.info(
            "Starting evolution",
            generation=self.current_generation.generation_number + 1
        )

        population = self.current_generation.population
        new_generation_number = self.current_generation.generation_number + 1

        # Calculate elite count
        elite_count = int(len(population) * self.selection_operator.elite_percentage)
        offspring_count = len(population) - elite_count

        # Keep elite agents
        sorted_population = sorted(population, key=lambda g: g.fitness_score, reverse=True)
        elite = sorted_population[:elite_count]

        # Update elite for new generation
        for agent in elite:
            agent.generation = new_generation_number

        # Select parents for reproduction
        parents = await self.selection_operator.select(
            population,
            offspring_count * 2  # Need 2 parents per offspring
        )

        # Create offspring through crossover
        offspring = []
        for i in range(0, len(parents) - 1, 2):
            child = await self.crossover_operator.crossover(
                parents[i],
                parents[i + 1],
                new_generation_number
            )
            offspring.append(child)

            self.evolution_metrics.total_crossovers += 1

        # Apply mutations
        mutated_offspring = []
        for child in offspring:
            mutated = await self.mutation_operator.mutate(child)
            mutated_offspring.append(mutated)

            if mutated.mutations:
                self.evolution_metrics.total_mutations += 1

        # Combine elite and offspring
        new_population = elite + mutated_offspring[:offspring_count]

        # Simulate fitness (in real system, this would come from actual performance)
        for genome in new_population:
            if genome not in elite:
                # Simulate slight improvement from parents
                parent_fitness = sum(
                    p.fitness_score for p in population
                    if p.agent_id in genome.parent_ids
                ) / max(1, len(genome.parent_ids))

                # Add some variance
                genome.metrics = FitnessMetrics(
                    accuracy=min(1.0, parent_fitness + random.gauss(0.02, 0.05)),
                    speed=max(100, random.gauss(800, 200)),
                    novelty=random.uniform(0.2, 0.7),
                    actionability=random.uniform(0.3, 0.6),
                    cost_efficiency=random.uniform(0.4, 0.9)
                )

        # Evaluate new population
        new_population = await self.fitness_evaluator.evaluate_population(new_population)

        # Create new generation
        new_generation = Generation(
            generation_number=new_generation_number,
            population=new_population,
            average_fitness=sum(g.fitness_score for g in new_population) / len(new_population),
            best_fitness=new_population[0].fitness_score,
            best_agent_id=new_population[0].agent_id,
            diversity_score=await self._calculate_diversity(new_population)
        )

        # Track improvement
        improvement = (new_generation.average_fitness - self.current_generation.average_fitness) / max(0.001, self.current_generation.average_fitness)

        if improvement < self.improvement_target:
            self.evolution_metrics.stagnation_count += 1
        else:
            self.evolution_metrics.stagnation_count = 0

        self.evolution_metrics.improvement_rate = improvement
        self.evolution_metrics.generations_completed = new_generation_number

        if new_generation.best_fitness > self.evolution_metrics.best_fitness_ever:
            self.evolution_metrics.best_fitness_ever = new_generation.best_fitness
            self.evolution_metrics.best_agent_ever = new_generation.best_agent_id

        # Update state
        self.current_generation = new_generation
        self.generation_history.append(new_generation)

        logger.info(
            "Evolution completed",
            generation=new_generation_number,
            average_fitness=new_generation.average_fitness,
            best_fitness=new_generation.best_fitness,
            improvement=f"{improvement:.2%}"
        )

        return new_generation

    async def _calculate_diversity(self, population: List[AgentGenome]) -> float:
        """Calculate genetic diversity in population"""
        if len(population) < 2:
            return 0.0

        # Strategy diversity
        strategies = set(g.strategy for g in population)
        strategy_diversity = len(strategies) / len(population)

        # Parameter diversity (using variance)
        param_keys = set()
        for g in population:
            param_keys.update(g.parameters.keys())

        param_diversity = 0
        for key in param_keys:
            values = [g.parameters.get(key, 0) for g in population if isinstance(g.parameters.get(key), (int, float))]
            if values:
                mean = sum(values) / len(values)
                variance = sum((v - mean) ** 2 for v in values) / len(values)
                param_diversity += min(1.0, variance)

        param_diversity /= max(1, len(param_keys))

        return (strategy_diversity + param_diversity) / 2

    async def get_top_agents(self, n: int = 10) -> List[AgentGenome]:
        """Get top performing agents"""
        if self.current_generation is None:
            return []

        sorted_pop = sorted(
            self.current_generation.population,
            key=lambda g: g.fitness_score,
            reverse=True
        )
        return sorted_pop[:n]

    async def get_bottom_agents(self, n: int = 10) -> List[AgentGenome]:
        """Get worst performing agents (for replacement)"""
        if self.current_generation is None:
            return []

        sorted_pop = sorted(
            self.current_generation.population,
            key=lambda g: g.fitness_score
        )
        return sorted_pop[:n]

    async def check_stagnation(self) -> bool:
        """Check if evolution has stagnated"""
        return self.evolution_metrics.stagnation_count >= self.stagnation_threshold

    async def get_evolution_status(self) -> Dict[str, Any]:
        """Get current evolution status"""
        return {
            "current_generation": self.current_generation.generation_number if self.current_generation else 0,
            "population_size": len(self.current_generation.population) if self.current_generation else 0,
            "average_fitness": self.current_generation.average_fitness if self.current_generation else 0,
            "best_fitness": self.current_generation.best_fitness if self.current_generation else 0,
            "best_agent": self.current_generation.best_agent_id if self.current_generation else None,
            "diversity": self.current_generation.diversity_score if self.current_generation else 0,
            "improvement_rate": self.evolution_metrics.improvement_rate,
            "stagnation_count": self.evolution_metrics.stagnation_count,
            "total_mutations": self.evolution_metrics.total_mutations,
            "total_crossovers": self.evolution_metrics.total_crossovers,
            "best_fitness_ever": self.evolution_metrics.best_fitness_ever,
            "best_agent_ever": self.evolution_metrics.best_agent_ever
        }


# Factory function
async def create_evolution_engine(config_path: str) -> EvolutionEngine:
    """Create Evolution Engine from YAML config"""
    import yaml

    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    layer_4_config = config.get("core_architecture", {}).get("refinery_layers", {}).get("layer_4_evolution_engine", {})

    # Parse fitness weights
    fitness_config = layer_4_config.get("fitness_function", {}).get("metrics", {})
    fitness_weights = FitnessWeights(
        accuracy=fitness_config.get("accuracy", {}).get("weight", 0.40),
        speed=fitness_config.get("speed", {}).get("weight", 0.20),
        novelty=fitness_config.get("novelty", {}).get("weight", 0.20),
        actionability=fitness_config.get("actionability", {}).get("weight", 0.15),
        cost_efficiency=fitness_config.get("cost_efficiency", {}).get("weight", 0.05)
    )

    # Parse genetic operations
    genetic_config = layer_4_config.get("genetic_operations", {})
    selection_config = genetic_config.get("selection", {})
    crossover_config = genetic_config.get("crossover", {})
    mutation_config = genetic_config.get("mutation", {})

    # Parse generation config
    generations_config = layer_4_config.get("generations", {})

    # Parse frequency (e.g., "7d" -> 7) with proper validation
    frequency_str = str(generations_config.get("frequency", "7d"))
    import re
    frequency_match = re.match(r'^(\d+)d$', frequency_str)
    if frequency_match:
        frequency_days = int(frequency_match.group(1))
    else:
        # Default to 7 days if format is unexpected
        logger.warning("Invalid frequency format, defaulting to 7 days", frequency=frequency_str)
        frequency_days = 7

    engine = EvolutionEngine(
        population_size=generations_config.get("population_size", 640),
        fitness_weights=fitness_weights,
        selection_method=SelectionMethod(selection_config.get("method", "tournament")),
        elite_percentage=selection_config.get("elite_percentage", 0.10),
        crossover_probability=crossover_config.get("probability", 0.70),
        mutation_probability=mutation_config.get("probability", 0.05),
        generation_frequency_days=frequency_days,
        improvement_target=generations_config.get("improvement_target", 0.05),
        stagnation_threshold=generations_config.get("stagnation_threshold", 3)
    )

    return engine

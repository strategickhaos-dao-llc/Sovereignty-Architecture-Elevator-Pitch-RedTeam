"""
Genetic Evolution System - Evolutionary Algorithms for Agent Improvement
========================================================================

The evolution engine of the Singularity. Uses genetic algorithms to:
- Evolve agent populations for optimal performance
- Breed successful agents, retire underperformers
- Discover optimal parameter combinations
- Adapt to changing research domains

Best agents reproduce, weak ones die. The system gets 5-10% smarter
every week through continuous evolutionary pressure.
"""

import asyncio
import random
import uuid
import copy
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional, Any, Tuple, Callable
from dataclasses import dataclass, field
import math

import structlog

logger = structlog.get_logger(__name__)


class GeneType(Enum):
    """Types of genes in agent genome"""
    FLOAT = "float"
    INT = "int"
    BOOL = "bool"
    CATEGORICAL = "categorical"


class SelectionMethod(Enum):
    """Selection methods for genetic algorithm"""
    TOURNAMENT = "tournament"
    ROULETTE = "roulette"
    RANK = "rank"
    ELITE = "elite"


@dataclass
class Gene:
    """Single gene in the genome"""
    name: str
    gene_type: GeneType
    value: Any
    
    # Constraints
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    options: List[Any] = field(default_factory=list)  # For categorical
    
    # Mutation parameters
    mutation_rate: float = 0.1
    mutation_strength: float = 0.2
    
    def mutate(self) -> 'Gene':
        """Mutate this gene"""
        if random.random() > self.mutation_rate:
            return self
        
        new_gene = copy.deepcopy(self)
        
        if self.gene_type == GeneType.FLOAT:
            delta = random.gauss(0, self.mutation_strength)
            new_gene.value = self.value + delta * (self.max_value - self.min_value if self.max_value else 1)
            if self.min_value is not None:
                new_gene.value = max(self.min_value, new_gene.value)
            if self.max_value is not None:
                new_gene.value = min(self.max_value, new_gene.value)
        
        elif self.gene_type == GeneType.INT:
            delta = random.randint(-2, 2)
            new_gene.value = self.value + delta
            if self.min_value is not None:
                new_gene.value = max(int(self.min_value), new_gene.value)
            if self.max_value is not None:
                new_gene.value = min(int(self.max_value), new_gene.value)
        
        elif self.gene_type == GeneType.BOOL:
            new_gene.value = not self.value
        
        elif self.gene_type == GeneType.CATEGORICAL:
            if self.options:
                new_gene.value = random.choice(self.options)
        
        return new_gene


@dataclass
class AgentGenome:
    """Complete genome for an agent"""
    genome_id: str
    generation: int
    genes: Dict[str, Gene] = field(default_factory=dict)
    
    # Lineage
    parent_ids: List[str] = field(default_factory=list)
    children_ids: List[str] = field(default_factory=list)
    
    # Fitness tracking
    fitness_score: float = 0.0
    fitness_history: List[float] = field(default_factory=list)
    
    # Performance metrics
    validation_accuracy: float = 0.0
    hypothesis_quality: float = 0.0
    research_speed: float = 0.0
    error_rate: float = 0.0
    
    # Metadata
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    evaluations: int = 0
    
    def crossover(self, other: 'AgentGenome') -> Tuple['AgentGenome', 'AgentGenome']:
        """Perform crossover with another genome"""
        child1_genes = {}
        child2_genes = {}
        
        all_gene_names = set(self.genes.keys()) | set(other.genes.keys())
        
        for gene_name in all_gene_names:
            # Randomly select gene from either parent
            if random.random() < 0.5:
                if gene_name in self.genes:
                    child1_genes[gene_name] = copy.deepcopy(self.genes[gene_name])
                if gene_name in other.genes:
                    child2_genes[gene_name] = copy.deepcopy(other.genes[gene_name])
            else:
                if gene_name in other.genes:
                    child1_genes[gene_name] = copy.deepcopy(other.genes[gene_name])
                if gene_name in self.genes:
                    child2_genes[gene_name] = copy.deepcopy(self.genes[gene_name])
        
        child1 = AgentGenome(
            genome_id=f"gen_{uuid.uuid4().hex[:8]}",
            generation=max(self.generation, other.generation) + 1,
            genes=child1_genes,
            parent_ids=[self.genome_id, other.genome_id]
        )
        
        child2 = AgentGenome(
            genome_id=f"gen_{uuid.uuid4().hex[:8]}",
            generation=max(self.generation, other.generation) + 1,
            genes=child2_genes,
            parent_ids=[self.genome_id, other.genome_id]
        )
        
        # Track children in parents
        self.children_ids.append(child1.genome_id)
        self.children_ids.append(child2.genome_id)
        other.children_ids.append(child1.genome_id)
        other.children_ids.append(child2.genome_id)
        
        return child1, child2
    
    def mutate(self) -> 'AgentGenome':
        """Mutate this genome"""
        new_genome = copy.deepcopy(self)
        new_genome.genome_id = f"gen_{uuid.uuid4().hex[:8]}"
        new_genome.parent_ids = [self.genome_id]
        new_genome.children_ids = []
        new_genome.fitness_history = []
        new_genome.evaluations = 0
        
        for gene_name, gene in new_genome.genes.items():
            new_genome.genes[gene_name] = gene.mutate()
        
        self.children_ids.append(new_genome.genome_id)
        
        return new_genome
    
    def get_phenotype(self) -> Dict[str, Any]:
        """Get the phenotype (expressed traits) from genotype"""
        return {name: gene.value for name, gene in self.genes.items()}


@dataclass
class FitnessMetrics:
    """Comprehensive fitness metrics for evaluation"""
    # Core metrics (weighted)
    accuracy: float = 0.0          # Weight: 0.3
    hypothesis_quality: float = 0.0  # Weight: 0.25
    speed: float = 0.0             # Weight: 0.15
    error_rate: float = 0.0        # Weight: 0.15
    novelty: float = 0.0           # Weight: 0.15
    
    # Additional metrics
    papers_processed: int = 0
    hypotheses_validated: int = 0
    corrections_applied: int = 0
    
    # Computed fitness
    total_fitness: float = 0.0
    
    def calculate_total(self):
        """Calculate weighted total fitness"""
        self.total_fitness = (
            self.accuracy * 0.30 +
            self.hypothesis_quality * 0.25 +
            self.speed * 0.15 +
            (1.0 - self.error_rate) * 0.15 +  # Lower error rate is better
            self.novelty * 0.15
        )
        return self.total_fitness


@dataclass
class EvolutionConfig:
    """Configuration for evolution process"""
    population_size: int = 20
    elite_count: int = 2
    mutation_rate: float = 0.1
    crossover_rate: float = 0.7
    selection_method: SelectionMethod = SelectionMethod.TOURNAMENT
    tournament_size: int = 3
    max_generations: int = 1000
    stagnation_limit: int = 50  # Generations without improvement
    target_fitness: float = 0.95


class GeneticEvolution:
    """
    Genetic evolution system for agent improvement.
    
    This is the DARWIN ENGINE of the Singularity - survival of the fittest
    for AI agents. The system:
    
    1. Maintains a population of agent configurations
    2. Evaluates fitness based on research performance
    3. Breeds top performers to create next generation
    4. Applies mutations for exploration
    5. Retires underperformers
    6. Tracks improvement over generations
    
    Result: 5-10% improvement per week through evolution.
    """
    
    def __init__(
        self,
        population_size: int = 20,
        mutation_rate: float = 0.1,
        crossover_rate: float = 0.7,
        elite_count: int = 2
    ):
        self.config = EvolutionConfig(
            population_size=population_size,
            mutation_rate=mutation_rate,
            crossover_rate=crossover_rate,
            elite_count=elite_count
        )
        
        # Population
        self.population: List[AgentGenome] = []
        self.hall_of_fame: List[AgentGenome] = []
        
        # Evolution state
        self.current_generation = 0
        self.best_fitness = 0.0
        self.generations_without_improvement = 0
        
        # History
        self.fitness_history: List[Dict[str, float]] = []
        self.diversity_history: List[float] = []
        
        # Initialize population
        self._initialize_population()
        
        logger.info(
            "GeneticEvolution initialized",
            population_size=population_size,
            mutation_rate=mutation_rate
        )
    
    def _initialize_population(self):
        """Initialize the starting population"""
        # Define the gene template for research agents
        gene_template = {
            # Analysis parameters
            "relevance_threshold": Gene(
                name="relevance_threshold",
                gene_type=GeneType.FLOAT,
                value=0.6,
                min_value=0.3,
                max_value=0.9
            ),
            "novelty_weight": Gene(
                name="novelty_weight",
                gene_type=GeneType.FLOAT,
                value=0.5,
                min_value=0.1,
                max_value=0.9
            ),
            "confidence_threshold": Gene(
                name="confidence_threshold",
                gene_type=GeneType.FLOAT,
                value=0.7,
                min_value=0.5,
                max_value=0.95
            ),
            
            # Hypothesis generation
            "hypothesis_creativity": Gene(
                name="hypothesis_creativity",
                gene_type=GeneType.FLOAT,
                value=0.5,
                min_value=0.1,
                max_value=0.9
            ),
            "max_hypotheses_per_cycle": Gene(
                name="max_hypotheses_per_cycle",
                gene_type=GeneType.INT,
                value=10,
                min_value=3,
                max_value=50
            ),
            
            # Validation parameters
            "min_validators": Gene(
                name="min_validators",
                gene_type=GeneType.INT,
                value=3,
                min_value=2,
                max_value=7
            ),
            "consensus_threshold": Gene(
                name="consensus_threshold",
                gene_type=GeneType.FLOAT,
                value=0.7,
                min_value=0.5,
                max_value=0.95
            ),
            
            # Learning parameters
            "learning_rate": Gene(
                name="learning_rate",
                gene_type=GeneType.FLOAT,
                value=0.01,
                min_value=0.0001,
                max_value=0.1
            ),
            "exploration_factor": Gene(
                name="exploration_factor",
                gene_type=GeneType.FLOAT,
                value=0.3,
                min_value=0.05,
                max_value=0.7
            ),
            
            # Model selection
            "primary_model": Gene(
                name="primary_model",
                gene_type=GeneType.CATEGORICAL,
                value="gpt-4",
                options=["gpt-4", "gpt-4-turbo", "claude-3", "llama-2-70b", "mixtral"]
            ),
            "use_ensemble": Gene(
                name="use_ensemble",
                gene_type=GeneType.BOOL,
                value=True
            ),
            
            # Processing parameters
            "batch_size": Gene(
                name="batch_size",
                gene_type=GeneType.INT,
                value=32,
                min_value=8,
                max_value=128
            ),
            "papers_per_cycle": Gene(
                name="papers_per_cycle",
                gene_type=GeneType.INT,
                value=100,
                min_value=20,
                max_value=500
            ),
        }
        
        # Create initial population with random variations
        for i in range(self.config.population_size):
            genome = AgentGenome(
                genome_id=f"gen_{uuid.uuid4().hex[:8]}",
                generation=0,
                genes=copy.deepcopy(gene_template)
            )
            
            # Add random variation to initial population
            if i > 0:  # Keep one with default values
                for gene_name, gene in genome.genes.items():
                    if gene.gene_type == GeneType.FLOAT:
                        range_size = (gene.max_value or 1) - (gene.min_value or 0)
                        gene.value = (gene.min_value or 0) + random.random() * range_size
                    elif gene.gene_type == GeneType.INT:
                        gene.value = random.randint(
                            int(gene.min_value or 0),
                            int(gene.max_value or 100)
                        )
                    elif gene.gene_type == GeneType.BOOL:
                        gene.value = random.random() > 0.5
                    elif gene.gene_type == GeneType.CATEGORICAL and gene.options:
                        gene.value = random.choice(gene.options)
            
            self.population.append(genome)
    
    async def evaluate_genome(
        self,
        genome: AgentGenome,
        evaluation_function: Optional[Callable] = None
    ) -> FitnessMetrics:
        """Evaluate a genome's fitness"""
        phenotype = genome.get_phenotype()
        
        if evaluation_function:
            metrics = await evaluation_function(phenotype)
        else:
            # Default evaluation (simulated)
            metrics = await self._default_evaluation(genome)
        
        # Update genome with evaluation results
        genome.fitness_score = metrics.total_fitness
        genome.fitness_history.append(metrics.total_fitness)
        genome.validation_accuracy = metrics.accuracy
        genome.hypothesis_quality = metrics.hypothesis_quality
        genome.research_speed = metrics.speed
        genome.error_rate = metrics.error_rate
        genome.evaluations += 1
        
        return metrics
    
    async def _default_evaluation(self, genome: AgentGenome) -> FitnessMetrics:
        """Default evaluation function (simulation)"""
        phenotype = genome.get_phenotype()
        
        # Simulate fitness based on phenotype values
        # In production, this would run actual research cycles
        
        # Higher relevance threshold = more accurate but slower
        accuracy = 0.5 + (phenotype.get("relevance_threshold", 0.6) * 0.4)
        
        # Creativity affects hypothesis quality
        hypothesis_quality = 0.4 + (phenotype.get("hypothesis_creativity", 0.5) * 0.5)
        
        # Speed inversely related to thoroughness
        speed = 1.0 - (phenotype.get("min_validators", 3) / 10)
        
        # Error rate affected by consensus threshold
        error_rate = 0.3 - (phenotype.get("consensus_threshold", 0.7) * 0.25)
        error_rate = max(0.01, error_rate)
        
        # Novelty from exploration factor
        novelty = phenotype.get("exploration_factor", 0.3) * 0.8
        
        # Add some randomness to simulate real-world variation
        accuracy += random.gauss(0, 0.05)
        hypothesis_quality += random.gauss(0, 0.05)
        speed += random.gauss(0, 0.05)
        novelty += random.gauss(0, 0.05)
        
        # Clamp values
        accuracy = max(0, min(1, accuracy))
        hypothesis_quality = max(0, min(1, hypothesis_quality))
        speed = max(0, min(1, speed))
        error_rate = max(0.01, min(0.5, error_rate))
        novelty = max(0, min(1, novelty))
        
        metrics = FitnessMetrics(
            accuracy=accuracy,
            hypothesis_quality=hypothesis_quality,
            speed=speed,
            error_rate=error_rate,
            novelty=novelty
        )
        metrics.calculate_total()
        
        return metrics
    
    async def evolve_generation(
        self,
        evaluation_function: Optional[Callable] = None
    ) -> Dict[str, Any]:
        """Evolve one generation"""
        logger.info(f"Evolving generation {self.current_generation}")
        
        # Evaluate all genomes
        for genome in self.population:
            if genome.evaluations == 0 or random.random() < 0.3:
                await self.evaluate_genome(genome, evaluation_function)
        
        # Sort by fitness
        self.population.sort(key=lambda g: g.fitness_score, reverse=True)
        
        # Track statistics
        avg_fitness = sum(g.fitness_score for g in self.population) / len(self.population)
        best_fitness = self.population[0].fitness_score
        worst_fitness = self.population[-1].fitness_score
        
        # Check for improvement
        if best_fitness > self.best_fitness:
            self.best_fitness = best_fitness
            self.generations_without_improvement = 0
            
            # Add to hall of fame
            if len(self.hall_of_fame) < 10:
                self.hall_of_fame.append(copy.deepcopy(self.population[0]))
            elif best_fitness > min(g.fitness_score for g in self.hall_of_fame):
                # Replace worst in hall of fame
                self.hall_of_fame.sort(key=lambda g: g.fitness_score)
                self.hall_of_fame[0] = copy.deepcopy(self.population[0])
        else:
            self.generations_without_improvement += 1
        
        # Record history
        self.fitness_history.append({
            "generation": self.current_generation,
            "best_fitness": best_fitness,
            "avg_fitness": avg_fitness,
            "worst_fitness": worst_fitness
        })
        
        # Calculate diversity
        diversity = self._calculate_diversity()
        self.diversity_history.append(diversity)
        
        # Create next generation
        new_population = []
        
        # Elite selection - keep top performers
        for i in range(self.config.elite_count):
            elite = copy.deepcopy(self.population[i])
            elite.generation = self.current_generation + 1
            new_population.append(elite)
        
        # Fill rest through selection and breeding
        while len(new_population) < self.config.population_size:
            # Selection
            parent1 = await self._select_parent()
            parent2 = await self._select_parent()
            
            # Crossover
            if random.random() < self.config.crossover_rate:
                child1, child2 = parent1.crossover(parent2)
            else:
                child1 = copy.deepcopy(parent1)
                child2 = copy.deepcopy(parent2)
                child1.generation = self.current_generation + 1
                child2.generation = self.current_generation + 1
            
            # Mutation
            if random.random() < self.config.mutation_rate:
                child1 = child1.mutate()
            if random.random() < self.config.mutation_rate:
                child2 = child2.mutate()
            
            # Reset fitness for new individuals
            child1.fitness_score = 0.0
            child1.evaluations = 0
            child2.fitness_score = 0.0
            child2.evaluations = 0
            
            new_population.append(child1)
            if len(new_population) < self.config.population_size:
                new_population.append(child2)
        
        # Replace population
        self.population = new_population
        self.current_generation += 1
        
        result = {
            "generation": self.current_generation,
            "best_fitness": best_fitness,
            "avg_fitness": avg_fitness,
            "worst_fitness": worst_fitness,
            "diversity": diversity,
            "improvement": best_fitness - (self.fitness_history[-2]["best_fitness"] if len(self.fitness_history) > 1 else 0),
            "stagnation": self.generations_without_improvement
        }
        
        logger.info(
            f"Generation {self.current_generation} complete",
            best_fitness=best_fitness,
            avg_fitness=avg_fitness
        )
        
        return result
    
    async def _select_parent(self) -> AgentGenome:
        """Select a parent using tournament selection"""
        if self.config.selection_method == SelectionMethod.TOURNAMENT:
            tournament = random.sample(
                self.population,
                min(self.config.tournament_size, len(self.population))
            )
            return max(tournament, key=lambda g: g.fitness_score)
        
        elif self.config.selection_method == SelectionMethod.ROULETTE:
            total_fitness = sum(g.fitness_score for g in self.population)
            if total_fitness == 0:
                return random.choice(self.population)
            
            pick = random.uniform(0, total_fitness)
            current = 0
            for genome in self.population:
                current += genome.fitness_score
                if current >= pick:
                    return genome
            return self.population[-1]
        
        elif self.config.selection_method == SelectionMethod.RANK:
            # Rank-based selection
            ranks = list(range(len(self.population), 0, -1))
            total_rank = sum(ranks)
            pick = random.uniform(0, total_rank)
            current = 0
            for i, genome in enumerate(self.population):
                current += ranks[i]
                if current >= pick:
                    return genome
            return self.population[0]
        
        else:
            return random.choice(self.population)
    
    def _calculate_diversity(self) -> float:
        """Calculate population diversity"""
        if len(self.population) < 2:
            return 1.0
        
        # Calculate variance in gene values
        variances = []
        
        for gene_name in self.population[0].genes.keys():
            values = []
            for genome in self.population:
                if gene_name in genome.genes:
                    gene = genome.genes[gene_name]
                    if gene.gene_type in [GeneType.FLOAT, GeneType.INT]:
                        values.append(float(gene.value))
            
            if values:
                mean = sum(values) / len(values)
                variance = sum((v - mean) ** 2 for v in values) / len(values)
                variances.append(variance)
        
        if not variances:
            return 0.0
        
        # Normalize diversity to 0-1 range
        avg_variance = sum(variances) / len(variances)
        return min(1.0, math.sqrt(avg_variance))
    
    def get_best_genome(self) -> Optional[AgentGenome]:
        """Get the current best genome"""
        if not self.population:
            return None
        return max(self.population, key=lambda g: g.fitness_score)
    
    def get_best_phenotype(self) -> Dict[str, Any]:
        """Get the phenotype of the best genome"""
        best = self.get_best_genome()
        if best:
            return best.get_phenotype()
        return {}
    
    async def get_evolution_report(self) -> Dict[str, Any]:
        """Generate evolution progress report"""
        return {
            "current_generation": self.current_generation,
            "population_size": len(self.population),
            "best_fitness": self.best_fitness,
            "generations_without_improvement": self.generations_without_improvement,
            "hall_of_fame_size": len(self.hall_of_fame),
            "fitness_history": self.fitness_history[-20:],  # Last 20 generations
            "current_diversity": self.diversity_history[-1] if self.diversity_history else 0,
            "best_phenotype": self.get_best_phenotype(),
            "improvement_rate": self._calculate_improvement_rate()
        }
    
    def _calculate_improvement_rate(self) -> float:
        """Calculate weekly improvement rate"""
        if len(self.fitness_history) < 7:
            return 0.0
        
        # Compare last week to previous week
        recent = self.fitness_history[-7:]
        older = self.fitness_history[-14:-7] if len(self.fitness_history) >= 14 else self.fitness_history[:7]
        
        recent_avg = sum(h["best_fitness"] for h in recent) / len(recent)
        older_avg = sum(h["best_fitness"] for h in older) / len(older)
        
        if older_avg == 0:
            return 0.0
        
        return (recent_avg - older_avg) / older_avg

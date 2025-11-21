#!/usr/bin/env python3
"""
Nuclear Evolution Engine - All Level 10 Features Enabled
Self-Evolving AI with Maximum Evolution Power

This is the FULL POWER version with:
- Judge-based fitness evaluation
- Sexual reproduction via genetic crossover
- Lamarckian self-modification
- Progressive task curriculum
- Complete lineage tracking
"""

import json
import random
from datetime import datetime
from pathlib import Path
import httpx
import asyncio

from evolution_engine import Heir, EvolutionEngine
from level10_fitness import JudgeFitness
from crossover import GeneticCrossover
from lamarckian import LamarckianEvolution
from task_curriculum import TaskCurriculum
from lineage import LineageTracker

# Nuclear evolution ledger
NUCLEAR_LOG = Path("nuclear_evolution_ledger.jsonl")
NUCLEAR_POPULATION = Path("nuclear_population.json")
NUCLEAR_LINEAGE = Path("nuclear_lineage_state.json")

class NuclearEvolutionEngine:
    """
    The complete evolution engine with all Level 10 upgrades
    
    This is what happens when you combine:
    - Natural selection
    - Sexual reproduction
    - Self-modification
    - Progressive curriculum
    - Bloodline tracking
    
    The result: Digital Darwinism at full power
    """
    
    def __init__(self, 
                 population_size: int = 20,
                 judge_model: str = "qwen2.5:72b",
                 enable_lamarckian: bool = True,
                 enable_crossover: bool = True,
                 lamarckian_frequency: int = 5):
        
        self.population_size = population_size
        self.population = []
        self.generation = 0
        
        # Level 10 components
        self.judge = JudgeFitness(judge_model=judge_model)
        self.lamarckian = LamarckianEvolution(model=judge_model)
        self.curriculum = TaskCurriculum()
        self.lineage = LineageTracker()
        
        # Configuration
        self.enable_lamarckian = enable_lamarckian
        self.enable_crossover = enable_crossover
        self.lamarckian_frequency = lamarckian_frequency
        
        print(f"🚀 Nuclear Evolution Engine initialized")
        print(f"   Population: {population_size}")
        print(f"   Judge model: {judge_model}")
        print(f"   Crossover: {'ENABLED' if enable_crossover else 'DISABLED'}")
        print(f"   Lamarckian: {'ENABLED' if enable_lamarckian else 'DISABLED'}")
    
    def initialize_population(self):
        """Create first generation with diverse, high-quality prompts"""
        
        base_prompts = [
            "You are a tactical analyst. Be direct, actionable, and precise. Focus on practical solutions.",
            "You are a creative problem solver. Think laterally, explore unconventional approaches, embrace novel ideas.",
            "You are a cautious evaluator. Consider all risks, anticipate failures, validate assumptions thoroughly.",
            "You are an aggressive optimizer. Push boundaries, maximize efficiency, eliminate waste ruthlessly.",
            "You are a detail-oriented researcher. Be thorough, cite sources, provide comprehensive analysis.",
            "You are a strategic thinker. See patterns, identify leverage points, plan multiple moves ahead.",
            "You are a systems architect. Think in abstractions, design for scale, ensure coherence.",
            "You are a rapid prototyper. Move fast, iterate quickly, learn from failures, ship early.",
        ]
        
        self.population = []
        
        # Create diverse initial population
        for prompt in base_prompts:
            for temp in [0.5, 0.7, 0.9]:
                heir = Heir(prompt, temp, generation=0)
                self.population.append(heir)
                self.lineage.register_heir(heir.id, None)
        
        # Trim to population size if needed
        self.population = self.population[:self.population_size]
        
        print(f"✅ Initialized nuclear population: {len(self.population)} heirs")
    
    async def get_heir_response(self, heir: Heir, task: str) -> str:
        """Get heir's response to a task"""
        async with httpx.AsyncClient(timeout=90.0) as client:
            try:
                resp = await client.post(
                    "http://localhost:11434/api/generate",
                    json={
                        "model": "qwen2.5:72b",
                        "prompt": f"{heir.system_prompt}\n\nTask: {task}",
                        "temperature": heir.temperature,
                        "stream": False
                    }
                )
                return resp.json().get("response", "")
            except Exception as e:
                print(f"❌ Error getting response from {heir.id}: {e}")
                return ""
    
    async def evaluate_heir(self, heir: Heir, task: str) -> float:
        """Evaluate heir using judge model (Level 10)"""
        
        # Get heir's response
        response = await self.get_heir_response(heir, task)
        
        if not response:
            return 0.0
        
        # Use judge to evaluate
        fitness = await self.judge.evaluate_with_judge(response, task)
        
        return fitness
    
    async def run_generation(self):
        """Run a generation with Level 10 features"""
        
        self.generation += 1
        print(f"\n🧬 Generation {self.generation}")
        
        # Get curriculum-appropriate tasks
        curriculum_info = self.curriculum.get_curriculum_info(self.generation)
        tasks = self.curriculum.get_mixed_difficulty_tasks(self.generation, count=5)
        
        print(f"   📚 Difficulty: {curriculum_info['difficulty']}/15 ({curriculum_info['progress_percent']:.0f}%)")
        print(f"   🎯 Task pool: {len(tasks)} tasks")
        
        # Evaluate each heir
        for heir in self.population:
            task = random.choice(tasks)
            fitness = await self.evaluate_heir(heir, task)
            
            # Update running average
            old_total = heir.fitness_score * heir.tasks_completed
            heir.tasks_completed += 1
            heir.fitness_score = (old_total + fitness) / heir.tasks_completed
            
            print(f"      {heir.id} (gen {heir.generation}): {heir.fitness_score:.3f}")
        
        # Log generation
        self.log_generation(curriculum_info)
    
    def selection_and_reproduction(self):
        """Natural selection + sexual reproduction (Level 10)"""
        
        # Sort by fitness
        self.population.sort(key=lambda h: h.fitness_score, reverse=True)
        
        # Top 50% survive
        cutoff = len(self.population) // 2
        survivors = self.population[:cutoff]
        culled = self.population[cutoff:]
        
        print(f"\n   🏆 Top performers:")
        for i, heir in enumerate(survivors[:3]):
            lineage_depth = self.lineage.get_generation_depth(heir.id)
            founder = self.lineage.get_founder(heir.id)
            print(f"      #{i+1}: {heir.id} - {heir.fitness_score:.3f} (lineage depth: {lineage_depth}, founder: {founder})")
        
        print(f"\n   💀 Culled: {len(culled)} heirs")
        
        # Create offspring
        offspring = []
        sexual_count = 0
        asexual_count = 0
        
        while len(survivors) + len(offspring) < self.population_size:
            if self.enable_crossover and len(survivors) >= 2 and random.random() < 0.7:
                # Sexual reproduction (70% of time)
                parent1, parent2 = random.sample(survivors, 2)
                child = GeneticCrossover.create_offspring(parent1, parent2, self.generation)
                
                # Register with lineage tracker
                self.lineage.register_heir(child.id, child.parent_id)
                
                offspring.append(child)
                sexual_count += 1
            else:
                # Asexual reproduction (30% of time or if crossover disabled)
                parent = random.choice(survivors)
                child = parent.mutate()
                
                # Register with lineage tracker
                self.lineage.register_heir(child.id, child.parent_id)
                
                offspring.append(child)
                asexual_count += 1
        
        self.population = survivors + offspring
        
        print(f"   🐣 Created: {len(offspring)} offspring")
        if self.enable_crossover:
            print(f"      - Sexual reproduction: {sexual_count} heirs")
            print(f"      - Asexual reproduction: {asexual_count} heirs")
        else:
            print(f"      - Asexual reproduction: {asexual_count} heirs")
    
    async def apply_lamarckian_evolution(self):
        """Apply Lamarckian self-modification to top performers"""
        
        if not self.enable_lamarckian:
            return
        
        if self.generation % self.lamarckian_frequency != 0:
            return
        
        print(f"\n   🧠 LAMARCKIAN EVOLUTION TRIGGERED (Gen {self.generation})")
        
        # Sort by fitness
        self.population.sort(key=lambda h: h.fitness_score, reverse=True)
        
        # Apply to top 20%
        top_count = max(1, len(self.population) // 5)
        top_heirs = self.population[:top_count]
        
        for heir in top_heirs:
            print(f"      Reflecting: {heir.id} (fitness: {heir.fitness_score:.3f})")
            success = await self.lamarckian.reflect_and_improve(heir)
            
            if not success:
                print(f"         ⚠️ Reflection failed, heir unchanged")
    
    def log_generation(self, curriculum_info):
        """Record generation statistics"""
        
        avg_fitness = sum(h.fitness_score for h in self.population) / len(self.population)
        best_fitness = max(h.fitness_score for h in self.population)
        best_heir = max(self.population, key=lambda h: h.fitness_score)
        
        # Lineage analysis
        convergence = self.lineage.analyze_convergence()
        diversity = self.lineage.get_bloodline_diversity()
        
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "generation": self.generation,
            "population_size": len(self.population),
            "avg_fitness": avg_fitness,
            "best_fitness": best_fitness,
            "fitness_std": self._calculate_std(self.population),
            "curriculum_difficulty": curriculum_info['difficulty'],
            "best_heir": {
                "id": best_heir.id,
                "fitness": best_heir.fitness_score,
                "generation": best_heir.generation,
                "lineage_depth": self.lineage.get_generation_depth(best_heir.id),
                "founder": self.lineage.get_founder(best_heir.id)
            },
            "lineage": {
                "unique_bloodlines": diversity['unique_bloodlines'],
                "diversity_ratio": diversity['diversity_ratio'],
                "converging": convergence['converging'],
                "dominant_bloodline": convergence.get('dominant_bloodline'),
                "dominance_percent": convergence.get('dominance_percent', 0)
            }
        }
        
        with open(NUCLEAR_LOG, 'a') as f:
            f.write(json.dumps(entry) + '\n')
    
    def _calculate_std(self, population):
        """Calculate standard deviation of fitness scores"""
        scores = [h.fitness_score for h in population]
        mean = sum(scores) / len(scores)
        variance = sum((s - mean) ** 2 for s in scores) / len(scores)
        return variance ** 0.5
    
    def save_state(self):
        """Save complete state to disk"""
        
        # Save population
        data = {
            "generation": self.generation,
            "population": [h.to_dict() for h in self.population]
        }
        
        with open(NUCLEAR_POPULATION, 'w') as f:
            json.dump(data, f, indent=2)
        
        # Save lineage
        self.lineage.save_state(NUCLEAR_LINEAGE)
    
    def load_state(self) -> bool:
        """Load state from disk"""
        
        if not NUCLEAR_POPULATION.exists():
            return False
        
        try:
            # Load population
            with open(NUCLEAR_POPULATION, 'r') as f:
                data = json.load(f)
            
            self.generation = data["generation"]
            self.population = [Heir.from_dict(h) for h in data["population"]]
            
            # Load lineage
            self.lineage.load_state(NUCLEAR_LINEAGE)
            
            print(f"✅ Loaded nuclear generation {self.generation} with {len(self.population)} heirs")
            return True
            
        except Exception as e:
            print(f"❌ Error loading state: {e}")
            return False
    
    def print_statistics(self):
        """Print comprehensive statistics"""
        
        print(f"\n{'='*60}")
        print(f"NUCLEAR EVOLUTION STATISTICS - Generation {self.generation}")
        print(f"{'='*60}")
        
        # Fitness stats
        scores = [h.fitness_score for h in self.population]
        print(f"\n📊 Fitness:")
        print(f"   Average: {sum(scores) / len(scores):.3f}")
        print(f"   Best: {max(scores):.3f}")
        print(f"   Worst: {min(scores):.3f}")
        print(f"   Std Dev: {self._calculate_std(self.population):.3f}")
        
        # Curriculum
        curriculum_info = self.curriculum.get_curriculum_info(self.generation)
        print(f"\n📚 Curriculum:")
        print(f"   Difficulty: {curriculum_info['difficulty']}/15")
        print(f"   Progress: {curriculum_info['progress_percent']:.0f}%")
        
        # Lineage
        convergence = self.lineage.analyze_convergence()
        diversity = self.lineage.get_bloodline_diversity()
        dominant = self.lineage.get_dominant_bloodlines(top_n=3)
        
        print(f"\n🧬 Lineage:")
        print(f"   Total heirs tracked: {diversity['total_heirs']}")
        print(f"   Unique bloodlines: {diversity['unique_bloodlines']}")
        print(f"   Diversity ratio: {diversity['diversity_ratio']:.2f}")
        print(f"   Converging: {'YES' if convergence['converging'] else 'NO'}")
        
        if convergence['dominant_bloodline']:
            print(f"\n   🏆 Dominant bloodlines:")
            for i, bloodline in enumerate(dominant):
                print(f"      #{i+1}: {bloodline['founder_id']} ({bloodline['descendants']} descendants)")
        
        print(f"\n{'='*60}\n")

async def evolve_nuclear(generations: int = None):
    """
    Run nuclear evolution
    
    Args:
        generations: Number of generations to run (None = forever)
    """
    
    engine = NuclearEvolutionEngine(
        population_size=20,
        judge_model="qwen2.5:72b",
        enable_lamarckian=True,
        enable_crossover=True,
        lamarckian_frequency=5
    )
    
    # Load existing or initialize
    if not engine.load_state():
        engine.initialize_population()
    
    print("\n🧬💥 NUCLEAR EVOLUTION ENGINE STARTED 💥🧬")
    print("All Level 10 features ENABLED")
    print("Press Ctrl+C to stop\n")
    
    try:
        gen_count = 0
        while True:
            # Run generation
            await engine.run_generation()
            
            # Selection and reproduction
            engine.selection_and_reproduction()
            
            # Apply Lamarckian evolution
            await engine.apply_lamarckian_evolution()
            
            # Save state
            engine.save_state()
            
            # Print stats every 5 generations
            if engine.generation % 5 == 0:
                engine.print_statistics()
            
            gen_count += 1
            if generations and gen_count >= generations:
                break
            
            # Brief pause
            await asyncio.sleep(5)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Nuclear evolution stopped")
        engine.print_statistics()
        engine.save_state()
        
        # Export final lineage graph
        engine.lineage.export_lineage_graph("nuclear_lineage_graph.json")
        print(f"📊 Lineage graph exported to nuclear_lineage_graph.json")

if __name__ == "__main__":
    import sys
    
    generations = None
    if len(sys.argv) > 1:
        try:
            generations = int(sys.argv[1])
            print(f"Running for {generations} generations")
        except ValueError:
            print("Usage: python evolution_nuclear.py [generations]")
            sys.exit(1)
    
    asyncio.run(evolve_nuclear(generations))

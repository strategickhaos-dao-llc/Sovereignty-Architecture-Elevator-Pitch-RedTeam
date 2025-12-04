#!/usr/bin/env python3
"""
Evolution Demo - Shows system working without Ollama
Simulates evolution with mock fitness scoring
"""

import json
import random
import asyncio
from pathlib import Path
from evolution_engine import EvolutionEngine, Heir
from task_curriculum import TaskCurriculum
from lineage import LineageTracker

class DemoEvolutionEngine(EvolutionEngine):
    """Demo version with simulated fitness"""
    
    def __init__(self, population_size=10):
        super().__init__(population_size)
        self.curriculum = TaskCurriculum()
        self.lineage = LineageTracker()
        
    async def evaluate_heir(self, heir: Heir, task: str) -> float:
        """Simulate fitness evaluation without API calls"""
        
        # Simulate processing time
        await asyncio.sleep(0.1)
        
        # Simulate fitness based on heir characteristics
        # Better heirs have:
        # - Balanced temperature (0.7-0.9)
        # - Longer prompts (more detailed)
        # - Higher generation (evolved longer)
        
        temp_score = 1.0 - abs(heir.temperature - 0.8) / 1.0
        prompt_score = min(len(heir.system_prompt) / 200, 1.0)
        evolution_score = min(heir.generation / 20, 0.5)
        
        # Add some randomness
        random_factor = random.uniform(0.8, 1.2)
        
        fitness = ((temp_score + prompt_score + evolution_score) / 2.5) * random_factor
        fitness = max(0.1, min(1.0, fitness))  # Clamp to valid range
        
        return fitness

async def run_demo_evolution(generations: int = 10):
    """Run a demo evolution for specified generations"""
    
    print("=" * 60)
    print("Neural Heir Evolution System - DEMO MODE")
    print("=" * 60)
    print()
    print("This demo simulates evolution without requiring Ollama.")
    print(f"Running {generations} generations...\n")
    
    # Clean up any existing demo files
    demo_ledger = Path("demo_ledger.jsonl")
    demo_pop = Path("demo_population.json")
    demo_ledger.unlink(missing_ok=True)
    demo_pop.unlink(missing_ok=True)
    
    # Create engine
    engine = DemoEvolutionEngine(population_size=10)
    engine.initialize_population()
    
    # Register initial heirs with lineage tracker
    for heir in engine.population:
        engine.lineage.register_heir(heir.id, None)
    
    print()
    
    # Run evolution
    for i in range(generations):
        # Get curriculum task
        task = engine.curriculum.get_task_for_generation(engine.generation)
        curriculum_info = engine.curriculum.get_curriculum_info(engine.generation)
        
        print(f"🧬 Generation {engine.generation + 1}")
        print(f"   Difficulty: {curriculum_info['difficulty']}/15")
        print(f"   Task: {task[:50]}..." if len(task) > 50 else f"   Task: {task}")
        
        # Evaluate heirs
        for heir in engine.population:
            fitness = await engine.evaluate_heir(heir, task)
            heir.fitness_score = (heir.fitness_score * heir.tasks_completed + fitness) / (heir.tasks_completed + 1)
            heir.tasks_completed += 1
        
        # Log stats
        avg_fitness = sum(h.fitness_score for h in engine.population) / len(engine.population)
        best_fitness = max(h.fitness_score for h in engine.population)
        
        print(f"   Avg Fitness: {avg_fitness:.3f}")
        print(f"   Best Fitness: {best_fitness:.3f}")
        
        # Log to file
        entry = {
            "generation": engine.generation + 1,
            "avg_fitness": avg_fitness,
            "best_fitness": best_fitness,
            "difficulty": curriculum_info['difficulty']
        }
        with open(demo_ledger, 'a') as f:
            f.write(json.dumps(entry) + '\n')
        
        # Selection and reproduction
        engine.population.sort(key=lambda h: h.fitness_score, reverse=True)
        survivors = engine.population[:len(engine.population)//2]
        
        # Create offspring
        offspring = []
        while len(survivors) + len(offspring) < engine.population_size:
            parent = random.choice(survivors)
            child = parent.mutate()
            offspring.append(child)
            
            # Track lineage
            engine.lineage.register_heir(child.id, child.parent_id)
        
        engine.population = survivors + offspring
        engine.generation += 1
        
        print()
    
    # Final statistics
    print("=" * 60)
    print("EVOLUTION COMPLETE")
    print("=" * 60)
    print()
    
    # Show fitness progression
    print("📈 Fitness Progression:")
    with open(demo_ledger, 'r') as f:
        lines = f.readlines()
        first = json.loads(lines[0])
        last = json.loads(lines[-1])
        
        print(f"   Generation 1:  Avg={first['avg_fitness']:.3f}, Best={first['best_fitness']:.3f}")
        print(f"   Generation {generations}: Avg={last['avg_fitness']:.3f}, Best={last['best_fitness']:.3f}")
        
        improvement = ((last['avg_fitness'] - first['avg_fitness']) / first['avg_fitness'] * 100)
        print(f"   Improvement: +{improvement:.1f}%")
    
    print()
    
    # Show lineage analysis
    print("🧬 Lineage Analysis:")
    convergence = engine.lineage.analyze_convergence()
    
    print(f"   Total heirs tracked: {len(engine.lineage.lineages)}")
    print(f"   Unique bloodlines: {len(set(engine.lineage.get_founder(h) for h in engine.lineage.lineages.keys()))}")
    print(f"   Converging: {convergence['converging']}")
    if convergence['dominant_bloodline']:
        print(f"   Dominant bloodline: {convergence['dominant_bloodline']}")
        print(f"   Dominance: {convergence['dominance_percent']:.1f}%")
    
    print()
    
    # Show best heir
    best_heir = max(engine.population, key=lambda h: h.fitness_score)
    print("🏆 Best Heir:")
    print(f"   ID: {best_heir.id}")
    print(f"   Fitness: {best_heir.fitness_score:.3f}")
    print(f"   Generation: {best_heir.generation}")
    print(f"   Temperature: {best_heir.temperature:.2f}")
    print(f"   Tasks completed: {best_heir.tasks_completed}")
    print(f"   Lineage depth: {engine.lineage.get_generation_depth(best_heir.id)}")
    print()
    
    # Export lineage graph
    engine.lineage.export_lineage_graph("demo_lineage_graph.json")
    
    print("📊 Output files:")
    print(f"   - {demo_ledger} (evolution history)")
    print(f"   - demo_lineage_graph.json (visualization data)")
    print()
    print("✅ Demo complete!")
    print()

if __name__ == "__main__":
    import sys
    
    gens = 10
    if len(sys.argv) > 1:
        try:
            gens = int(sys.argv[1])
        except ValueError:
            print("Usage: python demo_evolution.py [generations]")
            sys.exit(1)
    
    asyncio.run(run_demo_evolution(gens))

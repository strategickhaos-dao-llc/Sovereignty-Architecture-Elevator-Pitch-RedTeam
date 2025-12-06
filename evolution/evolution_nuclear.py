#!/usr/bin/env python3
"""
Nuclear Evolution Engine - Full Level 10 Upgrades
Combines all advanced features for maximum evolution power
"""

import asyncio
import argparse
from pathlib import Path

from evolution_engine import EvolutionEngine, Heir
from level10_fitness import JudgeFitnessEvaluator
from crossover import selection_and_sexual_reproduction
from lamarckian import apply_lamarckian_evolution
from task_curriculum import AdaptiveCurriculum
from lineage import visualize_evolution_progress


class NuclearEvolutionEngine:
    """
    Full-featured evolution engine with all Level 10 upgrades:
    - Judge-based fitness evaluation
    - Sexual reproduction (crossover)
    - Lamarckian reflection (self-modification)
    - Adaptive task curriculum
    - Lineage tracking
    """
    
    def __init__(
        self,
        population_size: int = 20,
        model: str = "qwen2.5:72b",
        api_url: str = "http://localhost:11434",
        use_judge: bool = True,
        use_crossover: bool = True,
        use_lamarckian: bool = True,
        use_curriculum: bool = True
    ):
        self.engine = EvolutionEngine(population_size, model, api_url)
        self.use_judge = use_judge
        self.use_crossover = use_crossover
        self.use_lamarckian = use_lamarckian
        self.use_curriculum = use_curriculum
        
        # Initialize components
        self.evaluator = JudgeFitnessEvaluator(model, api_url) if use_judge else None
        self.curriculum = AdaptiveCurriculum() if use_curriculum else None
        
        print("🧬 Nuclear Evolution Engine Initialized")
        print(f"   Population size: {population_size}")
        print(f"   Judge evaluation: {'✅' if use_judge else '❌'}")
        print(f"   Sexual crossover: {'✅' if use_crossover else '❌'}")
        print(f"   Lamarckian reflection: {'✅' if use_lamarckian else '❌'}")
        print(f"   Adaptive curriculum: {'✅' if use_curriculum else '❌'}")
    
    async def evaluate_population(self, generation: int):
        """Evaluate all heirs with appropriate tasks"""
        
        # Get tasks for this generation
        if self.use_curriculum:
            tasks = self.curriculum.get_task_set_for_generation(generation, count=5)
        else:
            tasks = [
                "Analyze the security implications of distributed AI systems.",
                "Propose an efficient investigation workflow.",
                "Identify potential risks in autonomous operations.",
                "Design a verification framework for generated code.",
                "Explain quantum computing to a 10-year-old."
            ]
        
        # Evaluate each heir
        for heir in self.engine.population:
            task = tasks[generation % len(tasks)]
            
            if self.use_judge and self.evaluator:
                fitness = await self.evaluator.evaluate_heir_advanced(heir, task)
            else:
                fitness = await self.engine.evaluate_heir(heir, task)
            
            # Update heir fitness (running average)
            if heir.tasks_completed > 1:
                heir.fitness_score = (heir.fitness_score * (heir.tasks_completed - 1) + fitness) / heir.tasks_completed
            else:
                heir.fitness_score = fitness
    
    def evolve_population(self):
        """Apply evolution operators to population"""
        
        if self.use_crossover:
            # Use sexual reproduction
            self.engine.population = selection_and_sexual_reproduction(
                self.engine.population,
                self.engine.population_size
            )
        else:
            # Use mutation-only reproduction
            self.engine.selection_and_reproduction()
    
    async def apply_reflection(self, generation: int):
        """Apply Lamarckian reflection if enabled"""
        
        if self.use_lamarckian and generation % 5 == 0:
            await apply_lamarckian_evolution(
                self.engine.population,
                generation,
                reflection_frequency=5,
                api_url=self.engine.api_url
            )
    
    def update_curriculum(self, generation: int):
        """Update adaptive curriculum based on performance"""
        
        if self.use_curriculum and self.curriculum:
            avg_fitness = sum(h.fitness_score for h in self.engine.population) / len(self.engine.population)
            self.curriculum.update_performance(generation, avg_fitness)
    
    async def run_evolution(self, max_generations: int = 100, report_frequency: int = 10):
        """Run nuclear evolution for specified generations"""
        
        # Load or initialize population
        if not self.engine.load_population():
            self.engine.initialize_population()
        
        print(f"\n🔥 Nuclear Evolution Started - {max_generations} generations\n")
        
        try:
            start_gen = self.engine.generation + 1
            
            for generation in range(start_gen, start_gen + max_generations):
                self.engine.generation = generation
                
                print(f"🧬 Generation {generation}/{start_gen + max_generations - 1}")
                
                # Evaluate population
                await self.evaluate_population(generation)
                
                # Update curriculum
                self.update_curriculum(generation)
                
                # Evolve population
                self.evolve_population()
                
                # Apply reflection
                await self.apply_reflection(generation)
                
                # Log and save
                self.engine.log_generation()
                self.engine.save_population()
                
                # Progress report
                if generation % report_frequency == 0:
                    visualize_evolution_progress()
                
                # Brief pause
                await asyncio.sleep(2)
        
        except KeyboardInterrupt:
            print("\n\n🛑 Nuclear Evolution Stopped")
            visualize_evolution_progress()
        
        print(f"\n✅ Evolution Complete - Final Generation: {self.engine.generation}")


async def main():
    """Main entry point with CLI arguments"""
    
    parser = argparse.ArgumentParser(
        description="Nuclear Evolution Engine - Full Level 10 AI Evolution"
    )
    
    parser.add_argument(
        "--population",
        type=int,
        default=20,
        help="Population size (default: 20)"
    )
    
    parser.add_argument(
        "--generations",
        type=int,
        default=100,
        help="Number of generations to run (default: 100)"
    )
    
    parser.add_argument(
        "--model",
        type=str,
        default="qwen2.5:72b",
        help="LLM model to use (default: qwen2.5:72b)"
    )
    
    parser.add_argument(
        "--api-url",
        type=str,
        default="http://localhost:11434",
        help="API URL for LLM (default: http://localhost:11434)"
    )
    
    parser.add_argument(
        "--no-judge",
        action="store_true",
        help="Disable judge-based fitness evaluation"
    )
    
    parser.add_argument(
        "--no-crossover",
        action="store_true",
        help="Disable sexual reproduction (use mutation only)"
    )
    
    parser.add_argument(
        "--no-lamarckian",
        action="store_true",
        help="Disable Lamarckian self-reflection"
    )
    
    parser.add_argument(
        "--no-curriculum",
        action="store_true",
        help="Disable adaptive task curriculum"
    )
    
    parser.add_argument(
        "--report-frequency",
        type=int,
        default=10,
        help="Report progress every N generations (default: 10)"
    )
    
    args = parser.parse_args()
    
    # Create nuclear engine
    engine = NuclearEvolutionEngine(
        population_size=args.population,
        model=args.model,
        api_url=args.api_url,
        use_judge=not args.no_judge,
        use_crossover=not args.no_crossover,
        use_lamarckian=not args.no_lamarckian,
        use_curriculum=not args.no_curriculum
    )
    
    # Run evolution
    await engine.run_evolution(args.generations, args.report_frequency)


if __name__ == "__main__":
    asyncio.run(main())

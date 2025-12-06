#!/usr/bin/env python3
"""
Example Usage Scripts for Neural Heir Evolution System
Demonstrates various ways to use the evolution engine
"""

import asyncio


async def example_basic_evolution():
    """Example 1: Basic evolution with default settings"""
    from evolution_engine import EvolutionEngine
    
    print("Example 1: Basic Evolution\n")
    
    engine = EvolutionEngine(population_size=10)
    engine.initialize_population()
    
    # Run 5 generations
    for i in range(5):
        await engine.run_generation()
        engine.selection_and_reproduction()
        engine.save_population()
    
    print(f"\nFinal best fitness: {max(h.fitness_score for h in engine.population):.3f}")


async def example_with_judge_evaluation():
    """Example 2: Using judge-based fitness evaluation"""
    from evolution_engine import EvolutionEngine, Heir
    from level10_fitness import JudgeFitnessEvaluator
    
    print("\nExample 2: Judge-Based Evaluation\n")
    
    engine = EvolutionEngine(population_size=5)
    engine.initialize_population()
    evaluator = JudgeFitnessEvaluator()
    
    # Evaluate one generation with judge
    for heir in engine.population:
        task = "Explain the concept of emergence in complex systems."
        fitness = await evaluator.evaluate_heir_advanced(heir, task)
        heir.fitness_score = fitness
        print(f"{heir.id}: {fitness:.3f}")


async def example_with_crossover():
    """Example 3: Sexual reproduction with crossover"""
    from evolution_engine import Heir
    from crossover import CrossoverOperator
    
    print("\nExample 3: Sexual Reproduction\n")
    
    parent1 = Heir("You are analytical and careful. Think deeply.", 0.7, 5)
    parent1.fitness_score = 0.85
    
    parent2 = Heir("You are creative and bold. Take risks.", 0.9, 5)
    parent2.fitness_score = 0.78
    
    operator = CrossoverOperator()
    
    # Create offspring
    children = []
    for i in range(3):
        child = operator.crossover(parent1, parent2)
        children.append(child)
        print(f"Child {i+1}:")
        print(f"  Prompt: {child.system_prompt[:60]}...")
        print(f"  Temperature: {child.temperature:.2f}")
        print(f"  Parent: {child.parent_id}\n")


async def example_with_lamarckian():
    """Example 4: Lamarckian self-reflection"""
    from evolution_engine import Heir
    from lamarckian import LamarckianReflector
    
    print("\nExample 4: Lamarckian Self-Reflection\n")
    
    heir = Heir("You are a tactical analyst. Be direct and actionable.", 0.7, 10)
    heir.fitness_score = 0.75
    heir.tasks_completed = 50
    
    reflector = LamarckianReflector()
    
    print("Original prompt:")
    print(f"  {heir.system_prompt}\n")
    
    success = await reflector.lamarckian_reflect(heir)
    
    if success:
        print("Evolved prompt:")
        print(f"  {heir.system_prompt[:100]}...\n")


async def example_with_curriculum():
    """Example 5: Task curriculum with progressive difficulty"""
    from task_curriculum import TaskCurriculum, AdaptiveCurriculum
    
    print("\nExample 5: Task Curriculum\n")
    
    # Static curriculum
    curriculum = TaskCurriculum()
    
    print("Static Curriculum:")
    for gen in [1, 25, 50, 100, 150]:
        difficulty = curriculum.get_difficulty_for_generation(gen)
        task = curriculum.get_task_for_generation(gen)
        print(f"  Gen {gen:3d}: Difficulty {difficulty:2d}/15 - {task[:50]}...")
    
    print("\nAdaptive Curriculum:")
    adaptive = AdaptiveCurriculum()
    
    # Simulate high performance
    for gen in range(1, 31):
        adaptive.update_performance(gen, 0.85)  # High fitness
    
    task = adaptive.get_task_for_generation(30)
    print(f"  Gen 30 (high performance): {task[:60]}...")


async def example_lineage_tracking():
    """Example 6: Lineage tracking and visualization"""
    from evolution_engine import EvolutionEngine
    from lineage import LineageTracker, visualize_evolution_progress
    
    print("\nExample 6: Lineage Tracking\n")
    
    # Run a few generations first
    engine = EvolutionEngine(population_size=8)
    engine.initialize_population()
    
    for i in range(3):
        await engine.run_generation()
        engine.selection_and_reproduction()
        engine.save_population()
        engine.log_generation()
    
    # Analyze lineage
    tracker = LineageTracker()
    tracker.load_from_ledger()
    
    analysis = tracker.analyze_lineages()
    print(f"Total heirs tracked: {analysis['total_heirs']}")
    print(f"Root ancestors: {analysis['root_ancestors']}")
    print(f"Generations: {analysis['generations']}")


async def example_nuclear_evolution():
    """Example 7: Full nuclear evolution with all features"""
    from evolution_nuclear import NuclearEvolutionEngine
    
    print("\nExample 7: Nuclear Evolution (All Features)\n")
    
    engine = NuclearEvolutionEngine(
        population_size=10,
        use_judge=False,  # Disable for demo (requires LLM API)
        use_crossover=True,
        use_lamarckian=False,  # Disable for demo
        use_curriculum=True
    )
    
    # Run just 3 generations for demo
    await engine.run_evolution(max_generations=3, report_frequency=1)


async def main():
    """Run all examples"""
    print("=" * 70)
    print("NEURAL HEIR EVOLUTION SYSTEM - USAGE EXAMPLES")
    print("=" * 70)
    
    examples = [
        # Basic examples that don't require LLM API
        ("Crossover", example_with_crossover),
        ("Curriculum", example_with_curriculum),
        
        # Uncomment to run examples that require LLM API:
        # ("Basic Evolution", example_basic_evolution),
        # ("Judge Evaluation", example_with_judge_evaluation),
        # ("Lamarckian", example_with_lamarckian),
        # ("Lineage Tracking", example_lineage_tracking),
        # ("Nuclear Evolution", example_nuclear_evolution),
    ]
    
    for name, example_func in examples:
        try:
            await example_func()
        except Exception as e:
            print(f"Error in {name} example: {e}\n")
    
    print("=" * 70)
    print("\nNote: Some examples require a running LLM API (e.g., Ollama)")
    print("Uncomment them in main() to run with API access.")


if __name__ == "__main__":
    asyncio.run(main())

#!/usr/bin/env python3
"""
Basic tests for Neural Heir Evolution System
Tests core functionality without requiring live LLM API
"""

import sys
import json
import tempfile
from pathlib import Path

# Add evolution directory to path
sys.path.insert(0, str(Path(__file__).parent))

from evolution_engine import Heir, EvolutionEngine


def test_heir_creation():
    """Test basic heir creation and serialization"""
    print("Testing Heir creation...")
    
    heir = Heir("You are a test agent.", 0.7, generation=0)
    
    assert heir.system_prompt == "You are a test agent."
    assert heir.temperature == 0.7
    assert heir.generation == 0
    assert heir.fitness_score == 0.0
    assert heir.tasks_completed == 0
    
    # Test serialization
    heir_dict = heir.to_dict()
    assert "id" in heir_dict
    assert heir_dict["system_prompt"] == "You are a test agent."
    
    # Test deserialization
    heir2 = Heir.from_dict(heir_dict)
    assert heir2.id == heir.id
    assert heir2.system_prompt == heir.system_prompt
    
    print("✅ Heir creation test passed")


def test_heir_mutation():
    """Test heir mutation"""
    print("\nTesting Heir mutation...")
    
    parent = Heir("You are analytical.", 0.7, generation=5)
    parent.fitness_score = 0.8
    
    child = parent.mutate()
    
    assert child.generation == 6
    assert child.parent_id == parent.id
    assert "analytical" in child.system_prompt.lower() or "evolutionary adaptation" in child.system_prompt.lower()
    assert 0.1 <= child.temperature <= 2.0
    
    print(f"Parent prompt: {parent.system_prompt}")
    print(f"Child prompt: {child.system_prompt}")
    print(f"Parent temp: {parent.temperature}, Child temp: {child.temperature}")
    print("✅ Mutation test passed")


def test_evolution_engine_initialization():
    """Test evolution engine initialization"""
    print("\nTesting EvolutionEngine initialization...")
    
    engine = EvolutionEngine(population_size=10)
    engine.initialize_population()
    
    assert len(engine.population) >= 10  # Should have at least 10 heirs
    assert engine.generation == 0
    
    # Check diversity
    prompts = [h.system_prompt for h in engine.population]
    temperatures = [h.temperature for h in engine.population]
    
    assert len(set(prompts)) >= 3  # At least 3 different prompts
    assert len(set(temperatures)) >= 2  # At least 2 different temperatures
    
    print(f"Population size: {len(engine.population)}")
    print(f"Unique prompts: {len(set(prompts))}")
    print(f"Unique temperatures: {len(set(temperatures))}")
    print("✅ Initialization test passed")


def test_selection_and_reproduction():
    """Test selection and reproduction logic"""
    print("\nTesting selection and reproduction...")
    
    engine = EvolutionEngine(population_size=10)
    engine.initialize_population()
    
    # Assign random fitness scores
    import random
    for heir in engine.population:
        heir.fitness_score = random.random()
        heir.tasks_completed = 1
    
    initial_count = len(engine.population)
    initial_avg_fitness = sum(h.fitness_score for h in engine.population) / len(engine.population)
    
    # Get sorted initial population
    sorted_initial = sorted(engine.population, key=lambda h: h.fitness_score, reverse=True)
    top_half_fitness = sum(h.fitness_score for h in sorted_initial[:initial_count//2]) / (initial_count//2)
    
    # Run selection and reproduction
    engine.selection_and_reproduction()
    
    # Check population size maintained
    assert len(engine.population) == initial_count
    
    # Check that top performers survived
    survivors_with_fitness = [h for h in engine.population if h.tasks_completed > 0]
    survivor_avg_fitness = sum(h.fitness_score for h in survivors_with_fitness) / len(survivors_with_fitness)
    
    print(f"Initial avg fitness: {initial_avg_fitness:.3f}")
    print(f"Top half fitness: {top_half_fitness:.3f}")
    print(f"Survivor avg fitness: {survivor_avg_fitness:.3f}")
    print(f"Population maintained at: {len(engine.population)}")
    
    # Survivors should have higher fitness than initial average
    assert survivor_avg_fitness >= top_half_fitness * 0.95  # Survivors should be top performers
    
    print("✅ Selection and reproduction test passed")


def test_population_persistence():
    """Test saving and loading population"""
    print("\nTesting population persistence...")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Change to temp directory
        import os
        old_cwd = os.getcwd()
        os.chdir(tmpdir)
        
        try:
            # Create and save population
            engine = EvolutionEngine(population_size=5)
            engine.initialize_population()
            engine.generation = 10
            
            for heir in engine.population:
                heir.fitness_score = 0.75
                heir.tasks_completed = 20
            
            engine.save_population()
            
            # Create new engine and load
            engine2 = EvolutionEngine(population_size=5)
            success = engine2.load_population()
            
            assert success
            assert engine2.generation == 10
            assert len(engine2.population) == 5
            assert engine2.population[0].fitness_score == 0.75
            
            print(f"Saved and loaded generation: {engine2.generation}")
            print(f"Loaded population size: {len(engine2.population)}")
            print("✅ Persistence test passed")
            
        finally:
            os.chdir(old_cwd)


def test_ledger_logging():
    """Test evolution ledger logging"""
    print("\nTesting ledger logging...")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        import os
        old_cwd = os.getcwd()
        os.chdir(tmpdir)
        
        try:
            engine = EvolutionEngine(population_size=5)
            engine.initialize_population()
            engine.generation = 1
            
            for heir in engine.population:
                heir.fitness_score = 0.6
            
            engine.log_generation()
            
            # Read ledger
            from evolution_engine import EVOLUTION_LOG
            assert EVOLUTION_LOG.exists()
            
            with open(EVOLUTION_LOG, 'r') as f:
                line = f.readline()
                entry = json.loads(line)
            
            assert entry["generation"] == 1
            assert "avg_fitness" in entry
            assert "best_fitness" in entry
            assert "best_heir" in entry
            
            print(f"Logged generation: {entry['generation']}")
            print(f"Avg fitness: {entry['avg_fitness']:.3f}")
            print("✅ Ledger logging test passed")
            
        finally:
            os.chdir(old_cwd)


def test_crossover_module():
    """Test crossover functionality"""
    print("\nTesting crossover module...")
    
    try:
        from crossover import CrossoverOperator
        
        parent1 = Heir("You are analytical and careful.", 0.7, 5)
        parent1.fitness_score = 0.8
        
        parent2 = Heir("You are creative and bold.", 0.9, 5)
        parent2.fitness_score = 0.75
        
        operator = CrossoverOperator()
        child = operator.crossover(parent1, parent2)
        
        assert child.generation == 6
        assert "+" in child.parent_id  # Should reference both parents
        assert 0.1 <= child.temperature <= 2.0
        assert len(child.system_prompt) > 0
        
        print(f"Parent 1: {parent1.system_prompt[:40]}...")
        print(f"Parent 2: {parent2.system_prompt[:40]}...")
        print(f"Child: {child.system_prompt[:40]}...")
        print("✅ Crossover test passed")
        
    except ImportError as e:
        print(f"⚠️  Crossover module not available: {e}")


def test_task_curriculum():
    """Test task curriculum module"""
    print("\nTesting task curriculum...")
    
    try:
        from task_curriculum import TaskCurriculum
        
        curriculum = TaskCurriculum()
        
        # Test difficulty scaling
        diff_1 = curriculum.get_difficulty_for_generation(1)
        diff_50 = curriculum.get_difficulty_for_generation(50)
        diff_150 = curriculum.get_difficulty_for_generation(150)
        
        assert diff_1 < diff_50 < diff_150
        
        # Test task retrieval
        task = curriculum.get_task_for_generation(25)
        assert len(task) > 0
        
        print(f"Gen 1 difficulty: {diff_1}")
        print(f"Gen 50 difficulty: {diff_50}")
        print(f"Gen 150 difficulty: {diff_150}")
        print(f"Sample task: {task[:60]}...")
        print("✅ Task curriculum test passed")
        
    except ImportError as e:
        print(f"⚠️  Task curriculum module not available: {e}")


def run_all_tests():
    """Run all tests"""
    print("=" * 70)
    print("NEURAL HEIR EVOLUTION SYSTEM - TESTS")
    print("=" * 70)
    
    tests = [
        test_heir_creation,
        test_heir_mutation,
        test_evolution_engine_initialization,
        test_selection_and_reproduction,
        test_population_persistence,
        test_ledger_logging,
        test_crossover_module,
        test_task_curriculum,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"❌ {test.__name__} FAILED: {e}")
            failed += 1
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 70)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("=" * 70)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

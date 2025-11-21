#!/usr/bin/env python3
"""
Test Script for Neural Heir Evolution System
Validates core functionality without requiring Ollama
"""

import sys
import json
from pathlib import Path

def test_heir_creation():
    """Test Heir class creation and serialization"""
    print("Testing Heir class...")
    
    from evolution_engine import Heir
    
    heir = Heir("Test prompt", 0.7, 0)
    assert heir.system_prompt == "Test prompt"
    assert heir.temperature == 0.7
    assert heir.generation == 0
    assert heir.fitness_score == 0.0
    
    # Test serialization
    data = heir.to_dict()
    assert "id" in data
    assert "system_prompt" in data
    
    # Test deserialization
    heir2 = Heir.from_dict(data)
    assert heir2.system_prompt == heir.system_prompt
    assert heir2.temperature == heir.temperature
    
    print("✅ Heir class tests passed")

def test_mutation():
    """Test heir mutation"""
    print("Testing mutation...")
    
    from evolution_engine import Heir
    
    parent = Heir("Original prompt", 0.8, 0)
    child = parent.mutate()
    
    assert child.generation == 1
    assert child.parent_id == parent.id
    assert "Original prompt" in child.system_prompt
    assert child.temperature >= 0.1 and child.temperature <= 2.0
    
    print("✅ Mutation tests passed")

def test_evolution_engine():
    """Test EvolutionEngine initialization"""
    print("Testing EvolutionEngine...")
    
    from evolution_engine import EvolutionEngine
    
    engine = EvolutionEngine(population_size=10)
    engine.initialize_population()
    
    assert len(engine.population) == 15  # 5 prompts × 3 temps
    assert engine.generation == 0
    
    # Test selection logic (without actual evaluation)
    for heir in engine.population:
        heir.fitness_score = 0.5  # Set dummy fitness
    
    engine.selection_and_reproduction()
    
    assert len(engine.population) == 10  # Should maintain population size
    
    print("✅ EvolutionEngine tests passed")

def test_crossover():
    """Test genetic crossover"""
    print("Testing crossover...")
    
    from crossover import GeneticCrossover
    from evolution_engine import Heir
    
    parent1 = Heir("Line 1\nLine 2\nLine 3", 0.7, 1)
    parent2 = Heir("Line A\nLine B\nLine C", 0.9, 1)
    
    child_prompt = GeneticCrossover.crossover_prompts(
        parent1.system_prompt,
        parent2.system_prompt
    )
    
    assert len(child_prompt) > 0
    assert isinstance(child_prompt, str)
    
    child_temp = GeneticCrossover.crossover_temperature(
        parent1.temperature,
        parent2.temperature
    )
    
    assert child_temp >= 0.1 and child_temp <= 2.0
    
    print("✅ Crossover tests passed")

def test_task_curriculum():
    """Test task curriculum"""
    print("Testing task curriculum...")
    
    from task_curriculum import TaskCurriculum
    
    curriculum = TaskCurriculum()
    
    # Test difficulty scaling
    assert curriculum.get_difficulty_for_generation(0) == 1
    assert curriculum.get_difficulty_for_generation(20) == 5
    assert curriculum.get_difficulty_for_generation(100) == 12  # Gen 81+ = difficulty 12
    
    # Test task retrieval
    task = curriculum.get_task_for_generation(10)
    assert isinstance(task, str)
    assert len(task) > 0
    
    # Test mixed tasks
    tasks = curriculum.get_mixed_difficulty_tasks(25, count=3)
    assert len(tasks) <= 3
    assert all(isinstance(t, str) for t in tasks)
    
    # Test curriculum info
    info = curriculum.get_curriculum_info(50)
    assert info["generation"] == 50
    assert info["difficulty"] == 7
    
    print("✅ Task curriculum tests passed")

def test_lineage_tracker():
    """Test lineage tracking"""
    print("Testing lineage tracker...")
    
    from lineage import LineageTracker
    
    tracker = LineageTracker()
    
    # Register founders
    tracker.register_heir("heir_001", None)
    tracker.register_heir("heir_002", None)
    
    # Register children
    tracker.register_heir("heir_003", "heir_001")
    tracker.register_heir("heir_004", "heir_001")
    tracker.register_heir("heir_005", "heir_002")
    
    # Test lineage retrieval
    lineage = tracker.get_lineage("heir_003")
    assert lineage == ["heir_001", "heir_003"]
    
    # Test generation depth
    depth = tracker.get_generation_depth("heir_003")
    assert depth == 1
    
    # Test founder identification
    founder = tracker.get_founder("heir_004")
    assert founder == "heir_001"
    
    # Test bloodline stats
    dominant = tracker.get_dominant_bloodlines(top_n=2)
    assert len(dominant) == 2
    
    # Test diversity
    diversity = tracker.get_bloodline_diversity()
    assert diversity["unique_bloodlines"] == 2
    assert diversity["total_heirs"] == 5
    
    print("✅ Lineage tracker tests passed")

def test_serialization():
    """Test save/load functionality"""
    print("Testing serialization...")
    
    from evolution_engine import EvolutionEngine
    from pathlib import Path
    
    # Create test files
    test_pop_file = Path("/tmp/test_population.json")
    test_ledger_file = Path("/tmp/test_ledger.jsonl")
    
    # Clean up if exists
    test_pop_file.unlink(missing_ok=True)
    test_ledger_file.unlink(missing_ok=True)
    
    # Create engine and save
    engine = EvolutionEngine(population_size=5)
    engine.initialize_population()
    
    # Modify paths for test
    original_pop_file = Path("current_population.json")
    original_ledger = Path("evolution_ledger.jsonl")
    
    import evolution_engine
    evolution_engine.POPULATION_FILE = test_pop_file
    evolution_engine.EVOLUTION_LOG = test_ledger_file
    
    engine.save_population()
    
    assert test_pop_file.exists()
    
    # Load and verify
    engine2 = EvolutionEngine()
    loaded = engine2.load_population()
    
    assert loaded == True
    assert len(engine2.population) > 0
    
    # Clean up
    test_pop_file.unlink(missing_ok=True)
    test_ledger_file.unlink(missing_ok=True)
    
    print("✅ Serialization tests passed")

def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("Neural Heir Evolution System - Test Suite")
    print("=" * 60)
    print()
    
    tests = [
        test_heir_creation,
        test_mutation,
        test_evolution_engine,
        test_crossover,
        test_task_curriculum,
        test_lineage_tracker,
        test_serialization
    ]
    
    failed = []
    
    for test in tests:
        try:
            test()
        except Exception as e:
            print(f"❌ {test.__name__} FAILED: {e}")
            failed.append((test.__name__, str(e)))
        print()
    
    print("=" * 60)
    if not failed:
        print("✅ ALL TESTS PASSED")
        print("=" * 60)
        return 0
    else:
        print(f"❌ {len(failed)} TEST(S) FAILED:")
        for name, error in failed:
            print(f"  - {name}: {error}")
        print("=" * 60)
        return 1

if __name__ == "__main__":
    sys.exit(run_all_tests())

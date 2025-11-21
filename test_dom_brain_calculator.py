#!/usr/bin/env python3
"""
Tests for DomBrainCalculator
Validates the cognitive architecture implementation
"""

import unittest
import statistics
from dom_brain_calculator import (
    DomBrainCalculator,
    PathwayType,
    SolutionPath,
    Collision
)


class TestDomBrainCalculator(unittest.TestCase):
    """Test cases for DomBrainCalculator"""
    
    def setUp(self):
        """Set up test calculator"""
        self.calc = DomBrainCalculator(pathway_count=50, consolidation_threshold=0.3)
    
    def test_basic_addition(self):
        """Test basic addition calculation"""
        result = self.calc.calculate("5 + 3", 5, 3, '+')
        
        # Check answer is close to correct (within 1%)
        self.assertAlmostEqual(result['answer'], 8.0, delta=0.08)
        
        # Check structure
        self.assertIn('answer', result)
        self.assertIn('all_paths', result)
        self.assertIn('consolidated_paths', result)
        self.assertIn('collisions', result)
        self.assertIn('dopamine_hit', result)
        
        # Check paths were generated
        self.assertEqual(len(result['all_paths']), 50)
        self.assertGreater(len(result['consolidated_paths']), 0)
    
    def test_basic_multiplication(self):
        """Test basic multiplication calculation"""
        result = self.calc.calculate("12 * 7", 12, 7, '*')
        
        # Check answer is close to correct (within 1%)
        self.assertAlmostEqual(result['answer'], 84.0, delta=0.84)
        
        # Check paths were generated and consolidated
        self.assertEqual(len(result['all_paths']), 50)
        self.assertGreater(len(result['consolidated_paths']), 0)
    
    def test_basic_subtraction(self):
        """Test basic subtraction calculation"""
        result = self.calc.calculate("100 - 37", 100, 37, '-')
        
        # Check answer is close to correct (within 1%)
        self.assertAlmostEqual(result['answer'], 63.0, delta=0.63)
    
    def test_basic_division(self):
        """Test basic division calculation"""
        result = self.calc.calculate("100 / 4", 100, 4, '/')
        
        # Check answer is close to correct (within 1%)
        self.assertAlmostEqual(result['answer'], 25.0, delta=0.25)
    
    def test_memory_consolidation(self):
        """Test that memory consolidation prunes weak paths"""
        result = self.calc.calculate("Test consolidation", 10, 5, '+')
        
        # Should have pruned some paths
        self.assertLess(
            len(result['consolidated_paths']),
            len(result['all_paths'])
        )
        
        # All consolidated paths should meet threshold
        for path in result['consolidated_paths']:
            self.assertGreaterEqual(path.confidence, self.calc.consolidation_threshold)
    
    def test_collision_detection(self):
        """Test that collisions are detected when paths converge"""
        result = self.calc.calculate("Test collisions", 5, 3, '+')
        
        # Should detect some collisions
        self.assertGreater(len(result['collisions']), 0)
        
        # Each collision should have multiple paths
        for collision in result['collisions']:
            self.assertGreaterEqual(len(collision.paths), 2)
    
    def test_dopamine_hit_on_rediscovery(self):
        """Test dopamine hit mechanism for rediscovery"""
        problem = "5 + 3"
        
        # First calculation - no dopamine hit
        result1 = self.calc.calculate(problem, 5, 3, '+')
        self.assertFalse(result1['dopamine_hit'])
        
        # Second calculation - should trigger dopamine hit
        result2 = self.calc.calculate(problem, 5, 3, '+')
        self.assertTrue(result2['dopamine_hit'])
        
        # Verify counter incremented
        self.assertEqual(self.calc.dopamine_hits, 1)
    
    def test_pathway_diversity(self):
        """Test that multiple pathway types are used"""
        result = self.calc.calculate("Test diversity", 10, 5, '+')
        
        # Collect pathway types
        pathway_types = set(p.pathway_type for p in result['all_paths'])
        
        # Should have at least 5 different types
        self.assertGreaterEqual(len(pathway_types), 5)
    
    def test_confidence_calculation(self):
        """Test that confidence is calculated correctly"""
        result = self.calc.calculate("Test confidence", 10, 5, '+')
        
        # Confidence should be between 0 and 1
        self.assertGreaterEqual(result['confidence'], 0.0)
        self.assertLessEqual(result['confidence'], 1.0)
        
        # Should match average of consolidated paths
        expected = statistics.mean([p.confidence for p in result['consolidated_paths']])
        self.assertAlmostEqual(result['confidence'], expected, places=2)
    
    def test_symbolic_path_accuracy(self):
        """Test that symbolic path gives exact answer"""
        calc = DomBrainCalculator(pathway_count=10)
        result = calc.calculate("Symbolic test", 5, 3, '+')
        
        # Find symbolic path
        symbolic_paths = [p for p in result['all_paths'] if p.pathway_type == PathwayType.SYMBOLIC]
        
        # Should have exactly one symbolic path
        self.assertEqual(len(symbolic_paths), 1)
        
        # Should be exact
        self.assertEqual(symbolic_paths[0].result, 8.0)
        
        # Should have high confidence
        self.assertGreater(symbolic_paths[0].confidence, 0.9)
    
    def test_history_tracking(self):
        """Test that calculation history is tracked"""
        initial_count = len(self.calc.history)
        
        self.calc.calculate("History test 1", 5, 3, '+')
        self.calc.calculate("History test 2", 10, 5, '*')
        
        # Should have 2 more entries
        self.assertEqual(len(self.calc.history), initial_count + 2)
    
    def test_collision_strength(self):
        """Test collision strength calculation"""
        result = self.calc.calculate("Collision strength", 5, 3, '+')
        
        if result['collisions']:
            for collision in result['collisions']:
                # Strength should be positive
                self.assertGreater(collision.collision_strength, 0)
                
                # Should have synthesis result
                self.assertIsInstance(collision.synthesis_result, float)
    
    def test_zero_division_handling(self):
        """Test handling of division by zero"""
        result = self.calc.calculate("10 / 0", 10, 0, '/')
        
        # Should complete without error
        self.assertIn('answer', result)
        
        # Answer might be inf or large number
        # Just verify it didn't crash
    
    def test_large_numbers(self):
        """Test with large numbers"""
        result = self.calc.calculate("1000000 * 1000000", 1000000, 1000000, '*')
        
        # Should be close to 1 trillion (within 1%)
        expected = 1e12
        self.assertAlmostEqual(result['answer'], expected, delta=expected * 0.01)
    
    def test_negative_numbers(self):
        """Test with negative numbers"""
        result = self.calc.calculate("-5 + 3", -5, 3, '+')
        
        # Should be close to -2 (within 1%)
        self.assertAlmostEqual(result['answer'], -2.0, delta=0.02)
    
    def test_pathway_pruning(self):
        """Test that pruned paths are marked correctly"""
        result = self.calc.calculate("Pruning test", 10, 5, '+')
        
        # Check that pruned paths exist and are marked
        all_paths = result['all_paths']
        pruned_count = sum(1 for p in all_paths if p.pruned)
        
        # Should have pruned some paths
        self.assertGreater(pruned_count, 0)
        
        # Pruned paths should have low confidence
        for path in all_paths:
            if path.pruned:
                self.assertLess(path.confidence, self.calc.consolidation_threshold)


class TestSolutionPath(unittest.TestCase):
    """Test SolutionPath dataclass"""
    
    def test_solution_path_creation(self):
        """Test creating a SolutionPath"""
        path = SolutionPath(
            pathway_type=PathwayType.SYMBOLIC,
            result=8.0,
            confidence=0.95,
            reasoning="Test reasoning"
        )
        
        self.assertEqual(path.pathway_type, PathwayType.SYMBOLIC)
        self.assertEqual(path.result, 8.0)
        self.assertEqual(path.confidence, 0.95)
        self.assertFalse(path.pruned)
    
    def test_solution_path_repr(self):
        """Test string representation"""
        path = SolutionPath(
            pathway_type=PathwayType.QUANTUM,
            result=8.0,
            confidence=0.75,
            reasoning="Test"
        )
        
        repr_str = repr(path)
        self.assertIn("quantum_analogy", repr_str)
        self.assertIn("8.0", repr_str)


class TestCollision(unittest.TestCase):
    """Test Collision dataclass"""
    
    def test_collision_creation(self):
        """Test creating a Collision"""
        path1 = SolutionPath(PathwayType.SYMBOLIC, 8.0, 0.95, "Test 1")
        path2 = SolutionPath(PathwayType.QUANTUM, 8.0, 0.75, "Test 2")
        
        collision = Collision(
            paths=[path1, path2],
            insight="Test collision",
            synthesis_result=8.0,
            collision_strength=1.5
        )
        
        self.assertEqual(len(collision.paths), 2)
        self.assertEqual(collision.synthesis_result, 8.0)
        self.assertEqual(collision.collision_strength, 1.5)


def run_tests():
    """Run all tests"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestDomBrainCalculator))
    suite.addTests(loader.loadTestsFromTestCase(TestSolutionPath))
    suite.addTests(loader.loadTestsFromTestCase(TestCollision))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return success status
    return result.wasSuccessful()


if __name__ == "__main__":
    import sys
    success = run_tests()
    sys.exit(0 if success else 1)

#!/usr/bin/env python3
"""FlameLang Test Suite - Run all tests."""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.lexer import Lexer, TokenType
from glyphs.registry import REGISTRY
from physics.engine import ENGINE
from security.sovereignty import SOVEREIGNTY
from core.repl import Interpreter

def test_lexer():
    """Test lexer tokenization."""
    print("Testing Lexer...", end=" ")
    
    source = "sim BH1 M=1.989e30 r=1e7"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    
    # Should have: sim, BH1, M, =, number, r, =, number, EOF
    assert len(tokens) > 5, "Not enough tokens"
    assert tokens[0].type == TokenType.SIM, "First token should be SIM"
    assert tokens[1].type == TokenType.IDENTIFIER, "Second token should be identifier"
    
    print("✓")
    return True

def test_glyphs():
    """Test glyph registry."""
    print("Testing Glyph Registry...", end=" ")
    
    # Check core glyphs
    execute = REGISTRY.get('⚡')
    assert execute is not None, "Execute glyph not found"
    assert execute.name == 'Execute', "Execute glyph has wrong name"
    assert execute.frequency == 528, "Execute glyph has wrong frequency"
    
    # Check categories
    core_glyphs = REGISTRY.by_category('core')
    assert len(core_glyphs) == 6, f"Expected 6 core glyphs, got {len(core_glyphs)}"
    
    physics_glyphs = REGISTRY.by_category('physics')
    assert len(physics_glyphs) == 6, f"Expected 6 physics glyphs, got {len(physics_glyphs)}"
    
    security_glyphs = REGISTRY.by_category('security')
    assert len(security_glyphs) == 5, f"Expected 5 security glyphs, got {len(security_glyphs)}"
    
    print("✓")
    return True

def test_physics():
    """Test physics engine."""
    print("Testing Physics Engine...", end=" ")
    
    # Test Schwarzschild calculation
    M = 1.989e30  # Solar mass
    r = 1e7  # 10,000 km
    result = ENGINE.compute_schwarzschild(M, r)
    
    assert 'r_s' in result, "Missing Schwarzschild radius"
    assert 'g_tt' in result, "Missing metric component"
    assert result['r_s'] > 0, "Schwarzschild radius should be positive"
    assert result['g_tt'] < 0, "Metric component should be negative"
    
    # Test black hole simulation
    bh = ENGINE.simulate_black_hole('TEST_BH', M, r)
    assert bh['type'] == 'black_hole', "Wrong simulation type"
    assert bh['name'] == 'TEST_BH', "Wrong simulation name"
    
    # Test ocean eddy
    oc = ENGINE.simulate_ocean_eddy('TEST_OC', 0.95)
    assert oc['coherence'] == 0.95, "Wrong coherence value"
    
    print("✓")
    return True

def test_sovereignty():
    """Test sovereignty system."""
    print("Testing Sovereignty System...", end=" ")
    
    # Initialize
    SOVEREIGNTY.initialize_sovereign_environment()
    
    # Check status
    status = SOVEREIGNTY.get_status()
    assert 'initialized' in status, "Missing initialized status"
    assert status['initialized'], "Should be initialized"
    assert not status['network_enabled'], "Network should be disabled by default"
    
    # Test network blocking
    allowed = SOVEREIGNTY.network.check_network_operation("test")
    assert not allowed, "Network operation should be blocked"
    
    # Test telemetry blocking
    blocked = SOVEREIGNTY.telemetry.is_blocked("telemetry.microsoft.com")
    assert blocked, "Telemetry should be blocked"
    
    print("✓")
    return True

def test_interpreter():
    """Test interpreter execution."""
    print("Testing Interpreter...", end=" ")
    
    interpreter = Interpreter()
    
    # Test variable assignment
    result = interpreter.execute("x = 42")
    assert result == 42, "Variable assignment failed"
    assert interpreter.variables['x'] == 42, "Variable not stored"
    
    # Test constants
    assert 'pi' in interpreter.variables, "pi constant missing"
    assert 'c' in interpreter.variables, "c constant missing"
    
    # Test simulation
    result = interpreter.execute("sim BH1 M=1.989e30 r=1e7")
    assert result is not None, "Simulation failed"
    assert 'r_s' in result, "Simulation result missing Schwarzschild radius"
    
    print("✓")
    return True

def test_integration():
    """Test integration of all components."""
    print("Testing Integration...", end=" ")
    
    interpreter = Interpreter()
    
    # Multi-line execution
    lines = [
        "sim BH1 M=1.989e30 r=1e7",
        "coherence = 0.95",
        "sim OC1",
    ]
    
    for line in lines:
        try:
            interpreter.execute(line)
        except Exception as e:
            assert False, f"Failed to execute: {line} - {e}"
    
    # Check that simulations were stored
    bh = interpreter.physics.get_simulation('BH1')
    assert bh is not None, "BH1 simulation not found"
    
    oc = interpreter.physics.get_simulation('OC1')
    assert oc is not None, "OC1 simulation not found"
    
    # Check variables
    assert interpreter.variables['coherence'] == 0.95, "Variable not set"
    
    print("✓")
    return True

def main():
    """Run all tests."""
    print("=" * 60)
    print("🔥 FlameLang Test Suite")
    print("=" * 60)
    print()
    
    tests = [
        test_lexer,
        test_glyphs,
        test_physics,
        test_sovereignty,
        test_interpreter,
        test_integration,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
        except AssertionError as e:
            print(f"✗ - {e}")
            failed += 1
        except Exception as e:
            print(f"✗ - Unexpected error: {e}")
            failed += 1
    
    print()
    print("=" * 60)
    print(f"Results: {passed}/{len(tests)} passed")
    if failed > 0:
        print(f"         {failed}/{len(tests)} failed")
        sys.exit(1)
    else:
        print("🔥 All tests passed!")
    print("=" * 60)

if __name__ == '__main__':
    main()

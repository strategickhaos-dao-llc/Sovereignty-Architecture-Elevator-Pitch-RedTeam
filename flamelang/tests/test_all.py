#!/usr/bin/env python3
"""
FlameLang Comprehensive Test Suite
Tests all core components
"""
import sys
import os
import numpy as np

# Add parent directory to path
flamelang_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if flamelang_dir not in sys.path:
    sys.path.insert(0, flamelang_dir)

# Now import as if we're in the flamelang package
import glyphs.registry as glyph_module
import physics.engine as physics_module
import core.lexer as lexer_module
import core.compiler as compiler_module
import security.sovereignty as sovereignty_module

GLYPH_REGISTRY = glyph_module.GLYPH_REGISTRY
get_glyph = glyph_module.get_glyph
ENGINE = physics_module.ENGINE
simulate_black_hole = physics_module.simulate_black_hole
Lexer = lexer_module.Lexer
TokenType = lexer_module.TokenType
FlameLangCompiler = compiler_module.FlameLangCompiler
PROTOCOL = sovereignty_module.PROTOCOL


def test_glyph_registry():
    """Test 1: Glyph Registry"""
    print("🔥 Testing Glyph Registry...")
    
    # Check we have 17 glyphs
    assert len(GLYPH_REGISTRY) == 17, f"Expected 17 glyphs, got {len(GLYPH_REGISTRY)}"
    
    # Check core glyphs
    assert '⚡' in GLYPH_REGISTRY
    assert '🔥' in GLYPH_REGISTRY
    
    # Check physics glyphs
    assert 'BH1' in GLYPH_REGISTRY
    assert 'OC1' in GLYPH_REGISTRY
    
    # Check security glyphs
    assert '🛡️' in GLYPH_REGISTRY
    assert '🔒' in GLYPH_REGISTRY
    
    # Check glyph lookup
    glyph = get_glyph('🔥')
    assert glyph is not None
    assert glyph['name'] == 'flame'
    assert glyph['frequency'] == 528
    
    print("  ✓ Glyph registry working")
    return True


def test_physics_engine():
    """Test 2: Physics Engine"""
    print("🔥 Testing Physics Engine...")
    
    # Test Schwarzschild radius calculation
    solar_mass = 1.989e30  # kg
    r_s = ENGINE.schwarzschild_radius(solar_mass)
    expected_r_s = 2953  # meters (approximately)
    
    assert abs(r_s - expected_r_s) < 10, f"Schwarzschild radius incorrect: {r_s}"
    
    # Test black hole simulation
    result = simulate_black_hole(solar_mass, 1e7)
    assert 'schwarzschild_radius' in result
    assert result['schwarzschild_radius'] > 0
    
    print(f"  ✓ Schwarzschild metrics working (r_s={r_s/1000:.2f} km)")
    
    # Test symbolic metrics
    metric_str = ENGINE.symbolic_metric()
    assert 'Schwarzschild' in metric_str
    assert 'ds²' in metric_str
    
    print("  ✓ Symbolic metrics working")
    return True


def test_lexer():
    """Test 3: Lexer"""
    print("🔥 Testing Lexer...")
    
    source = """
sim BH1 M=1.989e30 r=1e7
x = 42
🔥
"""
    
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    
    # Check we got tokens
    assert len(tokens) > 0, "No tokens generated"
    
    # Check for specific tokens
    token_types = [t.type for t in tokens]
    assert TokenType.SIM in token_types
    assert TokenType.GLYPH in token_types
    assert TokenType.NUMBER in token_types
    assert TokenType.EOF in token_types
    
    print(f"  ✓ Lexer working ({len(tokens)} tokens parsed)")
    return True


def test_interpreter():
    """Test 4: Interpreter"""
    print("🔥 Testing Interpreter...")
    
    compiler = FlameLangCompiler()
    
    # Test constant lookup
    result = compiler.compile("c")
    assert result == 299792458, f"Speed of light incorrect: {result}"
    
    # Test simulation
    result = compiler.compile("sim BH1 M=1.989e30 r=1e7")
    assert result is not None
    assert 'schwarzschild_radius_km' in result
    
    print("  ✓ Interpreter working")
    return True


def test_sovereignty_layer():
    """Test 5: Sovereignty Layer"""
    print("🔥 Testing Sovereignty Layer...")
    
    # Initialize protocol
    init_result = PROTOCOL.initialize()
    assert init_result['network_isolation'] == True
    assert 'boundary_hash' in init_result
    
    # Test telemetry detection
    code_with_telemetry = "telemetry.microsoft.com"
    detected = PROTOCOL.detect_telemetry(code_with_telemetry)
    assert len(detected) > 0, "Telemetry not detected"
    
    # Test coherence monitoring
    status = PROTOCOL.monitor_process_coherence()
    assert 'coherent' in status
    assert 'boundary_hash' in status
    
    print("  ✓ Sovereignty layer working")
    return True


def test_end_to_end():
    """Test 6: End-to-End Execution"""
    print("🔥 Testing End-to-End Execution...")
    
    # Create a complete FlameLang program
    program = """
# Black hole simulation
sim BH1 M=1.989e30 r=1e7

# Variable assignment
x = 42
"""
    
    compiler = FlameLangCompiler()
    result = compiler.compile(program)
    
    # Check we got a result
    assert result is not None
    
    # Check variables were set
    assert 'x' in compiler.variables
    assert compiler.variables['x'] == 42
    
    print("  ✓ End-to-end execution working")
    return True


def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("🔥 FlameLang Comprehensive Test Suite")
    print("=" * 60)
    print()
    
    tests = [
        test_glyph_registry,
        test_physics_engine,
        test_lexer,
        test_interpreter,
        test_sovereignty_layer,
        test_end_to_end,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"  ✗ Test failed: {e}")
            failed += 1
    
    print()
    print("=" * 60)
    print(f"Results: {passed}/{len(tests)} passed, {failed}/{len(tests)} failed")
    print("=" * 60)
    print()
    
    if failed == 0:
        print("🔥 All tests passed! FlameLang is operational. 🔥")
        return 0
    else:
        print(f"❌ {failed} test(s) failed.")
        return 1


if __name__ == '__main__':
    sys.exit(run_all_tests())

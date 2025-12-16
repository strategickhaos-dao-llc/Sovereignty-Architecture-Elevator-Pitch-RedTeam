#!/usr/bin/env python3
"""
FlameLang ZyBooks Solver - Comprehensive Test Suite
Artifact: INV-083
Operator: Domenic Garza | Strategickhaos DAO LLC
"""

import yaml
import sys
from pathlib import Path
from typing import Dict, List, Tuple

def load_solver():
    """Load the FlameLang ZyBooks Solver pattern rules"""
    solver_path = Path(__file__).parent.parent / "flamelang_zybooks_solver_v1.yaml"
    with open(solver_path, 'r') as f:
        return yaml.safe_load(f)

def test_yaml_structure():
    """Test that YAML structure is valid and contains all required layers"""
    print("Testing YAML structure...")
    solver = load_solver()
    
    required_keys = [
        'meta',
        'layer_1_classification',
        'layer_2_roots',
        'layer_3_rules',
        'layer_4_confidence',
        'layer_5_output',
        'instructions_for_agents',
        'example',
        'architecture',
        'deployment',
        'extensions',
        'legal'
    ]
    
    for key in required_keys:
        assert key in solver, f"Missing required key: {key}"
        print(f"  ✓ {key}")
    
    print("  ✓ YAML structure valid\n")
    return True

def test_meta_information():
    """Test meta information completeness"""
    print("Testing meta information...")
    solver = load_solver()
    meta = solver['meta']
    
    assert meta['artifact_id'] == "INV-083", "Incorrect artifact ID"
    assert meta['version'] == "1.0", "Incorrect version"
    assert meta['type'] == "semantic_pattern_compiler", "Incorrect type"
    
    print(f"  ✓ Artifact ID: {meta['artifact_id']}")
    print(f"  ✓ Version: {meta['version']}")
    print(f"  ✓ Type: {meta['type']}")
    print(f"  ✓ Mode: {meta['mode']}\n")
    return True

def test_layer1_classification():
    """Test Layer 1 question type classification"""
    print("Testing Layer 1 classification...")
    solver = load_solver()
    classification = solver['layer_1_classification']
    
    question_types = ['type_boolean', 'type_comparison', 'type_trend', 
                     'type_percentage', 'type_prediction']
    
    for qtype in question_types:
        assert qtype in classification, f"Missing question type: {qtype}"
        assert 'triggers' in classification[qtype], f"Missing triggers for {qtype}"
        assert 'output_type' in classification[qtype], f"Missing output_type for {qtype}"
        print(f"  ✓ {qtype}: {classification[qtype]['output_type']}")
    
    print("  ✓ All question types defined\n")
    return True

def test_layer2_roots():
    """Test Layer 2 semantic roots"""
    print("Testing Layer 2 semantic roots...")
    solver = load_solver()
    roots = solver['layer_2_roots']
    
    assert 'chart_concepts' in roots, "Missing chart_concepts"
    assert 'logic_operators' in roots, "Missing logic_operators"
    
    # Test chart concepts
    chart_concepts = ['bar_chart', 'horizontal', 'vertical', 'category', 'value', 'relative']
    for concept in chart_concepts:
        assert concept in roots['chart_concepts'], f"Missing chart concept: {concept}"
        print(f"  ✓ chart_concepts.{concept}: {roots['chart_concepts'][concept]}")
    
    # Test logic operators
    logic_ops = ['excels_at', 'preferable', 'compare', 'trend']
    for op in logic_ops:
        assert op in roots['logic_operators'], f"Missing logic operator: {op}"
        print(f"  ✓ logic_operators.{op}: {roots['logic_operators'][op]}")
    
    print("  ✓ All semantic roots defined\n")
    return True

def test_layer3_rules():
    """Test Layer 3 pattern matching rules"""
    print("Testing Layer 3 pattern rules...")
    solver = load_solver()
    rules = solver['layer_3_rules']
    
    rule_categories = ['bar_chart_rules', 'orientation_rules', 'trend_rules', 'prediction_rules']
    
    for category in rule_categories:
        assert category in rules, f"Missing rule category: {category}"
        assert len(rules[category]) > 0, f"Empty rule category: {category}"
        
        print(f"  ✓ {category}: {len(rules[category])} rules")
        
        # Validate rule structure
        for i, rule in enumerate(rules[category]):
            assert 'pattern' in rule, f"{category}[{i}] missing pattern"
            # Some rules have 'answer', some have 'method'
            assert 'answer' in rule or 'method' in rule, f"{category}[{i}] missing answer/method"
            
            if 'answer' in rule:
                assert 'reason' in rule, f"{category}[{i}] missing reason"
    
    print("  ✓ All pattern rules valid\n")
    return True

def test_layer4_confidence():
    """Test Layer 4 confidence scoring criteria"""
    print("Testing Layer 4 confidence scoring...")
    solver = load_solver()
    confidence = solver['layer_4_confidence']
    
    levels = ['high_confidence', 'medium_confidence', 'low_confidence']
    
    for level in levels:
        assert level in confidence, f"Missing confidence level: {level}"
        assert len(confidence[level]) > 0, f"Empty confidence level: {level}"
        print(f"  ✓ {level}: {len(confidence[level])} criteria")
    
    print("  ✓ Confidence scoring criteria defined\n")
    return True

def test_layer5_output():
    """Test Layer 5 output encoding"""
    print("Testing Layer 5 output encoding...")
    solver = load_solver()
    output = solver['layer_5_output']
    
    assert 'codon_mapping' in output, "Missing codon_mapping"
    assert 'emit' in output, "Missing emit function"
    
    codons = ['ATG', 'TAA', 'TGG', 'TGA', 'TAG']
    for codon in codons:
        assert codon in output['codon_mapping'], f"Missing codon: {codon}"
        print(f"  ✓ {codon} → {output['codon_mapping'][codon]}")
    
    print("  ✓ Output encoding defined\n")
    return True

def test_example_execution():
    """Test the example execution walkthrough"""
    print("Testing example execution...")
    solver = load_solver()
    example = solver['example']
    
    assert 'input' in example, "Missing example input"
    assert 'layer_1' in example, "Missing layer_1 execution"
    assert 'layer_2' in example, "Missing layer_2 execution"
    assert 'layer_3' in example, "Missing layer_3 execution"
    assert 'layer_4' in example, "Missing layer_4 execution"
    assert 'layer_5' in example, "Missing layer_5 execution"
    assert 'final_output' in example, "Missing final_output"
    
    # Validate final output structure
    final = example['final_output']
    assert 'answer' in final, "Missing answer in final_output"
    assert 'confidence' in final, "Missing confidence in final_output"
    assert 'reason' in final, "Missing reason in final_output"
    
    print(f"  ✓ Input: {example['input'][:50]}...")
    print(f"  ✓ Answer: {final['answer']}")
    print(f"  ✓ Confidence: {final['confidence']}")
    print(f"  ✓ Reason: {final['reason']}")
    print("  ✓ Example execution valid\n")
    return True

def test_architecture_analogy():
    """Test the compiler architecture analogy"""
    print("Testing compiler architecture analogy...")
    solver = load_solver()
    arch = solver['architecture']
    
    assert 'description' in arch, "Missing architecture description"
    assert 'traditional_compiler' in arch, "Missing traditional_compiler"
    assert 'flamelang_zybooks_solver' in arch, "Missing flamelang_zybooks_solver"
    assert 'comparison' in arch, "Missing comparison"
    assert 'power' in arch, "Missing power statement"
    
    print(f"  ✓ Description: {arch['description']}")
    print(f"  ✓ Traditional: {arch['traditional_compiler']['pipeline']}")
    print(f"  ✓ FlameLang: {arch['flamelang_zybooks_solver']['pipeline']}")
    print(f"  ✓ Power: {arch['power']['statement']}\n")
    return True

def test_deployment_instructions():
    """Test deployment instructions completeness"""
    print("Testing deployment instructions...")
    solver = load_solver()
    deployment = solver['deployment']
    
    assert 'targets' in deployment, "Missing deployment targets"
    assert len(deployment['targets']) > 0, "No deployment targets defined"
    assert 'usage_pattern' in deployment, "Missing usage_pattern"
    assert 'parallel_solving' in deployment, "Missing parallel_solving"
    
    for target in deployment['targets']:
        assert 'platform' in target, "Target missing platform"
        assert 'method' in target, "Target missing method"
        print(f"  ✓ Platform: {target['platform']}")
    
    print("  ✓ Deployment instructions complete\n")
    return True

def run_all_tests():
    """Run all test suites"""
    tests = [
        ("YAML Structure", test_yaml_structure),
        ("Meta Information", test_meta_information),
        ("Layer 1: Classification", test_layer1_classification),
        ("Layer 2: Semantic Roots", test_layer2_roots),
        ("Layer 3: Pattern Rules", test_layer3_rules),
        ("Layer 4: Confidence Scoring", test_layer4_confidence),
        ("Layer 5: Output Encoding", test_layer5_output),
        ("Example Execution", test_example_execution),
        ("Architecture Analogy", test_architecture_analogy),
        ("Deployment Instructions", test_deployment_instructions),
    ]
    
    print("=" * 80)
    print("🔥 FLAMELANG ZYBOOKS SOLVER - COMPREHENSIVE TEST SUITE")
    print("=" * 80)
    print()
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            print(f"{'─' * 80}")
            print(f"TEST: {name}")
            print(f"{'─' * 80}")
            test_func()
            passed += 1
        except AssertionError as e:
            print(f"  ❌ FAILED: {e}\n")
            failed += 1
        except Exception as e:
            print(f"  ❌ ERROR: {e}\n")
            failed += 1
    
    print("=" * 80)
    print(f"TEST RESULTS: {passed} passed, {failed} failed")
    print("=" * 80)
    
    if failed == 0:
        print("✓ ALL TESTS PASSED")
        return 0
    else:
        print(f"✗ {failed} TEST(S) FAILED")
        return 1

if __name__ == "__main__":
    sys.exit(run_all_tests())

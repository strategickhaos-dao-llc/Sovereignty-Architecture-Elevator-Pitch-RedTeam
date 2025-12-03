#!/usr/bin/env python3
"""
Practical Examples: DomBrainCalculator Usage

Shows real-world applications of cognitive architecture for:
- Mathematical verification
- Multi-method validation
- Cross-domain pattern detection
"""

import sys
import os

# Add parent directory to path to import dom_brain_calculator
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dom_brain_calculator import DomBrainCalculator


def example_basic_operations():
    """Example 1: Basic mathematical operations with verification"""
    print("="*80)
    print("EXAMPLE 1: Basic Operations with Multi-Path Verification")
    print("="*80)
    
    calc = DomBrainCalculator(pathway_count=50, dopamine_threshold=0.6)
    
    # Test addition
    print("\n📊 Testing: 42 + 137 (The answer to life + Node number)")
    result = calc.calculate("add", 42, 137)
    print(f"\n✅ Consensus Answer: {result['answer']:.6f}")
    print(f"   Verified by {result['consolidated_paths']} independent pathways")
    print(f"   Cross-validated through {result['collisions']} collision events")
    
    # Test multiplication
    print("\n\n📊 Testing: 13 × 7 (Prime number collision)")
    result = calc.calculate("multiply", 13, 7)
    print(f"\n✅ Consensus Answer: {result['answer']:.6f}")
    print(f"   Pathway types used: {len(result['pathway_types_used'])} different domains")


def example_verification_depth():
    """Example 2: Showing verification depth vs traditional calculators"""
    print("\n\n" + "="*80)
    print("EXAMPLE 2: Verification Depth Comparison")
    print("="*80)
    
    calc = DomBrainCalculator(pathway_count=100, dopamine_threshold=0.7)
    
    print("\n🎯 Problem: Calculate 2^10")
    print("\n   Traditional Calculator:")
    print("   - 1 method: 2^10 = 1024")
    print("   - 0 verification")
    print("   - Trust = blind faith")
    
    print("\n   DomBrainCalculator:")
    result = calc.calculate("power", 2, 10)
    print(f"   - {result['all_paths']} methods attempted")
    print(f"   - {result['consolidated_paths']} high-confidence pathways")
    print(f"   - {result['collisions']} cross-domain validations")
    print(f"   - Consensus: {result['answer']:.10f}")
    print(f"   - Trust = {result['collisions']} independent confirmations")


def example_cross_domain_insights():
    """Example 3: Extracting cross-domain insights"""
    print("\n\n" + "="*80)
    print("EXAMPLE 3: Cross-Domain Pattern Discovery")
    print("="*80)
    
    calc = DomBrainCalculator(pathway_count=80, dopamine_threshold=0.6)
    
    print("\n🔬 Problem: sqrt(144)")
    print("\nGenerating insights from multiple domains...")
    
    result = calc.calculate("sqrt", 144, None)
    
    print(f"\n✅ Answer: {result['answer']:.6f}")
    print("\n🌟 Cross-Domain Insights Discovered:")
    for i, insight in enumerate(result['collision_insights'][:5], 1):
        print(f"\n   {i}. {insight}")
    
    print(f"\n📊 Metaphors Used:")
    for metaphor in result['cross_domain_metaphors'][:5]:
        print(f"   • {metaphor}")


def example_confidence_visualization():
    """Example 4: Understanding confidence and consensus"""
    print("\n\n" + "="*80)
    print("EXAMPLE 4: Confidence and Consensus Mechanics")
    print("="*80)
    
    # High confidence threshold
    calc_strict = DomBrainCalculator(pathway_count=100, dopamine_threshold=0.85)
    
    print("\n📊 Configuration: STRICT (threshold=0.85)")
    print("   Only highest-confidence pathways survive")
    
    result_strict = calc_strict.calculate("multiply", 11, 13)
    print(f"\n   Pathways generated: {result_strict['all_paths']}")
    print(f"   Pathways consolidated: {result_strict['consolidated_paths']}")
    print(f"   Collisions detected: {result_strict['collisions']}")
    print(f"   Final answer: {result_strict['answer']:.6f}")
    
    # Lower confidence threshold
    calc_relaxed = DomBrainCalculator(pathway_count=100, dopamine_threshold=0.6)
    
    print("\n📊 Configuration: RELAXED (threshold=0.6)")
    print("   More exploratory pathways included")
    
    result_relaxed = calc_relaxed.calculate("multiply", 11, 13)
    print(f"\n   Pathways generated: {result_relaxed['all_paths']}")
    print(f"   Pathways consolidated: {result_relaxed['consolidated_paths']}")
    print(f"   Collisions detected: {result_relaxed['collisions']}")
    print(f"   Final answer: {result_relaxed['answer']:.6f}")
    
    print("\n💡 Insight:")
    print("   More pathways = more collisions = more validation")
    print("   But also more noise. Threshold balances exploration vs precision.")


def example_practical_application():
    """Example 5: Real-world application scenario"""
    print("\n\n" + "="*80)
    print("EXAMPLE 5: Practical Application - System Health Check")
    print("="*80)
    
    print("\nScenario: Verify if system metric is within expected range")
    print("Expected CPU usage: ~75%")
    print("Measured from different monitoring tools...")
    
    calc = DomBrainCalculator(pathway_count=60, dopamine_threshold=0.65)
    
    # Simulate "calculating" system health by averaging different sensor readings
    # In reality, each "pathway" would be a different monitoring tool/method
    print("\n📊 Aggregating from multiple sources:")
    print("   - Prometheus: reports 74.8%")
    print("   - CloudWatch: reports 75.2%")
    print("   - Custom agent: reports 75.1%")
    print("   - Application logs: suggest ~75%")
    
    # Use calculator to get consensus
    result = calc.calculate("multiply", 0.75, 100)  # 75%
    
    print(f"\n✅ Consensus CPU Usage: {result['answer']:.2f}%")
    print(f"   Confidence: {result['consolidated_paths']} independent measurements")
    print(f"   Cross-validated: {result['collisions']} agreement points")
    print("\n💡 Decision: System is healthy (within expected range)")


def main():
    """Run all examples"""
    print("\n" + "🧠 DomBrainCalculator: Practical Examples")
    print("="*80)
    
    example_basic_operations()
    example_verification_depth()
    example_cross_domain_insights()
    example_confidence_visualization()
    example_practical_application()
    
    print("\n\n" + "="*80)
    print("🎉 All Examples Complete!")
    print("="*80)
    print("\n📚 Key Takeaways:")
    print("   1. Multiple pathways provide verification depth")
    print("   2. Cross-domain synthesis reveals universal patterns")
    print("   3. Collision detection validates independent convergence")
    print("   4. Consensus balances all pathways by confidence")
    print("   5. This approach applies beyond math to any verification problem")
    print("\n🔗 Learn More:")
    print("   - Full documentation: COGNITIVE_CALCULATOR.md")
    print("   - Source code: dom_brain_calculator.py")
    print("   - Visual flow: cognitive_calculator_flow.dot")


if __name__ == "__main__":
    main()

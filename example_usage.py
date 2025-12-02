#!/usr/bin/env python3
"""
Example usage of DomBrainCalculator
Demonstrates the cognitive architecture in action
"""

from dom_brain_calculator import DomBrainCalculator
import time


def example_basic_calculations():
    """Basic calculation examples"""
    print("=" * 80)
    print("EXAMPLE 1: Basic Calculations")
    print("=" * 80)
    
    calc = DomBrainCalculator(pathway_count=100)
    
    # Simple addition
    result = calc.calculate("What is 5 + 3?", 5, 3, '+')
    calc.show_work(result)
    
    # Multiplication
    result = calc.calculate("What is 12 * 7?", 12, 7, '*')
    calc.show_work(result)
    
    # Show session stats
    print(f"\n📊 Session: {len(calc.history)} calculations, {calc.dopamine_hits} dopamine hits\n")


def example_rediscovery():
    """Demonstrate dopamine hit mechanism"""
    print("=" * 80)
    print("EXAMPLE 2: Rediscovery & Dopamine Hits")
    print("=" * 80)
    
    calc = DomBrainCalculator(pathway_count=50)
    
    problem = "What is 10 + 5?"
    
    # First time - no dopamine hit
    print("\n🔍 First encounter with problem...")
    result1 = calc.calculate(problem, 10, 5, '+')
    print(f"   Answer: {result1['answer']:.2f}")
    print(f"   Dopamine hit: {result1['dopamine_hit']}")
    
    # Second time - dopamine hit!
    print("\n🔍 Rediscovering the problem...")
    result2 = calc.calculate(problem, 10, 5, '+')
    print(f"   Answer: {result2['answer']:.2f}")
    print(f"   Dopamine hit: {result2['dopamine_hit']} 🎉")
    
    # Third time - another dopamine hit!
    print("\n🔍 Third time's the charm...")
    result3 = calc.calculate(problem, 10, 5, '+')
    print(f"   Answer: {result3['answer']:.2f}")
    print(f"   Dopamine hit: {result3['dopamine_hit']} 🎉")
    
    print(f"\n📊 Total dopamine hits: {calc.dopamine_hits}\n")


def example_collision_analysis():
    """Demonstrate collision detection"""
    print("=" * 80)
    print("EXAMPLE 3: Collision Detection & Insights")
    print("=" * 80)
    
    calc = DomBrainCalculator(pathway_count=100)
    
    result = calc.calculate("What is 8 * 8?", 8, 8, '*')
    
    print(f"\n💥 Detected {result['collision_count']} collisions!")
    print(f"\n🔬 Collision Details:")
    
    for i, collision in enumerate(result['collisions'][:3], 1):
        print(f"\n   Collision {i}:")
        print(f"   {collision.insight}")
        print(f"   Strength: {collision.collision_strength:.2f}")
        print(f"   Synthesis: {collision.synthesis_result:.4f}")
        print(f"   Pathways involved:")
        for path in collision.paths[:5]:
            print(f"      - {path.pathway_type.value}: {path.result:.4f} (conf={path.confidence:.2%})")
    
    print()


def example_pathway_diversity():
    """Show pathway diversity"""
    print("=" * 80)
    print("EXAMPLE 4: Pathway Diversity")
    print("=" * 80)
    
    calc = DomBrainCalculator(pathway_count=100)
    
    result = calc.calculate("What is 7 + 3?", 7, 3, '+')
    
    # Count pathway types
    from collections import Counter
    pathway_counts = Counter(p.pathway_type.value for p in result['consolidated_paths'])
    
    print(f"\n🌟 Consolidated {len(result['consolidated_paths'])} pathways across domains:")
    for pathway_type, count in pathway_counts.most_common():
        print(f"   • {pathway_type}: {count} pathways")
    
    print(f"\n🎯 Confidence distribution:")
    high_conf = sum(1 for p in result['consolidated_paths'] if p.confidence > 0.7)
    med_conf = sum(1 for p in result['consolidated_paths'] if 0.4 <= p.confidence <= 0.7)
    low_conf = sum(1 for p in result['consolidated_paths'] if p.confidence < 0.4)
    
    print(f"   • High confidence (>70%): {high_conf} pathways")
    print(f"   • Medium confidence (40-70%): {med_conf} pathways")
    print(f"   • Exploratory (<40%): {low_conf} pathways")
    
    print()


def example_comparison():
    """Compare with traditional calculation"""
    print("=" * 80)
    print("EXAMPLE 5: Traditional vs Cognitive Comparison")
    print("=" * 80)
    
    calc = DomBrainCalculator(pathway_count=100)
    
    a, b = 15, 8
    traditional = a * b
    
    result = calc.calculate(f"What is {a} * {b}?", a, b, '*')
    
    print(f"\n🔢 Traditional Calculator:")
    print(f"   Method: 1 pathway (direct multiplication)")
    print(f"   Answer: {traditional}")
    print(f"   Confidence: 100%")
    print(f"   Insights: 0")
    
    print(f"\n🧠 Cognitive Calculator:")
    print(f"   Methods: {result['pathway_count']} pathways")
    print(f"   Answer: {result['answer']:.6f}")
    print(f"   Confidence: {result['confidence']:.2%}")
    print(f"   Insights: {result['collision_count']} collisions")
    
    diff = abs(result['answer'] - traditional)
    diff_pct = (diff / traditional) * 100
    
    print(f"\n📊 Analysis:")
    print(f"   Difference: {diff:.6f} ({diff_pct:.4f}%)")
    print(f"   Verification: {'✅ Consensus confirms traditional answer' if diff_pct < 0.5 else '⚠️ Exploring alternatives'}")
    
    print()


def main():
    """Run all examples"""
    print("\n" + "=" * 80)
    print("🧠 DomBrainCalculator - Example Usage")
    print("=" * 80)
    print("\nThis demonstrates the cognitive architecture implementation:")
    print("  • Divergent thinking (100+ pathways)")
    print("  • Memory consolidation (pruning)")
    print("  • Cross-domain pattern matching")
    print("  • Collision detection (insights)")
    print("  • Consensus synthesis")
    print("\n" + "=" * 80 + "\n")
    
    time.sleep(1)
    
    # Run examples
    example_basic_calculations()
    time.sleep(1)
    
    example_rediscovery()
    time.sleep(1)
    
    example_collision_analysis()
    time.sleep(1)
    
    example_pathway_diversity()
    time.sleep(1)
    
    example_comparison()
    
    print("=" * 80)
    print("✅ Examples Complete!")
    print("=" * 80)
    print("\nKey Takeaways:")
    print("  • Traditional calculators use 1 method")
    print("  • DomBrain uses 100+ methods with consensus")
    print("  • Collisions reveal insights from pattern convergence")
    print("  • Rediscovery triggers dopamine (engagement loop)")
    print("  • Cross-domain synthesis mirrors human creativity")
    print("\n" + "=" * 80 + "\n")


if __name__ == "__main__":
    main()

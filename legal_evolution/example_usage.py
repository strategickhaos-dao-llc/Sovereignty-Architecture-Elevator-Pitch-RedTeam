#!/usr/bin/env python3
"""
Example usage of the Legal Synthesizer Evolution Engine (LSEE)

This script demonstrates:
1. Running custom evolution with different parameters
2. Archiving external AI conversations
3. Analyzing ledger output
4. Extracting best strategies by type
"""

import json
from pathlib import Path
from legal_evolution_synthesizer import (
    LegalComplianceJudge,
    LegalEvolutionEngine,
    LegalStrategy,
    ExternalConversationArchive,
    US_CODES,
    BASE_BACKGROUND_CHECK_STRATEGY,
    BASE_OSINT_STRATEGY,
    BASE_SKIP_TRACE_STRATEGY,
)


def example_1_basic_evolution():
    """Example 1: Basic evolution run with default parameters."""
    print("\n" + "=" * 70)
    print("EXAMPLE 1: Basic Evolution Run")
    print("=" * 70)
    
    judge = LegalComplianceJudge(US_CODES)
    engine = LegalEvolutionEngine(judge=judge, population_size=8, generations=3)
    
    base_strategies = [
        LegalStrategy(BASE_BACKGROUND_CHECK_STRATEGY, generation=0, strategy_type="background_check"),
        LegalStrategy(BASE_OSINT_STRATEGY, generation=0, strategy_type="osint"),
    ]
    
    engine.seed_population(base_strategies)
    engine.run()


def example_2_custom_strategy():
    """Example 2: Evolve a custom strategy type."""
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Custom Strategy Evolution")
    print("=" * 70)
    
    custom_strategy = """
    Social media investigation must respect platform terms of service.
    No unauthorized account access or credential harvesting.
    Document all publicly visible profile information legally accessed.
    Comply with CFAA restrictions on computer system access.
    Maintain ethical standards for investigative journalism and research.
    Respect privacy expectations for non-public communications.
    """
    
    judge = LegalComplianceJudge(US_CODES)
    engine = LegalEvolutionEngine(
        judge=judge,
        population_size=6,
        mutation_rate=0.4,  # Higher mutation for more variation
        generations=4
    )
    
    base_strategies = [
        LegalStrategy(custom_strategy, generation=0, strategy_type="social_media_investigation"),
        LegalStrategy(BASE_OSINT_STRATEGY, generation=0, strategy_type="osint"),
    ]
    
    engine.seed_population(base_strategies)
    engine.run()


def example_3_archive_conversations():
    """Example 3: Archive multiple AI conversations."""
    print("\n" + "=" * 70)
    print("EXAMPLE 3: Archiving AI Conversations")
    print("=" * 70)
    
    archive = ExternalConversationArchive(Path("external_ai_ledger.jsonl"))
    
    # Archive the original Claude conversation
    archive.archive_conversation(
        source_url="https://claude.ai/share/777c7e93-fb67-4026-8370-1b1588c5df56",
        summary="Design of meta-evolution and legal synthesizer engine.",
        conversation_type="design_discussion",
        tags=["legal", "evolution", "compliance", "LSEE"]
    )
    
    # Archive a hypothetical follow-up discussion
    archive.archive_conversation(
        source_url="https://claude.ai/share/example-123",
        summary="Discussion of FCRA compliance requirements for background checks.",
        conversation_type="legal_research",
        tags=["FCRA", "background_check", "compliance"]
    )
    
    # Archive operational decision
    archive.archive_conversation(
        source_url="https://claude.ai/share/example-456",
        summary="Operational decision to implement OSINT workflow v2 with enhanced privacy safeguards.",
        conversation_type="operational_decision",
        tags=["OSINT", "privacy", "workflow"]
    )
    
    print("\n📚 Recent Archives:")
    for entry in archive.list_archives(limit=5):
        print(f"  [{entry['timestamp']}] {entry['type']}")
        print(f"    {entry['summary']}")
        print(f"    Tags: {', '.join(entry['tags'])}")
        print()


def example_4_analyze_ledger():
    """Example 4: Analyze evolution ledger."""
    print("\n" + "=" * 70)
    print("EXAMPLE 4: Ledger Analysis")
    print("=" * 70)
    
    ledger_path = Path("legal_evolution_ledger.jsonl")
    
    if not ledger_path.exists():
        print("⚠️  No ledger found. Run evolution first!")
        return
    
    strategies = []
    with open(ledger_path, 'r') as f:
        for line in f:
            strategies.append(json.loads(line))
    
    # Group by strategy type
    by_type = {}
    for s in strategies:
        stype = s.get('strategy_type', 'unknown')
        if stype not in by_type:
            by_type[stype] = []
        by_type[stype].append(s)
    
    print(f"\n📊 Total Entries: {len(strategies)}")
    print(f"📋 Strategy Types: {len(by_type)}")
    
    for stype, entries in by_type.items():
        compliant = [e for e in entries if e.get('compliant', False)]
        if entries:
            avg_fitness = sum(e.get('fitness', 0) for e in entries) / len(entries)
            max_gen = max(e.get('generation', 0) for e in entries)
            
            print(f"\n  {stype.upper()}")
            print(f"    Entries: {len(entries)}")
            print(f"    Compliant: {len(compliant)} ({len(compliant)/len(entries)*100:.1f}%)")
            print(f"    Avg Fitness: {avg_fitness:.2f}")
            print(f"    Max Generation: {max_gen}")
            
            # Find best
            if compliant:
                best = max(compliant, key=lambda x: x.get('fitness', 0))
                print(f"    Best Fitness: {best.get('fitness', 0):.2f} (Gen {best.get('generation', 0)})")


def example_5_extract_best_strategies():
    """Example 5: Extract best strategy for each type."""
    print("\n" + "=" * 70)
    print("EXAMPLE 5: Extract Best Strategies")
    print("=" * 70)
    
    ledger_path = Path("legal_evolution_ledger.jsonl")
    
    if not ledger_path.exists():
        print("⚠️  No ledger found. Run evolution first!")
        return
    
    strategies = []
    with open(ledger_path, 'r') as f:
        for line in f:
            strategies.append(json.loads(line))
    
    # Group by type and find best
    by_type = {}
    for s in strategies:
        if not s.get('compliant', False):
            continue
        
        stype = s.get('strategy_type', 'unknown')
        if stype not in by_type or s.get('fitness', 0) > by_type[stype].get('fitness', 0):
            by_type[stype] = s
    
    print(f"\n🏆 Best Strategies by Type:")
    for stype, strategy in by_type.items():
        print(f"\n  {'=' * 66}")
        print(f"  Type: {stype.upper()}")
        print(f"  Fitness: {strategy.get('fitness', 0):.2f}")
        print(f"  Generation: {strategy.get('generation', 0)}")
        print(f"  ID: {strategy.get('strategy_id', 'unknown')}")
        print(f"  {'=' * 66}")
        print(f"  {strategy.get('snippet', 'N/A')}")
    
    # Suggest saving to files
    print(f"\n💡 Tip: Export these to your SOP vault:")
    for stype in by_type.keys():
        filename = f"{stype.replace('_', '-')}-procedure-lsee.md"
        print(f"   - {filename}")


if __name__ == "__main__":
    print("🧬 Legal Synthesizer Evolution Engine - Examples")
    print("=" * 70)
    print("\nThis script demonstrates various LSEE usage patterns.")
    print("Choose an example to run:\n")
    print("  1. Basic evolution run")
    print("  2. Custom strategy evolution")
    print("  3. Archive AI conversations")
    print("  4. Analyze evolution ledger")
    print("  5. Extract best strategies")
    print("  6. Run all examples\n")
    
    choice = input("Enter choice (1-6): ").strip()
    
    if choice == "1":
        example_1_basic_evolution()
    elif choice == "2":
        example_2_custom_strategy()
    elif choice == "3":
        example_3_archive_conversations()
    elif choice == "4":
        example_4_analyze_ledger()
    elif choice == "5":
        example_5_extract_best_strategies()
    elif choice == "6":
        print("\n🚀 Running all examples...\n")
        example_1_basic_evolution()
        example_2_custom_strategy()
        example_3_archive_conversations()
        example_4_analyze_ledger()
        example_5_extract_best_strategies()
    else:
        print("❌ Invalid choice. Run with 1-6.")
    
    print("\n✨ Examples complete!")

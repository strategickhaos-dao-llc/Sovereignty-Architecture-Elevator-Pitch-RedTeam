#!/usr/bin/env python3
"""
Sovereign Cognitive OS - Main Entry Point

SPL (Sovereign Pattern Language) compliant CLI interface for the
Pattern-Dominant Cognitive Architecture.

Modes:
- diagnose: Differential reasoning and contradiction resolution
- experiment: Pattern exploration and schema synthesis

"The brain does not recall — it reconstructs."
"""

import argparse
import json
import sys
from pathlib import Path
from typing import List, Optional

try:
    # When run as module from src directory
    from swarm.cognitive_os import (
        CognitiveOS,
        Pattern,
        Schema,
    )
except ModuleNotFoundError:
    # When run from repository root
    from src.swarm.cognitive_os import (
        CognitiveOS,
        Pattern,
        Schema,
    )


def diagnose_mode(cos: CognitiveOS, symptoms: List[str], output: Optional[Path]) -> int:
    """
    SPL Diagnose Mode

    Run differential diagnosis on observed symptoms using
    House-style reasoning.

    Args:
        cos: Cognitive OS instance
        symptoms: List of symptoms to diagnose
        output: Optional output path for results

    Returns:
        Exit code (0 for success)
    """
    print("=" * 60)
    print("SOVEREIGN COGNITIVE OS - DIAGNOSE MODE")
    print("=" * 60)
    print()

    if not symptoms:
        print("Error: No symptoms provided for diagnosis")
        print("Usage: python -m src.main diagnose --symptom 'symptom1' --symptom 'symptom2'")
        return 1

    print("Symptoms received:")
    for i, symptom in enumerate(symptoms, 1):
        print(f"  {i}. {symptom}")
    print()

    # Run differential diagnosis
    print("Running differential diagnosis...")
    print("-" * 40)
    diagnosis = cos.diagnose(symptoms)

    # Display results
    print()
    print("DIAGNOSIS RESULTS")
    print("-" * 40)

    print("\nHypotheses (ranked by confidence):")
    for i, hyp in enumerate(diagnosis["hypotheses"], 1):
        confidence_bar = "█" * int(hyp["confidence"] * 10) + "░" * (10 - int(hyp["confidence"] * 10))
        print(f"\n  {i}. {hyp['statement']}")
        print(f"     Confidence: [{confidence_bar}] {hyp['confidence']:.2f}")

        if hyp["supporting_evidence"]:
            print("     Supporting evidence:")
            for ev in hyp["supporting_evidence"]:
                print(f"       + {ev}")

        if hyp["contradicting_evidence"]:
            print("     Contradicting evidence:")
            for ev in hyp["contradicting_evidence"]:
                print(f"       - {ev}")

    print("\nRecommended tests:")
    for test in diagnosis["recommended_tests"]:
        print(f"  → {test}")

    print(f"\nMost likely diagnosis: {diagnosis['most_likely']}")

    # Export if output path provided
    if output:
        output_path = cos.export(diagnosis, output)
        print(f"\nResults exported to: {output_path}")

    print()
    print("=" * 60)
    return 0


def experiment_mode(
    cos: CognitiveOS,
    input_data: Optional[str],
    input_file: Optional[Path],
    output: Optional[Path],
) -> int:
    """
    SPL Experiment Mode

    Explore patterns and synthesize schemas from input data.

    Args:
        cos: Cognitive OS instance
        input_data: Direct input string
        input_file: Path to input file
        output: Optional output path for results

    Returns:
        Exit code (0 for success)
    """
    print("=" * 60)
    print("SOVEREIGN COGNITIVE OS - EXPERIMENT MODE")
    print("=" * 60)
    print()

    # Get input data
    if input_file:
        if not input_file.exists():
            print(f"Error: Input file not found: {input_file}")
            return 1
        input_data = input_file.read_text()
        print(f"Input loaded from: {input_file}")
    elif input_data:
        print("Input received from command line")
    else:
        print("Reading input from stdin...")
        input_data = sys.stdin.read()

    if not input_data or not input_data.strip():
        print("Error: No input data provided")
        return 1

    print(f"\nInput preview: {input_data[:100]}...")
    print()

    # Phase 1: Pattern Recognition
    print("PHASE 1: PATTERN RECOGNITION")
    print("-" * 40)
    patterns = cos.recognize(input_data)

    if not patterns:
        print("No patterns recognized in input data")
        print("Try providing more structured input with:")
        print("  - Hierarchies (->)")
        print("  - Modules (class, component)")
        print("  - Protocols (request, response)")
        return 0

    print(f"Recognized {len(patterns)} pattern(s):")
    for p in patterns:
        confidence_bar = "█" * int(p.confidence * 10) + "░" * (10 - int(p.confidence * 10))
        print(f"  • {p.name}")
        print(f"    Type: {p.type.value}")
        print(f"    Confidence: [{confidence_bar}] {p.confidence:.2f}")
        print()

    # Phase 2: Pattern Synthesis
    if len(patterns) > 1:
        print("PHASE 2: PATTERN SYNTHESIS")
        print("-" * 40)
        synthesized = cos.pattern_engine.synthesize(patterns)
        print(f"Synthesized pattern: {synthesized.name}")
        print(f"  Combined confidence: {synthesized.confidence:.2f}")
        print(f"  Related patterns: {len(synthesized.related_patterns)}")
        patterns.append(synthesized)
        print()

    # Phase 3: Schema Creation
    print("PHASE 3: SCHEMA SYNTHESIS")
    print("-" * 40)
    schema = cos.create_schema(
        name="Experimental Schema",
        patterns=patterns,
        constraints=["Auto-generated from experiment mode"],
    )
    print(f"Created schema: {schema.name}")
    print(f"  ID: {schema.id}")
    print(f"  Patterns: {len(schema.patterns)}")
    print(f"  Hierarchy nodes: {len(schema.hierarchy)}")
    print()

    # Phase 4: Architecture Derivation
    print("PHASE 4: ARCHITECTURE DERIVATION")
    print("-" * 40)
    architecture = cos.schema_synthesizer.derive_architecture(schema)
    print("Architecture components:")
    for comp in architecture["components"]:
        print(f"  • {comp['name']} ({comp['type']})")
    print()

    # Export if output path provided
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        schema_path = cos.export(schema, output)
        print(f"Schema exported to: {schema_path}")

        # Also export patterns
        patterns_dir = output.parent / "patterns"
        patterns_dir.mkdir(parents=True, exist_ok=True)
        for p in patterns:
            pattern_path = cos.export(p, patterns_dir / f"{p.id}.md")
            print(f"Pattern exported to: {pattern_path}")

    print()
    print("=" * 60)
    print("Experiment complete. Use the patterns and schemas for further development.")
    print("=" * 60)
    return 0


def info_mode() -> int:
    """
    Display information about the Cognitive OS.

    Returns:
        Exit code (0 for success)
    """
    print("=" * 60)
    print("SOVEREIGN COGNITIVE OS - INFORMATION")
    print("=" * 60)
    print()
    print("Pattern-Dominant Cognitive Architecture v1.0")
    print()
    print("Core Components:")
    print("  • Pattern Engine - Pattern recognition and synthesis")
    print("  • Schema Synthesizer - Architecture creation")
    print("  • Contradiction Resolver - House-style differential diagnosis")
    print("  • Context Interpreter - Multi-agent mental model")
    print("  • Externalization Adapter - Vim + CLI integration")
    print()
    print("Modes:")
    print("  diagnose  - Differential reasoning on symptoms")
    print("  experiment - Pattern exploration and schema synthesis")
    print("  info      - Display this information")
    print()
    print("Documentation:")
    print("  docs/PATTERN_DOMINANT_COGNITIVE_ARCHITECTURE.md")
    print()
    print("\"The brain does not recall — it reconstructs.\"")
    print()
    print("=" * 60)
    return 0


def main() -> int:
    """
    SPL Main Entry Point

    Parse arguments and dispatch to appropriate mode.

    Returns:
        Exit code
    """
    parser = argparse.ArgumentParser(
        description="Sovereign Cognitive OS - Pattern-Dominant Cognitive Architecture",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Diagnose symptoms
  python -m src.main diagnose --symptom "Service timeout errors" --symptom "High CPU usage"

  # Experiment with input data
  python -m src.main experiment --input "The module handles request-response protocol"

  # Experiment from file
  python -m src.main experiment --file input.txt --output results/schema.md

  # Show information
  python -m src.main info
        """,
    )

    parser.add_argument(
        "mode",
        choices=["diagnose", "experiment", "info"],
        help="Operating mode",
    )

    parser.add_argument(
        "--symptom",
        action="append",
        dest="symptoms",
        help="Symptom for diagnosis (can be specified multiple times)",
    )

    parser.add_argument(
        "--input",
        dest="input_data",
        help="Direct input data for experiment mode",
    )

    parser.add_argument(
        "--file",
        type=Path,
        dest="input_file",
        help="Input file path for experiment mode",
    )

    parser.add_argument(
        "--output",
        type=Path,
        help="Output path for results",
    )

    parser.add_argument(
        "--output-base",
        type=Path,
        default=Path.cwd(),
        help="Base path for outputs (default: current directory)",
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON (where applicable)",
    )

    args = parser.parse_args()

    # Initialize Cognitive OS
    cos = CognitiveOS(output_path=args.output_base)

    # Dispatch to mode
    if args.mode == "diagnose":
        return diagnose_mode(cos, args.symptoms or [], args.output)
    elif args.mode == "experiment":
        return experiment_mode(cos, args.input_data, args.input_file, args.output)
    elif args.mode == "info":
        return info_mode()
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())

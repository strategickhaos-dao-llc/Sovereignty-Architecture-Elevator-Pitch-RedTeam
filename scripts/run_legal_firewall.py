#!/usr/bin/env python3
"""
Legal Firewall Runner Script
Strategickhaos DAO LLC

This script runs the Legal Firewall Engine to analyze legal documents
and generate compliance requirements for the DAO.

Usage:
    python scripts/run_legal_firewall.py [--stubs] [--todos] [--json]

Options:
    --stubs     Generate stub files for uncovered requirements
    --todos     Generate TODO markdown file
    --json      Output report as JSON instead of Markdown
"""

import argparse
import json
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from legal_firewall import LegalFirewallEngine


def dummy_llm(prompt: str) -> str:
    """
    Placeholder LLM callable.
    In production, wire this to your offline bridge or LLM API.
    
    Returns empty JSON array to fall back to regex-based extraction.
    """
    return "[]"


def main():
    parser = argparse.ArgumentParser(
        description="Run the Legal Firewall Engine for LB-GSE compliance analysis"
    )
    parser.add_argument(
        "--stubs",
        action="store_true",
        help="Generate stub files for uncovered requirements"
    )
    parser.add_argument(
        "--todos",
        action="store_true",
        help="Generate TODO markdown file"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output report as JSON instead of Markdown"
    )
    parser.add_argument(
        "--llm",
        action="store_true",
        help="Use LLM for enhanced extraction (requires implementation)"
    )
    parser.add_argument(
        "--legal-paths",
        nargs="+",
        default=[
            "legal/OPERATING_AGREEMENT.md",
            "legal/LEGAL_CONTRACT.md",
        ],
        help="Paths to legal documents (relative to repo root)"
    )
    parser.add_argument(
        "--registry",
        default=".strategickhaos/component_registry.yml",
        help="Path to component registry YAML"
    )
    
    args = parser.parse_args()
    
    # Initialize engine
    llm_callable = dummy_llm if args.llm else None
    engine = LegalFirewallEngine(repo_path=".", llm_callable=llm_callable)
    
    print("=" * 60)
    print("🔥 LEGAL FIREWALL ENGINE - LB-GSE Analysis")
    print("=" * 60)
    print(f"\n📄 Analyzing legal documents:")
    for path in args.legal_paths:
        exists = "✅" if Path(path).exists() else "❌"
        print(f"   {exists} {path}")
    
    print(f"\n📦 Component registry: {args.registry}")
    print(f"📝 Generate stubs: {'Yes' if args.stubs else 'No'}")
    print(f"✅ Generate TODOs: {'Yes' if args.todos else 'No'}")
    print("\n" + "-" * 60)
    
    # Run analysis
    report = engine.run_full_analysis(
        legal_paths=args.legal_paths,
        component_index_path=args.registry,
        auto_write_stubs=args.stubs,
        auto_create_issues=args.todos,
    )
    
    # Output report
    if args.json:
        print(json.dumps(report.to_dict(), indent=2))
    else:
        print(report.to_markdown())
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 ANALYSIS SUMMARY")
    print("=" * 60)
    print(f"   Legal Primitives Extracted: {len(report.primitives)}")
    print(f"   Capability Requirements:    {report.total_requirements}")
    print(f"   Components Discovered:      {len(report.components)}")
    print(f"   Requirements Covered:       {report.covered_requirements}/{report.total_requirements}")
    print(f"   Coverage Percentage:        {report.coverage_percentage:.1f}%")
    print(f"   High-Priority Gaps:         {len(report.high_priority_gaps)}")
    
    if args.stubs:
        stubs_with_path = [g for g in report.gaps if g.stub_path]
        print(f"\n📁 Generated {len(stubs_with_path)} stub files in .strategickhaos/requirements_stubs/")
    
    if args.todos:
        print(f"\n✅ Generated TODO file at .strategickhaos/legal_firewall_todos.md")
    
    print("\n🔥 Analysis complete!")
    
    # Return exit code based on coverage
    if report.coverage_percentage < 50:
        return 1  # Low coverage warning
    return 0


if __name__ == "__main__":
    sys.exit(main())

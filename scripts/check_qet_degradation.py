#!/usr/bin/env python3
"""
QET Degradation Check Script
Used by CI to analyze benchmark results and detect degradation.
"""

import json
import sys
from pathlib import Path


def check_degradation(results_path: str = "benchmarks/reports/qet_benchmark_results.json") -> int:
    """
    Check benchmark results for degradation.
    
    Returns:
        0 if OK, 1 if failed, 2 if warnings
    """
    results_file = Path(results_path)
    
    if not results_file.exists():
        print(f"Results file not found: {results_path}")
        return 1
    
    with open(results_file, "r") as f:
        results = json.load(f)
    
    failed = sum(1 for r in results if r.get("status") == "FAIL")
    warned = sum(1 for r in results if r.get("status") == "WARN")
    total = len(results)
    
    print(f"Tests: {total} | Failed: {failed} | Warnings: {warned}")
    
    # Output details for CI
    for r in results:
        status = r.get("status", "UNKNOWN")
        name = r.get("name", "Unknown")
        if status == "FAIL":
            reason = r.get("reason", "No reason provided")
            print(f"::error::{name} - {reason}")
        elif status == "WARN":
            reason = r.get("reason", "No reason provided")
            print(f"::warning::{name} - {reason}")
    
    if failed > 0:
        print("::error::Tokenizer tests failed - evolution may be required")
        return 1
    elif warned > 2:
        print("::warning::Multiple tokenizer warnings - review recommended")
        return 2
    
    return 0


if __name__ == "__main__":
    results_path = sys.argv[1] if len(sys.argv) > 1 else "benchmarks/reports/qet_benchmark_results.json"
    sys.exit(check_degradation(results_path))

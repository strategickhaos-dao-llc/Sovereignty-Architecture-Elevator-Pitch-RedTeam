#!/usr/bin/env python3
"""
State Updater for Strategickhaos Governance Board Layer

This script validates and updates the state snapshot file.
Run periodically to maintain accurate governance state.

Usage:
    python state_updater.py [--validate-only] [--update-timestamp]
"""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

# Configuration
SCRIPT_DIR = Path(__file__).parent
STATE_FILE = SCRIPT_DIR / "strategickhaos_state_snapshot.json"
RISKS_FILE = SCRIPT_DIR.parent / "risks" / "risks_from_corpus.json"


def load_json(filepath: Path) -> dict:
    """Load JSON file and return contents."""
    if not filepath.exists():
        print(f"Warning: File not found: {filepath}")
        return {}
    with open(filepath, "r") as f:
        return json.load(f)


def save_json(filepath: Path, data: dict) -> None:
    """Save data to JSON file."""
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Saved: {filepath}")


def validate_state(state: dict) -> list:
    """Validate state snapshot structure and return issues."""
    issues = []
    
    required_keys = ["version", "timestamp", "entity", "maturity", 
                     "infrastructure", "risks", "governance"]
    
    for key in required_keys:
        if key not in state:
            issues.append(f"Missing required key: {key}")
    
    # Validate maturity
    if "maturity" in state:
        maturity = state["maturity"]
        if "overall" in maturity:
            if not 0 <= maturity["overall"] <= 100:
                issues.append(f"Invalid maturity score: {maturity['overall']}")
        
        if "categories" in maturity:
            for cat, data in maturity["categories"].items():
                if "score" in data and not 0 <= data["score"] <= 100:
                    issues.append(f"Invalid {cat} score: {data['score']}")
    
    # Validate risks
    if "risks" in state:
        risks = state["risks"]
        if "count" in risks and "top_risks" in risks:
            if len(risks["top_risks"]) > risks["count"]:
                issues.append("top_risks exceeds risk count")
    
    return issues


def calculate_maturity(state: dict) -> int:
    """Calculate overall maturity from category scores."""
    if "maturity" not in state or "categories" not in state["maturity"]:
        return 0
    
    categories = state["maturity"]["categories"]
    if not categories:
        return 0
    
    total = sum(cat.get("score", 0) for cat in categories.values())
    return round(total / len(categories))


def update_timestamp(state: dict) -> dict:
    """Update the timestamp in state snapshot."""
    now = datetime.now(timezone.utc).isoformat()
    state["timestamp"] = now
    if "metadata" in state:
        state["metadata"]["last_updated"] = now
    return state


def sync_risk_count(state: dict) -> dict:
    """Sync risk count from risks file if available."""
    risks_data = load_json(RISKS_FILE)
    
    if risks_data and "risks" in risks_data:
        risk_list = risks_data["risks"]
        state["risks"]["count"] = len(risk_list)
        
        # Count by severity
        severity_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
        for risk in risk_list:
            severity = risk.get("severity", "medium").lower()
            if severity in severity_counts:
                severity_counts[severity] += 1
        
        state["risks"].update(severity_counts)
    
    return state


def main():
    """Main entry point."""
    print("=" * 50)
    print("Strategickhaos State Updater")
    print("=" * 50)
    
    # Parse arguments
    validate_only = "--validate-only" in sys.argv
    update_ts = "--update-timestamp" in sys.argv
    
    # Load current state
    print(f"\nLoading state from: {STATE_FILE}")
    state = load_json(STATE_FILE)
    
    if not state:
        print("Error: Could not load state file")
        sys.exit(1)
    
    # Validate
    print("\nValidating state structure...")
    issues = validate_state(state)
    
    if issues:
        print("\nValidation issues found:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("  ✓ State structure valid")
    
    if validate_only:
        print("\nValidation-only mode, exiting.")
        sys.exit(0 if not issues else 1)
    
    # Calculate maturity
    print("\nChecking maturity calculation...")
    calculated = calculate_maturity(state)
    current = state.get("maturity", {}).get("overall", 0)
    
    if calculated != current:
        print(f"  Maturity drift detected: {current} -> {calculated}")
        state["maturity"]["overall"] = calculated
    else:
        print(f"  ✓ Maturity consistent: {calculated}%")
    
    # Sync risks
    print("\nSyncing risk counts...")
    state = sync_risk_count(state)
    print(f"  Risks: {state['risks'].get('count', 'unknown')}")
    
    # Update timestamp if requested
    if update_ts:
        print("\nUpdating timestamp...")
        state = update_timestamp(state)
        print(f"  Timestamp: {state['timestamp']}")
    
    # Save updated state
    print("\nSaving updated state...")
    save_json(STATE_FILE, state)
    
    print("\n" + "=" * 50)
    print("State update complete")
    print("=" * 50)


if __name__ == "__main__":
    main()

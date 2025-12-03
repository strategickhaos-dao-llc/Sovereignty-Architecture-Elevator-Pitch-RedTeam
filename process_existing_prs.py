#!/usr/bin/env python3
"""
Process Existing PRs - SovereignPRManager

Scans all draft PRs, runs Legion review, synthesizes decisions,
auto-merges pure ones, and flags the rest for #requires-human.

Zero buttons. Pure sovereignty.
"""

import logging
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sovereignprmanager.core import SovereignPRManager

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Process all existing PRs in the repository."""
    logger.info("=" * 60)
    logger.info("SovereignPRManager - Processing Existing PRs")
    logger.info("=" * 60)
    
    # Get repository from environment or use default
    repo = os.environ.get(
        "GITHUB_REPOSITORY",
        "Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-"
    )
    github_token = os.environ.get("GITHUB_TOKEN")
    
    logger.info(f"Target repository: {repo}")
    
    # Initialize manager
    manager = SovereignPRManager(github_token=github_token)
    
    # Check heartbeat
    print(manager.heartbeat())
    print("Legion ready. Processing existing PRs...\n")
    
    # Process all PRs
    results = manager.process_all_prs(repo)
    
    # Output results
    print("\n" + "=" * 60)
    print("Processing Complete")
    print("=" * 60)
    print(f"Total PRs processed: {results['total']}")
    print(f"  ✓ Auto-merged: {results['merged']}")
    print(f"  ⚠ Flagged for human review: {results['flagged_for_human']}")
    print(f"  ✗ Errors: {results['errors']}")
    print("=" * 60)
    
    if results['flagged_for_human'] > 0:
        print("\nPRs requiring human review have been flagged in #requires-human")
    
    print("\nZero buttons. Pure sovereignty.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

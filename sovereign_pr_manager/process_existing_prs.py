#!/usr/bin/env python3
"""
Process Existing PRs Script
Bulk processes all open PRs through SovereignPRManager
"""

import asyncio
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from sovereign_pr_manager import SovereignPRManager
from sovereign_pr_manager.config import Settings


async def process_all_open_prs():
    """Process all existing open PRs"""
    
    print("=" * 60)
    print("🤖 SovereignPRManager - Bulk PR Processing")
    print("=" * 60)
    print(f"Timestamp: {datetime.utcnow().isoformat()}")
    print()
    
    # Load configuration
    config_path = os.getenv("SOVEREIGN_PR_CONFIG", "sovereign_pr_manager/config.yaml")
    
    if Path(config_path).exists():
        print(f"Loading config from: {config_path}")
        settings = Settings.load(config_path)
    else:
        print("Using environment variables for configuration")
        settings = Settings.load()
    
    # Validate required configuration
    if not settings.github.token:
        print("❌ Error: GITHUB_TOKEN environment variable not set")
        sys.exit(1)
    
    if not settings.github.repo:
        print("❌ Error: GITHUB_REPO environment variable not set")
        sys.exit(1)
    
    print(f"Repository: {settings.github.repo}")
    print(f"Auto-merge threshold: {settings.merge_thresholds.auto_merge:.0%}")
    print(f"Security veto threshold: {settings.merge_thresholds.security_veto:.0%}")
    print(f"Sovereignty minimum: {settings.merge_thresholds.sovereignty_minimum:.0%}")
    print()
    
    # Initialize manager
    manager = SovereignPRManager(settings=settings)
    
    # Process all open PRs
    print("Fetching open PRs...")
    report = await manager.process_all_open_prs(rate_limit_seconds=10)
    
    # Print report
    print_report(report)
    
    # Save report to file
    report_path = f"pr_processing_report_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2, default=str)
    
    print(f"\n📄 Full report saved to: {report_path}")
    
    return report


def print_report(report: dict):
    """Print formatted report"""
    
    summary = report.get("summary", {})
    results = report.get("results", [])
    
    print()
    print("=" * 60)
    print("📊 PROCESSING COMPLETE")
    print("=" * 60)
    print()
    print(f"Total PRs processed: {summary.get('total_prs', 0)}")
    print(f"✅ Auto-merged: {summary.get('auto_merged', 0)}")
    print(f"👁️ Requires review: {summary.get('requires_review', 0)}")
    print(f"🚫 Blocked: {summary.get('blocked', 0)}")
    print(f"❌ Errors: {summary.get('errors', 0)}")
    print()
    
    # Print individual PR results
    if results:
        print("-" * 60)
        print("Individual PR Results:")
        print("-" * 60)
        
        for result in results:
            pr_num = result.get("pr_number", "?")
            pr_title = result.get("pr_title", "Unknown")[:40]
            decision = result.get("decision", {})
            action = decision.get("action", "error")
            confidence = decision.get("confidence", 0)
            
            status_emoji = {
                "merge": "✅",
                "review_required": "👁️",
                "blocked": "🚫",
                "error": "❌",
            }.get(action, "❓")
            
            print(f"  {status_emoji} #{pr_num}: {pr_title}...")
            print(f"      Action: {action} | Confidence: {confidence:.0%}")
    
    print()
    print(f"Timestamp: {report.get('timestamp')}")
    print(f"Processed by: {report.get('processed_by')}")


if __name__ == "__main__":
    try:
        asyncio.run(process_all_open_prs())
    except KeyboardInterrupt:
        print("\n\n⚠️ Processing interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

"""
SovereignPRManager - Main Manager Module
Orchestrates the entire PR review and merge process
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional

from .config import Settings
from .pr_monitor import PRMonitor
from .legion_reviewer import LegionReviewer
from .conflict_detector import ConflictDetector
from .synthesis_engine import MergeDecisionEngine
from .auto_merger import AutoMerger

logger = logging.getLogger(__name__)


class SovereignPRManager:
    """
    Autonomous PR Orchestration System
    
    Zero-button operation: Copilot generates → Legion validates → System merges
    """
    
    def __init__(self, settings: Optional[Settings] = None, config_path: Optional[str] = None):
        self.settings = settings or Settings.load(config_path)
        
        # Initialize components
        self.monitor = PRMonitor(self.settings)
        self.reviewer = LegionReviewer(self.settings)
        self.conflict_detector = ConflictDetector()
        self.synthesis_engine = MergeDecisionEngine(self.settings)
        self.merger = AutoMerger(self.settings)
        
        # Track processing state
        self._processing: Dict[int, str] = {}
        self._results: Dict[int, Dict[str, Any]] = {}
    
    async def process_pr(self, pr_number: int) -> Dict[str, Any]:
        """Process a single PR through the complete pipeline"""
        
        logger.info(f"Processing PR #{pr_number}")
        self._processing[pr_number] = "fetching"
        
        try:
            # 1. Fetch PR data
            pr_data = await self.monitor.process_single_pr(pr_number)
            
            if not pr_data:
                return {
                    "pr_number": pr_number,
                    "status": "error",
                    "error": "Failed to fetch PR data",
                }
            
            # 2. Run Legion review
            self._processing[pr_number] = "reviewing"
            logger.info(f"PR #{pr_number}: Running Legion review...")
            reviews = await self.reviewer.review_pr(pr_data)
            
            # 3. Detect conflicts
            self._processing[pr_number] = "detecting_conflicts"
            logger.info(f"PR #{pr_number}: Detecting conflicts...")
            conflicts = self.conflict_detector.detect_conflicts(pr_data)
            
            # 4. Synthesize decision
            self._processing[pr_number] = "synthesizing"
            logger.info(f"PR #{pr_number}: Synthesizing decision...")
            decision = self.synthesis_engine.synthesize(reviews, conflicts, pr_data)
            
            # 5. Add review comment
            self._processing[pr_number] = "commenting"
            await self.merger.add_review_comment(pr_number, decision)
            
            # 6. Execute action
            self._processing[pr_number] = "executing"
            
            result = {
                "pr_number": pr_number,
                "pr_title": pr_data.get("title"),
                "reviews": reviews,
                "conflicts": conflicts,
                "decision": decision,
                "timestamp": datetime.utcnow().isoformat(),
            }
            
            if decision.get("action") == "merge":
                logger.info(f"PR #{pr_number}: Auto-merging...")
                merge_result = await self.merger.merge_pr(pr_number, decision, pr_data)
                result["merge_result"] = merge_result
            elif decision.get("action") == "blocked":
                logger.warning(f"PR #{pr_number}: Blocked - {decision.get('reasoning')}")
                result["status"] = "blocked"
            else:
                logger.info(f"PR #{pr_number}: Requires human review")
                result["status"] = "review_required"
            
            # Store result
            self._results[pr_number] = result
            self._processing[pr_number] = "completed"
            
            return result
            
        except Exception as e:
            logger.error(f"Error processing PR #{pr_number}: {e}")
            self._processing[pr_number] = "error"
            return {
                "pr_number": pr_number,
                "status": "error",
                "error": str(e),
            }
    
    async def process_all_open_prs(
        self,
        rate_limit_seconds: int = 10,
    ) -> Dict[str, Any]:
        """Process all open PRs in the repository"""
        
        logger.info("Fetching all open PRs...")
        prs = await self.monitor.get_open_prs()
        
        results = []
        
        for i, pr in enumerate(prs):
            pr_number = pr["number"]
            pr_title = pr.get("title", "")
            
            logger.info(f"Processing PR {i+1}/{len(prs)}: #{pr_number} - {pr_title}")
            
            result = await self.process_pr(pr_number)
            results.append(result)
            
            # Rate limit to avoid API throttling
            if i < len(prs) - 1:
                await asyncio.sleep(rate_limit_seconds)
        
        # Generate summary report
        report = self._generate_report(results)
        
        return report
    
    def _generate_report(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate summary report of bulk processing"""
        
        total = len(results)
        auto_merged = len([r for r in results if r.get("merge_result", {}).get("success")])
        review_required = len([r for r in results if r.get("decision", {}).get("action") == "review_required"])
        blocked = len([r for r in results if r.get("decision", {}).get("action") == "blocked"])
        errors = len([r for r in results if r.get("status") == "error"])
        
        report = {
            "summary": {
                "total_prs": total,
                "auto_merged": auto_merged,
                "requires_review": review_required,
                "blocked": blocked,
                "errors": errors,
            },
            "results": results,
            "timestamp": datetime.utcnow().isoformat(),
            "processed_by": "SovereignPRManager v1.0",
        }
        
        return report
    
    async def run_monitor(self) -> None:
        """Start the PR monitoring loop"""
        
        # Register callback for new PRs
        self.monitor.on_new_pr(self._on_new_pr)
        
        # Start monitoring
        await self.monitor.monitor()
    
    async def _on_new_pr(self, pr_data: Dict[str, Any]) -> None:
        """Handle new PR detected by monitor"""
        
        pr_number = pr_data.get("number")
        
        if pr_number:
            logger.info(f"New PR detected: #{pr_number} - Processing...")
            await self.process_pr(pr_number)
    
    def get_status(self, pr_number: int) -> Dict[str, Any]:
        """Get processing status for a PR"""
        
        return {
            "pr_number": pr_number,
            "processing_status": self._processing.get(pr_number, "not_started"),
            "result": self._results.get(pr_number),
        }
    
    def get_all_results(self) -> Dict[int, Dict[str, Any]]:
        """Get all processing results"""
        return self._results.copy()


async def main():
    """Main entry point for CLI usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description="SovereignPRManager - Autonomous PR Orchestration")
    parser.add_argument("--config", "-c", help="Path to config file")
    parser.add_argument("--pr", "-p", type=int, help="Process specific PR number")
    parser.add_argument("--all", "-a", action="store_true", help="Process all open PRs")
    parser.add_argument("--monitor", "-m", action="store_true", help="Start monitoring mode")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    # Configure logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    
    # Initialize manager
    manager = SovereignPRManager(config_path=args.config)
    
    if args.pr:
        # Process single PR
        result = await manager.process_pr(args.pr)
        print_result(result)
    
    elif args.all:
        # Process all open PRs
        report = await manager.process_all_open_prs()
        print_report(report)
    
    elif args.monitor:
        # Start monitoring mode
        logger.info("Starting PR monitor...")
        await manager.run_monitor()
    
    else:
        parser.print_help()


def print_result(result: Dict[str, Any]) -> None:
    """Print single PR result"""
    import json
    
    print("\n" + "=" * 60)
    print(f"PR #{result.get('pr_number')}: {result.get('pr_title', 'Unknown')}")
    print("=" * 60)
    
    decision = result.get("decision", {})
    print(f"\nAction: {decision.get('action', 'N/A')}")
    print(f"Confidence: {decision.get('confidence', 0):.2%}")
    print(f"\nReasoning:\n{decision.get('reasoning', 'N/A')}")
    
    merge_result = result.get("merge_result", {})
    if merge_result:
        print(f"\nMerge Status: {'✅ Success' if merge_result.get('success') else '❌ Failed'}")
        if merge_result.get("sha"):
            print(f"Merge SHA: {merge_result.get('sha')}")


def print_report(report: Dict[str, Any]) -> None:
    """Print bulk processing report"""
    
    summary = report.get("summary", {})
    
    print("\n" + "=" * 60)
    print("📊 BULK PROCESSING COMPLETE")
    print("=" * 60)
    print(f"Total PRs: {summary.get('total_prs', 0)}")
    print(f"Auto-merged: {summary.get('auto_merged', 0)}")
    print(f"Requires review: {summary.get('requires_review', 0)}")
    print(f"Blocked: {summary.get('blocked', 0)}")
    print(f"Errors: {summary.get('errors', 0)}")
    print(f"\nTimestamp: {report.get('timestamp')}")


if __name__ == "__main__":
    asyncio.run(main())

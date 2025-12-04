"""
PR Monitor - Watches GitHub for new PRs and publishes to NATS.

This module monitors GitHub repositories for open pull requests and
publishes events to NATS JetStream for processing by the AI Legion.

Author: SovereignPRManager Legion
"""

import asyncio
import json
import os
from datetime import datetime, timezone
from typing import Optional

import httpx
from github import Github
from nats.aio.client import Client as NATS


class PRMonitor:
    """Monitor GitHub PRs and publish events to NATS."""

    def __init__(
        self,
        github_token: str,
        repo_name: str,
        nats_url: str = "nats://localhost:4222",
    ):
        """Initialize PR Monitor.

        Args:
            github_token: GitHub Personal Access Token
            repo_name: Repository to monitor (owner/repo format)
            nats_url: NATS server URL
        """
        self.github = Github(github_token)
        self.repo = self.github.get_repo(repo_name)
        self.nats_url = nats_url
        self.nc: Optional[NATS] = None
        self._processed_prs: set[int] = set()

    async def connect_nats(self) -> None:
        """Connect to NATS JetStream."""
        self.nc = NATS()
        await self.nc.connect(self.nats_url)
        print(f"✅ Connected to NATS at {self.nats_url}")

    async def disconnect(self) -> None:
        """Disconnect from NATS."""
        if self.nc:
            await self.nc.close()
            print("🔌 Disconnected from NATS")

    async def monitor_loop(self, interval: int = 10) -> None:
        """Main monitoring loop.

        Args:
            interval: Seconds between checks
        """
        print(f"🔍 Starting PR monitor (checking every {interval}s)")

        while True:
            try:
                prs = self.repo.get_pulls(state="open")

                for pr in prs:
                    # Only process new unreviewed PRs
                    if pr.number not in self._processed_prs and not self._is_reviewed(
                        pr
                    ):
                        await self._publish_pr_event(pr)
                        self._processed_prs.add(pr.number)

                await asyncio.sleep(interval)

            except Exception as e:
                print(f"❌ Error in monitor loop: {e}")
                await asyncio.sleep(interval)

    def _is_reviewed(self, pr) -> bool:
        """Check if PR has been reviewed by Legion.

        Args:
            pr: Pull request object

        Returns:
            True if already reviewed by SovereignPRManager
        """
        comments = pr.get_issue_comments()
        for comment in comments:
            if "SovereignPRManager" in comment.body:
                return True
        return False

    async def _publish_pr_event(self, pr) -> None:
        """Publish PR to NATS for Legion review.

        Args:
            pr: Pull request object
        """
        if not self.nc:
            print("❌ Not connected to NATS")
            return

        event = {
            "type": "pr.new",
            "pr_number": pr.number,
            "title": pr.title,
            "author": pr.user.login,
            "created_at": pr.created_at.isoformat(),
            "updated_at": pr.updated_at.isoformat(),
            "url": pr.html_url,
            "diff_url": pr.diff_url,
            "files_changed": pr.changed_files,
            "additions": pr.additions,
            "deletions": pr.deletions,
            "base_branch": pr.base.ref,
            "head_branch": pr.head.ref,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        await self.nc.publish("pr.detected", json.dumps(event).encode())

        print(f"📤 Published PR #{pr.number}: {pr.title}")

    async def fetch_diff(self, diff_url: str) -> str:
        """Fetch PR diff content.

        Args:
            diff_url: URL to fetch diff from

        Returns:
            Diff content as string
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                diff_url, headers={"Accept": "application/vnd.github.v3.diff"}
            )
            return response.text


async def main() -> None:
    """Main entry point."""
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        raise ValueError("GITHUB_TOKEN environment variable required")

    repo_name = os.getenv(
        "GITHUB_REPO", "Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-"
    )
    nats_url = os.getenv("NATS_URL", "nats://localhost:4222")

    monitor = PRMonitor(
        github_token=github_token,
        repo_name=repo_name,
        nats_url=nats_url,
    )

    try:
        await monitor.connect_nats()
        await monitor.monitor_loop()
    finally:
        await monitor.disconnect()


if __name__ == "__main__":
    asyncio.run(main())

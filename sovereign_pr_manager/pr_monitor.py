"""
PR Monitor Module
Monitors GitHub for new PRs and publishes to NATS message queue
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Set, Callable, Any

import aiohttp

from .config import Settings

logger = logging.getLogger(__name__)


class PRMonitor:
    """Monitor GitHub for new PRs and publish to NATS"""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {settings.github.token}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "SovereignPRManager/1.0"
        }
        self._processed_prs: Set[int] = set()
        self._callbacks: List[Callable] = []
    
    def on_new_pr(self, callback: Callable) -> None:
        """Register callback for new PR events"""
        self._callbacks.append(callback)
    
    async def _notify_callbacks(self, pr_data: Dict[str, Any]) -> None:
        """Notify all registered callbacks"""
        for callback in self._callbacks:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(pr_data)
                else:
                    callback(pr_data)
            except Exception as e:
                logger.error(f"Callback error: {e}")
    
    async def get_open_prs(self, state: str = "open") -> List[Dict[str, Any]]:
        """Fetch all open PRs from the repository"""
        repo = self.settings.github.repo
        prs = []
        page = 1
        
        async with aiohttp.ClientSession() as session:
            while True:
                url = f"{self.base_url}/repos/{repo}/pulls?state={state}&page={page}&per_page=100"
                
                try:
                    async with session.get(url, headers=self.headers) as response:
                        if response.status != 200:
                            logger.error(f"Failed to fetch PRs: {response.status}")
                            break
                        
                        data = await response.json()
                        if not data:
                            break
                        
                        prs.extend(data)
                        page += 1
                        
                except Exception as e:
                    logger.error(f"Error fetching PRs: {e}")
                    break
        
        return prs
    
    async def get_pr_diff(self, pr_number: int) -> str:
        """Fetch the diff for a specific PR"""
        repo = self.settings.github.repo
        
        async with aiohttp.ClientSession() as session:
            url = f"{self.base_url}/repos/{repo}/pulls/{pr_number}"
            headers = {**self.headers, "Accept": "application/vnd.github.v3.diff"}
            
            try:
                async with session.get(url, headers=headers) as response:
                    if response.status != 200:
                        logger.error(f"Failed to fetch PR diff: {response.status}")
                        return ""
                    
                    return await response.text()
                    
            except Exception as e:
                logger.error(f"Error fetching PR diff: {e}")
                return ""
    
    async def get_pr_details(self, pr_number: int) -> Optional[Dict[str, Any]]:
        """Fetch detailed information for a specific PR"""
        repo = self.settings.github.repo
        
        async with aiohttp.ClientSession() as session:
            url = f"{self.base_url}/repos/{repo}/pulls/{pr_number}"
            
            try:
                async with session.get(url, headers=self.headers) as response:
                    if response.status != 200:
                        logger.error(f"Failed to fetch PR details: {response.status}")
                        return None
                    
                    return await response.json()
                    
            except Exception as e:
                logger.error(f"Error fetching PR details: {e}")
                return None
    
    async def get_pr_files(self, pr_number: int) -> List[Dict[str, Any]]:
        """Fetch the list of files changed in a PR"""
        repo = self.settings.github.repo
        files = []
        page = 1
        
        async with aiohttp.ClientSession() as session:
            while True:
                url = f"{self.base_url}/repos/{repo}/pulls/{pr_number}/files?page={page}&per_page=100"
                
                try:
                    async with session.get(url, headers=self.headers) as response:
                        if response.status != 200:
                            logger.error(f"Failed to fetch PR files: {response.status}")
                            break
                        
                        data = await response.json()
                        if not data:
                            break
                        
                        files.extend(data)
                        page += 1
                        
                except Exception as e:
                    logger.error(f"Error fetching PR files: {e}")
                    break
        
        return files
    
    def format_pr_data(self, pr: Dict[str, Any]) -> Dict[str, Any]:
        """Format PR data for processing"""
        return {
            "number": pr["number"],
            "title": pr.get("title", ""),
            "author": pr.get("user", {}).get("login", ""),
            "created_at": pr.get("created_at", ""),
            "updated_at": pr.get("updated_at", ""),
            "url": pr.get("html_url", ""),
            "diff_url": pr.get("diff_url", ""),
            "head_sha": pr.get("head", {}).get("sha", ""),
            "base_branch": pr.get("base", {}).get("ref", ""),
            "head_branch": pr.get("head", {}).get("ref", ""),
            "draft": pr.get("draft", False),
            "state": pr.get("state", ""),
            "mergeable": pr.get("mergeable", None),
            "labels": [label.get("name", "") for label in pr.get("labels", [])],
            "body": pr.get("body", ""),
        }
    
    async def monitor(self) -> None:
        """Main monitoring loop"""
        logger.info("Starting PR monitor...")
        
        while True:
            try:
                prs = await self.get_open_prs()
                
                for pr in prs:
                    pr_number = pr["number"]
                    
                    # Check if we've already processed this PR
                    if pr_number in self._processed_prs:
                        continue
                    
                    # Format and publish PR data
                    pr_data = self.format_pr_data(pr)
                    
                    logger.info(f"New PR detected: #{pr_number} - {pr_data['title']}")
                    
                    # Notify callbacks
                    await self._notify_callbacks(pr_data)
                    
                    # Mark as processed
                    self._processed_prs.add(pr_number)
                
            except Exception as e:
                logger.error(f"Monitor error: {e}")
            
            await asyncio.sleep(self.settings.poll_interval)
    
    async def process_single_pr(self, pr_number: int) -> Optional[Dict[str, Any]]:
        """Process a single PR by number"""
        pr_details = await self.get_pr_details(pr_number)
        
        if not pr_details:
            return None
        
        pr_data = self.format_pr_data(pr_details)
        pr_data["diff"] = await self.get_pr_diff(pr_number)
        pr_data["files"] = await self.get_pr_files(pr_number)
        
        return pr_data
    
    def reset_processed(self) -> None:
        """Reset the set of processed PRs"""
        self._processed_prs.clear()

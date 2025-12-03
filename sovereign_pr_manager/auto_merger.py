"""
Auto Merger Module
Autonomously merge PRs with cryptographic provenance
"""

import hashlib
import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional

import aiohttp

from .config import Settings

logger = logging.getLogger(__name__)


class AutoMerger:
    """Autonomously merge PRs with cryptographic provenance"""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {settings.github.token}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "SovereignPRManager/1.0"
        }
    
    async def merge_pr(
        self,
        pr_number: int,
        decision: Dict[str, Any],
        pr_data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Execute merge with full audit trail"""
        
        repo = self.settings.github.repo
        
        # Create provenance record
        provenance = {
            "pr_number": pr_number,
            "pr_title": decision.get("pr_title", ""),
            "decision": {
                "action": decision.get("action"),
                "confidence": decision.get("confidence"),
                "reasoning": decision.get("reasoning"),
            },
            "merged_by": "SovereignPRManager v1.0",
            "timestamp": datetime.utcnow().isoformat(),
            "git_sha": pr_data.get("head_sha") if pr_data else None,
        }
        
        # Generate cryptographic signature (BLAKE3-style hash)
        signature = self._sign_provenance(provenance)
        provenance["signature"] = signature
        
        # Generate timestamp proof (simplified)
        timestamp_proof = self._generate_timestamp_proof(provenance)
        provenance["timestamp_proof"] = timestamp_proof
        
        # Check if merge is allowed
        if decision.get("action") != "merge":
            return {
                "success": False,
                "pr_number": pr_number,
                "reason": f"Merge not authorized: {decision.get('action')}",
                "provenance": provenance,
            }
        
        # Execute merge
        try:
            merge_result = await self._execute_merge(
                repo=repo,
                pr_number=pr_number,
                decision=decision,
                provenance=provenance,
            )
            
            if merge_result.get("success"):
                # Log to Discord
                await self._notify_discord(pr_number, decision, merge_result)
                
                logger.info(f"Successfully merged PR #{pr_number}")
            
            return {
                "success": merge_result.get("success", False),
                "pr_number": pr_number,
                "merge_sha": merge_result.get("sha"),
                "provenance": provenance,
                "error": merge_result.get("error"),
            }
            
        except Exception as e:
            logger.error(f"Merge failed for PR #{pr_number}: {e}")
            return {
                "success": False,
                "pr_number": pr_number,
                "error": str(e),
                "provenance": provenance,
            }
    
    async def _execute_merge(
        self,
        repo: str,
        pr_number: int,
        decision: Dict[str, Any],
        provenance: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Execute the actual merge via GitHub API"""
        
        confidence = decision.get("confidence", 0.0)
        reasoning = decision.get("reasoning", "")
        signature = provenance.get("signature", "")[:16]
        timestamp_proof = provenance.get("timestamp_proof", "")[:16]
        
        commit_message = f"""Autonomously merged by SovereignPRManager v1.0

Confidence: {confidence:.2%}
Reviews: Multi-AI Legion review completed
Reasoning:
{reasoning}

Provenance: {signature}...
Timestamp Proof: {timestamp_proof}...
"""
        
        async with aiohttp.ClientSession() as session:
            url = f"{self.base_url}/repos/{repo}/pulls/{pr_number}/merge"
            
            async with session.put(
                url,
                headers=self.headers,
                json={
                    "commit_title": f"🤖 Auto-merge: #{pr_number}",
                    "commit_message": commit_message,
                    "merge_method": "squash",
                }
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "sha": data.get("sha"),
                        "message": data.get("message"),
                    }
                else:
                    error_data = await response.json()
                    return {
                        "success": False,
                        "error": error_data.get("message", "Unknown error"),
                        "status": response.status,
                    }
    
    def _sign_provenance(self, provenance: Dict[str, Any]) -> str:
        """Generate cryptographic signature for provenance"""
        # Serialize provenance (excluding signature field if present)
        provenance_copy = {k: v for k, v in provenance.items() if k != "signature"}
        provenance_str = json.dumps(provenance_copy, sort_keys=True)
        
        # Use SHA-256 (BLAKE3 would require additional dependency)
        signature = hashlib.sha256(provenance_str.encode()).hexdigest()
        
        return signature
    
    def _generate_timestamp_proof(self, provenance: Dict[str, Any]) -> str:
        """Generate timestamp proof"""
        # Simplified timestamp proof (in production, use OpenTimestamps)
        timestamp_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "provenance_hash": provenance.get("signature", ""),
        }
        
        proof = hashlib.sha256(
            json.dumps(timestamp_data, sort_keys=True).encode()
        ).hexdigest()
        
        return proof
    
    async def _notify_discord(
        self,
        pr_number: int,
        decision: Dict[str, Any],
        merge_result: Dict[str, Any],
    ) -> None:
        """Send Discord notification about the merge"""
        
        webhook_url = self.settings.discord.webhook_url
        
        if not webhook_url:
            logger.debug("No Discord webhook configured, skipping notification")
            return
        
        confidence = decision.get("confidence", 0.0)
        action = decision.get("action", "unknown")
        
        embed = {
            "title": f"🤖 PR #{pr_number} - Auto-merged",
            "description": f"**Confidence:** {confidence:.2%}\n**Action:** {action}",
            "color": 0x00ff00 if merge_result.get("success") else 0xff0000,
            "fields": [
                {
                    "name": "SHA",
                    "value": merge_result.get("sha", "N/A")[:12],
                    "inline": True,
                },
                {
                    "name": "Merged By",
                    "value": "SovereignPRManager v1.0",
                    "inline": True,
                },
            ],
            "timestamp": datetime.utcnow().isoformat(),
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                await session.post(
                    webhook_url,
                    json={"embeds": [embed]},
                )
        except Exception as e:
            logger.warning(f"Failed to send Discord notification: {e}")
    
    async def add_review_comment(
        self,
        pr_number: int,
        decision: Dict[str, Any],
    ) -> bool:
        """Add a review comment to the PR"""
        
        repo = self.settings.github.repo
        
        confidence = decision.get("confidence", 0.0)
        action = decision.get("action", "unknown")
        reasoning = decision.get("reasoning", "")
        scores = decision.get("scores", {})
        
        body = f"""## 🤖 SovereignPRManager Review

**Decision:** {action.upper()}
**Confidence:** {confidence:.2%}

### Scores
| Domain | Score |
|--------|-------|
| Security | {scores.get('security', 0):.2%} |
| Architecture | {scores.get('architecture', 0):.2%} |
| Sovereignty | {scores.get('sovereignty', 0):.2%} |
| Performance | {scores.get('performance', 0):.2%} |
| **Overall** | **{scores.get('overall', 0):.2%}** |

### Reasoning
{reasoning}

---
*Automated review by SovereignPRManager v1.0*
"""
        
        async with aiohttp.ClientSession() as session:
            url = f"{self.base_url}/repos/{repo}/issues/{pr_number}/comments"
            
            async with session.post(
                url,
                headers=self.headers,
                json={"body": body},
            ) as response:
                if response.status == 201:
                    logger.info(f"Added review comment to PR #{pr_number}")
                    return True
                else:
                    error = await response.text()
                    logger.error(f"Failed to add comment: {response.status} - {error}")
                    return False
    
    async def close_pr(
        self,
        pr_number: int,
        reason: str,
    ) -> bool:
        """Close a PR without merging"""
        
        repo = self.settings.github.repo
        
        async with aiohttp.ClientSession() as session:
            # Add comment explaining closure
            comment_url = f"{self.base_url}/repos/{repo}/issues/{pr_number}/comments"
            await session.post(
                comment_url,
                headers=self.headers,
                json={"body": f"🤖 **SovereignPRManager**: PR closed automatically.\n\n**Reason:** {reason}"},
            )
            
            # Close the PR
            url = f"{self.base_url}/repos/{repo}/pulls/{pr_number}"
            
            async with session.patch(
                url,
                headers=self.headers,
                json={"state": "closed"},
            ) as response:
                if response.status == 200:
                    logger.info(f"Closed PR #{pr_number}")
                    return True
                else:
                    error = await response.text()
                    logger.error(f"Failed to close PR: {response.status} - {error}")
                    return False

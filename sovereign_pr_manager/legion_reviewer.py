"""
Legion Reviewer Module
Multi-AI code review system with specialized agents
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path

import aiohttp

from .config import Settings

logger = logging.getLogger(__name__)


class LegionReviewer:
    """Multi-AI code review system"""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self._declaration_content: Optional[str] = None
    
    def _load_declaration(self) -> str:
        """Load the Technical Declaration content"""
        if self._declaration_content:
            return self._declaration_content
        
        declaration_path = self.settings.declaration_path
        
        if not declaration_path:
            # Try common locations
            possible_paths = [
                "DECLARATION.md",
                "docs/DECLARATION.md",
                "README.md",
            ]
            for path in possible_paths:
                if Path(path).exists():
                    declaration_path = path
                    break
        
        if declaration_path and Path(declaration_path).exists():
            with open(declaration_path, 'r') as f:
                self._declaration_content = f.read()
        else:
            self._declaration_content = "No declaration found"
        
        return self._declaration_content
    
    async def review_pr(self, pr_data: Dict[str, Any]) -> Dict[str, Any]:
        """Parallel review by specialized AI agents"""
        
        diff = pr_data.get("diff", "")
        
        if not diff:
            logger.warning(f"No diff available for PR #{pr_data.get('number')}")
        
        # Parallel AI reviews
        tasks = [
            self._security_review(diff, pr_data),
            self._architecture_review(diff, pr_data),
            self._sovereignty_review(diff, pr_data),
            self._performance_review(diff, pr_data),
        ]
        
        try:
            reviews = await asyncio.gather(*tasks, return_exceptions=True)
        except Exception as e:
            logger.error(f"Review error: {e}")
            reviews = []
        
        # Process results, handling any exceptions
        processed_reviews = []
        for i, review in enumerate(reviews):
            if isinstance(review, Exception):
                logger.error(f"Review {i} failed: {review}")
                processed_reviews.append({
                    "type": ["security", "architecture", "sovereignty", "performance"][i],
                    "status": "error",
                    "error": str(review),
                    "approve": False,
                    "confidence": 0.0,
                })
            else:
                processed_reviews.append(review)
        
        return {
            "pr_number": pr_data.get("number"),
            "pr_title": pr_data.get("title"),
            "reviews": processed_reviews,
            "timestamp": datetime.utcnow().isoformat(),
            "overall_approve": all(r.get("approve", False) for r in processed_reviews if r.get("status") != "error"),
            "average_confidence": sum(r.get("confidence", 0) for r in processed_reviews) / max(len(processed_reviews), 1),
        }
    
    async def _security_review(self, diff: str, pr_data: Dict[str, Any]) -> Dict[str, Any]:
        """Security vulnerability review"""
        
        prompt = f"""Review this code diff for security vulnerabilities.

Consider:
1. Credential exposure (API keys, passwords, tokens)
2. Injection attacks (SQL, command, XSS)
3. Access control issues
4. Cryptographic weaknesses
5. Supply chain risks

PR: #{pr_data.get('number')} - {pr_data.get('title')}
Author: {pr_data.get('author')}

Diff (first 10000 chars):
{diff[:10000]}

Respond in valid JSON format only:
{{
    "type": "security",
    "severity": "critical|high|medium|low|none",
    "vulnerabilities": ["list of issues found"],
    "recommendations": ["list of fixes"],
    "confidence": 0.0-1.0,
    "approve": true|false,
    "reasoning": "explanation"
}}
"""
        
        return await self._call_ai(prompt, "security")
    
    async def _architecture_review(self, diff: str, pr_data: Dict[str, Any]) -> Dict[str, Any]:
        """Architecture and code quality review"""
        
        prompt = f"""Review this code diff for architecture and code quality.

Consider:
1. Design patterns and best practices
2. Code organization and modularity
3. Error handling and resilience
4. Documentation and readability
5. Test coverage implications

PR: #{pr_data.get('number')} - {pr_data.get('title')}
Author: {pr_data.get('author')}

Diff (first 10000 chars):
{diff[:10000]}

Respond in valid JSON format only:
{{
    "type": "architecture",
    "quality_score": 0.0-1.0,
    "issues": ["list of architecture issues"],
    "improvements": ["suggestions for improvement"],
    "confidence": 0.0-1.0,
    "approve": true|false,
    "reasoning": "explanation"
}}
"""
        
        return await self._call_ai(prompt, "architecture")
    
    async def _sovereignty_review(self, diff: str, pr_data: Dict[str, Any]) -> Dict[str, Any]:
        """Sovereignty Architecture alignment review"""
        
        declaration = self._load_declaration()
        
        prompt = f"""Review this code against our Sovereignty Architecture principles.

Our Declaration (first 5000 chars):
{declaration[:5000]}

PR: #{pr_data.get('number')} - {pr_data.get('title')}
Author: {pr_data.get('author')}

Code diff (first 10000 chars):
{diff[:10000]}

Check for:
1. Zero-trust compliance
2. Self-hosted infrastructure preference
3. Cryptographic verification
4. Audit trail requirements
5. Intellectual property protection

Respond in valid JSON format only:
{{
    "type": "sovereignty",
    "sovereignty_score": 0.0-1.0,
    "violations": ["list of principle violations"],
    "enhancements": ["suggestions to improve sovereignty"],
    "confidence": 0.0-1.0,
    "approve": true|false,
    "reasoning": "explanation"
}}
"""
        
        return await self._call_ai(prompt, "sovereignty")
    
    async def _performance_review(self, diff: str, pr_data: Dict[str, Any]) -> Dict[str, Any]:
        """Performance and optimization review"""
        
        prompt = f"""Review this code diff for performance implications.

Consider:
1. Algorithm complexity (time and space)
2. Database query efficiency
3. Memory management
4. Caching opportunities
5. Async/concurrent operations

PR: #{pr_data.get('number')} - {pr_data.get('title')}
Author: {pr_data.get('author')}

Diff (first 10000 chars):
{diff[:10000]}

Respond in valid JSON format only:
{{
    "type": "performance",
    "performance_score": 0.0-1.0,
    "bottlenecks": ["potential performance issues"],
    "optimizations": ["suggested optimizations"],
    "confidence": 0.0-1.0,
    "approve": true|false,
    "reasoning": "explanation"
}}
"""
        
        return await self._call_ai(prompt, "performance")
    
    async def _call_ai(self, prompt: str, review_type: str) -> Dict[str, Any]:
        """Call AI API for review"""
        
        # Try Anthropic first
        if self.settings.ai.anthropic_key:
            try:
                return await self._call_anthropic(prompt, review_type)
            except Exception as e:
                logger.warning(f"Anthropic API failed: {e}")
        
        # Fallback to OpenAI
        if self.settings.ai.openai_key:
            try:
                return await self._call_openai(prompt, review_type)
            except Exception as e:
                logger.warning(f"OpenAI API failed: {e}")
        
        # Return default response if no AI available
        logger.warning("No AI API available, returning default review")
        return self._default_review(review_type)
    
    async def _call_anthropic(self, prompt: str, review_type: str) -> Dict[str, Any]:
        """Call Anthropic Claude API"""
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": self.settings.ai.anthropic_key,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json",
                },
                json={
                    "model": "claude-sonnet-4-20250514",
                    "max_tokens": 2000,
                    "messages": [{"role": "user", "content": prompt}]
                }
            ) as response:
                if response.status != 200:
                    error = await response.text()
                    raise Exception(f"Anthropic API error: {response.status} - {error}")
                
                data = await response.json()
                content = data.get("content", [{}])[0].get("text", "{}")
                
                # Parse JSON response
                try:
                    return json.loads(content)
                except json.JSONDecodeError:
                    # Try to extract JSON from response
                    import re
                    json_match = re.search(r'\{[\s\S]*\}', content)
                    if json_match:
                        return json.loads(json_match.group())
                    raise
    
    async def _call_openai(self, prompt: str, review_type: str) -> Dict[str, Any]:
        """Call OpenAI API"""
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.settings.ai.openai_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "gpt-4o",
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 2000,
                    "response_format": {"type": "json_object"}
                }
            ) as response:
                if response.status != 200:
                    error = await response.text()
                    raise Exception(f"OpenAI API error: {response.status} - {error}")
                
                data = await response.json()
                content = data.get("choices", [{}])[0].get("message", {}).get("content", "{}")
                
                return json.loads(content)
    
    def _default_review(self, review_type: str) -> Dict[str, Any]:
        """Return default review when no AI is available"""
        return {
            "type": review_type,
            "status": "manual_required",
            "message": "No AI API available - manual review required",
            "confidence": 0.0,
            "approve": False,
            "reasoning": "Automated review unavailable",
        }

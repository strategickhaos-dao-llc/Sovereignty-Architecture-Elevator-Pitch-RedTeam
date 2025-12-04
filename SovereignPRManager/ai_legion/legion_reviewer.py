"""
Legion Reviewer - Coordinates multiple AI agents for PR review.

This module orchestrates parallel reviews from multiple AI systems
and synthesizes their feedback into a unified recommendation.

Note: This component is designed to be called by a NATS consumer
that subscribes to 'pr.detected' events. The NATS subscription
logic is implemented in a separate event handler module.

Author: SovereignPRManager Legion
"""

import asyncio
import json
import os
from datetime import datetime, timezone
from typing import Any, Optional

import anthropic
import httpx
import openai


class LegionReviewer:
    """Coordinates multiple AI agents for comprehensive PR review."""

    def __init__(
        self,
        anthropic_key: str,
        openai_key: str,
        confidence_threshold: float = 0.9,
    ):
        """Initialize Legion Reviewer.

        Args:
            anthropic_key: Anthropic API key for Claude
            openai_key: OpenAI API key for GPT-4
            confidence_threshold: Threshold for auto-approval
        """
        self.claude = anthropic.Anthropic(api_key=anthropic_key)
        self.openai_client = openai.OpenAI(api_key=openai_key)
        self.confidence_threshold = confidence_threshold

    async def review_pr(self, pr_event: dict[str, Any]) -> dict[str, Any]:
        """Coordinate Legion review of PR.

        Args:
            pr_event: PR event data from monitor

        Returns:
            Synthesized review results
        """
        print(f"🤖 Legion reviewing PR #{pr_event['pr_number']}")

        # Fetch diff
        diff = await self._fetch_diff(pr_event["diff_url"])

        # Parallel AI reviews
        reviews = await asyncio.gather(
            self._claude_security_review(diff, pr_event),
            self._claude_sovereignty_review(diff, pr_event),
            self._gpt_architecture_review(diff, pr_event),
            self._gpt_performance_review(diff, pr_event),
            return_exceptions=True,
        )

        # Filter out any exceptions
        valid_reviews = [r for r in reviews if isinstance(r, dict)]

        # Synthesize reviews
        synthesis = self._synthesize_reviews(valid_reviews, pr_event)

        return synthesis

    async def _fetch_diff(self, diff_url: str) -> str:
        """Fetch PR diff content."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                diff_url, headers={"Accept": "application/vnd.github.v3.diff"}
            )
            return response.text

    async def _claude_security_review(
        self, diff: str, pr_event: dict[str, Any]
    ) -> dict[str, Any]:
        """Claude analyzes security implications.

        Args:
            diff: PR diff content
            pr_event: PR event data

        Returns:
            Security review results
        """
        prompt = f"""Review this PR for security vulnerabilities.

PR: #{pr_event['pr_number']} - {pr_event['title']}
Files changed: {pr_event['files_changed']}

Focus on:
1. Credential exposure (API keys, tokens, passwords)
2. Injection vulnerabilities (SQL, command, XSS)
3. Authentication/authorization issues
4. Cryptographic weaknesses
5. Supply chain risks (dependencies)

Diff (first 10K chars):
```
{diff[:10000]}
```

Respond in JSON format only:
{{
    "severity": "critical|high|medium|low|none",
    "vulnerabilities": ["list of found issues"],
    "recommendations": ["list of fixes"],
    "confidence": 0.0-1.0,
    "approve": true|false,
    "reasoning": "explanation"
}}
"""

        response = self.claude.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}],
        )

        try:
            review = json.loads(response.content[0].text)
        except json.JSONDecodeError:
            review = {
                "severity": "unknown",
                "vulnerabilities": [],
                "recommendations": [],
                "confidence": 0.5,
                "approve": False,
                "reasoning": "Failed to parse response",
            }

        review["reviewer"] = "Claude (Security)"
        return review

    async def _claude_sovereignty_review(
        self, diff: str, pr_event: dict[str, Any]
    ) -> dict[str, Any]:
        """Claude checks Sovereignty Architecture alignment.

        Args:
            diff: PR diff content
            pr_event: PR event data

        Returns:
            Sovereignty review results
        """
        prompt = f"""Review this PR against Sovereignty Architecture principles.

PR: #{pr_event['pr_number']} - {pr_event['title']}

Check alignment with:
1. Zero-trust architecture
2. Self-hosted infrastructure preference
3. Cryptographic verification
4. Audit trail requirements
5. Intellectual property protection
6. "880x cost reduction model" philosophy

Diff (first 10K chars):
```
{diff[:10000]}
```

Respond in JSON format only:
{{
    "sovereignty_score": 0.0-1.0,
    "violations": ["list of violations"],
    "enhancements": ["list of suggestions"],
    "confidence": 0.0-1.0,
    "approve": true|false,
    "reasoning": "explanation"
}}
"""

        response = self.claude.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}],
        )

        try:
            review = json.loads(response.content[0].text)
        except json.JSONDecodeError:
            review = {
                "sovereignty_score": 0.5,
                "violations": [],
                "enhancements": [],
                "confidence": 0.5,
                "approve": False,
                "reasoning": "Failed to parse response",
            }

        review["reviewer"] = "Claude (Sovereignty)"
        return review

    async def _gpt_architecture_review(
        self, diff: str, pr_event: dict[str, Any]
    ) -> dict[str, Any]:
        """GPT-4 reviews architecture and design.

        Args:
            diff: PR diff content
            pr_event: PR event data

        Returns:
            Architecture review results
        """
        prompt = f"""Review this PR for architecture and design quality.

PR: #{pr_event['pr_number']} - {pr_event['title']}
Files changed: {pr_event['files_changed']}

Evaluate:
1. Code organization and structure
2. Design patterns usage
3. Modularity and separation of concerns
4. API design and interfaces
5. Error handling and resilience

Diff (first 10K chars):
```
{diff[:10000]}
```

Respond in JSON format only:
{{
    "architecture_score": 0.0-1.0,
    "issues": ["list of issues"],
    "improvements": ["list of suggestions"],
    "confidence": 0.0-1.0,
    "approve": true|false,
    "reasoning": "explanation"
}}
"""

        response = self.openai_client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000,
        )

        try:
            review = json.loads(response.choices[0].message.content or "{}")
        except json.JSONDecodeError:
            review = {
                "architecture_score": 0.5,
                "issues": [],
                "improvements": [],
                "confidence": 0.5,
                "approve": False,
                "reasoning": "Failed to parse response",
            }

        review["reviewer"] = "GPT-4 (Architecture)"
        return review

    async def _gpt_performance_review(
        self, diff: str, pr_event: dict[str, Any]
    ) -> dict[str, Any]:
        """GPT-4 reviews performance implications.

        Args:
            diff: PR diff content
            pr_event: PR event data

        Returns:
            Performance review results
        """
        prompt = f"""Review this PR for performance implications.

PR: #{pr_event['pr_number']} - {pr_event['title']}
Additions: {pr_event['additions']}, Deletions: {pr_event['deletions']}

Evaluate:
1. Algorithm efficiency (time complexity)
2. Memory usage patterns
3. I/O operations and network calls
4. Caching opportunities
5. Concurrency and parallelism

Diff (first 10K chars):
```
{diff[:10000]}
```

Respond in JSON format only:
{{
    "performance_score": 0.0-1.0,
    "concerns": ["list of concerns"],
    "optimizations": ["list of suggestions"],
    "confidence": 0.0-1.0,
    "approve": true|false,
    "reasoning": "explanation"
}}
"""

        response = self.openai_client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000,
        )

        try:
            review = json.loads(response.choices[0].message.content or "{}")
        except json.JSONDecodeError:
            review = {
                "performance_score": 0.5,
                "concerns": [],
                "optimizations": [],
                "confidence": 0.5,
                "approve": False,
                "reasoning": "Failed to parse response",
            }

        review["reviewer"] = "GPT-4 (Performance)"
        return review

    def _synthesize_reviews(
        self, reviews: list[dict[str, Any]], pr_event: dict[str, Any]
    ) -> dict[str, Any]:
        """Synthesize multiple reviews into unified recommendation.

        Args:
            reviews: List of individual reviews
            pr_event: PR event data

        Returns:
            Synthesized review with recommendation
        """
        if not reviews:
            return {
                "pr_number": pr_event["pr_number"],
                "status": "error",
                "message": "No reviews completed",
                "approve": False,
                "confidence": 0.0,
            }

        # Calculate aggregate confidence
        confidences = [r.get("confidence", 0.5) for r in reviews]
        avg_confidence = sum(confidences) / len(confidences)

        # Check for blocking issues
        approvals = [r.get("approve", False) for r in reviews]
        all_approve = all(approvals)

        # Determine overall recommendation
        should_approve = all_approve and avg_confidence >= self.confidence_threshold

        return {
            "pr_number": pr_event["pr_number"],
            "title": pr_event["title"],
            "reviews": reviews,
            "synthesis": {
                "total_reviewers": len(reviews),
                "approvals": sum(1 for a in approvals if a),
                "rejections": sum(1 for a in approvals if not a),
                "average_confidence": round(avg_confidence, 3),
                "recommendation": "approve" if should_approve else "request_changes",
                "auto_merge_eligible": should_approve,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


async def main() -> None:
    """Main entry point for testing."""
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")

    if not anthropic_key or not openai_key:
        raise ValueError("ANTHROPIC_API_KEY and OPENAI_API_KEY required")

    reviewer = LegionReviewer(
        anthropic_key=anthropic_key,
        openai_key=openai_key,
    )

    # Example PR event for testing
    test_event = {
        "pr_number": 1,
        "title": "Test PR",
        "diff_url": "https://example.com/diff",
        "files_changed": 5,
        "additions": 100,
        "deletions": 50,
    }

    result = await reviewer.review_pr(test_event)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    asyncio.run(main())

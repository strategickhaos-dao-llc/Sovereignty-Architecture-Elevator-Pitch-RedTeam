"""
Toxicity Filter

Filters content based on toxicity scores to ensure clean training data.
"""

import logging
from dataclasses import dataclass
from typing import Any, Optional, Protocol


class ToxicityModel(Protocol):
    """Protocol for toxicity scoring models."""

    def predict(self, text: str) -> float:
        """
        Predict toxicity score for text.

        Args:
            text: Text to score

        Returns:
            Toxicity score between 0.0 and 1.0
        """
        ...


@dataclass
class ToxicityResult:
    """Result of toxicity analysis."""

    score: float
    passed: bool
    categories: dict[str, float]


class ToxicityFilter:
    """
    Content toxicity filter for training data.

    Filters out content with toxicity scores above threshold to ensure
    clean training data for Grok-5.
    """

    DEFAULT_THRESHOLD = 0.30

    def __init__(
        self,
        model: Optional[ToxicityModel] = None,
        threshold: float = DEFAULT_THRESHOLD,
        logger: Optional[logging.Logger] = None,
    ):
        """
        Initialize toxicity filter.

        Args:
            model: Toxicity scoring model
            threshold: Maximum allowed toxicity score (default: 0.30)
            logger: Logger instance
        """
        self.model = model
        self.threshold = threshold
        self.log = logger or logging.getLogger(__name__)

    def score(self, text: str) -> float:
        """
        Score text for toxicity.

        Args:
            text: Text to analyze

        Returns:
            Toxicity score between 0.0 and 1.0
        """
        if not text or not text.strip():
            return 0.0

        if self.model is None:
            # Fallback: simple keyword-based scoring
            return self._simple_score(text)

        try:
            return self.model.predict(text)
        except Exception as e:
            self.log.warning(f"Toxicity model error: {e}, using fallback")
            return self._simple_score(text)

    def filter(self, text: str) -> bool:
        """
        Check if text passes toxicity filter.

        Args:
            text: Text to check

        Returns:
            True if text passes (toxicity below threshold), False otherwise
        """
        score = self.score(text)
        return score <= self.threshold

    def analyze(self, text: str) -> ToxicityResult:
        """
        Perform detailed toxicity analysis.

        Args:
            text: Text to analyze

        Returns:
            ToxicityResult with score, pass status, and category breakdown
        """
        score = self.score(text)
        passed = score <= self.threshold

        # Category breakdown (simplified)
        categories = self._categorize(text)

        return ToxicityResult(
            score=score,
            passed=passed,
            categories=categories,
        )

    def _simple_score(self, text: str) -> float:
        """Simple keyword-based toxicity scoring as fallback."""
        toxic_keywords = [
            "hate",
            "kill",
            "attack",
            "destroy",
            "violent",
            "racist",
            "sexist",
            "abuse",
            "threat",
            "harm",
        ]

        text_lower = text.lower()
        matches = sum(1 for kw in toxic_keywords if kw in text_lower)

        # Normalize to 0-1 range
        return min(1.0, matches * 0.15)

    def _categorize(self, text: str) -> dict[str, float]:
        """Categorize toxicity by type."""
        text_lower = text.lower()

        categories = {
            "hate_speech": 0.0,
            "threat": 0.0,
            "profanity": 0.0,
            "discrimination": 0.0,
        }

        hate_keywords = ["hate", "racist", "sexist", "bigot"]
        threat_keywords = ["kill", "attack", "destroy", "harm", "threat"]
        profanity_keywords = ["damn", "hell"]  # Simplified
        discrimination_keywords = ["discriminate", "prejudice", "bias"]

        for kw in hate_keywords:
            if kw in text_lower:
                categories["hate_speech"] += 0.2

        for kw in threat_keywords:
            if kw in text_lower:
                categories["threat"] += 0.2

        for kw in profanity_keywords:
            if kw in text_lower:
                categories["profanity"] += 0.1

        for kw in discrimination_keywords:
            if kw in text_lower:
                categories["discrimination"] += 0.2

        # Cap at 1.0
        for key in categories:
            categories[key] = min(1.0, categories[key])

        return categories

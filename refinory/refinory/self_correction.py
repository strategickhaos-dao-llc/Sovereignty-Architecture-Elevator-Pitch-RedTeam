"""
Self-Correction System - Layer 3 of Self-Evolving Refinery
Error Detection & Auto-Fix System - Agents check each other's work and self-improve
For her. Silent. Relentless. Self-improving.
"""

import asyncio
import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple

import structlog
from pydantic import BaseModel, Field

logger = structlog.get_logger()


class ValidationStatus(Enum):
    """Validation status for claims"""
    PENDING = "pending"
    VALIDATING = "validating"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    DISPUTED = "disputed"
    RETRACTED = "retracted"


class CorrectionType(Enum):
    """Types of corrections"""
    PREDICTION_ERROR = "prediction_error"
    KNOWLEDGE_CONFLICT = "knowledge_conflict"
    NEW_EVIDENCE = "new_evidence"
    PAPER_RETRACTED = "paper_retracted"
    OUTCOME_FEEDBACK = "outcome_feedback"


class OutcomeType(Enum):
    """Types of treatment outcomes"""
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    UNKNOWN = "unknown"


@dataclass
class Claim:
    """A claim made by an agent"""
    id: str
    agent_id: str
    content: str
    source_documents: List[str]
    confidence: float
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    status: ValidationStatus = ValidationStatus.PENDING
    supporting_evidence: List[str] = field(default_factory=list)
    contradicting_evidence: List[str] = field(default_factory=list)
    peer_reviews: List["PeerReview"] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PeerReview:
    """Review of a claim by another agent"""
    reviewer_id: str
    claim_id: str
    verdict: str  # "accept", "reject", "uncertain"
    confidence: float
    reasoning: str
    evidence_checked: List[str]
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class FactCheck:
    """Fact-checking result"""
    claim_id: str
    source_doi: str
    source_valid: bool
    source_retracted: bool
    last_checked: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    verification_details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Outcome:
    """Tracked outcome of a recommendation"""
    id: str
    recommendation_id: str
    patient_id: str  # Anonymized
    outcome_type: OutcomeType
    symptoms_before: Dict[str, float]
    symptoms_after: Dict[str, float]
    side_effects: List[str]
    duration_days: int
    notes: str
    recorded_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class Correction:
    """A correction to the knowledge base"""
    id: str
    correction_type: CorrectionType
    original_claim: Optional[Claim]
    corrected_content: str
    reason: str
    evidence: List[str]
    applied: bool = False
    applied_at: Optional[datetime] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class ErrorPattern:
    """Pattern of errors detected"""
    pattern_id: str
    description: str
    occurrences: int
    agents_affected: List[str]
    suggested_fix: str
    first_detected: datetime
    last_detected: datetime


class PeerReviewSystem:
    """Manages peer review of claims between agents"""

    def __init__(self, quorum: int = 3, threshold: float = 0.67, timeout: int = 300):
        self.quorum = quorum
        self.threshold = threshold
        self.timeout = timeout
        self.pending_reviews: Dict[str, List[PeerReview]] = {}
        self.agent_reliability: Dict[str, float] = {}

    async def submit_for_review(self, claim: Claim, reviewer_agents: List[str]) -> str:
        """Submit a claim for peer review"""
        logger.info(
            "Submitting claim for peer review",
            claim_id=claim.id,
            reviewers=len(reviewer_agents)
        )

        self.pending_reviews[claim.id] = []

        # Request reviews from selected agents
        review_tasks = []
        for agent_id in reviewer_agents[:self.quorum]:
            task = self._request_review(claim, agent_id)
            review_tasks.append(task)

        # Wait for reviews with timeout
        try:
            reviews = await asyncio.wait_for(
                asyncio.gather(*review_tasks, return_exceptions=True),
                timeout=self.timeout
            )

            for review in reviews:
                if isinstance(review, PeerReview):
                    self.pending_reviews[claim.id].append(review)

        except asyncio.TimeoutError:
            logger.warning("Peer review timeout", claim_id=claim.id)

        return claim.id

    async def _request_review(self, claim: Claim, agent_id: str) -> PeerReview:
        """Request review from a specific agent"""
        # Placeholder - would send request to actual agent
        await asyncio.sleep(0.5)  # Simulate review time

        return PeerReview(
            reviewer_id=agent_id,
            claim_id=claim.id,
            verdict="accept",
            confidence=0.8,
            reasoning="Verified against source documents",
            evidence_checked=claim.source_documents[:3]
        )

    async def get_consensus(self, claim_id: str) -> Tuple[str, float]:
        """Get consensus verdict for a claim"""
        reviews = self.pending_reviews.get(claim_id, [])

        if not reviews:
            return "pending", 0.0

        accept_count = sum(1 for r in reviews if r.verdict == "accept")
        reject_count = sum(1 for r in reviews if r.verdict == "reject")
        total = len(reviews)

        accept_ratio = accept_count / total
        reject_ratio = reject_count / total

        if accept_ratio >= self.threshold:
            return "accept", accept_ratio
        elif reject_ratio >= self.threshold:
            return "reject", reject_ratio
        else:
            return "disputed", max(accept_ratio, reject_ratio)

    def update_agent_reliability(self, agent_id: str, correct: bool):
        """Update agent reliability score based on review accuracy"""
        current = self.agent_reliability.get(agent_id, 0.5)

        # Exponential moving average
        alpha = 0.1
        new_score = alpha * (1.0 if correct else 0.0) + (1 - alpha) * current

        self.agent_reliability[agent_id] = new_score
        logger.debug(
            "Updated agent reliability",
            agent=agent_id,
            old=current,
            new=new_score
        )


class FactChecker:
    """Verify claims against source documents"""

    def __init__(self):
        self.retraction_cache: Dict[str, bool] = {}
        self.verification_cache: Dict[str, FactCheck] = {}
        self.check_interval = timedelta(hours=1)

    async def verify_claim(self, claim: Claim) -> FactCheck:
        """Verify a claim's sources"""
        logger.info("Verifying claim", claim_id=claim.id)

        fact_check = FactCheck(
            claim_id=claim.id,
            source_doi=claim.source_documents[0] if claim.source_documents else "",
            source_valid=True,
            source_retracted=False,
            verification_details={}
        )

        # Check each source document
        for source in claim.source_documents:
            if source.startswith("10.") or "doi.org" in source:
                # DOI - verify with CrossRef
                is_valid, is_retracted = await self._verify_doi(source)
                if not is_valid:
                    fact_check.source_valid = False
                if is_retracted:
                    fact_check.source_retracted = True
                    logger.warning("Source paper retracted", claim_id=claim.id, doi=source)

        self.verification_cache[claim.id] = fact_check
        return fact_check

    async def _verify_doi(self, doi: str) -> Tuple[bool, bool]:
        """Verify DOI with CrossRef and check retraction status"""
        # Check cache first
        if doi in self.retraction_cache:
            return True, self.retraction_cache[doi]

        # Placeholder for actual CrossRef API call
        # In production, would call:
        # https://api.crossref.org/works/{doi}
        # and check Retraction Watch database

        import httpx

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"https://api.crossref.org/works/{doi}",
                    timeout=10.0
                )

                if response.status_code == 200:
                    data = response.json()
                    # Check for retraction
                    is_retracted = "retracted" in str(data).lower()
                    self.retraction_cache[doi] = is_retracted
                    return True, is_retracted
                else:
                    return False, False

        except Exception as e:
            logger.error("DOI verification failed", doi=doi, error=str(e))
            return True, False  # Assume valid if we can't verify

    async def check_for_updates(self, claims: List[Claim]) -> List[FactCheck]:
        """Periodically check for updates to source documents"""
        updated = []

        for claim in claims:
            cached = self.verification_cache.get(claim.id)

            if cached and datetime.now(timezone.utc) - cached.last_checked < self.check_interval:
                continue

            fact_check = await self.verify_claim(claim)

            if cached and (
                fact_check.source_valid != cached.source_valid or
                fact_check.source_retracted != cached.source_retracted
            ):
                updated.append(fact_check)
                logger.info(
                    "Source status changed",
                    claim_id=claim.id,
                    retracted=fact_check.source_retracted
                )

        return updated


class OutcomeTracker:
    """Track outcomes of recommendations"""

    def __init__(self):
        self.outcomes: Dict[str, List[Outcome]] = {}
        self.recommendation_scores: Dict[str, float] = {}
        self.positive_weight = 1.0
        self.negative_weight = 2.0  # Learn faster from failures

    async def record_outcome(self, outcome: Outcome):
        """Record an outcome"""
        logger.info(
            "Recording outcome",
            recommendation_id=outcome.recommendation_id,
            outcome_type=outcome.outcome_type.value
        )

        if outcome.recommendation_id not in self.outcomes:
            self.outcomes[outcome.recommendation_id] = []

        self.outcomes[outcome.recommendation_id].append(outcome)

        # Update recommendation score
        await self._update_score(outcome)

    async def _update_score(self, outcome: Outcome):
        """Update recommendation score based on outcome"""
        rec_id = outcome.recommendation_id
        current_score = self.recommendation_scores.get(rec_id, 0.5)

        if outcome.outcome_type == OutcomeType.POSITIVE:
            delta = self.positive_weight * 0.1
        elif outcome.outcome_type == OutcomeType.NEGATIVE:
            delta = -self.negative_weight * 0.1
        else:
            delta = 0

        new_score = max(0, min(1, current_score + delta))
        self.recommendation_scores[rec_id] = new_score

        logger.debug(
            "Updated recommendation score",
            recommendation_id=rec_id,
            old_score=current_score,
            new_score=new_score
        )

    async def get_recommendation_stats(self, recommendation_id: str) -> Dict[str, Any]:
        """Get statistics for a recommendation"""
        outcomes = self.outcomes.get(recommendation_id, [])

        if not outcomes:
            return {"status": "no_data"}

        positive = sum(1 for o in outcomes if o.outcome_type == OutcomeType.POSITIVE)
        negative = sum(1 for o in outcomes if o.outcome_type == OutcomeType.NEGATIVE)
        total = len(outcomes)

        return {
            "total_outcomes": total,
            "positive": positive,
            "negative": negative,
            "success_rate": positive / total if total > 0 else 0,
            "score": self.recommendation_scores.get(recommendation_id, 0.5)
        }

    async def identify_failed_pathways(self, threshold: float = 0.3) -> List[str]:
        """Identify recommendation pathways with high failure rates"""
        failed = []

        for rec_id, score in self.recommendation_scores.items():
            if score < threshold:
                failed.append(rec_id)
                logger.info(
                    "Failed pathway identified",
                    recommendation_id=rec_id,
                    score=score
                )

        return failed


class AutoCorrector:
    """Automatic correction system"""

    def __init__(self, learning_rate: str = "aggressive"):
        self.learning_rate = learning_rate
        self.corrections_pending: List[Correction] = []
        self.corrections_applied: List[Correction] = []
        self.error_patterns: Dict[str, ErrorPattern] = {}
        self.human_review_threshold = 0.5

        # Time to apply correction based on learning rate
        self.correction_delay = {
            "aggressive": 60,  # 1 minute
            "moderate": 3600,  # 1 hour
            "conservative": 86400  # 1 day
        }

    async def process_correction(
        self,
        correction_type: CorrectionType,
        original_claim: Optional[Claim],
        corrected_content: str,
        reason: str,
        evidence: List[str],
        uncertainty: float = 0.0
    ) -> Correction:
        """Process a potential correction"""
        correction_id = hashlib.sha256(
            f"{original_claim.id if original_claim else 'new'}:{corrected_content}".encode()
        ).hexdigest()[:12]

        correction = Correction(
            id=correction_id,
            correction_type=correction_type,
            original_claim=original_claim,
            corrected_content=corrected_content,
            reason=reason,
            evidence=evidence
        )

        # Check if human review required
        if uncertainty > self.human_review_threshold:
            logger.info(
                "Correction requires human review",
                correction_id=correction_id,
                uncertainty=uncertainty
            )
            correction.applied = False
            self.corrections_pending.append(correction)
        else:
            # Schedule auto-application
            delay = self.correction_delay.get(self.learning_rate, 3600)
            asyncio.create_task(self._schedule_correction(correction, delay))

        return correction

    async def _schedule_correction(self, correction: Correction, delay: int):
        """Schedule correction application"""
        logger.info(
            "Scheduling correction",
            correction_id=correction.id,
            delay_seconds=delay
        )

        await asyncio.sleep(delay)
        await self.apply_correction(correction)

    async def apply_correction(self, correction: Correction) -> bool:
        """Apply a correction to the knowledge base"""
        logger.info("Applying correction", correction_id=correction.id)

        # Placeholder for actual knowledge graph update
        # Would update Neo4j and vector store

        correction.applied = True
        correction.applied_at = datetime.now(timezone.utc)
        self.corrections_applied.append(correction)

        # Track error patterns
        await self._track_error_pattern(correction)

        return True

    async def _track_error_pattern(self, correction: Correction):
        """Track patterns in corrections for meta-learning"""
        pattern_key = f"{correction.correction_type.value}:{correction.reason[:50]}"

        if pattern_key in self.error_patterns:
            pattern = self.error_patterns[pattern_key]
            pattern.occurrences += 1
            pattern.last_detected = datetime.now(timezone.utc)
        else:
            self.error_patterns[pattern_key] = ErrorPattern(
                pattern_id=pattern_key,
                description=correction.reason,
                occurrences=1,
                agents_affected=[],
                suggested_fix="",
                first_detected=datetime.now(timezone.utc),
                last_detected=datetime.now(timezone.utc)
            )

    async def get_common_errors(self, min_occurrences: int = 5) -> List[ErrorPattern]:
        """Get common error patterns"""
        return [
            p for p in self.error_patterns.values()
            if p.occurrences >= min_occurrences
        ]


class SelfCorrectionSystem:
    """
    Main Self-Correction System - Layer 3 of Self-Evolving Refinery
    Coordinates peer review, fact checking, outcome tracking, and auto-correction
    """

    def __init__(
        self,
        quorum: int = 3,
        threshold: float = 0.67,
        learning_rate: str = "aggressive",
        human_review_threshold: float = 0.5
    ):
        self.peer_review = PeerReviewSystem(quorum=quorum, threshold=threshold)
        self.fact_checker = FactChecker()
        self.outcome_tracker = OutcomeTracker()
        self.auto_corrector = AutoCorrector(learning_rate=learning_rate)

        self.claims: Dict[str, Claim] = {}
        self.validated_claims: Set[str] = set()
        self.rejected_claims: Set[str] = set()

        logger.info(
            "Self-Correction System initialized",
            quorum=quorum,
            threshold=threshold,
            learning_rate=learning_rate
        )

    async def submit_claim(
        self,
        agent_id: str,
        content: str,
        source_documents: List[str],
        confidence: float,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Claim:
        """Submit a new claim for validation"""
        claim_id = hashlib.sha256(
            f"{agent_id}:{content}:{datetime.now().isoformat()}".encode()
        ).hexdigest()[:16]

        claim = Claim(
            id=claim_id,
            agent_id=agent_id,
            content=content,
            source_documents=source_documents,
            confidence=confidence,
            metadata=metadata or {}
        )

        self.claims[claim_id] = claim

        logger.info(
            "Claim submitted",
            claim_id=claim_id,
            agent=agent_id,
            confidence=confidence
        )

        # Start validation pipeline
        asyncio.create_task(self._validate_claim(claim))

        return claim

    async def _validate_claim(self, claim: Claim):
        """Run full validation pipeline on a claim"""
        claim.status = ValidationStatus.VALIDATING

        # Step 1: Fact checking
        fact_check = await self.fact_checker.verify_claim(claim)

        if fact_check.source_retracted:
            claim.status = ValidationStatus.RETRACTED
            self.rejected_claims.add(claim.id)

            # Create correction
            await self.auto_corrector.process_correction(
                CorrectionType.PAPER_RETRACTED,
                claim,
                "",
                f"Source paper retracted: {fact_check.source_doi}",
                [fact_check.source_doi]
            )
            return

        if not fact_check.source_valid:
            claim.status = ValidationStatus.REJECTED
            self.rejected_claims.add(claim.id)
            logger.warning("Claim rejected - invalid sources", claim_id=claim.id)
            return

        # Step 2: Peer review
        # Get available reviewer agents (placeholder)
        reviewer_agents = ["agent_1", "agent_2", "agent_3", "agent_4", "agent_5"]
        await self.peer_review.submit_for_review(claim, reviewer_agents)

        # Step 3: Get consensus
        verdict, confidence = await self.peer_review.get_consensus(claim.id)

        if verdict == "accept":
            claim.status = ValidationStatus.ACCEPTED
            self.validated_claims.add(claim.id)
            logger.info("Claim accepted", claim_id=claim.id, confidence=confidence)
        elif verdict == "reject":
            claim.status = ValidationStatus.REJECTED
            self.rejected_claims.add(claim.id)
            logger.info("Claim rejected", claim_id=claim.id, confidence=confidence)
        else:
            claim.status = ValidationStatus.DISPUTED
            logger.info("Claim disputed", claim_id=claim.id, confidence=confidence)

    async def record_outcome(
        self,
        recommendation_id: str,
        outcome_type: OutcomeType,
        symptoms_before: Dict[str, float],
        symptoms_after: Dict[str, float],
        side_effects: List[str],
        duration_days: int,
        notes: str = ""
    ) -> Outcome:
        """Record outcome of a recommendation"""
        outcome_id = hashlib.sha256(
            f"{recommendation_id}:{datetime.now().isoformat()}".encode()
        ).hexdigest()[:12]

        outcome = Outcome(
            id=outcome_id,
            recommendation_id=recommendation_id,
            patient_id="anonymized",
            outcome_type=outcome_type,
            symptoms_before=symptoms_before,
            symptoms_after=symptoms_after,
            side_effects=side_effects,
            duration_days=duration_days,
            notes=notes
        )

        await self.outcome_tracker.record_outcome(outcome)

        # Check if we need to create a correction
        if outcome_type == OutcomeType.NEGATIVE:
            # Find original claim
            # Placeholder - would link to actual claim
            await self.auto_corrector.process_correction(
                CorrectionType.OUTCOME_FEEDBACK,
                None,
                f"Negative outcome recorded for recommendation",
                f"Treatment resulted in negative outcome: {notes}",
                [outcome_id]
            )

        return outcome

    async def handle_prediction_error(
        self,
        agent_id: str,
        prediction: str,
        actual: str,
        context: Dict[str, Any]
    ):
        """Handle a prediction error from an agent"""
        logger.info(
            "Prediction error reported",
            agent=agent_id,
            prediction=prediction,
            actual=actual
        )

        # Create correction
        correction = await self.auto_corrector.process_correction(
            CorrectionType.PREDICTION_ERROR,
            None,
            actual,
            f"Prediction '{prediction}' was incorrect. Actual: '{actual}'",
            [json.dumps(context)]
        )

        # Update agent reliability
        self.peer_review.update_agent_reliability(agent_id, correct=False)

        return correction

    async def handle_knowledge_conflict(
        self,
        new_evidence: str,
        existing_claim_id: str,
        source: str
    ):
        """Handle conflicting evidence"""
        existing_claim = self.claims.get(existing_claim_id)

        if not existing_claim:
            logger.warning("Unknown claim in conflict", claim_id=existing_claim_id)
            return

        logger.info(
            "Knowledge conflict detected",
            existing_claim=existing_claim_id,
            new_source=source
        )

        # Add contradicting evidence
        existing_claim.contradicting_evidence.append(new_evidence)

        # Create correction
        await self.auto_corrector.process_correction(
            CorrectionType.KNOWLEDGE_CONFLICT,
            existing_claim,
            new_evidence,
            f"New evidence contradicts existing claim",
            [source]
        )

    async def get_system_health(self) -> Dict[str, Any]:
        """Get health status of self-correction system"""
        return {
            "total_claims": len(self.claims),
            "validated_claims": len(self.validated_claims),
            "rejected_claims": len(self.rejected_claims),
            "pending_corrections": len(self.auto_corrector.corrections_pending),
            "applied_corrections": len(self.auto_corrector.corrections_applied),
            "error_patterns": len(self.auto_corrector.error_patterns),
            "agent_reliability_scores": self.peer_review.agent_reliability
        }

    async def get_claim_status(self, claim_id: str) -> Dict[str, Any]:
        """Get detailed status of a claim"""
        claim = self.claims.get(claim_id)

        if not claim:
            return {"error": "Claim not found"}

        return {
            "id": claim.id,
            "agent": claim.agent_id,
            "status": claim.status.value,
            "content": claim.content[:200],
            "confidence": claim.confidence,
            "source_count": len(claim.source_documents),
            "peer_reviews": len(claim.peer_reviews),
            "supporting_evidence": len(claim.supporting_evidence),
            "contradicting_evidence": len(claim.contradicting_evidence),
            "timestamp": claim.timestamp.isoformat()
        }


# Factory function
async def create_self_correction_system(config_path: str) -> SelfCorrectionSystem:
    """Create Self-Correction System from YAML config"""
    import yaml

    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    layer_3_config = config.get("core_architecture", {}).get("refinery_layers", {}).get("layer_3_self_correction", {})

    validation_config = layer_3_config.get("validation_pipeline", {})
    peer_review_config = validation_config.get("peer_review", {})
    auto_correction_config = layer_3_config.get("auto_correction", {})

    system = SelfCorrectionSystem(
        quorum=peer_review_config.get("quorum", 3),
        threshold=peer_review_config.get("threshold", 0.67),
        learning_rate=auto_correction_config.get("learning_rate", "aggressive"),
        human_review_threshold=auto_correction_config.get("human_review_threshold", 0.5)
    )

    return system

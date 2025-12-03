"""
Synthesis Engine Module
Dialectical synthesis of reviews into merge decision
"""

import logging
from datetime import datetime
from typing import Dict, List, Any, Optional

from .config import Settings

logger = logging.getLogger(__name__)


class MergeDecisionEngine:
    """Synthesize Legion reviews into final merge decision"""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.thresholds = settings.merge_thresholds
    
    def synthesize(
        self,
        reviews: Dict[str, Any],
        conflicts: Dict[str, Any],
        pr_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Apply dialectical synthesis to reach merge decision"""
        
        review_list = reviews.get("reviews", [])
        
        # Extract contradictions from reviews
        contradictions = self._extract_contradictions(review_list)
        
        # Calculate composite scores
        scores = self._calculate_scores(review_list)
        
        # Apply dialectical synthesis
        synthesis = self._dialectical_synthesis(review_list, contradictions, scores)
        
        # Calculate final confidence
        confidence = self._calculate_confidence(review_list, synthesis, conflicts)
        
        # Make decision
        action = self._make_decision(confidence, review_list, conflicts)
        
        decision = {
            "action": action,
            "confidence": confidence,
            "scores": scores,
            "synthesis": synthesis,
            "contradictions": contradictions,
            "reasoning": self._generate_reasoning(review_list, synthesis, conflicts, action),
            "timestamp": datetime.utcnow().isoformat(),
            "thresholds_used": {
                "auto_merge": self.thresholds.auto_merge,
                "security_veto": self.thresholds.security_veto,
                "sovereignty_minimum": self.thresholds.sovereignty_minimum,
            },
            "pr_number": pr_data.get("number"),
            "pr_title": pr_data.get("title"),
        }
        
        return decision
    
    def _extract_contradictions(self, reviews: List[Dict]) -> List[Dict[str, Any]]:
        """Extract contradictions between reviews"""
        contradictions = []
        
        # Compare approval status
        approvals = [r.get("approve", False) for r in reviews if r.get("status") != "error"]
        
        if True in approvals and False in approvals:
            contradictions.append({
                "type": "approval_conflict",
                "description": "Reviews have conflicting approval decisions",
                "details": [
                    f"{r.get('type', 'unknown')}: {'approve' if r.get('approve') else 'reject'}"
                    for r in reviews
                ],
            })
        
        # Check for conflicting severity assessments
        security_review = next((r for r in reviews if r.get("type") == "security"), None)
        
        if security_review and security_review.get("severity") in ["critical", "high"]:
            # Check if other reviews approve
            other_approvals = [
                r for r in reviews
                if r.get("type") != "security" and r.get("approve", False)
            ]
            
            if other_approvals:
                contradictions.append({
                    "type": "security_override",
                    "description": "Security concerns vs other approvals",
                    "severity": security_review.get("severity"),
                })
        
        return contradictions
    
    def _calculate_scores(self, reviews: List[Dict]) -> Dict[str, float]:
        """Calculate composite scores from reviews"""
        scores = {
            "security": 0.0,
            "architecture": 0.0,
            "sovereignty": 0.0,
            "performance": 0.0,
            "overall": 0.0,
        }
        
        for review in reviews:
            review_type = review.get("type", "")
            confidence = review.get("confidence", 0.0)
            
            if review_type == "security":
                severity = review.get("severity", "none")
                severity_score = {
                    "none": 1.0,
                    "low": 0.9,
                    "medium": 0.7,
                    "high": 0.4,
                    "critical": 0.0,
                }.get(severity, 0.5)
                scores["security"] = severity_score * confidence
            
            elif review_type == "architecture":
                quality_score = review.get("quality_score", 0.0)
                scores["architecture"] = quality_score * confidence
            
            elif review_type == "sovereignty":
                sovereignty_score = review.get("sovereignty_score", 0.0)
                scores["sovereignty"] = sovereignty_score * confidence
            
            elif review_type == "performance":
                perf_score = review.get("performance_score", 0.0)
                scores["performance"] = perf_score * confidence
        
        # Calculate overall score (weighted average)
        weights = {
            "security": 0.35,
            "architecture": 0.25,
            "sovereignty": 0.25,
            "performance": 0.15,
        }
        
        scores["overall"] = sum(
            scores.get(key, 0) * weight
            for key, weight in weights.items()
        )
        
        return scores
    
    def _dialectical_synthesis(
        self,
        reviews: List[Dict],
        contradictions: List[Dict],
        scores: Dict[str, float],
    ) -> Dict[str, Any]:
        """Apply dialectical synthesis to resolve contradictions"""
        
        synthesis = {
            "thesis": None,
            "antithesis": None,
            "synthesis": None,
            "resolution": "approved" if scores["overall"] >= 0.8 else "needs_review",
        }
        
        # If no contradictions, simple synthesis
        if not contradictions:
            synthesis["synthesis"] = "Unanimous agreement across all review domains"
            synthesis["resolution"] = "approved" if all(
                r.get("approve", False) for r in reviews if r.get("status") != "error"
            ) else "rejected"
            return synthesis
        
        # Process contradictions
        for contradiction in contradictions:
            if contradiction["type"] == "approval_conflict":
                synthesis["thesis"] = "Some reviews approve the changes"
                synthesis["antithesis"] = "Some reviews reject the changes"
                
                # Resolve based on severity
                security_review = next((r for r in reviews if r.get("type") == "security"), None)
                
                if security_review and security_review.get("severity") in ["critical", "high"]:
                    synthesis["synthesis"] = "Security concerns take precedence"
                    synthesis["resolution"] = "rejected"
                elif scores["overall"] >= self.thresholds.auto_merge:
                    synthesis["synthesis"] = "Overall quality sufficient despite minor disagreements"
                    synthesis["resolution"] = "approved"
                else:
                    synthesis["synthesis"] = "Human review required to resolve conflicts"
                    synthesis["resolution"] = "review_required"
            
            elif contradiction["type"] == "security_override":
                synthesis["thesis"] = "Code quality and architecture are acceptable"
                synthesis["antithesis"] = f"Security concerns: {contradiction.get('severity')}"
                synthesis["synthesis"] = "Security issues must be addressed before merge"
                synthesis["resolution"] = "rejected"
        
        return synthesis
    
    def _calculate_confidence(
        self,
        reviews: List[Dict],
        synthesis: Dict[str, Any],
        conflicts: Dict[str, Any],
    ) -> float:
        """Calculate merge confidence based on review consensus"""
        
        # Start with base confidence from reviews
        review_confidences = [
            r.get("confidence", 0.0)
            for r in reviews
            if r.get("status") != "error"
        ]
        
        if not review_confidences:
            return 0.0
        
        avg_confidence = sum(review_confidences) / len(review_confidences)
        
        # Check if all reviews approve
        all_approve = all(
            r.get("approve", False)
            for r in reviews
            if r.get("status") != "error"
        )
        
        if not all_approve:
            avg_confidence *= 0.5  # Significant penalty for non-unanimous approval
        
        # Penalty for conflicts
        conflict_count = conflicts.get("conflict_count", 0)
        conflict_penalty = min(0.3, conflict_count * 0.1)
        
        avg_confidence -= conflict_penalty
        
        # Penalty for critical security issues
        security_review = next((r for r in reviews if r.get("type") == "security"), None)
        if security_review:
            if security_review.get("severity") == "critical":
                avg_confidence = 0.0
            elif security_review.get("severity") == "high":
                avg_confidence *= 0.3
        
        # Bonus for sovereignty alignment
        sovereignty_review = next((r for r in reviews if r.get("type") == "sovereignty"), None)
        if sovereignty_review:
            sovereignty_score = sovereignty_review.get("sovereignty_score", 0.0)
            if sovereignty_score >= 0.8:
                avg_confidence += 0.05
        
        return max(0.0, min(1.0, avg_confidence))
    
    def _make_decision(
        self,
        confidence: float,
        reviews: List[Dict],
        conflicts: Dict[str, Any],
    ) -> str:
        """Make final merge decision"""
        
        # Critical conflicts block merge
        if conflicts.get("severity") in ["critical", "high"]:
            return "blocked"
        
        # Security veto
        security_review = next((r for r in reviews if r.get("type") == "security"), None)
        if security_review:
            security_confidence = security_review.get("confidence", 0.0)
            if security_confidence < self.thresholds.security_veto:
                return "review_required"
            if security_review.get("severity") in ["critical", "high"]:
                return "blocked"
        
        # Sovereignty minimum
        sovereignty_review = next((r for r in reviews if r.get("type") == "sovereignty"), None)
        if sovereignty_review:
            sovereignty_score = sovereignty_review.get("sovereignty_score", 0.0)
            if sovereignty_score < self.thresholds.sovereignty_minimum:
                return "review_required"
        
        # Auto-merge threshold
        if confidence >= self.thresholds.auto_merge:
            return "merge"
        
        return "review_required"
    
    def _generate_reasoning(
        self,
        reviews: List[Dict],
        synthesis: Dict[str, Any],
        conflicts: Dict[str, Any],
        action: str,
    ) -> str:
        """Generate human-readable reasoning for the decision"""
        
        reasons = []
        
        # Add synthesis explanation
        if synthesis.get("synthesis"):
            reasons.append(f"Synthesis: {synthesis['synthesis']}")
        
        # Add action-specific reasoning
        if action == "merge":
            reasons.append("All review criteria met for automatic merge")
            
            # Add review summaries
            for review in reviews:
                review_type = review.get("type", "unknown")
                approve = "✅" if review.get("approve") else "❌"
                confidence = review.get("confidence", 0.0)
                reasons.append(f"  {approve} {review_type}: {confidence:.0%} confidence")
        
        elif action == "blocked":
            reasons.append("Merge blocked due to critical issues")
            
            if conflicts.get("severity") in ["critical", "high"]:
                reasons.append(f"  - Conflicts: {conflicts.get('conflict_count', 0)} found")
            
            for review in reviews:
                if review.get("severity") in ["critical", "high"]:
                    reasons.append(f"  - {review.get('type')}: {review.get('severity')} severity")
        
        elif action == "review_required":
            reasons.append("Human review required before merge")
            reasons.append(f"  - Confidence: {synthesis.get('resolution', 'unknown')}")
        
        return "\n".join(reasons)

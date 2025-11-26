"""
Unified Verifier

Orchestrates all verification steps for Grok-5 deployment.
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional

from .safety_gate import SafetyGate, SafetyReport
from .audit_logger import AuditLogger, AuditEvent


class VerificationStatus(Enum):
    """Status of verification."""

    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    BLOCKED = "blocked"


@dataclass
class VerificationResult:
    """Result of unified verification."""

    status: VerificationStatus
    safety_report: Optional[SafetyReport] = None
    opa_passed: bool = True
    deployment_approved: bool = False
    blockers: list[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.utcnow)


class UnifiedVerifier:
    """
    Unified verification orchestrator for Grok-5 deployment.

    Combines:
    - Safety gate checks
    - OPA policy validation
    - Deployment approval workflow
    - Audit logging
    """

    def __init__(
        self,
        safety_gate: Optional[SafetyGate] = None,
        audit_logger: Optional[AuditLogger] = None,
        opa_endpoint: Optional[str] = None,
        logger: Optional[logging.Logger] = None,
    ):
        """
        Initialize unified verifier.

        Args:
            safety_gate: Safety gate instance
            audit_logger: Audit logger instance
            opa_endpoint: OPA server endpoint for policy checks
            logger: Logger instance
        """
        self.safety = safety_gate or SafetyGate()
        self.audit = audit_logger or AuditLogger()
        self.opa_endpoint = opa_endpoint
        self.log = logger or logging.getLogger(__name__)

    def verify(self, deployment_id: str) -> VerificationResult:
        """
        Run full verification for deployment.

        Args:
            deployment_id: Unique deployment identifier

        Returns:
            VerificationResult with all check results
        """
        self.log.info(f"Starting verification for deployment: {deployment_id}")

        # Log verification start
        self.audit.log(AuditEvent(
            event_type="verification_start",
            deployment_id=deployment_id,
            details={"status": "running"},
        ))

        result = VerificationResult(status=VerificationStatus.RUNNING)

        # Run safety gate
        safety_report = self.safety.evaluate()
        result.safety_report = safety_report

        if not safety_report.ok:
            result.blockers.extend(safety_report.reasons)

        # Run OPA policy checks
        opa_passed = self._check_opa_policies(deployment_id)
        result.opa_passed = opa_passed

        if not opa_passed:
            result.blockers.append("OPA policy check failed")

        # Determine final status
        if result.blockers:
            result.status = VerificationStatus.FAILED
            result.deployment_approved = False
        else:
            result.status = VerificationStatus.PASSED
            result.deployment_approved = True

        # Log verification result
        self.audit.log(AuditEvent(
            event_type="verification_complete",
            deployment_id=deployment_id,
            details={
                "status": result.status.value,
                "approved": result.deployment_approved,
                "blockers": result.blockers,
            },
        ))

        self.log.info(
            f"Verification complete: deployment={deployment_id} "
            f"status={result.status.value} "
            f"approved={result.deployment_approved}"
        )

        return result

    def _check_opa_policies(self, deployment_id: str) -> bool:
        """
        Check OPA policies.

        Args:
            deployment_id: Deployment identifier

        Returns:
            True if all policies pass
        """
        if not self.opa_endpoint:
            self.log.debug("No OPA endpoint configured, skipping policy check")
            return True

        try:
            import requests

            # Check each policy
            policies = [
                "data_quality",
                "energy_threshold",
                "training_safety",
                "deployment_approval",
            ]

            for policy in policies:
                url = f"{self.opa_endpoint}/v1/data/colossus/{policy}/allow"
                response = requests.post(url, json={"input": {}}, timeout=5)

                if response.status_code != 200:
                    self.log.warning(f"OPA policy check failed: {policy}")
                    return False

                result = response.json().get("result", False)
                if not result:
                    self.log.warning(f"OPA policy denied: {policy}")
                    return False

            return True

        except Exception as e:
            self.log.error(f"OPA policy check error: {e}")
            return False

    def quick_check(self) -> bool:
        """
        Run quick verification (safety gate only).

        Returns:
            True if safety gate passes
        """
        report = self.safety.evaluate()
        return report.ok

    def get_status(self, deployment_id: str) -> VerificationStatus:
        """
        Get verification status for deployment.

        Args:
            deployment_id: Deployment identifier

        Returns:
            Current verification status
        """
        # In production, this would check persistent storage
        return VerificationStatus.PENDING

    def approve_manual(
        self,
        deployment_id: str,
        approver: str,
        notes: Optional[str] = None,
    ) -> bool:
        """
        Manually approve deployment (for overrides).

        Args:
            deployment_id: Deployment identifier
            approver: Identity of approver
            notes: Approval notes

        Returns:
            True if approval recorded
        """
        self.audit.log(AuditEvent(
            event_type="manual_approval",
            deployment_id=deployment_id,
            user=approver,
            details={"notes": notes or "No notes provided"},
        ))

        self.log.warning(
            f"Manual approval: deployment={deployment_id} approver={approver}"
        )

        return True

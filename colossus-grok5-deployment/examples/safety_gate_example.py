#!/usr/bin/env python3
"""
Safety Gate Example

Demonstrates how to use the SafetyGate for pre-deployment verification.

Artifact #3558 - Colossus Grok-5 Deployment Suite
"""

import logging
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from verification.safety_gate import SafetyGate, SafetyReport
from verification.unified_verifier import UnifiedVerifier
from verification.audit_logger import AuditLogger, AuditEvent


class MockMetricsClient:
    """Mock metrics client for demonstration."""

    def __init__(
        self,
        power_mw: float = 200.0,
        nox_rate: float = 0.5,
        nox_limit: float = 1.0,
    ):
        self._power = power_mw
        self._nox_rate = nox_rate
        self._nox_limit = nox_limit

    def power_mw(self) -> float:
        return self._power

    def nox_emissions_rate(self) -> float:
        return self._nox_rate

    def nox_permit_limit(self) -> float:
        return self._nox_limit


class MockProvenanceClient:
    """Mock provenance client for demonstration."""

    def __init__(self, verified: bool = True):
        self._verified = verified

    def latest_root_verified(self) -> bool:
        return self._verified


class MockCheckpointClient:
    """Mock checkpoint client for demonstration."""

    def __init__(self, consensus: float = 0.995):
        self._consensus = consensus

    def latest_consensus_fraction(self) -> float:
        return self._consensus


class MockEvalClient:
    """Mock evaluation client for demonstration."""

    def __init__(
        self,
        bias: float = 0.15,
        hallucination: float = 0.10,
    ):
        self._bias = bias
        self._hallucination = hallucination

    def bias_score(self) -> float:
        return self._bias

    def hallucination_rate(self) -> float:
        return self._hallucination


def run_safety_gate_example():
    """Run the safety gate example."""
    print("=" * 60)
    print("Safety Gate Example - Colossus Grok-5")
    print("=" * 60)
    print()

    # Scenario 1: All checks pass
    print("Scenario 1: All checks pass")
    print("-" * 40)

    gate = SafetyGate(
        metrics_client=MockMetricsClient(power_mw=200.0),
        provenance_client=MockProvenanceClient(verified=True),
        checkpoint_client=MockCheckpointClient(consensus=0.995),
        eval_client=MockEvalClient(bias=0.15, hallucination=0.10),
    )

    report = gate.evaluate()
    print_report(report)

    # Scenario 2: Power exceeded
    print("\nScenario 2: Power exceeded")
    print("-" * 40)

    gate = SafetyGate(
        metrics_client=MockMetricsClient(power_mw=280.0),  # Over limit
        provenance_client=MockProvenanceClient(verified=True),
        checkpoint_client=MockCheckpointClient(consensus=0.995),
        eval_client=MockEvalClient(bias=0.15, hallucination=0.10),
    )

    report = gate.evaluate()
    print_report(report)

    # Scenario 3: Multiple failures
    print("\nScenario 3: Multiple failures")
    print("-" * 40)

    gate = SafetyGate(
        metrics_client=MockMetricsClient(power_mw=260.0),  # Over limit
        provenance_client=MockProvenanceClient(verified=False),  # Failed
        checkpoint_client=MockCheckpointClient(consensus=0.85),  # Low
        eval_client=MockEvalClient(bias=0.30, hallucination=0.20),  # High
    )

    report = gate.evaluate()
    print_report(report)


def run_unified_verifier_example():
    """Run the unified verifier example."""
    print()
    print("=" * 60)
    print("Unified Verifier Example")
    print("=" * 60)
    print()

    # Set up logging
    logging.basicConfig(level=logging.WARNING)  # Reduce noise

    # Create audit logger
    import tempfile
    audit_dir = tempfile.mkdtemp()
    audit_logger = AuditLogger(log_dir=audit_dir)

    # Create safety gate
    gate = SafetyGate(
        metrics_client=MockMetricsClient(power_mw=200.0),
        provenance_client=MockProvenanceClient(verified=True),
        checkpoint_client=MockCheckpointClient(consensus=0.995),
        eval_client=MockEvalClient(bias=0.15, hallucination=0.10),
    )

    # Create verifier
    verifier = UnifiedVerifier(
        safety_gate=gate,
        audit_logger=audit_logger,
    )

    # Run verification
    print("Running unified verification...")
    result = verifier.verify(deployment_id="deploy-example-001")

    print()
    print("Verification Result:")
    print(f"  Status: {result.status.value}")
    print(f"  Deployment Approved: {result.deployment_approved}")
    print(f"  OPA Passed: {result.opa_passed}")
    if result.blockers:
        print(f"  Blockers: {result.blockers}")
    print()

    # Show audit chain
    print("Audit Chain:")
    for event in audit_logger.get_events():
        print(f"  [{event.event_type}] {event.details}")
    print()

    # Verify chain integrity
    is_valid = audit_logger.verify_chain()
    print(f"Audit chain integrity: {'✓ VALID' if is_valid else '✗ INVALID'}")


def print_report(report: SafetyReport):
    """Print a safety report."""
    status = "✓ PASSED" if report.ok else "✗ FAILED"
    print(f"Status: {status}")
    print(f"Checks: {report.checks_passed}/{report.checks_total} passed")
    print(f"Pass Rate: {report.pass_rate:.0%}")

    if report.reasons:
        print("Failure Reasons:")
        for reason in report.reasons:
            print(f"  • {reason}")
    else:
        print("All checks passed!")


def main():
    """Run all examples."""
    run_safety_gate_example()
    run_unified_verifier_example()

    print()
    print("=" * 60)
    print("Safety gate example complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()

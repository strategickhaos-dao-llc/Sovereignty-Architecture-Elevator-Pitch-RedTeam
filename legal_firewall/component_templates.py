#!/usr/bin/env python3
"""
Component Templates Module
Strategickhaos DAO LLC - Legally-Bounded Generative Systems Engineering (LB-GSE)

This module provides templates for auto-generating component specifications
based on legal requirements detected by the Legal-Firewall Generator.

Templates define the structure, interfaces, and requirements for each
type of component that may be needed to satisfy legal constraints.
"""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class ComponentSpec:
    """Specification for a software component to be built."""
    
    name: str
    description: str
    legal_basis: str
    interfaces: list
    dependencies: list
    security_requirements: list
    compliance_tags: list
    estimated_effort: str
    priority: str
    created_at: str = ""
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()


# Template definitions for common legal-constraint components
COMPONENT_TEMPLATES = {
    "immutable_event_logger": {
        "description": "Append-only log system with cryptographic hashing for audit trails",
        "interfaces": [
            "log_event(event_type: str, data: dict) -> str",
            "verify_chain() -> bool",
            "get_events(since: datetime) -> List[Event]",
            "export_audit_trail(format: str) -> bytes"
        ],
        "dependencies": ["hashlib", "datetime", "json"],
        "security_requirements": [
            "Append-only enforcement at storage level",
            "SHA-256 hash chain for tamper detection",
            "Timestamp from trusted source",
            "Access control for read/write operations"
        ],
        "compliance_tags": ["Wyoming DAO LLC", "Audit Trail", "SOC2"]
    },
    
    "percentage_validator": {
        "description": "Validates charitable percentage requirements are maintained",
        "interfaces": [
            "validate_allocation(amount: float, total: float) -> bool",
            "get_current_percentage() -> float",
            "check_compliance() -> ComplianceResult",
            "get_violation_report() -> Report"
        ],
        "dependencies": ["decimal"],
        "security_requirements": [
            "Cannot be bypassed for fund movements",
            "Alerts on threshold violations",
            "Immutable percentage configuration"
        ],
        "compliance_tags": ["Charitable Constraint", "Fund Management"]
    },
    
    "risk_assessment_agent": {
        "description": "AI agent for evaluating risks before executing DAO proposals",
        "interfaces": [
            "assess_risk(proposal: Proposal) -> RiskScore",
            "get_risk_factors() -> List[RiskFactor]",
            "simulate_outcome(proposal: Proposal) -> Simulation",
            "recommend_action(risk_score: RiskScore) -> Recommendation"
        ],
        "dependencies": ["numpy", "transformers"],
        "security_requirements": [
            "Model outputs must be auditable",
            "Human override capability required",
            "No autonomous execution without approval"
        ],
        "compliance_tags": ["Fiduciary Duty", "Due Care", "AI Governance"]
    },
    
    "proposal_simulator": {
        "description": "Sandbox environment for testing proposal outcomes before deployment",
        "interfaces": [
            "create_sandbox() -> SandboxId",
            "execute_proposal(sandbox_id: str, proposal: Proposal) -> Result",
            "get_state_diff(sandbox_id: str) -> StateDiff",
            "cleanup_sandbox(sandbox_id: str) -> None"
        ],
        "dependencies": ["docker", "subprocess"],
        "security_requirements": [
            "Complete isolation from production state",
            "Resource limits enforced",
            "Deterministic execution",
            "Results signed and logged"
        ],
        "compliance_tags": ["Fiduciary Duty", "Due Care", "Testing"]
    },
    
    "governance_reporter": {
        "description": "Automated generator for transparent governance reports",
        "interfaces": [
            "generate_report(period: str) -> Report",
            "get_voting_summary() -> VotingSummary",
            "export_report(format: str) -> bytes",
            "schedule_report(frequency: str) -> ScheduleId"
        ],
        "dependencies": ["jinja2", "reportlab"],
        "security_requirements": [
            "Reports must be cryptographically signed",
            "Historical reports immutable",
            "Access control for sensitive data"
        ],
        "compliance_tags": ["Transparency", "Governance", "Reporting"]
    },
    
    "vote_explainer_agent": {
        "description": "AI agent that explains vote rationale to stakeholders",
        "interfaces": [
            "explain_vote(vote_id: str) -> Explanation",
            "summarize_discussion(proposal_id: str) -> Summary",
            "generate_faq(topic: str) -> FAQ",
            "answer_question(question: str) -> Answer"
        ],
        "dependencies": ["openai", "langchain"],
        "security_requirements": [
            "Must cite sources for explanations",
            "AI-generated content disclaimer required",
            "Cannot fabricate vote rationales"
        ],
        "compliance_tags": ["Transparency", "AI Governance", "Communication"]
    },
    
    "policy_enforcement_firewall": {
        "description": "Firewall that enforces liability boundaries and permissioning",
        "interfaces": [
            "check_permission(actor: str, action: str) -> bool",
            "enforce_boundary(action: Action) -> Result",
            "get_policy_violations() -> List[Violation]",
            "update_policy(policy: Policy) -> None"
        ],
        "dependencies": ["yaml", "jsonschema"],
        "security_requirements": [
            "Fail-closed design (deny by default)",
            "Policy changes require multi-sig approval",
            "All decisions logged immutably"
        ],
        "compliance_tags": ["Liability", "Access Control", "Security"]
    },
    
    "legal_action_validator": {
        "description": "Validates actions against legal scope boundaries",
        "interfaces": [
            "validate_action(action: Action) -> ValidationResult",
            "get_legal_bounds() -> LegalBounds",
            "check_jurisdiction(action: Action) -> JurisdictionResult",
            "get_prohibited_actions() -> List[str]"
        ],
        "dependencies": ["pydantic"],
        "security_requirements": [
            "Cannot be disabled without governance vote",
            "Validation logic auditable",
            "Integration with legal primitive definitions"
        ],
        "compliance_tags": ["Liability", "Legal Compliance", "Validation"]
    },
    
    "ai_disclaimer_system": {
        "description": "System for injecting AI-generated content disclaimers",
        "interfaces": [
            "add_disclaimer(content: str, source: str) -> str",
            "detect_ai_content(text: str) -> bool",
            "get_disclaimer_template(content_type: str) -> str",
            "validate_disclaimer(content: str) -> bool"
        ],
        "dependencies": [],
        "security_requirements": [
            "Disclaimers cannot be stripped by downstream processing",
            "Audit trail for all AI-generated content",
            "Configurable disclaimer templates"
        ],
        "compliance_tags": ["AI Governance", "Transparency", "Disclosure"]
    },
    
    "human_oversight_system": {
        "description": "Gate system requiring human approval for critical decisions",
        "interfaces": [
            "request_approval(decision: Decision) -> ApprovalRequest",
            "approve(request_id: str, approver: str) -> Result",
            "reject(request_id: str, approver: str, reason: str) -> Result",
            "get_pending_approvals() -> List[ApprovalRequest]"
        ],
        "dependencies": ["asyncio"],
        "security_requirements": [
            "Multi-factor authentication for approvers",
            "Time-limited approval windows",
            "Escalation for stale requests",
            "Cannot be bypassed for critical actions"
        ],
        "compliance_tags": ["AI Governance", "Human Oversight", "Critical Decisions"]
    },
    
    "conflict_registry": {
        "description": "Registry for tracking and disclosing conflicts of interest",
        "interfaces": [
            "register_conflict(member: str, conflict: Conflict) -> str",
            "check_conflicts(member: str, proposal: Proposal) -> List[Conflict]",
            "get_all_conflicts() -> List[Conflict]",
            "resolve_conflict(conflict_id: str, resolution: str) -> Result"
        ],
        "dependencies": [],
        "security_requirements": [
            "Conflicts immutably recorded",
            "Automatic conflict checking on votes",
            "Privacy controls for sensitive disclosures"
        ],
        "compliance_tags": ["Fiduciary Duty", "Loyalty", "Disclosure"]
    },
    
    "fund_lockup_contract": {
        "description": "Smart contract preventing withdrawal of irrevocable funds",
        "interfaces": [
            "lock_funds(amount: float, duration: str) -> LockId",
            "get_locked_amount() -> float",
            "attempt_withdrawal(amount: float) -> Result",
            "get_lock_status() -> LockStatus"
        ],
        "dependencies": ["web3"],
        "security_requirements": [
            "On-chain enforcement",
            "No admin bypass capability",
            "Time-lock for any modifications",
            "Multi-sig for emergency actions"
        ],
        "compliance_tags": ["Charitable Constraint", "Fund Management", "Smart Contract"]
    }
}


class ComponentTemplateEngine:
    """
    Engine for generating component specifications from templates.
    
    Uses the COMPONENT_TEMPLATES to create specifications that satisfy
    legal requirements detected by the Legal-Firewall Generator.
    """
    
    def __init__(self):
        self.templates = COMPONENT_TEMPLATES.copy()
    
    def get_template(self, component_name: str) -> Optional[dict]:
        """
        Get template for a component type.
        
        Args:
            component_name: Name of the component template.
            
        Returns:
            Template dictionary or None if not found.
        """
        return self.templates.get(component_name)
    
    def generate_spec(
        self,
        component_name: str,
        legal_basis: str,
        priority: str = "medium",
        estimated_effort: str = "medium"
    ) -> Optional[ComponentSpec]:
        """
        Generate a component specification from a template.
        
        Args:
            component_name: Name of the component template to use.
            legal_basis: Legal requirement that necessitates this component.
            priority: Development priority (critical, high, medium, low).
            estimated_effort: Estimated development effort (low, medium, high).
            
        Returns:
            ComponentSpec object or None if template not found.
        """
        template = self.get_template(component_name)
        
        if template is None:
            return None
        
        return ComponentSpec(
            name=component_name,
            description=template["description"],
            legal_basis=legal_basis,
            interfaces=template["interfaces"],
            dependencies=template["dependencies"],
            security_requirements=template["security_requirements"],
            compliance_tags=template["compliance_tags"],
            estimated_effort=estimated_effort,
            priority=priority
        )
    
    def generate_specs_for_requirements(self, required_components: list) -> list:
        """
        Generate specifications for all required components.
        
        Args:
            required_components: List of RequiredComponent objects from generator.
            
        Returns:
            List of ComponentSpec objects.
        """
        specs = []
        
        for req_comp in required_components:
            spec = self.generate_spec(
                component_name=req_comp.name,
                legal_basis=req_comp.legal_source,
                priority=req_comp.priority,
                estimated_effort=req_comp.estimated_effort
            )
            
            if spec:
                specs.append(spec)
            else:
                # Generate a basic spec for unknown components
                specs.append(ComponentSpec(
                    name=req_comp.name,
                    description=req_comp.description,
                    legal_basis=req_comp.legal_source,
                    interfaces=["TBD - requires design"],
                    dependencies=[],
                    security_requirements=["TBD - requires security review"],
                    compliance_tags=[req_comp.constraint_type],
                    estimated_effort=req_comp.estimated_effort,
                    priority=req_comp.priority
                ))
        
        return specs
    
    def export_spec_to_yaml(self, spec: ComponentSpec) -> str:
        """
        Export a component specification to YAML format.
        
        Args:
            spec: ComponentSpec to export.
            
        Returns:
            YAML string representation.
        """
        import yaml
        
        spec_dict = {
            "component": {
                "name": spec.name,
                "description": spec.description,
                "legal_basis": spec.legal_basis,
                "interfaces": spec.interfaces,
                "dependencies": spec.dependencies,
                "security_requirements": spec.security_requirements,
                "compliance_tags": spec.compliance_tags,
                "estimated_effort": spec.estimated_effort,
                "priority": spec.priority,
                "created_at": spec.created_at
            }
        }
        
        return yaml.dump(spec_dict, default_flow_style=False, sort_keys=False)
    
    def export_spec_to_markdown(self, spec: ComponentSpec) -> str:
        """
        Export a component specification to Markdown format.
        
        Args:
            spec: ComponentSpec to export.
            
        Returns:
            Markdown string representation.
        """
        lines = [
            f"# Component Specification: {spec.name}",
            "",
            f"**Created:** {spec.created_at}",
            f"**Priority:** {spec.priority}",
            f"**Estimated Effort:** {spec.estimated_effort}",
            "",
            "## Description",
            "",
            spec.description,
            "",
            "## Legal Basis",
            "",
            spec.legal_basis,
            "",
            "## Interfaces",
            "",
        ]
        
        for interface in spec.interfaces:
            lines.append(f"- `{interface}`")
        
        lines.extend([
            "",
            "## Dependencies",
            "",
        ])
        
        if spec.dependencies:
            for dep in spec.dependencies:
                lines.append(f"- {dep}")
        else:
            lines.append("- None")
        
        lines.extend([
            "",
            "## Security Requirements",
            "",
        ])
        
        for req in spec.security_requirements:
            lines.append(f"- {req}")
        
        lines.extend([
            "",
            "## Compliance Tags",
            "",
            ", ".join(f"`{tag}`" for tag in spec.compliance_tags),
            ""
        ])
        
        return "\n".join(lines)


if __name__ == "__main__":
    # Example usage
    engine = ComponentTemplateEngine()
    
    print("Available Component Templates:")
    print("-" * 40)
    
    for name in engine.templates:
        template = engine.templates[name]
        print(f"\n📦 {name}")
        print(f"   {template['description']}")
        print(f"   Tags: {', '.join(template['compliance_tags'])}")

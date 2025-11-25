"""
Data Models for Legal Firewall Engine
Strategickhaos DAO LLC

Defines the core data structures used throughout the LB-GSE implementation.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Dict, Any
from datetime import datetime


class PrimitiveCategory(Enum):
    """Categories for legal primitives extracted from documents."""
    OBLIGATION = "obligation"
    CONSTRAINT = "constraint"
    PROHIBITION = "prohibition"
    PERMISSION = "permission"
    DEFINITION = "definition"


class CapabilityType(Enum):
    """Types of system capabilities that can be required or implemented."""
    VALIDATOR = "validator"
    AGENT = "agent"
    GOVERNANCE_ENGINE = "governance_engine"
    LOGGER = "logger"
    INTEGRATION = "integration"
    REGISTRY = "registry"
    SECURITY = "security"
    REPORTING = "reporting"


class ComponentStatus(Enum):
    """Status of a component in the registry."""
    IMPLEMENTED = "implemented"
    PLANNED = "planned"
    DEPRECATED = "deprecated"
    IN_PROGRESS = "in_progress"


@dataclass
class LegalPrimitive:
    """
    A legal primitive is a discrete, actionable clause extracted from legal documents.
    Each primitive represents a single legal requirement, constraint, or obligation.
    """
    id: str
    source_file: str
    category: PrimitiveCategory
    text: str
    tags: List[str] = field(default_factory=list)
    line_number: Optional[int] = None
    section: Optional[str] = None
    confidence: float = 1.0
    extracted_at: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "id": self.id,
            "source_file": self.source_file,
            "category": self.category.value,
            "text": self.text,
            "tags": self.tags,
            "line_number": self.line_number,
            "section": self.section,
            "confidence": self.confidence,
            "extracted_at": self.extracted_at.isoformat(),
        }


@dataclass
class CapabilityRequirement:
    """
    A capability requirement is derived from one or more legal primitives.
    It describes a system capability that must be implemented to satisfy
    the legal obligations.
    """
    id: str
    primitive_id: str
    capability_type: CapabilityType
    description: str
    implementation_notes: str = ""
    test_expectations: List[str] = field(default_factory=list)
    priority: int = 5  # 1-10 scale, 10 being highest
    tags: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "id": self.id,
            "primitive_id": self.primitive_id,
            "capability_type": self.capability_type.value,
            "description": self.description,
            "implementation_notes": self.implementation_notes,
            "test_expectations": self.test_expectations,
            "priority": self.priority,
            "tags": self.tags,
        }


@dataclass
class ComponentInfo:
    """
    Information about an implemented component discovered in the repository
    or defined in the component registry.
    """
    id: str
    path: str
    description: str
    capability_type: CapabilityType
    tags: List[str] = field(default_factory=list)
    status: ComponentStatus = ComponentStatus.IMPLEMENTED
    discovered_at: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "id": self.id,
            "path": self.path,
            "description": self.description,
            "capability_type": self.capability_type.value,
            "tags": self.tags,
            "status": self.status.value,
            "discovered_at": self.discovered_at.isoformat(),
        }


@dataclass
class CapabilityGap:
    """
    A capability gap represents a legally required capability that is not
    yet fully implemented in the system.
    """
    requirement: CapabilityRequirement
    covering_components: List[ComponentInfo] = field(default_factory=list)
    coverage_score: float = 0.0  # 0.0 = no coverage, 1.0 = fully covered
    priority_score: float = 0.0  # Combined score for prioritization
    stub_path: Optional[str] = None
    
    @property
    def is_fully_implemented(self) -> bool:
        """Check if the requirement is fully covered."""
        return self.coverage_score >= 1.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "requirement": self.requirement.to_dict(),
            "covering_components": [c.to_dict() for c in self.covering_components],
            "coverage_score": self.coverage_score,
            "priority_score": self.priority_score,
            "is_fully_implemented": self.is_fully_implemented,
            "stub_path": self.stub_path,
        }


@dataclass
class FirewallReport:
    """
    The complete report generated by the Legal Firewall Engine.
    Contains all extracted primitives, requirements, components, and gaps.
    """
    primitives: List[LegalPrimitive] = field(default_factory=list)
    requirements: List[CapabilityRequirement] = field(default_factory=list)
    components: List[ComponentInfo] = field(default_factory=list)
    gaps: List[CapabilityGap] = field(default_factory=list)
    generated_at: datetime = field(default_factory=datetime.utcnow)
    legal_paths: List[str] = field(default_factory=list)
    repo_path: str = "."
    
    @property
    def total_requirements(self) -> int:
        """Total number of requirements identified."""
        return len(self.requirements)
    
    @property
    def covered_requirements(self) -> int:
        """Number of requirements with full coverage."""
        return sum(1 for g in self.gaps if g.is_fully_implemented)
    
    @property
    def coverage_percentage(self) -> float:
        """Overall coverage percentage."""
        if not self.requirements:
            return 100.0
        return (self.covered_requirements / self.total_requirements) * 100
    
    @property
    def high_priority_gaps(self) -> List[CapabilityGap]:
        """Gaps with priority score >= 7."""
        return [g for g in self.gaps if g.priority_score >= 7.0 and not g.is_fully_implemented]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "primitives": [p.to_dict() for p in self.primitives],
            "requirements": [r.to_dict() for r in self.requirements],
            "components": [c.to_dict() for c in self.components],
            "gaps": [g.to_dict() for g in self.gaps],
            "summary": {
                "total_primitives": len(self.primitives),
                "total_requirements": self.total_requirements,
                "total_components": len(self.components),
                "covered_requirements": self.covered_requirements,
                "coverage_percentage": self.coverage_percentage,
                "high_priority_gaps": len(self.high_priority_gaps),
            },
            "generated_at": self.generated_at.isoformat(),
            "legal_paths": self.legal_paths,
            "repo_path": self.repo_path,
        }
    
    def to_markdown(self) -> str:
        """Generate a human-readable Markdown report."""
        lines = [
            "# Legal Firewall Analysis Report",
            f"\n**Generated:** {self.generated_at.strftime('%Y-%m-%d %H:%M:%S UTC')}",
            f"**Repository:** `{self.repo_path}`",
            f"**Legal Documents Analyzed:** {len(self.legal_paths)}",
            "",
            "## Summary",
            "",
            f"- **Total Legal Primitives:** {len(self.primitives)}",
            f"- **Total Capability Requirements:** {self.total_requirements}",
            f"- **Discovered Components:** {len(self.components)}",
            f"- **Coverage:** {self.coverage_percentage:.1f}%",
            f"- **High-Priority Gaps:** {len(self.high_priority_gaps)}",
            "",
        ]
        
        # Legal Primitives section
        lines.extend([
            "## Extracted Legal Primitives",
            "",
        ])
        for prim in self.primitives[:20]:  # Limit to first 20
            lines.append(f"- **{prim.id}** [{prim.category.value}]: {prim.text[:100]}...")
        if len(self.primitives) > 20:
            lines.append(f"- ... and {len(self.primitives) - 20} more")
        lines.append("")
        
        # Requirements section
        lines.extend([
            "## Capability Requirements",
            "",
        ])
        for req in self.requirements[:15]:
            lines.append(f"- **{req.id}** ({req.capability_type.value}): {req.description}")
        if len(self.requirements) > 15:
            lines.append(f"- ... and {len(self.requirements) - 15} more")
        lines.append("")
        
        # Components section
        lines.extend([
            "## Discovered Components",
            "",
        ])
        for comp in self.components:
            status = "✅" if comp.status == ComponentStatus.IMPLEMENTED else "⏳"
            lines.append(f"- {status} **{comp.id}** ({comp.capability_type.value}): `{comp.path}`")
        lines.append("")
        
        # Gaps section
        lines.extend([
            "## Capability Gaps",
            "",
        ])
        uncovered = [g for g in self.gaps if not g.is_fully_implemented]
        for gap in sorted(uncovered, key=lambda g: -g.priority_score)[:10]:
            emoji = "🔴" if gap.priority_score >= 8 else "🟡" if gap.priority_score >= 5 else "🟢"
            lines.append(f"- {emoji} **{gap.requirement.id}** (Priority: {gap.priority_score:.1f})")
            lines.append(f"  - {gap.requirement.description}")
            lines.append(f"  - Coverage: {gap.coverage_score * 100:.0f}%")
        if len(uncovered) > 10:
            lines.append(f"- ... and {len(uncovered) - 10} more gaps")
        lines.append("")
        
        # TODOs section
        lines.extend([
            "## Recommended Actions",
            "",
        ])
        for i, gap in enumerate(sorted(uncovered, key=lambda g: -g.priority_score)[:5], 1):
            lines.append(f"{i}. Implement **{gap.requirement.capability_type.value}** for `{gap.requirement.primitive_id}`")
            if gap.requirement.implementation_notes:
                lines.append(f"   - Notes: {gap.requirement.implementation_notes}")
        
        return "\n".join(lines)

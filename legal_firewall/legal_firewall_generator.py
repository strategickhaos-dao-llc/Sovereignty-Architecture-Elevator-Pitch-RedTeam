#!/usr/bin/env python3
"""
Legal-Firewall Generator Module
Strategickhaos DAO LLC - Legally-Bounded Generative Systems Engineering (LB-GSE)

This module implements the LB-GSE methodology where legal architecture
(contracts, DAO operating agreements, fiduciary primitives, liability boundaries)
acts as a governance firewall that shapes the search space for new systems.

Software is generated, prioritized, or rejected based on whether it aligns
with the system's legal-ethical boundaries.

Definition:
    A software engineering methodology in which the legal architecture acts as a
    governance firewall that shapes, constrains, and expands the search space
    for new systems to build.
"""

import os
import yaml
from pathlib import Path
from typing import Any, Optional
from dataclasses import dataclass, field


@dataclass
class RequiredComponent:
    """Represents a software component required by legal constraints."""
    
    id: str
    name: str
    description: str
    legal_source: str
    constraint_type: str
    enforcement: str
    priority: str = "medium"
    estimated_effort: str = "medium"


@dataclass
class LegalRequirement:
    """Represents a legal requirement from a contract."""
    
    id: str
    description: str
    constraint_type: str
    enforcement: str


@dataclass
class AnalysisResult:
    """Result of analyzing a legal contract for required components."""
    
    total_requirements: int = 0
    implemented_components: list = field(default_factory=list)
    missing_components: list = field(default_factory=list)
    required_components: list = field(default_factory=list)
    compliance_score: float = 0.0


class LegalFirewallGenerator:
    """
    Analyzes legal primitives and detects required but unimplemented systems.
    
    This is the core engine of LB-GSE methodology that:
    1. Parses legal contracts (YAML format)
    2. Extracts governance rules and constraints
    3. Maps constraints to required software capabilities
    4. Detects gaps between requirements and implemented components
    5. Generates development requirements for missing capabilities
    
    Usage:
        generator = LegalFirewallGenerator()
        generator.load_contract("legal_firewall/contracts.yaml")
        required = generator.generate_required_components()
        
    The legal firewall forces the OS to invent missing components.
    """
    
    def __init__(self, component_registry: Optional[dict] = None):
        """
        Initialize the Legal Firewall Generator.
        
        Args:
            component_registry: Optional dict of existing components.
                               Keys are component IDs, values are component metadata.
        """
        self.contract: dict = {}
        self.component_registry: dict = component_registry or {}
        self.capability_mappings: dict = {}
        
    def load_contract(self, contract_path: str) -> dict:
        """
        Load and parse a legal contract from YAML file.
        
        Args:
            contract_path: Path to the YAML contract file.
            
        Returns:
            Parsed contract dictionary.
            
        Raises:
            FileNotFoundError: If contract file doesn't exist.
            yaml.YAMLError: If YAML parsing fails.
        """
        path = Path(contract_path)
        if not path.exists():
            raise FileNotFoundError(f"Contract file not found: {contract_path}")
            
        with open(path, 'r', encoding='utf-8') as f:
            self.contract = yaml.safe_load(f)
            
        # Extract component registry if present in contract
        if 'component_registry' in self.contract:
            registry = self.contract['component_registry']
            for component_id in registry.get('implemented', []):
                self.component_registry[component_id] = {"status": "implemented"}
                
        # Extract capability mappings
        if 'capability_mappings' in self.contract:
            self.capability_mappings = self.contract['capability_mappings']
            
        return self.contract
    
    def load_contract_from_string(self, yaml_content: str) -> dict:
        """
        Load and parse a legal contract from YAML string.
        
        Args:
            yaml_content: YAML content as string.
            
        Returns:
            Parsed contract dictionary.
        """
        self.contract = yaml.safe_load(yaml_content)
        
        if 'component_registry' in self.contract:
            registry = self.contract['component_registry']
            for component_id in registry.get('implemented', []):
                self.component_registry[component_id] = {"status": "implemented"}
                
        if 'capability_mappings' in self.contract:
            self.capability_mappings = self.contract['capability_mappings']
            
        return self.contract
    
    def component_exists(self, component_id: str) -> bool:
        """
        Check if a component exists in the registry.
        
        Args:
            component_id: ID of the component to check.
            
        Returns:
            True if component exists, False otherwise.
        """
        return component_id in self.component_registry
    
    def register_component(self, component_id: str, metadata: Optional[dict] = None) -> None:
        """
        Register a component as implemented.
        
        Args:
            component_id: ID of the component.
            metadata: Optional metadata about the component.
        """
        self.component_registry[component_id] = metadata or {"status": "implemented"}
    
    def _extract_requirements(self) -> list:
        """
        Extract all legal requirements from the loaded contract.
        
        Returns:
            List of LegalRequirement objects.
        """
        requirements = []
        
        legal_primitives = self.contract.get('legal_primitives', {})
        
        for category_name, category_data in legal_primitives.items():
            if isinstance(category_data, dict):
                # Handle nested structure (e.g., fiduciary_duties.duty_of_care)
                for subcategory_name, subcategory_data in category_data.items():
                    if isinstance(subcategory_data, dict):
                        # Check for 'requirements' list
                        if 'requirements' in subcategory_data:
                            for req in subcategory_data['requirements']:
                                requirements.append(LegalRequirement(
                                    id=req.get('id', ''),
                                    description=req.get('description', ''),
                                    constraint_type=req.get('constraint_type', 'unknown'),
                                    enforcement=req.get('enforcement', '')
                                ))
                        # Also check the item itself for requirement structure
                        elif 'id' in subcategory_data:
                            requirements.append(LegalRequirement(
                                id=subcategory_data.get('id', ''),
                                description=subcategory_data.get('description', ''),
                                constraint_type=subcategory_data.get('constraint_type', 'unknown'),
                                enforcement=subcategory_data.get('enforcement', '')
                            ))
        
        return requirements
    
    def generate_required_components(self) -> list:
        """
        Analyze legal primitives and detect required but unimplemented systems.
        
        This is the core LB-GSE function that:
        - Parses the legal contract
        - Identifies required capabilities
        - Checks against implemented components
        - Returns list of missing/needed components
        
        Returns:
            List of RequiredComponent objects representing needed software.
        """
        needed = []
        requirements = self._extract_requirements()
        
        for req in requirements:
            enforcement = req.enforcement
            
            # Get component mapping for this enforcement mechanism
            mapping = self.capability_mappings.get(enforcement, {})
            component_id = mapping.get('component', enforcement)
            
            # Check if component exists
            if not self.component_exists(component_id):
                needed.append(RequiredComponent(
                    id=req.id,
                    name=component_id,
                    description=req.description,
                    legal_source=f"Legal requirement: {req.id}",
                    constraint_type=req.constraint_type,
                    enforcement=enforcement,
                    priority=mapping.get('priority', 'medium'),
                    estimated_effort=mapping.get('estimated_effort', 'medium')
                ))
        
        return needed
    
    def analyze_contract(self) -> AnalysisResult:
        """
        Perform comprehensive analysis of the legal contract.
        
        Returns:
            AnalysisResult with compliance metrics and component lists.
        """
        requirements = self._extract_requirements()
        required_components = self.generate_required_components()
        
        # Identify implemented vs missing
        implemented = []
        missing = []
        
        for req in requirements:
            enforcement = req.enforcement
            mapping = self.capability_mappings.get(enforcement, {})
            component_id = mapping.get('component', enforcement)
            
            if self.component_exists(component_id):
                implemented.append(component_id)
            else:
                missing.append(component_id)
        
        # Calculate compliance score
        total = len(requirements)
        compliance_score = len(implemented) / total if total > 0 else 1.0
        
        return AnalysisResult(
            total_requirements=total,
            implemented_components=implemented,
            missing_components=missing,
            required_components=required_components,
            compliance_score=compliance_score
        )
    
    def prioritize_components(self, components: list) -> list:
        """
        Prioritize components for development based on legal constraints.
        
        Priority order:
        1. Critical (mandatory + security/compliance)
        2. High (mandatory)
        3. Medium (recommended)
        4. Low (permitted)
        
        Args:
            components: List of RequiredComponent objects.
            
        Returns:
            Sorted list with highest priority first.
        """
        priority_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        
        return sorted(
            components,
            key=lambda c: (
                priority_order.get(c.priority, 4),
                0 if c.constraint_type == 'mandatory' else 1
            )
        )
    
    def generate_development_roadmap(self) -> dict:
        """
        Generate a development roadmap based on legal constraints.
        
        Returns:
            Dictionary with prioritized phases and component assignments.
        """
        required = self.generate_required_components()
        prioritized = self.prioritize_components(required)
        
        roadmap = {
            "phase_1_critical": [],
            "phase_2_high": [],
            "phase_3_medium": [],
            "phase_4_low": []
        }
        
        for component in prioritized:
            if component.priority == 'critical':
                roadmap["phase_1_critical"].append(component)
            elif component.priority == 'high':
                roadmap["phase_2_high"].append(component)
            elif component.priority == 'medium':
                roadmap["phase_3_medium"].append(component)
            else:
                roadmap["phase_4_low"].append(component)
        
        return roadmap
    
    def validate_action(self, action_type: str, action_data: dict) -> tuple:
        """
        Validate whether an action is allowed by legal constraints.
        
        Args:
            action_type: Type of action (e.g., "withdraw_funds", "execute_proposal")
            action_data: Data about the proposed action.
            
        Returns:
            Tuple of (is_allowed, reasons)
        """
        is_allowed = True
        reasons = []
        
        # Check against liability boundaries
        liability = self.contract.get('legal_primitives', {}).get('liability_boundaries', {})
        if liability:
            # Check if action might breach liability shield
            if action_type in ['external_contract', 'personal_guarantee']:
                is_allowed = False
                reasons.append("Action may breach member liability shield")
        
        # Check against charitable constraints
        charitable = self.contract.get('legal_primitives', {}).get('charitable_constraints', {})
        if charitable and action_type == 'withdraw_funds':
            irrevocable = charitable.get('irrevocable_percentage', {})
            if irrevocable:
                pct = irrevocable.get('percentage', 0)
                if action_data.get('amount', 0) > action_data.get('available_balance', 0) * (1 - pct/100):
                    is_allowed = False
                    reasons.append(f"Cannot withdraw more than {100-pct}% of available funds (charitable reserve)")
        
        return (is_allowed, reasons)


def generate_required_components(legal_contract: dict) -> list:
    """
    Standalone function to analyze legal primitives and detect required systems.
    
    This is a convenience function that wraps the LegalFirewallGenerator class
    for simple use cases.
    
    Args:
        legal_contract: Dictionary containing legal primitives.
        
    Returns:
        List of component IDs that need to be implemented.
        
    Example:
        >>> contract = {"legal_primitives": {"fiduciary_duties": {...}}}
        >>> needed = generate_required_components(contract)
        >>> print(needed)
        ['risk_assessment_agent', 'governance_reporter']
    """
    generator = LegalFirewallGenerator()
    generator.contract = legal_contract
    
    # Extract capability mappings if present
    if 'capability_mappings' in legal_contract:
        generator.capability_mappings = legal_contract['capability_mappings']
    
    # Extract existing components if present
    if 'component_registry' in legal_contract:
        registry = legal_contract['component_registry']
        for component_id in registry.get('implemented', []):
            generator.component_registry[component_id] = {"status": "implemented"}
    
    required = generator.generate_required_components()
    return [comp.name for comp in required]


if __name__ == "__main__":
    # Example usage
    import sys
    
    # Default to the contracts.yaml in the same directory
    contract_path = os.path.join(os.path.dirname(__file__), "contracts.yaml")
    
    if len(sys.argv) > 1:
        contract_path = sys.argv[1]
    
    print("=" * 60)
    print("Legal-Firewall Generator - LB-GSE Methodology")
    print("Strategickhaos DAO LLC")
    print("=" * 60)
    
    try:
        generator = LegalFirewallGenerator()
        generator.load_contract(contract_path)
        
        print(f"\n📋 Loaded contract: {contract_path}")
        
        # Analyze contract
        analysis = generator.analyze_contract()
        
        print(f"\n📊 Analysis Results:")
        print(f"   Total Requirements: {analysis.total_requirements}")
        print(f"   Implemented Components: {len(analysis.implemented_components)}")
        print(f"   Missing Components: {len(analysis.missing_components)}")
        print(f"   Compliance Score: {analysis.compliance_score:.1%}")
        
        # Generate roadmap
        roadmap = generator.generate_development_roadmap()
        
        print(f"\n🗺️ Development Roadmap:")
        for phase, components in roadmap.items():
            if components:
                print(f"\n   {phase.upper().replace('_', ' ')}:")
                for comp in components:
                    print(f"      - {comp.name}")
                    print(f"        Description: {comp.description}")
                    print(f"        Constraint: {comp.constraint_type}")
                    print(f"        Effort: {comp.estimated_effort}")
        
        print("\n" + "=" * 60)
        print("✅ Legal-Firewall analysis complete")
        print("=" * 60)
        
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"❌ YAML parsing error: {e}")
        sys.exit(1)

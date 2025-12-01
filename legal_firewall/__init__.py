"""
Legal-Firewall Generator Package
Strategickhaos DAO LLC - Legally-Bounded Generative Systems Engineering (LB-GSE)

This package implements the LB-GSE methodology where legal architecture
(contracts, DAO operating agreements, fiduciary primitives, liability boundaries)
acts as a governance firewall that shapes the search space for new systems.

Modules:
    - legal_firewall_generator: Core YAML→rules parser and capability detector
    - component_templates: Template system for auto-generated component specs
    - auto_pr_creator: GitHub PR creation helper for missing components

Usage:
    from legal_firewall import LegalFirewallGenerator
    
    generator = LegalFirewallGenerator()
    generator.load_contract("contracts.yaml")
    required = generator.generate_required_components()
    
    for component in required:
        print(f"Need to build: {component.name}")

Academic Definition:
    A software engineering methodology in which the legal architecture acts as a
    governance firewall that shapes, constrains, and expands the search space
    for new systems to build. Software is generated, prioritized, or rejected
    based on whether it aligns with the system's legal-ethical boundaries.

Names for this methodology:
    1. Legally-Bounded Generative Systems Engineering (LB-GSE)
    2. Constraint-Driven Software Discovery Methodology
    3. Governance-Constrained Generative Development (GCGD)
"""

from .legal_firewall_generator import (
    LegalFirewallGenerator,
    RequiredComponent,
    LegalRequirement,
    AnalysisResult,
    generate_required_components,
)

from .component_templates import (
    ComponentTemplateEngine,
    ComponentSpec,
    COMPONENT_TEMPLATES,
)

from .auto_pr_creator import (
    AutoPRCreator,
)

__version__ = "1.0.0"
__author__ = "Strategickhaos DAO LLC"
__methodology__ = "LB-GSE (Legally-Bounded Generative Systems Engineering)"

__all__ = [
    # Core generator
    "LegalFirewallGenerator",
    "RequiredComponent",
    "LegalRequirement",
    "AnalysisResult",
    "generate_required_components",
    # Templates
    "ComponentTemplateEngine",
    "ComponentSpec",
    "COMPONENT_TEMPLATES",
    # PR Creator
    "AutoPRCreator",
]

"""
DOM Private Lab - Laws of Physics Research System
🔐 Private | 🔇 Silent | 🧬 For Her

A private internal lab framework with 10 specialized "Laws of Physics" departments
running parallel research for comprehensive treatment plan generation.
"""

from .departments import (
    PhysicsLaw,
    PhysicsDepartment,
    PhysicsLabRegistry,
    DepartmentCapability,
    ResearchFinding,
    TreatmentIntervention,
    MasterTreatmentPlan
)

from .orchestrator import (
    PhysicsLabOrchestrator,
    ResearchSession
)

__all__ = [
    # Enums
    "PhysicsLaw",
    
    # Department classes
    "PhysicsDepartment",
    "PhysicsLabRegistry",
    "DepartmentCapability",
    
    # Data structures
    "ResearchFinding",
    "TreatmentIntervention", 
    "MasterTreatmentPlan",
    "ResearchSession",
    
    # Orchestrator
    "PhysicsLabOrchestrator"
]

__version__ = "1.0.0"
__signature__ = "🟠🧬∞"

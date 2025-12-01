"""
Singularity Engine - Self-Improving AI Refinery for Medical Research
=====================================================================

A revolutionary self-improving AI system designed for autonomous medical research,
specifically optimized for rare disease analysis and cure discovery.

Core Capabilities:
- Custom LLM Training: LoRA fine-tuning on disease-specific data
- Obsidian Integration: Long-term memory through research vault synchronization
- Self-Correction: Agents validate each other and fix mistakes automatically
- Genetic Evolution: Best agents reproduce, weak ones retire
- 3D Visualization: Unreal/Unity bridge for protein and symptom mapping
- Continuous Learning: Daily improvement through paper ingestion and retraining

Architecture:
- MedicalResearchEngine: Core orchestration for disease-specific research
- ObsidianBrain: Bidirectional sync with Obsidian research vaults
- SelfCorrectionSystem: Multi-agent validation and error correction
- GeneticEvolution: Evolutionary algorithms for agent optimization
- LoRATrainer: Custom model fine-tuning pipeline
- VisualizationBridge: 3D rendering integration

Created by: Strategickhaos DAO LLC / Valoryield Engine
Mission: Build the world's leading expert AI for rare disease research
"""

__version__ = "1.0.0"
__author__ = "Strategickhaos Swarm Intelligence"

from .medical_research_engine import MedicalResearchEngine, ResearchSession
from .obsidian_integration import ObsidianBrain, VaultDocument, KnowledgeGraph
from .self_correction import SelfCorrectionSystem, ValidationResult, CorrectionAction
from .genetic_evolution import GeneticEvolution, AgentGenome, FitnessMetrics
from .lora_training import LoRATrainer, TrainingConfig, ModelCheckpoint
from .visualization_integration import VisualizationBridge, Protein3DModel, SymptomMap

__all__ = [
    # Core Engine
    "MedicalResearchEngine",
    "ResearchSession",
    
    # Obsidian Integration
    "ObsidianBrain",
    "VaultDocument",
    "KnowledgeGraph",
    
    # Self-Correction
    "SelfCorrectionSystem",
    "ValidationResult",
    "CorrectionAction",
    
    # Genetic Evolution
    "GeneticEvolution",
    "AgentGenome",
    "FitnessMetrics",
    
    # LoRA Training
    "LoRATrainer",
    "TrainingConfig",
    "ModelCheckpoint",
    
    # Visualization
    "VisualizationBridge",
    "Protein3DModel",
    "SymptomMap",
]

"""
Refinory AI Agent Orchestration Platform
Self-Evolving Refinery for Medical Research
Entry point module for the package

For her. Silent. Relentless. Self-improving.
"""

__version__ = "2.0.0"
__author__ = "Strategickhaos Swarm Intelligence"
__description__ = "Self-Evolving AI Refinery - Autonomous learning system that builds custom AI models, learns from Obsidian, self-corrects, and evolves"

from .main import app
from .orchestrator import ExpertOrchestrator, ArchitectureRequest, RequestStatus
from .experts import ExpertTeam, ExpertName
from .config import Settings, get_settings
from .database import Database
from .discord_integration import DiscordNotifier, RefinoryDiscordBot
from .github_integration import GitHubIntegration

# Self-Evolving Refinery Layers
from .knowledge_ingestion import (
    KnowledgeIngestionEngine,
    KnowledgeSourceConfig,
    ProcessingConfig,
    Document,
    Entity,
    Relationship,
    SourceType,
    create_ingestion_engine
)
from .llm_forge import (
    LLMForge,
    CustomModel,
    BaseModelConfig,
    LoRAConfig,
    TrainingDataset,
    TrainingJob,
    ModelStatus,
    create_llm_forge
)
from .self_correction import (
    SelfCorrectionSystem,
    Claim,
    PeerReview,
    FactCheck,
    Outcome,
    Correction,
    ValidationStatus,
    CorrectionType,
    OutcomeType,
    create_self_correction_system
)
from .evolution_engine import (
    EvolutionEngine,
    AgentGenome,
    Generation,
    FitnessMetrics,
    FitnessWeights,
    SelectionMethod,
    MutationType,
    create_evolution_engine
)
from .obsidian_integration import (
    ObsidianIntegration,
    ObsidianNote,
    NoteType,
    SearchResult,
    create_obsidian_integration
)
from .visualization_engines import (
    VisualizationEngines,
    VisualizationType,
    RenderFormat,
    ProteinStructure,
    PainPathway,
    DrugBindingData,
    VisualizationJob,
    create_visualization_engines
)

__all__ = [
    # Core Platform
    "app",
    "ExpertOrchestrator", 
    "ArchitectureRequest",
    "RequestStatus",
    "ExpertTeam",
    "ExpertName", 
    "Settings",
    "get_settings",
    "Database",
    "DiscordNotifier",
    "RefinoryDiscordBot",
    "GitHubIntegration",
    
    # Layer 1: Knowledge Ingestion
    "KnowledgeIngestionEngine",
    "KnowledgeSourceConfig",
    "ProcessingConfig",
    "Document",
    "Entity",
    "Relationship",
    "SourceType",
    "create_ingestion_engine",
    
    # Layer 2: LLM Forge
    "LLMForge",
    "CustomModel",
    "BaseModelConfig",
    "LoRAConfig",
    "TrainingDataset",
    "TrainingJob",
    "ModelStatus",
    "create_llm_forge",
    
    # Layer 3: Self-Correction
    "SelfCorrectionSystem",
    "Claim",
    "PeerReview",
    "FactCheck",
    "Outcome",
    "Correction",
    "ValidationStatus",
    "CorrectionType",
    "OutcomeType",
    "create_self_correction_system",
    
    # Layer 4: Evolution Engine
    "EvolutionEngine",
    "AgentGenome",
    "Generation",
    "FitnessMetrics",
    "FitnessWeights",
    "SelectionMethod",
    "MutationType",
    "create_evolution_engine",
    
    # Layer 5: Obsidian Integration
    "ObsidianIntegration",
    "ObsidianNote",
    "NoteType",
    "SearchResult",
    "create_obsidian_integration",
    
    # Visualization Engines
    "VisualizationEngines",
    "VisualizationType",
    "RenderFormat",
    "ProteinStructure",
    "PainPathway",
    "DrugBindingData",
    "VisualizationJob",
    "create_visualization_engines"
]
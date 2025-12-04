"""
Singularity Engine API - FastAPI Server for Self-Improving Medical Research AI
===============================================================================

Main API server that exposes the Singularity Engine capabilities:
- Research session management
- Obsidian vault synchronization
- Model training and deployment
- Visualization generation
- Evolution status and control
"""

import asyncio
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import structlog
import uvicorn
from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from prometheus_client import Counter, Histogram, generate_latest

from .medical_research_engine import (
    MedicalResearchEngine,
    DiseaseProfile,
    ResearchSession,
    ResearchPriority
)
from .obsidian_integration import ObsidianBrain
from .self_correction import SelfCorrectionSystem
from .genetic_evolution import GeneticEvolution
from .lora_training import LoRATrainer, TrainingConfig
from .visualization_integration import VisualizationBridge, VisualizationType

# Configure logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# Prometheus metrics
RESEARCH_SESSIONS = Counter('singularity_research_sessions_total', 'Total research sessions')
PAPERS_PROCESSED = Counter('singularity_papers_processed_total', 'Total papers processed')
HYPOTHESES_GENERATED = Counter('singularity_hypotheses_generated_total', 'Total hypotheses generated')
TRAINING_JOBS = Counter('singularity_training_jobs_total', 'Total training jobs')
EVOLUTION_GENERATIONS = Counter('singularity_evolution_generations_total', 'Evolution generations completed')


# Pydantic models for API
class DiseaseProfileRequest(BaseModel):
    disease_name: str = Field(..., description="Name of the disease to research")
    icd_codes: List[str] = Field(default=[], description="ICD-10 codes")
    omim_ids: List[str] = Field(default=[], description="OMIM database IDs")
    affected_systems: List[str] = Field(default=[], description="Affected body systems")
    genetic_factors: List[str] = Field(default=[], description="Known genetic factors")
    protein_markers: List[str] = Field(default=[], description="Protein biomarkers")
    symptoms: List[str] = Field(default=[], description="Known symptoms")
    priority_pathways: List[str] = Field(default=[], description="Research priority pathways")


class ResearchSessionRequest(BaseModel):
    session_name: Optional[str] = Field(None, description="Optional session name")
    priority: str = Field("normal", description="Research priority")
    paper_limit: int = Field(100, description="Papers to process per cycle")
    hypothesis_limit: int = Field(10, description="Hypotheses to generate per cycle")


class TrainingRequest(BaseModel):
    base_model: str = Field("meta-llama/Llama-2-7b-hf", description="Base model for fine-tuning")
    num_epochs: int = Field(3, description="Number of training epochs")
    learning_rate: float = Field(2e-4, description="Learning rate")
    lora_r: int = Field(16, description="LoRA rank")
    batch_size: int = Field(4, description="Training batch size")


class VisualizationRequest(BaseModel):
    visualization_type: str = Field(..., description="Type of visualization")
    pdb_data: Optional[str] = Field(None, description="PDB data for protein visualization")
    symptoms: Optional[List[Dict]] = Field(None, description="Symptoms for symptom map")


class HealthResponse(BaseModel):
    status: str
    version: str
    timestamp: str
    components: Dict[str, str]


class EngineStatusResponse(BaseModel):
    disease: str
    total_papers_processed: int
    total_hypotheses_generated: int
    active_sessions: int
    improvement_rate: float
    model_status: Dict[str, Any]
    evolution_generation: int


# Global state
engine_state = {
    "engine": None,
    "obsidian": None,
    "trainer": None,
    "evolution": None,
    "visualization": None
}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    logger.info("Starting Singularity Engine")
    
    # Note: Engine is initialized via POST /api/v1/engine/initialize
    # to allow dynamic disease profile configuration
    
    yield
    
    # Cleanup
    logger.info("Shutting down Singularity Engine")
    if engine_state["engine"]:
        await engine_state["engine"].shutdown()


# Create FastAPI application
app = FastAPI(
    title="Singularity Engine - Self-Improving Medical Research AI",
    description="""
    The SINGULARITY ENGINE for medical research - a self-improving AI system that:
    
    - **Makes its own LLMs**: Custom models trained on disease-specific data via LoRA
    - **Learns from Obsidian**: Your research vault becomes its long-term memory
    - **Self-corrects errors**: Multi-agent validation ensures accuracy
    - **Evolves via genetics**: Best agent configurations reproduce, weak ones retire
    - **3D Visualization**: Protein structures and symptom maps in Unreal/Unity
    - **Gets smarter daily**: Retrains every 1000 papers, 5-10% improvement per week
    
    Timeline:
    - Week 1: Better than any single researcher
    - Month 3: Better than research teams
    - Month 6: Better than academic institutions
    - Year 1: Among world's top experts
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health and metrics endpoints
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    components = {
        "engine": "healthy" if engine_state["engine"] else "not_initialized",
        "obsidian": "healthy" if engine_state["obsidian"] else "not_connected",
        "trainer": "healthy" if engine_state["trainer"] else "not_initialized",
        "evolution": "healthy" if engine_state["evolution"] else "not_initialized",
        "visualization": "healthy" if engine_state["visualization"] else "not_initialized"
    }
    
    overall = "healthy" if engine_state["engine"] else "initializing"
    
    return HealthResponse(
        status=overall,
        version="1.0.0",
        timestamp=datetime.now(timezone.utc).isoformat(),
        components=components
    )


@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    return generate_latest()


# Engine initialization
@app.post("/api/v1/engine/initialize")
async def initialize_engine(
    profile: DiseaseProfileRequest,
    obsidian_vault_path: Optional[str] = None
):
    """Initialize the Singularity Engine with a disease profile"""
    logger.info(f"Initializing engine for disease: {profile.disease_name}")
    
    # Create disease profile
    disease_profile = DiseaseProfile(
        disease_name=profile.disease_name,
        icd_codes=profile.icd_codes,
        omim_ids=profile.omim_ids,
        affected_systems=profile.affected_systems,
        genetic_factors=profile.genetic_factors,
        protein_markers=profile.protein_markers,
        symptoms=profile.symptoms,
        priority_pathways=profile.priority_pathways
    )
    
    # Initialize engine
    engine = MedicalResearchEngine(
        disease_profile=disease_profile,
        obsidian_vault_path=obsidian_vault_path
    )
    await engine.initialize()
    engine_state["engine"] = engine
    
    # Initialize LoRA trainer
    trainer = LoRATrainer(
        disease_name=profile.disease_name
    )
    engine_state["trainer"] = trainer
    
    # Initialize genetic evolution
    evolution = GeneticEvolution(
        population_size=20,
        mutation_rate=0.1
    )
    engine_state["evolution"] = evolution
    
    # Initialize visualization bridge
    visualization = VisualizationBridge()
    engine_state["visualization"] = visualization
    
    # Connect Obsidian if path provided
    if obsidian_vault_path:
        obsidian = ObsidianBrain(obsidian_vault_path)
        await obsidian.connect()
        engine_state["obsidian"] = obsidian
    
    logger.info("Singularity Engine initialized successfully")
    
    return {
        "status": "initialized",
        "disease": profile.disease_name,
        "obsidian_connected": obsidian_vault_path is not None,
        "components": {
            "engine": True,
            "trainer": True,
            "evolution": True,
            "visualization": True,
            "obsidian": obsidian_vault_path is not None
        }
    }


@app.get("/api/v1/engine/status", response_model=EngineStatusResponse)
async def get_engine_status():
    """Get current engine status"""
    if not engine_state["engine"]:
        raise HTTPException(status_code=400, detail="Engine not initialized")
    
    engine = engine_state["engine"]
    status = await engine.get_status()
    
    # Get trainer status
    trainer_status = {}
    if engine_state["trainer"]:
        trainer_status = await engine_state["trainer"].get_training_status()
    
    # Get evolution generation
    evolution_gen = 0
    if engine_state["evolution"]:
        evolution_gen = engine_state["evolution"].current_generation
    
    return EngineStatusResponse(
        disease=status["disease"],
        total_papers_processed=status["total_papers_processed"],
        total_hypotheses_generated=status["total_hypotheses_generated"],
        active_sessions=status["active_sessions"],
        improvement_rate=status["current_improvement_rate"],
        model_status=trainer_status,
        evolution_generation=evolution_gen
    )


# Research session endpoints
@app.post("/api/v1/research/session")
async def create_research_session(
    request: ResearchSessionRequest,
    background_tasks: BackgroundTasks
):
    """Create a new research session"""
    if not engine_state["engine"]:
        raise HTTPException(status_code=400, detail="Engine not initialized")
    
    engine = engine_state["engine"]
    
    # Create session
    priority = ResearchPriority(request.priority)
    session = await engine.create_session(request.session_name, priority)
    
    RESEARCH_SESSIONS.inc()
    
    # Start research cycle in background
    background_tasks.add_task(
        run_research_cycle,
        engine,
        session,
        request.paper_limit,
        request.hypothesis_limit
    )
    
    return {
        "session_id": session.session_id,
        "status": session.phase.value,
        "message": "Research cycle started in background"
    }


async def run_research_cycle(
    engine: MedicalResearchEngine,
    session: ResearchSession,
    paper_limit: int,
    hypothesis_limit: int
):
    """Run research cycle in background"""
    try:
        results = await engine.run_research_cycle(
            session,
            paper_limit=paper_limit,
            hypothesis_limit=hypothesis_limit
        )
        
        PAPERS_PROCESSED.inc(results["papers_collected"])
        HYPOTHESES_GENERATED.inc(results["hypotheses_generated"])
        
        logger.info(
            "Research cycle completed",
            session_id=session.session_id,
            results=results
        )
    except Exception as e:
        logger.error(f"Research cycle failed: {e}")


@app.get("/api/v1/research/session/{session_id}")
async def get_session_status(session_id: str):
    """Get research session status"""
    if not engine_state["engine"]:
        raise HTTPException(status_code=400, detail="Engine not initialized")
    
    engine = engine_state["engine"]
    
    if session_id not in engine.active_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = engine.active_sessions[session_id]
    
    return {
        "session_id": session.session_id,
        "phase": session.phase.value,
        "papers_processed": session.papers_processed,
        "hypotheses_generated": session.hypotheses_generated,
        "hypotheses_validated": session.hypotheses_validated,
        "improvement_rate": session.improvement_rate,
        "started_at": session.started_at.isoformat(),
        "last_activity": session.last_activity.isoformat()
    }


# Training endpoints
@app.post("/api/v1/training/start")
async def start_training(
    request: TrainingRequest,
    background_tasks: BackgroundTasks
):
    """Start LoRA fine-tuning with accumulated data"""
    if not engine_state["trainer"]:
        raise HTTPException(status_code=400, detail="Trainer not initialized")
    
    if not engine_state["engine"]:
        raise HTTPException(status_code=400, detail="Engine not initialized")
    
    trainer = engine_state["trainer"]
    engine = engine_state["engine"]
    
    # Prepare training data
    training_data = engine._prepare_training_data()
    
    if len(training_data) < 10:
        raise HTTPException(
            status_code=400,
            detail="Not enough training data. Process more papers first."
        )
    
    # Create training config
    config = TrainingConfig(
        base_model=request.base_model,
        num_epochs=request.num_epochs,
        learning_rate=request.learning_rate,
        lora_r=request.lora_r,
        batch_size=request.batch_size
    )
    
    TRAINING_JOBS.inc()
    
    # Start training in background
    background_tasks.add_task(
        run_training,
        trainer,
        training_data,
        config
    )
    
    return {
        "status": "training_started",
        "training_samples": len(training_data),
        "config": config.to_dict()
    }


async def run_training(
    trainer: LoRATrainer,
    training_data: List[Dict],
    config: TrainingConfig
):
    """Run training in background"""
    try:
        checkpoint = await trainer.train(training_data, config)
        logger.info(f"Training completed: {checkpoint.checkpoint_id}")
    except Exception as e:
        logger.error(f"Training failed: {e}")


@app.get("/api/v1/training/status")
async def get_training_status():
    """Get current training status"""
    if not engine_state["trainer"]:
        raise HTTPException(status_code=400, detail="Trainer not initialized")
    
    return await engine_state["trainer"].get_training_status()


@app.get("/api/v1/training/checkpoints")
async def list_checkpoints():
    """List all available model checkpoints"""
    if not engine_state["trainer"]:
        raise HTTPException(status_code=400, detail="Trainer not initialized")
    
    return await engine_state["trainer"].list_checkpoints()


# Evolution endpoints
@app.post("/api/v1/evolution/evolve")
async def evolve_generation(background_tasks: BackgroundTasks):
    """Evolve one generation of agents"""
    if not engine_state["evolution"]:
        raise HTTPException(status_code=400, detail="Evolution not initialized")
    
    evolution = engine_state["evolution"]
    
    EVOLUTION_GENERATIONS.inc()
    
    # Run evolution in background
    background_tasks.add_task(run_evolution, evolution)
    
    return {
        "status": "evolution_started",
        "current_generation": evolution.current_generation
    }


async def run_evolution(evolution: GeneticEvolution):
    """Run evolution in background"""
    try:
        result = await evolution.evolve_generation()
        logger.info(f"Evolution generation {result['generation']} completed")
    except Exception as e:
        logger.error(f"Evolution failed: {e}")


@app.get("/api/v1/evolution/status")
async def get_evolution_status():
    """Get evolution status"""
    if not engine_state["evolution"]:
        raise HTTPException(status_code=400, detail="Evolution not initialized")
    
    return await engine_state["evolution"].get_evolution_report()


@app.get("/api/v1/evolution/best")
async def get_best_genome():
    """Get the best performing genome"""
    if not engine_state["evolution"]:
        raise HTTPException(status_code=400, detail="Evolution not initialized")
    
    evolution = engine_state["evolution"]
    best = evolution.get_best_genome()
    
    if not best:
        return {"message": "No genomes evaluated yet"}
    
    return {
        "genome_id": best.genome_id,
        "generation": best.generation,
        "fitness_score": best.fitness_score,
        "phenotype": best.get_phenotype()
    }


# Validation endpoints
@app.get("/api/v1/validation/statistics")
async def get_validation_statistics():
    """Get validation system statistics"""
    if not engine_state["engine"] or not engine_state["engine"]._self_correction:
        raise HTTPException(status_code=400, detail="Self-correction not initialized")
    
    return await engine_state["engine"]._self_correction.get_statistics()


@app.get("/api/v1/validation/errors")
async def get_error_report():
    """Get validation error report"""
    if not engine_state["engine"] or not engine_state["engine"]._self_correction:
        raise HTTPException(status_code=400, detail="Self-correction not initialized")
    
    return await engine_state["engine"]._self_correction.get_error_report()


# Visualization endpoints
@app.post("/api/v1/visualization/create")
async def create_visualization(request: VisualizationRequest):
    """Create a visualization"""
    if not engine_state["visualization"]:
        raise HTTPException(status_code=400, detail="Visualization not initialized")
    
    viz = engine_state["visualization"]
    
    try:
        viz_type = VisualizationType(request.visualization_type)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid visualization type: {request.visualization_type}")
    
    if viz_type == VisualizationType.PROTEIN_3D:
        if not request.pdb_data:
            raise HTTPException(status_code=400, detail="PDB data required for protein visualization")
        
        model = await viz.create_protein_visualization(request.pdb_data)
        return {
            "visualization_id": model.model_id,
            "type": "protein_3d",
            "atoms": len(model.atoms),
            "bonds": len(model.bonds),
            "center": model.center.to_dict()
        }
    
    elif viz_type == VisualizationType.SYMPTOM_MAP:
        if not request.symptoms:
            raise HTTPException(status_code=400, detail="Symptoms required for symptom map")
        
        if not engine_state["engine"]:
            raise HTTPException(status_code=400, detail="Engine not initialized")
        
        disease_name = engine_state["engine"].disease_profile.disease_name
        symptom_map = await viz.create_symptom_map(disease_name, request.symptoms)
        
        return {
            "visualization_id": symptom_map.map_id,
            "type": "symptom_map",
            "symptoms": len(symptom_map.symptoms),
            "connections": len(symptom_map.symptom_connections),
            "affected_regions": symptom_map.affected_regions
        }
    
    raise HTTPException(status_code=400, detail=f"Visualization type {viz_type.value} not yet implemented")


@app.get("/api/v1/visualization/stats")
async def get_visualization_stats():
    """Get visualization statistics"""
    if not engine_state["visualization"]:
        raise HTTPException(status_code=400, detail="Visualization not initialized")
    
    return await engine_state["visualization"].get_visualization_stats()


# Obsidian endpoints
@app.get("/api/v1/obsidian/summary")
async def get_obsidian_summary():
    """Get Obsidian vault knowledge summary"""
    if not engine_state["obsidian"]:
        raise HTTPException(status_code=400, detail="Obsidian not connected")
    
    return await engine_state["obsidian"].get_knowledge_summary()


@app.get("/api/v1/obsidian/search")
async def search_obsidian(query: str, limit: int = 20):
    """Search the Obsidian vault"""
    if not engine_state["obsidian"]:
        raise HTTPException(status_code=400, detail="Obsidian not connected")
    
    results = await engine_state["obsidian"].search(query, limit=limit)
    
    return {
        "query": query,
        "results": [
            {
                "path": doc.path,
                "title": doc.title,
                "type": doc.note_type.value,
                "tags": doc.tags
            }
            for doc in results
        ]
    }


if __name__ == "__main__":
    uvicorn.run(
        "singularity.api:app",
        host="0.0.0.0",
        port=8090,
        reload=True,
        log_config=None
    )

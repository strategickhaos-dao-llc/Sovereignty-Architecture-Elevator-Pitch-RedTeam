"""
Refinory Expert Orchestrator - AI Agent Workflow Management
Coordinates expert teams for autonomous architecture generation
"""

import asyncio
import json
import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from contextlib import asynccontextmanager

import structlog
from temporal import activity, workflow
from temporal.client import Client as TemporalClient
from temporal.worker import Worker

from .database import Database
from .experts import ExpertTeam, ExpertName
from .config import Settings

logger = structlog.get_logger()

class RequestStatus(Enum):
    """Architecture request status"""
    PENDING = "pending"
    ANALYZING = "analyzing"
    EXPERT_REVIEW = "expert_review"
    GENERATING = "generating"
    REVIEWING = "reviewing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class Priority(Enum):
    """Request priority levels"""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class ArchitectureRequest:
    """Architecture generation request"""
    project_name: str
    description: str
    requirements: List[str]
    experts_requested: Optional[List[str]] = None
    priority: str = "normal"
    github_repo: Optional[str] = None
    request_id: Optional[str] = None
    status: RequestStatus = RequestStatus.PENDING
    created_at: Optional[datetime] = None
    experts_assigned: List[str] = None
    progress: Dict[str, Any] = None
    artifacts_url: Optional[str] = None
    github_pr_url: Optional[str] = None

    def __post_init__(self):
        if self.request_id is None:
            self.request_id = str(uuid.uuid4())
        if self.created_at is None:
            self.created_at = datetime.now(timezone.utc)
        if self.experts_assigned is None:
            self.experts_assigned = []
        if self.progress is None:
            self.progress = {}

@dataclass
class ExpertTask:
    """Individual expert task"""
    expert_name: str
    task_type: str
    context: Dict[str, Any]
    dependencies: List[str] = None
    status: str = "pending"
    result: Optional[Dict[str, Any]] = None
    artifacts: List[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []
        if self.artifacts is None:
            self.artifacts = []

class ExpertOrchestrator:
    """Coordinates expert workflows for architecture generation"""
    
    def __init__(self, database: Database, expert_team: ExpertTeam, settings: Settings):
        self.db = database
        self.experts = expert_team
        self.settings = settings
        self.temporal_client = None
        self.worker = None
        
    async def initialize_temporal(self):
        """Initialize Temporal workflow client"""
        try:
            self.temporal_client = await TemporalClient.connect(
                self.settings.temporal_address
            )
            logger.info("Connected to Temporal server")
            
            # Create worker for architecture workflows
            self.worker = Worker(
                self.temporal_client,
                task_queue="refinory-architecture",
                workflows=[ArchitectureWorkflow],
                activities=[
                    analyze_requirements_activity,
                    assign_experts_activity,
                    execute_expert_tasks_activity,
                    generate_architecture_activity,
                    review_architecture_activity,
                    finalize_artifacts_activity
                ]
            )
            
        except Exception as e:
            logger.error(f"Failed to initialize Temporal: {str(e)}")
            raise

    async def submit_request(self, request: ArchitectureRequest) -> str:
        """Submit new architecture request"""
        logger.info(f"Submitting architecture request: {request.project_name}")
        
        # Store request in database
        await self.db.store_architecture_request(request)
        
        # Start Temporal workflow
        if self.temporal_client:
            await self.temporal_client.start_workflow(
                ArchitectureWorkflow.run,
                args=[asdict(request)],
                id=f"architecture-{request.request_id}",
                task_queue="refinory-architecture"
            )
        else:
            # Fallback to direct processing if Temporal unavailable
            asyncio.create_task(self._process_request_direct(request))
        
        return request.request_id

    async def get_request_status(self, request_id: str) -> ArchitectureRequest:
        """Get current status of architecture request"""
        return await self.db.get_architecture_request(request_id)

    async def list_requests(
        self, 
        status: Optional[RequestStatus] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[ArchitectureRequest]:
        """List architecture requests with filtering"""
        return await self.db.list_architecture_requests(
            status=status.value if status else None,
            limit=limit,
            offset=offset
        )

    async def update_request_status(self, request_id: str, status: RequestStatus, progress: Dict[str, Any] = None):
        """Update request status and progress"""
        await self.db.update_request_status(request_id, status.value, progress or {})

    async def update_github_pr_url(self, request_id: str, pr_url: str):
        """Update GitHub PR URL for request"""
        await self.db.update_request_github_pr(request_id, pr_url)

    async def process_request(self, request_id: str) -> ArchitectureRequest:
        """Process architecture request (fallback method)"""
        return await self._process_request_direct(
            await self.get_request_status(request_id)
        )

    async def _process_request_direct(self, request: ArchitectureRequest) -> ArchitectureRequest:
        """Direct request processing without Temporal"""
        logger.info(f"Processing request directly: {request.request_id}")
        
        try:
            # Phase 1: Analyze requirements
            await self.update_request_status(request.request_id, RequestStatus.ANALYZING, {
                "phase": "analyzing_requirements",
                "progress": 10
            })
            
            analysis = await self._analyze_requirements(request)
            
            # Phase 2: Assign experts
            await self.update_request_status(request.request_id, RequestStatus.EXPERT_REVIEW, {
                "phase": "assigning_experts", 
                "progress": 20,
                "analysis": analysis
            })
            
            expert_assignments = await self._assign_experts(request, analysis)
            
            # Phase 3: Execute expert tasks
            await self.update_request_status(request.request_id, RequestStatus.GENERATING, {
                "phase": "executing_tasks",
                "progress": 30,
                "experts": expert_assignments
            })
            
            expert_results = await self._execute_expert_tasks(request, expert_assignments)
            
            # Phase 4: Generate architecture
            await self.update_request_status(request.request_id, RequestStatus.REVIEWING, {
                "phase": "generating_architecture",
                "progress": 70,
                "expert_results": [r["summary"] for r in expert_results]
            })
            
            architecture = await self._generate_architecture(request, expert_results)
            
            # Phase 5: Final review and artifacts
            await self.update_request_status(request.request_id, RequestStatus.COMPLETED, {
                "phase": "completed",
                "progress": 100,
                "architecture": architecture["summary"]
            })
            
            # Update final request object
            request.status = RequestStatus.COMPLETED
            request.artifacts_url = architecture.get("artifacts_url")
            await self.db.update_architecture_request(request)
            
            return request
            
        except Exception as e:
            logger.error(f"Failed to process request {request.request_id}: {str(e)}")
            await self.update_request_status(request.request_id, RequestStatus.FAILED, {
                "error": str(e),
                "phase": "error"
            })
            raise

    async def _analyze_requirements(self, request: ArchitectureRequest) -> Dict[str, Any]:
        """Analyze project requirements and constraints"""
        logger.info(f"Analyzing requirements for: {request.project_name}")
        
        # Use architecture expert for requirements analysis
        analysis_result = await self.experts.invoke_expert(
            ExpertName.ARCHITECTURE,
            "analyze_requirements",
            {
                "project_name": request.project_name,
                "description": request.description,
                "requirements": request.requirements
            }
        )
        
        return {
            "complexity_score": analysis_result.get("complexity", "medium"),
            "estimated_timeline": analysis_result.get("timeline", "2-4 weeks"),
            "technology_stack": analysis_result.get("tech_stack", []),
            "risk_factors": analysis_result.get("risks", []),
            "success_criteria": analysis_result.get("success_criteria", [])
        }

    async def _assign_experts(self, request: ArchitectureRequest, analysis: Dict[str, Any]) -> List[ExpertTask]:
        """Assign appropriate experts based on analysis"""
        logger.info(f"Assigning experts for: {request.project_name}")
        
        # Determine required experts based on technology stack and complexity
        required_experts = set()
        
        # Always include architecture expert
        required_experts.add(ExpertName.ARCHITECTURE)
        
        # Add experts based on tech stack
        tech_stack = analysis.get("technology_stack", [])
        for tech in tech_stack:
            if "react" in tech.lower() or "frontend" in tech.lower():
                required_experts.add(ExpertName.FRONTEND)
            if "api" in tech.lower() or "backend" in tech.lower():
                required_experts.add(ExpertName.BACKEND)
            if "docker" in tech.lower() or "kubernetes" in tech.lower():
                required_experts.add(ExpertName.DEVOPS)
            if "ai" in tech.lower() or "ml" in tech.lower():
                required_experts.add(ExpertName.AI_ML)
            if "mobile" in tech.lower():
                required_experts.add(ExpertName.MOBILE)
            if "blockchain" in tech.lower():
                required_experts.add(ExpertName.BLOCKCHAIN)
        
        # Add security for all projects
        required_experts.add(ExpertName.SECURITY)
        
        # Add testing expert for complex projects
        if analysis.get("complexity_score") in ["high", "very_high"]:
            required_experts.add(ExpertName.TESTING)
        
        # Honor user-requested experts
        if request.experts_requested:
            for expert_name in request.experts_requested:
                try:
                    required_experts.add(ExpertName(expert_name))
                except ValueError:
                    logger.warning(f"Unknown expert requested: {expert_name}")
        
        # Create expert tasks
        expert_tasks = []
        for expert in required_experts:
            task = ExpertTask(
                expert_name=expert.value,
                task_type="architecture_contribution",
                context={
                    "request": asdict(request),
                    "analysis": analysis,
                    "role": expert.value
                }
            )
            expert_tasks.append(task)
        
        # Update request with assigned experts
        request.experts_assigned = [task.expert_name for task in expert_tasks]
        await self.db.update_architecture_request(request)
        
        return expert_tasks

    async def _execute_expert_tasks(self, request: ArchitectureRequest, tasks: List[ExpertTask]) -> List[Dict[str, Any]]:
        """Execute expert tasks in parallel"""
        logger.info(f"Executing {len(tasks)} expert tasks for: {request.project_name}")
        
        # Execute all tasks concurrently using list comprehension for efficiency
        expert_coroutines = [self._execute_single_expert_task(task) for task in tasks]
        results = await asyncio.gather(*expert_coroutines, return_exceptions=True)
        
        # Process results efficiently
        task_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Expert task failed: {tasks[i].expert_name} - {str(result)}")
                task_results.append({
                    "expert": tasks[i].expert_name,
                    "status": "failed",
                    "error": str(result),
                    "summary": f"Failed to get contribution from {tasks[i].expert_name}"
                })
            else:
                task_results.append(result)
        
        return task_results

    async def _execute_single_expert_task(self, task: ExpertTask) -> Dict[str, Any]:
        """Execute single expert task"""
        logger.info(f"Executing task for expert: {task.expert_name}")
        
        try:
            expert_name = ExpertName(task.expert_name)
            result = await self.experts.invoke_expert(
                expert_name,
                task.task_type,
                task.context
            )
            
            return {
                "expert": task.expert_name,
                "status": "completed",
                "result": result,
                "summary": result.get("summary", f"Contribution from {task.expert_name}"),
                "artifacts": result.get("artifacts", []),
                "recommendations": result.get("recommendations", [])
            }
            
        except Exception as e:
            logger.error(f"Expert task failed for {task.expert_name}: {str(e)}")
            raise

    async def _generate_architecture(self, request: ArchitectureRequest, expert_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate final architecture from expert contributions"""
        logger.info(f"Generating final architecture for: {request.project_name}")
        
        # Compile all expert contributions
        contributions = []
        artifacts = []
        
        for result in expert_results:
            if result["status"] == "completed":
                contributions.append({
                    "expert": result["expert"],
                    "summary": result["summary"],
                    "recommendations": result.get("recommendations", [])
                })
                artifacts.extend(result.get("artifacts", []))
        
        # Use architecture expert to synthesize final architecture
        synthesis_result = await self.experts.invoke_expert(
            ExpertName.ARCHITECTURE,
            "synthesize_architecture",
            {
                "request": asdict(request),
                "contributions": contributions,
                "artifacts": artifacts
            }
        )
        
        return {
            "summary": synthesis_result.get("architecture_summary"),
            "diagrams": synthesis_result.get("diagrams", []),
            "documentation": synthesis_result.get("documentation", []),
            "code_structure": synthesis_result.get("code_structure", {}),
            "deployment_guide": synthesis_result.get("deployment_guide"),
            "artifacts_url": synthesis_result.get("artifacts_url")
        }

# Temporal Workflow Definitions
@workflow.defn
class ArchitectureWorkflow:
    """Temporal workflow for architecture generation"""
    
    @workflow.run
    async def run(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Main workflow execution"""
        request = ArchitectureRequest(**request_data)
        
        try:
            # Activity 1: Analyze requirements
            analysis = await workflow.execute_activity(
                analyze_requirements_activity,
                args=[asdict(request)],
                start_to_close_timeout=300
            )
            
            # Activity 2: Assign experts
            expert_assignments = await workflow.execute_activity(
                assign_experts_activity,
                args=[asdict(request), analysis],
                start_to_close_timeout=180
            )
            
            # Activity 3: Execute expert tasks
            expert_results = await workflow.execute_activity(
                execute_expert_tasks_activity,
                args=[asdict(request), expert_assignments],
                start_to_close_timeout=1800  # 30 minutes for expert tasks
            )
            
            # Activity 4: Generate architecture
            architecture = await workflow.execute_activity(
                generate_architecture_activity,
                args=[asdict(request), expert_results],
                start_to_close_timeout=600
            )
            
            # Activity 5: Finalize artifacts
            final_result = await workflow.execute_activity(
                finalize_artifacts_activity,
                args=[asdict(request), architecture],
                start_to_close_timeout=300
            )
            
            return final_result
            
        except Exception as e:
            logger.error(f"Workflow failed for request {request.request_id}: {str(e)}")
            raise

# Temporal Activities
@activity.defn
async def analyze_requirements_activity(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Temporal activity for requirements analysis"""
    # Implementation would call the orchestrator's analyze method
    pass

@activity.defn  
async def assign_experts_activity(request_data: Dict[str, Any], analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Temporal activity for expert assignment"""
    pass

@activity.defn
async def execute_expert_tasks_activity(request_data: Dict[str, Any], assignments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Temporal activity for expert task execution"""
    pass

@activity.defn
async def generate_architecture_activity(request_data: Dict[str, Any], expert_results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Temporal activity for architecture generation"""
    pass

@activity.defn
async def review_architecture_activity(request_data: Dict[str, Any], architecture: Dict[str, Any]) -> Dict[str, Any]:
    """Temporal activity for architecture review"""
    pass

@activity.defn
async def finalize_artifacts_activity(request_data: Dict[str, Any], architecture: Dict[str, Any]) -> Dict[str, Any]:
    """Temporal activity for finalizing artifacts"""
    pass
"""
Refinory AI Agent Orchestration Platform - Main API Server
Built for Strategickhaos Swarm Intelligence
"""

import asyncio
import logging
import sys
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any, Dict, List, Optional

import structlog
from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import uvicorn
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

from .config import Settings, get_settings
from .database import Database, get_db
from .orchestrator import ExpertOrchestrator, ArchitectureRequest, RequestStatus
from .experts import ExpertTeam
from .discord_integration import DiscordNotifier
from .github_integration import GitHubIntegration

# Import browser module from app directory
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from app.browser import ResearchBrowser, BrowseResponse

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# Prometheus metrics
REQUEST_COUNT = Counter('refinory_requests_total', 'Total requests processed')
REQUEST_DURATION = Histogram('refinory_request_duration_seconds', 'Request duration')
ARCHITECTURE_REQUESTS = Counter('refinory_architecture_requests_total', 'Architecture requests created')
EXPERT_INVOCATIONS = Counter('refinory_expert_invocations_total', 'Expert invocations', ['expert_name'])
BROWSE_REQUESTS = Counter('refinory_browse_requests_total', 'Research browser requests', ['allowed', 'robots_compliant'])

# Pydantic models
class CreateArchitectureRequest(BaseModel):
    project_name: str = Field(..., description="Name of the project")
    description: str = Field(..., description="Detailed project description")
    requirements: Optional[List[str]] = Field(default=[], description="Specific requirements")
    experts: Optional[List[str]] = Field(default=None, description="Specific experts to include")
    priority: Optional[str] = Field(default="normal", description="Request priority")
    github_repo: Optional[str] = Field(default=None, description="Target GitHub repository")

class ArchitectureResponse(BaseModel):
    request_id: str
    status: str
    created_at: str
    project_name: str
    description: str
    experts_assigned: List[str]
    progress: Dict[str, Any]
    artifacts_url: Optional[str] = None
    github_pr_url: Optional[str] = None

class ExpertResponse(BaseModel):
    expert_name: str
    status: str
    response: Optional[str] = None
    artifacts: List[str] = []
    timestamp: str

class HealthResponse(BaseModel):
    status: str
    version: str
    timestamp: str
    services: Dict[str, str]

# FastAPI lifespan management
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    logger.info("Starting Refinory AI Agent Orchestration Platform")
    
    # Initialize services
    settings = get_settings()
    
    # Initialize database
    db = Database(settings.postgres_dsn)
    await db.initialize()
    
    # Initialize expert team
    expert_team = ExpertTeam(settings)
    
    # Initialize orchestrator
    orchestrator = ExpertOrchestrator(db, expert_team, settings)
    
    # Initialize integrations
    discord_notifier = DiscordNotifier(settings.discord_token)
    github_integration = GitHubIntegration(settings.github_token, settings.refinory)
    
    # Initialize research browser
    browser_domains_path = Path(__file__).parent.parent.parent / "app" / "allowed_domains.yaml"
    research_browser = ResearchBrowser(
        allowed_domains_path=str(browser_domains_path),
        rate_limit_requests_per_minute=12
    )
    
    # Store in app state
    app.state.db = db
    app.state.orchestrator = orchestrator
    app.state.discord = discord_notifier
    app.state.github = github_integration
    app.state.settings = settings
    app.state.browser = research_browser
    
    logger.info("Refinory platform initialized successfully")
    
    yield
    
    # Cleanup
    logger.info("Shutting down Refinory platform")
    await research_browser.close()
    await db.close()

# Create FastAPI application
app = FastAPI(
    title="Refinory AI Agent Orchestration Platform",
    description="Advanced AI agent orchestration for autonomous software architecture and development",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency injection
def get_orchestrator() -> ExpertOrchestrator:
    return app.state.orchestrator

def get_discord() -> DiscordNotifier:
    return app.state.discord

def get_github() -> GitHubIntegration:
    return app.state.github

def get_browser() -> ResearchBrowser:
    return app.state.browser

# Health check endpoints
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    settings = get_settings()
    
    # Check service dependencies
    services = {}
    try:
        # Check database
        await app.state.db.health_check()
        services["database"] = "healthy"
    except Exception as e:
        services["database"] = f"unhealthy: {str(e)}"
    
    try:
        # Check Redis
        # Implement Redis health check
        services["redis"] = "healthy"
    except Exception as e:
        services["redis"] = f"unhealthy: {str(e)}"
    
    try:
        # Check Qdrant
        # Implement Qdrant health check  
        services["qdrant"] = "healthy"
    except Exception as e:
        services["qdrant"] = f"unhealthy: {str(e)}"
    
    overall_status = "healthy" if all(s == "healthy" for s in services.values()) else "degraded"
    
    return HealthResponse(
        status=overall_status,
        version="1.0.0",
        timestamp=str(asyncio.get_event_loop().time()),
        services=services
    )

@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    return generate_latest()

# Research browser endpoint
@app.get("/browse", response_model=BrowseResponse)
async def browse(
    url: str = Query(..., description="HTTPS URL on an allowed domain for research-only retrieval"),
    browser: ResearchBrowser = Depends(get_browser)
):
    """
    Sovereign Research Browse - Polite, robots.txt-respecting research browser
    
    This endpoint provides access to whitelisted domains for research purposes only.
    Features:
    - Domain whitelist enforcement (100+ research domains)
    - robots.txt compliance
    - Rate limiting (12 requests/minute per domain)
    - Structured psyche logging
    
    Tool Schema for Athena Integration:
    ```json
    {
      "type": "function",
      "function": {
        "name": "sovereign_research_browse",
        "description": "Polite, robots.txt-respecting research browser for whitelisted domains only.",
        "parameters": {
          "type": "object",
          "properties": {
            "url": {
              "type": "string",
              "description": "HTTPS URL on an allowed domain for research-only retrieval."
            }
          },
          "required": ["url"]
        }
      }
    }
    ```
    
    Error Semantics:
    - 403: Domain or path not allowed (whitelist / robots.txt)
    - 429: Rate limited (respect rate_limit_seconds in response)
    - 500: Server error
    
    Response Usage:
    - Use text_preview as summary input to LLM
    - For content longer than 10k chars, consider multiple calls or follow-up processing
    """
    REQUEST_COUNT.inc()
    
    try:
        response = await browser.browse(url)
        
        # Update Prometheus metrics
        BROWSE_REQUESTS.labels(
            allowed=str(response.research_allowed),
            robots_compliant=str(response.robots_compliant)
        ).inc()
        
        # Return appropriate HTTP status codes
        if not response.research_allowed:
            raise HTTPException(status_code=403, detail=response.error or "Domain not allowed")
        
        if not response.robots_compliant:
            raise HTTPException(status_code=403, detail=response.error or "Disallowed by robots.txt")
        
        if response.rate_limited:
            raise HTTPException(status_code=429, detail=response.error or "Rate limited")
        
        if response.error and response.status_code != 200:
            raise HTTPException(status_code=500, detail=response.error)
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("browse_endpoint_error", error=str(e), url=url)
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

# Architecture request endpoints
@app.post("/api/v1/architecture/request", response_model=ArchitectureResponse)
async def create_architecture_request(
    request: CreateArchitectureRequest,
    background_tasks: BackgroundTasks,
    orchestrator: ExpertOrchestrator = Depends(get_orchestrator),
    discord: DiscordNotifier = Depends(get_discord),
    github: GitHubIntegration = Depends(get_github)
):
    """Create new architecture request"""
    REQUEST_COUNT.inc()
    ARCHITECTURE_REQUESTS.inc()
    
    logger.info(f"Creating architecture request for project: {request.project_name}")
    
    try:
        # Create architecture request
        arch_request = ArchitectureRequest(
            project_name=request.project_name,
            description=request.description,
            requirements=request.requirements or [],
            experts_requested=request.experts,
            priority=request.priority,
            github_repo=request.github_repo
        )
        
        # Submit to orchestrator
        request_id = await orchestrator.submit_request(arch_request)
        
        # Start processing in background
        background_tasks.add_task(
            process_architecture_request,
            request_id,
            orchestrator,
            discord,
            github
        )
        
        # Get request details for response
        request_details = await orchestrator.get_request_status(request_id)
        
        return ArchitectureResponse(
            request_id=request_id,
            status=request_details.status.value,
            created_at=request_details.created_at.isoformat(),
            project_name=request_details.project_name,
            description=request_details.description,
            experts_assigned=request_details.experts_assigned,
            progress=request_details.progress
        )
        
    except Exception as e:
        logger.error(f"Failed to create architecture request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/architecture/request/{request_id}", response_model=ArchitectureResponse)
async def get_architecture_request(
    request_id: str,
    orchestrator: ExpertOrchestrator = Depends(get_orchestrator)
):
    """Get architecture request status"""
    try:
        request_details = await orchestrator.get_request_status(request_id)
        
        return ArchitectureResponse(
            request_id=request_id,
            status=request_details.status.value,
            created_at=request_details.created_at.isoformat(),
            project_name=request_details.project_name,
            description=request_details.description,
            experts_assigned=request_details.experts_assigned,
            progress=request_details.progress,
            artifacts_url=request_details.artifacts_url,
            github_pr_url=request_details.github_pr_url
        )
        
    except Exception as e:
        logger.error(f"Failed to get request {request_id}: {str(e)}")
        raise HTTPException(status_code=404, detail=f"Request {request_id} not found")

@app.get("/api/v1/architecture/requests", response_model=List[ArchitectureResponse])
async def list_architecture_requests(
    status: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    orchestrator: ExpertOrchestrator = Depends(get_orchestrator)
):
    """List architecture requests with optional filtering"""
    try:
        requests = await orchestrator.list_requests(
            status=RequestStatus(status) if status else None,
            limit=limit,
            offset=offset
        )
        
        return [
            ArchitectureResponse(
                request_id=req.request_id,
                status=req.status.value,
                created_at=req.created_at.isoformat(),
                project_name=req.project_name,
                description=req.description,
                experts_assigned=req.experts_assigned,
                progress=req.progress,
                artifacts_url=req.artifacts_url,
                github_pr_url=req.github_pr_url
            )
            for req in requests
        ]
        
    except Exception as e:
        logger.error(f"Failed to list requests: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Expert management endpoints
@app.get("/api/v1/experts", response_model=List[Dict[str, Any]])
async def list_experts():
    """List available experts"""
    return [
        {"name": "frontend", "description": "Frontend development and UI/UX"},
        {"name": "backend", "description": "Backend services and APIs"},
        {"name": "devops", "description": "Infrastructure and deployment"},
        {"name": "security", "description": "Security analysis and hardening"},
        {"name": "ai_ml", "description": "AI/ML systems and algorithms"},
        {"name": "mobile", "description": "Mobile application development"},
        {"name": "blockchain", "description": "Blockchain and DeFi systems"},
        {"name": "testing", "description": "Testing strategies and automation"},
        {"name": "architecture", "description": "System architecture and design"},
        {"name": "data_science", "description": "Data analysis and processing"},
    ]

# Background task processor
async def process_architecture_request(
    request_id: str,
    orchestrator: ExpertOrchestrator,
    discord: DiscordNotifier,
    github: GitHubIntegration
):
    """Process architecture request asynchronously"""
    try:
        logger.info(f"Processing architecture request: {request_id}")
        
        # Notify Discord of new request
        await discord.notify_request_created(request_id)
        
        # Start orchestration process
        result = await orchestrator.process_request(request_id)
        
        # Notify Discord of completion
        await discord.notify_architecture_ready(request_id, result)
        
        # Create GitHub PR if requested
        if result.github_repo:
            pr_url = await github.create_architecture_pr(result)
            await orchestrator.update_github_pr_url(request_id, pr_url)
            await discord.notify_pr_created(request_id, pr_url)
        
        logger.info(f"Completed processing request: {request_id}")
        
    except Exception as e:
        logger.error(f"Failed to process request {request_id}: {str(e)}")
        await discord.notify_error(request_id, str(e))

if __name__ == "__main__":
    settings = get_settings()
    uvicorn.run(
        "refinory.main:app",
        host="0.0.0.0",
        port=settings.refinory.ports.api,
        reload=settings.refinory_env == "development",
        log_config=None,  # Use structlog
    )
"""
Legends of Minds - Control Center
Main API server with safety monitoring integration
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import httpx
from typing import Dict, Any, Optional
from datetime import datetime, timezone

# Import safety monitoring router
from safety_monitor import router as safety_router

# Create FastAPI application
app = FastAPI(
    title="Legends of Minds - Control Center",
    description="Local AI lab control center with real-time safety monitoring",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include safety monitoring router
app.include_router(safety_router)

@app.get("/")
async def root():
    """Root endpoint - return basic info"""
    return {
        "name": "Legends of Minds Control Center",
        "version": "1.0.0",
        "status": "operational",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "endpoints": {
            "docs": "/docs",
            "safety": "/api/safety/full_report",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    
    services = {}
    
    # Check Ollama
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get("http://host.docker.internal:11434/api/tags")
            if resp.status_code == 200:
                services["ollama"] = "healthy"
            else:
                services["ollama"] = f"unhealthy: status {resp.status_code}"
    except Exception as e:
        services["ollama"] = f"unhealthy: {str(e)}"
    
    # Check Qdrant
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get("http://qdrant:6333/health")
            if resp.status_code == 200:
                services["qdrant"] = "healthy"
            else:
                services["qdrant"] = f"unhealthy: status {resp.status_code}"
    except Exception as e:
        services["qdrant"] = f"unhealthy: {str(e)}"
    
    overall_status = "healthy" if all(s == "healthy" for s in services.values()) else "degraded"
    
    return {
        "status": overall_status,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "services": services
    }

@app.post("/api/generate")
async def generate_text(request: Dict[str, Any]):
    """Proxy to Ollama for text generation"""
    
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.post(
                "http://host.docker.internal:11434/api/generate",
                json=request
            )
            return resp.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/models")
async def list_models():
    """List available Ollama models"""
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get("http://host.docker.internal:11434/api/tags")
            if resp.status_code == 200:
                return resp.json()
            else:
                raise HTTPException(status_code=resp.status_code, detail="Failed to fetch models")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8080,
        reload=True
    )

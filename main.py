# main.py
"""Main FastAPI application for artifact access control."""
from fastapi import FastAPI
from routes.artifacts import router as artifacts_router

app = FastAPI(
    title="Sovereignty Architecture - Artifact Access Control",
    description="Production-ready, audit-clean access control for classified artifacts",
    version="1.0.0",
)

app.include_router(artifacts_router)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "artifact-access-control"}

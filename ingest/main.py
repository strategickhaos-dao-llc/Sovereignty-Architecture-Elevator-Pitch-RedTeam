"""
Legends of Minds - File Ingest Service
Handles document upload and processing for the knowledge base
"""

from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pathlib import Path
from typing import List, Optional
import httpx
import hashlib
from datetime import datetime, timezone
import json
import os

app = FastAPI(
    title="Legends of Minds - File Ingest",
    description="Document ingestion and processing service",
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

# Configure upload directory
UPLOAD_DIR = Path("/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "Legends of Minds - File Ingest Service",
        "version": "1.0.0",
        "status": "operational",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "endpoints": {
            "docs": "/docs",
            "upload": "/api/upload",
            "files": "/api/files"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    
    services = {}
    
    # Check upload directory is writable
    try:
        test_file = UPLOAD_DIR / ".health_check"
        test_file.write_text("test")
        test_file.unlink()
        services["storage"] = "healthy"
    except Exception as e:
        services["storage"] = f"unhealthy: {str(e)}"
    
    # Check Ollama connectivity
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get("http://host.docker.internal:11434/api/tags")
            if resp.status_code == 200:
                services["ollama"] = "healthy"
            else:
                services["ollama"] = f"unhealthy: status {resp.status_code}"
    except Exception as e:
        services["ollama"] = f"unhealthy: {str(e)}"
    
    # Check Qdrant connectivity
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

@app.post("/api/upload")
async def upload_file(
    file: UploadFile = File(...),
    collection: Optional[str] = Form("default")
):
    """Upload and process a file"""
    
    try:
        # Generate file hash for deduplication
        content = await file.read()
        file_hash = hashlib.sha256(content).hexdigest()
        
        # Save file
        safe_filename = file.filename.replace("/", "_").replace("\\", "_")
        file_path = UPLOAD_DIR / f"{file_hash[:8]}_{safe_filename}"
        
        with open(file_path, "wb") as f:
            f.write(content)
        
        # Store metadata
        metadata = {
            "filename": file.filename,
            "size": len(content),
            "hash": file_hash,
            "uploaded_at": datetime.now(timezone.utc).isoformat(),
            "collection": collection,
            "path": str(file_path)
        }
        
        metadata_path = file_path.with_suffix(file_path.suffix + ".meta.json")
        with open(metadata_path, "w") as f:
            json.dump(metadata, f, indent=2)
        
        return {
            "status": "success",
            "file_id": file_hash[:16],
            "filename": file.filename,
            "size": len(content),
            "message": "File uploaded successfully. Processing will begin shortly."
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/files")
async def list_files():
    """List uploaded files"""
    
    try:
        files = []
        for meta_file in UPLOAD_DIR.glob("*.meta.json"):
            with open(meta_file, "r") as f:
                metadata = json.load(f)
                files.append(metadata)
        
        # Sort by upload time, newest first
        files.sort(key=lambda x: x.get("uploaded_at", ""), reverse=True)
        
        return {
            "status": "success",
            "count": len(files),
            "files": files
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/files/{file_id}")
async def delete_file(file_id: str):
    """Delete an uploaded file"""
    
    try:
        # Find file by hash prefix
        found = False
        for meta_file in UPLOAD_DIR.glob(f"{file_id}*.meta.json"):
            with open(meta_file, "r") as f:
                metadata = json.load(f)
            
            # Delete data file
            data_path = Path(metadata["path"])
            if data_path.exists():
                data_path.unlink()
            
            # Delete metadata file
            meta_file.unlink()
            found = True
        
        if not found:
            raise HTTPException(status_code=404, detail="File not found")
        
        return {
            "status": "success",
            "message": "File deleted successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

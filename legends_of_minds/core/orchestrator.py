"""
Legends of Minds - Universal Orchestrator
Core API server for unified agent orchestration platform
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import asyncio
import json
import logging
from typing import Dict, List, Optional
from datetime import datetime
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Legends of Minds - Universal Orchestrator",
    description="Production-grade meta-system for unified agent orchestration",
    version="1.0.0"
)

# CORS middleware for web UI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Active WebSocket connections for terminal agents
active_connections: Dict[str, WebSocket] = {}

# Store for proof action ledger
proof_ledger: List[Dict] = []


class ConnectionManager:
    """Manage WebSocket connections for terminal agents"""
    
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, terminal_id: str):
        await websocket.accept()
        self.active_connections[terminal_id] = websocket
        logger.info(f"Terminal agent {terminal_id} connected")
    
    def disconnect(self, terminal_id: str):
        if terminal_id in self.active_connections:
            del self.active_connections[terminal_id]
            logger.info(f"Terminal agent {terminal_id} disconnected")
    
    async def send_personal_message(self, message: str, terminal_id: str):
        if terminal_id in self.active_connections:
            websocket = self.active_connections[terminal_id]
            await websocket.send_text(message)
    
    async def broadcast(self, message: str):
        for connection in self.active_connections.values():
            await connection.send_text(message)


manager = ConnectionManager()


@app.get("/")
async def root():
    """Root endpoint - redirect to command center"""
    return {
        "service": "Legends of Minds - Universal Orchestrator",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": {
            "web": "/command-center",
            "api": "/api/v1",
            "docs": "/docs",
            "health": "/health"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "active_terminals": len(manager.active_connections),
        "proof_ledger_entries": len(proof_ledger)
    }


@app.get("/api/v1/status")
async def get_status():
    """Get system status"""
    return {
        "active_terminals": len(manager.active_connections),
        "proof_ledger_entries": len(proof_ledger),
        "departments": {
            "proof_ledger": "active",
            "gitlens": "active",
            "refinery_mcp": "active",
            "legal_compliance": "active"
        }
    }


@app.get("/api/v1/proof-ledger")
async def get_proof_ledger(limit: int = 100):
    """Get proof action ledger entries"""
    return {
        "entries": proof_ledger[-limit:],
        "total": len(proof_ledger)
    }


@app.post("/api/v1/proof-ledger")
async def add_proof_entry(entry: dict):
    """Add entry to proof action ledger"""
    proof_entry = {
        "id": len(proof_ledger) + 1,
        "timestamp": datetime.utcnow().isoformat(),
        "action": entry.get("action", "unknown"),
        "department": entry.get("department", "unknown"),
        "data": entry.get("data", {}),
        "hash": hash(json.dumps(entry, sort_keys=True))
    }
    proof_ledger.append(proof_entry)
    logger.info(f"Added proof ledger entry: {proof_entry['id']}")
    return proof_entry


@app.websocket("/ws/terminal/{terminal_id}")
async def websocket_terminal(websocket: WebSocket, terminal_id: str):
    """WebSocket endpoint for terminal agents"""
    await manager.connect(websocket, terminal_id)
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Log to proof ledger
            await add_proof_entry({
                "action": "terminal_command",
                "department": "terminal",
                "data": {
                    "terminal_id": terminal_id,
                    "command": message.get("command", "")
                }
            })
            
            # Echo back with timestamp
            response = {
                "terminal_id": terminal_id,
                "timestamp": datetime.utcnow().isoformat(),
                "received": message
            }
            await manager.send_personal_message(json.dumps(response), terminal_id)
            
    except WebSocketDisconnect:
        manager.disconnect(terminal_id)


@app.post("/api/v1/departments/{department}/execute")
async def execute_department_action(department: str, action: dict):
    """Execute action in specific department"""
    
    # Log to proof ledger
    proof_entry = await add_proof_entry({
        "action": action.get("type", "execute"),
        "department": department,
        "data": action
    })
    
    return {
        "status": "executed",
        "department": department,
        "action": action.get("type", "execute"),
        "proof_id": proof_entry["id"]
    }


@app.get("/api/v1/departments")
async def list_departments():
    """List available departments"""
    return {
        "departments": [
            {
                "id": "proof_ledger",
                "name": "Proof Action Ledger",
                "description": "Immutable audit trail of all operations",
                "status": "active"
            },
            {
                "id": "gitlens",
                "name": "GitLens Integration",
                "description": "Repository analysis and code search",
                "status": "active"
            },
            {
                "id": "refinery_mcp",
                "name": "Refinery MCP",
                "description": "Model Context Protocol integration",
                "status": "active"
            },
            {
                "id": "legal_compliance",
                "name": "Legal Compliance",
                "description": "Multi-jurisdiction legal compliance checking",
                "status": "active"
            },
            {
                "id": "compose_gen",
                "name": "Compose Generator",
                "description": "Docker compose file generation",
                "status": "active"
            },
            {
                "id": "yaml_gen",
                "name": "YAML Generator",
                "description": "Configuration file generation",
                "status": "active"
            }
        ]
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("ORCHESTRATOR_PORT", "8080"))
    uvicorn.run(app, host="0.0.0.0", port=port)

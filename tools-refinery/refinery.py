"""
Tools Refinery - FastAPI server for exposing safe, idempotent tools to LLM clients
Version 0.1
"""
from fastapi import FastAPI, HTTPException, Request, Body
from fastapi.responses import JSONResponse
from typing import Any, Dict
import uvicorn
import importlib
import inspect
import os
from pathlib import Path
import yaml

app = FastAPI(
    title="Tools Refinery",
    version="0.1",
    description="Safe, idempotent tools for LLM clients via OpenAI-compatible endpoints"
)

# Load configuration
config_path = Path(__file__).parent / "config.yaml"
with open(config_path) as f:
    config = yaml.safe_load(f)

# Simple API key auth (put whatever you want in header X-API-Key)
API_KEY = os.getenv("REFINERY_KEY", config.get("system", {}).get("api_key", "dev-key-change-me"))

@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    """Authentication middleware for tool endpoints"""
    if request.url.path.startswith("/v1/tools") or request.url.path == "/openapi.json":
        api_key = request.headers.get("x-api-key")
        if api_key != API_KEY:
            return JSONResponse(
                status_code=401,
                content={"error": "Unauthorized", "message": "Invalid or missing API key"}
            )
    response = await call_next(request)
    return response

@app.get("/")
async def root():
    """Root endpoint with basic info"""
    return {
        "name": "Tools Refinery",
        "version": "0.1",
        "description": "Safe, idempotent tools for LLM clients",
        "endpoints": {
            "tools": "/v1/tools/*",
            "openapi": "/openapi.json",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "version": "0.1"}

# Auto-register every function in tools.* that has a __tool__ dict
tools_dir = Path(__file__).parent / "tools"
registered_tools = []

if tools_dir.exists():
    for module_file in tools_dir.glob("*.py"):
        if module_file.name.startswith("_"):
            continue
        
        module_name = module_file.stem
        try:
            module = importlib.import_module(f"tools.{module_name}")
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if callable(attr) and hasattr(attr, "__tool__"):
                    tool_info = attr.__tool__
                    tool_name = tool_info.get("name", attr_name)
                    
                    # Get the function signature to find the args model
                    sig = inspect.signature(attr)
                    args_param = list(sig.parameters.values())[0]
                    args_model = args_param.annotation
                    
                    # Create endpoint with proper type hints for FastAPI
                    def make_endpoint(func, model):
                        async def tool_endpoint(args: model = Body(...)):
                            """Dynamically created tool endpoint"""
                            try:
                                result = func(args)
                                return {"result": result, "success": True}
                            except Exception as e:
                                return {"error": str(e), "success": False}
                        return tool_endpoint
                    
                    endpoint = make_endpoint(attr, args_model)
                    endpoint.__name__ = tool_name
                    endpoint.__doc__ = tool_info.get("description", "")
                    
                    # Register with FastAPI
                    app.post(f"/v1/tools/{tool_name}")(endpoint)
                    registered_tools.append(tool_name)
                    
        except Exception as e:
            print(f"Warning: Could not load tools from {module_name}: {e}")

print(f"Registered {len(registered_tools)} tools: {', '.join(registered_tools)}")

if __name__ == "__main__":
    host = config.get("system", {}).get("host", "127.0.0.1")
    port = config.get("system", {}).get("port", 8211)
    uvicorn.run("refinery:app", host=host, port=port, reload=True)

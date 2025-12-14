#!/usr/bin/env python3
"""
Claude API Mirror
Creates local replicas of Claude API endpoints for sovereign mesh
"""

import os
import time
import json
import asyncio
from typing import Dict, Optional, Any
from datetime import datetime, timedelta
import httpx
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import redis.asyncio as redis

# Configuration
CLAUDE_API_BASE = os.getenv("CLAUDE_API_BASE", "https://claude.ai")
CLAUDE_SESSION_KEY = os.getenv("CLAUDE_SESSION_KEY", "")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
CACHE_TTL = int(os.getenv("CACHE_TTL", "3600"))  # 1 hour

# CORS middleware (will be added after app initialization)

# Global clients
httpx_client = None
redis_client = None

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan."""
    global httpx_client, redis_client
    
    # Startup
    # HTTP client with Claude session key
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; SovereignMesh/1.0)",
        "Accept": "application/json, text/x-component",
        "Cookie": f"sessionKey={CLAUDE_SESSION_KEY}"
    }
    
    httpx_client = httpx.AsyncClient(
        headers=headers,
        timeout=30,
        follow_redirects=True
    )
    
    # Redis client for caching
    try:
        redis_client = redis.from_url(REDIS_URL, decode_responses=True)
        await redis_client.ping()
        print("✅ Connected to Redis cache")
    except Exception as e:
        print(f"⚠️ Redis not available: {e}")
        redis_client = None
    
    print("🚀 Claude API Mirror started")
    
    yield
    
    # Shutdown
    if httpx_client:
        await httpx_client.aclose()
    
    if redis_client:
        await redis_client.close()
    
    print("👋 Claude API Mirror shutdown")

# Update app initialization to use lifespan
app = FastAPI(
    title="Claude API Mirror",
    description="Local replica of Claude API endpoints for sovereign mesh",
    version="1.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def get_cached(key: str) -> Optional[str]:
    """Get cached response from Redis."""
    if not redis_client:
        return None
    
    try:
        return await redis_client.get(key)
    except Exception:
        return None

async def set_cached(key: str, value: str, ttl: int = CACHE_TTL):
    """Cache response in Redis."""
    if not redis_client:
        return
    
    try:
        await redis_client.setex(key, ttl, value)
    except Exception:
        pass

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "service": "Claude API Mirror",
        "version": "1.0.0",
        "description": "Local replica of Claude API endpoints",
        "endpoints": {
            "spotlight": "/api/organizations/{org}/spotlight",
            "recents": "/api/organizations/{org}/recents",
            "chat": "/chat/{uuid}",
            "health": "/health"
        }
    }

@app.get("/health")
async def health():
    """Health check."""
    return {
        "status": "healthy",
        "redis": redis_client is not None,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/organizations/{org}/spotlight")
async def mirror_spotlight(org: str):
    """
    Mirror Claude spotlight endpoint.
    Returns feature flags and configuration.
    """
    cache_key = f"spotlight:{org}"
    
    # Check cache
    cached = await get_cached(cache_key)
    if cached:
        return Response(content=cached, media_type="application/json")
    
    # Fetch from Claude API
    try:
        url = f"{CLAUDE_API_BASE}/api/organizations/{org}/spotlight"
        response = await httpx_client.get(url)
        
        if response.status_code == 403:
            raise HTTPException(status_code=403, detail="Endpoint disabled or unauthorized")
        
        response.raise_for_status()
        
        # Cache successful response
        await set_cached(cache_key, response.text)
        
        return Response(
            content=response.text,
            media_type="application/json",
            headers={"X-Cache": "MISS"}
        )
        
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/organizations/{org}/recents")
async def mirror_recents(org: str, limit: int = 20):
    """
    Mirror Claude recents endpoint.
    Returns recent chat sessions.
    """
    cache_key = f"recents:{org}:limit={limit}"
    
    # Check cache with shorter TTL (recent data changes frequently)
    cached = await get_cached(cache_key)
    if cached:
        return Response(content=cached, media_type="application/json")
    
    # Fetch from Claude API
    try:
        url = f"{CLAUDE_API_BASE}/api/organizations/{org}/recents"
        response = await httpx_client.get(url, params={"limit": limit})
        
        if response.status_code == 403:
            raise HTTPException(status_code=403, detail="Endpoint disabled or unauthorized")
        
        response.raise_for_status()
        
        # Cache with shorter TTL (5 minutes for recent data)
        await set_cached(cache_key, response.text, ttl=300)
        
        return Response(
            content=response.text,
            media_type="application/json",
            headers={"X-Cache": "MISS"}
        )
        
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/chat/{uuid}")
async def mirror_chat(uuid: str):
    """
    Mirror Claude chat endpoint.
    Returns chat session data in RSC format.
    """
    cache_key = f"chat:{uuid}"
    
    # Check cache
    cached = await get_cached(cache_key)
    if cached:
        return Response(content=cached, media_type="text/x-component")
    
    # Fetch from Claude API
    try:
        url = f"{CLAUDE_API_BASE}/chat/{uuid}"
        response = await httpx_client.get(url)
        
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Chat not found")
        
        response.raise_for_status()
        
        # Cache chat data (longer TTL as it's less likely to change)
        await set_cached(cache_key, response.text, ttl=7200)  # 2 hours
        
        return Response(
            content=response.text,
            media_type="text/x-component",
            headers={"X-Cache": "MISS"}
        )
        
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/organizations/{org}/published_artifacts")
async def mirror_artifacts(org: str):
    """
    Mirror Claude published artifacts endpoint.
    Note: This may return 403 as it's often disabled.
    """
    cache_key = f"artifacts:{org}"
    
    # Check cache
    cached = await get_cached(cache_key)
    if cached:
        return Response(content=cached, media_type="application/json")
    
    # Fetch from Claude API
    try:
        url = f"{CLAUDE_API_BASE}/api/organizations/{org}/published_artifacts"
        response = await httpx_client.get(url)
        
        if response.status_code == 403:
            # Return structured 403 response
            return Response(
                content=json.dumps({
                    "error": "Endpoint disabled",
                    "message": "Published artifacts endpoint is not available for this organization"
                }),
                status_code=403,
                media_type="application/json"
            )
        
        response.raise_for_status()
        
        # Cache successful response
        await set_cached(cache_key, response.text)
        
        return Response(
            content=response.text,
            media_type="application/json",
            headers={"X-Cache": "MISS"}
        )
        
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/cache/{key}")
async def invalidate_cache(key: str):
    """Invalidate cache entry."""
    if not redis_client:
        raise HTTPException(status_code=503, detail="Cache not available")
    
    try:
        deleted = await redis_client.delete(key)
        return {
            "invalidated": deleted > 0,
            "key": key
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/cache/stats")
async def cache_stats():
    """Get cache statistics."""
    if not redis_client:
        raise HTTPException(status_code=503, detail="Cache not available")
    
    try:
        info = await redis_client.info("stats")
        
        # Get all keys matching our patterns
        patterns = ["spotlight:*", "recents:*", "chat:*", "artifacts:*"]
        total_keys = 0
        
        for pattern in patterns:
            keys = await redis_client.keys(pattern)
            total_keys += len(keys)
        
        return {
            "total_keys": total_keys,
            "redis_info": {
                "total_connections_received": info.get("total_connections_received"),
                "total_commands_processed": info.get("total_commands_processed"),
                "keyspace_hits": info.get("keyspace_hits"),
                "keyspace_misses": info.get("keyspace_misses")
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7001)

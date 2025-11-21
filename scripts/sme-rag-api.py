#!/usr/bin/env python3
"""
SME RAG API
Query the SME knowledge base using RAG (Retrieval Augmented Generation)
"""

import os
import json
import time
from typing import Dict, List, Optional
import yaml
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

# Configuration
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
MODEL_NAME = os.getenv("MODEL_NAME", "llama3:70b")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "sme_knowledge")
API_PORT = int(os.getenv("API_PORT", "8090"))

# Initialize FastAPI
app = FastAPI(
    title="SME RAG API",
    description="Query sovereign infrastructure knowledge base",
    version="1.0.0"
)

# Request/Response models
class QueryRequest(BaseModel):
    question: str
    max_results: int = 5
    min_score: float = 0.5


class QueryResponse(BaseModel):
    question: str
    answer: str
    sources: List[Dict]
    query_time: float


def get_embedding(text: str) -> List[float]:
    """Get embedding from Ollama"""
    try:
        response = requests.post(
            f"{OLLAMA_HOST}/api/embeddings",
            json={
                "model": EMBEDDING_MODEL,
                "prompt": text
            },
            timeout=60
        )
        response.raise_for_status()
        result = response.json()
        return result.get("embedding", [])
    except Exception as e:
        print(f"Embedding error: {e}")
        return []


def search_qdrant(query_vector: List[float], limit: int = 5, score_threshold: float = 0.5) -> List[Dict]:
    """Search Qdrant for similar vectors"""
    try:
        response = requests.post(
            f"{QDRANT_URL}/collections/{COLLECTION_NAME}/points/search",
            json={
                "vector": query_vector,
                "limit": limit,
                "score_threshold": score_threshold,
                "with_payload": True
            },
            timeout=30
        )
        response.raise_for_status()
        result = response.json()
        return result.get("result", [])
    except Exception as e:
        print(f"Search error: {e}")
        return []


def generate_answer(question: str, context_docs: List[Dict]) -> str:
    """Generate answer using Ollama with context"""
    
    # Build context from retrieved documents
    context_parts = []
    for i, doc in enumerate(context_docs[:5], 1):
        payload = doc.get("payload", {})
        context_parts.append(f"""
Source {i}: {payload.get('title', 'Unknown')}
Category: {payload.get('category', 'unknown')}
URL: {payload.get('url', 'N/A')}
Content: {payload.get('text_sample', 'N/A')}
""")
    
    context = "\n---\n".join(context_parts)
    
    prompt = f"""You are a sovereign infrastructure expert. Answer the following question using the provided documentation sources.

Question: {question}

Available Documentation:
{context}

Instructions:
1. Answer the question accurately based on the sources
2. Cite specific sources when possible
3. If the sources don't contain enough information, say so
4. Provide practical, actionable guidance
5. Be concise but thorough

Answer:"""

    try:
        response = requests.post(
            f"{OLLAMA_HOST}/api/generate",
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False
            },
            timeout=180
        )
        response.raise_for_status()
        result = response.json()
        return result.get("response", "Unable to generate answer")
    except Exception as e:
        return f"Error generating answer: {e}"


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "SME RAG API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    # Check Qdrant
    qdrant_ok = False
    try:
        response = requests.get(f"{QDRANT_URL}/", timeout=5)
        qdrant_ok = response.status_code == 200
    except:
        pass
    
    # Check Ollama
    ollama_ok = False
    try:
        response = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=5)
        ollama_ok = response.status_code == 200
    except:
        pass
    
    return {
        "status": "healthy" if (qdrant_ok and ollama_ok) else "degraded",
        "qdrant": "ok" if qdrant_ok else "unavailable",
        "ollama": "ok" if ollama_ok else "unavailable",
        "timestamp": time.time()
    }


@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """Query the knowledge base"""
    start_time = time.time()
    
    question = request.question
    max_results = request.max_results
    min_score = request.min_score
    
    print(f"\nQuery: {question}")
    
    # Get question embedding
    query_vector = get_embedding(question)
    if not query_vector:
        raise HTTPException(status_code=500, detail="Failed to generate embedding")
    
    # Search Qdrant
    search_results = search_qdrant(query_vector, limit=max_results, score_threshold=min_score)
    print(f"Found {len(search_results)} relevant documents")
    
    if not search_results:
        return QueryResponse(
            question=question,
            answer="No relevant documentation found for your question.",
            sources=[],
            query_time=time.time() - start_time
        )
    
    # Generate answer
    answer = generate_answer(question, search_results)
    
    # Format sources
    sources = []
    for result in search_results:
        payload = result.get("payload", {})
        sources.append({
            "title": payload.get("title", "Unknown"),
            "category": payload.get("category", "unknown"),
            "url": payload.get("url", ""),
            "relevance_score": result.get("score", 0.0),
            "topics": payload.get("sme_topics", [])
        })
    
    query_time = time.time() - start_time
    print(f"Query completed in {query_time:.2f}s")
    
    return QueryResponse(
        question=question,
        answer=answer,
        sources=sources,
        query_time=query_time
    )


@app.get("/collection/info")
async def collection_info():
    """Get collection information"""
    try:
        response = requests.get(f"{QDRANT_URL}/collections/{COLLECTION_NAME}")
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=404, detail="Collection not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/stats")
async def stats():
    """Get API statistics"""
    try:
        # Get collection stats
        response = requests.get(f"{QDRANT_URL}/collections/{COLLECTION_NAME}")
        collection_info = response.json() if response.status_code == 200 else {}
        
        points_count = collection_info.get("result", {}).get("points_count", 0)
        
        return {
            "collection_name": COLLECTION_NAME,
            "total_documents": points_count,
            "embedding_model": EMBEDDING_MODEL,
            "llm_model": MODEL_NAME,
            "qdrant_url": QDRANT_URL,
            "ollama_host": OLLAMA_HOST
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def main():
    """Start the API server"""
    print("=" * 80)
    print("SME RAG API")
    print("=" * 80)
    print(f"Qdrant URL: {QDRANT_URL}")
    print(f"Ollama host: {OLLAMA_HOST}")
    print(f"Collection: {COLLECTION_NAME}")
    print(f"LLM Model: {MODEL_NAME}")
    print(f"Embedding Model: {EMBEDDING_MODEL}")
    print(f"Port: {API_PORT}")
    print()
    print(f"API will be available at: http://0.0.0.0:{API_PORT}")
    print("Documentation: http://0.0.0.0:{API_PORT}/docs")
    print("=" * 80)
    print()
    
    # Start server
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=API_PORT,
        log_level="info"
    )


if __name__ == "__main__":
    main()

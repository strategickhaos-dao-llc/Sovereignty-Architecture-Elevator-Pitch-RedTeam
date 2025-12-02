#!/usr/bin/env python3
"""
Vector Indexer
Indexes SME resources into Qdrant vector database
"""

import os
import json
import time
from pathlib import Path
from typing import Dict, List
import requests

# Configuration
DATA_DIR = Path("/app/data/processed")
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "sme_knowledge")


def create_collection():
    """Create Qdrant collection if it doesn't exist"""
    try:
        # Check if collection exists
        response = requests.get(f"{QDRANT_URL}/collections/{COLLECTION_NAME}")
        if response.status_code == 200:
            print(f"✓ Collection '{COLLECTION_NAME}' already exists")
            return True
    except:
        pass
    
    # Create collection
    print(f"Creating collection '{COLLECTION_NAME}'...")
    response = requests.put(
        f"{QDRANT_URL}/collections/{COLLECTION_NAME}",
        json={
            "vectors": {
                "size": 768,  # nomic-embed-text dimension
                "distance": "Cosine"
            }
        }
    )
    
    if response.status_code in [200, 201]:
        print("✓ Collection created")
        return True
    else:
        print(f"✗ Failed to create collection: {response.text}")
        return False


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
        print(f"  ✗ Embedding error: {e}")
        return []


def index_resource(resource_data: Dict) -> bool:
    """Index a single resource into Qdrant"""
    
    resource_id = resource_data.get("resource_id")
    title = resource_data.get("title", "")
    text = resource_data.get("text", "")
    category = resource_data.get("category", "")
    url = resource_data.get("url", "")
    
    # Create text for embedding (title + first 1000 chars)
    embedding_text = f"{title}\n\n{text[:1000]}"
    
    print(f"  Getting embedding for resource {resource_id}...")
    embedding = get_embedding(embedding_text)
    
    if not embedding:
        return False
    
    # Prepare point for Qdrant
    point = {
        "id": resource_id,
        "vector": embedding,
        "payload": {
            "title": title,
            "category": category,
            "url": url,
            "text_sample": text[:500],  # Store sample for quick retrieval
            "full_text_length": len(text),
            "sme_topics": resource_data.get("sme_topics", []),
            "indexed_at": time.time()
        }
    }
    
    # Upload to Qdrant
    try:
        response = requests.put(
            f"{QDRANT_URL}/collections/{COLLECTION_NAME}/points",
            json={
                "points": [point]
            }
        )
        
        if response.status_code in [200, 201]:
            print(f"  ✓ Indexed resource {resource_id}")
            return True
        else:
            print(f"  ✗ Failed to index: {response.text}")
            return False
            
    except Exception as e:
        print(f"  ✗ Index error: {e}")
        return False


def main():
    print("=" * 80)
    print("Vector Indexer")
    print("=" * 80)
    print(f"Data directory: {DATA_DIR}")
    print(f"Qdrant URL: {QDRANT_URL}")
    print(f"Ollama host: {OLLAMA_HOST}")
    print(f"Embedding model: {EMBEDDING_MODEL}")
    print(f"Collection: {COLLECTION_NAME}")
    print()
    
    # Check services availability
    print("Checking services...")
    try:
        requests.get(f"{QDRANT_URL}/", timeout=5)
        print("✓ Qdrant is available")
    except Exception as e:
        print(f"✗ Qdrant not available: {e}")
        return
    
    try:
        requests.get(f"{OLLAMA_HOST}/api/tags", timeout=5)
        print("✓ Ollama is available")
    except Exception as e:
        print(f"✗ Ollama not available: {e}")
        return
    
    print()
    
    # Create collection
    if not create_collection():
        return
    
    # Find processed files
    processed_files = list(DATA_DIR.glob("*.json"))
    print(f"\nFound {len(processed_files)} processed resources to index")
    
    if not processed_files:
        print("No processed files found. Run the crawler first.")
        return
    
    # Index resources
    success_count = 0
    fail_count = 0
    
    for i, file_path in enumerate(processed_files, 1):
        print(f"\n[{i}/{len(processed_files)}] Processing {file_path.name}")
        
        try:
            with open(file_path, 'r') as f:
                resource_data = json.load(f)
            
            if index_resource(resource_data):
                success_count += 1
            else:
                fail_count += 1
            
            # Rate limiting
            time.sleep(0.5)
            
        except Exception as e:
            print(f"  ✗ Error: {e}")
            fail_count += 1
    
    # Summary
    print("\n" + "=" * 80)
    print("INDEXING SUMMARY")
    print("=" * 80)
    print(f"Total resources: {len(processed_files)}")
    print(f"Successfully indexed: {success_count}")
    print(f"Failed: {fail_count}")
    print(f"Collection: {COLLECTION_NAME}")
    
    # Get collection info
    try:
        response = requests.get(f"{QDRANT_URL}/collections/{COLLECTION_NAME}")
        if response.status_code == 200:
            info = response.json()
            points_count = info.get("result", {}).get("points_count", 0)
            print(f"Total points in collection: {points_count}")
    except:
        pass
    
    print("\n✓ Indexing complete!")


if __name__ == "__main__":
    main()

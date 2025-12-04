from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os, uuid, json
from datetime import datetime
from pathlib import Path
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings

PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "/data/chroma")
os.makedirs(PERSIST_DIR, exist_ok=True)

embedder = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path=PERSIST_DIR, settings=Settings(anonymized_telemetry=False))
collection = client.get_or_create_collection(name="ailab_memory")

app = FastAPI(title="AILab Memory")

class MemItem(BaseModel):
    id: str | None = None
    text: str
    metadata: dict | None = None
    tags: list[str] | None = []

class QueryReq(BaseModel):
    query: str
    k: int = 4

@app.post("/store")
def store(item: MemItem):
    item_id = item.id or str(uuid.uuid4())
    emb = embedder.encode(item.text).tolist()
    meta = item.metadata or {}
    meta.update({"ts": datetime.utcnow().isoformat(), "tags": item.tags or []})
    collection.add(ids=[item_id], documents=[item.text], embeddings=[emb], metadatas=[meta])
    return {"id": item_id, "status": "stored"}

@app.post("/query")
def query(req: QueryReq):
    emb = embedder.encode(req.query).tolist()
    res = collection.query(query_embeddings=[emb], n_results=req.k, include=["documents","metadatas","distances"])
    docs = []
    if res and res.get("documents"):
        for d,m,dist in zip(res["documents"][0], res["metadatas"][0], res["distances"][0]):
            docs.append({"doc": d, "meta": m, "distance": dist})
    return {"results": docs}

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os, requests, typing, json

MEMORY_URL = os.getenv("MEMORY_URL", "http://memory:8001")
LLM_API_URL = os.getenv("LLM_API_URL", "")
LLM_API_KEY = os.getenv("LLM_API_KEY", "")
LLM_API_TYPE = os.getenv("LLM_API_TYPE", "openai")  # behavior below uses OpenAI-like POST

app = FastAPI(title="AILab RAG API")

class AskReq(BaseModel):
    prompt: str
    k: int = 4

def query_memory(q: str, k:int=4):
    r = requests.post(f"{MEMORY_URL}/query", json={"query": q, "k": k}, timeout=15)
    if r.status_code != 200:
        raise HTTPException(502, "memory query failed")
    return r.json().get("results", [])

def call_llm(system_prompt: str, user_prompt: str):
    if not LLM_API_URL:
        # fallback: simple echo (safe dev mode)
        return {"text": f"[DEV LLM] {system_prompt}\n\n{user_prompt}"}
    # assume OpenAI-like completion endpoint for v0; adapt as needed
    headers = {"Authorization": f"Bearer {LLM_API_KEY}"} if LLM_API_KEY else {}
    payload = {"model":"gpt-4o-mini","messages":[{"role":"system","content":system_prompt},{"role":"user","content":user_prompt}], "max_tokens":800}
    resp = requests.post(LLM_API_URL, headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
    return resp.json()

@app.post("/ask")
def ask(req: AskReq):
    results = query_memory(req.prompt, req.k)
    context = "\n\n".join([f"- {r['doc'][:600]}" for r in results])
    system_prompt = "You are a concise RAG assistant. Use only the provided context; if unsure, say you don't know."
    user_prompt = f"Context:\n{context}\n\nQuestion: {req.prompt}\n\nAnswer briefly and cite which context bullet you used."
    llm_out = call_llm(system_prompt, user_prompt)
    return {"llm": llm_out, "memory_hits": results}

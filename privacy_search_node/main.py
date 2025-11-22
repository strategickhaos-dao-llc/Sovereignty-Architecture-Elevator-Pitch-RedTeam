from fastapi import FastAPI, Query
from duckduckgo_search import DDGS
import httpx
from bs4 import BeautifulSoup
import json, datetime, os

app = FastAPI(title="Privacy Search Node", description="DuckDuckGo search + page fetch behind unique VPN IP")

def psyche_log(event: str, **kwargs):
    entry = {"timestamp": datetime.datetime.utcnow().isoformat() + "Z", "event": event, **kwargs}
    with open("/logs/events.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")

@app.get("/search")
async def search(q: str = Query(...), max_results: int = 10):
    psyche_log("search_text", query=q, max_results=max_results)
    with DDGS() as ddgs:
        results = [r for r in ddgs.text(q, max_results=max_results)]
    return {"query": q, "results": results}

@app.get("/browse")
async def browse(url: str = Query(...)):
    psyche_log("browse_page", url=url)
    async with httpx.AsyncClient(timeout=30, follow_redirects=True) as client:
        resp = await client.get(url)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "lxml")
        text = soup.get_text(separator="\n", strip=True)
        return {"url": url, "title": soup.title.string if soup.title else "", "text_preview": text[:4000] + "..." if len(text) > 4000 else text}

@app.get("/health")
async def health():
    return {"status": "healthy", "exit_ip": httpx.get("https://api.ipify.org").text}

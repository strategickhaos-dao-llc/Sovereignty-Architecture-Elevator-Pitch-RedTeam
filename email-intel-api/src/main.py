"""
StrategicKhaos Email Intelligence API
Legion of Minds - Sovereign Email Processing Service
Built for GKE deployment with Zapier + Grok integration
"""

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from pydantic import BaseModel
import httpx

# Configuration constants
GROK_API_KEY = os.getenv("GROK_API_KEY", "")
NEXT_ACTION = os.getenv("NEXT_ACTION", "send_to_queen_app")

# HTTP client instance (reused across requests)
http_client: httpx.AsyncClient | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle - create/cleanup HTTP client"""
    global http_client
    http_client = httpx.AsyncClient(timeout=30.0)
    yield
    await http_client.aclose()


app = FastAPI(
    title="StrategicKhaos Email Intelligence",
    lifespan=lifespan
)


class EmailPayload(BaseModel):
    """Email payload from Zapier webhook"""
    email_from: str
    email_subject: str
    email_body: str
    ai_summary: str = ""
    approval_status: str = ""


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "email-intelligence",
        "legion": "minds",
        "sovereign": True
    }


@app.get("/369")
async def tesla_mode():
    """Secret Tesla 369 mode (Grok's idea!)"""
    return {
        "vibe": 369,
        "quote": "If you only knew the magnificence of 3, 6, and 9, "
                 "you would have the key to the universe.",
        "sovereignty_score": 1.0,
        "status": "resonating"
    }


@app.post("/intel")
async def process_intelligence(payload: EmailPayload):
    """
    Main intelligence processing endpoint
    Receives email from Zapier → Grok analysis → structured output
    """

    if not GROK_API_KEY:
        return {
            "error": "GROK_API_KEY not configured",
            "status": "degraded"
        }

    # Prepare Grok prompt
    grok_prompt = f"""
Analyze this email for StrategicKhaos DAO sovereign operations.

From: {payload.email_from}
Subject: {payload.email_subject}
Body: {payload.email_body}

Provide JSON response with:
1. category (academic/business/personal/spam)
2. urgency (low/medium/high)
3. intent (what they want)
4. recommended_actions (list)
5. sovereignty_score (0.0-1.0, how aligned with DAO mission)

Zapier already provided: {payload.ai_summary}
Human decision: {payload.approval_status}
"""

    # Call Grok API
    try:
        response = await http_client.post(
            "https://api.x.ai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROK_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "grok-beta",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are the intelligence processor for "
                                   "a sovereign DAO. Respond in clean JSON."
                    },
                    {
                        "role": "user",
                        "content": grok_prompt
                    }
                ],
                "temperature": 0.3
            }
        )
        response.raise_for_status()
        grok_data = response.json()

        # Extract intelligence with validation
        choices = grok_data.get("choices", [])
        if not choices:
            return {
                "status": "error",
                "error": "No choices in Grok response",
                "fallback_mode": True
            }

        message = choices[0].get("message", {})
        grok_analysis = message.get("content", "")

        if not grok_analysis:
            return {
                "status": "error",
                "error": "Empty content in Grok response",
                "fallback_mode": True
            }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "fallback_mode": True
        }

    # Return structured intelligence
    return {
        "status": "processed",
        "email": {
            "from": payload.email_from,
            "subject": payload.email_subject
        },
        "zapier_summary": payload.ai_summary,
        "human_decision": payload.approval_status,
        "grok_intelligence": grok_analysis,
        "next_action": NEXT_ACTION
    }


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "StrategicKhaos Email Intelligence API",
        "version": "1.0.0",
        "legion": "minds",
        "endpoints": {
            "health": "/health",
            "intelligence": "POST /intel",
            "tesla_mode": "/369"
        }
    }

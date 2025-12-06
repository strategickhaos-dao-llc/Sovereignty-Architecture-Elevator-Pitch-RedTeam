"""
Email Intelligence Service for StrategicKhaos DAO
Receives webhooks from Zapier, processes with Grok API, integrates with Queen App.
"""
import os
import logging
from typing import Optional

from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
import httpx

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("email-intelligence")

app = FastAPI(
    title="Email Intelligence Service",
    description="Sovereign Email Processing for StrategicKhaos DAO",
    version="1.0.0"
)


class EmailPayload(BaseModel):
    """Incoming email payload from Zapier webhook."""
    email_from: Optional[str] = None
    email_subject: Optional[str] = None
    email_body: Optional[str] = None
    ai_summary: Optional[str] = None
    approval_status: Optional[str] = None


class IntelligenceResponse(BaseModel):
    """Response after processing email with Grok API."""
    status: str
    email: Optional[str] = None
    grok_intelligence: Optional[dict] = None
    error: Optional[str] = None


async def call_grok_api(subject: str, body: str) -> dict:
    """
    Call Grok API for intelligence processing.
    
    Args:
        subject: Email subject line
        body: Email body content
        
    Returns:
        dict: Grok API response with analysis
    """
    grok_api_key = os.getenv("GROK_API_KEY")
    if not grok_api_key:
        logger.warning("GROK_API_KEY not set, skipping Grok analysis")
        return {"message": "Grok API key not configured", "analysis": None}
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post(
                "https://api.x.ai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {grok_api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "grok-beta",
                    "messages": [
                        {
                            "role": "user",
                            "content": (
                                f"Analyze this email for StrategicKhaos DAO:\n\n"
                                f"Subject: {subject}\n\n"
                                f"Body: {body}"
                            )
                        }
                    ]
                }
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"Grok API HTTP error: {e.response.status_code}")
            return {"error": f"Grok API error: {e.response.status_code}"}
        except httpx.RequestError as e:
            logger.error(f"Grok API request error: {e}")
            return {"error": f"Grok API request failed: {str(e)}"}


async def send_to_queen(intelligence: dict) -> bool:
    """
    Send processed intelligence to Queen App.
    
    Args:
        intelligence: Processed intelligence from Grok API
        
    Returns:
        bool: True if successfully sent, False otherwise
    """
    queen_api_key = os.getenv("QUEEN_API_KEY")
    queen_api_url = os.getenv("QUEEN_API_URL")
    
    if not queen_api_key or not queen_api_url:
        logger.info("Queen App integration not configured, skipping")
        return False
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post(
                queen_api_url,
                headers={
                    "Authorization": f"Bearer {queen_api_key}",
                    "Content-Type": "application/json"
                },
                json={"intelligence": intelligence}
            )
            response.raise_for_status()
            logger.info("Successfully sent intelligence to Queen App")
            return True
        except httpx.HTTPError as e:
            logger.error(f"Failed to send to Queen App: {e}")
            return False


@app.post("/webhook/email-intelligence", response_model=IntelligenceResponse)
async def process_email(request: Request):
    """
    Receive webhook from Zapier.
    Process with Grok API.
    Send to Queen App.
    """
    try:
        payload_data = await request.json()
        payload = EmailPayload(**payload_data)
    except Exception as e:
        logger.error(f"Invalid payload: {e}")
        raise HTTPException(status_code=400, detail=f"Invalid payload: {str(e)}")
    
    logger.info(f"Processing email: {payload.email_subject}")
    
    # Process with Grok API
    grok_response = await call_grok_api(
        payload.email_subject or "",
        payload.email_body or ""
    )
    
    # Send to Queen App (non-blocking, best effort)
    await send_to_queen(grok_response)
    
    return IntelligenceResponse(
        status="processed",
        email=payload.email_subject,
        grok_intelligence=grok_response
    )


@app.get("/health")
async def health():
    """Health check endpoint for Kubernetes probes."""
    return {"status": "healthy", "service": "email-intelligence"}


@app.get("/ready")
async def ready():
    """Readiness check endpoint for Kubernetes probes."""
    return {"status": "ready", "service": "email-intelligence"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)

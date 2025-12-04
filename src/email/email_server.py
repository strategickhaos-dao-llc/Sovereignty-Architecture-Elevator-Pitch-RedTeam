"""
StrategicKhaos Email Intelligence Service
Sovereign email infrastructure with Grok AI integration
"""

from fastapi import FastAPI, Request, BackgroundTasks
from pydantic import BaseModel
import os
from typing import Optional

import httpx

from .grok_intelligence import GrokEmailProcessor
from .zapier_webhooks import ZapierConnector
from .sendgrid_integration import SendGridClient

app = FastAPI(title="StrategicKhaos Email Service")

# Initialize components
grok_processor = GrokEmailProcessor(api_key=os.getenv("GROK_API_KEY", ""))
zapier = ZapierConnector(webhook_url=os.getenv("ZAPIER_WEBHOOK_URL", ""))
sendgrid = SendGridClient(api_key=os.getenv("SENDGRID_API_KEY", ""))


class InboundEmail(BaseModel):
    """Email received from external source"""
    from_address: str
    to_address: str
    subject: str
    body: str
    headers: dict = {}


class OutboundEmail(BaseModel):
    """Email to send"""
    to: str
    subject: str
    body: str
    from_address: str = "flamekeeper@strategickhaos.net"


@app.post("/webhook/inbound")
async def receive_email(email: InboundEmail, background_tasks: BackgroundTasks):
    """
    Receive inbound email, process with Grok, send to Zapier
    This endpoint gets called by SendGrid Inbound Parse or similar
    """
    print(f"📧 Received email from {email.from_address}: {email.subject}")
    
    # Process email with Grok AI
    background_tasks.add_task(process_email_intelligence, email)
    
    return {"status": "received", "email_id": email.subject}


async def process_email_intelligence(email: InboundEmail):
    """Process email with Grok AI for intelligence extraction"""
    
    # 1. Send to Grok for AI processing
    intelligence = await grok_processor.analyze_email(
        subject=email.subject,
        body=email.body,
        sender=email.from_address
    )
    
    print(f"🧠 Grok Analysis: {intelligence.get('category')}")
    
    # 2. Send to Zapier for your workflow
    zapier_payload = {
        "email_from": email.from_address,
        "email_subject": email.subject,
        "email_body": email.body,
        "grok_analysis": intelligence,
        "action_required": intelligence.get("requires_approval", False)
    }
    
    await zapier.send_to_workflow(zapier_payload)
    
    # 3. If academic intelligence, special handling
    if intelligence.get("category") == "academic":
        await handle_academic_intelligence(email, intelligence)


async def handle_academic_intelligence(email: InboundEmail, intelligence: dict):
    """Special handler for academic emails"""
    
    # Send approval request to you
    approval_email = OutboundEmail(
        to="garza.domenic101@gmail.com",
        subject=f"⚠️ ACADEMIC INTEL: {email.subject}",
        body=f"""
Academic intelligence detected for your sovereign review.

From: {email.from_address}
Subject: {email.subject}

Grok Analysis:
{intelligence.get('summary', 'No summary')}

Reply APPROVE to send to Queen App
Reply NUKE to reject
        """
    )
    
    await sendgrid.send_email(approval_email)


@app.post("/webhook/zapier")
async def zapier_trigger(request: Request):
    """
    Receive webhook from Zapier
    Zapier can trigger email sends, automations, etc.
    """
    payload = await request.json()
    
    action = payload.get("action")
    
    if action == "send_email":
        email = OutboundEmail(**payload.get("email_data", {}))
        result = await sendgrid.send_email(email)
        return {"status": "sent", "result": result}
    
    elif action == "process_approval":
        # Handle your approval/nuke responses
        approval_status = payload.get("response")
        email_id = payload.get("email_id")
        
        if approval_status == "APPROVE":
            # Send to Queen App
            await send_to_queen_app(payload.get("intelligence_data", {}))
        
        return {"status": "processed", "approval": approval_status, "email_id": email_id}
    
    return {"status": "unknown_action"}


@app.post("/api/send")
async def send_email_endpoint(email: OutboundEmail):
    """
    API endpoint to send emails
    Can be called from GitHub Actions or other services
    """
    result = await sendgrid.send_email(email)
    return {"status": "sent", "message_id": result}


@app.get("/health")
async def health_check():
    """Health check for monitoring"""
    return {
        "status": "healthy",
        "service": "StrategicKhaos Email Intelligence",
        "grok_connected": grok_processor.is_connected(),
        "sendgrid_connected": sendgrid.is_connected()
    }


async def send_to_queen_app(intelligence_data: dict):
    """Send approved intelligence to your Queen App"""
    # Integration with your Queen App
    queen_endpoint = os.getenv("QUEEN_APP_URL", "")
    
    if not queen_endpoint:
        print("⚠️ Queen App URL not configured")
        return
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{queen_endpoint}/api/intelligence",
            json=intelligence_data,
            headers={"Authorization": f"Bearer {os.getenv('QUEEN_API_KEY', '')}"}
        )
    
    print(f"👑 Sent to Queen App: {response.status_code}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

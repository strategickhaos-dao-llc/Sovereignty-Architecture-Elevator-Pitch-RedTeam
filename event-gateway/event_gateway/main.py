"""
Event Gateway - FastAPI Main Application

Strategickhaos Sovereignty Architecture - Webhook Router

This gateway provides:
- GitHub webhook processing with HMAC verification
- Alertmanager webhook handling
- Discord notification routing
- Health and metrics endpoints

LLM Directive: Extension points are marked with TODO comments.
When extending this gateway:
1. Add new webhook handlers in separate modules
2. Register routes in the create_app() function
3. Update HMAC verification for new sources
4. Add metrics for observability
"""

import os
import logging
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import JSONResponse

from .hmac_verifier import verify_signature, verify_github_signature
from .github_webhook import handle_github_event
from .alertmanager_endpoint import handle_alertmanager
from .discord_notifier import DiscordNotifier, send_to_discord

logger = logging.getLogger(__name__)

# Configuration from environment
DISCORD_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
GITHUB_WEBHOOK_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET", "")
EVENTS_HMAC_KEY = os.getenv("EVENTS_HMAC_KEY", "")
PORT = int(os.getenv("PORT", "8080"))

# Channel IDs
CHANNEL_IDS = {
    "prs": os.getenv("PRS_CHANNEL_ID", ""),
    "deployments": os.getenv("DEPLOYMENTS_CHANNEL_ID", ""),
    "alerts": os.getenv("ALERTS_CHANNEL_ID", ""),
    "cluster_status": os.getenv("CLUSTER_STATUS_CHANNEL_ID", ""),
}

# Global notifier instance
discord_notifier: DiscordNotifier | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    global discord_notifier
    
    # Startup
    logger.info("Event Gateway starting up...")
    
    if DISCORD_TOKEN:
        discord_notifier = DiscordNotifier(DISCORD_TOKEN, CHANNEL_IDS)
        logger.info("Discord notifier initialized")
    else:
        logger.warning("DISCORD_BOT_TOKEN not set - notifications disabled")
    
    yield
    
    # Shutdown
    logger.info("Event Gateway shutting down...")
    if discord_notifier:
        await discord_notifier.close()


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="Strategickhaos Event Gateway",
        description="Webhook router for the Discord DevOps Control Plane",
        version="0.1.0",
        lifespan=lifespan,
    )
    
    # Register routes
    register_routes(app)
    
    return app


def register_routes(app: FastAPI):
    """Register all API routes."""
    
    @app.get("/health")
    async def health():
        """Health check endpoint."""
        return {"status": "healthy", "service": "event-gateway"}
    
    @app.get("/ready")
    async def ready():
        """Readiness check endpoint."""
        checks = {
            "discord_configured": DISCORD_TOKEN is not None,
            "github_secret_configured": bool(GITHUB_WEBHOOK_SECRET),
        }
        
        all_ready = all(checks.values())
        return JSONResponse(
            status_code=200 if all_ready else 503,
            content={"ready": all_ready, "checks": checks}
        )
    
    @app.post("/webhook/github")
    async def github_webhook(request: Request):
        """
        Handle GitHub webhook events.
        
        Verifies HMAC signature and routes events to appropriate Discord channels.
        
        LLM Directive: Extend this to handle additional GitHub event types.
        Add handlers in github_webhook.py.
        """
        body = await request.body()
        signature = request.headers.get("X-Hub-Signature-256", "")
        
        # Verify signature
        if GITHUB_WEBHOOK_SECRET:
            if not verify_github_signature(body, signature, GITHUB_WEBHOOK_SECRET):
                logger.warning("Invalid GitHub webhook signature")
                raise HTTPException(status_code=401, detail="Invalid signature")
        
        # Get event type
        event_type = request.headers.get("X-GitHub-Event", "unknown")
        delivery_id = request.headers.get("X-GitHub-Delivery", "unknown")
        
        logger.info("GitHub webhook received: event=%s delivery=%s", event_type, delivery_id)
        
        # Parse payload
        try:
            payload = await request.json()
        except Exception as e:
            logger.error("Failed to parse GitHub webhook payload: %s", e)
            raise HTTPException(status_code=400, detail="Invalid JSON payload")
        
        # Handle event
        try:
            message = handle_github_event(event_type, payload)
            
            if message and discord_notifier:
                channel = message.get("channel", "prs")
                await discord_notifier.send_embed(
                    channel=channel,
                    title=message["title"],
                    description=message.get("description", ""),
                    color=message.get("color", 0x2f81f7),
                    fields=message.get("fields", []),
                )
        except Exception as e:
            logger.error("Failed to handle GitHub event: %s", e)
            # Don't fail the webhook - log and continue
        
        return {"status": "ok", "event": event_type}
    
    @app.post("/alert")
    async def alertmanager_webhook(request: Request):
        """
        Handle Alertmanager webhook events.
        
        Routes alerts to the #alerts Discord channel.
        
        LLM Directive: Extend this to:
        - Add severity-based routing
        - Implement alert grouping
        - Add escalation logic
        """
        try:
            payload = await request.json()
        except Exception as e:
            logger.error("Failed to parse Alertmanager payload: %s", e)
            raise HTTPException(status_code=400, detail="Invalid JSON payload")
        
        logger.info("Alertmanager webhook received: %d alerts", len(payload.get("alerts", [])))
        
        # Handle alerts
        try:
            messages = handle_alertmanager(payload)
            
            if discord_notifier:
                for message in messages:
                    await discord_notifier.send_embed(
                        channel="alerts",
                        title=message["title"],
                        description=message.get("description", ""),
                        color=message.get("color", 0xff0000),
                        fields=message.get("fields", []),
                    )
        except Exception as e:
            logger.error("Failed to handle Alertmanager event: %s", e)
        
        return {"status": "ok"}
    
    @app.post("/event")
    async def generic_event(request: Request):
        """
        Handle generic events from internal services.
        
        Requires HMAC signature verification.
        
        LLM Directive: Extend this to handle custom event types
        from your internal services.
        """
        body = await request.body()
        signature = request.headers.get("X-Sig", "")
        
        # Verify signature
        if EVENTS_HMAC_KEY:
            if not verify_signature(body, signature, EVENTS_HMAC_KEY):
                logger.warning("Invalid event signature")
                raise HTTPException(status_code=401, detail="Invalid signature")
        
        try:
            payload = await request.json()
        except Exception as e:
            logger.error("Failed to parse event payload: %s", e)
            raise HTTPException(status_code=400, detail="Invalid JSON payload")
        
        event_type = payload.get("type", "unknown")
        logger.info("Generic event received: type=%s", event_type)
        
        # Route to appropriate channel
        channel = payload.get("channel", "cluster_status")
        
        if discord_notifier:
            await discord_notifier.send_message(
                channel=channel,
                content=f"**{payload.get('service', 'Unknown')}**: {payload.get('message', 'No message')}"
            )
        
        return {"status": "ok", "event_type": event_type}


# Create the application instance
app = create_app()


def main():
    """Main entry point for the Event Gateway."""
    import uvicorn
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='{"timestamp": "%(asctime)s", "level": "%(levelname)s", "service": "event-gateway", "message": "%(message)s"}'
    )
    
    logger.info("Starting Event Gateway on port %d", PORT)
    uvicorn.run(app, host="0.0.0.0", port=PORT)


if __name__ == "__main__":
    main()

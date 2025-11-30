# claude_prime agent - Verification Node
# Use faststream for NATS integration
from fastapi import FastAPI
from faststream.nats import NatsBroker
import os
import json
import httpx

app = FastAPI()
broker = NatsBroker(os.getenv("NATS_URL", "nats://nats:4222"))


@broker.subscriber("board.deliberate")
async def handle_deliberation(msg: dict):
    """Agent-specific logic: verify decisions."""
    decision = {"role": "verification_node", "recommendation": "Verify and approve"}
    # Enforce OPA: Query OPA for guardrails
    if await opa_approve(decision):
        await broker.publish(decision, "board.decisions")
    else:
        await broker.publish({"error": "Guardrail violation"}, "board.alerts")


async def opa_approve(decision: dict) -> bool:
    """Query OPA for guardrail enforcement."""
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(
                "http://opa:8181/v1/data/guardrails/approve",
                json={"input": decision}
            )
            return resp.json().get("result", False)
        except Exception:
            return False


@app.on_event("startup")
async def connect():
    """Connect to NATS broker on startup."""
    await broker.connect()


@app.on_event("shutdown")
async def disconnect():
    """Disconnect from NATS broker on shutdown."""
    await broker.close()


@app.post("/trigger_deliberation")
async def trigger_deliberation(topic: str = "board.deliberate"):
    """External trigger endpoint for deliberation."""
    await broker.publish({"trigger": "manual", "source": "claude_prime"}, topic)
    return {"status": "triggered", "topic": topic}


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy", "role": os.getenv("ROLE", "verification_node")}

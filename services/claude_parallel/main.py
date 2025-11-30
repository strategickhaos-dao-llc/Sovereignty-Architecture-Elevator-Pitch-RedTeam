# claude_parallel agent - Deep Architect
# Use faststream for NATS integration
from contextlib import asynccontextmanager
from fastapi import FastAPI
from faststream.nats import NatsBroker
import os
import json
import httpx

broker = NatsBroker(os.getenv("NATS_URL", "nats://nats:4222"))


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage NATS broker lifecycle."""
    await broker.connect()
    yield
    await broker.close()


app = FastAPI(lifespan=lifespan)


@broker.subscriber("board.deliberate")
async def handle_deliberation(msg: dict):
    """Agent-specific logic: deep architecture analysis."""
    decision = {"role": "deep_architect", "recommendation": "Architecture approved"}
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


@app.post("/trigger_deliberation")
async def trigger_deliberation(topic: str = "board.deliberate"):
    """External trigger endpoint for deliberation."""
    await broker.publish({"trigger": "manual", "source": "claude_parallel"}, topic)
    return {"status": "triggered", "topic": topic}


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy", "role": os.getenv("ROLE", "deep_architect")}

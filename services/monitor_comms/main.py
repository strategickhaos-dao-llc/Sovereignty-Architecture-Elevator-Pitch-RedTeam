# monitor_comms service - Gmail/Drive Monitoring
from contextlib import asynccontextmanager
from fastapi import FastAPI
from faststream.nats import NatsBroker
import asyncio
import os
import json

GOOGLE_CREDENTIALS = os.getenv("GOOGLE_CREDENTIALS", "/secrets/credentials.json")
POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", "300"))

broker = NatsBroker(os.getenv("NATS_URL", "nats://nats:4222"))

# Use asyncio.Event for clean task management
shutdown_event = asyncio.Event()


async def poll_gmail():
    """Poll Gmail for board-relevant messages."""
    # Note: Requires google-api-python-client and valid credentials
    # This is a stub implementation
    try:
        # In production, use:
        # from googleapiclient.discovery import build
        # from google.oauth2.service_account import Credentials
        # creds = Credentials.from_service_account_file(GOOGLE_CREDENTIALS, ...)
        # gmail = build('gmail', 'v1', credentials=creds)
        # results = gmail.users().messages().list(userId='me', q='label:board').execute()
        pass
    except Exception as e:
        await broker.publish(
            {"type": "error", "service": "monitor_comms", "error": str(e)},
            "board.alerts"
        )


async def poll_drive():
    """Poll Google Drive for board-relevant files."""
    # Note: Requires google-api-python-client and valid credentials
    # This is a stub implementation
    try:
        # In production, use:
        # drive = build('drive', 'v3', credentials=creds)
        # results = drive.files().list(...).execute()
        pass
    except Exception as e:
        await broker.publish(
            {"type": "error", "service": "monitor_comms", "error": str(e)},
            "board.alerts"
        )


async def poll_loop():
    """Main polling loop with clean shutdown support."""
    while not shutdown_event.is_set():
        await poll_gmail()
        await poll_drive()
        try:
            await asyncio.wait_for(shutdown_event.wait(), timeout=POLL_INTERVAL)
        except asyncio.TimeoutError:
            pass


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage NATS broker lifecycle and polling task."""
    await broker.connect()
    task = asyncio.create_task(poll_loop())
    yield
    shutdown_event.set()
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass
    await broker.close()


app = FastAPI(lifespan=lifespan)


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "monitor_comms",
        "polling_interval": POLL_INTERVAL,
        "polling_active": not shutdown_event.is_set()
    }


@app.post("/poll")
async def trigger_poll():
    """Manually trigger a poll cycle."""
    await poll_gmail()
    await poll_drive()
    return {"status": "polled"}

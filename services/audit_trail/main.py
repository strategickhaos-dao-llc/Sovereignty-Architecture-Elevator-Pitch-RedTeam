# audit_trail service - Cryptographic Audit Trail
from fastapi import FastAPI
from faststream.nats import NatsBroker
import sqlite3
import os
import json
import hashlib
from datetime import datetime

app = FastAPI()
broker = NatsBroker(os.getenv("NATS_URL", "nats://nats:4222"))

DB_FILE = os.getenv("DB_FILE", "/data/audit.db")
GIT_REPO = os.getenv("GIT_REPO", "/repo")


def init_db():
    """Initialize the audit database."""
    conn = sqlite3.connect(DB_FILE)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            decision TEXT NOT NULL,
            hash TEXT NOT NULL,
            merkle_root TEXT
        )
    """)
    conn.commit()
    conn.close()


def compute_hash(data: str) -> str:
    """Compute SHA256 hash of data."""
    return hashlib.sha256(data.encode()).hexdigest()


def compute_merkle_root(hashes: list) -> str:
    """Compute Merkle root from list of hashes."""
    if not hashes:
        return compute_hash("")
    while len(hashes) > 1:
        if len(hashes) % 2 == 1:
            hashes.append(hashes[-1])
        hashes = [
            compute_hash(hashes[i] + hashes[i + 1])
            for i in range(0, len(hashes), 2)
        ]
    return hashes[0]


@broker.subscriber("board.decisions")
async def log_decision(msg: dict):
    """Log a board decision with cryptographic audit trail."""
    timestamp = datetime.utcnow().isoformat()
    decision_json = json.dumps(msg)
    decision_hash = compute_hash(decision_json)
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Get all existing hashes for Merkle root calculation
    cursor.execute("SELECT hash FROM logs")
    existing_hashes = [row[0] for row in cursor.fetchall()]
    existing_hashes.append(decision_hash)
    merkle_root = compute_merkle_root(existing_hashes)
    
    # Insert the log entry
    cursor.execute(
        "INSERT INTO logs (timestamp, decision, hash, merkle_root) VALUES (?, ?, ?, ?)",
        (timestamp, decision_json, decision_hash, merkle_root)
    )
    conn.commit()
    conn.close()
    
    # Write Merkle root to file for Git anchoring
    merkle_file = os.path.join(GIT_REPO, "audit", "merkle_roots.txt")
    os.makedirs(os.path.dirname(merkle_file), exist_ok=True)
    with open(merkle_file, "a") as f:
        f.write(f"{timestamp},{merkle_root}\n")


@app.on_event("startup")
async def startup():
    """Initialize database and connect to NATS."""
    os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
    init_db()
    await broker.connect()


@app.on_event("shutdown")
async def shutdown():
    """Disconnect from NATS."""
    await broker.close()


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy", "service": "audit_trail"}


@app.get("/logs")
async def get_logs(limit: int = 100):
    """Get recent audit logs."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM logs ORDER BY id DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return {"logs": [
        {"id": r[0], "timestamp": r[1], "decision": json.loads(r[2]), "hash": r[3], "merkle_root": r[4]}
        for r in rows
    ]}

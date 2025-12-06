"""
Honeytrap Flask Application - Sovereignty Architecture Honeypot

This application logs all incoming requests as potential attack vectors,
stores them in GCS, and publishes to Pub/Sub for Legion analysis.
"""

import json
import os
from datetime import datetime
from typing import Any

from flask import Flask, jsonify, request

app = Flask(__name__)

# Configuration from environment
BUCKET = os.getenv("HONEYTRAP_LOG_BUCKET", "honeytrap-attack-logs")
TOPIC = os.getenv(
    "LEGION_PUBSUB_TOPIC",
    "projects/gen-lang-client-0012743775/topics/legion-attack-analysis",
)

# Optional GCP clients (only initialize if available)
storage_client = None
pubsub_client = None

try:
    from google.cloud import pubsub_v1, storage

    storage_client = storage.Client()
    pubsub_client = pubsub_v1.PublisherClient()
except ImportError:
    pass


def log_attack(attack: dict[str, Any]) -> None:
    """Log attack to GCS and publish to Pub/Sub."""
    attack_json = json.dumps(attack)

    # Log to GCS if available
    if storage_client:
        try:
            bucket = storage_client.bucket(BUCKET)
            blob = bucket.blob(f"attacks/{attack['timestamp']}.json")
            blob.upload_from_string(attack_json)
        except Exception as e:
            app.logger.error(f"GCS upload failed: {e}")

    # Publish to Pub/Sub if available
    if pubsub_client:
        try:
            pubsub_client.publish(TOPIC, attack_json.encode())
        except Exception as e:
            app.logger.error(f"Pub/Sub publish failed: {e}")

    # Always log locally
    app.logger.info(f"Attack logged: {attack['path']} from {attack['source_ip']}")


@app.route("/<path:path>", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
def catch_all(path: str):
    """Log all requests as attacks."""
    attack = {
        "timestamp": datetime.utcnow().isoformat(),
        "method": request.method,
        "path": f"/{path}",
        "headers": dict(request.headers),
        "body": request.get_data(as_text=True),
        "source_ip": request.remote_addr,
        "user_agent": request.headers.get("User-Agent"),
    }

    log_attack(attack)

    # Return fake success (honeypot trick)
    return jsonify({"status": "success", "message": "Signal routed"}), 200


@app.route("/health")
def health():
    """Health check endpoint."""
    return jsonify({"status": "operational", "honeypot": True}), 200


@app.route("/")
def root():
    """Root endpoint - also logged as potential attack."""
    attack = {
        "timestamp": datetime.utcnow().isoformat(),
        "method": request.method,
        "path": "/",
        "headers": dict(request.headers),
        "body": "",
        "source_ip": request.remote_addr,
        "user_agent": request.headers.get("User-Agent"),
    }

    log_attack(attack)

    return jsonify({"status": "success", "message": "Welcome to the signal router"}), 200


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

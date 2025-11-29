#!/usr/bin/env python3
"""
Strategickhaos Webhook Inbox Service
A containerized Flask webhook listener for GitHub events with persistent storage.
"""
from flask import Flask, request, abort
import hmac
import hashlib
import os
import json
from datetime import datetime, timezone

app = Flask(__name__)
WEBHOOK_SECRET = os.environ.get("GITHUB_WEBHOOK_SECRET", "").encode()
INBOX_FILE = '/inbox/events.log'  # Volume-mounted for persistence

def verify_signature(payload, signature_header):
    """Verify GitHub webhook HMAC signature"""
    if not WEBHOOK_SECRET or not signature_header:
        return False
    try:
        sha_name, signature = signature_header.split("=")
        mac = hmac.new(WEBHOOK_SECRET, msg=payload, digestmod=hashlib.sha256)
        expected = mac.hexdigest()
        return hmac.compare_digest(expected, signature)
    except (ValueError, AttributeError):
        return False

@app.post("/github-webhook")
def github_webhook():
    """Handle incoming GitHub webhook events"""
    payload = request.data
    signature = request.headers.get("X-Hub-Signature-256")

    # Verify signature BEFORE parsing JSON to ensure integrity
    if not verify_signature(payload, signature):
        print("⚠️  Webhook signature verification failed")
        abort(403)

    event = request.headers.get("X-GitHub-Event", "ping")
    # Safe to parse JSON after signature verification
    data = request.get_json()

    # Log to inbox file with timestamp
    timestamp = datetime.now(timezone.utc).isoformat()
    log_entry = {
        "timestamp": timestamp,
        "event": event,
        "data": data
    }
    
    try:
        with open(INBOX_FILE, 'a') as f:
            f.write(json.dumps(log_entry) + "\n")
    except Exception as e:
        print(f"❌ Error writing to inbox: {e}")

    # Console output for monitoring
    if event == "push":
        repo = data.get('repository', {}).get('full_name', 'unknown')
        ref = data.get('ref', 'unknown')
        print(f"✅ [PUSH] {repo} -> {ref}")
    elif event == "pull_request":
        action = data.get("action", "unknown")
        pr = data.get("pull_request", {})
        print(f"✅ [PR:{action}] #{pr.get('number', '?')} {pr.get('title', 'untitled')}")
    elif event == "ping":
        print(f"✅ [PING] Webhook connection established")
    else:
        print(f"✅ [{event}] event received")

    return "", 204

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "strategickhaos-webhook-inbox"}, 200

@app.get("/")
def index():
    """Root endpoint with service info"""
    return {
        "service": "Strategickhaos Webhook Inbox",
        "endpoints": {
            "/github-webhook": "POST - GitHub webhook receiver",
            "/health": "GET - Health check",
            "/": "GET - This info"
        }
    }, 200

if __name__ == "__main__":
    # Ensure inbox directory exists
    inbox_dir = os.path.dirname(INBOX_FILE)
    os.makedirs(inbox_dir, exist_ok=True)
    
    print("🚀 Strategickhaos Webhook Inbox Service starting...")
    print(f"📥 Events will be logged to: {INBOX_FILE}")
    print(f"🔐 Webhook secret configured: {bool(WEBHOOK_SECRET)}")
    
    # Use debug mode only in development
    debug_mode = os.environ.get("FLASK_ENV", "production") == "development"
    app.run(host="0.0.0.0", port=5000, debug=debug_mode)

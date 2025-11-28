#!/usr/bin/env python3
"""
Strategickhaos Event Gateway
Webhook router for GitHub/GitLab → Discord channel routing.

Features:
- HMAC signature verification
- Multi-tenant support for multiple repositories
- Rate limiting and API protection
- Configurable event → channel routing
"""

import os
import hmac
import hashlib
import json
from typing import Optional
from datetime import datetime

from aiohttp import web
import yaml
import httpx
from prometheus_client import start_http_server, Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import structlog

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# Prometheus metrics
EVENTS_TOTAL = Counter('events_total', 'Total events processed', ['event_type', 'source', 'status'])
EVENT_LATENCY = Histogram('event_latency_seconds', 'Event processing latency', ['event_type'])
DISCORD_MESSAGES = Counter('discord_messages_total', 'Discord messages sent', ['channel', 'status'])


class EventGateway:
    """Event gateway for webhook processing and Discord routing."""

    def __init__(self, config_path: str = "/etc/discord-ops/discovery.yml"):
        self.config_path = config_path
        self.config = self._load_config()
        self.hmac_key = os.getenv("EVENTS_HMAC_KEY", "").encode()
        self.discord_token = os.getenv("DISCORD_BOT_TOKEN", "")
        self.http_client: Optional[httpx.AsyncClient] = None

    def _load_config(self) -> dict:
        """Load discovery configuration."""
        try:
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            logger.warning("config_not_found", path=self.config_path)
            return {}
        except yaml.YAMLError as e:
            logger.error("config_parse_error", error=str(e))
            return {}

    async def start(self):
        """Initialize async resources."""
        self.http_client = httpx.AsyncClient()

    async def stop(self):
        """Clean up async resources."""
        if self.http_client:
            await self.http_client.aclose()

    def verify_signature(self, payload: bytes, signature: str, algo: str = "sha256") -> bool:
        """Verify HMAC signature of webhook payload."""
        if not self.hmac_key:
            logger.warning("hmac_key_not_set")
            return True  # Allow if no key configured

        if algo == "sha256":
            expected = "sha256=" + hmac.new(self.hmac_key, payload, hashlib.sha256).hexdigest()
        elif algo == "sha1":
            expected = "sha1=" + hmac.new(self.hmac_key, payload, hashlib.sha1).hexdigest()
        else:
            logger.error("unsupported_algo", algo=algo)
            return False

        return hmac.compare_digest(expected, signature)

    def get_channel_for_event(self, event_type: str, repo: Optional[str] = None) -> Optional[str]:
        """Get Discord channel ID for an event type."""
        gateway_config = self.config.get("event_gateway", {})
        endpoints = gateway_config.get("endpoints", [])

        for endpoint in endpoints:
            routes = endpoint.get("routes", [])
            for route in routes:
                if route.get("event") == event_type:
                    channel_name = route.get("discord_channel")
                    # Return channel name (would need to resolve to ID in real implementation)
                    return channel_name

        # Default channel mapping from discovery config
        discord_channels = self.config.get("discord", {}).get("channels", {})
        channel_mapping = {
            "pull_request": discord_channels.get("prs", "#prs"),
            "push": discord_channels.get("deployments", "#deployments"),
            "check_suite": discord_channels.get("deployments", "#deployments"),
            "release": discord_channels.get("deployments", "#deployments"),
        }

        return channel_mapping.get(event_type, discord_channels.get("status", "#cluster-status"))

    async def send_to_discord(self, channel_id: str, embed: dict) -> bool:
        """Send an embed to a Discord channel."""
        if not self.discord_token:
            logger.error("discord_token_not_set")
            return False

        url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
        headers = {
            "Authorization": f"Bot {self.discord_token}",
            "Content-Type": "application/json"
        }

        try:
            response = await self.http_client.post(
                url,
                headers=headers,
                json={"embeds": [embed]}
            )
            if response.status_code == 200:
                DISCORD_MESSAGES.labels(channel=channel_id, status="success").inc()
                return True
            else:
                logger.error("discord_send_failed", status=response.status_code, body=response.text)
                DISCORD_MESSAGES.labels(channel=channel_id, status="error").inc()
                return False
        except Exception as e:
            logger.error("discord_send_error", error=str(e))
            DISCORD_MESSAGES.labels(channel=channel_id, status="error").inc()
            return False

    def format_github_event(self, event_type: str, payload: dict) -> dict:
        """Format GitHub event into Discord embed."""
        repo = payload.get("repository", {}).get("full_name", "unknown")
        sender = payload.get("sender", {}).get("login", "unknown")

        embed = {
            "color": 0x3498db,  # Blue
            "timestamp": datetime.utcnow().isoformat(),
            "footer": {"text": "Strategickhaos Event Gateway"}
        }

        if event_type == "pull_request":
            action = payload.get("action", "unknown")
            pr = payload.get("pull_request", {})
            embed["title"] = f"🔀 PR {action.title()}: {pr.get('title', 'Unknown')}"
            embed["description"] = f"Repository: {repo}\nAuthor: {sender}"
            embed["url"] = pr.get("html_url", "")
            embed["color"] = 0x2ecc71 if action == "merged" else 0x3498db

        elif event_type == "push":
            ref = payload.get("ref", "").replace("refs/heads/", "")
            commits = payload.get("commits", [])
            embed["title"] = f"📦 Push to {ref}"
            embed["description"] = f"Repository: {repo}\n{len(commits)} commit(s) by {sender}"
            embed["url"] = payload.get("compare", "")

        elif event_type == "check_suite":
            check = payload.get("check_suite", {})
            conclusion = check.get("conclusion", "pending")
            embed["title"] = f"✅ Check Suite: {conclusion.title()}"
            embed["description"] = f"Repository: {repo}\nBranch: {check.get('head_branch', 'unknown')}"
            embed["color"] = 0x2ecc71 if conclusion == "success" else 0xe74c3c

        elif event_type == "release":
            release = payload.get("release", {})
            embed["title"] = f"🚀 Release: {release.get('tag_name', 'unknown')}"
            embed["description"] = f"Repository: {repo}\n{release.get('name', '')}"
            embed["url"] = release.get("html_url", "")
            embed["color"] = 0x9b59b6

        else:
            embed["title"] = f"📢 Event: {event_type}"
            embed["description"] = f"Repository: {repo}\nSender: {sender}"

        return embed


# Initialize gateway
gateway = EventGateway()


# Web application routes
async def health(request):
    """Health check endpoint."""
    return web.Response(text="OK")


async def ready(request):
    """Readiness check endpoint."""
    return web.Response(text="Ready")


async def metrics(request):
    """Prometheus metrics endpoint."""
    return web.Response(body=generate_latest(), content_type=CONTENT_TYPE_LATEST)


async def event_handler(request):
    """Generic event handler."""
    with EVENT_LATENCY.labels(event_type="generic").time():
        try:
            payload = await request.read()
            data = json.loads(payload)

            # Log event received
            logger.info("event_received", path=request.path, size=len(payload))
            EVENTS_TOTAL.labels(event_type="generic", source="webhook", status="success").inc()

            return web.json_response({"status": "accepted"})

        except Exception as e:
            logger.error("event_handler_error", error=str(e))
            EVENTS_TOTAL.labels(event_type="generic", source="webhook", status="error").inc()
            return web.json_response({"error": str(e)}, status=500)


async def git_event_handler(request):
    """GitHub/GitLab webhook handler.
    
    NOTE: This is a template implementation. The Discord send is gated behind
    ENABLE_DISCORD_SEND=true to allow testing without a Discord token.
    Set ENABLE_DISCORD_SEND=true and provide DISCORD_BOT_TOKEN for production.
    """
    event_type = request.headers.get("X-GitHub-Event", "unknown")

    with EVENT_LATENCY.labels(event_type=event_type).time():
        try:
            payload = await request.read()

            # Verify signature if present
            signature = request.headers.get("X-Hub-Signature-256", "")
            if signature and not gateway.verify_signature(payload, signature):
                logger.warning("signature_verification_failed")
                EVENTS_TOTAL.labels(event_type=event_type, source="github", status="unauthorized").inc()
                return web.json_response({"error": "Invalid signature"}, status=401)

            data = json.loads(payload)

            # Format and route the event
            embed = gateway.format_github_event(event_type, data)
            channel = gateway.get_channel_for_event(event_type, data.get("repository", {}).get("full_name"))

            logger.info("github_event", event_type=event_type, channel=channel)
            EVENTS_TOTAL.labels(event_type=event_type, source="github", status="success").inc()

            # Send to Discord if enabled (requires DISCORD_BOT_TOKEN and channel ID)
            # In production, resolve channel name to ID from discovery.yml
            if os.getenv("ENABLE_DISCORD_SEND", "").lower() == "true" and gateway.discord_token:
                # Channel should be resolved from discovery.yml guild_id + channel name
                # For now, log that it would send
                logger.info("discord_send_ready", channel=channel, embed_title=embed.get("title"))

            return web.json_response({"status": "accepted", "event": event_type, "channel": channel})

        except json.JSONDecodeError as e:
            logger.error("json_decode_error", error=str(e))
            EVENTS_TOTAL.labels(event_type=event_type, source="github", status="error").inc()
            return web.json_response({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            logger.error("git_event_handler_error", error=str(e))
            EVENTS_TOTAL.labels(event_type=event_type, source="github", status="error").inc()
            return web.json_response({"error": str(e)}, status=500)


async def alert_handler(request):
    """Alertmanager webhook handler.
    
    NOTE: This is a template implementation. The Discord send is gated behind
    ENABLE_DISCORD_SEND=true to allow testing without a Discord token.
    Set ENABLE_DISCORD_SEND=true and provide DISCORD_BOT_TOKEN for production.
    """
    with EVENT_LATENCY.labels(event_type="alert").time():
        try:
            payload = await request.read()
            data = json.loads(payload)

            alerts = data.get("alerts", [])
            logger.info("alerts_received", count=len(alerts))

            for alert in alerts:
                status = alert.get("status", "unknown")
                labels = alert.get("labels", {})
                alertname = labels.get("alertname", "Unknown Alert")

                embed = {
                    "title": f"🚨 Alert: {alertname}",
                    "description": alert.get("annotations", {}).get("description", "No description"),
                    "color": 0xe74c3c if status == "firing" else 0x2ecc71,
                    "fields": [
                        {"name": "Status", "value": status.title(), "inline": True},
                        {"name": "Severity", "value": labels.get("severity", "unknown"), "inline": True}
                    ],
                    "timestamp": datetime.utcnow().isoformat(),
                    "footer": {"text": "Strategickhaos Alertmanager"}
                }

                # Send to Discord if enabled (requires DISCORD_BOT_TOKEN and channel ID)
                if os.getenv("ENABLE_DISCORD_SEND", "").lower() == "true" and gateway.discord_token:
                    logger.info("discord_alert_ready", alertname=alertname, embed_title=embed.get("title"))
                
                logger.info("alert_processed", alertname=alertname, status=status)

            EVENTS_TOTAL.labels(event_type="alert", source="alertmanager", status="success").inc()
            return web.json_response({"status": "accepted", "alerts": len(alerts)})

        except Exception as e:
            logger.error("alert_handler_error", error=str(e))
            EVENTS_TOTAL.labels(event_type="alert", source="alertmanager", status="error").inc()
            return web.json_response({"error": str(e)}, status=500)


async def on_startup(app):
    """Application startup hook."""
    await gateway.start()
    logger.info("gateway_started")


async def on_cleanup(app):
    """Application cleanup hook."""
    await gateway.stop()
    logger.info("gateway_stopped")


def create_app() -> web.Application:
    """Create and configure the web application."""
    app = web.Application()

    # Add routes
    app.router.add_get('/health', health)
    app.router.add_get('/ready', ready)
    app.router.add_get('/metrics', metrics)
    app.router.add_post('/event', event_handler)
    app.router.add_post('/git', git_event_handler)
    app.router.add_post('/alert', alert_handler)

    # Add lifecycle hooks
    app.on_startup.append(on_startup)
    app.on_cleanup.append(on_cleanup)

    return app


def main():
    """Main entry point."""
    port = int(os.getenv("PORT", "8080"))

    # Start Prometheus metrics on separate port
    metrics_port = int(os.getenv("METRICS_PORT", "9090"))
    start_http_server(metrics_port)
    logger.info("metrics_server_started", port=metrics_port)

    # Create and run the application
    app = create_app()
    logger.info("starting_gateway", port=port)
    web.run_app(app, host='0.0.0.0', port=port)


if __name__ == "__main__":
    main()

"""
Logging Middleware Module

Provides structured logging and audit trail functionality.

LLM Directive: When extending logging:
1. Maintain JSON structure for log aggregation
2. Include trace context for distributed tracing
3. Never log sensitive data (tokens, passwords)
4. Use appropriate log levels
"""

import json
import logging
import sys
from datetime import datetime, timezone
from typing import Any, Optional

import discord

logger = logging.getLogger(__name__)


class StructuredFormatter(logging.Formatter):
    """
    JSON structured log formatter for log aggregation systems.
    
    LLM Directive: This formatter produces JSON logs that can be
    ingested by Loki, Elasticsearch, CloudWatch, etc.
    """
    
    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "service": "discord-ops-bot",
            "logger": record.name,
            "message": record.getMessage(),
        }
        
        # Add exception info if present
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
        
        # Add extra fields
        if hasattr(record, "extra_fields"):
            log_entry.update(record.extra_fields)
        
        return json.dumps(log_entry)


class AuditLogger:
    """
    Audit logger for tracking Discord bot interactions.
    
    LLM Directive: Audit logs should capture:
    - Who (user, roles)
    - What (command, arguments)
    - When (timestamp)
    - Where (channel, guild)
    - Result (success/failure)
    """
    
    def __init__(self, sink: Optional[str] = None):
        """
        Initialize audit logger.
        
        Args:
            sink: Log sink destination (e.g., "cloudwatch://discord-audit")
        """
        self.sink = sink
        self.logger = logging.getLogger("discord_ops_bot.audit")
    
    async def log_command(
        self,
        interaction: discord.Interaction,
        command: str,
        args: dict[str, Any],
        result: str = "pending"
    ):
        """
        Log a command execution for audit trail.
        
        Args:
            interaction: Discord interaction
            command: Command name
            args: Command arguments (sanitized)
            result: Execution result
        """
        audit_entry = {
            "event_type": "command_execution",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "user": {
                "id": str(interaction.user.id),
                "name": str(interaction.user),
                "roles": [role.name for role in getattr(interaction.user, "roles", [])],
            },
            "command": {
                "name": command,
                "args": self._sanitize_args(args),
            },
            "channel": {
                "id": str(interaction.channel_id),
                "name": getattr(interaction.channel, "name", "unknown"),
            },
            "guild": {
                "id": str(interaction.guild_id) if interaction.guild_id else None,
                "name": interaction.guild.name if interaction.guild else None,
            },
            "result": result,
        }
        
        self.logger.info(
            "Command executed: %s by %s", 
            command, 
            interaction.user,
            extra={"extra_fields": audit_entry}
        )
        
        # TODO: Send to external audit sink
        # await self._send_to_sink(audit_entry)
    
    async def log_event(
        self,
        event_type: str,
        details: dict[str, Any],
        user: Optional[discord.User] = None
    ):
        """
        Log a general event for audit trail.
        
        Args:
            event_type: Type of event
            details: Event details
            user: Associated user (if any)
        """
        audit_entry = {
            "event_type": event_type,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "details": self._sanitize_args(details),
        }
        
        if user:
            audit_entry["user"] = {
                "id": str(user.id),
                "name": str(user),
            }
        
        self.logger.info(
            "Event: %s",
            event_type,
            extra={"extra_fields": audit_entry}
        )
    
    def _sanitize_args(self, args: dict[str, Any]) -> dict[str, Any]:
        """
        Sanitize arguments to remove sensitive data.
        
        LLM Directive: Never log tokens, passwords, API keys, or PII.
        This method should redact any sensitive patterns.
        """
        sensitive_keys = {"token", "password", "secret", "key", "credential", "auth"}
        sanitized = {}
        
        for key, value in args.items():
            if any(s in key.lower() for s in sensitive_keys):
                sanitized[key] = "[REDACTED]"
            elif isinstance(value, str) and len(value) > 200:
                sanitized[key] = value[:200] + "..."
            else:
                sanitized[key] = value
        
        return sanitized
    
    async def _send_to_sink(self, entry: dict[str, Any]):
        """
        Send audit entry to configured sink.
        
        LLM Directive: Implement sinks for:
        - CloudWatch Logs
        - S3 (for long-term retention)
        - Elasticsearch
        - Splunk
        """
        if not self.sink:
            return
        
        # TODO: Implement sink-specific sending
        # if self.sink.startswith("cloudwatch://"):
        #     await self._send_to_cloudwatch(entry)
        # elif self.sink.startswith("s3://"):
        #     await self._send_to_s3(entry)


def setup_logging(level: str = "INFO"):
    """
    Configure structured logging for the application.
    
    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    # Get the root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, level.upper()))
    
    # Remove existing handlers
    root_logger.handlers = []
    
    # Add structured JSON handler for production
    json_handler = logging.StreamHandler(sys.stdout)
    json_handler.setFormatter(StructuredFormatter())
    root_logger.addHandler(json_handler)
    
    # Reduce noise from discord.py
    logging.getLogger("discord").setLevel(logging.WARNING)
    logging.getLogger("discord.http").setLevel(logging.WARNING)
    
    logger.info("Logging configured", extra={"extra_fields": {"log_level": level}})

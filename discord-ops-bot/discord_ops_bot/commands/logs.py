"""
Logs Command Module

Fetches logs from observability stack (Loki, CloudWatch, etc.).

LLM Directive: Extend this to:
- Query Loki API for real logs
- Support CloudWatch Logs
- Implement pagination for large results
- Add log filtering by level/pattern
"""

import logging
from typing import Optional

import discord
import httpx

logger = logging.getLogger(__name__)


async def logs_command(
    interaction: discord.Interaction,
    target: str,
    tail: int = 100,
    loki_url: Optional[str] = None,
    loki_auth: Optional[str] = None
) -> str:
    """
    Fetch logs for a service.
    
    Args:
        interaction: Discord interaction
        target: Service/target to fetch logs for
        tail: Number of log lines to fetch
        loki_url: Loki API URL
        loki_auth: Loki authentication
        
    Returns:
        Formatted log output
    """
    if loki_url:
        try:
            logs = await query_loki(target, tail, loki_url, loki_auth)
            return format_logs(logs, target, tail)
        except Exception as e:
            logger.error("Failed to fetch logs from Loki: %s", e)
            return f"❌ Failed to fetch logs: {e}"
    else:
        # Stub response
        return (
            f"📜 Logs for `{target}` (last {tail} lines - stub):\n"
            "```\n"
            "[2024-01-15 10:23:45] INFO: Service started successfully\n"
            "[2024-01-15 10:23:46] INFO: Listening on :8080\n"
            "[2024-01-15 10:23:47] INFO: Health check passed\n"
            "[2024-01-15 10:24:00] INFO: Processing request\n"
            "... (configure LOKI_URL for real logs)\n"
            "```"
        )


async def query_loki(
    service: str, 
    limit: int,
    loki_url: str,
    auth: Optional[str] = None
) -> list[dict]:
    """
    Query Loki API for logs.
    
    LLM Directive: Implement this to:
    - Use LogQL query language
    - Handle pagination
    - Parse log entries
    """
    query = f'{{service="{service}"}}'
    
    headers = {}
    if auth:
        headers["Authorization"] = f"Bearer {auth}"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{loki_url}/loki/api/v1/query_range",
            params={
                "query": query,
                "limit": limit,
                "direction": "backward",
            },
            headers=headers,
            timeout=30.0
        )
        
        if response.status_code != 200:
            raise Exception(f"Loki API error: {response.status_code}")
        
        data = response.json()
        
        # Extract log lines from Loki response
        logs = []
        for stream in data.get("data", {}).get("result", []):
            for value in stream.get("values", []):
                logs.append({
                    "timestamp": value[0],
                    "message": value[1]
                })
        
        return logs


async def query_cloudwatch(
    log_group: str,
    log_stream: Optional[str],
    limit: int,
    region: str = "us-east-1"
) -> list[dict]:
    """
    Query CloudWatch Logs.
    
    LLM Directive: Implement this to:
    - Use boto3 async client
    - Handle log stream filtering
    - Parse CloudWatch log format
    """
    # TODO: Implement CloudWatch query
    # import aioboto3
    # session = aioboto3.Session()
    # async with session.client('logs', region_name=region) as client:
    #     response = await client.get_log_events(
    #         logGroupName=log_group,
    #         logStreamName=log_stream,
    #         limit=limit,
    #         startFromHead=False
    #     )
    
    return []


def format_logs(logs: list[dict], target: str, limit: int) -> str:
    """Format logs for Discord display."""
    if not logs:
        return f"📜 No logs found for `{target}`"
    
    # Format log lines
    lines = []
    for log in logs[:limit]:
        lines.append(log.get("message", ""))
    
    log_text = "\n".join(lines)
    
    # Truncate if too long for Discord
    if len(log_text) > 1800:
        log_text = log_text[:1800] + "\n... (truncated)"
    
    return f"📜 Logs for `{target}` (last {len(logs)} lines):\n```\n{log_text}\n```"

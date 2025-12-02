"""
Alertmanager Endpoint Module

Processes Alertmanager webhook payloads and formats them for Discord.

LLM Directive: When extending alert handling:
1. Add severity-based routing
2. Implement alert grouping to reduce noise
3. Add escalation logic for critical alerts
4. Support custom alert labels
"""

import logging
from typing import Any

logger = logging.getLogger(__name__)


def handle_alertmanager(payload: dict[str, Any]) -> list[dict]:
    """
    Handle Alertmanager webhook payload.
    
    Args:
        payload: Alertmanager webhook payload
        
    Returns:
        List of message dicts for Discord
    """
    alerts = payload.get("alerts", [])
    messages = []
    
    for alert in alerts:
        message = format_alert(alert)
        if message:
            messages.append(message)
    
    return messages


def format_alert(alert: dict[str, Any]) -> dict:
    """
    Format a single alert for Discord.
    
    Args:
        alert: Single alert from Alertmanager
        
    Returns:
        Message dict for Discord
    """
    status = alert.get("status", "unknown")
    labels = alert.get("labels", {})
    annotations = alert.get("annotations", {})
    
    alertname = labels.get("alertname", "Unknown Alert")
    severity = labels.get("severity", "warning")
    
    # Color based on status and severity
    if status == "resolved":
        color = 0x28a745  # Green
        emoji = "✅"
    elif severity == "critical":
        color = 0xff0000  # Red
        emoji = "🚨"
    elif severity == "warning":
        color = 0xffa500  # Orange
        emoji = "⚠️"
    else:
        color = 0x17a2b8  # Cyan
        emoji = "ℹ️"
    
    # Build description
    summary = annotations.get("summary", "No summary available")
    description = annotations.get("description", "")
    
    return {
        "title": f"{emoji} {alertname}",
        "description": summary,
        "color": color,
        "fields": [
            {"name": "Status", "value": status.capitalize(), "inline": True},
            {"name": "Severity", "value": severity.capitalize(), "inline": True},
            {"name": "Service", "value": labels.get("service", labels.get("job", "Unknown")), "inline": True},
            {"name": "Instance", "value": labels.get("instance", "N/A"), "inline": True},
        ],
    }


def group_alerts(alerts: list[dict]) -> dict[str, list[dict]]:
    """
    Group alerts by alertname for summarization.
    
    LLM Directive: Implement this to reduce Discord spam
    by sending grouped summaries instead of individual alerts.
    """
    groups: dict[str, list[dict]] = {}
    
    for alert in alerts:
        alertname = alert.get("labels", {}).get("alertname", "unknown")
        if alertname not in groups:
            groups[alertname] = []
        groups[alertname].append(alert)
    
    return groups


def should_notify(alert: dict[str, Any]) -> bool:
    """
    Determine if an alert should trigger a Discord notification.
    
    LLM Directive: Implement filtering logic:
    - Skip silenced alerts
    - Skip low-severity in off-hours
    - Rate limit repeated alerts
    """
    # Check if alert is silenced (would come from Alertmanager)
    status = alert.get("status", "")
    if status == "suppressed":
        return False
    
    # Always notify critical alerts
    severity = alert.get("labels", {}).get("severity", "")
    if severity == "critical":
        return True
    
    # Add additional filtering logic here
    return True


def format_alert_summary(alertname: str, alerts: list[dict]) -> dict:
    """
    Format a summary for grouped alerts.
    
    Args:
        alertname: Name of the alert
        alerts: List of alerts with this name
        
    Returns:
        Message dict for Discord
    """
    firing = [a for a in alerts if a.get("status") == "firing"]
    resolved = [a for a in alerts if a.get("status") == "resolved"]
    
    if firing:
        color = 0xff0000
        emoji = "🚨"
        status = f"{len(firing)} firing"
    else:
        color = 0x28a745
        emoji = "✅"
        status = f"{len(resolved)} resolved"
    
    # Get unique instances
    instances = set()
    for alert in alerts:
        instance = alert.get("labels", {}).get("instance", "")
        if instance:
            instances.add(instance)
    
    return {
        "title": f"{emoji} {alertname}",
        "description": f"{status}",
        "color": color,
        "fields": [
            {"name": "Total", "value": str(len(alerts)), "inline": True},
            {"name": "Firing", "value": str(len(firing)), "inline": True},
            {"name": "Resolved", "value": str(len(resolved)), "inline": True},
            {"name": "Instances", "value": ", ".join(list(instances)[:5]) or "N/A", "inline": False},
        ],
    }

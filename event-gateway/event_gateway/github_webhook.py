"""
GitHub Webhook Handler Module

Processes GitHub webhook events and formats them for Discord.

LLM Directive: When adding new event handlers:
1. Add a handler function for the event type
2. Register it in the HANDLERS dict
3. Return a message dict with title, description, color, channel
"""

import logging
from typing import Any, Optional

logger = logging.getLogger(__name__)


def handle_github_event(event_type: str, payload: dict[str, Any]) -> Optional[dict]:
    """
    Handle a GitHub webhook event.
    
    Args:
        event_type: GitHub event type (X-GitHub-Event header)
        payload: Webhook payload
        
    Returns:
        Message dict for Discord or None if event should be ignored
    """
    handler = HANDLERS.get(event_type)
    
    if handler is None:
        logger.debug("No handler for event type: %s", event_type)
        return None
    
    try:
        return handler(payload)
    except Exception as e:
        logger.error("Error handling %s event: %s", event_type, e)
        return None


def handle_pull_request(payload: dict[str, Any]) -> Optional[dict]:
    """Handle pull_request events."""
    action = payload.get("action", "")
    pr = payload.get("pull_request", {})
    repo = payload.get("repository", {})
    
    # Only notify on certain actions
    if action not in ("opened", "closed", "merged", "ready_for_review", "review_requested"):
        return None
    
    # Determine status and color
    if action == "opened":
        title = f"🔄 PR Opened: #{pr.get('number')} {pr.get('title', 'Untitled')}"
        color = 0x6f42c1  # Purple
    elif action == "closed":
        if pr.get("merged"):
            title = f"✅ PR Merged: #{pr.get('number')} {pr.get('title', 'Untitled')}"
            color = 0x28a745  # Green
        else:
            title = f"❌ PR Closed: #{pr.get('number')} {pr.get('title', 'Untitled')}"
            color = 0x6a737d  # Gray
    elif action == "ready_for_review":
        title = f"👀 PR Ready for Review: #{pr.get('number')} {pr.get('title', 'Untitled')}"
        color = 0x0366d6  # Blue
    elif action == "review_requested":
        title = f"📝 Review Requested: #{pr.get('number')} {pr.get('title', 'Untitled')}"
        color = 0xffa500  # Orange
    else:
        title = f"PR {action}: #{pr.get('number')} {pr.get('title', 'Untitled')}"
        color = 0x2f81f7  # Default blue
    
    return {
        "channel": "prs",
        "title": title,
        "description": f"{pr.get('user', {}).get('login', 'Unknown')} → {repo.get('full_name', 'Unknown')}",
        "color": color,
        "fields": [
            {"name": "Branch", "value": pr.get("head", {}).get("ref", "unknown"), "inline": True},
            {"name": "Base", "value": pr.get("base", {}).get("ref", "unknown"), "inline": True},
            {"name": "Link", "value": f"[View PR]({pr.get('html_url', '#')})", "inline": True},
        ],
    }


def handle_push(payload: dict[str, Any]) -> Optional[dict]:
    """Handle push events."""
    ref = payload.get("ref", "")
    repo = payload.get("repository", {})
    commits = payload.get("commits", [])
    
    # Only notify on main/release branches
    if not any(ref.endswith(b) for b in ("/main", "/master", "/develop")) and "/release/" not in ref:
        return None
    
    branch = ref.split("/")[-1]
    commit_count = len(commits)
    
    return {
        "channel": "deployments",
        "title": f"📦 Push to {branch}",
        "description": f"{commit_count} commit(s) to {repo.get('full_name', 'Unknown')}",
        "color": 0x17a2b8,  # Cyan
        "fields": [
            {"name": "Branch", "value": branch, "inline": True},
            {"name": "Commits", "value": str(commit_count), "inline": True},
            {"name": "Compare", "value": f"[View Changes]({payload.get('compare', '#')})", "inline": True},
        ],
    }


def handle_check_suite(payload: dict[str, Any]) -> Optional[dict]:
    """Handle check_suite events."""
    action = payload.get("action", "")
    check_suite = payload.get("check_suite", {})
    repo = payload.get("repository", {})
    
    # Only notify on completion
    if action != "completed":
        return None
    
    conclusion = check_suite.get("conclusion", "unknown")
    
    # Color based on conclusion
    color_map = {
        "success": 0x28a745,
        "failure": 0xff0000,
        "cancelled": 0x6a737d,
        "timed_out": 0xffa500,
        "neutral": 0x6a737d,
    }
    color = color_map.get(conclusion, 0x2f81f7)
    
    # Emoji based on conclusion
    emoji_map = {
        "success": "✅",
        "failure": "❌",
        "cancelled": "⏹️",
        "timed_out": "⏱️",
    }
    emoji = emoji_map.get(conclusion, "🔄")
    
    return {
        "channel": "deployments",
        "title": f"{emoji} Checks {conclusion}",
        "description": f"{check_suite.get('app', {}).get('name', 'Unknown')} on {repo.get('full_name', 'Unknown')}",
        "color": color,
        "fields": [
            {"name": "Conclusion", "value": conclusion, "inline": True},
            {"name": "Branch", "value": check_suite.get("head_branch", "unknown"), "inline": True},
        ],
    }


def handle_release(payload: dict[str, Any]) -> Optional[dict]:
    """Handle release events."""
    action = payload.get("action", "")
    release = payload.get("release", {})
    repo = payload.get("repository", {})
    
    if action not in ("published", "released"):
        return None
    
    return {
        "channel": "deployments",
        "title": f"🚀 Release {release.get('tag_name', 'unknown')}",
        "description": f"New release in {repo.get('full_name', 'Unknown')}",
        "color": 0x28a745,
        "fields": [
            {"name": "Tag", "value": release.get("tag_name", "unknown"), "inline": True},
            {"name": "Prerelease", "value": str(release.get("prerelease", False)), "inline": True},
            {"name": "Link", "value": f"[View Release]({release.get('html_url', '#')})", "inline": True},
        ],
    }


def handle_issue_comment(payload: dict[str, Any]) -> Optional[dict]:
    """Handle issue_comment events."""
    action = payload.get("action", "")
    comment = payload.get("comment", {})
    issue = payload.get("issue", {})
    
    # Only notify on creation
    if action != "created":
        return None
    
    # Only if it's a PR comment
    if "pull_request" not in issue:
        return None
    
    return {
        "channel": "prs",
        "title": f"💬 Comment on PR #{issue.get('number', 'unknown')}",
        "description": f"{comment.get('user', {}).get('login', 'Unknown')}: {comment.get('body', '')[:200]}",
        "color": 0x6f42c1,
        "fields": [
            {"name": "Link", "value": f"[View Comment]({comment.get('html_url', '#')})", "inline": True},
        ],
    }


def handle_workflow_run(payload: dict[str, Any]) -> Optional[dict]:
    """Handle workflow_run events."""
    action = payload.get("action", "")
    workflow_run = payload.get("workflow_run", {})
    repo = payload.get("repository", {})
    
    # Only notify on completion
    if action != "completed":
        return None
    
    conclusion = workflow_run.get("conclusion", "unknown")
    
    color_map = {
        "success": 0x28a745,
        "failure": 0xff0000,
        "cancelled": 0x6a737d,
    }
    color = color_map.get(conclusion, 0x2f81f7)
    
    emoji_map = {
        "success": "✅",
        "failure": "❌",
        "cancelled": "⏹️",
    }
    emoji = emoji_map.get(conclusion, "🔄")
    
    return {
        "channel": "deployments",
        "title": f"{emoji} Workflow: {workflow_run.get('name', 'Unknown')}",
        "description": f"{conclusion} in {repo.get('full_name', 'Unknown')}",
        "color": color,
        "fields": [
            {"name": "Conclusion", "value": conclusion, "inline": True},
            {"name": "Branch", "value": workflow_run.get("head_branch", "unknown"), "inline": True},
            {"name": "Link", "value": f"[View Run]({workflow_run.get('html_url', '#')})", "inline": True},
        ],
    }


# Event type to handler mapping
HANDLERS = {
    "pull_request": handle_pull_request,
    "push": handle_push,
    "check_suite": handle_check_suite,
    "release": handle_release,
    "issue_comment": handle_issue_comment,
    "workflow_run": handle_workflow_run,
}

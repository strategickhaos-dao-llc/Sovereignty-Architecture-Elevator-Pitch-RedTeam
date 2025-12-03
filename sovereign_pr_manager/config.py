"""
SovereignPRManager Configuration Module
Handles configuration loading and environment variables
"""

import os
import yaml
from pathlib import Path
from typing import Any, Dict, Optional
from dataclasses import dataclass, field


@dataclass
class GitHubConfig:
    """GitHub API configuration"""
    token: str = ""
    repo: str = ""
    org: str = ""
    
    @classmethod
    def from_env(cls) -> "GitHubConfig":
        return cls(
            token=os.getenv("GITHUB_TOKEN", ""),
            repo=os.getenv("GITHUB_REPO", ""),
            org=os.getenv("GITHUB_ORG", "Strategickhaos-Swarm-Intelligence"),
        )


@dataclass
class AIConfig:
    """AI API configuration"""
    anthropic_key: str = ""
    openai_key: str = ""
    xai_key: str = ""
    
    @classmethod
    def from_env(cls) -> "AIConfig":
        return cls(
            anthropic_key=os.getenv("ANTHROPIC_API_KEY", ""),
            openai_key=os.getenv("OPENAI_API_KEY", ""),
            xai_key=os.getenv("XAI_API_KEY", ""),
        )


@dataclass
class NATSConfig:
    """NATS message queue configuration"""
    url: str = "nats://localhost:4222"
    subjects: Dict[str, str] = field(default_factory=lambda: {
        "pr_new": "pr.new",
        "pr_review": "pr.review",
        "pr_decision": "pr.decision",
    })


@dataclass
class MergeThresholds:
    """Merge confidence thresholds"""
    auto_merge: float = 0.90  # 90% confidence required
    security_veto: float = 0.80  # Security review below 80% = no merge
    sovereignty_minimum: float = 0.70  # Must meet 70% sovereignty standards


@dataclass
class DiscordConfig:
    """Discord webhook configuration"""
    webhook_url: str = ""
    channels: Dict[str, str] = field(default_factory=lambda: {
        "pr_notifications": "#pr-automation",
        "human_review": "#requires-human",
    })
    
    @classmethod
    def from_env(cls) -> "DiscordConfig":
        return cls(
            webhook_url=os.getenv("DISCORD_WEBHOOK_URL", ""),
        )


@dataclass
class Settings:
    """Complete SovereignPRManager settings"""
    github: GitHubConfig = field(default_factory=GitHubConfig.from_env)
    ai: AIConfig = field(default_factory=AIConfig.from_env)
    nats: NATSConfig = field(default_factory=NATSConfig)
    merge_thresholds: MergeThresholds = field(default_factory=MergeThresholds)
    discord: DiscordConfig = field(default_factory=DiscordConfig.from_env)
    declaration_path: str = ""
    enforce_declaration: bool = True
    poll_interval: int = 10  # seconds
    
    @classmethod
    def load(cls, config_path: Optional[str] = None) -> "Settings":
        """Load settings from config file and environment"""
        settings = cls()
        
        if config_path and Path(config_path).exists():
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
                settings = cls._from_dict(config)
        
        # Override with environment variables
        settings.github = GitHubConfig.from_env()
        settings.ai = AIConfig.from_env()
        settings.discord = DiscordConfig.from_env()
        
        return settings
    
    @classmethod
    def _from_dict(cls, data: Dict[str, Any]) -> "Settings":
        """Create settings from dictionary"""
        github_data = data.get("github", {})
        ai_data = data.get("ai_apis", {})
        nats_data = data.get("nats", {})
        thresholds_data = data.get("merge_thresholds", {})
        discord_data = data.get("discord", {})
        
        return cls(
            github=GitHubConfig(
                token=github_data.get("token", os.getenv("GITHUB_TOKEN", "")),
                repo=github_data.get("repo", ""),
                org=github_data.get("org", ""),
            ),
            ai=AIConfig(
                anthropic_key=ai_data.get("anthropic_key", os.getenv("ANTHROPIC_API_KEY", "")),
                openai_key=ai_data.get("openai_key", os.getenv("OPENAI_API_KEY", "")),
                xai_key=ai_data.get("xai_key", os.getenv("XAI_API_KEY", "")),
            ),
            nats=NATSConfig(
                url=nats_data.get("url", "nats://localhost:4222"),
                subjects=nats_data.get("subjects", {
                    "pr_new": "pr.new",
                    "pr_review": "pr.review",
                    "pr_decision": "pr.decision",
                }),
            ),
            merge_thresholds=MergeThresholds(
                auto_merge=thresholds_data.get("auto_merge", 0.90),
                security_veto=thresholds_data.get("security_veto", 0.80),
                sovereignty_minimum=thresholds_data.get("sovereignty_minimum", 0.70),
            ),
            discord=DiscordConfig(
                webhook_url=discord_data.get("webhook_url", os.getenv("DISCORD_WEBHOOK_URL", "")),
                channels=discord_data.get("channels", {
                    "pr_notifications": "#pr-automation",
                    "human_review": "#requires-human",
                }),
            ),
            declaration_path=data.get("declaration", {}).get("path", ""),
            enforce_declaration=data.get("declaration", {}).get("enforce", True),
            poll_interval=data.get("poll_interval", 10),
        )

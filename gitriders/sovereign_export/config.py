# GitRiders - FlameLang Sovereignty Export System
# Copyright (c) 2025 StrategicKhaos DAO LLC
# Licensed under MIT License
# Date: December 13, 2025

"""
Configuration and policy management for sovereign exports.
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional
import yaml


DEFAULT_CONFIG = {
    "export": {
        "default_encryption": True,
        "require_consent": True,
        "audit_all_operations": True,
    },
    "redaction": {
        "enabled": True,
        "patterns": [
            {"type": "email", "action": "redact"},
            {"type": "phone_number", "action": "redact"},
            {"type": "credit_card", "action": "block"},
            {"type": "ssn", "action": "block"},
        ],
    },
    "providers": {
        "openai": {
            "enabled": True,
            "auth_method": "oauth2",
            "scopes": ["export:read"],
        },
        "anthropic": {
            "enabled": True,
            "auth_method": "oauth2",
            "scopes": ["conversations:read"],
        },
        "google_takeout": {
            "enabled": True,
            "auth_method": "file",
        },
        "xai_grok": {
            "enabled": True,
            "auth_method": "oauth2",
            "scopes": ["chat:read"],
        },
        "perplexity": {
            "enabled": True,
            "auth_method": "oauth2",
            "scopes": ["history:read"],
        },
    },
}


def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Load configuration from file or return defaults.
    
    Args:
        config_path: Path to YAML config file. If None, checks:
                    1. SOVEREIGN_EXPORT_POLICY env var
                    2. ./policy.yaml
                    3. ~/.sovereign-export/policy.yaml
    
    Returns:
        Configuration dictionary
    """
    if config_path is None:
        # Check environment variable
        config_path = os.getenv("SOVEREIGN_EXPORT_POLICY")
        
        if config_path is None:
            # Check local directory
            local_path = Path("policy.yaml")
            if local_path.exists():
                config_path = str(local_path)
            else:
                # Check home directory
                home_path = Path.home() / ".sovereign-export" / "policy.yaml"
                if home_path.exists():
                    config_path = str(home_path)
    
    if config_path and Path(config_path).exists():
        with open(config_path, "r") as f:
            custom_config = yaml.safe_load(f)
            # Merge with defaults
            config = DEFAULT_CONFIG.copy()
            config.update(custom_config)
            return config
    
    return DEFAULT_CONFIG.copy()


def get_keydir() -> Path:
    """
    Get the directory for key storage.
    
    Returns:
        Path to key directory
    """
    keydir = os.getenv("SOVEREIGN_EXPORT_KEYDIR")
    if keydir:
        path = Path(keydir)
    else:
        path = Path.home() / ".sovereign-export" / "keys"
    
    path.mkdir(parents=True, exist_ok=True)
    return path


def validate_config(config: Dict[str, Any]) -> bool:
    """
    Validate configuration structure and values.
    
    Args:
        config: Configuration dictionary
    
    Returns:
        True if valid, raises ValueError if invalid
    """
    required_sections = ["export", "redaction", "providers"]
    for section in required_sections:
        if section not in config:
            raise ValueError(f"Missing required config section: {section}")
    
    # Validate export settings
    export = config["export"]
    if not isinstance(export.get("default_encryption"), bool):
        raise ValueError("export.default_encryption must be boolean")
    if not isinstance(export.get("require_consent"), bool):
        raise ValueError("export.require_consent must be boolean")
    if not isinstance(export.get("audit_all_operations"), bool):
        raise ValueError("export.audit_all_operations must be boolean")
    
    # Validate redaction settings
    redaction = config["redaction"]
    if not isinstance(redaction.get("enabled"), bool):
        raise ValueError("redaction.enabled must be boolean")
    if not isinstance(redaction.get("patterns"), list):
        raise ValueError("redaction.patterns must be a list")
    
    # Validate providers
    providers = config["providers"]
    if not isinstance(providers, dict):
        raise ValueError("providers must be a dictionary")
    
    return True

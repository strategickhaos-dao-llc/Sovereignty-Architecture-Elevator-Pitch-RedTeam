# GitRiders - FlameLang Sovereignty Export System
# Copyright (c) 2025 StrategicKhaos DAO LLC
# Licensed under MIT License
# Date: December 13, 2025

"""
GitRiders Sovereignty Export System

A production-ready system for exporting AI chat conversations with complete
user sovereignty, cryptographic signing, encryption, and audit logging.
"""

__version__ = "1.0.0"
__author__ = "StrategicKhaos DAO LLC"
__license__ = "MIT"

from sovereign_export.manifest import ManifestGenerator, verify_manifest
from sovereign_export.encrypt import EncryptionManager
from sovereign_export.audit import AuditLogger
from sovereign_export.config import load_config

__all__ = [
    "ManifestGenerator",
    "verify_manifest",
    "EncryptionManager",
    "AuditLogger",
    "load_config",
]

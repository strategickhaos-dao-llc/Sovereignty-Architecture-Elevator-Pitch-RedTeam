"""
Legends of Minds - Core Module
Universal orchestrator for unified agent platform
"""

from .orchestrator import app
from .routing import router, RequestRouter

__all__ = ['app', 'router', 'RequestRouter']

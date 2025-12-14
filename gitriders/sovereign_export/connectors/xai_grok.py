# GitRiders - FlameLang Sovereignty Export System
# Copyright (c) 2025 StrategicKhaos DAO LLC
# Licensed under MIT License
# Date: December 13, 2025

"""
xAI Grok connector using official export API.
"""

import os
from typing import Dict, Any, Optional
import requests
from requests_oauthlib import OAuth2Session


class XAIGrokConnector:
    """Connector for xAI Grok exports using delegated OAuth2."""
    
    EXPORT_API_URL = "https://api.x.ai/v1/grok/export"
    AUTH_URL = "https://auth.x.ai/oauth2/authorize"
    TOKEN_URL = "https://auth.x.ai/oauth2/token"
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize xAI Grok connector.
        
        Args:
            api_key: Optional API key (reads from XAI_API_KEY env var if not provided)
        """
        self.api_key = api_key or os.getenv("XAI_API_KEY")
        self.session: Optional[OAuth2Session] = None
    
    def authenticate(self, client_id: str, redirect_uri: str) -> str:
        """
        Initiate OAuth2 authentication flow.
        
        Args:
            client_id: OAuth2 client ID
            redirect_uri: Redirect URI for callback
        
        Returns:
            Authorization URL for user to visit
        """
        self.session = OAuth2Session(
            client_id,
            redirect_uri=redirect_uri,
            scope=["chat:read"]
        )
        authorization_url, state = self.session.authorization_url(self.AUTH_URL)
        return authorization_url
    
    def complete_authentication(self, authorization_response: str) -> None:
        """
        Complete OAuth2 flow with authorization response.
        
        Args:
            authorization_response: Full callback URL with code
        """
        if not self.session:
            raise ValueError("Must call authenticate() first")
        
        self.session.fetch_token(
            self.TOKEN_URL,
            authorization_response=authorization_response
        )
    
    def export_conversations(self) -> Dict[str, Any]:
        """
        Export all conversations using official API.
        
        Returns:
            Export data containing conversations
        """
        if self.api_key:
            return self._export_with_api_key()
        elif self.session:
            return self._export_with_oauth()
        else:
            raise ValueError("No authentication method available")
    
    def _export_with_api_key(self) -> Dict[str, Any]:
        """
        Export using API key (if available).
        
        Returns:
            Export data
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        response = requests.get(self.EXPORT_API_URL, headers=headers)
        response.raise_for_status()
        
        return {
            "provider": "xai_grok",
            "conversations": response.json(),
            "export_method": "api_key"
        }
    
    def _export_with_oauth(self) -> Dict[str, Any]:
        """
        Export using OAuth2 session.
        
        Returns:
            Export data
        """
        if not self.session:
            raise ValueError("OAuth2 session not initialized")
        
        response = self.session.get(self.EXPORT_API_URL)
        response.raise_for_status()
        
        return {
            "provider": "xai_grok",
            "conversations": response.json(),
            "export_method": "oauth2"
        }

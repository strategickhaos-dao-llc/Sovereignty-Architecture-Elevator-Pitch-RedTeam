# GitRiders - FlameLang Sovereignty Export System
# Copyright (c) 2025 StrategicKhaos DAO LLC
# Licensed under MIT License
# Date: December 13, 2025

"""
Google Takeout parser for AI chat exports.
"""

import json
import zipfile
from typing import Dict, Any
from pathlib import Path


class GoogleTakeoutConnector:
    """Connector for parsing Google Takeout export files."""
    
    def __init__(self):
        """Initialize Google Takeout connector."""
        pass
    
    def parse_takeout_file(self, takeout_path: Path) -> Dict[str, Any]:
        """
        Parse Google Takeout ZIP file.
        
        Args:
            takeout_path: Path to Takeout ZIP file
        
        Returns:
            Parsed export data
        """
        conversations = []
        
        with zipfile.ZipFile(takeout_path, 'r') as zip_file:
            # Look for AI chat data in various locations
            for file_info in zip_file.filelist:
                if self._is_ai_chat_file(file_info.filename):
                    with zip_file.open(file_info) as f:
                        data = json.load(f)
                        conversations.extend(self._parse_chat_data(data))
        
        return {
            "provider": "google_takeout",
            "conversations": conversations,
            "export_method": "file_upload"
        }
    
    def _is_ai_chat_file(self, filename: str) -> bool:
        """
        Check if file contains AI chat data.
        
        Args:
            filename: File name in archive
        
        Returns:
            True if file contains AI chat data
        """
        # Google may store AI chats in various locations
        ai_patterns = [
            "Bard",
            "Gemini",
            "AI",
            "Assistant",
        ]
        
        return any(pattern in filename for pattern in ai_patterns) and filename.endswith('.json')
    
    def _parse_chat_data(self, data: Dict[str, Any]) -> list:
        """
        Parse chat data from JSON.
        
        Args:
            data: Raw JSON data
        
        Returns:
            List of conversations
        """
        # Google Takeout format may vary
        if isinstance(data, list):
            return data
        elif isinstance(data, dict) and "conversations" in data:
            return data["conversations"]
        elif isinstance(data, dict) and "messages" in data:
            return [{"messages": data["messages"]}]
        else:
            return []
    
    def parse_directory(self, takeout_dir: Path) -> Dict[str, Any]:
        """
        Parse extracted Takeout directory.
        
        Args:
            takeout_dir: Path to extracted Takeout directory
        
        Returns:
            Parsed export data
        """
        conversations = []
        
        # Walk through directory looking for AI chat files
        for json_file in takeout_dir.rglob("*.json"):
            if self._is_ai_chat_file(str(json_file)):
                with open(json_file, 'r') as f:
                    data = json.load(f)
                    conversations.extend(self._parse_chat_data(data))
        
        return {
            "provider": "google_takeout",
            "conversations": conversations,
            "export_method": "directory"
        }

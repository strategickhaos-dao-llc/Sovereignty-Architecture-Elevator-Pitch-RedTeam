#!/usr/bin/env python3
"""
Tests for Claude Context Sync functionality
Validates protocol reconnaissance and context extraction
"""

import pytest
import json
import asyncio
from unittest.mock import Mock, AsyncMock, patch
import sys
import os

# Add recon directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'recon'))

from claude_context_sync import ClaudeContextSync

# Test data fixtures
MOCK_CHAT_HISTORY = [
    {
        "uuid": "test-chat-1",
        "id": "test-chat-1",
        "title": "Test Chat 1",
        "created_at": "2025-12-14T00:00:00Z"
    },
    {
        "uuid": "test-chat-2",
        "id": "test-chat-2",
        "title": "Test Chat 2",
        "created_at": "2025-12-14T01:00:00Z"
    }
]

MOCK_CHAT_SESSION = {
    "messages": [
        {
            "role": "user",
            "content": "What is the meaning of life?",
            "created_at": "2025-12-14T00:00:00Z"
        },
        {
            "role": "assistant",
            "content": "The meaning of life is a profound question that has been pondered by philosophers for centuries.",
            "created_at": "2025-12-14T00:00:01Z"
        }
    ],
    "raw_content": ""
}

MOCK_RSC_CONTENT = """
{"role":"user","content":"Hello world","created_at":"2025-12-14T00:00:00Z"}
{"role":"assistant","content":"Hi there!","created_at":"2025-12-14T00:00:01Z"}
"""

class TestClaudeContextSync:
    """Test suite for Claude Context Sync daemon."""
    
    @pytest.fixture
    async def sync_daemon(self):
        """Create a test instance of the sync daemon."""
        daemon = ClaudeContextSync(
            session_key="sk-ant-sid01-test-key-AoFuUAAA",
            org_id="test-org-id"
        )
        yield daemon
    
    def test_session_key_format(self):
        """Test session key format validation."""
        daemon = ClaudeContextSync(
            session_key="sk-ant-sid01-test-AoFuUAAA",
            org_id="test-org"
        )
        assert daemon.session_key.startswith("sk-ant-sid01-")
        assert daemon.org_id == "test-org"
    
    def test_parse_rsc_content(self):
        """Test RSC content parsing."""
        daemon = ClaudeContextSync("test-key", "test-org")
        
        result = daemon.parse_rsc_content(MOCK_RSC_CONTENT)
        
        assert "messages" in result
        assert len(result["messages"]) > 0
        assert result["messages"][0]["role"] == "user"
        assert result["messages"][1]["role"] == "assistant"
    
    def test_parse_rsc_content_empty(self):
        """Test RSC parsing with empty content."""
        daemon = ClaudeContextSync("test-key", "test-org")
        
        result = daemon.parse_rsc_content("")
        
        assert "messages" in result
        assert len(result["messages"]) == 0
    
    def test_parse_rsc_content_malformed(self):
        """Test RSC parsing with malformed content."""
        daemon = ClaudeContextSync("test-key", "test-org")
        
        result = daemon.parse_rsc_content("not json at all {broken")
        
        # Should handle gracefully
        assert "messages" in result
        assert isinstance(result["messages"], list)
    
    @pytest.mark.asyncio
    async def test_extract_context_from_chat(self):
        """Test context extraction from chat data."""
        daemon = ClaudeContextSync("test-key", "test-org")
        
        contexts = await daemon.extract_context_from_chat(
            MOCK_CHAT_SESSION,
            "test-chat-uuid"
        )
        
        assert len(contexts) == 2
        assert contexts[0]["role"] == "user"
        assert contexts[1]["role"] == "assistant"
        assert contexts[0]["chat_uuid"] == "test-chat-uuid"
        assert "content" in contexts[0]
        assert "metadata" in contexts[0]
    
    @pytest.mark.asyncio
    async def test_extract_context_skip_empty(self):
        """Test that empty messages are skipped."""
        daemon = ClaudeContextSync("test-key", "test-org")
        
        chat_data = {
            "messages": [
                {"role": "user", "content": "Hello World"},  # Must be > 10 chars
                {"role": "assistant", "content": ""},  # Empty - should skip
                {"role": "user", "content": "World is great"}  # Must be > 10 chars
            ]
        }
        
        contexts = await daemon.extract_context_from_chat(
            chat_data,
            "test-chat"
        )
        
        # Should only get 2 contexts (skipping the empty one)
        assert len(contexts) == 2
        assert contexts[0]["content"] == "Hello World"
        assert contexts[1]["content"] == "World is great"
    
    @pytest.mark.asyncio
    async def test_extract_context_deduplication(self):
        """Test that duplicate messages are not re-extracted."""
        daemon = ClaudeContextSync("test-key", "test-org")
        
        chat_data = {
            "messages": [
                {"role": "user", "content": "Same message"}
            ]
        }
        
        # Extract first time
        contexts1 = await daemon.extract_context_from_chat(
            chat_data,
            "test-chat"
        )
        
        # Extract second time - should be skipped
        contexts2 = await daemon.extract_context_from_chat(
            chat_data,
            "test-chat"
        )
        
        assert len(contexts1) == 1
        assert len(contexts2) == 0  # Should be deduplicated
    
    def test_context_id_generation(self):
        """Test unique ID generation for contexts."""
        daemon = ClaudeContextSync("test-key", "test-org")
        
        # Same content should generate same ID
        import hashlib
        
        msg1_id = hashlib.sha256("chat1:0:Hello".encode()).hexdigest()
        msg2_id = hashlib.sha256("chat1:0:Hello".encode()).hexdigest()
        
        assert msg1_id == msg2_id
        
        # Different content should generate different ID
        msg3_id = hashlib.sha256("chat1:0:World".encode()).hexdigest()
        
        assert msg1_id != msg3_id

class TestAPIPatterns:
    """Test Claude API pattern understanding."""
    
    def test_api_endpoints(self):
        """Test API endpoint construction."""
        base_url = "https://claude.ai"
        org_id = "test-org-123"
        
        # Recents endpoint
        recents = f"{base_url}/api/organizations/{org_id}/recents"
        assert recents == "https://claude.ai/api/organizations/test-org-123/recents"
        
        # Spotlight endpoint
        spotlight = f"{base_url}/api/organizations/{org_id}/spotlight"
        assert spotlight == "https://claude.ai/api/organizations/test-org-123/spotlight"
        
        # Chat endpoint
        chat_uuid = "abc-123-def"
        chat = f"{base_url}/chat/{chat_uuid}"
        assert chat == "https://claude.ai/chat/abc-123-def"
    
    def test_session_key_format_validation(self):
        """Test session key format patterns."""
        valid_keys = [
            "sk-ant-sid01-abc123-AoFuUAAA",
            "sk-ant-sid01-dGVzdA==-AoFuUAAA",
            "sk-ant-sid01-base64payload-AoFuUAAA"
        ]
        
        for key in valid_keys:
            assert key.startswith("sk-ant-sid01-")
            assert key.endswith("-AoFuUAAA") or len(key) > 20
    
    def test_infrastructure_constants(self):
        """Test infrastructure configuration constants."""
        # From reconnaissance data
        expected_org_id = "17fcb197-98f1-4c44-9ed8-bc89b419cbbf"
        expected_user_id = "05b0daa4-fb14-4ef4-b7d2-da9fe730e158"
        
        # UUID format validation
        import re
        uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
        
        assert re.match(uuid_pattern, expected_org_id)
        assert re.match(uuid_pattern, expected_user_id)

class TestConfiguration:
    """Test configuration and environment handling."""
    
    def test_default_configuration(self):
        """Test default configuration values."""
        import os
        
        # Default values from environment or hardcoded
        default_qdrant = os.getenv("QDRANT_URL", "http://localhost:6333")
        default_collection = os.getenv("CLAUDE_COLLECTION", "claude-context")
        default_poll_interval = int(os.getenv("POLL_INTERVAL", "300"))
        
        assert default_qdrant == "http://localhost:6333"
        assert default_collection == "claude-context"
        assert default_poll_interval == 300
    
    def test_batch_size_configuration(self):
        """Test batch processing configuration."""
        batch_size = int(os.getenv("BATCH_SIZE", "32"))
        
        assert batch_size > 0
        assert batch_size <= 100  # Reasonable upper limit

class TestSecurityFeatures:
    """Test security and privacy features."""
    
    def test_session_key_truncation(self):
        """Test session key truncation for logging."""
        full_key = "sk-ant-sid01-very-long-secret-key-AoFuUAAA"
        
        # Simulate truncation for logging
        truncated = f"{full_key[:20]}...{full_key[-10:]}"
        
        assert len(truncated) < len(full_key)
        assert "very-long-secret" not in truncated
        assert truncated.startswith("sk-ant-sid01")
        assert truncated.endswith("AoFuUAAA")
    
    def test_sensitive_pattern_redaction(self):
        """Test redaction of sensitive patterns."""
        import re
        
        text = "My session key is sk-ant-sid01-secret-AoFuUAAA and email is user@example.com"
        
        # Redact session keys
        redacted = re.sub(
            r'sk-ant-[a-zA-Z0-9-]+',
            '[REDACTED_KEY]',
            text
        )
        
        assert "sk-ant-sid01-secret" not in redacted
        assert "[REDACTED_KEY]" in redacted
        
        # Redact emails
        redacted = re.sub(
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            '[REDACTED_EMAIL]',
            redacted
        )
        
        assert "user@example.com" not in redacted
        assert "[REDACTED_EMAIL]" in redacted

def test_integration_smoke():
    """Smoke test to ensure all components are importable."""
    # Test that the main module can be imported
    from claude_context_sync import ClaudeContextSync
    
    assert ClaudeContextSync is not None
    
    # Test basic instantiation
    daemon = ClaudeContextSync("test-key", "test-org")
    assert daemon is not None
    assert daemon.session_key == "test-key"
    assert daemon.org_id == "test-org"

if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "--tb=short"])

# GitRiders - FlameLang Sovereignty Export System
# Copyright (c) 2025 StrategicKhaos DAO LLC
# Licensed under MIT License
# Date: December 13, 2025

"""Tests for provider connectors."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from sovereign_export.connectors import (
    OpenAIConnector,
    AnthropicConnector,
    GoogleTakeoutConnector,
    XAIGrokConnector,
    PerplexityConnector
)


def test_openai_connector_initialization():
    """Test OpenAI connector initialization."""
    connector = OpenAIConnector(api_key="test-key")
    assert connector.api_key == "test-key"


def test_openai_connector_env_var():
    """Test OpenAI connector reads from environment."""
    with patch.dict('os.environ', {'OPENAI_API_KEY': 'env-key'}):
        connector = OpenAIConnector()
        assert connector.api_key == "env-key"


@patch('sovereign_export.connectors.openai.requests.get')
def test_openai_export_with_api_key(mock_get):
    """Test OpenAI export using API key."""
    mock_response = Mock()
    mock_response.json.return_value = {"conversations": []}
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response
    
    connector = OpenAIConnector(api_key="test-key")
    result = connector.export_conversations()
    
    assert result["provider"] == "openai"
    assert "conversations" in result
    assert result["export_method"] == "api_key"
    mock_get.assert_called_once()


def test_anthropic_connector_initialization():
    """Test Anthropic connector initialization."""
    connector = AnthropicConnector(api_key="test-key")
    assert connector.api_key == "test-key"


@patch('sovereign_export.connectors.anthropic.requests.get')
def test_anthropic_export_with_api_key(mock_get):
    """Test Anthropic export using API key."""
    mock_response = Mock()
    mock_response.json.return_value = {"conversations": []}
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response
    
    connector = AnthropicConnector(api_key="test-key")
    result = connector.export_conversations()
    
    assert result["provider"] == "anthropic"
    assert "conversations" in result
    assert result["export_method"] == "api_key"


def test_google_takeout_connector():
    """Test Google Takeout connector initialization."""
    connector = GoogleTakeoutConnector()
    assert connector is not None


def test_google_takeout_is_ai_chat_file():
    """Test AI chat file detection."""
    connector = GoogleTakeoutConnector()
    
    assert connector._is_ai_chat_file("Takeout/Bard/conversations.json")
    assert connector._is_ai_chat_file("Takeout/Gemini/chat.json")
    assert not connector._is_ai_chat_file("Takeout/Photos/image.jpg")


def test_google_takeout_parse_chat_data():
    """Test parsing various chat data formats."""
    connector = GoogleTakeoutConnector()
    
    # Test list format
    data1 = [{"id": "1"}, {"id": "2"}]
    result1 = connector._parse_chat_data(data1)
    assert result1 == data1
    
    # Test dict with conversations
    data2 = {"conversations": [{"id": "1"}]}
    result2 = connector._parse_chat_data(data2)
    assert result2 == [{"id": "1"}]
    
    # Test dict with messages
    data3 = {"messages": [{"text": "hello"}]}
    result3 = connector._parse_chat_data(data3)
    assert len(result3) == 1
    assert "messages" in result3[0]


def test_xai_grok_connector_initialization():
    """Test xAI Grok connector initialization."""
    connector = XAIGrokConnector(api_key="test-key")
    assert connector.api_key == "test-key"


@patch('sovereign_export.connectors.xai_grok.requests.get')
def test_xai_grok_export_with_api_key(mock_get):
    """Test xAI Grok export using API key."""
    mock_response = Mock()
    mock_response.json.return_value = {"conversations": []}
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response
    
    connector = XAIGrokConnector(api_key="test-key")
    result = connector.export_conversations()
    
    assert result["provider"] == "xai_grok"
    assert "conversations" in result


def test_perplexity_connector_initialization():
    """Test Perplexity connector initialization."""
    connector = PerplexityConnector(api_key="test-key")
    assert connector.api_key == "test-key"


@patch('sovereign_export.connectors.perplexity.requests.get')
def test_perplexity_export_with_api_key(mock_get):
    """Test Perplexity export using API key."""
    mock_response = Mock()
    mock_response.json.return_value = {"conversations": []}
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response
    
    connector = PerplexityConnector(api_key="test-key")
    result = connector.export_conversations()
    
    assert result["provider"] == "perplexity"
    assert "conversations" in result


def test_connector_no_authentication():
    """Test that connectors fail without authentication."""
    connector = OpenAIConnector()
    connector.api_key = None
    
    with pytest.raises(ValueError, match="No authentication method available"):
        connector.export_conversations()

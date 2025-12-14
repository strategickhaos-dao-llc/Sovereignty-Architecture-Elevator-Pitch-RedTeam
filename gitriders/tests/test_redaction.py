# GitRiders - FlameLang Sovereignty Export System
# Copyright (c) 2025 StrategicKhaos DAO LLC
# Licensed under MIT License
# Date: December 13, 2025

"""Tests for PII redaction."""

import pytest
from sovereign_export.redaction import RedactionEngine


def test_pii_detection():
    """Test basic PII detection."""
    engine = RedactionEngine()
    
    text = "Contact me at john.doe@example.com or call 555-1234"
    results = engine.detect_pii(text)
    
    # Should detect at least email
    assert len(results) > 0
    assert any(r["type"] == "EMAIL_ADDRESS" for r in results)


def test_redact_email():
    """Test email redaction."""
    engine = RedactionEngine()
    
    text = "My email is john.doe@example.com"
    redacted = engine.redact_text(text, entities=["EMAIL_ADDRESS"])
    
    # Email should be redacted
    assert "john.doe@example.com" not in redacted
    assert "*" in redacted


def test_redact_conversation():
    """Test conversation redaction."""
    engine = RedactionEngine()
    
    conversation = {
        "id": "1",
        "title": "Discussion about john@example.com",
        "messages": [
            {
                "role": "user",
                "content": "Please email me at john@example.com"
            },
            {
                "role": "assistant",
                "content": "I'll send the info to that email address."
            }
        ]
    }
    
    redacted = engine.redact_conversation(conversation)
    
    # Check title is redacted
    assert "john@example.com" not in redacted["title"]
    
    # Check messages are redacted
    assert "john@example.com" not in redacted["messages"][0]["content"]


def test_redaction_report():
    """Test PII detection report generation."""
    engine = RedactionEngine()
    
    data = {
        "conversations": [
            {
                "id": "1",
                "messages": [
                    {
                        "content": "Contact john@example.com or call 555-1234"
                    }
                ]
            }
        ]
    }
    
    report = engine.generate_redaction_report(data)
    
    assert "total_pii_found" in report
    assert "by_type" in report
    assert "by_conversation" in report
    assert report["total_pii_found"] > 0


def test_no_pii_detected():
    """Test handling of text with no PII."""
    engine = RedactionEngine()
    
    text = "This is a simple message with no personal information"
    results = engine.detect_pii(text)
    
    # Should detect nothing or very few items
    assert len(results) == 0 or all(r["score"] < 0.5 for r in results)


def test_redact_structured_content():
    """Test redaction of structured message content."""
    engine = RedactionEngine()
    
    message = {
        "content": {
            "text": "Email: john@example.com",
            "metadata": "User info"
        }
    }
    
    redacted = engine._redact_message(message)
    
    # Structured content should be handled
    assert isinstance(redacted["content"], dict)
    assert "john@example.com" not in redacted["content"]["text"]

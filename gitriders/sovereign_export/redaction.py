# GitRiders - FlameLang Sovereignty Export System
# Copyright (c) 2025 StrategicKhaos DAO LLC
# Licensed under MIT License
# Date: December 13, 2025

"""
PII detection and redaction using Presidio.
"""

from typing import Dict, Any, List, Optional
from presidio_analyzer import AnalyzerEngine, RecognizerRegistry
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig


class RedactionEngine:
    """PII detection and redaction engine using Presidio."""
    
    def __init__(self):
        """Initialize redaction engine."""
        self.analyzer = AnalyzerEngine()
        self.anonymizer = AnonymizerEngine()
        
        # Default PII types to detect
        self.default_entities = [
            "EMAIL_ADDRESS",
            "PHONE_NUMBER",
            "CREDIT_CARD",
            "US_SSN",
            "PERSON",
            "LOCATION",
            "DATE_TIME",
            "IP_ADDRESS",
            "URL",
        ]
    
    def detect_pii(
        self,
        text: str,
        entities: Optional[List[str]] = None,
        language: str = "en"
    ) -> List[Dict[str, Any]]:
        """
        Detect PII in text.
        
        Args:
            text: Text to analyze
            entities: List of entity types to detect (uses defaults if None)
            language: Language code
        
        Returns:
            List of detected PII entities
        """
        entities = entities or self.default_entities
        
        results = self.analyzer.analyze(
            text=text,
            entities=entities,
            language=language
        )
        
        return [
            {
                "type": result.entity_type,
                "start": result.start,
                "end": result.end,
                "score": result.score,
                "text": text[result.start:result.end]
            }
            for result in results
        ]
    
    def redact_text(
        self,
        text: str,
        entities: Optional[List[str]] = None,
        language: str = "en",
        redaction_char: str = "*"
    ) -> str:
        """
        Redact PII from text.
        
        Args:
            text: Text to redact
            entities: List of entity types to redact
            language: Language code
            redaction_char: Character to use for redaction
        
        Returns:
            Redacted text
        """
        entities = entities or self.default_entities
        
        # Analyze text
        results = self.analyzer.analyze(
            text=text,
            entities=entities,
            language=language
        )
        
        # Anonymize text
        anonymized = self.anonymizer.anonymize(
            text=text,
            analyzer_results=results,
            operators={
                "DEFAULT": OperatorConfig("replace", {"new_value": redaction_char * 8})
            }
        )
        
        return anonymized.text
    
    def redact_conversation(
        self,
        conversation: Dict[str, Any],
        entities: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Redact PII from a conversation object.
        
        Args:
            conversation: Conversation dictionary
            entities: List of entity types to redact
        
        Returns:
            Redacted conversation
        """
        redacted = conversation.copy()
        
        # Redact messages
        if "messages" in redacted:
            redacted["messages"] = [
                self._redact_message(msg, entities)
                for msg in redacted["messages"]
            ]
        
        # Redact title if present
        if "title" in redacted:
            redacted["title"] = self.redact_text(redacted["title"], entities)
        
        return redacted
    
    def _redact_message(
        self,
        message: Dict[str, Any],
        entities: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Redact PII from a single message.
        
        Args:
            message: Message dictionary
            entities: List of entity types to redact
        
        Returns:
            Redacted message
        """
        redacted = message.copy()
        
        # Redact content
        if "content" in redacted:
            if isinstance(redacted["content"], str):
                redacted["content"] = self.redact_text(redacted["content"], entities)
            elif isinstance(redacted["content"], dict):
                # Handle structured content
                for key, value in redacted["content"].items():
                    if isinstance(value, str):
                        redacted["content"][key] = self.redact_text(value, entities)
        
        return redacted
    
    def generate_redaction_report(
        self,
        data: Dict[str, Any],
        entities: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Generate a report of PII found in data.
        
        Args:
            data: Export data
            entities: List of entity types to detect
        
        Returns:
            Redaction report
        """
        report = {
            "total_pii_found": 0,
            "by_type": {},
            "by_conversation": []
        }
        
        conversations = data.get("conversations", [])
        
        for conv_idx, conversation in enumerate(conversations):
            conv_report = {
                "conversation_id": conversation.get("id", conv_idx),
                "pii_found": []
            }
            
            # Analyze messages
            if "messages" in conversation:
                for msg in conversation["messages"]:
                    if "content" in msg and isinstance(msg["content"], str):
                        pii_results = self.detect_pii(msg["content"], entities)
                        
                        for pii in pii_results:
                            # Update totals
                            report["total_pii_found"] += 1
                            entity_type = pii["type"]
                            report["by_type"][entity_type] = report["by_type"].get(entity_type, 0) + 1
                            
                            # Add to conversation report
                            conv_report["pii_found"].append(pii)
            
            if conv_report["pii_found"]:
                report["by_conversation"].append(conv_report)
        
        return report

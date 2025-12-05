"""
Redaction engine for partial access scenarios.
Removes or masks sensitive fields based on access policies.
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Set, Union

import structlog

logger = structlog.get_logger()


@dataclass
class RedactedField:
    """Metadata about a redacted field."""
    field_path: str
    reason: str
    policy_id: Optional[str] = None
    original_type: Optional[str] = None


class RedactionEngine:
    """
    Engine for redacting sensitive fields from artifacts.
    Supports nested field paths and configurable redaction markers.
    """

    # Default redaction marker
    REDACTION_MARKER = "[REDACTED]"
    REDACTION_METADATA_KEY = "_redaction_info"

    def __init__(
        self,
        redaction_marker: str = REDACTION_MARKER,
        include_metadata: bool = True,
        preserve_structure: bool = True,
    ):
        """
        Initialize redaction engine.

        Args:
            redaction_marker: String to replace redacted values with
            include_metadata: Whether to include redaction info in output
            preserve_structure: Whether to preserve dict/list structure
        """
        self.redaction_marker = redaction_marker
        self.include_metadata = include_metadata
        self.preserve_structure = preserve_structure

    def redact(
        self,
        data: Dict[str, Any],
        fields_to_redact: List[str],
        reason: str = "access_policy",
        policy_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Redact specified fields from data.

        Args:
            data: Dictionary containing data to redact
            fields_to_redact: List of field paths to redact (supports dot notation)
            reason: Reason for redaction
            policy_id: Optional policy ID that triggered redaction

        Returns:
            Copy of data with specified fields redacted
        """
        if not fields_to_redact:
            return data

        # Deep copy to avoid modifying original
        result = self._deep_copy(data)
        redacted_fields: List[RedactedField] = []

        for field_path in fields_to_redact:
            if self._redact_field(result, field_path, reason, policy_id):
                redacted_fields.append(
                    RedactedField(
                        field_path=field_path,
                        reason=reason,
                        policy_id=policy_id,
                        original_type=self._get_field_type(data, field_path),
                    )
                )

        # Add redaction metadata if configured
        if self.include_metadata and redacted_fields:
            result[self.REDACTION_METADATA_KEY] = {
                "redacted": True,
                "redacted_at": datetime.now(timezone.utc).isoformat(),
                "redacted_fields": [
                    {
                        "path": rf.field_path,
                        "reason": rf.reason,
                        "policy_id": rf.policy_id,
                    }
                    for rf in redacted_fields
                ],
                "total_redacted": len(redacted_fields),
            }

        logger.debug(
            "Applied redaction",
            fields_redacted=len(redacted_fields),
            policy_id=policy_id,
        )

        return result

    def _redact_field(
        self,
        data: Dict[str, Any],
        field_path: str,
        reason: str,
        policy_id: Optional[str],
    ) -> bool:
        """
        Redact a single field by path.

        Returns True if field was found and redacted.
        """
        parts = field_path.split(".")
        current = data

        # Navigate to parent of target field
        for i, part in enumerate(parts[:-1]):
            if isinstance(current, dict) and part in current:
                current = current[part]
            elif isinstance(current, list):
                # Handle list indexing like "items.0.field"
                try:
                    idx = int(part)
                    if 0 <= idx < len(current):
                        current = current[idx]
                    else:
                        return False
                except ValueError:
                    # Redact field in all list items
                    for item in current:
                        if isinstance(item, dict):
                            remaining_path = ".".join(parts[i:])
                            self._redact_field(item, remaining_path, reason, policy_id)
                    return True
            else:
                return False

        # Redact the target field
        target_key = parts[-1]
        if isinstance(current, dict) and target_key in current:
            original_value = current[target_key]
            if self.preserve_structure:
                current[target_key] = self._create_redacted_value(original_value)
            else:
                current[target_key] = self.redaction_marker
            return True

        return False

    def _create_redacted_value(self, original: Any) -> Any:
        """Create redacted value preserving type structure where possible."""
        if isinstance(original, dict):
            return {"_redacted": True, "_type": "object"}
        elif isinstance(original, list):
            return {"_redacted": True, "_type": "array", "_length": len(original)}
        elif isinstance(original, str):
            return self.redaction_marker
        elif isinstance(original, (int, float)):
            return 0
        elif isinstance(original, bool):
            return False
        elif original is None:
            return None
        else:
            return self.redaction_marker

    def _get_field_type(self, data: Dict[str, Any], field_path: str) -> Optional[str]:
        """Get the type of a field by path."""
        parts = field_path.split(".")
        current = data

        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            elif isinstance(current, list):
                try:
                    idx = int(part)
                    if 0 <= idx < len(current):
                        current = current[idx]
                    else:
                        return None
                except ValueError:
                    return "array"
            else:
                return None

        return type(current).__name__

    def _deep_copy(self, data: Any) -> Any:
        """Create a deep copy of data."""
        if isinstance(data, dict):
            return {k: self._deep_copy(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._deep_copy(item) for item in data]
        else:
            return data


# Module-level convenience function
_default_engine: Optional[RedactionEngine] = None


def get_redaction_engine() -> RedactionEngine:
    """Get or create default redaction engine."""
    global _default_engine
    if _default_engine is None:
        _default_engine = RedactionEngine()
    return _default_engine


def redact_artifact(
    artifact: Union[Dict[str, Any], Any],
    fields_to_redact: List[str],
    reason: str = "access_policy",
    policy_id: Optional[str] = None,
) -> Union[Dict[str, Any], Any]:
    """
    Convenience function to redact fields from an artifact.

    Args:
        artifact: The artifact data (dict or Pydantic model)
        fields_to_redact: List of field paths to redact
        reason: Reason for redaction
        policy_id: Optional policy ID

    Returns:
        Artifact with redacted fields
    """
    if not fields_to_redact:
        return artifact

    # Convert Pydantic models to dict
    if hasattr(artifact, "dict"):
        data = artifact.dict()
    elif hasattr(artifact, "model_dump"):
        data = artifact.model_dump()
    elif isinstance(artifact, dict):
        data = artifact
    else:
        # Can't redact non-dict types
        return artifact

    engine = get_redaction_engine()
    return engine.redact(data, fields_to_redact, reason, policy_id)


def create_redacted_preview(
    artifact: Dict[str, Any],
    classification_level: str,
    max_length: int = 100,
) -> Dict[str, Any]:
    """
    Create a redacted preview of an artifact for UI display.

    Shows limited information based on classification level.
    """
    preview = {
        "id": artifact.get("id"),
        "classification": classification_level,
        "preview_available": True,
    }

    # Include title/name if present
    if "title" in artifact:
        preview["title"] = artifact["title"]
    elif "name" in artifact:
        preview["name"] = artifact["name"]
    elif "project_name" in artifact:
        preview["project_name"] = artifact["project_name"]

    # Include truncated description if present
    if "description" in artifact:
        desc = artifact["description"]
        if len(desc) > max_length:
            preview["description"] = desc[:max_length] + "..."
        else:
            preview["description"] = desc

    # Add metadata
    preview["_redacted_preview"] = True
    preview["_full_access_required"] = True

    return preview

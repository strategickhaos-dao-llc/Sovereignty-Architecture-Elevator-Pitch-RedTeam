# opa.py
from dataclasses import dataclass
from typing import Dict, Any, Optional


@dataclass
class OPADecision:
    allow: bool
    redact: bool = False
    reason: Optional[str] = None


class OPAClient:
    """Client for Open Policy Agent decisions."""

    async def decide(self, user: Dict[str, Any], artifact: Dict[str, Any]) -> OPADecision:
        """Make a policy decision based on user and artifact attributes."""
        clearance = user.get("clearance_level", 0)
        classification = artifact.get("classification", "")

        classification_levels = {
            "public": 0,
            "internal": 1,
            "confidential": 2,
            "secret": 3,
            "top_secret": 4,
        }

        required_level = classification_levels.get(classification.lower(), 999)

        if clearance >= required_level:
            return OPADecision(allow=True, redact=False)
        elif clearance >= required_level - 1:
            return OPADecision(allow=False, redact=True, reason="Partial clearance")
        else:
            return OPADecision(allow=False, redact=False, reason="Insufficient clearance")


opa_client = OPAClient()

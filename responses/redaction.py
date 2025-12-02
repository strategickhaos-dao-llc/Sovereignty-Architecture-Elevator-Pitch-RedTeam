# responses/redaction.py
from pydantic import BaseModel


class RedactionResponse(BaseModel):
    id: str
    classification: str
    redacted: bool = True
    reason: str
    visible_preview: str = "Empire Eternal – some truths are above classification"

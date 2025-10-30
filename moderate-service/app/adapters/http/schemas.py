from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.domain.entities import ModerationStatus


class TagResponse(BaseModel):
    id: str
    clip_id: str
    tag_text: str
    timestamp: float
    created_at: datetime
    created_by: str
    status: ModerationStatus
    moderated_by: Optional[str] = None
    moderated_at: Optional[datetime] = None
    moderation_note: Optional[str] = None


class ModerationRequest(BaseModel):
    status: ModerationStatus
    note: Optional[str] = None



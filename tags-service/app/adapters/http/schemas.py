from datetime import datetime
from pydantic import BaseModel
from app.domain.entities import ModerationStatus


class TagCreate(BaseModel):
    clip_id: str
    tag_text: str
    timestamp: float
    created_by: str


class TagUpdate(BaseModel):
    tag_text: str
    timestamp: float


class TagModeration(BaseModel):
    status: ModerationStatus
    moderation_note: str = ""


class TagResponse(BaseModel):
    id: str
    clip_id: str
    tag_text: str
    timestamp: float
    created_at: datetime
    created_by: str
    status: ModerationStatus
    moderated_by: str | None = None
    moderated_at: datetime | None = None
    moderation_note: str | None = None
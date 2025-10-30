from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class ModerationStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class UserRole(str, Enum):
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"


class User(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    username: str
    password_hash: str
    role: UserRole = UserRole.USER
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Tag(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    clip_id: str
    tag_text: str
    timestamp: float  # Timestamp in seconds
    created_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: str  # User who created the tag
    status: ModerationStatus = ModerationStatus.PENDING
    moderated_by: Optional[str] = None
    moderated_at: Optional[datetime] = None
    moderation_note: Optional[str] = None
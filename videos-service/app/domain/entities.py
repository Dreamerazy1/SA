from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, HttpUrl
import uuid


def generate_clip_id() -> str:
    return uuid.uuid4().hex


class Video(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    clip_id: str = Field(default_factory=generate_clip_id)
    url: HttpUrl
    title: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: str | None = None
    # persisted as [], but populated at read time from tags collection
    tags: List[dict] = Field(default_factory=list)



from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, HttpUrl


class VideoCreate(BaseModel):
    url: HttpUrl
    title: str | None = None
    created_by: str | None = None


class VideoResponse(BaseModel):
    clip_id: str
    url: HttpUrl
    title: str | None
    created_at: datetime
    created_by: str | None
    tags: List[dict]



from typing import List, Optional

from app.domain.entities import Video
from app.domain.repositories import VideoRepository


class VideoService:
    def __init__(self, repository: VideoRepository):
        self.repository = repository

    async def create_video(self, url: str, title: str | None, created_by: str | None) -> Video:
        video = Video(url=url, title=title, created_by=created_by)
        return await self.repository.create_video(video)

    async def get_by_clip_id(self, clip_id: str) -> Optional[Video]:
        return await self.repository.get_video_by_clip_id(clip_id)

    async def list_videos(self, limit: int = 100) -> List[Video]:
        return await self.repository.list_videos(limit=limit)



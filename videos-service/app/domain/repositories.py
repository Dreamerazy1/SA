from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities import Video


class VideoRepository(ABC):
    @abstractmethod
    async def create_video(self, video: Video) -> Video:
        pass

    @abstractmethod
    async def get_video_by_clip_id(self, clip_id: str) -> Optional[Video]:
        pass

    @abstractmethod
    async def list_videos(self, limit: int = 100) -> List[Video]:
        pass



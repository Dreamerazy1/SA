from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities import Tag


class TagRepository(ABC):
    @abstractmethod
    async def create_tag(self, tag: Tag) -> Tag:
        pass

    @abstractmethod
    async def get_tags_by_clip_id(self, clip_id: str) -> List[Tag]:
        pass

    @abstractmethod
    async def delete_tag(self, tag_id: str) -> bool:
        pass

    @abstractmethod
    async def get_tag_by_id(self, tag_id: str) -> Optional[Tag]:
        pass

    @abstractmethod
    async def update_tag(self, tag_id: str, tag_data: dict) -> Optional[Tag]:
        pass
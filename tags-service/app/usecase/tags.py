from typing import List, Optional
from app.domain.entities import Tag
from app.domain.repositories import TagRepository


class TagService:
    def __init__(self, tag_repository: TagRepository):
        self.tag_repository = tag_repository

    async def create_tag(self, clip_id: str, tag_text: str, timestamp: float, created_by: str) -> Tag:
        tag = Tag(
            clip_id=clip_id,
            tag_text=tag_text,
            timestamp=timestamp,
            created_by=created_by
        )
        return await self.tag_repository.create_tag(tag)

    async def get_tags_by_clip_id(self, clip_id: str) -> List[Tag]:
        return await self.tag_repository.get_tags_by_clip_id(clip_id)

    async def delete_tag(self, tag_id: str) -> bool:
        return await self.tag_repository.delete_tag(tag_id)

    async def get_tag_by_id(self, tag_id: str) -> Optional[Tag]:
        return await self.tag_repository.get_tag_by_id(tag_id)

    async def update_tag(self, tag_id: str, tag_text: str, timestamp: float) -> Optional[Tag]:
        update_data = {
            "tag_text": tag_text,
            "timestamp": timestamp
        }
        return await self.tag_repository.update_tag(tag_id, update_data)
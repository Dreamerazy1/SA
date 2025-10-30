from typing import List, Optional

from app.domain.entities import Tag, ModerationStatus
from app.adapters.repo.mongo_tag_repo import MongoTagModerationRepository


class ModerationService:
    def __init__(self, tag_repository: MongoTagModerationRepository):
        self.tag_repository = tag_repository

    async def list_pending(self, limit: int = 100) -> List[Tag]:
        return await self.tag_repository.list_pending(limit=limit)

    async def moderate_tag(
        self,
        tag_id: str,
        status: ModerationStatus,
        moderator_username: str,
        note: Optional[str] = None,
    ) -> Optional[Tag]:
        return await self.tag_repository.set_moderation(
            tag_id=tag_id,
            status=status,
            moderator_username=moderator_username,
            note=note,
        )



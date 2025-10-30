from datetime import datetime
from typing import List, Optional
from bson import ObjectId

from app.domain.entities import Tag, ModerationStatus
from app.infrastructure.db import get_database
from pymongo import ReturnDocument


class MongoTagModerationRepository:
    def __init__(self):
        self.db = get_database()
        self.collection = self.db.tags

    async def list_pending(self, limit: int = 100) -> List[Tag]:
        cursor = self.collection.find({"status": ModerationStatus.PENDING.value}).limit(limit)
        items: List[Tag] = []
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])  # bson -> str
            items.append(Tag(**doc))
        return items

    async def get_by_id(self, tag_id: str) -> Optional[Tag]:
        doc = await self.collection.find_one({"_id": ObjectId(tag_id)})
        if not doc:
            return None
        doc["_id"] = str(doc["_id"])  # bson -> str
        return Tag(**doc)

    async def set_moderation(
        self,
        tag_id: str,
        status: ModerationStatus,
        moderator_username: str,
        note: Optional[str] = None,
    ) -> Optional[Tag]:
        update = {
            "status": status.value,
            "moderated_by": moderator_username,
            "moderated_at": datetime.utcnow(),
            "moderation_note": note,
        }
        result = await self.collection.find_one_and_update(
            {"_id": ObjectId(tag_id)},
            {"$set": update},
            return_document=ReturnDocument.AFTER,
        )
        if result:
            result["_id"] = str(result["_id"])  # bson -> str
            return Tag(**result)
        return None



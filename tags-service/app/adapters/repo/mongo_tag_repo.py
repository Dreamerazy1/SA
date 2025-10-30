from typing import List, Optional
from bson import ObjectId

from app.domain.entities import Tag
from app.domain.repositories import TagRepository
from app.infrastructure.db import get_database


class MongoTagRepository(TagRepository):
    def __init__(self):
        self.db = get_database()
        self.collection = self.db.tags

    async def create_tag(self, tag: Tag) -> Tag:
        tag_dict = tag.model_dump(exclude={"id"})
        result = await self.collection.insert_one(tag_dict)
        tag.id = str(result.inserted_id)
        return tag

    async def get_tags_by_clip_id(self, clip_id: str) -> List[Tag]:
        cursor = self.collection.find({"clip_id": clip_id})
        tags = []
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            tags.append(Tag(**doc))
        return tags

    async def delete_tag(self, tag_id: str) -> bool:
        result = await self.collection.delete_one({"_id": ObjectId(tag_id)})
        return result.deleted_count > 0

    async def get_tag_by_id(self, tag_id: str) -> Optional[Tag]:
        doc = await self.collection.find_one({"_id": ObjectId(tag_id)})
        if doc:
            doc["_id"] = str(doc["_id"])
            return Tag(**doc)
        return None

    async def update_tag(self, tag_id: str, tag_data: dict) -> Optional[Tag]:
        result = await self.collection.find_one_and_update(
            {"_id": ObjectId(tag_id)},
            {"$set": tag_data},
            return_document=True
        )
        if result:
            result["_id"] = str(result["_id"])
            return Tag(**result)
        return None
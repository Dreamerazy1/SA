from typing import List, Optional
from bson import ObjectId

from app.domain.entities import Video
from app.domain.repositories import VideoRepository
from app.infrastructure.db import get_database


class MongoVideoRepository(VideoRepository):
    def __init__(self):
        self.db = get_database()
        self.collection = self.db.videos
        self.tags = self.db.tags

    async def create_video(self, video: Video) -> Video:
        doc = video.model_dump(exclude={"id", "tags"})
        # Ensure URL is stored as a plain string (HttpUrl is not BSON-serializable)
        if isinstance(doc.get("url"), str) is False:
            doc["url"] = str(doc["url"])
        # Ensure persisted doc has empty tags array
        doc.setdefault("tags", [])
        result = await self.collection.insert_one(doc)
        video.id = str(result.inserted_id)
        return video

    async def get_video_by_clip_id(self, clip_id: str) -> Optional[Video]:
        doc = await self.collection.find_one({"clip_id": clip_id})
        if not doc:
            return None
        doc["_id"] = str(doc["_id"])  # bson -> str
        # populate tags from tags collection by clip_id
        tag_cursor = self.tags.find({"clip_id": clip_id})
        tag_list = []
        async for t in tag_cursor:
            t["_id"] = str(t["_id"])  # bson -> str
            # keep only relevant fields for the view
            tag_list.append({
                "id": t["_id"],
                "tag_text": t.get("tag_text"),
                "timestamp": t.get("timestamp"),
                "status": t.get("status"),
                "created_by": t.get("created_by"),
            })
        doc["tags"] = tag_list
        return Video(**doc)

    async def list_videos(self, limit: int = 100) -> List[Video]:
        cursor = self.collection.find({}).sort("created_at", -1).limit(limit)
        out: List[Video] = []
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])  # bson -> str
            # populate tags for each video
            tag_cursor = self.tags.find({"clip_id": doc.get("clip_id")})
            tag_list = []
            async for t in tag_cursor:
                t["_id"] = str(t["_id"])  # bson -> str
                tag_list.append({
                    "id": t["_id"],
                    "tag_text": t.get("tag_text"),
                    "timestamp": t.get("timestamp"),
                    "status": t.get("status"),
                    "created_by": t.get("created_by"),
                })
            doc["tags"] = tag_list
            out.append(Video(**doc))
        return out



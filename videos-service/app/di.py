from functools import lru_cache

from app.adapters.repo.mongo_video_repo import MongoVideoRepository
from app.usecase.videos import VideoService


@lru_cache()
def get_video_repository() -> MongoVideoRepository:
    return MongoVideoRepository()


@lru_cache()
def get_video_service() -> VideoService:
    return VideoService(get_video_repository())



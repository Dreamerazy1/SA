from functools import lru_cache

from app.adapters.repo.mongo_user_repo import MongoUserRepository
from app.adapters.repo.mongo_tag_repo import MongoTagModerationRepository
from app.usecase.users import UserService
from app.usecase.moderation import ModerationService


@lru_cache()
def get_user_repository() -> MongoUserRepository:
    return MongoUserRepository()


@lru_cache()
def get_user_service() -> UserService:
    return UserService(get_user_repository())


@lru_cache()
def get_tag_repository() -> MongoTagModerationRepository:
    return MongoTagModerationRepository()


@lru_cache()
def get_moderation_service() -> ModerationService:
    return ModerationService(get_tag_repository())



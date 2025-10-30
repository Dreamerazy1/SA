from functools import lru_cache
from app.adapters.repo.mongo_tag_repo import MongoTagRepository
from app.usecase.tags import TagService
from app.adapters.repo.mongo_user_repo import MongoUserRepository
from app.usecase.users import UserService


@lru_cache()
def get_tag_repository() -> MongoTagRepository:
    return MongoTagRepository()


@lru_cache()
def get_tag_service() -> TagService:
    repository = get_tag_repository()
    return TagService(repository)


@lru_cache()
def get_user_repository() -> MongoUserRepository:
    return MongoUserRepository()


@lru_cache()
def get_user_service() -> UserService:
    repository = get_user_repository()
    return UserService(repository)
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    mongodb_url: str = "mongodb://localhost:27017"
    mongodb_database: str = "tags_db"
    jwt_secret: str = "change-me-in-prod"


@lru_cache()
def get_settings() -> Settings:
    return Settings()

from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # MongoDB connection URL
    # For local: mongodb://localhost:27017
    # For Atlas: mongodb+srv://username:password@cluster.mongodb.net/database?retryWrites=true&w=majority
    mongodb_url: str = "mongodb://localhost:27017"
    mongodb_database: str = "tags_db"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
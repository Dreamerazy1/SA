import motor.motor_asyncio
from app.settings import get_settings

_database = None


def get_database():
    global _database
    if not _database:
        settings = get_settings()
        client = motor.motor_asyncio.AsyncIOMotorClient(settings.mongodb_url)
        _database = client[settings.mongodb_database]
    return _database
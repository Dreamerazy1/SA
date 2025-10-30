from typing import Optional
from bson import ObjectId

from app.domain.entities import User
from app.domain.user_repository import UserRepository
from app.infrastructure.db import get_database


class MongoUserRepository(UserRepository):
    def __init__(self):
        self.db = get_database()
        self.collection = self.db.users

    async def create_user(self, user: User) -> User:
        user_dict = user.model_dump(exclude={"id"})
        result = await self.collection.insert_one(user_dict)
        user.id = str(result.inserted_id)
        return user

    async def get_user_by_username(self, username: str) -> Optional[User]:
        doc = await self.collection.find_one({"username": username})
        if doc:
            doc["_id"] = str(doc["_id"])
            return User(**doc)
        return None

    async def update_user(self, user_id: str, user_data: dict) -> Optional[User]:
        result = await self.collection.find_one_and_update(
            {"_id": ObjectId(user_id)},
            {"$set": user_data},
            return_document=True
        )
        if result:
            result["_id"] = str(result["_id"])
            return User(**result)
        return None
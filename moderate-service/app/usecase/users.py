from typing import Optional

from app.domain.entities import User
from app.domain.user_repository import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def create_user(self, user: User) -> User:
        return await self.user_repository.create_user(user)

    async def get_user_by_username(self, username: str) -> Optional[User]:
        return await self.user_repository.get_user_by_username(username)

    async def update_user(self, user_id: str, user_data: dict) -> Optional[User]:
        return await self.user_repository.update_user(user_id, user_data)



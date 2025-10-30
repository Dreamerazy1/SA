from pydantic import BaseModel
from app.domain.entities import UserRole


class UserCreate(BaseModel):
    username: str
    password: str
    role: UserRole = UserRole.USER


class UserResponse(BaseModel):
    id: str
    username: str
    role: UserRole


class Token(BaseModel):
    access_token: str
    token_type: str



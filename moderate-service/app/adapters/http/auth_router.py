from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.adapters.http.auth_schemas import UserCreate, UserResponse, Token
from app.domain.entities import User, UserRole
from app.infrastructure.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    verify_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
from app.di import get_user_service
from app.usecase.users import UserService


router = APIRouter(prefix="/auth")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


@router.post("/register", response_model=UserResponse)
async def register(
    user_create: UserCreate,
    user_service: UserService = Depends(get_user_service)
):
    existing_user = await user_service.get_user_by_username(user_create.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    user = User(
        username=user_create.username,
        password_hash=get_password_hash(user_create.password),
        role=user_create.role
    )
    created_user = await user_service.create_user(user)
    return UserResponse(
        id=created_user.id,
        username=created_user.username,
        role=created_user.role
    )


@router.post("/token", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_service: UserService = Depends(get_user_service)
):
    user = await user_service.get_user_by_username(form_data.username)
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role},
        expires_delta=access_token_expires,
    )
    return Token(access_token=access_token, token_type="bearer")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_service: UserService = Depends(get_user_service)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = verify_token(token)
    if not payload:
        raise credentials_exception

    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception

    user = await user_service.get_user_by_username(username)
    if user is None:
        raise credentials_exception

    return user


async def get_current_moderator(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role not in [UserRole.MODERATOR, UserRole.ADMIN]:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions",
        )
    return current_user



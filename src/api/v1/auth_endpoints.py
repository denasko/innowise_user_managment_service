from typing import Any

from fastapi import Depends, Form, APIRouter, UploadFile, File
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import EmailStr

from src.core.database.models.user import User
from src.core.dependencies import (
    get_authorization_service,
    get_user_service,
    get_user_from_token,
    get_token_service,
    get_rabbitmq_service,
)
from src.core.schemas.token import TokenInfo
from src.core.schemas.user import UserRead
from src.services.authorization_service import AuthService
from src.services.rabbitmq_service import RabbitMQService
from src.services.token_sevice import TokenService
from src.services.user_service import UserService
from src.core.schemas.validate_create_user_shemas import CreateUser

auth_router = APIRouter(prefix="/auth")


@auth_router.post("/login", response_model=TokenInfo)
async def login(
    username: str = Form(),
    password: str = Form(),
    auth_service: AuthService = Depends(get_authorization_service),
):
    return await auth_service.login(username=username, password=password)


@auth_router.post("/signup", response_model=UserRead)
async def create_new_user(
    new_user: CreateUser = Depends(),
    user_photo: UploadFile = File(...),
    user_service: UserService = Depends(get_user_service),
):
    return await user_service.create_new_user(
        new_user=CreateUser.new_user_to_pydantic_schema(new_user=new_user),
        user_photo=user_photo,
    )


@auth_router.get("/refresh-token", response_model=TokenInfo)
async def auth_refresh_jwt(
    current_user: User = Depends(get_user_from_token),
    token_service: TokenService = Depends(get_token_service),
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
):
    return await token_service.refresh_token(current_user=current_user, credentials=credentials)


@auth_router.post("/auth/reset-password")
async def reset_password(email: EmailStr, rabbitmq_service: RabbitMQService = Depends(get_rabbitmq_service)) -> Any:
    return await rabbitmq_service.create_message_to_rabbitmq(queue="reset-password-stream", email=email)

from fastapi import Depends, Form, APIRouter
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.core.database.models.user import User
from src.core.dependencies import (
    get_authorization_service,
    get_user_service,
    get_user_from_token,
    get_token_service,
)
from src.core.schemas.token import TokenInfo
from src.core.schemas.user import UserCreate, UserRead
from src.services.authorization_service import AuthService
from src.services.token_sevice import TokenService
from src.services.user_service import UserService

auth_router = APIRouter(prefix="/auth")


@auth_router.post("/login", response_model=TokenInfo)
async def login(
    username: str = Form(),
    password: str = Form(),
    auth_service: AuthService = Depends(get_authorization_service),
):
    return await auth_service.login(username=username, password=password)


@auth_router.post("/signup", response_model=UserRead)
async def create_new_user(new_user: UserCreate, user_service: UserService = Depends(get_user_service)):
    return await user_service.create_new_user(new_user=new_user)


@auth_router.get("/refresh-token", response_model=TokenInfo)
async def auth_refresh_jwt(
    current_user: User = Depends(get_user_from_token),
    token_service: TokenService = Depends(get_token_service),
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
):
    return token_service.refresh_token(current_user=current_user, credentials=credentials)

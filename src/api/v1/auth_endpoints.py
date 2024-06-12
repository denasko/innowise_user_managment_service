from fastapi import Depends, Form, APIRouter

from src.core.dependencies import get_authorization_service, get_user_service
from src.core.schemas.token import TokenInfo
from src.core.schemas.user import UserCreate, UserRead
from src.services.authorization_service import AuthService
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

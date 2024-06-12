from typing import Any

from fastapi import Depends, APIRouter
from fastapi.security import HTTPAuthorizationCredentials

from src.api.v1.bearer import bearer
from src.core.dependencies import get_user_service
from src.core.schemas.user import UserUpdate, UserRead
from src.services.user_service import UserService

user_router = APIRouter(prefix="/user")


@user_router.patch("/me", response_model=UserUpdate)
async def edit_user(
    user_update: UserUpdate,
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
    user_service: UserService = Depends(get_user_service),
):
    return await user_service.update_current_user(user_update=user_update, credentials=credentials)


@user_router.get("/me", response_model=UserRead)
async def read_current_user(
    user_service: UserService = Depends(get_user_service),
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
):
    return await user_service.read_current_user(credentials=credentials)


@user_router.delete("/me")
async def delete_user(
    user_service: UserService = Depends(get_user_service),
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
) -> Any:
    return await user_service.delete_current_user(credentials=credentials)

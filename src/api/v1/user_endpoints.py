from typing import Any

from fastapi import Depends, APIRouter
from fastapi.security import HTTPBearer

from src.core.database.models.user import User
from src.core.dependencies import get_user_service, get_user_from_token
from src.core.schemas.user import UserRead
from src.services.user_service import UserService

user_router = APIRouter(prefix="/user", dependencies=[Depends(HTTPBearer)])


@user_router.patch("/me", response_model=UserRead)
async def edit_current_user(
    user_update: UserRead,
    current_user: User = Depends(get_user_from_token),
    user_service: UserService = Depends(get_user_service),
):
    return await user_service.update_current_user(user_update=user_update, current_user=current_user)


@user_router.get("/me", response_model=UserRead)
async def read_current_user(
    current_user: User = Depends(get_user_from_token),
):
    return current_user


@user_router.delete("/me")
async def delete_current_user(
    user_service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_user_from_token),
) -> Any:
    return await user_service.delete_current_user(current_user=current_user)

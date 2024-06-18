from typing import Any, Optional, Sequence
from uuid import UUID

from fastapi import Depends, APIRouter
from fastapi.security import HTTPBearer
from pydantic import PositiveInt

from src.core.database.enums.sorting import OrderBY, SortBY
from src.core.database.models.user import User
from src.core.dependencies import get_user_service, get_user_from_token
from src.core.schemas.user import UserRead, UserUpdate
from src.services.user_service import UserService

user_router = APIRouter(prefix="/user", dependencies=[Depends(HTTPBearer())])


@user_router.patch("/me", response_model=UserRead)
async def edit_current_user(
    user_update: UserUpdate,
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


@user_router.get("/users", response_model=Sequence[UserRead])
async def get_collection_of_users(
    page: PositiveInt = 1,
    limit: PositiveInt = 10,
    filter_by_name: Optional[str] = None,
    sort_by: Optional[str] = SortBY.NAME,
    order_by: Optional[str] = OrderBY.DESC,
    current_user: User = Depends(get_user_from_token),
    user_service: UserService = Depends(get_user_service),
):
    return await user_service.get_collection_of_users(
        current_user=current_user,
        page=page,
        limit=limit,
        filter_by_name=filter_by_name,
        sort_by=sort_by,
        order_by=order_by,
    )


@user_router.get("/{user_id}", response_model=UserRead)
async def read_target_user_by_id(
    user_id: UUID,
    current_user: User = Depends(get_user_from_token),
    user_service: UserService = Depends(get_user_service),
):
    return await user_service.get_target_user_with_permissions(current_user=current_user, target_user_id=user_id)


@user_router.patch("/{user_id}", response_model=UserRead)
async def edit_target_user_by_id(
    user_id: UUID,
    user_update: UserUpdate,
    current_user: User = Depends(get_user_from_token),
    user_service: UserService = Depends(get_user_service),
):
    return await user_service.update_another_user_by_id(
        target_user_id=user_id,
        target_user_updated_fields=user_update,
        current_user=current_user,
    )

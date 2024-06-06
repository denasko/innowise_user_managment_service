from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database.database import get_session
from src.core.schemas.schemas import UserUpdate, UserBase
from src.managers.user import user_manager
from src.services.validations import get_current_auth_not_blocked_user

patch_me = APIRouter(
    prefix="/me",
    tags=[
        "Test authentication",
    ],
)


@patch_me.patch("")
async def edit_user(
    user_update: UserUpdate,
    user: UserBase = Depends(get_current_auth_not_blocked_user),
    session: AsyncSession = Depends(get_session),
) -> UserBase:
    return await user_manager.edit_user(current_user=user, user_update=user_update, session=session)

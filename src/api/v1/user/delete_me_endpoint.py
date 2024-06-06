from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database.database import get_session
from src.services.validations import get_current_auth_not_blocked_user
from src.core.schemas.schemas import UserRead
from src.managers.user import user_manager

delete_me = APIRouter(
    prefix="/me",
    tags=[
        "Test authentication",
    ],
)


@delete_me.delete("")
async def auth_user_check_self_info(
    user: UserRead = Depends(get_current_auth_not_blocked_user),
    session: AsyncSession = Depends(get_session),
) -> dict:
    return await user_manager.delete_user(user_to_delete=user, session=session)

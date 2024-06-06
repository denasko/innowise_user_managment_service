from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database.database import get_session
from src.core.schemas.schemas import UserCreate
from src.managers.user import user_manager

signup_router = APIRouter(
    prefix="/signup",
    tags=[
        "Test authentication",
    ],
)


@signup_router.post("")
async def create_new_user(new_user: UserCreate, session: AsyncSession = Depends(get_session)) -> UserCreate:
    return await user_manager.create_user(new_user=new_user, session=session)

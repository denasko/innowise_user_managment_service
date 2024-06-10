from fastapi import Depends

from src.core.database.models.user import User
from src.core.dependencies import get_user_service
from src.core.schemas.user import UserCreate, UserRead
from src.services.user_service import UserService
from src.api.v1.auth import auth_router


@auth_router.post("/signup", response_model=UserRead)
async def create_new_user(new_user: UserCreate, user_service: UserService = Depends(get_user_service)) -> User:
    return await user_service.create_new_user(new_user=new_user)

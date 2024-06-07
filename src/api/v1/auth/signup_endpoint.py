from fastapi import Depends

from src.core.dependencies import get_user_service
from src.core.schemas.user import UserCreate
from src.services.user_service import UserService
from src.api.v1.auth import auth_router


@auth_router.post("/signup")
async def create_new_user(new_user: UserCreate, user_service: UserService = Depends(get_user_service)) -> UserCreate:
    return await user_service.create_new_user(new_user=new_user)

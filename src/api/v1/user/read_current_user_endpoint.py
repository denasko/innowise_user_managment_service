from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials
from src.api.v1.bearer import bearer
from src.core.database.models.user import User
from src.core.dependencies import get_user_service
from src.core.schemas.user import UserRead
from src.services.user_service import UserService
from src.api.v1.user import user_router


@user_router.get("/me", response_model=UserRead)
async def read_current_user(
    user_service: UserService = Depends(get_user_service),
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
) -> User:
    return await user_service.read_current_user(credentials=credentials)

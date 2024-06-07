from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials

from src.api.v1.bearer import bearer
from src.core.dependencies import get_user_service
from src.core.schemas.user import UserUpdate
from src.services.user_service import UserService
from src.api.v1.user import user_router


@user_router.patch("/me")
async def edit_user(
    user_update: UserUpdate,
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
    user_service: UserService = Depends(get_user_service),
) -> UserUpdate:
    return await user_service.update_user(user_update=user_update, credentials=credentials)

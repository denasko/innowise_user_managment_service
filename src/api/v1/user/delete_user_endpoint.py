from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials
from src.api.v1.bearer import bearer
from src.core.dependencies import get_user_service
from src.services.user_service import UserService
from src.api.v1.user import user_router


@user_router.delete("/me")
async def delete_user(
    user_service: UserService = Depends(get_user_service),
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
) -> dict:
    return await user_service.delete_user(credentials=credentials)

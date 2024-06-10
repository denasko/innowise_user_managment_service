from fastapi import Depends, Form
from src.core.dependencies import get_authorization_service
from src.services.authorization_service import AuthService
from src.core.schemas.token import TokenInfo
from src.api.v1.auth import auth_router


@auth_router.post("/login", response_model=TokenInfo)
async def login(
    username: str = Form(),
    password: str = Form(),
    auth_service: AuthService = Depends(get_authorization_service),
) -> TokenInfo:
    return await auth_service.login(username=username, password=password)

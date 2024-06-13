from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database.database import async_session
from src.core.database.models.user import User
from src.services.authorization_service import AuthService
from src.services.token_sevice import TokenService
from src.services.user_service import UserService


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


def get_user_service(session: AsyncSession = Depends(get_session)) -> UserService:
    return UserService(session=session)


def get_token_service() -> TokenService:
    return TokenService()


def get_authorization_service(
    session: AsyncSession = Depends(get_session),
) -> AuthService:
    return AuthService(session=session)


async def get_user_from_token(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer),
    auth_service: AuthService = Depends(get_authorization_service),
) -> User:
    payload: dict = auth_service.get_current_token_payload(credentials=credentials)

    user_from_jwt: User = await auth_service.get_user_from_jwt(payload=payload)

    return user_from_jwt

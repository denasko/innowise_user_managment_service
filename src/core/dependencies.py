from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database.database import async_session
from src.services.authorization_service import AuthService
from src.services.user_service import UserService
from src.services.token_sevice import TokenService


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

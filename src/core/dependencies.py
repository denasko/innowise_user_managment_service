import aio_pika
from aio_pika.abc import AbstractRobustConnection
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import settings
from src.core.database.database import async_session
from src.core.database.models.user import User
from src.services.authorization_service import AuthService
from src.services.rabbitmq_service import RabbitMQService
from src.services.token_sevice import TokenService
from src.services.user_service import UserService


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


def get_user_service(session: AsyncSession = Depends(get_session)) -> UserService:
    return UserService(session=session)


def get_token_service(session: AsyncSession = Depends(get_session)) -> TokenService:
    return TokenService(session=session)


def get_authorization_service(
    session: AsyncSession = Depends(get_session),
) -> AuthService:
    return AuthService(session=session)


async def get_user_from_token(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    token_service: TokenService = Depends(get_token_service),
) -> User:
    payload: dict = token_service.get_current_token_payload(credentials=credentials)
    user_from_jwt: User = await token_service.get_user_from_jwt(payload=payload)
    return user_from_jwt


async def get_rabbitmq_connection() -> AbstractRobustConnection:
    return await aio_pika.connect_robust(
        host=settings.rabbitmq.rabbitmq_host,
        port=settings.rabbitmq.rabbitmq_port,
        login=settings.rabbitmq.rabbitmq_user,
        password=settings.rabbitmq.rabbitmq_password,
    )


def get_rabbitmq_service(
    connection: AbstractRobustConnection = Depends(get_rabbitmq_connection),
) -> RabbitMQService:
    return RabbitMQService(connection=connection)

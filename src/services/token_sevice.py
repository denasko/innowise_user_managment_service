import datetime
from typing import Any

import jwt
from fastapi.security import HTTPAuthorizationCredentials
from jwt import PyJWTError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import settings
from src.core.database.enums.token import TokenType
from src.core.database.models.user import User as UserModel
from src.core.exeption_handlers import (
    TokenException,
    UserNotFoundException,
    AuthenticationException,
)
from src.core.schemas.token import TokenInfo
from src.managers.token_manager import RedisDB
from src.managers.user_manager import UserManager


class TokenService:
    def __init__(self, session: AsyncSession):
        self.redis = RedisDB()
        self.repository = UserManager(session=session)

    def create_jwt_token(self, user: UserModel, token_type: TokenType) -> str:
        """created token payload"""
        jwt_payload = {"type": token_type}

        if token_type == TokenType.REFRESH:
            jwt_payload.update({"sub": user.id})
            token_time_to_live = settings.jwt.jwt_refresh_token_time_to_live_minutes

        elif token_type == TokenType.ACCESS:
            jwt_payload.update({"sub": user.id, "role": user.role, "email": user.email})
            token_time_to_live = settings.jwt.jwt_access_token_time_to_live_minutes

        else:
            raise TokenException()

        return self.encode_jwt(payload=jwt_payload, token_time_to_live=token_time_to_live)

    @staticmethod
    def encode_jwt(
        payload: dict,
        private_key: str = settings.jwt.jwt_private_key,
        algorithm: str = settings.jwt.jwt_algorithm,
        token_time_to_live: int = settings.jwt.jwt_access_token_time_to_live_minutes,
    ) -> str:
        """append to jwt payload time to token live"""
        to_encode = payload.copy()
        time_now = datetime.datetime.now(datetime.timezone.utc)
        expire = time_now + datetime.timedelta(minutes=token_time_to_live)

        to_encode.update(exp=expire, iat=time_now)
        to_encode["sub"] = str(to_encode["sub"])

        encoded = jwt.encode(payload=to_encode, key=private_key, algorithm=algorithm)
        return encoded

    async def refresh_token(self, current_user: UserModel, credentials: HTTPAuthorizationCredentials) -> TokenInfo:
        token_payload = self.get_current_token_payload(credentials=credentials)
        if token_payload.get("type") != TokenType.REFRESH:
            raise TokenException(detail="Invalid token type")

        if self.is_token_expired(payload=token_payload):
            is_blacklisted = await self.redis.is_token_in_blacklist(credentials.credentials)
            if is_blacklisted:
                raise TokenException(detail="Token is blacklisted. Please log in again.")

            await self.redis.set_token(token=credentials.credentials, value=credentials.credentials)

        refresh_token = self.create_jwt_token(user=current_user, token_type=TokenType.REFRESH)
        access_token = self.create_jwt_token(user=current_user, token_type=TokenType.ACCESS)
        return TokenInfo(access_token=access_token, refresh_token=refresh_token)

    @staticmethod
    def is_token_expired(
        payload: Any,
    ) -> bool:
        expiration_time = datetime.datetime.fromtimestamp(payload.get("exp"))

        current_time = datetime.datetime.now()
        if current_time > expiration_time:
            return True
        return False

    @staticmethod
    def get_current_token_payload(
        credentials: HTTPAuthorizationCredentials,
    ) -> Any:
        """return decode token if token is valid"""
        token: str = credentials.credentials
        try:
            payload: Any = jwt.decode(
                jwt=token,
                algorithms=settings.jwt.jwt_algorithm,
                key=settings.jwt.jwt_public_key,
            )
        except PyJWTError:
            raise TokenException()
        return payload

    async def get_user_from_jwt(
        self,
        payload: Any,
    ) -> UserModel:
        """return user if user exist, not blocked and type token is access"""
        user: UserModel | None = await self.repository.get_user_by_field(user_id=payload["sub"])

        if user is None:
            raise UserNotFoundException()

        if user.is_blocked:
            raise AuthenticationException(detail="user is blocked")

        return user

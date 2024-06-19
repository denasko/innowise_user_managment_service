import jwt
from fastapi.security import HTTPAuthorizationCredentials
from jwt import PyJWTError
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.config import settings
from src.core.database.enums.token import TokenType
from src.core.database.models.user import User as UserModel
from src.core.schemas.token import TokenInfo
from src.managers.user_manager import UserManager
from src.services.token_sevice import TokenService
from src.utils.password import check_password
from src.core.exeption_handlers import (
    AuthenticationException,
    TokenException,
    UserNotFoundException,
)


class AuthService:
    def __init__(self, session: AsyncSession):
        self.repository = UserManager(session=session)
        self.token_service = TokenService()

    async def get_user_to_login(self, username: str, password: str) -> UserModel:
        """if user exist in db and password in form equal to password from db, return user"""
        user: UserModel | None = await self.repository.get_user_by_field(username=username)
        if user is None:
            raise UserNotFoundException()

        if not check_password(password=password, hashed_password=user.password):
            raise AuthenticationException()
        return user

    def get_current_token_payload(
        self,
        credentials: HTTPAuthorizationCredentials,
    ) -> dict:
        """return decode token if token is valid"""
        token: str = credentials.credentials
        try:
            payload: dict = jwt.decode(
                jwt=token,
                algorithms=settings.jwt.jwt_algorithm,
                key=settings.jwt.jwt_public_key,
            )
        except PyJWTError:
            raise TokenException()
        return payload

    async def get_user_from_jwt(
        self,
        payload: dict,
    ) -> UserModel:
        """return user if user exist, not blocked and type token is access"""
        user: UserModel | None = await self.repository.get_user_by_field(user_id=payload["sub"])

        if user is None:
            raise UserNotFoundException()

        if user.is_blocked:
            raise AuthenticationException(detail="user is blocked")

        return user

    async def login(self, username: str, password: str) -> TokenInfo:
        """take user from db and generate to him access and refresh token"""
        user: UserModel = await self.get_user_to_login(username=username, password=password)

        access_token = self.token_service.create_jwt_token(user=user, token_type=TokenType.ACCESS)
        refresh_token = self.token_service.create_jwt_token(user=user, token_type=TokenType.REFRESH)

        return TokenInfo(access_token=access_token, refresh_token=refresh_token)

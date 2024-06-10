from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from jwt.exceptions import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database.enums.token import TokenType
from src.core.database.models.user import User as UserModel
from src.api.v1.bearer import bearer
from src.core.schemas.token import TokenInfo
from src.managers.user_manager import UserManager
from src.utils.password import check_password
from src.services.token_sevice import TokenService


class AuthService:
    def __init__(self, session: AsyncSession):
        self.repository = UserManager(session=session)
        self.token_service = TokenService()

    async def validate_auth_user(self, username: str, password: str) -> UserModel | None:
        """return user if user exist, not blocked and password is correct"""
        user: UserModel | None = await self.repository.get_user_by_field(username=username)
        if user is None or not check_password(password=password, hashed_password=user.password):
            return None
        return user

    def get_current_token_payload(
        self,
        credentials: HTTPAuthorizationCredentials = Depends(bearer),
    ) -> dict:
        """return payload if token is valid"""
        token: str = credentials.credentials
        try:
            payload: dict = self.token_service.decode_jwt(token=token)
        except InvalidTokenError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"invalid token error: {e}",
            )

        return payload

    async def get_current_auth_not_blocked_user(
        self,
        payload: dict,
    ) -> UserModel:
        """return user if user exist, not blocked and type token is access"""

        token_type = payload.get("type")
        if token_type != TokenType.ACCESS:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token type")

        user: UserModel | None = await self.repository.get_user_by_field(user_id=payload["sub"])
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
        if user.is_blocked:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="user is blocked")

        return user

    async def login(self, username: str, password: str) -> TokenInfo:
        """if user exist and not blocked, generate access and refresh token"""
        user: UserModel | None = await self.validate_auth_user(username=username, password=password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="incorrect username or password",
            )
        return self.token_service.generate_two_tokens(user=user)

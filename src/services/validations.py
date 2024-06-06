from fastapi import Depends, HTTPException, status, Form
from fastapi.security import HTTPAuthorizationCredentials
from jwt.exceptions import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.v1.credentials import bearer
from src.core.database.database import get_session
from src.core.database.models.user import User
from src.managers.user import user_manager
from src.services.token_sevice import decode_jwt
from src.services.password import check_password


async def validate_auth_user(
    # credentials: HTTPBasicCredentials = Depends(security),
    username: str = Form(),
    password: str = Form(),
    session: AsyncSession = Depends(get_session),
) -> User | None:
    unauthed_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid login or password")

    user: User | None = await user_manager.get_user_by_username(session=session, username=username)

    if user is None:
        raise unauthed_exception

    if not check_password(password=password, hashed_password=user.password):
        raise unauthed_exception

    return user


def get_current_token_payload(
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
) -> dict:
    token: str = credentials.credentials
    try:
        payload: dict = decode_jwt(token)
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token error: {e}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload


async def get_current_auth_not_blocked_user(
    payload: dict = Depends(get_current_token_payload),
    session: AsyncSession = Depends(get_session),
) -> User | None:
    token_type = payload.get("type")
    if token_type != "access":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token type")
    user: User | None = await user_manager.get_user_by_id(session=session, user_id=payload["sub"])
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    if user.is_blocked:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="user is blocked")
    return user

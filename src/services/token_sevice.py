from src.core.schemas.schemas import TokenInfo, UserRead
import jwt
from datetime import datetime, timezone, timedelta
from src.core.config import settings


def create_jwt(
    token_type: str,
    user: UserRead,
) -> str:
    jwt_payload = {"type": token_type, "sub": user.id}
    return encode_jwt(
        payload=jwt_payload,
        token_time_to_live=settings.jwt.jwt_access_token_time_to_live_minutes,
    )


def generate_token(user: UserRead) -> TokenInfo:
    access_token = create_jwt(token_type="access", user=user)
    refresh_token = create_jwt(token_type="refresh", user=user)

    return TokenInfo(access_token=access_token, refresh_token=refresh_token)


def encode_jwt(
    payload: dict,
    private_key: str = settings.jwt.jwt_private_key,
    algorithm: str | None = settings.jwt.jwt_algorithm,
    token_time_to_live: int = settings.jwt.jwt_access_token_time_to_live_minutes,
):
    """return encoded jwt token"""
    to_encode = payload.copy()
    time_now = datetime.now(timezone.utc)
    expire = time_now + timedelta(minutes=token_time_to_live)
    to_encode.update(exp=expire, iat=time_now)
    to_encode["sub"] = str(to_encode["sub"])
    encoded = jwt.encode(payload=to_encode, key=private_key, algorithm=algorithm)
    return encoded


def decode_jwt(token: str | bytes):
    """return decode jwt token"""
    return jwt.decode(
        jwt=token,
        key=settings.jwt.jwt_public_key,
        algorithms=settings.jwt.jwt_algorithm,
    )

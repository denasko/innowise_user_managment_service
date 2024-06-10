from datetime import datetime, timezone, timedelta

import jwt
from src.core.database.models.user import User as UserModel
from src.core.config import settings
from src.core.schemas.token import TokenInfo
from src.core.database.enums.token import TokenType


class TokenService:
    def __init__(self):
        pass

    def create_jwt(self, token_type: str, token_data: dict, token_time_to_live: int) -> str:
        jwt_payload = {"type": token_type}
        jwt_payload.update(token_data)

        return self.encode_jwt(
            payload=jwt_payload,
            token_time_to_live=token_time_to_live,
        )

    def create_access_token(self, user: UserModel) -> str:
        print(user.username)
        jwt_payload = {"sub": user.id, "role": user.role, "email": user.email}

        return self.create_jwt(
            token_type=TokenType.ACCESS,
            token_data=jwt_payload,
            token_time_to_live=settings.jwt.jwt_access_token_time_to_live_minutes,
        )

    def create_refresh_token(self, user: UserModel) -> str:
        jwt_payload = {"sub": user.id}

        return self.create_jwt(
            token_type=TokenType.REFRESH,
            token_data=jwt_payload,
            token_time_to_live=settings.jwt.jwt_refresh_token_time_to_live_minutes,
        )

    def generate_two_tokens(self, user: UserModel) -> TokenInfo:
        access_token = self.create_access_token(user=user)
        refresh_token = self.create_refresh_token(user=user)

        return TokenInfo(access_token=access_token, refresh_token=refresh_token)

    def encode_jwt(
        self,
        payload: dict,
        private_key: str = settings.jwt.jwt_private_key,
        algorithm: str = settings.jwt.jwt_algorithm,
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

    def decode_jwt(self, token: str | bytes):
        """return decode jwt token"""
        return jwt.decode(
            jwt=token,
            key=settings.jwt.jwt_public_key,
            algorithms=settings.jwt.jwt_algorithm,
        )

from datetime import datetime, timezone, timedelta

import jwt

from src.core.config import settings
from src.core.database.enums.token import TokenType
from src.core.database.models.user import User as UserModel
from src.core.exeption_handlers import TokenException


class TokenService:
    def __init__(self):
        pass

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

    def encode_jwt(
        self,
        payload: dict,
        private_key: str = settings.jwt.jwt_private_key,
        algorithm: str = settings.jwt.jwt_algorithm,
        token_time_to_live: int = settings.jwt.jwt_access_token_time_to_live_minutes,
    ) -> str:
        """append to jwt payload time to token live"""
        to_encode = payload.copy()
        time_now = datetime.now(timezone.utc)
        expire = time_now + timedelta(minutes=token_time_to_live)

        to_encode.update(exp=expire, iat=time_now)
        to_encode["sub"] = str(to_encode["sub"])

        encoded = jwt.encode(payload=to_encode, key=private_key, algorithm=algorithm)
        return encoded

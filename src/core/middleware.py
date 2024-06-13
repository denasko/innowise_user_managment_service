from typing import Any

import jwt
from fastapi import FastAPI
from jwt import PyJWTError
from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from src.core.config import settings
from src.main import api_router


class BearerMiddleware(BaseHTTPMiddleware):
    AUTH_EXCLUDE_PATH = [router.path for router in api_router.routes if "user" in router.path]

    def __init__(self, app: FastAPI):
        super().__init__(app=app)

    async def dispatch(self, request, call_next):
        if request.url.path not in self.AUTH_EXCLUDE_PATH:
            return await call_next(request)

        if not request.headers.get("Authorization"):
            Response(status_code=status.HTTP_401_UNAUTHORIZED, content="Unauthorized")
            return await call_next(request)

        token: Any = request.headers["Authorization"]
        try:
            jwt.decode(
                jwt=token,
                algorithms=settings.jwt.jwt_algorithm,
                key=settings.jwt.jwt_public_key,
            )
        except PyJWTError:
            Response(status_code=status.HTTP_403_FORBIDDEN, content="Invalid token")
            return await call_next(request)

        return await call_next(request)

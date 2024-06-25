import jwt
from fastapi import FastAPI
from jwt import PyJWTError
from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from src.core.config import settings
from src.core.database.enums.token import TokenType
from src.main import api_router


class BearerMiddleware(BaseHTTPMiddleware):
    AUTH_INCLUDE_PATH = [router.path for router in api_router.routes if "auth" in router.path]
    AUTH_INCLUDE_PATH.extend(["/docs", "/openapi.json", "/healthcheck"])

    def __init__(self, app: FastAPI):
        super().__init__(app=app)

    async def dispatch(self, request, call_next):
        if request.url.path in self.AUTH_INCLUDE_PATH:
            return await call_next(request)

        authorization_header = request.headers.get("Authorization")

        if not authorization_header:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Unauthorized"},
            )

        bearer, token = request.headers["Authorization"].split(" ")
        if bearer != "Bearer":
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"detail": "Invalid token type"},
            )

        try:
            token_payload: dict = jwt.decode(
                jwt=token,
                algorithms=settings.jwt.jwt_algorithm,
                key=settings.jwt.jwt_public_key,
            )
        except PyJWTError:
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={"detail": "Invalid token"},
            )

        if token_payload.get("type") == TokenType.REFRESH:
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={"detail": "Invalid token type"},
            )

        return await call_next(request)

from fastapi import HTTPException
from starlette import status


class AuthenticationException(HTTPException):
    def __init__(
        self,
        detail: str = "Invalid login or password",
    ):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


class TokenException(HTTPException):
    def __init__(
        self,
        detail: str = "Invalid token",
    ):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


class PermissionException(HTTPException):
    def __init__(
        self,
        detail: str = "Permission denied",
    ):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


class UserNotFoundException(HTTPException):
    def __init__(
        self,
        detail: str = "User not found",
    ):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class RedisException(HTTPException):
    def __init__(self, detail: str = "Redis error occurred"):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)


class ValidationException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail)


class S3BucketException(HTTPException):
    def __init__(self, detail: str = "S3 bucket not found"):
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail)

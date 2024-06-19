from fastapi import HTTPException
from starlette import status


class AuthenticationException(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_403_FORBIDDEN,
        detail: str = "Invalid login or password",
    ):
        super().__init__(status_code=status_code, detail=detail)


class TokenException(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_403_FORBIDDEN,
        detail: str = "Invalid token",
    ):
        super().__init__(status_code=status_code, detail=detail)


class PermissionException(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_403_FORBIDDEN,
        detail: str = "Permission denied",
    ):
        super().__init__(status_code=status_code, detail=detail)


class UserNotFoundException(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_404_NOT_FOUND,
        detail: str = "User not found",
    ):
        super().__init__(status_code=status_code, detail=detail)

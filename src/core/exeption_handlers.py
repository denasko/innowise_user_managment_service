from fastapi import HTTPException
from starlette import status

unauthed_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid login or password")

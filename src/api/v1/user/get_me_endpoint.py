from fastapi import APIRouter, Depends

from src.core.schemas.schemas import UserRead
from src.services.validations import get_current_auth_not_blocked_user

get_me = APIRouter(
    prefix="/me",
    tags=[
        "Test authentication",
    ],
)


@get_me.get("")
def read_current_user(
    user: UserRead = Depends(get_current_auth_not_blocked_user),
) -> UserRead:
    return user

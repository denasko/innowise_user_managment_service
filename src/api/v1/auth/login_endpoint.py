from fastapi import Depends, APIRouter

from src.services import token_sevice
from src.services.validations import validate_auth_user
from src.core.schemas.schemas import TokenInfo, UserRead

login_router = APIRouter(
    prefix="/login",
    tags=[
        "Test authentication",
    ],
)


@login_router.post("/", response_model=TokenInfo)
async def login(user: UserRead = Depends(validate_auth_user)):
    return token_sevice.generate_token(user)

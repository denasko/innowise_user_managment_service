from fastapi import APIRouter

from .delete_me_endpoint import delete_me
from .get_me_endpoint import get_me
from .patch_me_endpoint import patch_me

user_router = APIRouter(prefix="/user")
user_router.include_router(get_me)
user_router.include_router(patch_me)
user_router.include_router(delete_me)

from .login_endpoint import login_router
from .signup_endpoint import signup_router

from fastapi import APIRouter

auth_router = APIRouter(prefix="/auth")
auth_router.include_router(login_router)
auth_router.include_router(signup_router)

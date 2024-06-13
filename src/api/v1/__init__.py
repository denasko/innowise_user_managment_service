from src.api.v1.auth_endpoints import auth_router
from src.api.v1.user_endpoints import user_router

from fastapi import APIRouter

api_v1_router = APIRouter(prefix="/v1", tags=["Test authorization"])
api_v1_router.include_router(auth_router)
api_v1_router.include_router(user_router)

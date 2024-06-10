from fastapi import APIRouter

from src.api.v1.user import (
    update_user_endpoint,
    read_current_user_endpoint,
    delete_user_endpoint,
)

__all__ = [
    "user_router",
    "update_user_endpoint",
    "delete_user_endpoint",
    "read_current_user_endpoint",
]
user_router = APIRouter(prefix="/user")

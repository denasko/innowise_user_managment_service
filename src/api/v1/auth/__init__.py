from fastapi import APIRouter

from src.api.v1.auth import signup_endpoint, login_endpoint

__all__ = ["signup_endpoint", "login_endpoint"]
auth_router = APIRouter(prefix="/auth")

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from src.core.database.enums.role import Role


class GroupBase(BaseModel):
    name: str


class GroupCreate(BaseModel):
    pass


class GroupUpdate(BaseModel):
    pass


class Group(BaseModel):
    id: UUID
    created_at: datetime


# ______________________________________________________________________________________________________________________


class UserBase(BaseModel):
    name: str
    surname: str
    username: str
    password: str
    phone_number: str
    email: str
    role: Role = Role.USER
    image_s3_path: Optional[str] = None
    is_blocked: bool = False


class UserRead(UserBase): ...


class UserCreate(BaseModel):
    name: str
    surname: str
    username: str
    password: str
    phone_number: str
    role: Role = Role.USER
    image_s3_path: str
    email: str
    group_id: UUID


class UserUpdate(BaseModel):
    name: str
    surname: str
    username: str
    phone_number: str
    email: str


class User(BaseModel):
    id: UUID
    created_at: datetime
    modified_at: datetime
    group: Group


# ______________________________________________________________________________________________________________________


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"

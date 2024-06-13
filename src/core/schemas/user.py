from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from src.core.database.enums.role import Role
from src.core.schemas.group import Group


class UserBase(BaseModel):
    name: str
    surname: str
    username: str
    phone_number: str
    email: str
    role: Role = Role.USER
    image_s3_path: Optional[str] = None


class UserRead(UserBase): ...


class UserCreate(UserBase):
    password: str
    group_id: UUID


class User(UserBase):
    id: UUID
    created_at: datetime
    modified_at: datetime
    is_blocked: bool = False
    group: Group

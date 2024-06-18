from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from src.core.database.enums.role import Role


class UserBase(BaseModel):
    name: str
    surname: str
    username: str
    phone_number: str
    email: str
    role: Role = Role.USER
    image_s3_path: Optional[str] = None


class UserRead(UserBase):
    id: UUID
    created_at: datetime
    modified_at: datetime
    is_blocked: bool = False
    group_id: UUID


class UserUpdate(UserBase): ...


class UserCreate(UserBase):
    password: str
    group_id: UUID

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class GroupBase(BaseModel):
    name: str


class GroupCreate(BaseModel):
    pass


class GroupUpdate(BaseModel):
    pass


class Group(BaseModel):
    id: UUID
    created_at: datetime

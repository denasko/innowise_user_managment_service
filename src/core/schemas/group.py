from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class GroupBase(BaseModel):
    name: str


class GroupCreate(GroupBase):
    pass


class GroupUpdate(GroupBase):
    pass


class Group(BaseModel):
    id: UUID
    created_at: datetime

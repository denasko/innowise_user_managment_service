import enum
from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Enum, MetaData, func

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, DeclarativeBase


class Base(DeclarativeBase):
    pass


class Role(enum.StrEnum):
    USER = "USER"
    ADMIN = "ADMIN"
    MODERATOR = "MODERATOR"


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    phone_number = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    role_enum = Column(Enum(Role), nullable=False, default=Role.USER, server_default=Role.USER)
    group_id = Column(UUID(as_uuid=True), ForeignKey("groups.id"), nullable=False)
    image_s3_path = Column(String, nullable=False)
    is_blocked = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False, server_default=func.now())
    modified_at = Column(DateTime, default=datetime.now, nullable=False, server_onupdate=func.now(),
                         server_default=func.now())

    group = relationship("Group", back_populates="users")


class Group(Base):
    __tablename__ = "groups"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False, server_default=func.now())

    users = relationship("User", back_populates="group")

from typing import Sequence, Any, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database.models.user import User
from src.core.schemas.schemas import UserCreate, UserUpdate
from src.services.password import hash_password


class UserManager:
    def __init__(self):
        pass

    async def _get_user_by_field(self, session: AsyncSession, **kwargs: Any) -> Optional[User]:
        """Get user by given unique field(s)"""
        stmt = select(User).where(*[getattr(User, key) == value for key, value in kwargs.items()])
        result = await session.execute(stmt)
        user = result.scalars().first()
        return user

    async def get_user_by_username(self, session: AsyncSession, username: str) -> Optional[User]:
        return await self._get_user_by_field(username=username, session=session)

    async def get_user_by_id(self, session: AsyncSession, user_id: UUID) -> Optional[User]:
        return await self._get_user_by_field(id=user_id, session=session)

    async def get_all_users(self, session: AsyncSession) -> Sequence[User] | None:
        stmt = select(User).order_by(User.id)
        result = await session.scalars(stmt)
        return result.all()

    async def create_user(self, session: AsyncSession, new_user: UserCreate) -> User:
        user = User(**new_user.model_dump())
        user.password = hash_password(new_user.password)
        session.add(user)
        await session.commit()
        return user

    async def edit_user(self, session: AsyncSession, current_user: UserUpdate, user_update: UserUpdate) -> UserUpdate:
        for field, value in user_update.model_dump().items():
            setattr(current_user, field, value)
        await session.commit()
        return current_user

    async def delete_user(self, session: AsyncSession, user_to_delete: UserUpdate) -> dict:
        username = user_to_delete.username
        await session.delete(user_to_delete)
        await session.commit()
        return {username: "was deleted"}


user_manager = UserManager()

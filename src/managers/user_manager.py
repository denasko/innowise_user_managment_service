from typing import Sequence, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database.models.user import User as UserModel
from src.core.schemas.user import UserCreate, UserRead


class UserManager:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_field(
        self,
        user_id: Optional[UUID] = None,
        username: Optional[str] = None,
        email: Optional[str] = None,
        phone_number: Optional[str] = None,
    ) -> Optional[UserModel]:
        """Get user by given unique field(s)"""
        stmt = select(UserModel)

        if user_id is not None:
            stmt = stmt.where(UserModel.id == user_id)
        if username is not None:
            stmt = stmt.where(UserModel.username == username)
        if email is not None:
            stmt = stmt.where(UserModel.email == email)
        if phone_number is not None:
            stmt = stmt.where(UserModel.phone_number == phone_number)

        result = await self.session.execute(stmt)
        user = result.scalars().first()

        return user

    async def get_all_users(self) -> Sequence[UserModel] | None:
        stmt = select(UserModel).order_by(UserModel.id)
        result = self.session.scalars(stmt)

        return result.all()

    async def create_user(self, new_user: UserCreate) -> UserModel:
        user_in_db: UserModel = UserModel(**new_user.model_dump())
        self.session.add(user_in_db)
        await self.session.commit()
        return user_in_db

    async def edit_user(self, current_user: UserModel, user_update: UserRead) -> UserModel:
        for field, value in user_update.model_dump().items():
            setattr(current_user, field, value)
        await self.session.commit()

        return current_user

    async def delete_user(self, user_to_delete: UserModel) -> dict:
        username = user_to_delete.username

        await self.session.delete(user_to_delete)
        await self.session.commit()

        return {username.title(): "Was deleted"}

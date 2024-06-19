from typing import Sequence, Optional
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exeption_handlers import UserNotFoundException
from src.core.database.enums.sorting import OrderBy, SortBy
from src.core.database.models.user import User as UserModel
from src.core.schemas.user import UserCreate, UserUpdate


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

    async def create_user(self, new_user: UserCreate) -> UserModel:
        user_in_db: UserModel = UserModel(**new_user.model_dump())
        self.session.add(user_in_db)
        await self.session.commit()
        return user_in_db

    async def edit_user(self, current_user_id: UUID, user_update: UserUpdate) -> UserModel:
        query = (
            update(UserModel).where(UserModel.id == current_user_id).values(**user_update.dict()).returning(UserModel)
        )

        result = await self.session.execute(query)

        await self.session.commit()

        updated_user = result.scalar()

        if not updated_user:
            raise UserNotFoundException()

        return updated_user

    async def delete_user(self, user_to_delete: UserModel) -> dict:
        username = user_to_delete.username

        await self.session.delete(user_to_delete)
        await self.session.commit()

        return {username.title(): "Was deleted"}

    async def get_collection_of_users(
        self,
        current_user: UserModel,
        page: int = 1,
        limit: int = 10,
        filter_by_name: Optional[str] = None,
        sort_by: Optional[str] = SortBy.NAME,
        order_by: Optional[str] = OrderBy.DESC,
        is_moderator: bool = False,
    ) -> Sequence[UserModel]:
        query = select(UserModel)

        if is_moderator:
            query = query.where(UserModel.group_id == current_user.group_id)

        if filter_by_name:
            query = query.where(
                UserModel.name.ilike(f"%{filter_by_name}%") | UserModel.surname.ilike(f"%{filter_by_name}%")
            )

        if sort_by and order_by:
            if hasattr(UserModel, sort_by):
                if order_by.lower() == OrderBy.DESC:
                    query = query.order_by(getattr(UserModel, sort_by.lower()).desc())
                else:
                    query = query.order_by(getattr(UserModel, sort_by.lower()).asc())
            else:
                raise UserNotFoundException(
                    detail=f"Field {sort_by} not found",
                )

        offset = (page - 1) * limit
        query = query.offset(offset).limit(limit)

        result = await self.session.execute(query)

        return result.scalars().all()

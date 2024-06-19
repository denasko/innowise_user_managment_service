from typing import Optional, Sequence
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database.enums.role import Role
from src.core.database.models.user import User as UserModel
from src.core.exeption_handlers import (
    PermissionException,
    UserNotFoundException,
)
from src.core.schemas.user import UserCreate, UserUpdate
from src.managers.user_manager import UserManager
from src.services.authorization_service import AuthService
from src.services.token_sevice import TokenService
from src.utils.password import hash_password
from src.core.database.enums.sorting import OrderBy, SortBy


class UserService:
    def __init__(self, session: AsyncSession):
        self.auth_service = AuthService(session=session)
        self.repository = UserManager(session=session)
        self.token_service = TokenService()

    async def create_new_user(self, new_user: UserCreate) -> UserModel:
        new_user.password = hash_password(new_user.password)

        return await self.repository.create_user(new_user=new_user)

    async def delete_current_user(self, current_user: UserModel) -> dict:
        return await self.repository.delete_user(user_to_delete=current_user)

    async def update_current_user(self, user_update: UserUpdate, current_user: UserModel) -> UserModel:
        return await self.repository.edit_user(user_update=user_update, current_user_id=current_user.id)

    async def update_another_user_by_id(
        self,
        current_user: UserModel,
        target_user_id: UUID,
        target_user_updated_fields: UserUpdate,
    ) -> UserModel:
        if current_user.role != Role.ADMIN:
            raise PermissionException(
                detail=f"User {current_user.username} with role {current_user.role} not have permissions",
            )

        return await self.repository.edit_user(current_user_id=target_user_id, user_update=target_user_updated_fields)

    async def get_target_user_with_permissions(self, current_user: UserModel, target_user_id: UUID) -> UserModel:
        target_user: Optional[UserModel] = await self.repository.get_user_by_field(user_id=target_user_id)

        if not target_user:
            raise UserNotFoundException()

        if not self._check_permissions_to_read_or_update_target_user(current_user, target_user):
            raise PermissionException(
                detail=f"User {current_user.username} does not have permission",
            )

        return target_user

    @staticmethod
    def _check_permissions_to_read_or_update_target_user(current_user: UserModel, target_user: UserModel) -> bool:
        if current_user.role == Role.USER:
            raise PermissionException()

        if current_user.role == Role.MODERATOR and target_user.role == Role.ADMIN:
            raise PermissionException()

        if current_user.role == Role.MODERATOR and current_user.group_id != target_user.group_id:
            raise PermissionException()

        return True

    async def get_collection_of_users(
        self,
        current_user: UserModel,
        page: int = 1,
        limit: int = 10,
        filter_by_name: Optional[str] = None,
        sort_by: Optional[str] = SortBy.NAME,
        order_by: Optional[str] = OrderBy.DESC,
    ) -> Sequence[UserModel]:
        if current_user.role == Role.USER:
            raise PermissionException(status_code=403, detail="Not enough permissions")

        return await self.repository.get_collection_of_users(
            page=page,
            limit=limit,
            filter_by_name=filter_by_name,
            sort_by=sort_by,
            order_by=order_by,
            current_user=current_user,
            is_moderator=current_user.role == Role.MODERATOR,
        )

from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.schemas.user import UserCreate, UserUpdate
from src.core.database.models.user import User as UserModel
from src.managers.user_manager import UserManager
from src.services.authorization_service import AuthService
from src.utils.password import hash_password
from src.services.token_sevice import TokenService


class UserService:
    def __init__(self, session: AsyncSession):
        self.auth_service = AuthService(session=session)
        self.repository = UserManager(session=session)
        self.token_service = TokenService()

    async def create_new_user(self, new_user: UserCreate) -> UserModel:
        new_user.password = hash_password(new_user.password)

        return await self.repository.create_user(new_user=new_user)

    async def delete_user(self, credentials: HTTPAuthorizationCredentials) -> dict:
        payload: dict = self.auth_service.get_current_token_payload(credentials=credentials)
        user_to_delete: UserModel = await self.auth_service.get_current_auth_not_blocked_user(payload=payload)

        return await self.repository.delete_user(user_to_delete=user_to_delete)

    async def update_user(self, user_update: UserUpdate, credentials: HTTPAuthorizationCredentials) -> UserModel:
        payload: dict = self.auth_service.get_current_token_payload(credentials=credentials)
        current_user: UserModel = await self.auth_service.get_current_auth_not_blocked_user(payload=payload)

        return await self.repository.edit_user(user_update=user_update, current_user=current_user)

    async def read_current_user(self, credentials: HTTPAuthorizationCredentials) -> UserModel:
        payload: dict = self.auth_service.get_current_token_payload(credentials=credentials)
        current_user: UserModel = await self.auth_service.get_current_auth_not_blocked_user(payload=payload)

        return current_user

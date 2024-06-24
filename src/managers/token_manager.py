from src.core.config import settings
from src.core.exeption_handlers import RedisException
from redis import asyncio as aioredis


class RedisDB:
    __redis_connect: aioredis.Redis = aioredis.Redis(host=settings.redis.redis_host, port=settings.redis.redis_port)

    async def set_token(self, token: str, value: str) -> None:
        try:
            await self.__redis_connect.set(name=token, value=value)
        except aioredis.RedisError:
            raise RedisException(detail="Failed to set token in blacklist")

    async def get_token(self, token: str) -> None:
        try:
            await self.__redis_connect.get(name=token)
        except aioredis.RedisError:
            raise RedisException(detail="Failed to get token from blacklist")

    async def is_token_in_blacklist(self, token: str) -> bool:
        try:
            return await self.__redis_connect.exists(token) > 0
        except aioredis.RedisError:
            raise RedisException(detail="Failed to check token in blacklist")

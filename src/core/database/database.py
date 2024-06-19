from aioredis import Redis, from_url
from typing import AsyncIterator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.core.config import settings

engine = create_async_engine(settings.db.DB_URL, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def init_redis_pool(host=settings.db.redis_host) -> AsyncIterator[Redis]:
    session = from_url(f"redis://{host}", encoding="utf-8")
    yield session
    session.close()
    await session.wait_closed()


class RedisDB:
    def __init__(self, redis: Redis):
        self.connection = redis

    async def get(self, key):
        return await self.connection.get(name=key)

    async def set(self, key, value):
        await self.connection.set(name=key, value=value)
        return await self.connection.get(name=key)

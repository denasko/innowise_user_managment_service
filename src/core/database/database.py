import redis
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.core.config import settings

engine = create_async_engine(settings.db.DB_URL, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


class RedisDB:
    __redis_connect: redis.Redis = redis.Redis(host="redis", port=6379)

    @classmethod
    async def set_token(cls, key, value):
        await cls.__redis_connect.set(name=key, value=value)
        return "its okey"

    @classmethod
    async def get_token(cls, key):
        await cls.__redis_connect.get(name=key)


redisik = RedisDB()

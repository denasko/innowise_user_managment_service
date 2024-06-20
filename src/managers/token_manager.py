import redis
from src.core.config import settings


class RedisDB:
    __redis_connect: redis.Redis = redis.Redis(host=settings.redis.redis_host, port=settings.redis.redis_port)

    def set_token(self, token: str, value: str) -> None:
        try:
            self.__redis_connect.set(name=token, value=value)
        except redis.RedisError as e:
            raise Exception(f"Redis error: {str(e)}")

    def get_token(self, token: str) -> None:
        self.__redis_connect.get(name=token)

    def is_token_in_blacklist(self, token: str) -> bool:
        print(settings.redis.redis_port, settings.redis.redis_host, sep="\n")
        try:
            return self.__redis_connect.exists(token) == 1
        except redis.RedisError as e:
            raise Exception(f"Redis error: {str(e)}")

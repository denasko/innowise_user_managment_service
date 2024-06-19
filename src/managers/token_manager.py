import redis


class RedisDB:
    __redis_connect: redis.Redis = redis.Redis(host="redis", port=6379)

    def set_token(self, token: str, value: str) -> None:
        try:
            self.__redis_connect.set(name=token, value=value)
        except redis.RedisError as e:
            raise Exception(f"Redis error: {str(e)}")

    def get_token(self, token: str) -> None:
        self.__redis_connect.get(name=token)

    def is_token_in_blacklist(self, token: str) -> bool:
        try:
            return self.__redis_connect.exists(token) == 1
        except redis.RedisError as e:
            raise Exception(f"Redis error: {str(e)}")

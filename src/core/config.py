from pydantic_settings import BaseSettings, SettingsConfigDict


class ConfiguredSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class AuthJWT(ConfiguredSettings):
    jwt_private_key: str
    jwt_public_key: str
    jwt_algorithm: str
    jwt_access_token_time_to_live_minutes: int = 15
    jwt_refresh_token_time_to_live_minutes: int = 15000


class DatabaseSettings(ConfiguredSettings):
    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: str

    @property
    def DB_URL(self) -> str:
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"


class RedisSettings(ConfiguredSettings):
    redis_host: str
    redis_port: int


class RabbitMQSettings(ConfiguredSettings):
    rabbitmq_host: str
    rabbitmq_port: int
    rabbitmq_user: str
    rabbitmq_password: str


class Settings(ConfiguredSettings):
    db: DatabaseSettings = DatabaseSettings()
    redis: RedisSettings = RedisSettings()
    jwt: AuthJWT = AuthJWT()
    rabbitmq: RabbitMQSettings = RabbitMQSettings()


settings = Settings()

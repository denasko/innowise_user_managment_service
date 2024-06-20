from pydantic_settings import BaseSettings, SettingsConfigDict


class AuthJWT(BaseSettings):
    jwt_private_key: str
    jwt_public_key: str
    jwt_algorithm: str
    jwt_access_token_time_to_live_minutes: int = 15
    jwt_refresh_token_time_to_live_minutes: int = 15000

    model_config = SettingsConfigDict(env_file=".env", extra="allow")


class DatabaseSettings(BaseSettings):
    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: str

    model_config = SettingsConfigDict(env_file=".env", extra="allow")

    @property
    def DB_URL(self) -> str:
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"


class RedisSettings(BaseSettings):
    redis_host: str
    redis_port: int

    model_config = SettingsConfigDict(env_file=".env", extra="allow")


class Settings(BaseSettings):
    db: DatabaseSettings = DatabaseSettings()
    jwt: AuthJWT = AuthJWT()
    redis: RedisSettings = RedisSettings()

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()

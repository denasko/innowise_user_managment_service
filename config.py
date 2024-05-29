from pydantic_settings import BaseSettings


class PostgresSettings(BaseSettings):
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "db_user_management"
    DB_USER: str = "db_user_management"
    DB_PASSWORD: str = "db_user_management"

    @property
    def DB_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = PostgresSettings()

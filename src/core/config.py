from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings


class AuthJWT(BaseModel):
    private_key_path: Path = Path("src") / "core" / "auth" / "sertificats" / "jwt-private.pem"
    public_key_path: Path = Path("src") / "core" / "auth" / "sertificats" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_time_to_live: int = 3


class DatabaseSettings(BaseModel):
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "db_user_management"
    DB_USER: str = "db_user_management"
    DB_PASSWORD: str = "db_user_management"

    POSTGRES_DB: str = "postgres"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"

    @property
    def DB_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


class Settings(BaseSettings):
    db: DatabaseSettings = DatabaseSettings()
    jwt: AuthJWT = AuthJWT()


settings = Settings()

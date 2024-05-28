from pydantic_settings import BaseSettings
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from config import PostgresSettings

postrgres_settings = PostgresSettings()

# sqlalchemy.url = postgresql+asyncpg://db_user_management:db_user_management@localhost/db_user_management
sql_url = "postgresql+asyncpg://%(DB_USER)s:%(DB_PASS)s@%(DB_HOST)s:%(DB_PORT)s%(DB_NAME)s"


class Settings(BaseSettings):
    DATABASE_URL: str = (
        f"postgresql+asyncpg://{postrgres_settings.DB_USER}:{postrgres_settings.DB_NAME}@"
        f"{postrgres_settings.DB_HOST}/{postrgres_settings.DB_PASSWORD}"
    )

    class Config:
        env_file = ".env"


settings = Settings()

engine = create_async_engine(settings.DATABASE_URL, echo=True)
async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session

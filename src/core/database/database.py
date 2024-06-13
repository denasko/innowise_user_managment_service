from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.core.config import settings

engine = create_async_engine(settings.db.DB_URL, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

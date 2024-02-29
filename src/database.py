from typing import AsyncGenerator

from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from src.config import setting


engin = create_async_engine(url=setting.DATABASE_URL_asyncpg)
async_session_maker = sessionmaker(engin, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncEngine
from typing import AsyncGenerator
from settings import SETTINGS

async_engine: AsyncEngine = create_async_engine(SETTINGS.POSTGRES.ENGINE_URL.get_secret_value())
async_session_maker = async_sessionmaker[AsyncSession](bind=async_engine, expire_on_commit=False)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    try:
        session: AsyncSession = async_session_maker()
        yield session
    finally:
        await session.close()

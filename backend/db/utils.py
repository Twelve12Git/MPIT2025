from db.sessions import async_engine
from db.base import BaseModel

async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)

async def drop_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)

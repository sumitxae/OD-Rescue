from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base
from app.config.config import Config

Base = declarative_base()

engine = create_async_engine(
    Config.DATABASE_URL,
    echo=True,
)  

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

async def get_db() -> AsyncGenerator[AsyncSession, None]: 
    async with async_session_maker() as session:
        yield session
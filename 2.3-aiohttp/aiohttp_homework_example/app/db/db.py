from typing import Type

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from config import PG_ASYNC_DSN
from tools import singleton


@singleton
def get_engine() -> AsyncEngine:
    return create_async_engine(PG_ASYNC_DSN)


Session: Type[AsyncSession] = sessionmaker(bind=get_engine(), expire_on_commit=False, class_=AsyncSession)

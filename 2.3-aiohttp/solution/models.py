import os
import uuid

from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, func
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy_utils import EmailType, UUIDType

PG_USER = os.getenv("PG_USER", "user")
PG_PASSWORD = os.getenv("PG_PASSWORD", "1234")
PG_DB = os.getenv("PG_DB", "netology")
PG_HOST = os.getenv("PG_HOST", "127.0.0.1")
PG_PORT = os.getenv("PG_PORT", "5431")

PG_DSN = f"postgresql+asyncpg://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"

engine = create_async_engine(PG_DSN)
Session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()


class User(Base):
    __tablename__ = "app_users"
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    email = Column(EmailType, unique=True, index=True)


class Token(Base):
    __tablename__ = "tokens"
    id = Column(UUIDType, primary_key=True, default=uuid.uuid4)
    creation_time = Column(DateTime, server_default=func.now())
    user_id = Column(Integer, ForeignKey("app_users.id", ondelete="CASCADE"))
    user = relationship("User", lazy="joined")
    

class Advertisement(Base):
    __tablename__ = "advertisements"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    owner = Column(ForeignKey("app_users.id", ondelete="CASCADE"))
    creation_time = Column(
        DateTime, default=func.now()
    )

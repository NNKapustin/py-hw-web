import uuid
from typing import Type

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy_utils import EmailType, UUIDType

Base = declarative_base()


class Advertisement(Base):

    __tablename__ = "advertisements"

    id = Column(Integer, primary_key=True)
    title = Column(String(256), nullable=False)
    description = Column(String, nullable=False)
    creation_time = Column(DateTime, server_default=func.now())
    owner_id = Column(Integer, ForeignKey("ads_users.id", ondelete="CASCADE"))
    owner = relationship("User", lazy="joined")


class User(Base):

    __tablename__ = "ads_users"

    id = Column(Integer, primary_key=True)
    email = Column(EmailType, unique=True, index=True)
    password = Column(String(60), nullable=False)


class Token(Base):

    __tablename__ = "tokens"

    id = Column(UUIDType, primary_key=True, default=uuid.uuid4)
    creation_time = Column(DateTime, server_default=func.now())
    user_id = Column(Integer, ForeignKey("ads_users.id", ondelete="CASCADE"))
    user = relationship("User", lazy="joined")


ORM_MODEL_CLS = Type[Advertisement] | Type[User] | Type[Token]
ORM_MODEL = Advertisement | User | Token

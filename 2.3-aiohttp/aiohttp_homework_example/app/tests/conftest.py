import datetime
import secrets
import time

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from auth.auth import hash_password
from config import PG_DB, PG_HOST, PG_PASSWORD, PG_PORT, PG_USER
from db.models import Advertisement, Base, Token, User
from tests.config import ROOT_USER_EMAIL, ROOT_USER_PASSWORD
from tools import singleton


@singleton
def get_engine():
    return create_engine(f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}")


Session = sessionmaker(bind=get_engine())


def get_random_password():
    password = secrets.token_hex()
    return f"{password[:10]}{password[10:20].upper()}"


@pytest.fixture(scope="session", autouse=True)
def init_database():
    engine = get_engine()
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    engine.dispose()


def create_user(email: str = None, password: str = None):
    email = email or f"user{time.time()}@email.te"
    password = password or get_random_password()
    with Session() as session:
        new_user = User(email=email, password=hash_password(password))
        session.add(new_user)
        session.commit()
        return {"id": new_user.id, "email": new_user.email, "password": password}


@pytest.fixture(scope="session")
def root_user():
    return create_user(ROOT_USER_EMAIL, ROOT_USER_PASSWORD)


@pytest.fixture()
def new_user():
    return create_user()


@pytest.fixture()
def new_user_advertisement():
    new_user = create_user()
    with Session() as session:
        new_advertisement = Advertisement(
            title=f"title{time.time()}", description=f"description{time.time()}", owner_id=new_user["id"]
        )
        session.add(new_advertisement)
        session.commit()
        return {
            "advertisement_id": new_advertisement.id,
            "advertisement_title": new_advertisement.title,
            "advertisement_description": new_advertisement.description,
            "advertisement_creation_time": new_advertisement.creation_time,
            "user_id": new_user["id"],
            "user_email": new_user["email"],
            "user_password": new_user["password"],
        }


@pytest.fixture()
def expired_token():
    with Session() as session:
        user = create_user()
        token = Token(user_id=user["id"], creation_time=datetime.datetime.utcnow() - datetime.timedelta(days=1000))
        session.add(token)
        session.commit()
        return str(token.id)

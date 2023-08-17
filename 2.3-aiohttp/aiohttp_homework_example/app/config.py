import os

PG_USER = os.getenv("PG_USER", "ads")
PG_PASSWORD = os.getenv("PG_PASSWORD", "secret")
PG_HOST = os.getenv("PG_HOST", "127.0.0.1")
PG_PORT = os.getenv("PG_PORT", 5431)
PG_DB = os.getenv("PG_DB", "ads")


PG_ASYNC_DSN = f"postgresql+asyncpg://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"
TOKEN_TTL = int(os.getenv("TOKEN_TTL", 60 * 60 * 24))
PASSWORD_LENGTH = int(os.getenv("PASSWORD_LENGTH", 12))

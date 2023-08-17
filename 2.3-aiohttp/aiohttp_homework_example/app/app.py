from aiohttp import web

from middleware import session_middleware
from views import AdvertisementView, login, register
from db.db import get_engine
from db.models import Base


async def init_database(app: web.Application):
    engine = get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


async def get_app():
    app = web.Application(middlewares=[session_middleware])
    app.add_routes(
        [
            web.post("/login", login),
            web.post("/register", register),
            web.get("/advertisement/{advertisement_id:\d+}", AdvertisementView),
            web.post("/advertisement", AdvertisementView),
            web.patch("/advertisement/{advertisement_id:\d+}", AdvertisementView),
            web.delete("/advertisement/{advertisement_id:\d+}", AdvertisementView),
        ]
    )
    app.cleanup_ctx.append(init_database)

    return app

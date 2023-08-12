import json

from aiohttp import web
from bcrypt import checkpw, gensalt, hashpw
from sqlalchemy.exc import IntegrityError

from models import Base, Session, User, engine, Advertisement


def hash_password(password: str):
    password = str(password).encode()
    password = hashpw(password, gensalt())
    password = password.decode()
    return password


def check_password(password: str, hashed_password: str):
    password = password.encode()
    hashed_password = hashed_password.encode()
    return checkpw(password, hashed_password)


def get_http_error(http_error_class, message):
    return http_error_class(
        text=json.dumps({"error": message}), content_type="application/json")



app = web.Application()


async def orm_cntx(app: web.Application):
    print("START")
    async with engine.begin() as con:
        #await con.run_sync(Base.metadata.drop_all)
        await con.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()
    print("SHUT DOWN")


@web.middleware
async def session_middleware(request: web.Request, handler):
    async with Session() as session:
        request["session"] = session
        response = await handler(request)
        return response


app.cleanup_ctx.append(orm_cntx)
app.middlewares.append(session_middleware)


async def get_user(user_id: int, session: Session) -> User:
    user = await session.get(User, user_id)
    if user is None:
        raise get_http_error(web.HTTPNotFound, "user not found")
    return user


class UserView(web.View):
    @property
    def session(self) -> Session:
        return self.request["session"]

    @property
    def user_id(self) -> int:
        return int(self.request.match_info["user_id"])

    async def get(self):
        user = await get_user(self.user_id, self.session)
        return web.json_response(
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            }
        )

    async def post(self):
        json_data = await self.request.json()
        json_data["password"] = hash_password(json_data["password"])
        user = User(**json_data)
        try:
            self.session.add(user)
            await self.session.commit()
        except IntegrityError as err:
            raise get_http_error(web.HTTPConflict, "user already exists")
        return web.json_response({"id": user.id})

    async def patch(self):
        json_data = await self.request.json()
        if "password" in json_data:
            json_data["password"] = hash_password(json_data["password"])
        user = await get_user(self.user_id, self.session)
        for key, value in json_data.items():
            setattr(user, key, value)
        try:
            self.session.add(user)
            await self.session.commit()
        except IntegrityError as err:
            raise get_http_error(web.HTTPConflict, "user already exists")
        return web.json_response({"id": user.id})

    async def delete(self):
        user = await get_user(self.user_id, self.session)
        await self.session.delete(user)
        await self.session.commit()
        return web.json_response({"status": "deleted"})
    

async def get_advertisement(adv_id: int, session: Session) -> Advertisement:
    user = await session.get(Advertisement, adv_id)
    if user is None:
        raise get_http_error(web.HTTPNotFound, "advertisement not found")
    return user


class AdvertisementView(web.View):
    @property
    def session(self) -> Session:
        return self.request["session"]

    @property
    def adv_id(self) -> int:
        return int(self.request.match_info["adv_id"])
    
    async def get(self):
        advertisement = await get_advertisement(self.adv_id, self.session)
        return web.json_response(
            {
                "id": advertisement.id,
                "title": advertisement.title,
                "email": advertisement.description,
            }
        )

    async def post(self):
        json_data = await self.request.json()
        advertisement = Advertisement(**json_data)
        self.session.add(advertisement)
        await self.session.commit()
        return web.json_response({"id": advertisement.id})

    async def patch(self):
        json_data = await self.request.json()
        advertisement = await get_advertisement(self.adv_id, self.session)
        for key, value in json_data.items():
            setattr(advertisement, key, value)
        self.session.add(advertisement)
        await self.session.commit()
        return web.json_response({"id": advertisement.id})

    async def delete(self):
        advertisement = await get_user(self.adv_id, self.session)
        await self.session.delete(advertisement)
        await self.session.commit()
        return web.json_response({"status": "deleted"})


app.add_routes(
    [
        web.get("/user/{user_id:\d+}/", UserView),
        web.patch("/user/{user_id:\d+}/", UserView),
        web.delete("/user/{user_id:\d+}/", UserView),
        web.post("/user/", UserView),

        web.get("/advertisement/{adv_id:\d+}/", AdvertisementView),
        web.patch("/advertisement/{adv_id:\d+}/", AdvertisementView),
        web.delete("/advertisement/{adv_id:\d+}/", AdvertisementView),
        web.post("/advertisement/", AdvertisementView),
    ]
)

if __name__ == "__main__":
    web.run_app(app)

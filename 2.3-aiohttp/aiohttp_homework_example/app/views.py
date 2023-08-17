from aiohttp import web
from sqlalchemy.future import select

from auth.auth import check_password, hash_password
from auth.check import check_auth
from crud import create_item, delete_item, get_item, patch_item
from db.models import Advertisement, Token, User
from errors import Forbidden, Unauthorized
from schema import CreateAdvertisement, Login, PatchAdvertisement, Register, validate


async def register(request: web.Request):
    json_data = await request.json()
    user_data = validate(Register, json_data)

    user_data["password"] = hash_password(user_data["password"])
    user = await create_item(request["session"], User, **user_data)
    return web.json_response({"id": user.id})


async def login(request: web.Request):
    json_data = await request.json()
    login_data = validate(Login, json_data)
    query = select(User).where(User.email == login_data["email"])
    result = await request["session"].execute(query)
    user = result.scalar()
    if not user or not check_password(login_data["password"], user.password):
        raise Unauthorized("incorrect login or password")

    token = Token(user=user)
    request["session"].add(token)
    await request["session"].commit()

    return web.json_response({"token": str(token.id)})


class AdvertisementView(web.View):
    async def get(self):
        advertisement_id = int(self.request.match_info["advertisement_id"])

        advertisement = await get_item(self.request["session"], Advertisement, advertisement_id)
        return web.json_response(
            {
                "id": advertisement.id,
                "owner_id": advertisement.owner_id,
                "title": advertisement.title,
                "description": advertisement.description,
                "creation_time": advertisement.creation_time.isoformat(),
            }
        )

    async def post(self):
        advertisement_data = validate(CreateAdvertisement, await self.request.json())
        token = await check_auth(self.request)
        new_advertisement = await create_item(
            self.request["session"], Advertisement, owner_id=token.user_id, **advertisement_data
        )
        return web.json_response({"id": new_advertisement.id})

    async def patch(self):
        advertisement_id = int(self.request.match_info["advertisement_id"])
        patch_data = validate(PatchAdvertisement, await self.request.json())
        token = await check_auth(self.request)
        advertisement = await get_item(self.request["session"], Advertisement, advertisement_id)
        if token.user_id != advertisement.owner_id:
            raise Forbidden("user has no access")
        advertisement = await patch_item(self.request["session"], advertisement, **patch_data)

        return web.json_response(
            {
                "id": advertisement.id,
                "title": advertisement.title,
                "description": advertisement.description,
                "creation_time": advertisement.creation_time.isoformat(),
            }
        )

    async def delete(self):
        advertisement_id = int(self.request.match_info["advertisement_id"])
        advertisement = await get_item(self.request["session"], Advertisement, advertisement_id)
        token = await check_auth(self.request)
        if token.user_id != advertisement.owner_id:
            raise Forbidden("user has no access")

        await delete_item(self.request["session"], advertisement)

        return web.json_response({"deleted": True})

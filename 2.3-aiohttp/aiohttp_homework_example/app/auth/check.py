import datetime
from uuid import UUID

from aiohttp import web

from config import TOKEN_TTL
from crud import get_item
from db.models import Token
from errors import Forbidden, NotFound


async def check_auth(request: web.Request) -> Token:
    token_id = request.headers.get("token")
    try:
        token_id = UUID(token_id)
    except (TypeError, ValueError):
        token_id = None
    if not token_id:
        raise Forbidden("incorrect token")
    try:
        token = await get_item(request["session"], Token, token_id)
    except NotFound:
        token = None
    if not token or token.creation_time + datetime.timedelta(seconds=TOKEN_TTL) <= datetime.datetime.now():
        raise Forbidden("incorrect token")
    request["token"] = token
    return token

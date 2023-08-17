import json

from aiohttp.web_exceptions import HTTPException


class BaseError(HTTPException):
    def __init__(self, description: str | dict | list):
        super().__init__(
            text=json.dumps({"status": "error", "description": description}), content_type="application/json"
        )


class BadRequest(BaseError):
    status_code = 400


class Unauthorized(BaseError):
    status_code = 401


class Forbidden(BaseError):
    status_code = 403


class NotFound(BaseError):
    status_code = 404


class Conflict(BaseError):
    status_code = 409

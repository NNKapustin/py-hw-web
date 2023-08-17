import re
from typing import Any, Dict, Optional, Type

from pydantic import BaseModel, EmailStr, ValidationError, validator

from config import PASSWORD_LENGTH
from errors import BadRequest

PASSWORD_REGEX = re.compile(
    "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-])*.{{{password_length},}}$".format(
        password_length=PASSWORD_LENGTH
    )
)


class Register(BaseModel):

    email: EmailStr
    password: str

    @validator("password")
    def strong_password(cls, value: str):
        if not PASSWORD_REGEX.match(value):
            raise ValueError("password is to easy")
        return value


class Login(BaseModel):

    email: EmailStr
    password: str


class CreateAdvertisement(BaseModel):

    title: str
    description: str


class PatchAdvertisement(BaseModel):

    title: Optional[str]
    description: Optional[str]


SCHEMA_TYPE = Type[Register] | Type[Login] | Type[CreateAdvertisement]


def validate(schema: SCHEMA_TYPE, data: Dict[str, Any], exclude_none: bool = True) -> dict:
    try:
        validated = schema(**data).dict(exclude_none=exclude_none)
    except ValidationError as er:
        raise BadRequest(er.errors())
    return validated

from typing import Optional

from pydantic import BaseModel, validator


class CreateUser(BaseModel):
    username: str
    password: str
    email: str

    @validator("password")
    def secure_password(cls, value):
        if len(value) <= 6:
            return ValueError("Password is short")
        return value


class UpdateUser(BaseModel):
    username: Optional[
        str
    ]  # при обновлении поля могут быть не все, делаем их опциональными
    password: Optional[str]
    email: Optional[str]

    @validator("password")
    def secure_password(cls, value):
        if len(value) <= 6:
            return ValueError("Password is short")
        return value
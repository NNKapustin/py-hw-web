import json
from typing import Literal
from urllib.parse import urljoin

import requests

from tests.config import API_URL

session = requests.Session()


class ApiError(Exception):
    def __init__(self, status_code: int, message: str | dict | list):
        self.status_code = status_code
        self.message = message


def base_request(http_method: Literal["get", "post", "delete", "patch"], path: "str", *args, **kwargs) -> dict:
    method = getattr(session, http_method)
    response = method(urljoin(API_URL, path), *args, **kwargs)
    if response.status_code >= 400:
        try:
            message = response.json()
        except json.JSONDecodeError:
            message = response.text
        raise ApiError(response.status_code, message)
    return response.json()


def register(email: str, password: str) -> int:
    return base_request("post", "register", json={"email": email, "password": password})["id"]


def login(email: str, password: str) -> str:
    return base_request("post", "login", json={"email": email, "password": password})["token"]


def get_advertisement(advertisement_id: int) -> dict:
    return base_request("get", f"advertisement/{advertisement_id}")


def create_advertisement(title: str, description: str, token: str) -> int:
    return base_request(
        "post", "advertisement", json={"title": title, "description": description}, headers={"token": token}
    )["id"]


def delete_advertisement(advertisement_id: int, token: str) -> bool:
    return base_request("delete", f"advertisement/{advertisement_id}", headers={"token": token})["deleted"]


def patch_advertisement(advertisement_id: int, token: str, title: str = None, description: str = None) -> dict:
    params = {key: value for key, value in (("title", title), ("description", description)) if value is not None}
    return base_request("patch", f"advertisement/{advertisement_id}", json=params, headers={"token": token})

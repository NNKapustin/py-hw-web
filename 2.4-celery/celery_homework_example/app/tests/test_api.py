import time

import requests
from PIL import Image

from tests.config import API_URL


def test_api():

    response = requests.post(f"{API_URL}/upload", files={"image": open("tests/download.jpg", "rb")})
    task = response.json()["task"]

    status = "PENDING"

    while status == "PENDING":
        time.sleep(0.1)
        response = requests.get(f"{API_URL}/tasks/{task}").json()
        status = response["status"]

    response = requests.get(f'{API_URL}{response["link"]}')

    with open("tests/download_scaled.jpg", "wb") as file:
        file.write(response.content)

    source_width, source_height = Image.open("tests/download.jpg").size
    scaled_width, scaled_height = Image.open("tests/download_scaled.jpg").size

    assert source_width * 2 == scaled_width
    assert source_height * 2 == scaled_height


def test_not_exist():

    response = requests.get(f"{API_URL}/processed/1/upscaled.jpg")
    assert response.status_code == 423

import os

import pytest


@pytest.fixture(scope="session", autouse=True)
def prepare_files():
    if os.path.exists("tests/download_scaled.jpg"):
        os.remove("tests/download_scaled.jpg")

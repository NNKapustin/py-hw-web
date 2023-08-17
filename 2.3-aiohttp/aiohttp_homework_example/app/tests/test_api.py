import uuid

import pytest

from tests.api_requests import (
    ApiError,
    create_advertisement,
    delete_advertisement,
    get_advertisement,
    login,
    patch_advertisement,
    register,
)
from tests.config import DEFAULT_PASSWORD


def test_register():
    user_id = register("user_1@email.te", DEFAULT_PASSWORD)

    assert isinstance(user_id, int)


def test_register_simple_password():
    with pytest.raises(ApiError) as error:
        register("user_1@email.te", "1234")

    assert error.value.status_code == 400
    assert error.value.message == {
        "status": "error",
        "description": [{"loc": ["password"], "msg": "password is to easy", "type": "value_error"}],
    }


def test_invalid_email():
    with pytest.raises(ApiError) as error:
        register("invalid_email", DEFAULT_PASSWORD)

    assert error.value.status_code == 400
    assert error.value.message == {
        "status": "error",
        "description": [{"loc": ["email"], "msg": "value is not a valid email address", "type": "value_error.email"}],
    }


def test_register_existed(new_user):
    with pytest.raises(ApiError) as error:
        register(new_user["email"], DEFAULT_PASSWORD)
    assert error.value.status_code == 409
    assert error.value.message == {"status": "error", "description": f"such user already exists"}


def test_login(new_user):
    token = login(new_user["email"], new_user["password"])
    assert isinstance(token, str)


def test_login_incorrect(new_user):
    with pytest.raises(ApiError) as error:
        login(new_user["email"], new_user["password"] + "a")
    assert error.value.status_code == 401


def test_get_advertisement(new_user_advertisement):
    advertisement = get_advertisement(new_user_advertisement["advertisement_id"])
    assert advertisement == {
        "id": new_user_advertisement["advertisement_id"],
        "title": new_user_advertisement["advertisement_title"],
        "description": new_user_advertisement["advertisement_description"],
        "creation_time": new_user_advertisement["advertisement_creation_time"].isoformat(),
        "owner_id": new_user_advertisement["user_id"],
    }


def test_get_unexisting_advertisement():
    with pytest.raises(ApiError) as er:
        get_advertisement(9999999)
    assert er.value.status_code == 404
    assert er.value.message == {"status": "error", "description": "advertisement not found"}


def test_create_advertisement(root_user):
    token = login(root_user["email"], root_user["password"])
    advertisement_id = create_advertisement("some_title", "some_description", token)
    assert isinstance(advertisement_id, int)


@pytest.mark.parametrize("token", ["bad_token", str(uuid.uuid4()), None])
def test_create_advertisement_bad_token(token):
    with pytest.raises(ApiError) as er:
        create_advertisement("some_title", "some_description", token)
    assert er.value.status_code == 403
    assert er.value.message == {"status": "error", "description": "incorrect token"}


@pytest.mark.parametrize("title, description", [[None, None], ["a", None], [None, "a"]])
def test_create_advertisement_bad_params(root_user, title, description):
    token = login(root_user["email"], root_user["password"])
    with pytest.raises(ApiError) as er:
        create_advertisement(title, description, token)
    assert er.value.status_code == 400


def test_delete_own_advertisement(root_user):
    root_user_token = login(root_user["email"], root_user["password"])
    advertisement_id = create_advertisement("title", "description", root_user_token)
    result = delete_advertisement(advertisement_id, root_user_token)
    assert result is True


def test_delete_foreign_advertisement(root_user, new_user):
    new_user_token = login(new_user["email"], new_user["password"])
    advertisement_id = create_advertisement("title", "description", new_user_token)

    root_user_token = login(root_user["email"], root_user["password"])
    with pytest.raises(ApiError) as er:
        delete_advertisement(advertisement_id, root_user_token)
    assert er.value.status_code == 403
    assert er.value.message == {"status": "error", "description": "user has no access"}


def test_patch_own_advertisement(new_user_advertisement):
    token = login(new_user_advertisement["user_email"], new_user_advertisement["user_password"])
    advertisement = patch_advertisement(
        new_user_advertisement["advertisement_id"],
        title="patched_title",
        description="patched_description",
        token=token,
    )
    assert advertisement["title"] == "patched_title"
    assert advertisement["description"] == "patched_description"

    advertisement = get_advertisement(new_user_advertisement["advertisement_id"])
    assert advertisement["title"] == "patched_title"
    assert advertisement["description"] == "patched_description"


def test_patch_foreign_advertisement(new_user, new_user_advertisement):
    new_user_token = login(new_user["email"], new_user["password"])
    with pytest.raises(ApiError) as er:
        patch_advertisement(
            new_user_advertisement["advertisement_id"],
            token=new_user_token,
            title="patched_title",
            description="patched_description",
        )
    assert er.value.status_code == 403
    assert er.value.message == {"status": "error", "description": "user has no access"}


def test_expired_token(expired_token):
    with pytest.raises(ApiError) as er:
        create_advertisement("title", "description", expired_token)

    assert er.value.status_code == 403
    assert er.value.message == {"status": "error", "description": "incorrect token"}

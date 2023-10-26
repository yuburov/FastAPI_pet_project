import pytest
from httpx import AsyncClient

from tests.conftest import client, create_test_auth_headers_for_user


def test_register():
    user_data = {
        "username": "Aron",
        "email": "aron@gmail.com",
        "password": "string",
    }
    response = client.post("/auth/register", json=user_data)

    assert response.status_code == 200


async def test_create_user_duplicate_email_error(get_user_from_database):
    user_data = {
        "username": "Nikolai",
        "email": "lol@kek.com",
        "password": "SamplePass1!",
    }
    user_data_same = {
        "username": "Petr",
        "email": "lol@kek.com",
        "password": "SamplePass1!",
    }
    resp = client.post("auth/register", json=user_data)
    data_from_resp = resp.json()
    assert resp.status_code == 200
    assert data_from_resp["result"]["username"] == user_data["username"]
    assert data_from_resp["result"]["email"] == user_data["email"]
    users_from_db = await get_user_from_database(data_from_resp["result"]["id"])
    assert len(users_from_db) == 1
    user_from_db = dict(users_from_db[0])
    assert user_from_db["username"] == user_data["username"]
    assert user_from_db["email"] == user_data["email"]
    assert user_from_db["id"] == data_from_resp["result"]["id"]
    resp = client.post("auth/register", json=user_data_same)
    assert resp.status_code == 400
    assert ('Email already exists!' == resp.json()["detail"])


async def test_login(ac: AsyncClient):
    user_data = {
        "username": "Melis",
        "email": "meilis@gmail.com",
        "password": "string",
    }
    await ac.post("/auth/register", json=user_data)
    resp = await ac.post("auth/login", json=user_data)
    assert resp.status_code == 200
    user_from_response = resp.json()
    assert user_from_response["detail"] == "Successfully login"


async def test_logout(ac: AsyncClient):
    user_data = {
        "username": "Mara",
        "email": "mara@gmail.com",
        "password": "string",
    }
    register_resp = await ac.post("/auth/register", json=user_data)
    resp_json = register_resp.json()
    id = resp_json["result"]["id"]
    await ac.post("auth/login", json=user_data)
    resp = await ac.post("auth/logout", json=user_data,
                         headers=create_test_auth_headers_for_user(id))
    assert resp.status_code == 200
    result = resp.json()
    assert result["detail"] == "Successfully logout"


async def test_logout_failed(ac: AsyncClient):
    user_data = {
        "username": "Mara",
        "email": "mara@gmail.com",
        "password": "string",
    }
    await ac.post("/auth/register", json=user_data)
    await ac.post("auth/login", json=user_data)
    resp = await ac.post("auth/logout", json=user_data)
    assert resp.status_code == 403
    result = resp.json()
    assert result["detail"] == "Not authenticated"


async def test_login_with_wrong_password(ac: AsyncClient):
    user_data = {
        "username": "Melis",
        "email": "meilis@gmail.com",
        "password": "string",
    }
    await ac.post("/auth/register", json=user_data)
    resp = await ac.post("auth/login", json={
        "username": "Melis",
        "email": "meilis@gmail.com",
        "password": "stringgg",
    })
    assert resp.status_code == 400
    user_from_response = resp.json()
    assert user_from_response["detail"] == "Invalid Password !"


@pytest.mark.parametrize(
    "user_data_for_creation, expected_status_code, expected_detail",
    [
        (
            {},
            422,
            {
                'detail':
                    [
                        {
                            'type': 'missing',
                            'loc': ['body', 'username'],
                            'msg': 'Field required',
                            'input': {},
                            'url': 'https://errors.pydantic.dev/2.4/v/missing'
                        },
                        {
                            'type': 'missing',
                            'loc': ['body', 'email'],
                            'msg': 'Field required',
                            'input': {},
                            'url': 'https://errors.pydantic.dev/2.4/v/missing'
                        },
                        {
                            'type': 'missing',
                            'loc': ['body', 'password'],
                            'msg': 'Field required',
                            'input': {},
                            'url': 'https://errors.pydantic.dev/2.4/v/missing'
                        }
                    ]
            }
        ),
        (
            {"username": 123, "email": "lol@gmail.com", "password": "string"},
            422,
            {
                'detail':
                    [
                        {
                            'type': 'string_type',
                            'loc': ['body', 'username'],
                            'msg': 'Input should be a valid string',
                            'input': 123,
                            'url': 'https://errors.pydantic.dev/2.4/v/string_type'
                         }
                    ]
            },
        ),
        (
            {"username": "Nikolai", "email": "lol"},
            422,
            {
                'detail':
                    [
                        {
                            'type': 'value_error',
                            'loc': ['body', 'email'],
                            'msg': 'value is not a valid email address: The email address is not valid. It must have exactly one @-sign.',
                            'input': 'lol',
                            'ctx': {'reason': 'The email address is not valid. It must have exactly one @-sign.'}
                        },
                        {
                            'type': 'missing',
                            'loc': ['body', 'password'],
                            'msg': 'Field required',
                            'input': {'username': 'Nikolai', 'email': 'lol'},
                            'url': 'https://errors.pydantic.dev/2.4/v/missing'
                        }
                    ]
            }
        ),
    ],
)
async def test_create_user_validation_error(
    user_data_for_creation, expected_status_code, expected_detail
):
    resp = client.post("auth/register", json=user_data_for_creation)
    data_from_resp = resp.json()
    assert resp.status_code == expected_status_code
    assert data_from_resp == expected_detail

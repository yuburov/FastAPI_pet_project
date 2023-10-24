from httpx import AsyncClient

from tests.conftest import client


def test_register():
    response = client.post("/auth/register", json={
        "username": "Aron",
        "email": "aron@gmail.com",
        "password": "string",
    })

    assert response.status_code == 200
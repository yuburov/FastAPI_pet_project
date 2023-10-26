import asyncio
from typing import AsyncGenerator

import asyncpg
import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from src.config import MODE, DB_NAME
from src.db.db import Base, engine, DATABASE_URL
from src.main import app
from src.services.token_service import TokenService


@pytest.fixture(scope='session', autouse=True,)
async def setup_db():
    async with engine.begin() as conn:
        assert MODE == "TEST"
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        assert MODE == "TEST"
        await conn.run_sync(Base.metadata.drop_all)


# SETUP
@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


client = TestClient(app)


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session")
async def asyncpg_pool():
    pool = await asyncpg.create_pool(
        "".join(DATABASE_URL.split("+asyncpg"))
    )
    yield pool
    await pool.close()


@pytest.fixture
async def get_user_from_database(asyncpg_pool):
    async def get_user_from_database_by_uuid(user_id: str):
        async with asyncpg_pool.acquire() as connection:
            return await connection.fetch(
                """SELECT * FROM users WHERE id = $1;""", user_id
            )

    return get_user_from_database_by_uuid


def create_test_auth_headers_for_user(user_id: str) -> dict[str, str]:
    access_token, refresh_token = TokenService.generate_tokens(user_id)
    return {"Authorization": f"Bearer {access_token}"}
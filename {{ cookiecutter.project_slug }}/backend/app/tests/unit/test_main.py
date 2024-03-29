"""Test for main.py."""
from typing import AsyncIterator

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from app.main import app


### Using TestClient, which inherits from httpx.Client###
@pytest.fixture(scope="session")
def client():
    """Test Client."""
    return TestClient(app)


def test_root(client: TestClient) -> None:
    """Unit test for root get API call."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to FastAPI Course!"}


### Using httpx.AsyncClient ###
@pytest.fixture()
async def async_client() -> AsyncIterator[AsyncClient]:
    """Async client."""
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client


# To run test only on asyncio backend, not trio backend
@pytest.fixture()
def anyio_backend() -> str:
    """Letting anyio know that we run only on asyncio."""
    return "asyncio"


@pytest.mark.anyio
async def test_root_async(async_client: AsyncClient) -> None:
    """Unit test for root get api call using async."""
    response = await async_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to FastAPI Course!"}

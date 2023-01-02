import pytest
from mongomock_motor import AsyncMongoMockClient

from benbucks_core import init_db


@pytest.fixture
async def mongo_mock_client():
    client = AsyncMongoMockClient()
    await init_db(client, "test")

import pytest_asyncio
from beanie import init_beanie
from mongomock_motor import AsyncMongoMockClient

from benbucks_core import TriviaQuestion, User


@pytest_asyncio.fixture
async def mongo_mock_client():
    client = AsyncMongoMockClient()
    await init_beanie(
        document_models=[TriviaQuestion, User],
        database=client.get_database(name="db"),
    )
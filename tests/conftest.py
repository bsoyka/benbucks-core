import pytest
from beanie import init_beanie
from mongomock_motor import AsyncMongoMockClient

from benbucks_core import Pool, TriviaQuestion, User


@pytest.fixture
async def mongo_mock_client():
    client = AsyncMongoMockClient()
    await init_beanie(
        document_models=[Pool, TriviaQuestion, User],
        database=client.get_database(name="db"),
    )

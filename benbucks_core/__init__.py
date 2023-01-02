from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from .lottery import Lottery
from .pool import Pool
from .trivia import TriviaQuestion
from .user import User

__all__ = ["init_db", "Lottery", "Pool", "TriviaQuestion", "User"]


async def init_db(client: AsyncIOMotorClient, env: str = "prod"):
    await init_beanie(
        document_models=[Lottery, Pool, TriviaQuestion, User],
        database=client[env],
    )

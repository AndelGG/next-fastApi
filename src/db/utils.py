from motor.motor_asyncio import AsyncIOMotorClient
from ..pet.settings import settings


def get_mongodb_client() -> AsyncIOMotorClient:
    return AsyncIOMotorClient(settings.MONGO_URI)

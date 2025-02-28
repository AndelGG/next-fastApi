from pydantic import BaseModel
from .fields import PyObjectId


class MongoDBModel(BaseModel):
    class Meta:
        collection_name: str

    id: PyObjectId

    @classmethod
    def get_collection_name(cls):
        return cls.Meta.collection_name


class StartGame(BaseModel):
    player: str


class Game(BaseModel):
    class Meta:
        collections_name = "games"

    player1: str
    player2: str

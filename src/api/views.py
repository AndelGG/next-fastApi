from fastapi import APIRouter

from .models import StartGame, Game
from ..db.client import MongoDBClient

router = APIRouter(prefix="/games", tags=["games"])


@router.post("/")
async def start(player_data: StartGame) -> Game:
    data = {"player1": player_data.player, "player2": player_data.player}

    client = MongoDBClient()
    inserted_result = await client.insert(Game, data)  # type: ignore[arg-type]
    game_data = await client.get(
        Game,  # type: ignore[arg-type]
        inserted_result.inserted_id,
    )
    result = Game(**game_data)

    return result

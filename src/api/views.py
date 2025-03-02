from fastapi import APIRouter, HTTPException, status, WebSocket, WebSocketDisconnect
import logging
from typing import cast

from .fields import PyObjectId
from .models import StartGame, Game, get_model_safe, MoveInput
from .crud import (
    start_new_game,
    get_game_by_id,
    delete_games_from_db,
    join_new_game,
    list_games_from_db,
    update_game,
)
from .websocket import connection_manager
from .shortcuts import make_move
from .validators import validate

router = APIRouter(prefix="/games", tags=["games"])

logger = logging.getLogger(__name__)


@router.post("/")
async def start(player_data: StartGame) -> Game:
    game = await start_new_game(player_data.player)
    if game is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Game cannot be started right now, please try again later",
        )
    return game


@router.get("/{game_id}/")
async def get_game(game_id: PyObjectId) -> Game:
    game = await get_game_by_id(game_id)
    if game is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Game not found"
        )
    return game


@router.delete("/")
async def delete_game() -> dict[str, int]:
    deleted_count = await delete_games_from_db()
    return {"deleted_count": deleted_count}


@router.get("/")
async def list_games() -> list[Game]:
    return await list_games_from_db()  # type: ignore[return-value]


@router.post("/{game_id}/join/")
async def join_game(game_id: PyObjectId, player_data: StartGame) -> Game:
    game = await get_game_by_id(game_id)
    if game is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Game not found"
        )

    if game.player2 is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Game already started",
        )

    updated_game = await join_new_game(game, player_data.player)
    if updated_game is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Game cannot be joined right now, please try again later",
        )

    await connection_manager.broadcast_game(updated_game)

    return updated_game


@router.websocket("/ws/{game_id}/")
async def websocket_game_endpoint(websocket: WebSocket, game_id: PyObjectId) -> None:
    await connection_manager.connect(websocket, game_id)

    try:
        while True:
            move_data = await websocket.receive_json()  # {"col": int}

            # get game and move
            game = await get_game_by_id(id=game_id)
            move = get_model_safe(MoveInput, move_data)

            # validate
            error_msg = validate(game, move)  # type: ignore[arg-type]
            if error_msg:
                logger.warning(error_msg)
                continue

            # make move
            game = cast(Game, game)
            move = cast(MoveInput, move)
            make_move(game, move.col)  # type: ignore[arg-type]

            # update DB
            updated_game = cast(Game, await update_game(game.id, game.model_dump()))

            # broadcast game to all players
            await connection_manager.broadcast_game(updated_game)
    except WebSocketDisconnect:
        connection_manager.disconnect(websocket, game_id)

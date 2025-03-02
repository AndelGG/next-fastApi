from datetime import datetime, timezone

from ..constants import PlayerEnum
from ..core import detect_winner, mark_winner, calculate_row_by_col
from .models import Game


def make_move(game: Game, col: int) -> None:
    row = calculate_row_by_col(game.board, col)

    game.board[row][col] = game.next_player_to_move_sign  # type: ignore[index]
    game.move_number += 1

    winner = detect_winner(game.board)

    if winner:
        mark_winner(game.board, winner)
        game.winner = PlayerEnum(winner)
        game.finished_at = datetime.now(timezone.utc)

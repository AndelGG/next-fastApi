class CustomError(Exception):
    default_message = "An error occurred"

    def __init__(self, message: str | None = None):
        super().__init__(message or self.default_message)


class GameNotFound(CustomError):
    default_message = "Game not found"


class NotAllPlayersJoinedError(CustomError):
    default_message = "Not all players have joined"


class GameFinishedError(CustomError):
    default_message = "Game has already finished"


class MoveNotValidError(CustomError):
    default_message = "Move not valid"


class WrongPlayerToMoveError(CustomError):
    default_message = "It's not your turn"

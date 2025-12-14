from enum import Enum, auto

class MoveResult(Enum):
    OK = auto()
    INVALID_MOVE = auto()
    CELL_OCCUPIED = auto()
    CHECK = auto()
    CHECKMATE = auto()
from enum import Enum, auto

class PieceColor(Enum):
    BLACK = "black"
    WHITE = "white"

    def opposite(self) -> "PieceColor":
        return PieceColor.WHITE if self is PieceColor.BLACK else PieceColor.BLACK


class PieceType(Enum):
    KING =  auto()
    QUEEN = auto()
    ROOK =  auto()
    BISHOP = auto()
    KNIGHT = auto()
    PAWN =  auto()

class MoveResult(Enum):
    OK = auto()
    INVALID_MOVE = auto()
    CELL_OCCUPIED = auto()
    CHECK = auto()
    CHECKMATE = auto()
    ERROR = auto()

class MoveSpecial(Enum):
    CASTLE_KINGSIDE = auto() # O-O
    CASTLE_QUEENSIDE = auto() # 0-0-0
    EN_PASSANT = auto()
    PROMOTION_PAWN = auto()
    CAPTURE = auto()

class GameStatus(Enum):
    IN_PROGRESS = auto()
    PAT = auto()
    CHECKMATE = auto()
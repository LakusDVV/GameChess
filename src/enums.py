from enum import Enum, auto

class PieceColor(Enum):
    BLACK = "black"
    WHITE = "white"

class PieceType(Enum):
    KING = "king"
    QUEEN = "queen"
    ROOK = "rook"
    BISHOP = "bishop"
    KNIGHT = "knight"
    PAWN = "pawn"

class MoveResult(Enum):
    OK = auto()
    INVALID_MOVE = auto()
    CELL_OCCUPIED = auto()
    CHECK = auto()
    CHECKMATE = auto()

class MoveSpecial(Enum):
    CASTLE_KINGSIDE = auto() # O-O
    CASTLE_QUEENSIDE = auto() # 0-0-0
    EN_PASSANT = auto()
    PROMOTION_PAWN = auto()
    CAPTURE = auto()

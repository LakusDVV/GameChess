from shapes import King, Figure

from src.enums import MoveResult, PieceColor
from src.dataclass import MoveRecord, CastlingRights
from typing import Optional





class ChessBoard:
    def __init__(self):
        self.rows = 8
        self.cols = 8


        self._changes = []
        self._figures: list[Figure] = []
        self._board = [[0 for _ in range(self.rows)] for _ in range(self.cols)]

        self.castling_rights: CastlingRights = CastlingRights()
        self.en_passant_target: Optional[tuple[int, int]] = None
        self.side_to_move: PieceColor = PieceColor.WHITE



    def get_board(self):
        return self._board


    def add_figure(self, *, x: int, y: int, figure) -> MoveResult:
        if not self._board[y][x]: #If cell is empty

            self._board[y][x] = figure
            self._figures.append(figure)
            return MoveResult.OK

        return MoveResult.CELL_OCCUPIED


    def get_figures(self):
        return self._figures



    def apply_move(self, move: MoveRecord):
        from_x, from_y = move.from_pos
        to_x, to_y = move.to_pos

        piece: Figure = move.piece
        target = self._board[from_y][from_x]

        self._board[to_y][to_x] = piece
        self._board[from_y][from_x] = 0

        piece.cord = move.to_pos





    def undo(self, move: MoveRecord):
        from_x, from_y = move.from_pos
        to_x, to_y = move.to_pos

        piece: Figure = move.piece
        target = self._board[from_y][from_x]

        self._board[from_y][from_x] = piece
        self._board[to_y][to_x] = 0

        piece.cord = move.from_pos


    def get_figure(self, *, cord):
        x, y = cord
        return self._board[y][x]

    def is_empty(self, x: int, y: int) -> bool:
        return self._board[y][x] == 0


    def is_inside(self, x: int, y: int) -> bool:
        return 0 <= x < self.rows and 0 <= y < self.cols


    def print_board(self):
        for rows in self._board:
            for x in rows:
                print(f" {x} ", end="")
            print()


    def king_is_check(self, color: PieceColor):

        king_pos = self.find_king(color=color)

        for fig in self._figures:
            if king_pos in fig.get_moves(chessboard=self):
                return True
        return False


    def find_king(self, color: PieceColor) -> tuple[int, int]:
        for fig in self._figures:
            if isinstance(fig, King) and fig.color == color:
                return fig.cord

        raise Exception("King doesn't find")







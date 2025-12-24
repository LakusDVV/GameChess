from src.enums import MoveResult, PieceColor
from src.shapes import Figure
from src.game import CastlingRights
from typing import Optional





class ChessBoard:
    def __init__(self):
        self.rows = 8
        self.cols = 8


        self._changes = []
        self._figures = []
        self._board = [[0 for _ in range(self.rows)] for _ in range(self.cols)]

        self.castling_rights = CastlingRights
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


    def make_move(self, *,  old_x: int, old_y: int , new_x, new_y):
        piece = self._board[old_y][old_x]
        # target = self._board[new_y][new_x]
        self._board[old_y][old_x] = 0
        self._board[new_y][new_x] = piece
        self._changes.append(((old_x, old_y), (new_x, new_y)))


    def undo(self):
        last = self._changes.pop()


    def is_empty(self, x: int, y: int) -> bool:
        return self._board[y][x] == 0


    def is_inside(self, x: int, y: int) -> bool:
        return 0 <= x < self.rows and 0 <= y < self.cols


    def print_board(self):
        for rows in self._board:
            for x in rows:
                print(f" {x} ", end="")
            print()



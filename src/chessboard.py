from src.enums import MoveResult
from shapes import Figure





class ChessBoard:
    def __init__(self):
        self.rows = 8
        self.cols = 8



        self._figures = []
        self._board = [[0 for _ in range(self.rows)] for _ in range(self.cols)]


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





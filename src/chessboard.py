from shapes import King, Figure, Rook, Pawn

from src.enums import MoveResult, PieceColor
from src.dataclass import MoveRecord, CastlingRights
from typing import Optional, TYPE_CHECKING





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


        self._board[to_y][to_x] = piece
        self._board[from_y][from_x] = 0

        piece.cord = move.to_pos

        self.change_castling_rights(move)

        if move.captured_piece:
            self._figures.remove(move.captured_piece)





    def change_castling_rights(self, record: MoveRecord):
        piece = record.piece
        from_x, from_y = record.from_pos
        to_x, to_y = record.to_pos
        color = record.piece.color


        if isinstance(record.piece, Rook):

            if from_x == 0 and self.castling_rights.can_castle_kingside(color):
                if color == PieceColor.WHITE:
                    self.castling_rights.white_king_side = False

                if color == PieceColor.BLACK:
                    self.castling_rights.black_king_side = False

            if from_x == 7 and self.castling_rights.can_castle_queenside(color):
                if color == PieceColor.WHITE:
                    self.castling_rights.white_queen_side = False

                if color == PieceColor.BLACK:
                    self.castling_rights.black_queen_side = False


        if isinstance(piece, King):
            if color == PieceColor.WHITE:
                self.castling_rights.white_king_side = False
                self.castling_rights.white_queen_side = False

            elif color == PieceColor.BLACK:
                self.castling_rights.black_king_side = False
                self.castling_rights.black_queen_side = False

        dif = abs(from_y - to_y)
        if isinstance(piece, Pawn) and dif == 2:
            self.en_passant_target = (from_x, (from_y + to_y) / 2)

        else:
            self.en_passant_target = None





    def undo(self, move: MoveRecord):
        from_x, from_y = move.from_pos
        to_x, to_y = move.to_pos

        piece: Figure = move.piece


        self._board[from_y][from_x] = piece

        if move.captured_piece is None:
            self._board[to_y][to_x] = 0
        else:
            self._board[to_y][to_x] = move.captured_piece
            self._figures.append(move.captured_piece)

        piece.cord = move.from_pos

        self.castling_rights = move.prev_castling_rights
        self.en_passant_target = move.prev_en_passant


    def get_figure(self, *, cord):
        x, y = cord
        return self._board[y][x]


    def is_empty(self, x: int, y: int) -> bool:
        piece = self._board[y][x]
        return piece == 0


    def is_inside(self, x: int, y: int) -> bool:
        return 0 <= x < self.rows and 0 <= y < self.cols



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


    def __str__(self):
        text = ""
        for rows in self._board:
            for x in rows:
                text += f" {x} "
            text += "\n"
        return text



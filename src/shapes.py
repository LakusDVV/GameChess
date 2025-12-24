import raylibpy as rl

from src.enums import PieceColor
from src.chessboard import ChessBoard
from src.game import Move


class RenderComponent:
    def __init__(self, texture):
        self.texture = texture


    def draw(self, *, x, y, tile_size):
        rl.draw_texture(
            texture=self.texture,
            pos_x=x * tile_size,
            pos_y=y * tile_size,
            tint= rl.WHITE
        )



class Figure:

    _deltas = None

    def __init__(self, *, x: int, y: int, color, texture, tile_size=70):
        self.cord = (x, y)
        self.tile_size = tile_size

        self.color: PieceColor = color
        self.texture = texture
        self.renderer =  RenderComponent(texture)

        self.first_move = True
        self.direction = -1 if self.color == PieceColor.WHITE else 1



    def draw(self):
        x, y = self.cord
        self.renderer.draw(x=x, y=y, tile_size=self.tile_size)


    def get_moves(self, chessboard: ChessBoard) -> list:
        moves = []
        x, y = self.cord
        chessboard = chessboard
        board = chessboard.get_board()


        for dx, dy in self._deltas:

            nx, ny = x + dx, y + dy

            if not chessboard.is_inside(nx, ny):
                continue

            tx, ty = nx, ny
            while True:

                if not chessboard.is_inside(tx, ty):
                    break

                target: Figure = board[ty][ty]

                if target == 0:
                    moves.append(
                        Move(
                            piece=self,
                            from_pos=self.cord,
                            to_pos=(tx, ty),
                            special=None
                        )
                    )

                elif target.color != self.color:
                    moves.append(
                        Move(
                            piece=self,
                            from_pos=self.cord,
                            to_pos=(tx, ty),
                            special="capture"
                        )
                    )
                    break

                else:
                    break

                tx += dx
                ty += dy


        return moves




class Pawn(Figure):

    def get_moves(self, chessboard: ChessBoard):
        moves = []
        x, y = self.cord
        chessboard = chessboard
        board = chessboard.get_board()

        if chessboard.is_inside(x, y + self.direction):
            if chessboard.is_empty(y + self.direction, x):
                moves.append(
                    Move(
                        piece=self,
                        from_pos=self.cord,
                        to_pos=(x, y + self.direction),
                        special=None
                    )
                )

                # two moves forward, if the first move
                if self.first_move:
                    if chessboard.is_empty(x, y + 2 * self.direction):
                        moves.append(
                            moves.append(
                                Move(
                                    piece=self,
                                    from_pos=self.cord,
                                    to_pos=(x, y + 2 * self.direction),
                                    special=None
                                )
                            )
                        )

        for dx in (-1, 1):
            nx, ny = x + dx, y + self.direction
            if chessboard.is_inside(nx, ny):
                target = board[ny][nx]

                if target.color != self.color:
                    moves.append(
                        Move(
                            piece=self,
                            from_pos=self.cord,
                            to_pos=(nx, ny),
                            special="en_passant"
                        )
                    )


    def __str__(self):
        return "♙" if self.color == PieceColor.BLACK else "♟"



class King(Figure):

    _deltas = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

    def get_moves(self, chessboard: ChessBoard) -> list:
        moves = []
        x, y = self.cord
        chessboard = chessboard
        board = chessboard.get_board()


        for dx, dy in self._deltas:

            nx, ny = x + dx, y + dy

            if not chessboard.is_inside(nx, ny):
                continue

            target: Figure = board[ny][ny]

            if target == 0:
                moves.append(
                    Move(
                        piece=self,
                        from_pos=self.cord,
                        to_pos=(nx, ny),
                        special=None
                    )
                )

            elif target.color != self.color:
                moves.append(
                    Move(
                        piece=self,
                        from_pos=self.cord,
                        to_pos=(nx, ny),
                        special="capture"
                    )
                )



        rank: int = y

        # kingside castling
        if chessboard.castling_rights.can_castle_kingside(self.color):
            if (
                    chessboard.is_empty(5, rank) and
                    chessboard.is_empty(6, rank)
            ):
                moves.append(
                    Move(
                        piece=self,
                        from_pos=self.cord,
                        to_pos=(7, rank),
                        special="castle_kingside"
                    )
                )


        # queenside castling
        if chessboard.castling_rights.can_castle_queenside(self.color):
            if (
                    chessboard.is_empty(1, rank) and
                    chessboard.is_empty(2, rank) and
                    chessboard.is_empty(3, rank)
            ):
                moves.append(
                    Move(
                        piece=self,
                        from_pos=self.cord,
                        to_pos=(0, rank),
                        special="castle_queenside"
                    )
                )



        return moves



    def __str__(self):
        return "♚" if self.color == "white" else "♔"



class Queen(Figure):

    _deltas = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]


    def __str__(self):
        return "♛" if self.color == "white" else "♕"


class Rook(Figure):

    _deltas = [(-1, 0), (1, 0), (0, -1), (0, 1)]


    def __str__(self):
        return "♜" if self.color == "white" else "♖"


class Bishop(Figure):

    _deltas = [(-1, -1), (-1, 1), (1, -1), (1, 1)]


    def __str__(self):
        return "♝" if self.color == "white" else "♗"


class Knight(Figure):
    _deltas = [(-1, 2), (1, 2), (2, -1), (2, 1), (-1, -2), (1, -2), (-2, -1), (-2, 1)]


    def get_moves(self, chessboard: ChessBoard) -> list:
        moves = []
        x, y = self.cord
        chessboard = chessboard
        board = chessboard.get_board()

        for dx, dy in self._deltas:

            nx, ny = x + dx, y + dy

            if not chessboard.is_inside(nx, ny):
                continue

            target: Figure = board[ny][ny]

            if target == 0:
                moves.append(
                    Move(
                        piece=self,
                        from_pos=self.cord,
                        to_pos=(nx, ny),
                        special=None
                    )
                )

            elif target.color != self.color:
                moves.append(
                    Move(
                        piece=self,
                        from_pos=self.cord,
                        to_pos=(nx, ny),
                        special="capture"
                    )
                )

        return moves


    def __str__(self):
        return "♞" if self.color == "white" else "♘"

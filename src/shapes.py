from src.enums import PieceColor, MoveSpecial
from src.dataclass import Move
from src.render import RenderComponent

class Figure:

    _deltas = None


    def __init__(self, *, x: int, y: int, color: PieceColor, texture, tile_size=70):
        self.cord = (x, y)
        self.tile_size = tile_size

        self.color: PieceColor = color
        self.texture = texture
        self.renderer =  RenderComponent(texture)


        self.direction = 1 if self.color == PieceColor.WHITE else -1 # The bug,  because my board


    def draw(self):
        x, y = self.cord
        self.renderer.draw(x=x, y=y, tile_size=self.tile_size)


    def get_moves(self, *, chessboard) -> list[Move]:
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

                target: Figure = board[ty][tx]

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
                            special=MoveSpecial.CAPTURE
                        )
                    )
                    break

                else:
                    break

                tx += dx
                ty += dy


        return moves




class Pawn(Figure):

    def get_moves(self, chessboard):
        moves = []
        x, y = self.cord
        chessboard = chessboard
        board = chessboard.get_board()

        start_pos = 1 if self.color == PieceColor.WHITE else 6

        if chessboard.is_inside(x, y + self.direction):
            if chessboard.is_empty(x, y + self.direction):
                moves.append(
                    Move(
                        piece=self,
                        from_pos=self.cord,
                        to_pos=(x, y + self.direction),
                        special=None
                    )
                )

                # two moves forward, if the first move
                if y == start_pos:
                    if chessboard.is_empty(x, y + 2 * self.direction):

                        moves.append(
                            Move(
                                piece=self,
                                from_pos=self.cord,
                                to_pos=(x, y + 2 * self.direction),
                                special=None
                            )
                        )


        for dx in (-1, 1):
            nx, ny = x + dx, y + self.direction
            if chessboard.is_inside(nx, ny) and not chessboard.is_empty(nx, ny):

                target = board[ny][nx]



                if target.color != self.color:
                    moves.append(
                        Move(
                            piece=self,
                            from_pos=self.cord,
                            to_pos=(nx, ny),
                            special=MoveSpecial.CAPTURE
                        )
                    )
            if chessboard.en_passant_target == (nx, ny):

                moves.append(
                    Move(
                        piece=self,
                        from_pos=self.cord,
                        to_pos=(nx, ny),
                        special=MoveSpecial.EN_PASSANT
                    )
                )

        return moves


    def __str__(self):
        return "♙" if self.color == PieceColor.BLACK else "♟"



class King(Figure):

    _deltas = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]


    def get_moves(self, *, chessboard) -> list[Move]:
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
                        special=MoveSpecial.CAPTURE
                    )
                )



        rank = y

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
                        special=MoveSpecial.CASTLE_KINGSIDE
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
                        special=MoveSpecial.CASTLE_QUEENSIDE
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


    def get_moves(self, *, chessboard) -> list[Move]:
        moves = []
        x, y = self.cord
        chessboard = chessboard
        board = chessboard.get_board()

        for dx, dy in self._deltas:

            nx, ny = x + dx, y + dy

            if not chessboard.is_inside(nx, ny):
                continue

            target: Figure = board[ny][nx]

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
                        special=MoveSpecial.CAPTURE
                    )
                )

        return moves


    def __str__(self):
        return "♞" if self.color == "white" else "♘"

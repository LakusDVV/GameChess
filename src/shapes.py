import raylibpy as rl
from enum import Enum


class PieceColor(Enum):
    WHITE = 1,
    BLACK = 2


class Figure:
    def __init__(self, *, x: int, y: int, tile_size: int, chessboard, color, texture, rows: int=8, cols: int=8):
        self.cord = (x, y)
        self.tile_size = tile_size

        self.rows = rows
        self.cols = cols

        self.color = color
        self.texture = texture

        self.chessboard = chessboard

        self.first_move = True

    def in_bounds(self, x, y):
        return 0 <= x < self.rows and 0 <= y < self.cols


    def draw(self):
        x, y = self.cord

        rl.draw_texture(
            texture=self.texture,
            pos_x= x * self.tile_size,
            pos_y= y & self.tile_size,
            tint= rl.WHITE
        )



class Pawn(Figure):
    def get_moves(self):
        x, y = self.cord
        board = self.chessboard.get_board()

        moves = []
        direction = -1 if self.color == PieceColor.WHITE else 1

        # Pawn can be like 1 square if this square is empty
        if self.in_bounds(x, y + direction) and board[y + direction][x] == 0:
            moves.append((x, y + direction))

            # Pawn can be like 2 squares if this is it's first move
            if self.in_bounds(x, y + direction * 2) and board[y + direction * 2][x] == 0 and self.first_move:
                moves.append((x, y + direction * 2))


        for dx in (-1, 1):
            nx, ny = x + dx, y + direction
            if self.in_bounds(nx, ny):
                target = board[ny][nx]

                if target != 0 and target.color != self.color:
                    moves.append((nx, ny))

        return moves



    def __str__(self):
        return "♙" if self.color == PieceColor.BLACK else "♟"


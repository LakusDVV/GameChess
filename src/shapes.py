import raylibpy as rl
from enum import Enum





class RenderComponent:
    def __init__(self, texture):
        self.texture = texture


    def draw(self, *, x, y, tile_size):
        rl.draw_texture(
            texture=self.texture,
            pos_x=  x * tile_size,
            pos_y=  y * tile_size,
            tint=   rl.WHITE
        )


class PieceColor(Enum):
    WHITE = 1,
    BLACK = 2


class Figure:
    def __init__(self, *, x: int, y: int, color, texture, tile_size=70):
        self.cord = (x, y)
        self.tile_size = tile_size

        self.color = color
        self.texture = texture
        self.renderer =  RenderComponent(texture)

        self.first_move = True



    def draw(self):
        x, y = self.cord
        self.renderer.draw(x=x, y=y, tile_size=self.tile_size)



class Pawn(Figure):
    def get_moves(self):
        direction = -1 if self.color == PieceColor.WHITE else 1

        return direction



    def __str__(self):
        return "♙" if self.color == PieceColor.BLACK else "♟"


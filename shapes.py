import raylibpy as rl
from main import myChessboard, CK

tile_size = 70
class Figure:
    def __init__(self, *, texture, color, start_cord: str):
        self.texture = texture
        self.color = color
        self.cord = CK.get_cords_for_array(start_cord)
        myChessboard.redact_board_add(
            cord=self.cord,
            element=self
        )


    def draw(self):
        x, y = self.cord
        rl.draw_texture(self.texture, x * tile_size, y * tile_size, rl.WHITE)


    def move(self, new_cord):
        myChessboard.redact_board_move(
            new_cord=new_cord,
            cord=self.cord
        )
        self.cord = new_cord

        self.draw()







class Pawn(Figure):
    def __init__(self, *, texture, color,start_cord: str):
        super().__init__(
            texture=texture,
            color=color,
            start_cord=start_cord
        )


class King(Figure):
    def __init__(self, *, texture, color, start_cord):
        super().__init__(
            texture=texture,
            color=color,
            start_cord=start_cord
        )
